platform.apiLevel = '2.0'
-- Rally: bat-and-ball game against the calculator, for the TI-Nspire CX II
-- (Lua). Paste into a Script Editor page. Up/down (8 2) push your bat on the
-- left: each press speeds it up and it glides to a stop, so tap or hold.
-- First to 7 wins. Enter or Esc pauses; on the title left/right picks how
-- good the calculator is.

local TICK = 0.05
local TOP, BOTTOM = 15, 212
local BW, BH = 4, 30                -- bat size
local PX, CX = 8, 306               -- left edges of the two bats
local BALL = 4
local PUSH, PMAX, GLIDE = 5, 9, 0.82
local MAXANG = 0.9                  -- about 50 degrees from level
local WIN = 7
local LEVELS = {'Easy', 'Normal', 'Hard'}
-- calculator bat: top speed, aiming error (pixels at the starting ball
-- speed, more when faster), ticks between looks, whether it works out where
-- the ball will bounce to, and how far over (x) the ball must be before it
-- reacts
local CPU = {{1.7, 14, 5, false, 150}, {2.4, 10, 4, false, 170}, {2.6, 12, 3, true, 160}}

local BG = {14, 30, 26}
local LINE = {90, 140, 120}
local TEXT = {235, 240, 235}
local DIM = {150, 175, 165}
local GOLD = {250, 200, 40}
local YOU = {120, 220, 255}
local THEM = {255, 140, 110}

G = {state = 'title', diff = 2, wins = 0, me = 0, cpu = 0, py = 91, pv = 0,
     cy = 91, aim = 106, look = 0, x = 0, y = 0, vx = 0, vy = 0, speed = 0,
     wait = 0, toward = -1, won = false}

local function color(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end

local function font(gc, size, st) gc:setFont('sansserif', st or 'r', size) end

local function centre(gc, s, y)
  gc:drawString(s, math.floor((318 - gc:getStringWidth(s)) / 2), y, 'top')
end

local function loadwins()
  local ok, v = pcall(var.recall, 'rlywins' .. G.diff)
  G.wins = (ok and type(v) == 'number') and v or 0
end

local function savewins()
  pcall(var.store, 'rlywins' .. G.diff, G.wins)
  pcall(document.markChanged)
end

-- ball back in the middle; it goes toward side d (-1 you, 1 calculator)
local function serve(d)
  G.x, G.y = 157, math.random(TOP + 40, BOTTOM - 40)
  G.vx, G.vy = 0, 0
  G.toward = d
  G.state, G.wait = 'serve', 20
end

local function start()
  math.randomseed(timer.getMilliSecCounter())
  G.me, G.cpu, G.won = 0, 0, false
  G.py, G.pv, G.cy = 91, 0, 91
  G.aim = 106
  loadwins()
  serve(math.random(0, 1) * 2 - 1)
end

local function launch()
  G.speed = 3
  local a = (math.random() - 0.5) * 0.9
  G.vx, G.vy = G.toward * G.speed * math.cos(a), G.speed * math.sin(a)
  G.state = 'play'
end

local function clamp(v, lo, hi)
  if v < lo then return lo end
  if v > hi then return hi end
  return v
end

-- where the ball's centre will be when it reaches the calculator's bat
local function predict()
  if G.vx <= 0 then return (TOP + BOTTOM) / 2 end
  local t = (CX - BALL - G.x) / G.vx
  local y = G.y + BALL / 2 + G.vy * t
  local lo, hi = TOP + BALL / 2, BOTTOM - BALL / 2
  local span = hi - lo
  -- fold the straight path back into the court (bounces)
  local m = (y - lo) % (2 * span)
  if m > span then m = 2 * span - m end
  return lo + m
end

local function think()
  local c = CPU[G.diff]
  G.look = G.look - 1
  if G.look <= 0 then
    G.look = c[3]
    local target
    if G.vx > 0 and G.x > c[5] then
      target = c[4] and predict() or (G.y + BALL / 2)
      target = target + (math.random() * 2 - 1) * c[2] * G.speed / 3
    else
      target = (TOP + BOTTOM) / 2
    end
    G.aim = target
  end
  local d = G.aim - (G.cy + BH / 2)
  G.cy = G.cy + clamp(d, -c[1], c[1])
  G.cy = clamp(G.cy, TOP, BOTTOM - BH)
end

local function bounce(by, side)
  local off = clamp((G.y + BALL / 2 - by - BH / 2) / (BH / 2 + BALL / 2), -1, 1)
  G.speed = math.min(G.speed + 0.15, 6)
  local a = off * MAXANG
  G.vx, G.vy = side * G.speed * math.cos(a), G.speed * math.sin(a)
end

local function point(mine)
  if mine then G.me = G.me + 1 else G.cpu = G.cpu + 1 end
  if G.me >= WIN or G.cpu >= WIN then
    G.won = G.me >= WIN
    if G.won then
      G.wins = G.wins + 1
      savewins()
    end
    G.state = 'over'
  else
    serve(mine and 1 or -1)
  end
end

local function moveball()
  local n = math.ceil(G.speed / 2)
  for _ = 1, n do
    local x, y = G.x + G.vx / n, G.y + G.vy / n
    if y < TOP then
      y, G.vy = 2 * TOP - y, -G.vy
    elseif y + BALL > BOTTOM then
      y, G.vy = 2 * (BOTTOM - BALL) - y, -G.vy
    end
    local face = PX + BW
    if G.vx < 0 and G.x >= face and x < face and y + BALL > G.py and y < G.py + BH then
      x = face
      G.y = y
      bounce(G.py, 1)
    elseif G.vx > 0 and G.x + BALL <= CX and x + BALL > CX and y + BALL > G.cy and y < G.cy + BH then
      x = CX - BALL
      G.y = y
      bounce(G.cy, -1)
    end
    G.x, G.y = x, y
    if G.x + BALL < 0 then
      point(false)
      return
    elseif G.x > 318 then
      point(true)
      return
    end
  end
end

local function movebat()
  G.py = G.py + G.pv
  G.pv = G.pv * GLIDE
  if math.abs(G.pv) < 0.3 then G.pv = 0 end
  if G.py < TOP then G.py, G.pv = TOP, 0 end
  if G.py > BOTTOM - BH then G.py, G.pv = BOTTOM - BH, 0 end
end

function on.timer()
  local s = G.state
  if s == 'serve' or s == 'play' then
    movebat()
    think()
    if s == 'serve' then
      G.wait = G.wait - 1
      if G.wait <= 0 then launch() end
    else
      moveball()
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
  if G.state == 'title' then
    if k == 'left' or k == 'right' then
      G.diff = (G.diff + (k == 'right' and 1 or -1) + 2) % 3 + 1
      loadwins()
    end
  elseif k == 'up' then
    push(-1)
  elseif k == 'down' then
    push(1)
  end
  platform.window:invalidate()
end

function on.charIn(ch)
  if ch == '8' then
    on.arrowKey('up')
  elseif ch == '2' then
    on.arrowKey('down')
  elseif ch == '4' or ch == '6' then
    on.arrowKey(ch == '4' and 'left' or 'right')
  elseif ch == 'p' and (G.state == 'play' or G.state == 'serve' or G.state == 'pause') then
    on.enterKey()
  end
end

function on.enterKey()
  local s = G.state
  if s == 'title' or s == 'over' then
    start()
  elseif s == 'play' or s == 'serve' then
    G.paused = s
    G.state = 'pause'
  elseif s == 'pause' then
    G.state = G.paused or 'play'
  end
  platform.window:invalidate()
end

function on.escapeKey()
  local s = G.state
  if s == 'play' or s == 'serve' then
    G.paused = s
    G.state = 'pause'
  elseif s == 'pause' or s == 'over' then
    G.state = 'title'
    loadwins()
  end
  platform.window:invalidate()
end

function on.activate() timer.start(TICK) end

function on.deactivate()
  if G.state == 'play' or G.state == 'serve' then
    G.paused = G.state
    G.state = 'pause'
  end
end

local function court(gc)
  color(gc, LINE)
  gc:fillRect(0, TOP - 2, 318, 2)
  for y = TOP + 4, BOTTOM - 8, 12 do gc:fillRect(158, y, 2, 6) end
  color(gc, YOU)
  gc:fillRect(PX, math.floor(G.py), BW, BH)
  color(gc, THEM)
  gc:fillRect(CX, math.floor(G.cy), BW, BH)
  if G.x >= 0 and G.x <= 318 - BALL then
    color(gc, TEXT)
    gc:fillArc(math.floor(G.x), math.floor(G.y), BALL, BALL, 0, 360)
  end
  font(gc, 9, 'b')
  color(gc, TEXT)
  gc:drawString('RALLY', 4, 0, 'top')
  font(gc, 9)
  color(gc, DIM)
  gc:drawString(LEVELS[G.diff], 270, 0, 'top')
  font(gc, 12, 'b')
  color(gc, YOU)
  gc:drawString(tostring(G.me), 128, 0, 'top')
  color(gc, THEM)
  gc:drawString(tostring(G.cpu), 182, 0, 'top')
  font(gc, 7)
  color(gc, DIM)
  gc:drawString('you', 100, 3, 'top')
  gc:drawString('calc', 198, 3, 'top')
end

local function panel(gc, lines)
  color(gc, BG)
  gc:fillRect(69, 70, 180, 72)
  color(gc, LINE)
  gc:drawRect(69, 70, 180, 72)
  color(gc, TEXT)
  font(gc, 16, 'b')
  centre(gc, lines[1], 76)
  font(gc, 10)
  for i = 2, #lines do centre(gc, lines[i], 70 + i * 16) end
end

local function title(gc)
  color(gc, GOLD)
  font(gc, 24, 'b')
  centre(gc, 'RALLY', 20)
  color(gc, YOU)
  gc:fillRect(60, 60, BW, BH)
  color(gc, THEM)
  gc:fillRect(254, 74, BW, BH)
  color(gc, TEXT)
  gc:fillArc(150, 80, BALL, BALL, 0, 360)
  color(gc, LINE)
  gc:fillRect(84, 108, 150, 20)
  color(gc, TEXT)
  font(gc, 12)
  centre(gc, 'Calculator:  < ' .. LEVELS[G.diff] .. ' >', 110)
  font(gc, 10)
  centre(gc, 'Games won: ' .. G.wins, 138)
  color(gc, DIM)
  font(gc, 9)
  centre(gc, 'Enter: play    8 2 or up/down: move your bat', 168)
  centre(gc, 'First to 7.    Esc: pause', 184)
end

function on.paint(gc)
  color(gc, BG)
  gc:fillRect(0, 0, 318, 212)
  if G.state == 'title' then
    title(gc)
    return
  end
  court(gc)
  if G.state == 'pause' then
    panel(gc, {'PAUSED', 'Enter: resume', 'Esc: title'})
  elseif G.state == 'over' then
    panel(gc, {G.won and 'YOU WIN' or 'CALCULATOR WINS', G.me .. ' : ' .. G.cpu,
               'Enter: again   Esc: title'})
  end
end

loadwins()
timer.start(TICK)
