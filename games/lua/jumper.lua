platform.apiLevel = '2.0'
-- Jumper: side-scrolling platform game for the TI-Nspire CX II (Lua).
-- Paste into a Script Editor page. Left/right (4 6) walk, up / 8 / Enter
-- jump, 7 and 9 jump left and right, down (2) stops, Esc pauses. Stomp the
-- brown walkers, jump over the purple spikies, bump ? blocks for coins and
-- reach the flag. The calculator only reports key presses (no releases), so
-- on the title screen pick how walking works: Tap (each press or repeat
-- walks a short way) or Keep going (walk until you press down or back).

local TICK = 0.05
local T = 12                    -- tile size
local ROWS = 16
local TOPBAR = 20
local GRAV, JUMP, MAXFALL = 0.55, -7.2, 7
local WALK = 2.6
local HOLD = 8                  -- ticks one press keeps you walking (Tap)
local PW, PH = 9, 11            -- player box
local EW, EH = 10, 10           -- enemy box
local LIVES, TIME = 3, 200
local MODES = {'Tap', 'Keep going'}

-- ground: 'h*n' = n columns of ground h tiles high (0 = pit);
-- things: 'column,row,tiles' laid out to the right from that square,
-- rows counted from the top (1-16). # stone, B brick, ? coin block,
-- P pipe, C coin, E walker, K spiky, F flag
local LEVELS = {
  {sky = {110, 170, 240}, check = 80,
   ground = '2*30 0*2 2*20 0*3 2*25 3*8 2*12 0*2 2*20 4*4 2*37',
   things = '10,11,CCC 16,11,B?B?B 18,7,? 24,14,E 30,11,CCCC 40,13,PP 40,14,PP ' ..
            '46,14,E 60,14,E 66,14,E 64,11,B??B 84,13,E 95,12,PP 95,13,PP ' ..
            '95,14,PP 100,10,CC 110,14,K 115,11,?B? 124,10,CCCC 135,14,E ' ..
            '140,14,E 150,5,F'},
  {sky = {80, 120, 180}, check = 80,
   ground = '2*20 0*3 2*10 0*3 2*12 0*6 2*15 3*5 4*5 2*10 0*3 2*25 0*3 2*20 3*10 2*25',
   things = '8,11,?B? 14,14,E 22,10,CCC 28,14,E 40,13,PP 40,14,PP 45,14,E ' ..
            '51,13,## 51,11,CC 60,11,BBBBB 62,7,? 58,14,E 64,14,K 77,11,CC ' ..
            '85,14,E 91,10,CCC 100,11,B?B 98,14,E 104,14,E 108,14,K 119,10,CCC ' ..
            '125,13,PP 125,14,PP 131,14,E 136,14,E 145,13,E 150,10,?B? 160,5,F'},
  {sky = {40, 50, 90}, check = 79,
   ground = '2*15 0*3 2*8 3*4 4*2 5*6 0*3 5*4 2*12 0*3 2*6 0*3 2*6 0*3 2*20 3*3 4*3 ' ..
            '5*3 6*3 2*20 0*3 2*30',
   things = '6,11,?B? 10,14,E 17,10,CCC 22,14,K 28,13,E 40,8,CCC 50,11,B??B ' ..
            '50,14,E 53,14,E 55,14,K 59,10,CC 63,14,E 68,10,CC 72,14,K 77,10,CC ' ..
            '85,13,PP 85,14,PP 90,12,PP 90,13,PP 90,14,PP 94,14,E 96,14,E ' ..
            '118,11,?B?B? 115,14,K 120,14,E 124,14,K 132,10,CCC 140,14,E 146,14,E 155,5,F'},
}

local SOLID = {['#'] = true, B = true, ['?'] = true, P = true, U = true, G = true}

local HUD = {20, 24, 36}
local TEXT = {240, 240, 240}
local DIM = {160, 170, 185}
local GOLD = {250, 200, 40}
local DIRT = {150, 95, 50}
local GRASS = {70, 180, 70}
local STONE = {120, 120, 130}
local BRICK = {185, 80, 50}
local USED = {130, 100, 70}
local PIPE = {40, 170, 70}
local PIPEDK = {20, 110, 45}
local BODY = {50, 110, 230}
local CAP = {230, 60, 60}
local WALKER = {140, 85, 40}
local SPIKY = {150, 60, 200}
local WHITE = {255, 255, 255}
local INK = {20, 20, 30}

G = {state = 'title', mode = 1, best = 0, score = 0, coins = 0, lives = LIVES,
     level = 1, time = TIME, sub = 0, map = {}, width = 0, flag = 0, foes = {},
     bits = {}, p = {x = 0, y = 0, vx = 0, vy = 0, ground = false, face = 1},
     walk = 0, hold = 0, jumpbuf = 0, coyote = 0, camx = 0, wait = 0,
     checked = false, record = false}

local function color(gc, c) gc:setColorRGB(c[1], c[2], c[3]) end

local function font(gc, size, st) gc:setFont('sansserif', st or 'r', size) end

local function centre(gc, s, y)
  gc:drawString(s, math.floor((318 - gc:getStringWidth(s)) / 2), y, 'top')
end

local function loadbest()
  local ok, v = pcall(var.recall, 'jmpbest')
  G.best = (ok and type(v) == 'number') and v or 0
end

local function savebest()
  pcall(var.store, 'jmpbest', G.best)
  pcall(document.markChanged)
end

-- the tile in column c, row r: the level's ends are walls, below is a pit
local function tile(c, r)
  if c < 1 or c > G.width then return 'G' end
  if r < 1 or r > ROWS then return '.' end
  return G.map[r][c]
end

local function solid(c, r) return SOLID[tile(c, r)] end

-- the tile column / row holding position v; 'last' for a box's far edge,
-- which is just short of v (a box that ends where a tile starts is not in it)
local function at(v) return math.floor(v / T) + 1 end
local function last(v) return math.floor((v - 0.01) / T) + 1 end

local function build()
  local L = LEVELS[G.level]
  local cols = {}
  for h, n in string.gmatch(L.ground, '(%d+)%*(%d+)') do
    for _ = 1, tonumber(n) do cols[#cols + 1] = tonumber(h) end
  end
  G.width = #cols
  G.map = {}
  for r = 1, ROWS do
    G.map[r] = {}
    for c = 1, G.width do
      G.map[r][c] = (r > ROWS - cols[c]) and '#' or '.'
    end
  end
  G.foes, G.bits, G.flag = {}, {}, G.width - 5
  for c0, r, s in string.gmatch(L.things, '(%d+),(%d+),(%S+)') do
    c0, r = tonumber(c0), tonumber(r)
    for k = 1, #s do
      local ch, c = string.sub(s, k, k), c0 + k - 1
      if ch == 'E' or ch == 'K' then
        G.foes[#G.foes + 1] = {x = (c - 1) * T + 1, y = (r - 1) * T + T - EH,
                               vx = -0.7, kind = ch, dead = 0}
      elseif ch == 'F' then
        G.flag = c
        G.flagtop = r
      else
        G.map[r][c] = ch
      end
    end
  end
end

-- put the player on the ground in column c
local function place(c)
  local p = G.p
  local r = 1
  while r <= ROWS and not solid(c, r) do r = r + 1 end
  p.x, p.y = (c - 1) * T + 1, (r - 1) * T - PH
  p.vx, p.vy, p.ground, p.face = 0, 0, false, 1
  G.walk, G.hold, G.jumpbuf, G.coyote = 0, 0, 0, 0
end

local function startlevel()
  build()
  G.time, G.sub = TIME, 0
  place(G.checked and LEVELS[G.level].check or 3)
  G.state = 'play'
end

local function start()
  math.randomseed(timer.getMilliSecCounter())
  G.score, G.coins, G.lives, G.level, G.record = 0, 0, LIVES, 1, false
  G.checked = false
  loadbest()
  startlevel()
end

local function finish(state)
  if G.score > G.best then
    G.best = G.score
    G.record = true
    savebest()
  end
  G.state = state
end

local function coin(x, y)
  G.coins = G.coins + 1
  G.score = G.score + 100
  if G.coins % 50 == 0 then G.lives = G.lives + 1 end
  if #G.bits < 30 then G.bits[#G.bits + 1] = {x = x, y = y, vx = 0, vy = -4, t = 10, c = GOLD} end
end

local function bump(c, r)
  local ch = tile(c, r)
  if ch == '?' then
    G.map[r][c] = 'U'
    coin((c - 1) * T + 4, (r - 2) * T)
  elseif ch == 'B' then
    G.map[r][c] = '.'
    G.score = G.score + 50
    for k = 1, 4 do
      if #G.bits < 30 then
        G.bits[#G.bits + 1] = {x = (c - 1) * T + 4, y = (r - 1) * T + 4,
                               vx = (k % 2 == 0) and 1.5 or -1.5, vy = k > 2 and -5 or -3, t = 20, c = BRICK}
      end
    end
  end
  -- a walker standing on the bumped block is knocked out
  for _, e in ipairs(G.foes) do
    if e.dead == 0 and e.y + EH == (r - 1) * T and e.x + EW > (c - 1) * T and e.x < c * T then
      e.dead = 15
      G.score = G.score + 100
    end
  end
end

local function hurt()
  G.state, G.wait = 'dead', 30
  G.p.vy = -6
end

local function collect()
  local p = G.p
  local c1, c2 = at(p.x), last(p.x + PW)
  local r1, r2 = at(p.y), last(p.y + PH)
  for r = r1, r2 do
    for c = c1, c2 do
      if tile(c, r) == 'C' then
        G.map[r][c] = '.'
        coin((c - 1) * T + 4, (r - 1) * T)
      end
    end
  end
end

local function moveplayer()
  local p = G.p
  if G.mode == 1 then
    if G.hold > 0 then G.hold = G.hold - 1 else G.walk = 0 end
  end
  p.vx = G.walk * WALK
  if G.walk ~= 0 then p.face = G.walk end
  if G.jumpbuf > 0 then
    if p.ground or G.coyote > 0 then
      p.vy, p.ground, G.coyote, G.jumpbuf = JUMP, false, 0, 0
    else
      G.jumpbuf = G.jumpbuf - 1
    end
  end
  p.vy = math.min(p.vy + GRAV, MAXFALL)
  -- across, then up/down, stopping at solid tiles
  p.x = p.x + p.vx
  if p.x < 0 then p.x = 0 end
  local r1, r2 = at(p.y), last(p.y + PH)
  if p.vx > 0 then
    local c = last(p.x + PW)
    for r = r1, r2 do if solid(c, r) then p.x = (c - 1) * T - PW break end end
  elseif p.vx < 0 then
    local c = at(p.x)
    for r = r1, r2 do if solid(c, r) then p.x = c * T break end end
  end
  p.y = p.y + p.vy
  local c1, c2 = at(p.x), last(p.x + PW)
  p.ground = false
  if p.vy > 0 then
    local r = last(p.y + PH)
    if solid(c1, r) or solid(c2, r) then
      p.y, p.vy, p.ground = (r - 1) * T - PH, 0, true
    end
  elseif p.vy < 0 then
    local r = at(p.y)
    if solid(c1, r) or solid(c2, r) then
      p.y, p.vy = r * T, 0
      local cc = at(p.x + PW / 2)
      if solid(cc, r) then bump(cc, r) else bump(solid(c1, r) and c1 or c2, r) end
    end
  end
  if p.ground then G.coyote = 3 elseif G.coyote > 0 then G.coyote = G.coyote - 1 end
  collect()
  if p.y > ROWS * T then hurt() end
end

local function movefoes()
  local p = G.p
  for _, e in ipairs(G.foes) do
    if e.dead > 0 then
      e.dead = e.dead - 1
      if e.dead == 0 then e.dead = -1 end
    elseif e.dead == 0 and math.abs(e.x - G.camx - 159) < 220 then
      e.x = e.x + e.vx
      local front = e.vx > 0 and last(e.x + EW) or at(e.x)
      local r = at(e.y + EH / 2)
      if solid(front, r) or not solid(front, r + 1) then
        e.x = e.x - e.vx
        e.vx = -e.vx
      end
      if p.x + PW > e.x and p.x < e.x + EW and p.y + PH > e.y and p.y < e.y + EH then
        if e.kind == 'E' and p.vy > 0 and p.y + PH - p.vy <= e.y + 4 then
          e.dead = 15
          p.vy = -5
          G.score = G.score + 100
        else
          hurt()
          return
        end
      end
    end
  end
end

local function camera()
  local x = G.p.x - 130
  local hi = G.width * T - 318
  if x > hi then x = hi end
  if x < 0 then x = 0 end
  G.camx = math.floor(x)
end

local function movebits()
  local keep = {}
  for _, b in ipairs(G.bits) do
    b.x, b.y, b.vy, b.t = b.x + b.vx, b.y + b.vy, b.vy + GRAV, b.t - 1
    if b.t > 0 then keep[#keep + 1] = b end
  end
  G.bits = keep
end

function on.timer()
  local s = G.state
  if s == 'play' then
    moveplayer()
    if G.state == 'play' then movefoes() end
    if not G.checked and G.p.x >= (LEVELS[G.level].check - 1) * T then G.checked = true end
    if G.state == 'play' and G.p.x + PW / 2 >= (G.flag - 1) * T + 4 then
      G.score = G.score + G.time * 5
      G.state, G.wait = 'goal', 40
    end
    G.sub = G.sub + 1
    if G.sub >= 20 then
      G.sub = 0
      G.time = G.time - 1
      if G.time <= 0 and G.state == 'play' then hurt() end
    end
    camera()
    movebits()
    platform.window:invalidate()
  elseif s == 'dead' then
    local p = G.p
    p.vy = p.vy + GRAV
    p.y = p.y + p.vy
    G.wait = G.wait - 1
    if G.wait <= 0 then
      G.lives = G.lives - 1
      if G.lives <= 0 then finish('over') else startlevel() end
    end
    platform.window:invalidate()
  elseif s == 'goal' then
    movebits()
    G.wait = G.wait - 1
    if G.wait <= 0 then
      if G.level >= #LEVELS then
        finish('win')
      else
        G.level, G.checked = G.level + 1, false
        startlevel()
      end
    end
    platform.window:invalidate()
  end
end

local function walk(d)
  if G.mode == 2 and G.walk == -d then
    G.walk = 0
  else
    G.walk = d
  end
  G.hold = HOLD
end

local function jump(d)
  if d then G.walk, G.hold = d, HOLD end
  G.jumpbuf = 4
end

function on.arrowKey(k)
  if G.state == 'title' then
    if k == 'left' or k == 'right' then G.mode = 3 - G.mode end
  elseif G.state == 'play' then
    if k == 'left' then
      walk(-1)
    elseif k == 'right' then
      walk(1)
    elseif k == 'up' then
      jump()
    elseif k == 'down' then
      G.walk = 0
    end
  end
  platform.window:invalidate()
end

local KEYS = {['4'] = 'left', ['6'] = 'right', ['8'] = 'up', ['2'] = 'down', ['5'] = 'up'}

function on.charIn(ch)
  if KEYS[ch] then
    on.arrowKey(KEYS[ch])
  elseif G.state == 'play' and (ch == '7' or ch == '9') then
    jump(ch == '7' and -1 or 1)
  elseif ch == 'p' and (G.state == 'play' or G.state == 'pause') then
    G.state = G.state == 'play' and 'pause' or 'play'
    platform.window:invalidate()
  end
end

function on.enterKey()
  local s = G.state
  if s == 'title' or s == 'over' or s == 'win' then
    start()
  elseif s == 'play' then
    jump()
  elseif s == 'pause' then
    G.state = 'play'
  end
  platform.window:invalidate()
end

function on.escapeKey()
  local s = G.state
  if s == 'play' then
    G.state = 'pause'
  elseif s == 'pause' or s == 'over' or s == 'win' then
    G.state = 'title'
    loadbest()
  end
  platform.window:invalidate()
end

function on.activate() timer.start(TICK) end

function on.deactivate()
  if G.state == 'play' then G.state = 'pause' end
end

-- drawing: world x/y to the screen, cut to the play area
local function rect(gc, x, y, w, h)
  if x < 0 then w, x = w + x, 0 end
  if x + w > 318 then w = 318 - x end
  if y < TOPBAR then h, y = h + y - TOPBAR, TOPBAR end
  if y + h > 212 then h = 212 - y end
  if w > 0 and h > 0 then gc:fillRect(x, y, w, h) end
end

local function inside(x, y, w, h)
  return x >= 0 and x + w <= 318 and y >= TOPBAR and y + h <= 212
end

local function drawtile(gc, ch, c, r, x, y)
  if ch == '#' then
    local top = not SOLID[tile(c, r - 1)]
    color(gc, (G.map[ROWS][c] == '#' and r > 8) and DIRT or STONE)
    rect(gc, x, y, T, T)
    if top then
      color(gc, GRASS)
      rect(gc, x, y, T, 3)
    end
  elseif ch == 'B' then
    color(gc, BRICK)
    rect(gc, x, y, T - 1, T - 1)
    color(gc, DIRT)
    rect(gc, x, y + 5, T - 1, 1)
    rect(gc, x + 5, y, 1, 5)
  elseif ch == '?' or ch == 'U' then
    color(gc, ch == '?' and GOLD or USED)
    rect(gc, x, y, T - 1, T - 1)
    if ch == '?' and inside(x, y, T, T) then
      color(gc, DIRT)
      font(gc, 9, 'b')
      gc:drawString('?', x + 3, y, 'top')
    end
  elseif ch == 'P' then
    local lip = tile(c, r - 1) ~= 'P'
    local left = tile(c - 1, r) ~= 'P'
    color(gc, PIPE)
    rect(gc, x, y, T, T)
    color(gc, PIPEDK)
    rect(gc, left and x or x + T - 2, y, 2, T)
    if lip then rect(gc, x, y, T, 3) end
  elseif ch == 'C' then
    if inside(x + 3, y + 2, 6, 8) then
      color(gc, GOLD)
      gc:fillArc(x + 3, y + 2, 6, 8, 0, 360)
    end
  end
end

local function drawflag(gc)
  local x = (G.flag - 1) * T + 5 - G.camx
  if x < -20 or x > 330 then return end
  local r = G.flagtop or 5
  local foot = r
  while foot <= ROWS and not solid(G.flag, foot) do foot = foot + 1 end
  color(gc, WHITE)
  rect(gc, x, TOPBAR + (r - 1) * T, 2, (foot - r) * T)
  local fy = TOPBAR + (r - 1) * T
  if inside(x - 14, fy, 16, 10) then
    color(gc, GRASS)
    gc:fillPolygon({x, fy, x, fy + 10, x - 14, fy + 5})
  end
end

local function drawplayer(gc)
  local p = G.p
  local x, y = math.floor(p.x) - G.camx, math.floor(p.y) + TOPBAR
  color(gc, CAP)
  rect(gc, x, y, PW, 4)
  rect(gc, x + (p.face > 0 and 3 or -2), y + 2, 8, 2)
  color(gc, BODY)
  rect(gc, x, y + 4, PW, 5)
  color(gc, WHITE)
  rect(gc, x + (p.face > 0 and 5 or 1), y + 4, 3, 3)
  color(gc, INK)
  rect(gc, x + (p.face > 0 and 6 or 2), y + 5, 1, 2)
  local step = (p.ground and p.vx ~= 0 and math.floor(p.x / 6) % 2 == 1) and 1 or 0
  rect(gc, x + step, y + 9, 3, 2)
  rect(gc, x + PW - 3 - step, y + 9, 3, 2)
end

local function drawfoe(gc, e)
  local x, y = math.floor(e.x) - G.camx, math.floor(e.y) + TOPBAR
  if not inside(x, y, EW, EH) then return end
  if e.dead > 0 then
    color(gc, WALKER)
    gc:fillRect(x, y + EH - 3, EW, 3)
    return
  end
  color(gc, e.kind == 'E' and WALKER or SPIKY)
  gc:fillArc(x, y, EW, EH, 0, 360)
  if e.kind == 'K' then
    color(gc, WHITE)
    gc:fillPolygon({x + 1, y + 3, x + 3, y, x + 5, y + 3})
    gc:fillPolygon({x + 5, y + 3, x + 7, y, x + 9, y + 3})
  end
  color(gc, WHITE)
  gc:fillRect(x + 2, y + 3, 2, 3)
  gc:fillRect(x + 6, y + 3, 2, 3)
  color(gc, INK)
  gc:fillRect(x + 6, y + EH - 2, 3, 2)
  gc:fillRect(x + 1, y + EH - 2, 3, 2)
end

local function world(gc)
  local L = LEVELS[G.level]
  color(gc, L.sky)
  gc:fillRect(0, TOPBAR, 318, 212 - TOPBAR)
  -- clouds drift at a third of the speed
  color(gc, G.level == 3 and {70, 80, 120} or WHITE)
  for k = 0, 5 do
    local x = (k * 97 + 40 - math.floor(G.camx / 3)) % 420 - 50
    if inside(x, 36 + (k % 3) * 14, 34, 12) then gc:fillArc(x, 36 + (k % 3) * 14, 34, 12, 0, 360) end
  end
  local c1 = math.floor(G.camx / T) + 1
  for c = c1, c1 + 27 do
    if c <= G.width then
      for r = 1, ROWS do
        local ch = G.map[r][c]
        if ch ~= '.' then drawtile(gc, ch, c, r, (c - 1) * T - G.camx, TOPBAR + (r - 1) * T) end
      end
    end
  end
  drawflag(gc)
  for _, e in ipairs(G.foes) do
    if e.dead >= 0 then drawfoe(gc, e) end
  end
  for _, b in ipairs(G.bits) do
    color(gc, b.c)
    rect(gc, math.floor(b.x) - G.camx, math.floor(b.y) + TOPBAR, 4, 4)
  end
  drawplayer(gc)
  color(gc, HUD)
  gc:fillRect(0, 0, 318, TOPBAR)
  color(gc, TEXT)
  font(gc, 9, 'b')
  gc:drawString('JUMPER', 4, 3, 'top')
  font(gc, 9)
  gc:drawString('Level ' .. G.level, 58, 3, 'top')
  gc:drawString(tostring(G.score), 108, 3, 'top')
  color(gc, GOLD)
  gc:fillArc(160, 5, 6, 8, 0, 360)
  color(gc, TEXT)
  gc:drawString('x' .. G.coins, 168, 3, 'top')
  color(gc, CAP)
  gc:fillRect(204, 6, 7, 7)
  color(gc, TEXT)
  gc:drawString('x' .. G.lives, 213, 3, 'top')
  gc:drawString('Time ' .. G.time, 260, 3, 'top')
end

local function panel(gc, lines)
  color(gc, HUD)
  gc:fillRect(59, 66, 200, 80)
  color(gc, DIM)
  gc:drawRect(59, 66, 200, 80)
  color(gc, TEXT)
  font(gc, 16, 'b')
  centre(gc, lines[1], 72)
  font(gc, 10)
  for i = 2, #lines do centre(gc, lines[i], 76 + i * 16) end
end

local function title(gc)
  color(gc, {110, 170, 240})
  gc:fillRect(0, 0, 318, 212)
  color(gc, DIRT)
  gc:fillRect(0, 188, 318, 24)
  color(gc, GRASS)
  gc:fillRect(0, 188, 318, 4)
  G.p.x, G.p.y, G.p.face, G.camx = 60, 157, 1, 0
  drawplayer(gc)
  drawfoe(gc, {x = 240, y = 158, kind = 'E', dead = 0})
  drawtile(gc, '?', 0, 0, 150, 146)
  color(gc, GOLD)
  font(gc, 24, 'b')
  centre(gc, 'JUMPER', 18)
  color(gc, HUD)
  gc:fillRect(79, 62, 160, 20)
  color(gc, TEXT)
  font(gc, 12)
  centre(gc, 'Walk:  < ' .. MODES[G.mode] .. ' >', 64)
  color(gc, HUD)
  font(gc, 10, 'b')
  centre(gc, 'Best ' .. G.best, 90)
  font(gc, 9)
  centre(gc, 'Enter: play    4 6: walk    8 or Enter: jump', 106)
  centre(gc, '7 9: jump left/right    2: stop    Esc: pause', 120)
end

function on.paint(gc)
  if G.state == 'title' then
    title(gc)
    return
  end
  world(gc)
  if G.state == 'pause' then
    panel(gc, {'PAUSED', 'Enter: resume', 'Esc: title'})
  elseif G.state == 'goal' then
    panel(gc, {'LEVEL ' .. G.level .. ' DONE', 'Time bonus ' .. G.time * 5})
  elseif G.state == 'over' or G.state == 'win' then
    panel(gc, {G.state == 'win' and 'YOU WIN!' or 'GAME OVER',
               'Score ' .. G.score .. (G.record and '  New best!' or ''),
               'Enter: again   Esc: title'})
  end
end

loadbest()
timer.start(TICK)
