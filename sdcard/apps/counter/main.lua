local count = 0
local function draw()
  passport.ui.clear()
  passport.ui.title("随身计数器")
  passport.ui.text("当前计数：" .. tostring(count))
  passport.ui.text("上 +1 · 下 -1 · 确认 清零")
  passport.ui.text("长按确认返回桌面，计数自动保存")
end
function on_start()
  count = tonumber(passport.storage.get("count")) or 0
  draw()
end
function on_key(key)
  if key == "up" then count = count + 1
  elseif key == "down" then count = count - 1
  elseif key == "ok" then count = 0 end
  passport.storage.set("count", tostring(count))
  draw()
end
