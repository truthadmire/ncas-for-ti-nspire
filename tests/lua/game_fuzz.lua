-- Random keys and timer ticks for every Lua game: no Lua errors, no
-- drawing errors, game state stays bounded.
--   luajit tests/lua/game_fuzz.lua [runs]
package.path = 'tests/lua/?.lua;' .. package.path
local T = require('mock_ti')

local GAMES = {'snake', 'blocks', 'bricks', 'rally', 'sudoku', 'jumper'}
local CHARS = {'2', '4', '6', '8', '5', '0', '1', '7', '9', 'p', 'n', 'h', 'c', 'z',
               'w', 'a', 's', 'd', 'x', ' '}

-- per-game invariants on the global G after every event
local INV = {
  snake = function(G)
    local n = 0
    for _ in pairs(G.occ) do n = n + 1 end
    if G.state == 'play' and n ~= #G.body then
      return 'occupied cells ' .. n .. ' ~= body ' .. #G.body
    end
    if #G.q > 3 then return 'turn queue ' .. #G.q end
  end,
  blocks = function(G)
    -- the well keeps its 22 rows of 10 after clears
    if G.state == 'play' and #G.board ~= 22 then return 'board rows ' .. #G.board end
    for y = 1, #G.board do
      if #G.board[y] ~= 10 then return 'row ' .. y .. ' has ' .. #G.board[y] end
    end
    if #G.queue > 4 then return 'queue ' .. #G.queue end
  end,
  bricks = function(G)
    if G.state == 'play' and (G.x < 0 or G.x > 318 or G.y < 13) then
      return string.format('ball out at %.1f %.1f', G.x, G.y)
    end
    if G.left < 0 then return 'bricks left ' .. G.left end
  end,
  rally = function(G)
    if G.state == 'play' and (G.y < 13 or G.y > 212) then return 'ball y ' .. G.y end
    if G.me > 7 or G.cpu > 7 then return 'score' end
  end,
  sudoku = function(G)
    if G.state == 'play' then
      for i = 1, 81 do
        if G.given[i] and G.grid[i] ~= G.sol[i] then return 'given changed at ' .. i end
      end
    end
  end,
  jumper = function(G)
    if #G.bits > 30 then return 'bits ' .. #G.bits end
    if G.state == 'play' and G.p.x < 0 then return 'x ' .. G.p.x end
  end,
}

local runs = tonumber(arg[1]) or 200
local bad = 0
for _, name in ipairs(GAMES) do
  for run = 1, runs do
    local seed = run * 7919
    local ok, err = pcall(function()
      local g = T.load('games/lua/' .. name .. '.lua', {}, seed)
      local G = g.env.G
      for i = 1, 400 do
        local r = math.random()
        if r < 0.5 then
          T.tick(g, math.random(1, 6))
        elseif r < 0.8 then
          T.key(g, T.KEYNAMES[math.random(1, 4)])
        elseif r < 0.9 then
          T.key(g, T.KEYNAMES[math.random(1, #T.KEYNAMES)])
        else
          T.key(g, CHARS[math.random(1, #CHARS)])
        end
        -- mostly keep playing: leave the title and game-over screens
        if (G.state == 'title' or G.state == 'over') and math.random() < 0.3 then
          T.key(g, 'enter')
        end
        if #g.errors > 0 then error(g.errors[1]) end
        local why = INV[name] and INV[name](G)
        if why then error(why) end
      end
    end)
    if not ok then
      bad = bad + 1
      if bad <= 5 then print(name .. ' seed ' .. seed .. ': ' .. tostring(err)) end
    end
  end
end
print(string.format('game_fuzz: %d games x %d runs, %d failed', #GAMES, runs, bad))
if bad > 0 then os.exit(1) end
