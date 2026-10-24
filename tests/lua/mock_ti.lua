-- Desktop stand-in for the TI-Nspire Lua API (tests only), for LuaJIT
-- (Lua 5.1 like the calculator). load() runs a game script in a fresh
-- environment with fake platform, timer, var, document and cursor tables;
-- key() and tick() send it events; every paint is recorded as a list of
-- drawing operations and checked: only calls the real gc has, colours
-- 0-255, font sizes the handheld has, nothing drawn off the screen.
local M = {}

M.W = 318
M.H = 212
M.SIZES = {[7] = 1, [9] = 1, [10] = 1, [11] = 1, [12] = 1, [16] = 1, [24] = 1}

-- a rough width for TI's proportional font: 0.55 of the size per character
local function strw(font, s)
  return math.floor(#tostring(s) * font.size * 0.55 + 0.5)
end

local function newgc(game)
  local gc = {ops = {}, col = {0, 0, 0}, font = {fam = 'sansserif', st = 'r', size = 12}}
  local function bad(msg)
    game.errors[#game.errors + 1] = msg
  end
  local function inside(x, y, w, h, what)
    if x < 0 or y < 0 or x + w > M.W or y + h > M.H then
      bad(string.format('%s off screen: %s %s %s %s', what, x, y, w, h))
    end
  end
  local function num(...)
    local a = {...}
    for i = 1, #a do
      if type(a[i]) ~= 'number' or a[i] ~= a[i] then
        bad('not a number: ' .. tostring(a[i]))
        return false
      end
    end
    return true
  end
  local function add(op)
    op.col = gc.col
    gc.ops[#gc.ops + 1] = op
  end
  function gc:setColorRGB(r, g, b)
    if g == nil then
      -- one 0xRRGGBB number
      r, g, b = math.floor(r / 65536) % 256, math.floor(r / 256) % 256, r % 256
    end
    if not num(r, g, b) or r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255 then
      bad('bad colour')
    end
    gc.col = {r, g, b}
  end
  function gc:setFont(fam, st, size)
    if not M.SIZES[size] then bad('font size ' .. tostring(size)) end
    if fam ~= 'sansserif' and fam ~= 'serif' then bad('font ' .. tostring(fam)) end
    gc.font = {fam = fam, st = st, size = size}
  end
  function gc:setPen(thick, style) gc.pen = {thick, style} end
  function gc:getStringWidth(s) return strw(gc.font, s) end
  function gc:getStringHeight(s) return math.floor(gc.font.size * 1.4) end
  function gc:fillRect(x, y, w, h)
    if num(x, y, w, h) then inside(x, y, w, h, 'fillRect') end
    add({'rect', x, y, w, h})
  end
  function gc:drawRect(x, y, w, h)
    if num(x, y, w, h) then inside(x, y, w + 1, h + 1, 'drawRect') end
    add({'frame', x, y, w, h})
  end
  function gc:fillArc(x, y, w, h, a, b)
    if num(x, y, w, h, a, b) then inside(x, y, w, h, 'fillArc') end
    add({'oval', x, y, w, h})
  end
  function gc:drawArc(x, y, w, h, a, b)
    if num(x, y, w, h, a, b) then inside(x, y, w + 1, h + 1, 'drawArc') end
    add({'ring', x, y, w, h})
  end
  function gc:drawLine(x1, y1, x2, y2)
    if num(x1, y1, x2, y2) then
      inside(math.min(x1, x2), math.min(y1, y2), math.abs(x2 - x1), math.abs(y2 - y1), 'drawLine')
    end
    add({'line', x1, y1, x2, y2})
  end
  function gc:fillPolygon(pts)
    for i = 1, #pts, 2 do
      if num(pts[i], pts[i + 1]) then inside(pts[i], pts[i + 1], 0, 0, 'fillPolygon') end
    end
    add({'poly', pts})
  end
  function gc:drawString(s, x, y, align)
    if type(s) ~= 'string' then bad('drawString of ' .. type(s)) end
    if align ~= 'top' then bad('drawString without "top": ' .. tostring(s)) end
    if num(x, y) then inside(x, y, strw(gc.font, s), gc.font.size, 'drawString "' .. tostring(s) .. '"') end
    add({'text', x, y, tostring(s), gc.font.size, gc.font.st})
  end
  return gc
end

-- run the script at path; returns the game: env (its globals), frames,
-- errors, vars (what var.store saved) and clock (ms)
function M.load(path, vars, seed)
  local game = {frames = {}, errors = {}, vars = vars or {}, clock = 0,
                period = nil, dirty = false, changed = false}
  local env = {}
  setmetatable(env, {__index = _G})
  env.on = {}
  env.platform = {
    apiLevel = '2.0',
    window = {
      invalidate = function() game.dirty = true end,
      width = function() return M.W end,
      height = function() return M.H end,
      setFocus = function() end,
    },
  }
  env.timer = {
    start = function(p)
      if type(p) ~= 'number' or p < 0.01 then
        game.errors[#game.errors + 1] = 'timer.start ' .. tostring(p)
      end
      game.period = p
    end,
    stop = function() game.period = nil end,
    getMilliSecCounter = function() return game.clock end,
  }
  env.var = {
    store = function(name, v)
      if not string.match(name, '^%a[%w_]*$') or #name > 15 then
        game.errors[#game.errors + 1] = 'bad var name ' .. name
      end
      game.vars[name] = v
    end,
    recall = function(name) return game.vars[name] end,
  }
  env.document = {markChanged = function() game.changed = true end}
  env.cursor = {hide = function() end, show = function() end, set = function() end}
  -- the game's math.random is the shared one: seed it for repeatable runs
  math.randomseed(seed or 1)
  local chunk, err = loadfile(path)
  if not chunk then error(err) end
  setfenv(chunk, env)
  chunk()
  game.env = env
  local on = env.on
  if on.construction then on.construction() end
  if on.resize then on.resize(M.W, M.H) end
  if on.activate then on.activate() end
  M.paint(game)
  return game
end

-- paint a frame (as the OS does after invalidate) and keep it
function M.paint(game)
  game.dirty = false
  local gc = newgc(game)
  if game.env.on.paint then game.env.on.paint(gc) end
  game.frames[#game.frames + 1] = gc.ops
  if #game.frames > 50 then table.remove(game.frames, 1) end
  return gc.ops
end

local KEYS = {
  up = {'arrowKey', 'up'}, down = {'arrowKey', 'down'},
  left = {'arrowKey', 'left'}, right = {'arrowKey', 'right'},
  enter = {'enterKey'}, esc = {'escapeKey'}, tab = {'tabKey'},
  backtab = {'backtabKey'}, del = {'backspaceKey'}, clear = {'clearKey'},
  ret = {'returnKey'},
}
M.KEYNAMES = {'up', 'down', 'left', 'right', 'enter', 'esc', 'tab', 'backtab',
              'del', 'clear', 'ret'}

-- press one key: a name from KEYS or one character (charIn)
function M.key(game, k)
  local on = game.env.on
  local e = KEYS[k]
  if e then
    if on[e[1]] then on[e[1]](e[2]) end
  elseif on.charIn then
    on.charIn(k)
  end
  if game.dirty then M.paint(game) end
end

-- let n timer periods pass (or n * 50 ms with no timer running)
function M.tick(game, n)
  for _ = 1, n or 1 do
    local p = game.period
    game.clock = game.clock + math.floor((p or 0.05) * 1000 + 0.5)
    if p and game.env.on.timer then game.env.on.timer() end
    if game.dirty then M.paint(game) end
  end
end

-- the text drawn in the last frame, one string joined by '|'
function M.text(game)
  local f = game.frames[#game.frames] or {}
  local t = {}
  for i = 1, #f do
    if f[i][1] == 'text' then t[#t + 1] = f[i][4] end
  end
  return table.concat(t, '|')
end

return M
