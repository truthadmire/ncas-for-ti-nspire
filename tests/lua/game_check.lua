-- Checks for the Lua games, run on the mock TI API (tests/lua/mock_ti.lua):
--   luajit tests/lua/game_check.lua
package.path = 'tests/lua/?.lua;' .. package.path
local T = require('mock_ti')

local passed, failed = 0, 0

local function check(name, ok, info)
  if ok then
    passed = passed + 1
  else
    failed = failed + 1
    print('FAIL ' .. name .. (info and ('  ' .. tostring(info)) or ''))
  end
end

local function clean(name, g)
  check(name .. ': no drawing errors', #g.errors == 0, g.errors[1])
end

local function has(g, s)
  return string.find(T.text(g), s, 1, true) ~= nil
end

-- snake --------------------------------------------------------------------

local SNAKE = 'games/lua/snake.lua'

local function snake(vars)
  local g = T.load(SNAKE, vars)
  return g, g.env.G
end

do
  local g, G = snake()
  check('snake title', has(g, 'SNAKE') and has(g, 'Normal') and has(g, 'Walls'), T.text(g))
  T.key(g, 'right')
  check('snake title mode', G.mode == 2 and has(g, 'Wrap'))
  T.key(g, 'down')
  T.key(g, 'right')
  check('snake title speed', G.speed == 3 and has(g, 'Fast'))
  T.key(g, 'left')
  T.key(g, 'left')
  check('snake title speed wraps', G.speed == 1)
  clean('snake title', g)
end

do
  local g, G = snake()
  T.key(g, 'enter')
  check('snake starts', G.state == 'play' and #G.body == 4)
  local x = G.body[1].x
  T.tick(g, 4)
  check('snake moves one cell per 4 ticks', G.body[1].x == x + 1, G.body[1].x)
  T.key(g, 'left')
  T.tick(g, 4)
  check('snake ignores reversing', G.dir == 'right' and G.body[1].x == x + 2)
  T.key(g, '8')
  T.tick(g, 4)
  check('snake turns with 8', G.dir == 'up' and G.body[1].x == x + 2)
  T.key(g, 'enter')
  local y = G.body[1].y
  T.tick(g, 20)
  check('snake pauses', G.state == 'pause' and G.body[1].y == y and has(g, 'PAUSED'))
  T.key(g, 'enter')
  T.tick(g, 200)
  check('snake hits the wall', G.state == 'over' and has(g, 'GAME OVER'), G.state)
  clean('snake wall', g)
end

do
  local g, G = snake()
  T.key(g, 'enter')
  local h = G.body[1]
  G.food = {x = h.x + 1, y = h.y}
  T.tick(g, 4)
  check('snake eats', G.score == 10 and #G.body == 5 and G.eaten == 1, G.score)
  check('snake new food is free', G.food and not G.occ[G.food.y * 31 + G.food.x])
  T.key(g, 'esc')
  check('snake esc pauses', G.state == 'pause')
  T.key(g, 'enter')
  -- grow, then fold back on itself: up, left, down
  G.grow = 6
  T.tick(g, 24)
  T.key(g, 'up')
  T.tick(g, 4)
  T.key(g, 'left')
  T.tick(g, 4)
  T.key(g, 'down')
  T.tick(g, 4)
  check('snake hits itself', G.state == 'crash', G.state)
  T.tick(g, 25)
  check('snake game over screen', G.state == 'over' and has(g, 'New best!'), T.text(g))
  check('snake saves the best', g.vars.snkbest2 == 10 and g.changed, g.vars.snkbest2)
  local g2, G2 = snake(g.vars)
  check('snake best is read back', G2.best == 10 and has(g2, 'Best 10'), G2.best)
  T.key(g, 'esc')
  check('snake back to title', G.state == 'title')
  clean('snake self', g)
end

do
  local g, G = snake()
  T.key(g, 'right')
  T.key(g, 'enter')
  T.key(g, 'up')
  T.tick(g, 4 * 12)
  local y = G.body[1].y
  check('snake wraps top to bottom', G.state == 'play' and y > 9, y)
  clean('snake wrap', g)
end

do
  -- one free cell left: eating the food there wins
  local g, G = snake()
  T.key(g, 'enter')
  local h = G.body[1]
  for y = 0, 18 do
    for x = 0, 30 do G.occ[y * 31 + x] = true end
  end
  G.occ[h.y * 31 + h.x + 1] = nil
  G.food = {x = h.x + 1, y = h.y}
  T.tick(g, 4)
  check('snake fills the board', G.state == 'over' and G.win and has(g, 'YOU WIN'), G.state)
end

do
  local g, G = snake()
  T.key(g, 'enter')
  G.eaten = 30
  local t = 0
  local x = G.body[1].x
  while G.body[1].x == x do
    T.tick(g, 1)
    t = t + 1
  end
  check('snake speeds up', t == 2, t)
end

-- blocks ------------------------------------------------------------------

local function blocks(vars)
  local g = T.load('games/lua/blocks.lua', vars)
  return g, g.env.G
end

-- put piece p at rotation r, column x, row y as the current piece
local function setpiece(G, p, r, x, y)
  G.cur = {p = p, r = r or 0, x = x or 4, y = y or 1}
end

local function fill(G, y, gap)
  for x = 1, 10 do G.board[y][x] = (x == gap) and 0 or 'J' end
end

do
  local g, G = blocks()
  check('blocks title', has(g, 'BLOCKS') and has(g, 'Level:  < 1 >'), T.text(g))
  T.key(g, 'left')
  check('blocks start level wraps', G.start == 10)
  T.key(g, 'right')
  T.key(g, 'right')
  check('blocks start level', G.start == 2)
  T.key(g, 'enter')
  check('blocks starts', G.state == 'play' and G.level == 2 and G.cur ~= nil)
  -- 7-bag: the first 7 pieces (current, queue, rest of the bag) are all different
  local seen = {G.cur.p}
  for _, p in ipairs(G.queue) do seen[#seen + 1] = p end
  for _, p in ipairs(G.bag) do seen[#seen + 1] = p end
  local n = 0
  local set = {}
  for _, p in ipairs(seen) do if not set[p] then set[p] = true; n = n + 1 end end
  check('blocks 7-bag', n == 7, table.concat(seen))
  clean('blocks title', g)
end

do
  local g, G = blocks()
  T.key(g, 'enter')
  -- an I piece standing up drops into a one-wide gap and clears 4 rows
  for y = 19, 22 do fill(G, y, 10) end
  setpiece(G, 'I', 1, 8, 1)
  T.key(g, 'enter')
  check('blocks flash before clearing', G.flash > 0 and #G.rows == 4, #G.rows)
  T.tick(g, 6)
  local empty = true
  for y = 1, 22 do for x = 1, 10 do if G.board[y][x] ~= 0 then empty = false end end end
  check('blocks tetris clears', empty and G.lines == 4, G.lines)
  check('blocks tetris score', G.score >= 800 and G.score < 900, G.score)
  check('blocks next piece after clear', G.cur ~= nil and G.flash == 0)
  clean('blocks clear', g)
end

do
  local g, G = blocks()
  T.key(g, 'enter')
  -- T piece against the left wall still turns (kick)
  setpiece(G, 'T', 1, 0, 10)
  T.key(g, 'up')
  check('blocks turn kicks off the wall', G.cur.r == 2 and G.cur.x >= 1, G.cur.r .. ' ' .. G.cur.x)
  T.key(g, '7')
  check('blocks turn back', G.cur.r == 1, G.cur.r)
  -- O never turns
  setpiece(G, 'O', 0, 5, 5)
  T.key(g, 'up')
  check('blocks O does not turn', G.cur.r == 0)
  -- moving stops at walls
  for _ = 1, 12 do T.key(g, 'left') end
  check('blocks wall left', G.cur.x == 1, G.cur.x)
  for _ = 1, 12 do T.key(g, '6') end
  check('blocks wall right', G.cur.x == 9, G.cur.x)
end

do
  local g, G = blocks()
  T.key(g, 'enter')
  local first = G.cur.p
  local nxt = G.queue[1]
  T.key(g, 'tab')
  check('blocks hold', G.hold == first and G.cur.p == nxt and not G.canhold)
  T.key(g, '0')
  check('blocks hold once per piece', G.hold == first and G.cur.p == nxt)
  T.key(g, '5')
  T.key(g, 'tab')
  check('blocks hold swaps back', G.cur.p == first, G.cur.p)
end

do
  local g, G = blocks()
  T.key(g, 'enter')
  setpiece(G, 'O', 0, 5, 1)
  local y = G.cur.y
  T.key(g, 'down')
  check('blocks soft drop', G.cur.y == y + 1 and G.score == 1)
  T.tick(g, 16)
  check('blocks gravity at level 1', G.cur.y == y + 2, G.cur.y)
  -- a piece on the ground locks after LOCK ticks
  setpiece(G, 'O', 0, 5, 21)
  T.tick(g, 11)
  check('blocks locks on the ground', G.board[22][5] == 'O' and G.cur.y < 5)
  -- 10 lines raise the level
  G.lines = 9
  fill(G, 22, 1)
  setpiece(G, 'I', 1, -1, 1)
  T.key(g, 'enter')
  T.tick(g, 6)
  check('blocks level up', G.lines == 10 and G.level == 2, G.level)
  clean('blocks gravity', g)
end

do
  local g, G = blocks()
  T.key(g, 'enter')
  for y = 3, 22 do fill(G, y, (y % 2) + 3) end
  setpiece(G, 'O', 0, 5, 1)
  G.score = 500
  T.key(g, 'enter')
  check('blocks tops out', G.state == 'over' and has(g, 'GAME OVER'), G.state)
  check('blocks saves best', g.vars.blkbest == G.score and G.score > 0, g.vars.blkbest)
  T.key(g, 'esc')
  check('blocks back to title', G.state == 'title' and has(g, 'Best ' .. G.score))
  clean('blocks over', g)
end

-- bricks ------------------------------------------------------------------

local function bricks(vars)
  local g = T.load('games/lua/bricks.lua', vars)
  return g, g.env.G
end

do
  local g, G = bricks()
  check('bricks title', has(g, 'BRICKS') and has(g, 'Best 0'), T.text(g))
  T.key(g, 'enter')
  check('bricks serve', G.state == 'serve' and G.left == 50, G.left)
  local px = G.px
  T.key(g, 'right')
  T.tick(g, 20)
  local glide = G.px - px
  check('bricks bat glides and stops', glide > 15 and glide < 40 and G.pv == 0, glide)
  check('bricks ball rides the bat', math.abs(G.x + 2 - G.px) < 0.01)
  for _ = 1, 30 do T.key(g, '4') T.tick(g, 1) end
  check('bricks bat stops at the wall', G.px == 2 + 22, G.px)
  T.key(g, 'enter')
  check('bricks launch', G.state == 'play' and G.vy < 0)
  clean('bricks serve', g)
end

do
  local g, G = bricks()
  T.key(g, 'enter')
  T.key(g, 'enter')
  -- straight up under brick row 5, column 3 (hp 1)
  G.x, G.y, G.vx, G.vy, G.speed = 4 + 2 * 31 + 10, 90, 0, -3, 3
  local left, score = G.left, G.score
  for _ = 1, 10 do T.tick(g, 1) end
  check('bricks breaks a brick', G.bricks[5][3] == 0 and G.left == left - 1 and G.vy > 0, G.left)
  check('bricks scores', G.score == score + 20, G.score)
  -- a 3-hit brick takes 3 hits
  G.bricks[4][3], G.bricks[3][3], G.bricks[2][3], G.bricks[1][3] = 0, 0, 0, 3
  local hits = 0
  for _ = 1, 3 do
    G.x, G.y, G.vx, G.vy = 4 + 2 * 31 + 10, 60, 0, -3
    for _ = 1, 20 do T.tick(g, 1) end
    hits = hits + 1
  end
  check('bricks 3 hits', G.bricks[1][3] == 0, G.bricks[1][3])
  -- the bat sends the ball the way it was hit
  G.px = 150
  G.x, G.y, G.vx, G.vy = 150 + 15, 186, 0, 3
  T.tick(g, 3)
  check('bricks right side of the bat sends right', G.vx > 0 and G.vy < 0, G.vx)
  G.x, G.y, G.vx, G.vy = 150 - 19, 186, 0, 3
  T.tick(g, 3)
  check('bricks left side of the bat sends left', G.vx < 0 and G.vy < 0, G.vx)
  -- a miss costs a life
  G.x, G.y, G.vx, G.vy = 20, 205, 0, 3
  G.px = 200
  T.tick(g, 4)
  check('bricks miss loses a life', G.lives == 2 and G.state == 'serve', G.lives)
  clean('bricks hits', g)
end

do
  local g, G = bricks()
  T.key(g, 'enter')
  T.key(g, 'enter')
  G.level = 2
  for r = 1, #G.bricks do for c = 1, 10 do G.bricks[r][c] = 0 end end
  G.bricks[1][1], G.bricks[2][2], G.left = 1, -1, 1
  G.x, G.y, G.vx, G.vy = 4 + 10, 60, 0, -3
  for _ = 1, 15 do T.tick(g, 1) end
  check('bricks level clear', G.state == 'clear' and has(g, 'LEVEL 2 CLEAR'), G.state)
  T.tick(g, 30)
  check('bricks next layout', G.state == 'serve' and G.level == 3 and G.left == 30, G.left)
  -- steel never breaks; lose all lives
  G.lives = 1
  T.key(g, 'enter')
  G.x, G.y, G.vx, G.vy = 20, 205, 0, 3
  G.px = 200
  T.tick(g, 4)
  check('bricks game over', G.state == 'over' and has(g, 'GAME OVER') and g.vars.brkbest == G.score)
  clean('bricks levels', g)
end

do
  -- steel bricks bounce the ball but stay
  local g, G = bricks()
  T.key(g, 'enter')
  G.level = 2
  T.key(g, 'esc')
  T.key(g, 'esc')
  T.key(g, 'enter')
  check('bricks restart', G.level == 1)
  G.bricks[4][2] = -1
  G.bricks[5][2] = 0
  G.x, G.y, G.vx, G.vy, G.state, G.speed = 4 + 31 + 10, 90, 0, -3, 'play', 3
  for _ = 1, 10 do T.tick(g, 1) end
  check('bricks steel stays', G.bricks[4][2] == -1 and G.vy > 0)
end

-- rally -------------------------------------------------------------------

local function rally(vars, seed)
  local g = T.load('games/lua/rally.lua', vars, seed)
  return g, g.env.G
end

do
  local g, G = rally()
  check('rally title', has(g, 'RALLY') and has(g, 'Normal') and has(g, 'Games won: 0'), T.text(g))
  T.key(g, 'right')
  check('rally difficulty', G.diff == 3 and has(g, 'Hard'))
  T.key(g, '6')
  check('rally difficulty wraps', G.diff == 1 and has(g, 'Easy'))
  T.key(g, 'enter')
  check('rally serve waits', G.state == 'serve' and G.vx == 0)
  T.tick(g, 20)
  check('rally serves', G.state == 'play' and G.vx ~= 0)
  local py = G.py
  T.key(g, 'down')
  T.tick(g, 20)
  check('rally bat glides', G.py > py + 15 and G.pv == 0, G.py - py)
  for _ = 1, 40 do T.key(g, '8') T.tick(g, 1) end
  check('rally bat stops at the top', G.py == 15, G.py)
  clean('rally start', g)
end

do
  local g, G = rally()
  T.key(g, 'enter')
  T.tick(g, 20)
  -- ball comes at the middle of your bat
  G.py, G.pv = 100, 0
  G.x, G.y, G.vx, G.vy, G.speed = 30, 113, -3, 0, 3
  T.tick(g, 8)
  check('rally your bat returns the ball', G.vx > 0 and G.me == 0 and G.cpu == 0, G.vx)
  check('rally ball speeds up', G.speed > 3)
  -- ball far from your bat: the calculator scores, then serves to you
  G.py = 15
  G.x, G.y, G.vx, G.vy, G.speed = 30, 180, -3, 0, 3
  T.tick(g, 12)
  check('rally a miss is a point', G.cpu == 1 and G.state == 'serve' and G.toward == -1, G.cpu)
  -- bounces off the top wall
  G.state = 'play'
  G.x, G.y, G.vx, G.vy, G.speed = 150, 17, 1, -3, 3
  T.tick(g, 2)
  check('rally wall bounce', G.vy > 0 and G.y >= 15, G.y)
  clean('rally points', g)
end

-- play whole games with a bat that always gets there: count who wins and
-- how often the calculator returns the ball
local function match(diff, seed, perfect)
  local g, G = rally({}, seed)
  G.diff = diff
  T.key(g, 'enter')
  local returns, chances = 0, 0
  local going = false
  for _ = 1, 20000 do
    if perfect then G.py = math.max(15, math.min(182, G.y + 2 - 15 + math.random(-12, 12))) end
    local before = G.vx
    T.tick(g, 1)
    if G.state == 'over' then break end
    if before > 0 and G.x > 250 then going = true end
    if going and G.vx < 0 then returns, chances, going = returns + 1, chances + 1, false end
    if going and G.state == 'serve' then chances, going = chances + 1, false end
  end
  return G, returns, chances
end

do
  local won = 0
  for seed = 1, 5 do
    local G = match(1, seed, true)
    if G.won then won = won + 1 end
  end
  check('rally easy can be beaten', won >= 4, won)
  local r, c = 0, 0
  for seed = 1, 5 do
    local _, rr, cc = match(3, seed, true)
    r, c = r + rr, c + cc
  end
  check('rally hard returns most balls', c > 0 and r / c > 0.7, r .. '/' .. c)
  local G, _, _ = match(2, 9, false)
  check('rally calculator beats a still bat', G.state == 'over' and not G.won and G.cpu == 7)
  local g, G2 = rally({}, 4)
  G2.diff = 1
  T.key(g, 'enter')
  G2.me = 6
  G2.state, G2.x, G2.y, G2.vx, G2.vy, G2.speed, G2.cy = 'play', 300, 20, 3, 0, 3, 150
  T.tick(g, 10)
  check('rally win saves', G2.state == 'over' and G2.won and g.vars.rlywins1 == 1 and has(g, 'YOU WIN'))
end

-- sudoku ------------------------------------------------------------------

local function sudoku(vars, seed)
  local g = T.load('games/lua/sudoku.lua', vars, seed)
  return g, g.env.G
end

-- count solutions (up to 2) with plain backtracking, independent of the game
local function count(grid)
  local g = {}
  for i = 1, 81 do g[i] = grid[i] end
  local function ok(i, d)
    local r, c = math.floor((i - 1) / 9), (i - 1) % 9
    for k = 0, 8 do
      if g[r * 9 + k + 1] == d or g[k * 9 + c + 1] == d then return false end
    end
    local br, bc = r - r % 3, c - c % 3
    for y = br, br + 2 do for x = bc, bc + 2 do if g[y * 9 + x + 1] == d then return false end end end
    return true
  end
  local n = 0
  local function go(i)
    if n >= 2 then return end
    while i <= 81 and g[i] ~= 0 do i = i + 1 end
    if i > 81 then n = n + 1 return end
    for d = 1, 9 do
      if ok(i, d) then g[i] = d; go(i + 1); g[i] = 0 end
    end
  end
  go(1)
  return n
end

local function valid(sol)
  for i = 1, 81 do
    local d = sol[i]
    if d < 1 or d > 9 then return false end
    sol[i] = 0
    local r, c = math.floor((i - 1) / 9), (i - 1) % 9
    for k = 0, 8 do
      if sol[r * 9 + k + 1] == d or sol[k * 9 + c + 1] == d then sol[i] = d return false end
    end
    sol[i] = d
  end
  return true
end

local function makesudoku(diff, seed)
  local g, G = sudoku({}, seed)
  G.diff = diff
  T.key(g, 'enter')
  local t = 0
  while G.state == 'gen' and t < 2000 do T.tick(g, 1) t = t + 1 end
  return g, G
end

do
  local g, G = sudoku()
  check('sudoku title', has(g, 'SUDOKU') and has(g, 'Medium') and has(g, 'Best time -'), T.text(g))
  T.key(g, 'left')
  check('sudoku level', G.diff == 1 and has(g, 'Easy'))
  clean('sudoku title', g)
  local most = {38, 30, 25}
  for diff = 1, 3 do
    for seed = 1, 4 do
      local g2, G2 = makesudoku(diff, seed * 31 + diff)
      local givens, match = 0, true
      for i = 1, 81 do
        if G2.grid[i] ~= 0 then
          givens = givens + 1
          if G2.grid[i] ~= G2.sol[i] then match = false end
        end
      end
      local name = 'sudoku level ' .. diff .. ' seed ' .. seed
      check(name .. ' ready', G2.state == 'play')
      check(name .. ' givens', givens <= most[diff] and givens >= 17, givens)
      check(name .. ' one solution', count(G2.grid) == 1)
      check(name .. ' solution valid', valid(G2.sol) and match)
      clean(name, g2)
    end
  end
end

do
  local g, G = makesudoku(1, 5)
  -- find an empty square and a given one
  local e, gv
  for i = 1, 81 do
    if G.grid[i] == 0 and not e then e = i end
    if G.given[i] and not gv then gv = i end
  end
  G.cur = gv
  local d = G.grid[gv]
  T.key(g, tostring(d % 9 + 1))
  check('sudoku given cannot change', G.grid[gv] == d)
  G.cur = e
  local right = G.sol[e]
  local wrong = right % 9 + 1
  -- a wrong digit that clashes in its row shows red
  local clash
  for k = 1, 9 do
    local j = (math.floor((e - 1) / 9)) * 9 + k
    if G.grid[j] ~= 0 and j ~= e then clash = G.grid[j] break end
  end
  T.key(g, tostring(clash))
  local red = false
  for _, op in ipairs(g.frames[#g.frames]) do
    if op[1] == 'text' and op[4] == tostring(clash) and op.col[1] == 215 and op.col[2] == 40 then red = true end
  end
  check('sudoku clash shown red', G.grid[e] == clash and red)
  T.key(g, 'del')
  check('sudoku erase', G.grid[e] == 0)
  -- notes
  T.key(g, 'enter')
  check('sudoku notes mode', G.pencil and has(g, 'Notes'))
  T.key(g, tostring(right))
  T.key(g, tostring(wrong))
  check('sudoku notes', G.grid[e] == 0 and G.notes[e][right] and G.notes[e][wrong])
  T.key(g, tostring(wrong))
  check('sudoku note off', G.notes[e][wrong] == nil)
  -- writing a digit next door clears that note
  local peer
  for i = 1, 81 do
    if i ~= e and G.grid[i] == 0 and math.floor((i - 1) / 9) == math.floor((e - 1) / 9) then peer = i break end
  end
  G.notes[peer][G.sol[peer]] = true
  G.notes[e][G.sol[peer]] = true
  T.key(g, 'tab')
  G.cur = peer
  T.key(g, tostring(G.sol[peer]))
  check('sudoku pen clears notes nearby', G.grid[peer] == G.sol[peer] and not G.notes[e][G.sol[peer]])
  -- hint fills in the right digit
  G.cur = e
  T.key(g, 'h')
  check('sudoku hint', G.grid[e] == right and G.hints == 1 and has(g, 'Hints 1'))
  -- cursor wraps
  G.cur = 1
  T.key(g, 'left')
  T.key(g, 'up')
  check('sudoku cursor wraps', G.cur == 81, G.cur)
  -- time runs, pause stops it
  T.tick(g, 25)
  local t = G.ticks
  T.key(g, 'esc')
  T.tick(g, 50)
  check('sudoku pause stops the clock', G.ticks == t and has(g, 'PAUSED'))
  T.key(g, 'enter')
  -- fill in everything else: solved
  for i = 1, 81 do
    if G.grid[i] == 0 then
      G.cur = i
      T.key(g, tostring(G.sol[i]))
    end
  end
  check('sudoku solved', G.state == 'done' and has(g, 'SOLVED'), G.state)
  check('sudoku best time saved', g.vars.sdkbest1 == G.time and G.time == 2 + 30, G.time)
  clean('sudoku play', g)
end

-- jumper ------------------------------------------------------------------

local function jumper(vars, seed)
  local g = T.load('games/lua/jumper.lua', vars, seed)
  return g, g.env.G
end

local function jsolid(G, c, r)
  if c < 1 or c > G.width then return true end
  if r < 1 or r > 16 then return false end
  local ch = G.map[r][c]
  return ch == '#' or ch == 'B' or ch == '?' or ch == 'P' or ch == 'U'
end

-- put the player standing in column c, on the first ground from row r0 down
local function stand(g, G, c, r0)
  local r = r0 or 1
  while r <= 16 and not jsolid(G, c, r) do r = r + 1 end
  local p = G.p
  p.x, p.y, p.vx, p.vy = (c - 1) * 12 + 1, (r - 1) * 12 - 11, 0, 0
  G.walk, G.hold, G.jumpbuf = 0, 0, 0
  T.tick(g, 2)
end

-- walk right, jumping at walls and gaps; enemies taken out
local function bot(g, G, limit)
  G.mode = 2
  local level = G.level
  for _ = 1, limit do
    if G.state ~= 'play' then return G.state end
    G.foes = {}
    local p = G.p
    if G.walk ~= 1 then T.key(g, 'right') end
    local ahead = math.floor((p.x + 9 + 5) / 12) + 1
    local foot = math.floor((p.y + 11) / 12) + 1
    local top = math.floor(p.y / 12) + 1
    local wall = jsolid(G, ahead, foot - 1) or jsolid(G, ahead, top)
    -- a pit: nothing to land on anywhere below (a step down is walked)
    local gap = true
    for r = foot, 16 do if jsolid(G, ahead, r) then gap = false end end
    if p.ground and (wall or gap) then T.key(g, 'up') end
    T.tick(g, 1)
  end
  return G.state
end

do
  local g, G = jumper()
  check('jumper title', has(g, 'JUMPER') and has(g, 'Tap'), T.text(g))
  T.key(g, 'right')
  check('jumper walk mode', G.mode == 2 and has(g, 'Keep going'))
  T.key(g, 'left')
  T.key(g, 'enter')
  T.tick(g, 5)
  check('jumper starts on the ground', G.state == 'play' and G.p.ground, G.p.y)
  check('jumper level 1 built', G.width == 163 and G.flag == 150, G.width)
  clean('jumper title', g)

  -- Tap: one press walks a short way and stops
  local x = G.p.x
  T.key(g, 'right')
  T.tick(g, 20)
  local d = G.p.x - x
  check('jumper tap walks a little', d > 18 and d < 30 and G.walk == 0, d)
  -- repeats keep walking
  x = G.p.x
  for _ = 1, 10 do T.key(g, '6') T.tick(g, 2) end
  check('jumper held key keeps walking', G.p.x - x > 45, G.p.x - x)
  -- jump height
  stand(g, G, 5)
  local y0, low = G.p.y, G.p.y
  T.key(g, 'up')
  for _ = 1, 30 do T.tick(g, 1) low = math.min(low, G.p.y) end
  check('jumper jumps 3+ tiles', y0 - low > 36 and y0 - low < 52 and G.p.ground, y0 - low)
  -- a jump pressed just before landing still happens
  T.key(g, 'up')
  T.tick(g, 12)
  local fall = 0
  while not G.p.ground and fall < 40 do
    if G.p.vy > 0 and G.p.y > y0 - 10 then T.key(g, '8') end
    T.tick(g, 1)
    fall = fall + 1
  end
  T.tick(g, 3)
  check('jumper jump buffer', G.p.vy < 0 or G.p.y < y0 - 5, G.p.y - y0)
end

do
  local g, G = jumper()
  T.key(g, 'right')
  T.key(g, 'enter')
  -- Keep going walks until stopped
  stand(g, G, 3)
  local x = G.p.x
  T.key(g, 'right')
  T.tick(g, 20)
  check('jumper keeps going', G.walk == 1 and G.p.x - x > 45, G.p.x - x)
  T.key(g, 'left')
  check('jumper back stops', G.walk == 0)
  T.key(g, 'left')
  check('jumper back again turns', G.walk == -1)
  T.key(g, 'down')
  check('jumper down stops', G.walk == 0)
  -- bump the ? block in column 17, row 11
  G.foes = {}
  stand(g, G, 17, 12)
  T.key(g, 'up')
  T.tick(g, 30)
  check('jumper ? block gives a coin', G.map[11][17] == 'U' and G.coins == 1 and G.score == 100, G.map[11][17])
  stand(g, G, 16, 12)
  G.p.x = 15 * 12 + 1
  T.key(g, 'up')
  T.tick(g, 30)
  check('jumper brick breaks', G.map[11][16] == '.' and G.score == 150, G.score)
  -- coins in the air
  stand(g, G, 10)
  T.key(g, 'up')
  T.tick(g, 30)
  check('jumper collects a coin', G.map[11][10] == '.' and G.coins == 2, G.coins)
  clean('jumper blocks', g)
end

do
  local g, G = jumper()
  T.key(g, 'enter')
  -- stomp: fall onto a walker
  stand(g, G, 26)
  local e = {x = G.p.x, y = G.p.y + 1, vx = 0, kind = 'E', dead = 0}
  G.foes = {e}
  G.p.y = G.p.y - 30
  G.p.vy = 3
  T.tick(g, 8)
  check('jumper stomps a walker', e.dead ~= 0 and G.state == 'play' and G.score == 100, e.dead)
  -- walking into a walker hurts
  stand(g, G, 30)
  G.foes = {{x = G.p.x + 12, y = G.p.y + 1, vx = -0.7, kind = 'E', dead = 0}}
  T.key(g, 'right')
  T.tick(g, 6)
  check('jumper walker hurts from the side', G.state == 'dead', G.state)
  T.tick(g, 31)
  check('jumper loses a life', G.state == 'play' and G.lives == 2 and G.p.x < 40, G.lives)
  -- spikies hurt even from above
  stand(g, G, 30)
  G.foes = {{x = G.p.x, y = G.p.y + 1, vx = 0, kind = 'K', dead = 0}}
  G.p.y = G.p.y - 30
  G.p.vy = 3
  T.tick(g, 8)
  check('jumper spiky hurts from above', G.state == 'dead')
  T.tick(g, 31)
  -- pits
  G.foes = {}
  stand(g, G, 30)
  T.key(g, 'right')
  T.tick(g, 40)
  check('jumper falls in a pit', G.state == 'dead', G.state)
  T.tick(g, 31)
  check('jumper game over', G.state == 'over' and has(g, 'GAME OVER'), G.state)
  clean('jumper hurts', g)
end

do
  local g, G = jumper()
  T.key(g, 'enter')
  -- walkers turn at walls and ledges and never leave their ground
  local ok = true
  for _ = 1, 400 do
    G.p.y = -100
    G.p.vy = 0
    G.p.x = 1
    T.tick(g, 1)
    G.state = 'play'
    for _, e in ipairs(G.foes) do
      local c = math.floor((e.x + 5) / 12) + 1
      local r = math.floor((e.y + 5) / 12) + 1
      if not jsolid(G, c, r + 1) or jsolid(G, c, r) then ok = false end
    end
  end
  check('jumper walkers stay on their ground', ok)
end

do
  local g, G = jumper()
  T.key(g, 'enter')
  for level = 1, 3 do
    local s = bot(g, G, 3000)
    check('jumper bot finishes level ' .. level, s == 'goal', s .. ' at x ' .. math.floor(G.p.x / 12 + 1))
    if s ~= 'goal' then break end
    T.tick(g, 40)
  end
  check('jumper wins after level 3', G.state == 'win' and has(g, 'YOU WIN!'), G.state)
  check('jumper best saved', g.vars.jmpbest == G.score and G.score > 0, g.vars.jmpbest)
  clean('jumper bot', g)
end

do
  local g, G = jumper()
  T.key(g, 'enter')
  stand(g, G, 85)
  T.tick(g, 1)
  check('jumper checkpoint', G.checked)
  G.foes = {}
  G.time = 1
  T.tick(g, 20)
  check('jumper time runs out', G.state == 'dead')
  T.tick(g, 31)
  check('jumper back at the checkpoint', G.state == 'play' and math.floor(G.p.x / 12) + 1 == 80, G.p.x)
end

-- every game pastes in one go: under 20,000 characters, plain ASCII
for _, name in ipairs({'snake', 'blocks', 'bricks', 'rally', 'sudoku', 'jumper'}) do
  local f = assert(io.open('games/lua/' .. name .. '.lua', 'rb'))
  local src = f:read('*a')
  f:close()
  check(name .. ' under 20,000 characters', #src < 20000, #src)
  check(name .. ' is ASCII', not string.find(src, '[\128-\255]'))
  check(name .. ' starts with the API level', string.sub(src, 1, 26) == "platform.apiLevel = '2.0'\n")
end

print(string.format('game_check: %d passed, %d failed', passed, failed))
if failed > 0 then os.exit(1) end
