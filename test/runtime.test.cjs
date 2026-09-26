'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { Runtime } = require('../simulator/runtime.cjs');

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'passport-'));
  fs.cpSync(path.join(__dirname, '../sdcard/apps'), path.join(root, 'apps'), { recursive: true });
  const runtime = new Runtime(root, { timeout: 1000 });
  t.after(async () => { await runtime.stop(); fs.rmSync(root, { recursive: true, force: true }); });
  return { root, runtime };
}
function app(root, id, source, permissions = []) {
  const dir = path.join(root, 'apps', id);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'manifest.json'), JSON.stringify({ id, name: id, version: '0.1.0', api_version: 1, entry: 'main.lua', permissions }));
  fs.writeFileSync(path.join(dir, 'main.lua'), source);
}
test('switch apps; persisted count survives a new runtime', async t => {
  const { root, runtime } = fixture(t);
  assert.equal(runtime.state().apps.length, 2);
  assert.equal((await runtime.start('counter')).error, null);
  assert.match((await runtime.key('up')).screen.lines[0], /1$/);
  assert.equal((await runtime.start('badge')).active.id, 'badge');
  assert.equal((await runtime.key('hold-ok')).active, null);
  const second = new Runtime(root);
  t.after(() => second.stop());
  assert.match((await second.start('counter')).screen.lines[0], /1$/);
});
test('storage belongs to each application', async t => {
  const { root, runtime } = fixture(t);
  const source = fs.readFileSync(path.join(root, 'apps/counter/main.lua'), 'utf8');
  app(root, 'other-counter', source, ['storage']);
  await runtime.start('counter'); await runtime.key('up');
  assert.match((await runtime.start('other-counter')).screen.lines[0], /0$/);
});
test('no card still boots to empty launcher', async t => {
  const { root, runtime } = fixture(t);
  fs.rmSync(root, { recursive: true });
  assert.deepEqual(runtime.state().apps, []);
  assert.equal((await runtime.key('home')).active, null);
});
test('bad manifest does not hide valid apps; traversal rejected', async t => {
  const { root, runtime } = fixture(t);
  app(root, 'broken', '');
  fs.writeFileSync(path.join(root, 'apps/broken/manifest.json'), '{');
  assert.equal(runtime.state().apps.length, 2);
  assert.equal(runtime.state().errors.length, 1);
  assert.match((await runtime.start('../counter')).error, /ID/);
});
test('syntax and callback errors return to launcher', async t => {
  const { root, runtime } = fixture(t);
  app(root, 'bad-syntax', 'this is not lua');
  assert.ok((await runtime.start('bad-syntax')).error);
  app(root, 'crash', 'function on_start() end function on_key(k) error("intentional") end');
  await runtime.start('crash');
  const state = await runtime.key('up');
  assert.equal(state.active, null); assert.match(state.error, /intentional/);
  assert.equal((await runtime.start('badge')).error, null);
});
test('infinite callback and infinite startup are terminated', async t => {
  const { root, runtime } = fixture(t);
  app(root, 'hang', 'function on_start() end function on_key(k) while true do end end');
  await runtime.start('hang');
  assert.match((await runtime.key('up')).error, /超时/);
  app(root, 'hang-start', 'while true do end');
  assert.match((await runtime.start('hang-start')).error, /超时/);
  assert.equal((await runtime.start('badge')).active.id, 'badge');
});
test('storage permission and unsafe standard libraries are unavailable', async t => {
  const { root, runtime } = fixture(t);
  app(root, 'permissions', 'function on_start() passport.storage.set("x", "1") end function on_key(k) end');
  assert.match((await runtime.start('permissions')).error, /storage/);
  app(root, 'libraries', 'function on_start() assert(io == nil and os == nil and debug == nil and package == nil and require == nil and load == nil) end function on_key(k) end');
  assert.equal((await runtime.start('libraries')).error, null);
});
test('reject app and data symlinks', async t => {
  const { root, runtime } = fixture(t);
  fs.symlinkSync(path.join(root, 'apps/badge'), path.join(root, 'apps/linked'));
  assert.ok(runtime.state().errors.some(e => e.id === 'linked'));
  fs.mkdirSync(path.join(root, 'data'));
  fs.symlinkSync(path.join(root, 'apps/badge'), path.join(root, 'data/counter'));
  assert.match((await runtime.start('counter')).error, /符号链接/);
});
test('corrupt data reports an error rather than silently erasing it', async t => {
  const { root, runtime } = fixture(t);
  await runtime.start('counter'); await runtime.key('home');
  fs.writeFileSync(path.join(root, 'data/counter/state.json'), '{broken');
  assert.ok((await runtime.start('counter')).error);
  assert.equal(fs.readFileSync(path.join(root, 'data/counter/state.json'), 'utf8'), '{broken');
});
test('queued switches and keys act on the intended foreground app', async t => {
  const { runtime } = fixture(t);
  await Promise.all([runtime.start('counter'), runtime.key('up'), runtime.start('badge'), runtime.key('home')]);
  assert.equal(runtime.state().active, null);
  assert.match((await runtime.start('counter')).screen.lines[0], /1$/);
});
