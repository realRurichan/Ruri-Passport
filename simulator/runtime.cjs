'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { Worker } = require('node:worker_threads');
const { discover, readApp } = require('./catalog.cjs');

class Runtime {
  constructor(root, { timeout = 1500 } = {}) {
    this.root = path.resolve(root); this.timeout = timeout;
    this.worker = null; this.active = null; this.error = null; this.screen = null;
    this.seq = 0; this.pending = new Map(); this.queue = Promise.resolve();
  }
  state() { return { ...discover(this.root), active: this.active, screen: this.screen, error: this.error }; }
  // Serialize input so a delayed old callback cannot overwrite a newly opened app.
  action(fn) {
    const result = this.queue.then(fn);
    this.queue = result.catch(() => {});
    return result;
  }
  async stop() {
    const worker = this.worker; this.worker = null;
    for (const p of this.pending.values()) { clearTimeout(p.timer); p.reject(Error('应用已停止')); }
    this.pending.clear(); this.active = null; this.screen = null;
    if (worker) await worker.terminate();
  }
  dataFile(id) {
    const base = path.join(this.root, 'data');
    fs.mkdirSync(base, { recursive: true });
    if (fs.lstatSync(base).isSymbolicLink()) throw Error('data 不允许符号链接');
    const dir = path.join(base, id);
    fs.mkdirSync(dir, { recursive: true });
    if (fs.lstatSync(dir).isSymbolicLink()) throw Error('应用数据目录不允许符号链接');
    return path.join(dir, 'state.json');
  }
  load(id) {
    const file = this.dataFile(id);
    if (!fs.existsSync(file)) return {};
    if (fs.lstatSync(file).isSymbolicLink() || fs.statSync(file).size > 16384) throw Error('数据文件类型或大小错误');
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (!data || typeof data !== 'object' || Array.isArray(data) || Object.keys(data).length > 32 || Object.entries(data).some(([k,v]) => !/^[a-z][a-z0-9_]{0,39}$/.test(k) || typeof v !== 'string' || v.length > 1024)) throw Error('应用数据损坏');
    return data;
  }
  save(id, data) {
    const file = this.dataFile(id), temp = `${file}.${process.pid}.${this.seq}.tmp`;
    try { fs.writeFileSync(temp, JSON.stringify(data), { flag: 'wx' }); fs.renameSync(temp, file); }
    finally { if (fs.existsSync(temp)) fs.unlinkSync(temp); }
  }
  request(method, key) {
    const seq = ++this.seq;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { this.pending.delete(seq); reject(Error('应用超时，已返回桌面')); }, this.timeout);
      this.pending.set(seq, { resolve, reject, timer });
      this.worker.postMessage({ seq, method, key });
    });
  }
  async apply(result) {
    if (result.error) throw Error(result.error);
    if (this.active.permissions.includes('storage')) this.save(this.active.id, result.data);
    this.screen = result.screen;
    if (result.exit) await this.stop();
  }
  start(id) { return this.action(async () => {
    await this.stop(); this.error = null;
    try {
      const app = readApp(this.root, id);
      this.active = app.manifest;
      const data = app.manifest.permissions.includes('storage') ? this.load(id) : {};
      const worker = this.worker = new Worker(path.join(__dirname, 'worker.cjs'), {
        workerData: { ...app, data }, resourceLimits: { maxOldGenerationSizeMb: 32, maxYoungGenerationSizeMb: 8, stackSizeMb: 2 }
      });
      await new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(Error('应用启动超时')), this.timeout);
        const fail = e => {
          clearTimeout(timer); reject(e);
          for (const p of this.pending.values()) { clearTimeout(p.timer); p.reject(e); }
          this.pending.clear();
          if (this.worker === worker) { this.error = e.message; this.worker = null; this.active = null; this.screen = null; }
        };
        worker.on('error', fail);
        worker.on('exit', code => { if (this.worker === worker) fail(Error(`应用进程退出 (${code})`)); });
        worker.on('message', message => {
          if (message.ready) { clearTimeout(timer); resolve(); return; }
          if (message.seq === undefined) { clearTimeout(timer); reject(Error(message.error)); return; }
          const p = this.pending.get(message.seq);
          if (p) { clearTimeout(p.timer); this.pending.delete(message.seq); p.resolve(message); }
        });
      });
      await this.apply(await this.request('on_start'));
    } catch (e) { await this.stop(); this.error = e.message; }
    return this.state();
  }); }
  key(key) { return this.action(async () => {
    if (key === 'home' || key === 'hold-ok') { await this.stop(); this.error = null; return this.state(); }
    if (!['up','down','ok'].includes(key)) throw Error('未知按键');
    if (!this.worker) return this.state();
    try { await this.apply(await this.request('on_key', key)); }
    catch (e) { await this.stop(); this.error = e.message; }
    return this.state();
  }); }
}
module.exports = { Runtime };
