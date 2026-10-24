platform.apiLevel = '2.0'
-- Blocks: falling-block puzzle for the TI-Nspire CX II (Lua). Paste into a
-- Script Editor page. Left/right (4 6) move, up (8) turns, 7 turns back,
-- down (2) drops faster, Enter (5) drops at once, Tab (0) holds a piece,
-- Esc pauses. On the title screen left/right picks the starting level.

local W, H = 10, 22          -- rows 1-2 are hidden above the well
local CELL = 10
local X0, Y0 = 109, 6        -- screen position of column 1, row 3
local TICK = 0.05
local FALL = {16, 14, 12, 10, 8, 7, 6, 5, 4, 3, 3, 2, 2, 2, 1}
local LOCK, RESETS, FLASH = 10, 15, 6
local LINEPTS = {100, 300, 500, 800}
local NAMES = {'I', 'O', 'T', 'S', 'Z', 'J', 'L'}

-- spawn cells in an n x n box (x, y pairs, y down)
local SHAPES = {
  I = {4, {0, 1, 1, 1, 2, 1, 3, 1}},
  O = {2, {0, 0, 1, 0, 0, 1, 1, 1}},
  T = {3, {1, 0, 0, 1, 1, 1, 2, 1}},
  S = {3, {1, 0, 2, 0, 0, 1, 1, 1}},
  Z = {3, {0, 0, 1, 0, 1, 1, 2, 1}},
  J = {3, {0, 0, 0, 1, 1, 1, 2, 1}},
  L = {3, {2, 0, 0, 1, 1, 1, 2, 1}},
}

local COLORS = {
  I = {60, 210, 230}, O = {240, 210, 50}, T = {170, 80, 210}, S = {80, 200, 80},
  Z = {230, 70, 70}, J = {60, 110, 230}, L = {240, 150, 40},
}

-- wall kicks for turning right from state r (x right, y up, as usually
-- written); turning left from r to r-1 uses the negated kicks of r-1 -> r
local KICKS = {
  [0] = {0, 0, -1, 0, -1, 1, 0, -2, -1, -2},
  {0, 0, 1, 0, 1, -1, 0, 2, 1, 2},
  {0, 0, 1, 0, 1, 1, 0, -2, 1, -2},
  {0, 0, -1, 0, -1, -1, 0, 2, -1, 2},
}
local IKICKS = {
  [0] = {0, 0, -2, 0, 1, 0, -2, -1, 1, 2},
  {0, 0, -1, 0, 2, 0, -1, 2, 2, -1},
  {0, 0, 2, 0, -1, 0, 2, 1, -1, -2},
  {0, 0, 1, 0, -2, 0, 1, -2, -2, 1},
}

local BG = {18, 22, 34}
local WELL = {30, 36, 52}
local LINE = {90, 100, 130}
local TEXT = {235, 235, 235}
local DIM = {150, 160, 175}
local GOLD = {250, 200, 40}

-- ROT[p][r] = cell list for rotation r (0-3), turned right each time
local ROT = {}
for p, s in pairs(SHAPES) do
  local n, c = s[1], s[2]
  ROT[p] = {[0] = c}
  for r = 1, 3 do
    local prev, t = ROT[p][r - 1], {}
    for i = 1, #prev, 2 do
      t[i], t[i + 1] = n - 1 - prev[i + 1], prev[i]
    end
    ROT[p][r] = t
  end
end

G = {state = 'title', start = 1, score = 0, lines = 0, level = 1, best = 0,
     board = {}, cur = nil, bag = {}, queue = {}, hold = nil, canhold = true,
     fall = 0, lock = 0, resets = 0, flash = 0, rows = {}, record = false}

local function color(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end

local function font(gc, size, st) gc:setFont('sansserif', st or 'r', size) end

local function centre(gc, s, y, x0, w)
  x0, w = x0 or 0, w or 318
  gc:drawString(s, x0 + math.floor((w - gc:getStringWidth(s)) / 2), y, 'top')
end

local function loadbest()
  local ok, v = pcall(var.recall, 'blkbest')
  G.best = (ok and type(v) == 'number') and v or 0
end

local function savebest()
  pcall(var.store, 'blkbest', G.best)
  pcall(document.markChanged)
end

local function fits(p, r, x, y)
  local c = ROT[p][r]
  for i = 1, #c, 2 do
    local cx, cy = x + c[i], y + c[i + 1]
    if cx < 1 or cx > W or cy < 1 or cy > H or G.board[cy][cx] ~= 0 then
      return false
    end
  end
  return true
end

local function nextpiece()
  while #G.queue < 4 do
    if #G.bag == 0 then
      for i = 1, 7 do G.bag[i] = NAMES[i] end
      for i = 7, 2, -1 do
        local j = math.random(1, i)
        G.bag[i], G.bag[j] = G.bag[j], G.bag[i]
      end
    end
    G.queue[#G.queue + 1] = table.remove(G.bag)
  end
  return table.remove(G.queue, 1)
end

local function finish()
  if G.score > G.best then
    G.best = G.score
    G.record = true
    savebest()
  end
  G.state = 'over'
end

local function spawn(p)
  p = p or nextpiece()
  local x = p == 'O' and 5 or 4
  G.cur = {p = p, r = 0, x = x, y = 1}
  G.fall, G.lock, G.resets = 0, 0, 0
  if not fits(p, 0, x, 1) then finish() end
end

local function start()
  math.randomseed(timer.getMilliSecCounter())
  G.board = {}
  for y = 1, H do
    G.board[y] = {}
    for x = 1, W do G.board[y][x] = 0 end
  end
  G.bag, G.queue, G.hold, G.canhold = {}, {}, nil, true
  G.score, G.lines, G.level, G.flash, G.rows, G.record = 0, 0, G.start, 0, {}, false
  loadbest()
  G.state = 'play'
  spawn()
end

local function grounded()
  local c = G.cur
  return not fits(c.p, c.r, c.x, c.y + 1)
end

-- after a successful move or turn: a piece on the ground gets more time
local function moved()
  if G.resets < RESETS and grounded() then
    G.lock = 0
    G.resets = G.resets + 1
  end
end

local function shift(dx, dy)
  local c = G.cur
  if fits(c.p, c.r, c.x + dx, c.y + dy) then
    c.x, c.y = c.x + dx, c.y + dy
    moved()
    return true
  end
  return false
end

local function turn(dir)
  local c = G.cur
  if c.p == 'O' then return false end
  local nr = (c.r + dir) % 4
  local k = c.p == 'I' and IKICKS or KICKS
  local t, s = k[c.r], 1
  if dir < 0 then t, s = k[nr], -1 end
  for i = 1, #t, 2 do
    local x, y = c.x + s * t[i], c.y - s * t[i + 1]
    if fits(c.p, nr, x, y) then
      c.r, c.x, c.y = nr, x, y
      moved()
      return true
    end
  end
  return false
end

local function ghost()
  local c = G.cur
  local y = c.y
  while fits(c.p, c.r, c.x, y + 1) do y = y + 1 end
  return y
end

local function lockpiece()
  local c = G.cur
  local cells = ROT[c.p][c.r]
  local above = true
  for i = 1, #cells, 2 do
    local y = c.y + cells[i + 1]
    G.board[y][c.x + cells[i]] = c.p
    if y > 2 then above = false end
  end
  G.cur = nil
  G.canhold = true
  if above then
    finish()
    return
  end
  G.rows = {}
  for y = 1, H do
    local full = true
    for x = 1, W do
      if G.board[y][x] == 0 then
        full = false
        break
      end
    end
    if full then G.rows[#G.rows + 1] = y end
  end
  if #G.rows > 0 then
    G.flash = FLASH
  else
    spawn()
  end
end

local function clearrows()
  local n = #G.rows
  for i = 1, n do
    table.remove(G.board, G.rows[i])
    local row = {}
    for x = 1, W do row[x] = 0 end
    table.insert(G.board, 1, row)
  end
  G.score = G.score + LINEPTS[n] * G.level
  G.lines = G.lines + n
  local lv = G.start + math.floor(G.lines / 10)
  if lv > G.level then G.level = lv end
  G.rows = {}
  spawn()
end

local function harddrop()
  local c = G.cur
  local y = ghost()
  G.score = G.score + 2 * (y - c.y)
  c.y = y
  lockpiece()
end

local function hold()
  if not G.canhold then return end
  local p = G.cur.p
  G.canhold = false
  spawn(G.hold)
  G.hold = p
end

function on.timer()
  if G.state ~= 'play' then return end
  if G.flash > 0 then
    G.flash = G.flash - 1
    if G.flash == 0 then clearrows() end
    platform.window:invalidate()
    return
  end
  local change = false
  G.fall = G.fall + 1
  if G.fall >= FALL[math.min(G.level, #FALL)] then
    G.fall = 0
    if shift(0, 1) then change = true end
  end
  if G.cur and grounded() then
    G.lock = G.lock + 1
    if G.lock >= LOCK then
      lockpiece()
      change = true
    end
  elseif G.cur then
    G.lock = 0
  end
  if change then platform.window:invalidate() end
end

local ACT = {left = 'left', right = 'right', up = 'cw', down = 'soft',
             ['4'] = 'left', ['6'] = 'right', ['8'] = 'cw', x = 'cw', ['9'] = 'cw',
             ['7'] = 'ccw', z = 'ccw', ['2'] = 'soft', ['5'] = 'drop', [' '] = 'drop',
             ['0'] = 'hold', c = 'hold'}

local function act(a)
  if G.state == 'title' then
    if a == 'left' or a == 'right' then
      G.start = (G.start + (a == 'right' and 1 or -1) + 9) % 10 + 1
    end
  elseif G.state == 'play' and G.cur and G.flash == 0 then
    if a == 'left' then
      shift(-1, 0)
    elseif a == 'right' then
      shift(1, 0)
    elseif a == 'cw' then
      turn(1)
    elseif a == 'ccw' then
      turn(-1)
    elseif a == 'soft' then
      if shift(0, 1) then
        G.score = G.score + 1
        G.fall = 0
      end
    elseif a == 'drop' then
      harddrop()
    elseif a == 'hold' then
      hold()
    end
  end
  platform.window:invalidate()
end

function on.arrowKey(k) act(ACT[k]) end

function on.charIn(ch)
  if ch == 'p' and (G.state == 'play' or G.state == 'pause') then
    G.state = G.state == 'play' and 'pause' or 'play'
    platform.window:invalidate()
  elseif ACT[ch] then
    act(ACT[ch])
  end
end

function on.tabKey() act('hold') end

function on.enterKey()
  if G.state == 'title' or G.state == 'over' then
    start()
  elseif G.state == 'pause' then
    G.state = 'play'
  elseif G.state == 'play' then
    act('drop')
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

function on.activate() timer.start(TICK) end

function on.deactivate()
  if G.state == 'play' then G.state = 'pause' end
end

local function block(gc, x, y, s, c)
  color(gc, c)
  gc:fillRect(x, y, s - 1, s - 1)
  gc:setColorRGB(math.min(255, c[1] + 50), math.min(255, c[2] + 50), math.min(255, c[3] + 50))
  gc:fillRect(x, y, s - 1, 2)
end

-- a small picture of piece p centred in the box at (x, y, w, h)
local function mini(gc, p, x, y, w, h)
  local c, n = ROT[p][0], SHAPES[p][1]
  local s = 8
  local minx, maxx, miny, maxy = 9, -1, 9, -1
  for i = 1, #c, 2 do
    minx, maxx = math.min(minx, c[i]), math.max(maxx, c[i])
    miny, maxy = math.min(miny, c[i + 1]), math.max(maxy, c[i + 1])
  end
  local ox = x + math.floor((w - (maxx - minx + 1) * s) / 2) - minx * s
  local oy = y + math.floor((h - (maxy - miny + 1) * s) / 2) - miny * s
  for i = 1, #c, 2 do block(gc, ox + c[i] * s, oy + c[i + 1] * s, s, COLORS[p]) end
end

local function sx(x) return X0 + (x - 1) * CELL end
local function sy(y) return Y0 + (y - 3) * CELL end

local function well(gc)
  color(gc, WELL)
  gc:fillRect(X0, Y0, W * CELL, (H - 2) * CELL)
  color(gc, LINE)
  gc:drawRect(X0 - 1, Y0 - 1, W * CELL + 1, (H - 2) * CELL + 1)
  local flash = {}
  for i = 1, #G.rows do flash[G.rows[i]] = true end
  for y = 3, H do
    for x = 1, W do
      local v = G.board[y][x]
      if flash[y] then
        if G.flash % 2 == 0 then
          color(gc, TEXT)
          gc:fillRect(sx(x), sy(y), CELL - 1, CELL - 1)
        end
      elseif v ~= 0 then
        block(gc, sx(x), sy(y), CELL, COLORS[v])
      end
    end
  end
  local c = G.cur
  if c and G.state ~= 'over' then
    local cells, gy = ROT[c.p][c.r], ghost()
    color(gc, COLORS[c.p])
    for i = 1, #cells, 2 do
      local y = gy + cells[i + 1]
      if y > 2 then gc:drawRect(sx(c.x + cells[i]), sy(y), CELL - 2, CELL - 2) end
    end
    for i = 1, #cells, 2 do
      local y = c.y + cells[i + 1]
      if y > 2 then block(gc, sx(c.x + cells[i]), sy(y), CELL, COLORS[c.p]) end
    end
  end
end

local function side(gc)
  font(gc, 10, 'b')
  color(gc, DIM)
  gc:drawString('HOLD', 12, 6, 'top')
  gc:drawString('NEXT', 222, 6, 'top')
  color(gc, WELL)
  gc:fillRect(12, 22, 84, 40)
  gc:fillRect(222, 22, 84, 104)
  if G.hold then mini(gc, G.hold, 12, 22, 84, 40) end
  for i = 1, 3 do
    if G.queue[i] then mini(gc, G.queue[i], 222, 22 + (i - 1) * 34, 84, 36) end
  end
  local rows = {{'Score', G.score}, {'Lines', G.lines}, {'Level', G.level},
                {'Best', math.max(G.best, G.score)}}
  for i = 1, #rows do
    local y = 74 + (i - 1) * 30
    font(gc, 9)
    color(gc, DIM)
    gc:drawString(rows[i][1], 12, y, 'top')
    font(gc, 12, 'b')
    color(gc, TEXT)
    gc:drawString(tostring(rows[i][2]), 12, y + 11, 'top')
  end
  font(gc, 9)
  color(gc, DIM)
  local help = {'4 6  move', '8  turn  7  back', '2  down', '5 Enter  drop', '0 Tab  hold'}
  for i = 1, #help do gc:drawString(help[i], 222, 132 + (i - 1) * 14, 'top') end
end

local function panel(gc, lines)
  color(gc, BG)
  gc:fillRect(84, 70, 150, 72)
  color(gc, LINE)
  gc:drawRect(84, 70, 150, 72)
  color(gc, TEXT)
  font(gc, 16, 'b')
  centre(gc, lines[1], 76)
  font(gc, 10)
  for i = 2, #lines do centre(gc, lines[i], 70 + i * 16) end
end

local function title(gc)
  local demo = {'T', 'I', 'L', 'S', 'O', 'Z', 'J'}
  for i = 1, 7 do mini(gc, demo[i], 20 + (i - 1) * 40, 64, 38, 30) end
  color(gc, GOLD)
  font(gc, 24, 'b')
  centre(gc, 'BLOCKS', 20)
  color(gc, WELL)
  gc:fillRect(84, 110, 150, 20)
  color(gc, TEXT)
  font(gc, 12)
  centre(gc, 'Level:  < ' .. G.start .. ' >', 112)
  font(gc, 10)
  centre(gc, 'Best ' .. G.best, 140)
  color(gc, DIM)
  font(gc, 9)
  centre(gc, 'Enter: play    4 6: move    8: turn    5: drop', 172)
  centre(gc, '0 or Tab: hold    Esc: pause', 188)
end

function on.paint(gc)
  color(gc, BG)
  gc:fillRect(0, 0, 318, 212)
  if G.state == 'title' then
    title(gc)
    return
  end
  well(gc)
  side(gc)
  if G.state == 'pause' then
    panel(gc, {'PAUSED', 'Enter: resume', 'Esc: title'})
  elseif G.state == 'over' then
    panel(gc, {'GAME OVER', 'Score ' .. G.score .. (G.record and '  New best!' or ''),
               'Enter: again   Esc: title'})
  end
end

loadbest()
timer.start(TICK)
