# 应用 SDK v0.1（桌面原型）

本文是当前可执行的接口契约。AI 生成应用时只使用本文已列出的 API；NFC、网络、音频和红外暂不可调用。目标 ESP32 SDK 尚未实现。

## 包结构

```text
sdcard/
  apps/
    my-app/
      manifest.json
      main.lua
  data/
    my-app/
      state.json       # 系统管理，应用不能直接访问文件
```

`manifest.json`：

```json
{
  "id": "my-app",
  "name": "我的应用",
  "version": "0.1.0",
  "api_version": 1,
  "entry": "main.lua",
  "permissions": ["storage"]
}
```

ID 与目录名一致，以小写字母开头，只用小写字母、数字、连字符，最多 48 字符。名称 1–40 字符。版本为三段数字。入口固定为 `main.lua`，最多 64 KiB。唯一可用权限为 `storage`；不需要保存数据时使用空数组。

## 生命周期

应用必须定义 `on_start()` 与 `on_key(key)`。加载顶层代码后调用 `on_start`；用户按键时调用 `on_key`。回调须快速返回，不写常驻循环、不等待输入、不休眠。没有定时器和后台任务 API。

四个实体按钮为上、下、确认、电源。应用的 `key` 仅为 `up`、`down` 或 `ok`。模拟器的 `hold-ok`（别名 `home`）表示长按确认，由系统直接结束应用，不能拦截，也不触发短按确认。实际按压时长、去抖和电源控制尚未实现；电源键不开放给应用。

退出、切换、异常或超时都会销毁该应用虚拟机，未保存的局部变量丢失。每次启动都是全新 VM。退出回调尚未实现。

## 已实现 API

| API | 行为 |
| --- | --- |
| `passport.ui.clear()` | 清空本帧标题和正文 |
| `passport.ui.title(text)` | 设置标题，最多 80 字符 |
| `passport.ui.text(text)` | 追加一行，最多 256 字符；最多 24 行 |
| `passport.storage.get(key)` | 读取本应用字符串值，不存在返回 `nil` |
| `passport.storage.set(key, value)` | 设置本应用字符串值，需声明 `storage` |
| `passport.system.exit()` | 请求退出，在当前回调返回后生效 |

显示在回调结束后更新。上述显示为文字模型，不承诺真实屏幕坐标、字体、像素和性能。存储只接收字符串；数字用 `tostring` 和 `tonumber` 转换。

数据键以小写字母开头，只用小写字母、数字和下划线，最多 40 字符。最多 32 个键，每值最多 1024 字符，序列化后总量最多 16 KiB。数据在成功回调后通过临时文件替换写入；失败回调的更新不提交。不提供断电持久性保证，ESP32 的 SD 文件系统仍需单独验证。

可用基础语言和 `string`、`table`、`math`、`utf8` 库。不提供 `io`、`os`、`debug`、`package`、`require`、`load`、`loadfile`、`dofile`、`print`、`collectgarbage` 或 JavaScript 桥接。

## 最小应用

```lua
function on_start()
  passport.ui.clear()
  passport.ui.title("你好")
  passport.ui.text("长按确认返回桌面")
end

function on_key(key)
  if key == "ok" then
    passport.system.exit()
    return
  end
end
```

## 给 AI 的提示词模板

> 为 Ruri Passport SDK v0.1 写一个 Lua 5.3 应用，功能为【填写需求】。严格按照随附 APP_SDK.md，只使用已实现 API。输出 manifest.json 和 main.lua，保证两个生命周期回调都存在、每次回调快速返回，只使用上、下、确认三种应用按键，保留系统长按确认回桌面行为。存储只用字符串并声明权限。不要生成硬件驱动或固件，不要假设网络、计时器或图形 API 已存在。附上在模拟器中的逐步验收操作。

## 验证

`npm run check -- <SD目录>` 会检查包并执行启动回调；`npm start -- <SD目录>` 用于交互验证。检查启动成功不代表所有分支都正确，需覆盖按键、退出和再次进入的数据行为。
