-- Pictures of the Lua games for games/README.md, drawn from the mock TI
-- API (tests/lua/mock_ti.lua) as SVG files in games/img. They are
-- simulated screens: the calculator's font differs.
--   luajit tools/game_shots.lua
package.path = 'tests/lua/?.lua;' .. package.path
local T = require('mock_ti')

local function esc(s)
  return (s:gsub('&', '&amp;'):gsub('<', '&lt;'):gsub('>', '&gt;'))
end

local function rgb(c) return string.format('rgb(%d,%d,%d)', c[1], c[2], c[3]) end

local function svg(ops, path)
  local o = {string.format('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">',
                           T.W * 2, T.H * 2, T.W, T.H)}
  for _, op in ipairs(ops) do
    local k, c = op[1], rgb(op.col)
    if k == 'rect' then
      o[#o + 1] = string.format('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>', op[2], op[3], op[4], op[5], c)
    elseif k == 'frame' then
      o[#o + 1] = string.format('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="%s"/>',
                                op[2] + 0.5, op[3] + 0.5, op[4], op[5], c)
    elseif k == 'oval' or k == 'ring' then
      o[#o + 1] = string.format('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" %s="%s"/>', op[2] + op[4] / 2,
                                op[3] + op[5] / 2, op[4] / 2, op[5] / 2, k == 'oval' and 'fill' or 'fill="none" stroke', c)
    elseif k == 'line' then
      o[#o + 1] = string.format('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s"/>', op[2], op[3], op[4], op[5], c)
    elseif k == 'poly' then
      local p = {}
      for i = 1, #op[2], 2 do p[#p + 1] = op[2][i] .. ',' .. op[2][i + 1] end
      o[#o + 1] = string.format('<polygon points="%s" fill="%s"/>', table.concat(p, ' '), c)
    elseif k == 'text' then
      o[#o + 1] = string.format('<text xml:space="preserve" x="%g" y="%g" font-family="Helvetica, Arial, sans-serif" font-size="%g"%s fill="%s">%s</text>',
                                op[2], op[3] + op[5] * 0.95, op[5], op[6]:find('b') and ' font-weight="bold"' or '', c, esc(op[4]))
    end
  end
  o[#o + 1] = '</svg>\n'
  local f = assert(io.open(path, 'w'))
  f:write(table.concat(o, '\n'))
  f:close()
  print(path)
end

local function last(g) return g.frames[#g.frames] end

local SHOTS = {
  snake = function(shot)
    local g = T.load('games/lua/snake.lua', {snkbest2 = 240}, 3)
    shot(g, 'title')
    T.key(g, 'enter')
    local G = g.env.G
    -- a few meals along a winding path
    local path = {'right', 'down', 'right', 'up', 'right', 'up', 'right', 'down', 'right'}
    for i, d in ipairs(path) do
      T.key(g, d)
      for _ = 1, 3 do
        local h = G.body[1]
        G.food = {x = h.x + (d == 'right' and 1 or d == 'left' and -1 or 0),
                  y = h.y + (d == 'down' and 1 or d == 'up' and -1 or 0)}
        -- one move (the delay shrinks as it eats)
        while G.body[1] == h do T.tick(g, 1) end
      end
    end
    G.food = {x = 24, y = 5}
    G.bonus = {x = 6, y = 14, left = 45}
    T.tick(g, 1)
    shot(g, 'play')
  end,
  blocks = function(shot)
    local g = T.load('games/lua/blocks.lua', {blkbest = 12400}, 5)
    shot(g, 'title')
    T.key(g, 'enter')
    local G = g.env.G
    local rows = {'IIII.ZZ.OO', 'JJJ.SZZ.OO', 'LJ.SSTTTLL', 'LLL.T..ILL', 'OO.JJ..I.L', 'OO.J...I.L'}
    for k = 1, #rows do
      local y = 23 - k
      for x = 1, 10 do
        local ch = rows[k]:sub(x, x)
        G.board[y][x] = ch == '.' and 0 or ch
      end
    end
    G.cur = {p = 'T', r = 2, x = 4, y = 9}
    G.hold, G.score, G.lines, G.level = 'I', 4820, 23, 3
    T.key(g, 'left')
    shot(g, 'play')
  end,
  bricks = function(shot)
    local g = T.load('games/lua/bricks.lua', {brkbest = 2310}, 2)
    shot(g, 'title')
    T.key(g, 'enter')
    T.key(g, 'enter')
    local G = g.env.G
    local gone = {{5, 3}, {5, 4}, {4, 4}, {5, 8}, {4, 8}, {3, 8}, {5, 9}, {2, 6}}
    for _, b in ipairs(gone) do G.bricks[b[1]][b[2]] = 0 end
    G.bricks[1][2], G.bricks[2][5] = 1, 1
    G.x, G.y, G.vx, G.vy, G.speed, G.score, G.lives = 200, 120, 1.5, 2.5, 3, 340, 2
    G.px = 180
    T.tick(g, 1)
    shot(g, 'play')
  end,
  rally = function(shot)
    local g = T.load('games/lua/rally.lua', {rlywins2 = 4}, 3)
    shot(g, 'title')
    T.key(g, 'enter')
    local G = g.env.G
    T.tick(g, 20)
    G.me, G.cpu = 4, 3
    G.x, G.y, G.vx, G.vy, G.speed, G.py = 190, 70, 3, -1, 3.5, 120
    T.tick(g, 1)
    shot(g, 'play')
  end,
  sudoku = function(shot)
    local g = T.load('games/lua/sudoku.lua', {sdkbest2 = 742}, 11)
    shot(g, 'title')
    T.key(g, 'enter')
    local G = g.env.G
    while G.state == 'gen' do T.tick(g, 1) end
    -- a few answers and some pencil notes
    local n = 0
    for i = 1, 81 do
      if G.grid[i] == 0 and n < 12 and i % 3 == 0 then
        G.grid[i] = G.sol[i]
        n = n + 1
      end
    end
    for i = 1, 81 do
      if G.grid[i] == 0 and n < 16 then
        G.notes[i] = {[G.sol[i]] = true, [G.sol[i] % 9 + 1] = true}
        n = n + 1
      end
    end
    G.ticks = 2050
    G.cur = 41
    T.tick(g, 10)
    shot(g, 'play')
  end,
  jumper = function(shot)
    local g = T.load('games/lua/jumper.lua', {jmpbest = 8150}, 4)
    shot(g, 'title')
    T.key(g, 'enter')
    local G = g.env.G
    G.p.x, G.p.y = 13 * 12, 100
    G.p.vy = -2
    G.coins, G.score = 7, 1450
    G.map[11][17] = 'U'
    for _ = 1, 3 do T.tick(g, 1) end
    shot(g, 'play')
  end,
}

for name, run in pairs(SHOTS) do
  run(function(g, what) svg(last(g), 'games/img/' .. name .. '-' .. what .. '.svg') end)
end
