'use strict';
const fs = require('node:fs');
const path = require('node:path');
const ID = /^[a-z][a-z0-9-]{0,47}$/;
const MAX_SOURCE = 64 * 1024;

function regularFile(file, max) {
  const stat = fs.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.size > max) throw Error('文件类型或大小不符合要求');
  return fs.readFileSync(file, 'utf8');
}

function readApp(root, id) {
  if (!ID.test(id)) throw Error('无效应用 ID');
  const dir = path.join(root, 'apps', id);
  if (!fs.lstatSync(dir).isDirectory() || fs.lstatSync(dir).isSymbolicLink()) throw Error('应用必须为真实目录');
  const manifest = JSON.parse(regularFile(path.join(dir, 'manifest.json'), 4096));
  if (manifest.id !== id) throw Error('应用 ID 与目录不一致');
  if (typeof manifest.name !== 'string' || !manifest.name.trim() || manifest.name.length > 40) throw Error('名称须为 1–40 个字符');
  if (typeof manifest.version !== 'string' || !/^\d+\.\d+\.\d+$/.test(manifest.version)) throw Error('version 须为 x.y.z');
  if (manifest.api_version !== 1 || manifest.entry !== 'main.lua') throw Error('仅支持 API 1 与 main.lua 入口');
  if (!Array.isArray(manifest.permissions) || manifest.permissions.some(p => p !== 'storage')) throw Error('当前只实现 storage 权限');
  const source = regularFile(path.join(dir, 'main.lua'), MAX_SOURCE);
  return { manifest, source };
}

function discover(root) {
  const apps = [], errors = [];
  let entries;
  try { entries = fs.readdirSync(path.join(root, 'apps'), { withFileTypes: true }); }
  catch (e) { if (e.code === 'ENOENT') return { apps, errors }; throw e; }
  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
    try { apps.push(readApp(root, entry.name).manifest); }
    catch (e) { errors.push({ id: entry.name, error: e.message }); }
  }
  return { apps, errors };
}
module.exports = { readApp, discover, ID };
