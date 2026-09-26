local page = 1
local function draw()
  passport.ui.clear()
  passport.ui.title("RURI / PASSPORT")
  if page == 1 then
    passport.ui.text("你好，我是 Ruri")
    passport.ui.text("用 AI 创作自己的掌上应用")
  else
    passport.ui.text("这是从 SD 卡加载的 Lua 应用")
    passport.ui.text("无需重刷系统即可切换应用")
  end
  passport.ui.text("上/下/确认：翻页 · 长按确认：桌面")
end
function on_start() draw() end
function on_key(key)
  if key == "up" or key == "down" or key == "ok" then
    page = 3 - page
    draw()
  end
end
