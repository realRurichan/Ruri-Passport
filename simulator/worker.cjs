'use strict';
// One disposable Lua VM per foreground app. No filesystem/network bindings in Lua.
const { parentPort, workerData } = require('node:worker_threads');
const { lua, lauxlib: aux, lualib: lib, to_luastring: str, to_jsstring: js } = require('fengari');
const L = aux.luaL_newstate();
let screen = { title: '', lines: [] }, exitRequested = false;
let data = Object.assign(Object.create(null), workerData.data);
const hasStorage = workerData.manifest.permissions.includes('storage');
const textArg = (index, max = 256) => {
  const result = js(aux.luaL_checkstring(L, index));
  if (result.length > max) aux.luaL_error(L, str('字符串超过长度限制'));
  return result;
};
const keyArg = () => {
  const key = textArg(1, 40);
  if (!/^[a-z][a-z0-9_]{0,39}$/.test(key)) aux.luaL_error(L, str('无效数据键'));
  return key;
};
function bind(name, fn) { lua.lua_pushcfunction(L, fn); lua.lua_setfield(L, -2, str(name)); }
function table(name, methods) {
  lua.lua_newtable(L);
  for (const [key, fn] of Object.entries(methods)) bind(key, fn);
  lua.lua_setfield(L, -2, str(name));
}
function run(source) {
  if (aux.luaL_loadbufferx(L, str(source), null, str('@main.lua'), str('t')) !== lua.LUA_OK || lua.lua_pcall(L, 0, 0, 0) !== lua.LUA_OK) {
    throw Error(js(lua.lua_tostring(L, -1)));
  }
}
try {
  for (const [name, open] of [['_G', lib.luaopen_base], ['string', lib.luaopen_string], ['table', lib.luaopen_table], ['math', lib.luaopen_math], ['utf8', lib.luaopen_utf8]]) {
    aux.luaL_requiref(L, str(name), open, 1); lua.lua_pop(L, 1);
  }
  for (const name of ['dofile', 'loadfile', 'load', 'collectgarbage', 'print']) {
    lua.lua_pushnil(L); lua.lua_setglobal(L, str(name));
  }
  lua.lua_newtable(L);
  table('ui', {
    clear: () => { screen = { title: '', lines: [] }; return 0; },
    title: () => { screen.title = textArg(1, 80); return 0; },
    text: () => {
      if (screen.lines.length >= 24) return aux.luaL_error(L, str('屏幕最多 24 行'));
      screen.lines.push(textArg(1)); return 0;
    }
  });
  table('storage', {
    get: () => {
      if (!hasStorage) return aux.luaL_error(L, str('未声明 storage 权限'));
      const value = data[keyArg()];
      if (value === undefined) lua.lua_pushnil(L); else lua.lua_pushstring(L, str(value));
      return 1;
    },
    set: () => {
      if (!hasStorage) return aux.luaL_error(L, str('未声明 storage 权限'));
      const key = keyArg(), value = textArg(2, 1024);
      const next = { ...data, [key]: value };
      if (Object.keys(next).length > 32 || Buffer.byteLength(JSON.stringify(next)) > 16384) return aux.luaL_error(L, str('应用存储配额已满'));
      data = next; return 0;
    }
  });
  table('system', { exit: () => { exitRequested = true; return 0; } });
  lua.lua_setglobal(L, str('passport'));
  run(workerData.source);
  for (const name of ['on_start', 'on_key']) {
    lua.lua_getglobal(L, str(name));
    if (!lua.lua_isfunction(L, -1)) throw Error(`缺少 ${name} 回调`);
    lua.lua_pop(L, 1);
  }
  parentPort.on('message', ({ seq, method, key }) => {
    try {
      lua.lua_getglobal(L, str(method));
      if (key !== undefined) lua.lua_pushstring(L, str(key));
      if (lua.lua_pcall(L, key === undefined ? 0 : 1, 0, 0) !== lua.LUA_OK) throw Error(js(lua.lua_tostring(L, -1)));
      parentPort.postMessage({ seq, screen, data, exit: exitRequested });
    } catch (e) { parentPort.postMessage({ seq, error: e.message }); }
  });
  parentPort.postMessage({ ready: true });
} catch (e) { parentPort.postMessage({ error: e.message }); }
