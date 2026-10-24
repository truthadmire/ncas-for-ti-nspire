platform.apiLevel = '2.0'
-- Snake for the TI-Nspire CX II (Lua). Paste into a Script Editor page.
-- Arrows or 8 4 6 2 steer, Enter starts and pauses, Esc pauses / goes back.
-- On the title screen up/down picks a line and left/right changes it.

local COLS, ROWS, CELL = 31, 19, 10
local X0, Y0 = 4, 18
local TICK = 0.05
local SPEEDS = {'Slow', 'Normal', 'Fast'}
local DELAY = {6, 4, 3}
local MODES = {'Walls', 'Wrap'}
local DX = {up = 0, down = 0, left = -1, right = 1}
local DY = {up = -1, down = 1, left = 0, right = 0}
local BACK = {up = 'down', down = 'up', left = 'right', right = 'left'}
local DIGIT = {['8'] = 'up', ['2'] = 'down', ['4'] = 'left', ['6'] = 'right',
               w = 'up', s = 'down', a = 'left', d = 'right'}

local BG = {20, 28, 36}
local FIELD = {32, 44, 56}
local BODY = {90, 200, 90}
local HEAD = {40, 150, 40}
local FOOD = {230, 60, 60}
local GOLD = {250, 200, 40}
local TEXT = {235, 235, 235}
local DIM = {150, 160, 170}

G = {state = 'title', line = 1, mode = 1, speed = 2, score = 0, best = 0,
     body = {}, occ = {}, q = {}, dir = 'right', grow = 0, wait = 0, eaten = 0,
     food = nil, bonus = nil, crash = 0, record = false, win = false}

local function color(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end

local function font(gc, size, st) gc:setFont('sansserif', st or 'r', size) end

local function centre(gc, s, y)
  gc:drawString(s, math.floor((318 - gc:getStringWidth(s)) / 2), y, 'top')
end

local function bestname() return 'snkbest' .. ((G.mode - 1) * 3 + G.speed) end

local function loadbest()
  local ok, v = pcall(var.recall, bestname())
  G.best = (ok and type(v) == 'number') and v or 0
end

local function savebest()
  pcall(var.store, bestname(), G.best)
  pcall(document.markChanged)
end

local function key(x, y) return y * COLS + x end

local function free(x, y) return not G.occ[key(x, y)] end

-- a random empty cell, or nil when the board is full
local function place(avoid)
  for _ = 1, 40 do
    local x, y = math.random(0, COLS - 1), math.random(0, ROWS - 1)
    if free(x, y) and not (avoid and avoid.x == x and avoid.y == y) then
      return {x = x, y = y}
    end
  end
  local cells = {}
  for y = 0, ROWS - 1 do
    for x = 0, COLS - 1 do
      if free(x, y) and not (avoid and avoid.x == x and avoid.y == y) then
        cells[#cells + 1] = {x = x, y = y}
      end
    end
  end
  if #cells == 0 then return nil end
  return cells[math.random(1, #cells)]
end

local function start()
  math.randomseed(timer.getMilliSecCounter())
  G.body, G.occ, G.q = {}, {}, {}
  local y = math.floor(ROWS / 2)
  for i = 0, 3 do
    G.body[#G.body + 1] = {x = 8 - i, y = y}
    G.occ[key(8 - i, y)] = true
  end
  G.dir, G.grow, G.wait, G.eaten, G.score = 'right', 0, 0, 0, 0
  G.bonus, G.crash, G.record, G.win = nil, 0, false, false
  G.food = place()
  loadbest()
  G.state = 'play'
end

-- ticks between moves: shorter as the snake eats
local function delay()
  local d = DELAY[G.speed] - math.floor(G.eaten / 5)
  local low = G.speed == 3 and 1 or 2
  if d < low then d = low end
  return d
end

local function finish(win)
  G.win = win
  if G.score > G.best then
    G.best = G.score
    G.record = true
    savebest()
  end
  if win then
    G.state = 'over'
  else
    G.state = 'crash'
    G.crash = 20
  end
end

local function turn(d)
  if #G.q < 3 then G.q[#G.q + 1] = d end
end

local function step()
  -- take the first queued turn that is not straight back
  while #G.q > 0 do
    local d = table.remove(G.q, 1)
    if d ~= G.dir and d ~= BACK[G.dir] then
      G.dir = d
      break
    end
  end
  local head = G.body[1]
  local x, y = head.x + DX[G.dir], head.y + DY[G.dir]
  if G.mode == 2 then
    x, y = x % COLS, y % ROWS
  elseif x < 0 or y < 0 or x >= COLS or y >= ROWS then
    finish(false)
    return
  end
  local food = G.food and G.food.x == x and G.food.y == y
  local gold = G.bonus and G.bonus.x == x and G.bonus.y == y
  if food then G.grow = G.grow + 1 end
  if G.grow > 0 then
    G.grow = G.grow - 1
  else
    local tail = table.remove(G.body)
    G.occ[key(tail.x, tail.y)] = nil
  end
  if G.occ[key(x, y)] then
    finish(false)
    return
  end
  table.insert(G.body, 1, {x = x, y = y})
  G.occ[key(x, y)] = true
  if food then
    G.score = G.score + 10
    G.eaten = G.eaten + 1
    G.food = place(G.bonus)
    if G.eaten % 5 == 0 and not G.bonus then
      G.bonus = place(G.food)
      if G.bonus then G.bonus.left = 70 end
    end
    if not G.food then finish(true) end
  elseif gold then
    G.score = G.score + 50
    G.bonus = nil
  end
end

function on.timer()
  if G.state == 'play' then
    local moved = false
    if G.bonus then
      G.bonus.left = G.bonus.left - 1
      if G.bonus.left <= 0 then G.bonus = nil end
      moved = true
    end
    G.wait = G.wait + 1
    if G.wait >= delay() then
      G.wait = 0
      step()
      moved = true
    end
    if moved then platform.window:invalidate() end
  elseif G.state == 'crash' then
    G.crash = G.crash - 1
    if G.crash <= 0 then G.state = 'over' end
    platform.window:invalidate()
  end
end

function on.arrowKey(k)
  if G.state == 'play' then
    turn(k)
  elseif G.state == 'title' then
    if k == 'up' or k == 'down' then
      G.line = 3 - G.line
    elseif G.line == 1 then
      G.mode = 3 - G.mode
    else
      G.speed = (G.speed + (k == 'right' and 1 or -1) + 2) % 3 + 1
    end
    loadbest()
  end
  platform.window:invalidate()
end

function on.charIn(ch)
  local d = DIGIT[ch]
  if d then
    on.arrowKey(d)
  elseif ch == 'p' and (G.state == 'play' or G.state == 'pause') then
    G.state = G.state == 'play' and 'pause' or 'play'
    platform.window:invalidate()
  end
end

function on.enterKey()
  if G.state == 'title' or G.state == 'over' then
    start()
  elseif G.state == 'play' then
    G.state = 'pause'
  elseif G.state == 'pause' then
    G.state = 'play'
  end
  platform.window:invalidate()
end

function on.escapeKey()
  if G.state == 'play' then
    G.state = 'pause'
  elseif G.state == 'pause' or G.state == 'over' then
    G.state = 'title'
    loadbest()
  end
  platform.window:invalidate()
end

function on.activate()
  timer.start(TICK)
end

function on.deactivate()
  if G.state == 'play' then G.state = 'pause' end
end

local function cell(gc, x, y, c)
  color(gc, c)
  gc:fillRect(X0 + x * CELL, Y0 + y * CELL, CELL - 1, CELL - 1)
end

local function dot(gc, p, c)
  color(gc, c)
  gc:fillArc(X0 + p.x * CELL, Y0 + p.y * CELL, CELL - 1, CELL - 1, 0, 360)
end

local function board(gc)
  color(gc, FIELD)
  gc:fillRect(X0, Y0, COLS * CELL, ROWS * CELL)
  color(gc, G.mode == 1 and DIM or FIELD)
  gc:drawRect(X0 - 1, Y0 - 1, COLS * CELL + 1, ROWS * CELL + 1)
  if G.food then dot(gc, G.food, FOOD) end
  if G.bonus then
    dot(gc, G.bonus, GOLD)
    color(gc, GOLD)
    gc:fillRect(250, 6, math.floor(G.bonus.left * 60 / 70), 4)
  end
  local n = #G.body
  for i = n, 2, -1 do cell(gc, G.body[i].x, G.body[i].y, BODY) end
  local h = G.body[1]
  if h then
    cell(gc, h.x, h.y, G.state == 'crash' and FOOD or HEAD)
    -- eyes, on the side the snake is looking
    color(gc, TEXT)
    local cx, cy = X0 + h.x * CELL + 4, Y0 + h.y * CELL + 4
    local ex, ey = DX[G.dir] * 2, DY[G.dir] * 2
    gc:fillRect(cx + ex - ey - 1, cy + ey - ex - 1, 2, 2)
    gc:fillRect(cx + ex + ey - 1, cy + ey + ex - 1, 2, 2)
  end
  color(gc, TEXT)
  font(gc, 9, 'b')
  gc:drawString('SNAKE', 6, 1, 'top')
  font(gc, 9)
  gc:drawString('Score ' .. G.score, 70, 1, 'top')
  gc:drawString('Best ' .. math.max(G.best, G.score), 160, 1, 'top')
end

local function panel(gc, lines)
  color(gc, BG)
  gc:fillRect(59, 64, 200, 84)
  color(gc, DIM)
  gc:drawRect(59, 64, 200, 84)
  color(gc, TEXT)
  font(gc, 16, 'b')
  centre(gc, lines[1], 70)
  font(gc, 10)
  for i = 2, #lines do centre(gc, lines[i], 76 + i * 16) end
end

local function title(gc)
  color(gc, GOLD)
  font(gc, 24, 'b')
  centre(gc, 'SNAKE', 22)
  for i = 1, 6 do
    cell(gc, 10 + i, 5, i == 6 and HEAD or BODY)
  end
  dot(gc, {x = 19, y = 5}, FOOD)
  font(gc, 12)
  local rows = {'Mode:  < ' .. MODES[G.mode] .. ' >', 'Speed:  < ' .. SPEEDS[G.speed] .. ' >'}
  for i = 1, 2 do
    if G.line == i then
      color(gc, FIELD)
      gc:fillRect(84, 98 + (i - 1) * 24, 150, 20)
    end
    color(gc, G.line == i and TEXT or DIM)
    centre(gc, rows[i], 100 + (i - 1) * 24)
  end
  color(gc, TEXT)
  font(gc, 10)
  centre(gc, 'Best ' .. G.best, 152)
  color(gc, DIM)
  font(gc, 9)
  centre(gc, 'Enter: play    arrows or 8 4 6 2: steer', 176)
  centre(gc, 'Esc or Enter: pause', 190)
end

function on.paint(gc)
  color(gc, BG)
  gc:fillRect(0, 0, 318, 212)
  if G.state == 'title' then
    title(gc)
    return
  end
  board(gc)
  if G.state == 'pause' then
    panel(gc, {'PAUSED', 'Enter: resume', 'Esc: title'})
  elseif G.state == 'over' then
    panel(gc, {G.win and 'YOU WIN' or 'GAME OVER',
               'Score ' .. G.score .. (G.record and '   New best!' or ''),
               'Enter: again    Esc: title'})
  end
end

loadbest()
timer.start(TICK)
