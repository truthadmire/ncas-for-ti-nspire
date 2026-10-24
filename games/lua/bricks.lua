platform.apiLevel = '2.0'
-- Bricks: bat-and-ball brick breaker for the TI-Nspire CX II (Lua). Paste
-- into a Script Editor page. Left/right (4 6) push the bat: each press
-- speeds it up and it glides to a stop, so tap or hold. Enter (8, 5, up)
-- serves, Enter or Esc pauses, Esc in the pause goes back to the title.

local TICK = 0.05
local LEFT, RIGHT, TOP = 2, 316, 15
local BX0, BY0, BW, BH = 4, 30, 30, 9      -- first brick, brick size
local PY, PH = 196, 5                      -- bat top and height
local PW = 44
local BALL = 4
local PUSH, PMAX, GLIDE = 5, 9, 0.82
local MAXANG = 1.05                        -- 60 degrees from straight up

-- one string per row, 10 bricks: 1-3 = hits needed, # = never breaks
local LAYOUTS = {
  {'3333333333', '2222222222', '2222222222', '1111111111', '1111111111'},
  {'..333333..', '.22222222.', '1111111111', '1#1#11#1#1', '1111111111', '.22222222.'},
  {'3.3.3.3.3.', '.2.2.2.2.2', '1.1.1.1.1.', '.1.1.1.1.1', '2.2.2.2.2.', '.3.3.3.3.3'},
  {'1........1', '21......12', '321....123', '#321..123#', '3321111233', '2222222222', '1111111111'},
}

local BG = {16, 20, 32}
local TEXT = {235, 235, 235}
local DIM = {150, 160, 175}
local GOLD = {250, 200, 40}
local BAT = {220, 225, 235}
local HP = {{90, 200, 110}, {240, 170, 50}, {230, 70, 70}}
local STEEL = {120, 125, 140}

G = {state = 'title', score = 0, best = 0, lives = 3, level = 1, bricks = {},
     left = 0, px = 159, pv = 0, x = 0, y = 0, vx = 0, vy = 0, speed = 0,
     wait = 0, record = false}

local function color(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end

local function font(gc, size, st) gc:setFont('sansserif', st or 'r', size) end

local function centre(gc, s, y)
  gc:drawString(s, math.floor((318 - gc:getStringWidth(s)) / 2), y, 'top')
end

local function loadbest()
  local ok, v = pcall(var.recall, 'brkbest')
  G.best = (ok and type(v) == 'number') and v or 0
end

local function savebest()
  pcall(var.store, 'brkbest', G.best)
  pcall(document.markChanged)
end

local function build()
  local rows = LAYOUTS[(G.level - 1) % #LAYOUTS + 1]
  G.bricks, G.left = {}, 0
  for r = 1, #rows do
    G.bricks[r] = {}
    for c = 1, 10 do
      local ch = string.sub(rows[r], c, c)
      local v = 0
      if ch == '#' then
        v = -1
      elseif ch ~= '.' then
        v = tonumber(ch)
        G.left = G.left + 1
      end
      G.bricks[r][c] = v
    end
  end
end

-- ball sits on the bat until served
local function serve()
  G.state = 'serve'
  G.x = G.px - BALL / 2
  G.y = PY - BALL
  G.vx, G.vy = 0, 0
end

local function start()
  math.randomseed(timer.getMilliSecCounter())
  G.score, G.lives, G.level, G.record = 0, 3, 1, false
  G.px, G.pv = 159, 0
  loadbest()
  build()
  serve()
end

local function launch()
  G.speed = math.min(2.6 + (G.level - 1) * 0.3, 4.2)
  local a = (math.random() - 0.5) * 0.8
  G.vx, G.vy = G.speed * math.sin(a), -G.speed * math.cos(a)
  G.state = 'play'
end

local function finish()
  if G.score > G.best then
    G.best = G.score
    G.record = true
    savebest()
  end
  G.state = 'over'
end

-- the brick under point (x, y): row, column
local function brickat(x, y)
  local c = math.floor((x - BX0) / (BW + 1)) + 1
  local r = math.floor((y - BY0) / (BH + 2)) + 1
  if r < 1 or c < 1 or c > 10 or not G.bricks[r] then return nil end
  -- the 1-pixel gaps between bricks are empty
  if x - BX0 - (c - 1) * (BW + 1) >= BW or y - BY0 - (r - 1) * (BH + 2) >= BH then return nil end
  if G.bricks[r][c] == 0 then return nil end
  return r, c
end

-- does the ball at (x, y) hit a brick? hits the first one found
local function hitbrick(x, y)
  local pts = {x, y, x + BALL - 1, y, x, y + BALL - 1, x + BALL - 1, y + BALL - 1}
  for i = 1, 8, 2 do
    local r, c = brickat(pts[i], pts[i + 1])
    if r then
      local v = G.bricks[r][c]
      if v > 0 then
        G.bricks[r][c] = v - 1
        G.score = G.score + 10
        if v == 1 then
          G.left = G.left - 1
          G.score = G.score + 10 * G.level
        end
      end
      return true
    end
  end
  return false
end

local function bat(x)
  local off = (x + BALL / 2 - G.px) / (PW / 2)
  if off < -1 then off = -1 end
  if off > 1 then off = 1 end
  G.speed = math.min(G.speed + 0.08, 5)
  local a = off * MAXANG
  G.vx, G.vy = G.speed * math.sin(a), -G.speed * math.cos(a)
end

local function moveball()
  local n = math.ceil(G.speed / 2)
  for _ = 1, n do
    local x = G.x + G.vx / n
    if x < LEFT or x + BALL > RIGHT or hitbrick(x, G.y) then
      G.vx = -G.vx
    else
      G.x = x
    end
    local y = G.y + G.vy / n
    if y < TOP or hitbrick(G.x, y) then
      G.vy = -G.vy
    elseif G.vy > 0 and G.y + BALL <= PY and y + BALL > PY
           and G.x + BALL > G.px - PW / 2 and G.x < G.px + PW / 2 then
      G.y = PY - BALL
      bat(G.x)
    else
      G.y = y
    end
    if G.left == 0 then return end
  end
end

local function movebat()
  G.px = G.px + G.pv
  G.pv = G.pv * GLIDE
  if math.abs(G.pv) < 0.3 then G.pv = 0 end
  if G.px < LEFT + PW / 2 then G.px, G.pv = LEFT + PW / 2, 0 end
  if G.px > RIGHT - PW / 2 then G.px, G.pv = RIGHT - PW / 2, 0 end
end

function on.timer()
  local s = G.state
  if s == 'serve' or s == 'play' then
    movebat()
    if s == 'serve' then
      G.x = G.px - BALL / 2
    else
      moveball()
      if G.left == 0 then
        G.state, G.wait = 'clear', 30
      elseif G.y > 212 then
        G.lives = G.lives - 1
        if G.lives <= 0 then finish() else serve() end
      end
    end
    platform.window:invalidate()
  elseif s == 'clear' then
    G.wait = G.wait - 1
    if G.wait <= 0 then
      G.level = G.level + 1
      build()
      serve()
    end
    platform.window:invalidate()
  end
end

local function push(d)
  if G.state ~= 'play' and G.state ~= 'serve' then return end
  if G.pv * d > 0 then
    G.pv = G.pv + d * PUSH
  else
    G.pv = d * PUSH
  end
  if math.abs(G.pv) > PMAX then G.pv = d * PMAX end
end

function on.arrowKey(k)
  if k == 'left' then
    push(-1)
  elseif k == 'right' then
    push(1)
  elseif k == 'up' and G.state == 'serve' then
    launch()
  end
  platform.window:invalidate()
end

function on.enterKey()
  local s = G.state
  if s == 'title' or s == 'over' then
    start()
  elseif s == 'serve' then
    launch()
  elseif s == 'play' then
    G.state = 'pause'
  elseif s == 'pause' then
    G.state = G.vy == 0 and 'serve' or 'play'
  end
  platform.window:invalidate()
end

function on.charIn(ch)
  if ch == '4' then
    on.arrowKey('left')
  elseif ch == '6' then
    on.arrowKey('right')
  elseif (ch == '8' or ch == '5') and G.state == 'serve' then
    launch()
  elseif ch == 'p' and (G.state == 'play' or G.state == 'pause') then
    on.enterKey()
  end
  platform.window:invalidate()
end

function on.escapeKey()
  local s = G.state
  if s == 'play' or s == 'serve' then
    G.state = 'pause'
  elseif s == 'pause' or s == 'over' then
    G.state = 'title'
    loadbest()
  end
  platform.window:invalidate()
end

function on.activate() timer.start(TICK) end

function on.deactivate()
  if G.state == 'play' or G.state == 'serve' then G.state = 'pause' end
end

local function field(gc)
  for r = 1, #G.bricks do
    for c = 1, 10 do
      local v = G.bricks[r][c]
      if v ~= 0 then
        color(gc, v < 0 and STEEL or HP[v])
        local x, y = BX0 + (c - 1) * (BW + 1), BY0 + (r - 1) * (BH + 2)
        gc:fillRect(x, y, BW, BH)
        if v < 0 then
          color(gc, DIM)
          gc:drawRect(x + 2, y + 2, BW - 5, BH - 5)
        end
      end
    end
  end
  color(gc, DIM)
  gc:fillRect(0, TOP - 2, 318, 2)
  color(gc, BAT)
  gc:fillRect(math.floor(G.px - PW / 2), PY, PW, PH)
  if G.y <= 212 - BALL then
    color(gc, TEXT)
    gc:fillArc(math.floor(G.x), math.floor(G.y), BALL, BALL, 0, 360)
  end
  color(gc, TEXT)
  font(gc, 9, 'b')
  gc:drawString('BRICKS', 4, 0, 'top')
  font(gc, 9)
  gc:drawString('Score ' .. G.score, 60, 0, 'top')
  gc:drawString('Best ' .. math.max(G.best, G.score), 140, 0, 'top')
  gc:drawString('Level ' .. G.level, 210, 0, 'top')
  for i = 1, G.lives do
    color(gc, GOLD)
    gc:fillArc(266 + i * 10, 3, 6, 6, 0, 360)
  end
end

local function panel(gc, lines)
  color(gc, BG)
  gc:fillRect(69, 110, 180, 72)
  color(gc, DIM)
  gc:drawRect(69, 110, 180, 72)
  color(gc, TEXT)
  font(gc, 16, 'b')
  centre(gc, lines[1], 116)
  font(gc, 10)
  for i = 2, #lines do centre(gc, lines[i], 110 + i * 16) end
end

local function title(gc)
  for c = 1, 10 do
    color(gc, HP[(c % 3) + 1])
    gc:fillRect(BX0 + (c - 1) * (BW + 1), 62, BW, BH)
  end
  color(gc, GOLD)
  font(gc, 24, 'b')
  centre(gc, 'BRICKS', 20)
  color(gc, BAT)
  gc:fillRect(137, 112, PW, PH)
  color(gc, TEXT)
  gc:fillArc(157, 94, BALL, BALL, 0, 360)
  font(gc, 10)
  centre(gc, 'Best ' .. G.best, 134)
  color(gc, DIM)
  font(gc, 9)
  centre(gc, 'Enter: play    4 6 or arrows: move the bat', 166)
  centre(gc, 'Enter or 8: serve    Esc: pause', 182)
end

function on.paint(gc)
  color(gc, BG)
  gc:fillRect(0, 0, 318, 212)
  if G.state == 'title' then
    title(gc)
    return
  end
  field(gc)
  if G.state == 'pause' then
    panel(gc, {'PAUSED', 'Enter: resume', 'Esc: title'})
  elseif G.state == 'clear' then
    panel(gc, {'LEVEL ' .. G.level .. ' CLEAR', 'Next: level ' .. (G.level + 1)})
  elseif G.state == 'over' then
    panel(gc, {'GAME OVER', 'Score ' .. G.score .. (G.record and '  New best!' or ''),
               'Enter: again   Esc: title'})
  end
end

loadbest()
timer.start(TICK)
