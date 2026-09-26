'use strict';
const path = require('node:path');
const { Runtime } = require('./runtime.cjs');
const runtime = new Runtime(path.resolve(process.argv[2] || 'sdcard'));
(async () => {
  const catalog = runtime.state();
  for (const e of catalog.errors) console.error(`${e.id}: ${e.error}`);
  let failed = catalog.errors.length;
  for (const app of catalog.apps) {
    const state = await runtime.start(app.id);
    console.log(`${state.error ? 'FAIL' : 'PASS'} ${app.id}${state.error ? ': ' + state.error : ''}`);
    if (state.error) failed++;
  }
  await runtime.stop();
  if (!catalog.apps.length) { console.error('未找到有效应用'); failed++; }
  process.exitCode = failed ? 1 : 0;
})().catch(e => { console.error(e); process.exitCode = 1; });
