'use strict';
const path = require('node:path');
const readline = require('node:readline/promises');
const { Runtime } = require('./runtime.cjs');
const runtime = new Runtime(path.resolve(process.argv[2] || 'sdcard'));
function render(state) {
  console.log('\n=== Ruri Passport · 桌面模拟器 ===');
  if (state.error) console.log(`应用错误：${state.error}`);
  if (state.active) console.log(`[${state.active.name}]\n${state.screen?.title || ''}\n${state.screen?.lines.join('\n') || ''}`);
  else {
    for (const app of state.apps) console.log(`${app.id} — ${app.name}`);
    if (!state.apps.length) console.log('没有应用；检查 SD 卡目录。');
    for (const e of state.errors) console.log(`忽略 ${e.id}：${e.error}`);
  }
  console.log('命令：open <id> / up down ok / hold-ok（长按确认）/ home / list / quit');
}
async function main() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  render(runtime.state());
  try {
    for await (const line of rl) {
      const command = line.trim();
      if (command === 'quit') break;
      try {
        if (command.startsWith('open ')) render(await runtime.start(command.slice(5)));
        else if (command === 'list') render(runtime.state());
        else render(await runtime.key(command));
      } catch (e) { console.log(e.message); }
    }
  } finally { rl.close(); await runtime.stop(); }
}
main().catch(e => { console.error(e); process.exitCode = 1; });
