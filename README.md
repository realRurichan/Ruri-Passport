# Ruri Passport

让用户用 AI 创作掌上应用，把多个应用放进 SD 卡，在设备上启动和切换。

**状态：早期原型。当前可运行的是电脑端 Lua 应用模拟器，不是 ESP32 固件；尚无可生产的原理图、PCB、BOM 或 Gerber。**

本项目受 [FoloToy AI Passport](https://ai-passport.folotoy.cn/) 启发，为独立项目，与 FoloToy 无隶属关系。没有复制其固件或硬件文件，不承诺兼容其社区固件。

## 当前实现

- 从 `sdcard/apps/<id>/` 发现并校验应用包。
- 实际执行 Lua 5.3 应用，提供文字界面、按键、退出与独立存储 API。
- 单前台应用；切换时销毁旧虚拟机，超时或运行错误后回到启动器。
- 示例：电子身份卡、随身计数器。
- 应用隔离、坏包、超时、存储与切换测试。

## 快速开始

需要 Node.js 20 或更新版本。

```sh
npm ci
npm test
npm run check
npm start
```

在模拟器里逐行输入：

```text
open counter
up
hold-ok
open badge
down
hold-ok
open counter
quit
```

计数器的数值会保留。运行数据位于 `sdcard/data/`，已排除在 Git 之外。也可使用 `npm start -- /path/to/sdcard` 指定另一个目录。

## 用 AI 写应用

把 [应用 SDK 文档](docs/APP_SDK.md) 和一个示例交给 AI，描述要实现的功能。生成 `manifest.json` 和 `main.lua`，放入独立的应用目录，然后运行 `npm run check`，再到模拟器里验证操作。

当前安装方式是复制应用目录。压缩包安装、图形界面、设备传输、应用商店与在线下载尚未实现。NFC、红外、音频、Wi-Fi 和 BLE 的应用 API 也尚未实现。

## 目标硬件

| 部分 | 目标 |
| --- | --- |
| 主控 | ESP32-S3，候选 16 MB Flash + 8 MB PSRAM |
| 外形 | 约 125 × 88 mm，待机械验证 |
| 屏幕 | 接近银行卡显示面积，彩色非触摸 |
| 无线 | 2.4 GHz Wi-Fi、BLE 手机通信 |
| 外设 | NFC 标签读写、红外收发、扬声器、麦克风、microSD |
| 按钮 | 上、下、确认、电源；长按确认返回桌面（交互草案） |
| 供电 | USB-C、可充电电池 |
| 制造 | 嘉立创 PCB 与 SMT，单套目标预算约 ¥200，尚未核价 |

详见 [硬件方案](HARDWARE_PLAN.md)。屏幕选型、GPIO、NFC 调谐、电源预算、实际报价和实机可靠性仍需验证。

## 原型边界

桌面使用 [Fengari](https://github.com/fengari-lua/fengari) 执行 Lua。每个应用在可终止的 Node Worker 中运行，设有时间与 JS 堆上限。这不是硬件内存预算，也不是经过安全审计的沙箱。不要将模拟器当成运行未知恶意代码的安全环境。未来 ESP32 版本需要独立实现内存配额、调度、硬件驱动和恢复机制。

`npm run check` 会执行应用的启动回调，因此可能写入该应用的本地数据；它不是纯静态检查。应用源文件上限 64 KiB，不加载 Lua 二进制字节码。

## 路线

1. 桌面应用协议与两个应用切换验证（已实现）。
2. 确认屏幕、采购型号、GPIO 和整机成本。
3. 用现成 ESP32-S3 开发板验证 Lua、显示、SD 卡与恢复流程。
4. 原理图、PCB、制造检查与首批样机测试。
5. 增加外设 SDK、图形组件和应用安装工具。

## 持续集成

[GitHub Actions 配置模板](docs/github-actions-test.yml) 已提供，但尚未启用。发布时的凭据缺少 `workflow` 权限，因此未提交到 `.github/workflows/`；有相应权限的维护者可将模板移入该目录。本地测试不受影响。

## 参与与许可

欢迎提交问题和改进，见 [贡献说明](CONTRIBUTING.md)。原创代码与文档采用 [MIT 许可证](LICENSE)。第三方组件保留各自许可证；外部参考链接中的内容不包含在本项目授权内。
