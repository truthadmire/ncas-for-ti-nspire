platform.apiLevel = '2.0'
-- Sudoku for the TI-Nspire CX II (Lua). Paste into a Script Editor page.
-- Arrows move, 1-9 write, 0 / del / clear erase, Enter or Tab switches
-- between pen and pencil notes, h fills in the square (30 s penalty), Esc
-- pauses. Every puzzle is made on the calculator and has one solution.

local TICK = 0.1
local BUDGET = 70                -- ms of puzzle making per timer tick
local CELL = 22
local X0, Y0 = 6, 7
local LEVELS = {'Easy', 'Medium', 'Hard'}
local GIVENS = {38, 30, 25}
local PENALTY = 30

local PAPER = {250, 248, 240}
local INK = {20, 24, 32}
local PEN = {40, 90, 200}
local BAD = {215, 40, 40}
local THIN = {170, 170, 170}
local BAND = {230, 236, 246}
local SAME = {200, 220, 250}
local CURSOR = {255, 220, 110}
local DIM = {110, 115, 125}

-- row, column, box of each square 1-81 and the 20 squares that share one
local ROW, COL, BOX, PEERS = {}, {}, {}, {}
for i = 1, 81 do
  ROW[i] = math.floor((i - 1) / 9) + 1
  COL[i] = (i - 1) % 9 + 1
  BOX[i] = math.floor((ROW[i] - 1) / 3) * 3 + math.floor((COL[i] - 1) / 3) + 1
end
for i = 1, 81 do
  PEERS[i] = {}
  for j = 1, 81 do
    if j ~= i and (ROW[i] == ROW[j] or COL[i] == COL[j] or BOX[i] == BOX[j]) then
      PEERS[i][#PEERS[i] + 1] = j
    end
  end
end

G = {state = 'title', diff = 2, best = 0, cur = 41, grid = {}, given = {},
     sol = {}, notes = {}, pencil = false, ticks = 0, hints = 0, gen = nil,
     record = false}

local function color(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end

local function font(gc, size, st) gc:setFont('sansserif', st or 'r', size) end

local function centre(gc, s, y, x0, w)
  x0, w = x0 or 0, w or 318
  gc:drawString(s, x0 + math.floor((w - gc:getStringWidth(s)) / 2), y, 'top')
end

local function clock(t)
  local s = math.floor(t)
  return string.format('%d:%02d', math.floor(s / 60), s % 60)
end

local function loadbest()
  local ok, v = pcall(var.recall, 'sdkbest' .. G.diff)
  G.best = (ok and type(v) == 'number') and v or 0
end

local function savebest()
  pcall(var.store, 'sdkbest' .. G.diff, G.best)
  pcall(document.markChanged)
end

local function shuffle(t)
  for i = #t, 2, -1 do
    local j = math.random(1, i)
    t[i], t[j] = t[j], t[i]
  end
end

-- solver: used[k] marks digit d used in row r (k = r*10+d), column
-- (100 + c*10 + d) or box (200 + b*10 + d)
local function mark(u, i, d, v)
  u[ROW[i] * 10 + d] = v
  u[100 + COL[i] * 10 + d] = v
  u[200 + BOX[i] * 10 + d] = v
end

local function free(u, i, d)
  return not (u[ROW[i] * 10 + d] or u[100 + COL[i] * 10 + d] or u[200 + BOX[i] * 10 + d])
end

-- count solutions of g up to limit; on reaching the limit g is left
-- holding the last solution found (random order when rand)
local function search(g, u, limit, rand)
  local best, bestn, opts = nil, 10, nil
  for i = 1, 81 do
    if g[i] == 0 then
      local o, n = {}, 0
      for d = 1, 9 do
        if free(u, i, d) then
          n = n + 1
          o[n] = d
        end
      end
      if n == 0 then return 0 end
      if n < bestn then
        best, bestn, opts = i, n, o
        if n == 1 then break end
      end
    end
  end
  if not best then return 1 end
  if rand then shuffle(opts) end
  local count = 0
  for k = 1, bestn do
    local d = opts[k]
    g[best] = d
    mark(u, best, d, true)
    count = count + search(g, u, limit - count, rand)
    if count >= limit then return count end
    mark(u, best, d, nil)
  end
  g[best] = 0
  return count
end

local function solutions(grid, limit, rand)
  local g, u = {}, {}
  for i = 1, 81 do
    g[i] = grid[i]
    if g[i] ~= 0 then mark(u, i, g[i], true) end
  end
  return search(g, u, limit, rand), g
end

-- squares holding the same digit as another square they share a line with
local function conflicts()
  local bad = {}
  for i = 1, 81 do
    local d = G.grid[i]
    if d ~= 0 then
      local p = PEERS[i]
      for k = 1, 20 do
        if G.grid[p[k]] == d then
          bad[i] = true
          break
        end
      end
    end
  end
  return bad
end

local function solved()
  for i = 1, 81 do
    if G.grid[i] ~= G.sol[i] then return false end
  end
  return true
end

-- start making a puzzle: a random full grid, then squares are taken out
-- in mirrored pairs (a few per tick) while the solution stays unique, then
-- single squares (negative entries in order) if more must go
local function newpuzzle()
  math.randomseed(timer.getMilliSecCounter())
  local empty = {}
  for i = 1, 81 do empty[i] = 0 end
  local _, full = solutions(empty, 1, true)
  G.sol = full
  G.grid = {}
  for i = 1, 81 do G.grid[i] = full[i] end
  local order, single = {}, {}
  for i = 1, 41 do order[i] = i end
  for i = 1, 81 do single[i] = -i end
  shuffle(order)
  shuffle(single)
  for i = 1, 81 do order[41 + i] = single[i] end
  G.gen = {order = order, k = 1, left = 81}
  G.state = 'gen'
end

local function ready()
  G.gen = nil
  G.given, G.notes = {}, {}
  for i = 1, 81 do
    G.given[i] = G.grid[i] ~= 0
    G.notes[i] = {}
  end
  G.cur, G.pencil, G.ticks, G.hints, G.record = 41, false, 0, 0, false
  loadbest()
  G.state = 'play'
end

local function makestep()
  local gen = G.gen
  local stop = timer.getMilliSecCounter() + BUDGET
  repeat
    if gen.k > #gen.order or gen.left <= GIVENS[G.diff] then
      ready()
      return
    end
    local i = gen.order[gen.k]
    local j = 82 - i
    if i < 0 then i, j = -i, -i end
    gen.k = gen.k + 1
    local a, b = G.grid[i], G.grid[j]
    if a ~= 0 and b ~= 0 then
      G.grid[i], G.grid[j] = 0, 0
      if solutions(G.grid, 2) == 1 then
        gen.left = gen.left - (i == j and 1 or 2)
      else
        G.grid[i], G.grid[j] = a, b
      end
    end
  until timer.getMilliSecCounter() >= stop
end

local function finish()
  local t = math.floor(G.ticks * TICK) + G.hints * PENALTY
  G.time = t
  if G.best == 0 or t < G.best then
    G.best = t
    G.record = true
    savebest()
  end
  G.state = 'done'
end

local function write(d)
  local i = G.cur
  if G.given[i] then return end
  if G.pencil and d ~= 0 then
    if G.grid[i] == 0 then G.notes[i][d] = not G.notes[i][d] or nil end
    return
  end
  G.grid[i] = d
  if d ~= 0 then
    G.notes[i] = {}
    -- the digit is no longer a candidate next to it
    local p = PEERS[i]
    for k = 1, 20 do G.notes[p[k]][d] = nil end
    if solved() then finish() end
  end
end

local function hint()
  local i = G.cur
  if G.given[i] or G.grid[i] == G.sol[i] then return end
  G.hints = G.hints + 1
  local pen = G.pencil
  G.pencil = false
  write(G.sol[i])
  G.pencil = pen
end

function on.timer()
  if G.state == 'gen' then
    makestep()
    platform.window:invalidate()
  elseif G.state == 'play' then
    local before = math.floor(G.ticks * TICK)
    G.ticks = G.ticks + 1
    if math.floor(G.ticks * TICK) ~= before then platform.window:invalidate() end
  end
end

local MOVE = {up = -9, down = 9, left = -1, right = 1}

function on.arrowKey(k)
  if G.state == 'title' then
    if k == 'left' or k == 'right' then
      G.diff = (G.diff + (k == 'right' and 1 or -1) + 2) % 3 + 1
      loadbest()
    end
  elseif G.state == 'play' then
    local r, c = ROW[G.cur], COL[G.cur]
    if k == 'up' then r = (r + 7) % 9 + 1 end
    if k == 'down' then r = r % 9 + 1 end
    if k == 'left' then c = (c + 7) % 9 + 1 end
    if k == 'right' then c = c % 9 + 1 end
    G.cur = (r - 1) * 9 + c
  end
  platform.window:invalidate()
end

function on.charIn(ch)
  if G.state ~= 'play' then return end
  local d = tonumber(ch)
  if d and d >= 0 and d <= 9 and #ch == 1 then
    write(d)
  elseif ch == 'n' then
    G.pencil = not G.pencil
  elseif ch == 'h' then
    hint()
  end
  platform.window:invalidate()
end

local function erase()
  if G.state == 'play' then
    if G.grid[G.cur] == 0 and not G.given[G.cur] then
      G.notes[G.cur] = {}
    else
      write(0)
    end
    platform.window:invalidate()
  end
end

on.backspaceKey = erase
on.clearKey = erase
on.deleteKey = erase

local function toggle()
  if G.state == 'play' then
    G.pencil = not G.pencil
    platform.window:invalidate()
  end
end

on.tabKey = toggle

function on.enterKey()
  local s = G.state
  if s == 'title' or s == 'done' then
    newpuzzle()
  elseif s == 'play' then
    toggle()
  elseif s == 'pause' then
    G.state = 'play'
  end
  platform.window:invalidate()
end

function on.escapeKey()
  local s = G.state
  if s == 'play' then
    G.state = 'pause'
  elseif s == 'pause' or s == 'done' or s == 'gen' then
    G.state = 'title'
    G.gen = nil
    loadbest()
  end
  platform.window:invalidate()
end

function on.activate() timer.start(TICK) end

function on.deactivate()
  if G.state == 'play' then G.state = 'pause' end
end

local function sx(i) return X0 + (COL[i] - 1) * CELL end
local function sy(i) return Y0 + (ROW[i] - 1) * CELL end

local function board(gc, hide)
  color(gc, PAPER)
  gc:fillRect(X0, Y0, 9 * CELL, 9 * CELL)
  local cur = G.cur
  local d0 = G.grid[cur]
  if not hide then
    for i = 1, 81 do
      local c
      if i == cur then
        c = CURSOR
      elseif d0 ~= 0 and G.grid[i] == d0 then
        c = SAME
      elseif ROW[i] == ROW[cur] or COL[i] == COL[cur] or BOX[i] == BOX[cur] then
        c = BAND
      end
      if c then
        color(gc, c)
        gc:fillRect(sx(i), sy(i), CELL, CELL)
      end
    end
    local bad = conflicts()
    for i = 1, 81 do
      local d = G.grid[i]
      if d ~= 0 then
        font(gc, 12, G.given[i] and 'b' or 'r')
        color(gc, bad[i] and BAD or (G.given[i] and INK or PEN))
        local s = tostring(d)
        gc:drawString(s, sx(i) + math.floor((CELL - gc:getStringWidth(s)) / 2), sy(i) + 3, 'top')
      else
        font(gc, 7)
        color(gc, DIM)
        for n = 1, 9 do
          if G.notes[i][n] then
            gc:drawString(tostring(n), sx(i) + 2 + ((n - 1) % 3) * 7, sy(i) + 1 + math.floor((n - 1) / 3) * 7, 'top')
          end
        end
      end
    end
  end
  for k = 0, 9 do
    color(gc, k % 3 == 0 and INK or THIN)
    local w = k % 3 == 0 and 2 or 1
    local p = k * CELL - (k == 9 and 1 or 0)
    gc:fillRect(X0 + p, Y0, w, 9 * CELL)
    gc:fillRect(X0, Y0 + p, 9 * CELL, w)
  end
end

local function side(gc)
  local x = 214
  color(gc, INK)
  font(gc, 12, 'b')
  gc:drawString('SUDOKU', x, 6, 'top')
  font(gc, 10)
  color(gc, DIM)
  gc:drawString(LEVELS[G.diff], x, 24, 'top')
  color(gc, INK)
  font(gc, 16, 'b')
  local t = math.floor(G.ticks * TICK) + G.hints * PENALTY
  gc:drawString(clock(G.state == 'done' and G.time or t), x, 40, 'top')
  font(gc, 9)
  color(gc, DIM)
  gc:drawString('Best ' .. (G.best > 0 and clock(G.best) or '-'), x, 64, 'top')
  if G.hints > 0 then gc:drawString('Hints ' .. G.hints, x, 76, 'top') end
  color(gc, G.pencil and PEN or INK)
  gc:fillRect(x, 92, 96, 18)
  color(gc, PAPER)
  font(gc, 10, 'b')
  centre(gc, G.pencil and 'Notes' or 'Pen', 94, x, 96)
  font(gc, 9)
  color(gc, DIM)
  local help = {'1-9  write', '0 del  erase', 'Enter  pen/notes', 'h  hint (+30 s)', 'Esc  pause'}
  for i = 1, #help do gc:drawString(help[i], x, 120 + (i - 1) * 16, 'top') end
end

local function panel(gc, lines)
  color(gc, PAPER)
  gc:fillRect(25, 70, 160, 72)
  color(gc, INK)
  gc:drawRect(25, 70, 160, 72)
  font(gc, 16, 'b')
  centre(gc, lines[1], 76, 25, 160)
  font(gc, 10)
  for i = 2, #lines do centre(gc, lines[i], 70 + i * 16, 25, 160) end
end

local function title(gc)
  local demo = {5, 3, 0, 0, 7, 0, 0, 0, 0, 6, 0, 0, 1, 9, 5, 0, 0, 0, 0, 9, 8, 0, 0, 0, 0, 6, 0}
  for k = 1, 27 do
    local x, y = 78 + ((k - 1) % 9) * 18, 56 + math.floor((k - 1) / 9) * 18
    color(gc, PAPER)
    gc:fillRect(x, y, 17, 17)
    if demo[k] > 0 then
      color(gc, INK)
      font(gc, 10, 'b')
      gc:drawString(tostring(demo[k]), x + 5, y + 2, 'top')
    end
  end
  color(gc, PAPER)
  font(gc, 24, 'b')
  centre(gc, 'SUDOKU', 14)
  color(gc, PEN)
  gc:fillRect(84, 120, 150, 20)
  color(gc, PAPER)
  font(gc, 12)
  centre(gc, 'Level:  < ' .. LEVELS[G.diff] .. ' >', 122)
  font(gc, 10)
  centre(gc, 'Best time ' .. (G.best > 0 and clock(G.best) or '-'), 148)
  font(gc, 9)
  centre(gc, 'Enter: new puzzle    arrows: move    1-9: write', 174)
  centre(gc, 'Enter: pen / notes    h: hint    Esc: pause', 190)
end

function on.paint(gc)
  if G.state == 'title' then
    color(gc, {40, 52, 72})
    gc:fillRect(0, 0, 318, 212)
    title(gc)
    return
  end
  color(gc, {232, 230, 222})
  gc:fillRect(0, 0, 318, 212)
  board(gc, G.state == 'gen' or G.state == 'pause')
  side(gc)
  if G.state == 'gen' then
    local done = G.gen and (81 - G.gen.left) / (81 - GIVENS[G.diff]) or 1
    panel(gc, {'Making puzzle', '', ''})
    color(gc, THIN)
    gc:fillRect(45, 110, 120, 10)
    color(gc, PEN)
    gc:fillRect(45, 110, math.floor(120 * math.min(1, done)), 10)
  elseif G.state == 'pause' then
    panel(gc, {'PAUSED', 'Enter: resume', 'Esc: title'})
  elseif G.state == 'done' then
    panel(gc, {'SOLVED', 'Time ' .. clock(G.time) .. (G.record and '  New best!' or ''),
               'Enter: new   Esc: title'})
  end
end

loadbest()
timer.start(TICK)
