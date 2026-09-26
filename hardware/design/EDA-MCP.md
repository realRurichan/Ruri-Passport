# 本机 EasyEDA MCP 配置记录

2026-09-26：已安装并实际读回工程标签页。

- Skill：daishuge/pcb-skill，提交 `6e939b64907e3c63236c7522c511af5d7d1afaad`。
- Skill 推荐的 sheares/easyeda-mcp-fix 仓库返回 404；采用 javawizard/easyeda-agent-mcp-server，提交 `3b8f2e59e39828614a8f389610224b2c0f43c5d5`。不声称具备不可取得分支的全部修复。
- EasyEDA Agent 扩展 v1.1.5，UUID `0d3d35b927d9451ba42c527576079161`。
- 本机安装目录：`~/.local/share/ruri-easyeda-mcp/`；Codex MCP 名称 `easyeda-agent`，stdio。
- EDA 4.1.60 半离线模式；用户已明确授权第三方扩展安装及联网/本地文件访问权限。已启用外部交互、顶部菜单，自动更新保持关闭。
- 源码测试：48/48 通过。打包工具缺少 build/dist 时需先创建该目录。
- 实测 `server_info`：extensionConnected=true，工程 Ruri-Passport-RevA，本机 WS 127.0.0.1:16168，allowAllOrigins=false。
- 实测 `editor_get_open_tabs`：Display.Mainboard、Core.Mainboard、Mainboard。验证没有修改电路。

扩展菜单仍叫 Claude，这是上游命名，连接的服务也可供 Codex 使用。连接器工具是否已在当前 Codex 会话加载，必须单独核实，不能以配置文件存在代替。服务无客户端时会退出；下次 MCP 调用自动启动，扩展需要重连。

对设计写入前先导出备份，写入后读回网表验证。连接通过并不表示电路、封装或布线已验证。
