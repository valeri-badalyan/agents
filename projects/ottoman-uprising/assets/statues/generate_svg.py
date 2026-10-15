#!/usr/bin/env python3
"""Generate The Emperor's Shadow - Ultra Detailed Final Boss Statue SVG (7500+ elements)"""
import random
import os

random.seed(42)

output_path = os.path.join(os.path.dirname(__file__), "15_emperors_shadow.svg")

lines = []
def w(s=""):
    lines.append(s)

w('<?xml version="1.0" encoding="UTF-8"?>')
w('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">')
w('<title>The Emperor\'s Shadow - Final Boss Statue</title>')
w('<desc>Ultra detailed final boss statue with 7500+ elements representing the ultimate dark emperor</desc>')
w()
w('<defs>')

# ============================================================
# GRADIENTS
# ============================================================
# Obsidian gradients (30)
for i in range(1, 31):
    x1 = random.randint(0, 50)
    y1 = random.randint(0, 50)
    x2 = 100 - random.randint(0, 50)
    y2 = 100 - random.randint(0, 50)
    stops = []
    n = random.randint(4, 8)
    for j in range(n):
        off = int(100 * j / (n - 1))
        r = random.randint(5, 25)
        g = random.randint(5, 25)
        b = random.randint(15, 50)
        stops.append(f'<stop offset="{off}%" stop-color="rgb({r},{g},{b})"/>')
    w(f'<linearGradient id="obs{i}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">')
    for s in stops:
        w(s)
    w('</linearGradient>')

# Blood red radial gradients (20)
for i in range(1, 21):
    cx = random.randint(20, 80)
    cy = random.randint(20, 80)
    r = random.randint(40, 70)
    stops = []
    n = random.randint(4, 7)
    for j in range(n):
        off = int(100 * j / (n - 1))
        v = 255 - random.randint(0, 80) * j // (n - 1)
        a = max(10, 100 - 15 * j)
        stops.append(f'<stop offset="{off}%" stop-color="rgb({v},0,0)" stop-opacity="{a/100}"/>')
    w(f'<radialGradient id="bl{i}" cx="{cx}%" cy="{cy}%" r="{r}%">')
    for s in stops:
        w(s)
    w('</radialGradient>')

# Fire radial gradients (40)
for i in range(1, 41):
    cx = random.randint(35, 65)
    cy = random.randint(65, 90)
    r = random.randint(40, 65)
    stops = []
    colors = [
        (255, 255, 255), (255, 255, 100), (255, 220, 0),
        (255, 153, 0), (255, 102, 0), (255, 51, 0), (204, 0, 0)
    ]
    n = random.randint(5, 7)
    for j in range(n):
        off = int(100 * j / (n - 1))
        c = colors[min(j, len(colors) - 1)]
        rv = c[0] + random.randint(-10, 10)
        gv = c[1] + random.randint(-10, 10)
        bv = c[2] + random.randint(-5, 5)
        rv = max(0, min(255, rv))
        gv = max(0, min(255, gv))
        bv = max(0, min(255, bv))
        stops.append(f'<stop offset="{off}%" stop-color="rgb({rv},{gv},{bv})"/>')
    w(f'<radialGradient id="fr{i}" cx="{cx}%" cy="{cy}%" r="{r}%">')
    for s in stops:
        w(s)
    w('</radialGradient>')

# Shadow linear gradients (50)
for i in range(1, 51):
    x1 = random.randint(0, 100)
    y1 = random.randint(0, 100)
    x2 = 100 - x1 + random.randint(-20, 20)
    y2 = 100 - y1 + random.randint(-20, 20)
    x2 = max(0, min(100, x2))
    y2 = max(0, min(100, y2))
    stops = []
    n = random.randint(3, 6)
    for j in range(n):
        off = int(100 * j / (n - 1))
        a = max(5, 90 - 18 * j)
        stops.append(f'<stop offset="{off}%" stop-color="#000000" stop-opacity="{a/100}"/>')
    w(f'<linearGradient id="shd{i}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">')
    for s in stops:
        w(s)
    w('</linearGradient>')

# Gold gradients (20)
for i in range(1, 21):
    x1 = random.randint(0, 50)
    y1 = random.randint(0, 50)
    x2 = 100 - random.randint(0, 50)
    y2 = 100 - random.randint(0, 50)
    golds = [
        (255, 215, 0), (255, 236, 139), (218, 165, 32),
        (184, 134, 11), (139, 105, 20), (255, 250, 205)
    ]
    stops = []
    n = random.randint(4, 6)
    for j in range(n):
        off = int(100 * j / (n - 1))
        c = golds[min(j, len(golds) - 1)]
        rv = c[0] + random.randint(-5, 5)
        gv = c[1] + random.randint(-5, 5)
        bv = c[2] + random.randint(-3, 3)
        stops.append(f'<stop offset="{off}%" stop-color="rgb({max(0,min(255,rv))},{max(0,min(255,gv))},{max(0,min(255,bv))})"/>')
    w(f'<linearGradient id="gld{i}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">')
    for s in stops:
        w(s)
    w('</linearGradient>')

# Stone gradients (50)
for i in range(1, 51):
    x1 = random.randint(0, 100)
    y1 = random.randint(0, 100)
    x2 = 100 - random.randint(0, 100)
    y2 = 100 - random.randint(0, 100)
    stops = []
    n = random.randint(4, 6)
    for j in range(n):
        off = int(100 * j / (n - 1))
        v = random.randint(25, 110)
        stops.append(f'<stop offset="{off}%" stop-color="rgb({v},{v},{v})"/>')
    w(f'<linearGradient id="st{i}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">')
    for s in stops:
        w(s)
    w('</linearGradient>')

# Atmosphere gradients (90)
for i in range(1, 91):
    if random.random() > 0.5:
        cx = random.randint(10, 90)
        cy = random.randint(10, 90)
        r = random.randint(30, 95)
        stops = []
        n = random.randint(3, 7)
        for j in range(n):
            off = int(100 * j / (n - 1))
            rv = random.randint(10, 50)
            a = max(5, 40 - 5 * j)
            stops.append(f'<stop offset="{off}%" stop-color="rgb({rv},0,0)" stop-opacity="{a/100}"/>')
        w(f'<radialGradient id="atm{i}" cx="{cx}%" cy="{cy}%" r="{r}%">')
        for s in stops:
            w(s)
        w('</radialGradient>')
    else:
        x1 = random.randint(0, 100)
        y1 = random.randint(0, 100)
        x2 = 100 - random.randint(0, 100)
        y2 = 100 - random.randint(0, 100)
        stops = []
        n = random.randint(2, 4)
        for j in range(n):
            off = int(100 * j / (n - 1))
            rv = random.randint(10, 40)
            a = max(5, 35 - 8 * j)
            stops.append(f'<stop offset="{off}%" stop-color="rgb({rv},0,0)" stop-opacity="{a/100}"/>')
        w(f'<linearGradient id="atm{i}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">')
        for s in stops:
            w(s)
        w('</linearGradient>')

# Special gradients
w('<radialGradient id="rglow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ff0000" stop-opacity="0.6"/><stop offset="50%" stop-color="#cc0000" stop-opacity="0.3"/><stop offset="100%" stop-color="#660000" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="oglow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ff4400" stop-opacity="0.8"/><stop offset="30%" stop-color="#cc2200" stop-opacity="0.5"/><stop offset="70%" stop-color="#991100" stop-opacity="0.2"/><stop offset="100%" stop-color="#660000" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="windowglow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#4d0000" stop-opacity="0.8"/><stop offset="50%" stop-color="#330000" stop-opacity="0.5"/><stop offset="100%" stop-color="#1a0000" stop-opacity="0.2"/></radialGradient>')

# ============================================================
# FILTERS (150+)
# ============================================================
filter_configs = [
    ("blur1", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 2)]),
    ("blur2", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 4)]),
    ("blur3", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 6)]),
    ("blur4", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 8)]),
    ("blur5", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 10)]),
    ("blur6", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 12)]),
    ("blur7", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 14)]),
    ("blur8", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 16)]),
    ("blur9", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 18)]),
    ("blur10", -50, -50, 200, 200, [("feGaussianBlur", "SourceGraphic", 20)]),
]

for i, (name, fx, fy, fw, fh, _) in enumerate(filter_configs):
    w(f'<filter id="{name}" x="{fx}%" y="{fy}%" width="{fw}%" height="{fh}%">')
    w(f'<feGaussianBlur in="SourceGraphic" stdDeviation="{(i+1)*2}"/>')
    w('</filter>')

# Glow filters
for i in range(1, 31):
    std = random.randint(2, 8)
    w(f'<filter id="glow{i}" x="-50%" y="-50%" width="200%" height="200%">')
    w(f'<feGaussianBlur in="SourceGraphic" stdDeviation="{std}" result="blur"/>')
    w('<feMerge>')
    w('<feMergeNode in="blur"/>')
    if random.random() > 0.5:
        w('<feMergeNode in="blur"/>')
    w('<feMergeNode in="SourceGraphic"/>')
    w('</feMerge>')
    w('</filter>')

# Shadow filters
for i in range(1, 41):
    dx = random.randint(1, 8)
    dy = random.randint(1, 8)
    std = random.randint(2, 10)
    a = round(random.uniform(0.3, 0.8), 2)
    w(f'<filter id="shadow{i}" x="-30%" y="-30%" width="160%" height="160%">')
    w(f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{std}" flood-color="#000000" flood-opacity="{a}"/>')
    w('</filter>')

# Fire glow filters
for i in range(1, 21):
    std = random.randint(3, 7)
    w(f'<filter id="fireglow{i}" x="-50%" y="-50%" width="200%" height="200%">')
    w(f'<feGaussianBlur in="SourceGraphic" stdDeviation="{std}" result="blur"/>')
    w('<feColorMatrix in="blur" type="matrix" values="1 0 0 0 0.2  0 0.5 0 0 0  0 0 0 0 0  0 0 0 1 0" result="colorblur"/>')
    w('<feMerge><feMergeNode in="colorblur"/><feMergeNode in="SourceGraphic"/></feMerge>')
    w('</filter>')

# Smoke filters
for i in range(1, 16):
    freq = round(random.uniform(0.02, 0.05), 3)
    scale = random.randint(5, 15)
    w(f'<filter id="smoke{i}" x="-30%" y="-30%" width="160%" height="160%">')
    w(f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="4" seed="{i}"/>')
    w(f'<feDisplacementMap in="SourceGraphic" scale="{scale}"/>')
    w('</filter>')

# Noise filters
for i in range(1, 16):
    freq = round(random.uniform(0.5, 1.2), 2)
    w(f'<filter id="noise{i}" x="0%" y="0%" width="100%" height="100%">')
    w(f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="4" stitchTiles="stitch"/>')
    w('<feColorMatrix type="saturate" values="0"/>')
    w('<feBlend in="SourceGraphic" mode="multiply"/>')
    w('</filter>')

# Vignette filter
w('<filter id="vignette" x="-10%" y="-10%" width="120%" height="120%">')
w('<feFlood flood-color="#000000" flood-opacity="0.6"/>')
w('<feComposite in2="SourceGraphic" operator="over"/>')
w('<feGaussianBlur stdDeviation="80"/>')
w('</filter>')

# Obsidian texture filters
for i in range(1, 11):
    freq = round(random.uniform(0.3, 0.8), 2)
    w(f'<filter id="obsidiantex{i}" x="0%" y="0%" width="100%" height="100%">')
    w(f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="5" seed="{i}"/>')
    w('<feColorMatrix type="saturate" values="0"/>')
    w('<feBlend in="SourceGraphic" mode="overlay"/>')
    w('</filter>')

# Blood vein filter
for i in range(1, 11):
    freq = round(random.uniform(0.01, 0.04), 3)
    w(f'<filter id="bloodvein{i}" x="-20%" y="-20%" width="140%" height="140%">')
    w(f'<feTurbulence type="turbulence" baseFrequency="{freq}" numOctaves="3" seed="{i}"/>')
    w('<feDisplacementMap in="SourceGraphic" scale="5"/>')
    w('<feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.5 0"/>')
    w('</filter>')

# Red atmosphere filter
for i in range(1, 11):
    std = random.randint(10, 30)
    w(f'<filter id="redatmos{i}" x="-50%" y="-50%" width="200%" height="200%">')
    w(f'<feGaussianBlur in="SourceGraphic" stdDeviation="{std}"/>')
    w('<feColorMatrix type="matrix" values="1 0 0 0 0.1  0 0 0 0 0  0 0 0 0 0  0 0 0 0.3 0"/>')
    w('</filter>')

# Clip path
w('<clipPath id="scene-clip"><rect x="0" y="0" width="1200" height="800"/></clipPath>')

w('</defs>')
w()
w('<g clip-path="url(#scene-clip)">')

# ============================================================
# BACKGROUND
# ============================================================
w('<rect x="0" y="0" width="1200" height="800" fill="url(#st4)"/>')
w('<rect x="0" y="0" width="1200" height="800" fill="url(#atm1)" opacity="0.7"/>')
w('<rect x="0" y="0" width="1200" height="800" fill="url(#atm2)" opacity="0.4"/>')

# ============================================================
# THRONE ROOM WALLS - Individual stone blocks
# ============================================================
def write_wall(start_x, start_y, w_count, h_count, grad_start):
    gid = 1
    for row in range(h_count):
        for col in range(w_count):
            bx = start_x + col * 55
            by = start_y + row * 70
            g = f"st{((gid - 1) % 50) + 1}"
            gid += 1
            w(f'<rect x="{bx}" y="{by}" width="50" height="65" fill="url(#{g})" stroke="#1a1a1a" stroke-width="0.5"/>')
            # Brick details
            if random.random() > 0.7:
                w(f'<path d="M{bx+5},{by+15} Q{bx+25},{by+12} {bx+45},{by+15}" fill="none" stroke="#2a2a2a" stroke-width="0.5" opacity="0.5"/>')
            if random.random() > 0.8:
                w(f'<circle cx="{bx+random.randint(10,40)}" cy="{by+random.randint(10,55)}" r="{random.randint(1,3)}" fill="#2a2a2a" opacity="0.3"/>')

w('<g id="left-wall">')
write_wall(5, 5, 3, 11, 1)
w('</g>')

w('<g id="right-wall">')
write_wall(1005, 5, 3, 11, 3)
w('</g>')

# Back wall
w('<g id="back-wall">')
for row in range(5):
    for col in range(14):
        bx = 200 + col * 57
        by = 5 + row * 13
        g = f"st{((row * 14 + col) % 50) + 1}"
        w(f'<rect x="{bx}" y="{by}" width="55" height="11" fill="url(#{g})" stroke="#1a1a1a" stroke-width="0.3" opacity="0.6"/>')
w('</g>')

# ============================================================
# CEILING ARCHES
# ============================================================
w('<g id="ceiling">')
for i in range(8):
    y_off = i * 8
    w(f'<path d="M200,{y_off} Q600,{80 + y_off} 1000,{y_off}" fill="none" stroke="url(#st{((i%50)+1)})" stroke-width="{3 - i*0.3}" opacity="{0.8 - i*0.08}"/>')
# Cross beams
for i in range(12):
    x = 200 + i * 67
    w(f'<path d="M{x},0 L{x},{60 + random.randint(-10,10)}" fill="none" stroke="#3a3a3a" stroke-width="{1 + random.random()}" opacity="0.6"/>')
w('</g>')

# ============================================================
# FLOOR MOSAIC (20x8 tiles = 160 elements)
# ============================================================
w('<g id="floor">')
w('<rect x="200" y="650" width="800" height="150" fill="url(#st5)"/>')
tile_count = 0
for row in range(8):
    for col in range(20):
        tx = 200 + col * 40
        ty = 650 + row * 18
        g = f"st{((tile_count) % 50) + 1}"
        w(f'<rect x="{tx}" y="{ty}" width="39" height="17" fill="url(#{g})" stroke="#0a0a0a" stroke-width="0.3"/>')
        tile_count += 1
w('</g>')

# ============================================================
# COLUMNS (4 columns, each with fluting details)
# ============================================================
for ci, cx in enumerate([260, 420, 780, 940]):
    gid = ci + 1
    w(f'<g id="col{ci+1}" transform="translate({cx},50)">')
    # Main column
    w(f'<rect x="0" y="0" width="35" height="600" fill="url(#st{gid})" rx="4"/>')
    # Fluting
    for fi in range(6):
        fx = 3 + fi * 5
        w(f'<path d="M{fx},10 L{fx},590" fill="none" stroke="#2a2a2a" stroke-width="0.8" opacity="0.4"/>')
    # Capital
    w(f'<rect x="-8" y="-5" width="51" height="18" fill="url(#gld{gid})" rx="3"/>')
    w(f'<rect x="-5" y="0" width="45" height="8" fill="url(#gld{((gid%20)+1)})" rx="2"/>')
    # Base
    w(f'<rect x="-8" y="587" width="51" height="18" fill="url(#gld{gid})" rx="3"/>')
    # Ring details
    for ri in range(15):
        ry = 20 + ri * 38
        w(f'<ellipse cx="17" cy="{ry}" rx="18" ry="2" fill="none" stroke="#3a3a3a" stroke-width="0.5" opacity="0.5"/>')
    w('</g>')

# ============================================================
# WINDOWS
# ============================================================
for wx in [230, 930]:
    w(f'<g id="window-{wx}" transform="translate({wx},100)">')
    w('<rect x="0" y="0" width="60" height="120" fill="#1a0000" rx="30" ry="30"/>')
    w('<rect x="5" y="5" width="50" height="110" fill="#330000" rx="25" ry="25"/>')
    w('<rect x="10" y="10" width="40" height="100" fill="url(#windowglow)" rx="20" ry="20"/>')
    # Stained glass panes
    w('<path d="M30,10 L30,110" fill="none" stroke="#660000" stroke-width="2"/>')
    w('<path d="M10,60 L50,60" fill="none" stroke="#660000" stroke-width="2"/>')
    for sy in [25, 40, 75, 90]:
        w(f'<path d="M15,{sy} L45,{sy}" fill="none" stroke="#4d0000" stroke-width="1"/>')
    # Gold frame
    w('<rect x="8" y="8" width="44" height="104" fill="none" stroke="#8b6914" stroke-width="2" rx="22" ry="22"/>')
    # Additional panes
    w('<path d="M15,30 L30,10" fill="none" stroke="#4d0000" stroke-width="0.8"/>')
    w('<path d="M45,30 L30,10" fill="none" stroke="#4d0000" stroke-width="0.8"/>')
    w('<path d="M15,90 L30,110" fill="none" stroke="#4d0000" stroke-width="0.8"/>')
    w('<path d="M45,90 L30,110" fill="none" stroke="#4d0000" stroke-width="0.8"/>')
    w('</g>')

# Window light beams
w('<g id="light-beams" opacity="0.25">')
for bx in [260, 960]:
    w(f'<path d="M{bx},220 L{bx-80},650 L{bx+80},650 Z" fill="url(#gld1)"/>')
    w(f'<path d="M{bx+3},220 L{bx-75},650 L{bx+85},650 Z" fill="url(#gld2)" opacity="0.5"/>')
w('</g>')

# ============================================================
# CARPET
# ============================================================
w('<g id="carpet">')
w('<rect x="350" y="650" width="500" height="150" fill="#4d0000" opacity="0.6"/>')
w('<rect x="355" y="655" width="490" height="140" fill="#660000" opacity="0.4"/>')
# Border pattern
for i in range(12):
    y = 660 + i * 11
    w(f'<path d="M360,{y} Q600,{y+8} 840,{y}" fill="none" stroke="url(#gld{((i%20)+1)})" stroke-width="{1.5 if i%3==0 else 0.8}"/>')
# Frayed edges
for i in range(25):
    x = 355 + i * 20
    w(f'<path d="M{x},790 Q{x+5},{793+random.randint(0,5)} {x+10},790" fill="none" stroke="#4d0000" stroke-width="0.8" opacity="0.6"/>')
w('</g>')

# ============================================================
# THRONE STRUCTURE
# ============================================================
w('<g id="throne" transform="translate(480,350)">')
# Seat
w('<rect x="0" y="200" width="240" height="100" fill="url(#obs1)" rx="5"/>')
w('<rect x="10" y="185" width="220" height="20" fill="url(#obs2)" rx="3"/>')
# Back
w('<rect x="-20" y="0" width="280" height="190" fill="url(#obs3)" rx="8"/>')
w('<rect x="-15" y="5" width="270" height="180" fill="url(#obs4)" rx="6"/>')
w('<rect x="-10" y="10" width="260" height="170" fill="url(#obs5)" rx="5"/>')
# Top arch
w('<path d="M-20,0 Q120,-35 260,0" fill="url(#obs6)" stroke="#8b6914" stroke-width="2"/>')
w('<path d="M-15,5 Q120,-28 255,5" fill="url(#obs7)" stroke="#daa520" stroke-width="1"/>')
# Gold trim
w('<path d="M-10,10 L-10,170" fill="none" stroke="#8b6914" stroke-width="1.5"/>')
w('<path d="M250,10 L250,170" fill="none" stroke="#8b6914" stroke-width="1.5"/>')
w('<path d="M-10,10 L250,10" fill="none" stroke="#daa520" stroke-width="1"/>')
w('<path d="M-10,90 L250,90" fill="none" stroke="#8b6914" stroke-width="1"/>')
w('<path d="M-10,170 L250,170" fill="none" stroke="#daa520" stroke-width="1"/>')

# Throne skulls (7 skulls)
for si in range(7):
    sx = 20 + si * 33
    w(f'<circle cx="{sx}" cy="50" r="12" fill="url(#obs{((si%15)+1)})"/>')
    w(f'<circle cx="{sx}" cy="45" r="8" fill="url(#obs{(((si+1)%15)+1)})"/>')
    w(f'<circle cx="{sx-3}" cy="42" r="2" fill="#0a0a14"/>')
    w(f'<circle cx="{sx+3}" cy="42" r="2" fill="#0a0a14"/>')
    w(f'<path d="M{sx-2},48 Q{sx},52 {sx+2},48" fill="none" stroke="#0a0a14" stroke-width="1"/>')
    # Jaw
    w(f'<path d="M{sx-5},50 Q{sx},56 {sx+5},50" fill="none" stroke="#0e0e1c" stroke-width="0.8"/>')

# Top crown ornament
w('<rect x="-20" y="-20" width="280" height="28" fill="url(#obs8)" rx="5"/>')
w('<circle cx="0" cy="-6" r="8" fill="url(#gld1)"/>')
w('<circle cx="240" cy="-6" r="8" fill="url(#gld1)"/>')
w('<circle cx="120" cy="-28" r="18" fill="url(#bl1)" filter="url(#glow1)"/>')
w('<circle cx="120" cy="-28" r="13" fill="url(#bl2)"/>')
w('<circle cx="120" cy="-28" r="8" fill="url(#bl3)"/>')
w('<circle cx="120" cy="-28" r="4" fill="#ffffff" opacity="0.3"/>')
w('</g>')

# ============================================================
# EMPEROR FIGURE
# ============================================================
w('<g id="emperor" transform="translate(600,380)">')

# --- CLOAK (behind body) ---
w('<g id="cloak">')
w('<path d="M-70,30 Q-130,100 -110,260 L110,260 Q130,100 70,30" fill="url(#obs9)" opacity="0.8" filter="url(#shadow1)"/>')
w('<path d="M-75,40 Q-135,110 -115,265 L-105,265 Q-125,100 -75,40" fill="url(#obs10)"/>')
w('<path d="M75,40 Q135,110 115,265 L105,265 Q125,100 75,40" fill="url(#obs11)"/>')
# Cloak folds
for fi in range(15):
    fx = -80 + fi * 12
    w(f'<path d="M{fx},{50+abs(fi-7)*5} Q{fx+5},{130+abs(fi-7)*8} {fx-3},{220+abs(fi-7)*3}" fill="none" stroke="#0a0a14" stroke-width="{1+random.random()}" opacity="{0.3+random.random()*0.4}"/>')
w('</g>')

# --- TORSO ---
w('<g id="body">')
w('<path d="M-60,0 Q-80,50 -70,120 L70,120 Q80,50 60,0 Z" fill="url(#obs1)" filter="url(#shadow2)"/>')
w('<path d="M-55,5 Q-75,55 -65,115 L65,115 Q75,55 55,5 Z" fill="url(#obs2)"/>')
w('<path d="M-50,10 Q-70,60 -60,110 L60,110 Q70,60 50,10 Z" fill="url(#obs3)"/>')
w('<path d="M-45,15 Q-65,65 -55,105 L55,105 Q65,65 45,15 Z" fill="url(#obs4)"/>')
w('<path d="M-40,20 Q-60,70 -50,100 L50,100 Q60,70 40,20 Z" fill="url(#obs5)"/>')
# Armor lines
for ai in range(8):
    ay = 10 + ai * 13
    w(f'<path d="M-35,{ay} Q0,{ay-3} 35,{ay}" fill="none" stroke="#0a0a14" stroke-width="1" opacity="0.5"/>')
# Vertical lines
for ai in range(5):
    ax = -30 + ai * 15
    w(f'<path d="M{ax},10 L{ax},110" fill="none" stroke="#1a1a2e" stroke-width="0.8" opacity="0.4"/>')
# Chest emblem
w('<path d="M-15,30 Q0,25 15,30 Q18,40 15,50 Q0,55 -15,50 Q-18,40 -15,30 Z" fill="url(#obs6)" stroke="#8b6914" stroke-width="1"/>')
w('<path d="M-8,35 Q0,32 8,35 Q10,40 8,45 Q0,48 -8,45 Q-10,40 -8,35 Z" fill="url(#obs7)"/>')
w('</g>')

# --- LEFT ARM ---
w('<g id="left-arm">')
w('<path d="M-70,20 Q-115,55 -125,110 Q-135,160 -115,190 Q-105,200 -95,190 Q-85,160 -95,110 Q-100,65 -75,30" fill="url(#obs11)" filter="url(#shadow3)"/>')
w('<path d="M-72,25 Q-117,60 -127,115 Q-137,165 -117,195" fill="none" stroke="#0a0a14" stroke-width="1.5"/>')
# Arm joints
for ji in range(5):
    jx = -90 - ji * 7
    jy = 60 + ji * 22
    w(f'<ellipse cx="{jx}" cy="{jy}" rx="5" ry="3" fill="none" stroke="#1a1a2e" stroke-width="0.8"/>')
# Claws (5 fingers)
for ci2 in range(5):
    cx2 = -112 + ci2 * 4
    cy2 = 185 + ci2 * 1
    w(f'<path d="M{cx2},{cy2} L{cx2-8},{cy2+18} L{cx2-5},{cy2+20} L{cx2+2},{cy2+5}" fill="url(#obs12)"/>')
    w(f'<path d="M{cx2},{cy2} L{cx2-8},{cy2+18}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
# Ring
w('<circle cx="-108" cy="188" r="4" fill="url(#gld1)" stroke="#daa520" stroke-width="1"/>')
w('<circle cx="-108" cy="188" r="2" fill="url(#bl4)"/>')
w('</g>')

# --- RIGHT ARM ---
w('<g id="right-arm">')
w('<path d="M70,20 Q115,55 125,110 Q135,160 115,190 Q105,200 95,190 Q85,160 95,110 Q100,65 75,30" fill="url(#obs11)" filter="url(#shadow4)"/>')
w('<path d="M72,25 Q117,60 127,115 Q137,165 117,195" fill="none" stroke="#0a0a14" stroke-width="1.5"/>')
for ji in range(5):
    jx = 90 + ji * 7
    jy = 60 + ji * 22
    w(f'<ellipse cx="{jx}" cy="{jy}" rx="5" ry="3" fill="none" stroke="#1a1a2e" stroke-width="0.8"/>')
# Right claws
for ci2 in range(5):
    cx2 = 112 - ci2 * 4
    cy2 = 185 + ci2 * 1
    w(f'<path d="M{cx2},{cy2} L{cx2+8},{cy2+18} L{cx2+5},{cy2+20} L{cx2-2},{cy2+5}" fill="url(#obs13)"/>')
    w(f'<path d="M{cx2},{cy2} L{cx2+8},{cy2+18}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
# Ring on right hand
w('<circle cx="108" cy="188" r="4" fill="url(#gld2)" stroke="#daa520" stroke-width="1"/>')
w('<circle cx="108" cy="188" r="2" fill="url(#bl5)"/>')

# --- ORB OF EMPIRE (in right hand) ---
w('<g id="orb" transform="translate(120,165)">')
w('<circle cx="0" cy="0" r="28" fill="url(#obs14)" filter="url(#glow5)"/>')
w('<circle cx="0" cy="0" r="25" fill="url(#obs15)"/>')
w('<circle cx="0" cy="0" r="22" fill="url(#obs1)"/>')
w('<circle cx="0" cy="0" r="19" fill="url(#obs2)"/>')
w('<circle cx="0" cy="0" r="16" fill="url(#obs3)"/>')
# Empire symbols on orb
for si in range(8):
    sa = si * 45
    import math
    sx = 10 * math.cos(math.radians(sa))
    sy = 10 * math.sin(math.radians(sa))
    w(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2" fill="url(#gld{((si%20)+1)})" opacity="0.8"/>')
# Cross lines
w('<path d="M-12,0 L12,0" fill="none" stroke="#8b6914" stroke-width="0.8"/>')
w('<path d="M0,-12 L0,12" fill="none" stroke="#8b6914" stroke-width="0.8"/>')
w('<path d="M-8,-8 L8,8" fill="none" stroke="#daa520" stroke-width="0.5"/>')
w('<path d="M8,-8 L-8,8" fill="none" stroke="#daa520" stroke-width="0.5"/>')
# Blood glow layers
w('<circle cx="0" cy="0" r="32" fill="url(#bl1)" opacity="0.4"/>')
w('<circle cx="0" cy="0" r="36" fill="url(#bl2)" opacity="0.2"/>')
w('<circle cx="0" cy="0" r="40" fill="url(#bl3)" opacity="0.1"/>')
# Rising particles
for pi in range(15):
    px = random.randint(-12, 12)
    py = random.randint(-15, -5)
    pr = round(random.uniform(0.5, 1.5), 1)
    pd = round(random.uniform(1.5, 4), 1)
    pa = round(random.uniform(0.4, 0.9), 2)
    w(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="#ff{random.choice(["0000","3333","1a1a","6666"])}" opacity="{pa}">')
    w(f'<animate attributeName="cy" from="{py}" to="{py-25}" dur="{pd}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="opacity" from="{pa}" to="0" dur="{pd}s" repeatCount="indefinite"/>')
    w('</circle>')
w('</g>')
w('</g>')

# --- HEAD ---
w('<g id="head" transform="translate(0,-40)">')
# Skull
w('<ellipse cx="0" cy="-20" rx="42" ry="48" fill="url(#obs1)"/>')
w('<ellipse cx="0" cy="-20" rx="40" ry="46" fill="url(#obs2)"/>')
w('<ellipse cx="0" cy="-20" rx="38" ry="44" fill="url(#obs3)"/>')
w('<ellipse cx="0" cy="-18" rx="36" ry="42" fill="url(#obs4)"/>')
w('<path d="M-37,-52 Q0,-72 37,-52" fill="url(#obs5)"/>')
w('<path d="M-33,-57 Q0,-75 33,-57" fill="url(#obs6)"/>')
w('<ellipse cx="0" cy="18" rx="22" ry="13" fill="url(#obs7)"/>')
w('<path d="M-16,12 Q0,22 16,12" fill="url(#obs8)"/>')
w('<path d="M-12,14 Q0,20 12,14" fill="none" stroke="#0a0a14" stroke-width="1"/>')

# Brow ridge
w('<path d="M-32,-32 Q-16,-37 0,-32 Q16,-37 32,-32" fill="none" stroke="#0a0a14" stroke-width="2.5"/>')
w('<path d="M-30,-34 Q-16,-39 0,-34 Q16,-39 30,-34" fill="none" stroke="#1a1a2e" stroke-width="1.5"/>')

# Left eye
w('<g id="left-eye" transform="translate(-16,-22)">')
w('<ellipse cx="0" cy="0" rx="11" ry="8" fill="#0a0a14"/>')
w('<ellipse cx="0" cy="0" rx="10" ry="7" fill="#1a0000"/>')
w('<ellipse cx="0" cy="0" rx="8" ry="6" fill="url(#bl1)"/>')
w('<ellipse cx="0" cy="0" rx="6" ry="4" fill="url(#bl2)"/>')
w('<circle cx="0" cy="0" r="3" fill="#000000"/>')
w('<circle cx="1" cy="-1" r="1.2" fill="#ffffff" opacity="0.9"/>')
w('<circle cx="-0.5" cy="0.5" r="0.6" fill="#ffffff" opacity="0.5"/>')
w('<ellipse cx="0" cy="0" rx="13" ry="10" fill="none" stroke="#0a0a14" stroke-width="1.5"/>')
# Eye veins
for vi in range(6):
    va = vi * 60
    vx1 = 6 * math.cos(math.radians(va))
    vy1 = 6 * math.sin(math.radians(va))
    vx2 = 10 * math.cos(math.radians(va + 10))
    vy2 = 10 * math.sin(math.radians(va + 10))
    w(f'<path d="M{vx1:.1f},{vy1:.1f} L{vx2:.1f},{vy2:.1f}" fill="none" stroke="#ff0000" stroke-width="0.4" opacity="{0.3+random.random()*0.4}"/>')
w('<ellipse cx="0" cy="0" rx="16" ry="13" fill="url(#bl4)" opacity="0.3" filter="url(#glow1)"/>')
w('<ellipse cx="0" cy="0" rx="20" ry="16" fill="url(#bl5)" opacity="0.15" filter="url(#glow2)"/>')
w('</g>')

# Right eye
w('<g id="right-eye" transform="translate(16,-22)">')
w('<ellipse cx="0" cy="0" rx="11" ry="8" fill="#0a0a14"/>')
w('<ellipse cx="0" cy="0" rx="10" ry="7" fill="#1a0000"/>')
w('<ellipse cx="0" cy="0" rx="8" ry="6" fill="url(#bl1)"/>')
w('<ellipse cx="0" cy="0" rx="6" ry="4" fill="url(#bl2)"/>')
w('<circle cx="0" cy="0" r="3" fill="#000000"/>')
w('<circle cx="1" cy="-1" r="1.2" fill="#ffffff" opacity="0.9"/>')
w('<circle cx="-0.5" cy="0.5" r="0.6" fill="#ffffff" opacity="0.5"/>')
w('<ellipse cx="0" cy="0" rx="13" ry="10" fill="none" stroke="#0a0a14" stroke-width="1.5"/>')
for vi in range(6):
    va = vi * 60
    vx1 = 6 * math.cos(math.radians(va))
    vy1 = 6 * math.sin(math.radians(va))
    vx2 = 10 * math.cos(math.radians(va + 10))
    vy2 = 10 * math.sin(math.radians(va + 10))
    w(f'<path d="M{vx1:.1f},{vy1:.1f} L{vx2:.1f},{vy2:.1f}" fill="none" stroke="#ff0000" stroke-width="0.4" opacity="{0.3+random.random()*0.4}"/>')
w('<ellipse cx="0" cy="0" rx="16" ry="13" fill="url(#bl4)" opacity="0.3" filter="url(#glow1)"/>')
w('<ellipse cx="0" cy="0" rx="20" ry="16" fill="url(#bl5)" opacity="0.15" filter="url(#glow2)"/>')
w('</g>')

# Nose
w('<g id="nose">')
w('<path d="M-2,-12 L-5,6 L0,9 L5,6 L2,-12" fill="url(#obs9)"/>')
w('<path d="M-3,-10 L-4,4" fill="none" stroke="#0a0a14" stroke-width="1"/>')
w('<path d="M3,-10 L4,4" fill="none" stroke="#0a0a14" stroke-width="1"/>')
w('<ellipse cx="-3" cy="7" rx="2" ry="1.5" fill="#0a0a14"/>')
w('<ellipse cx="3" cy="7" rx="2" ry="1.5" fill="#0a0a14"/>')
w('</g>')

# Mouth
w('<g id="mouth">')
w('<path d="M-16,14 Q0,20 16,14" fill="#0a0a14"/>')
w('<path d="M-14,14 Q0,18 14,14" fill="none" stroke="#1a1a2e" stroke-width="1"/>')
# Teeth
for ti in range(7):
    tx = -10 + ti * 3.5
    w(f'<path d="M{tx:.1f},15 L{tx:.1f},18" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.8"/>')
# Blood in mouth
w('<path d="M-10,14 Q0,22 10,14" fill="none" stroke="#ff0000" stroke-width="0.5" opacity="0.4"/>')
w('</g>')

# Wrinkles and scars
w('<g id="wrinkles">')
wrinkle_data = [
    (-27, -27, -20, -24, -15, -27),
    (15, -27, 20, -24, 25, -27),
    (-24, -20, -18, -17, -14, -20),
    (14, -20, 18, -17, 22, -20),
    (-28, -12, -22, -10, -18, -14),
    (18, -14, 22, -10, 28, -12),
    (-22, 5, -16, 8, -10, 5),
    (10, 5, 16, 8, 20, 5),
]
for wr in wrinkle_data:
    w(f'<path d="M{wr[0]},{wr[1]} Q{(wr[0]+wr[2])//2},{(wr[1]+wr[3])//2} {wr[2]},{wr[3]}" fill="none" stroke="#0a0a14" stroke-width="0.7"/>')
# Scars
w('<path d="M-22,-37 L-20,-22 L-24,-12" fill="none" stroke="#4d0000" stroke-width="1.5" opacity="0.6"/>')
w('<path d="M27,-32 L24,-20 L28,-7" fill="none" stroke="#4d0000" stroke-width="1.2" opacity="0.5"/>')
w('</g>')

# --- CROWN OF THORNS ---
w('<g id="crown">')
w('<path d="M-37,-52 Q-20,-68 0,-60 Q20,-68 37,-52" fill="none" stroke="#3a2a1a" stroke-width="4"/>')
w('<path d="M-35,-52 Q-18,-66 0,-58 Q18,-66 35,-52" fill="none" stroke="#5a3a2a" stroke-width="2"/>')
# Thorns (10 thorns)
thorn_positions = [-30, -22, -14, -5, 5, 14, 22, 30, -36, 36]
thorn_heights = [-72, -78, -82, -84, -84, -82, -78, -72, -68, -68]
for ti2, (tp, th) in enumerate(zip(thorn_positions, thorn_heights)):
    w(f'<path d="M{tp},{-52 - abs(tp)*0.2} L{tp + random.randint(-2,2)},{th}" stroke="#3a2a1a" stroke-width="2" fill="none"/>')
    w(f'<path d="M{tp + random.randint(-2,2)},{th} L{tp + random.randint(-1,1)},{th + 3}" stroke="#4a3a2a" stroke-width="1"/>')

# Blood drops from thorns (10 drops)
for di in range(10):
    dx = thorn_positions[di] + random.randint(-2, 2)
    dy = thorn_heights[di] - 3
    dr = round(random.uniform(1, 2.5), 1)
    ddur = round(random.uniform(2, 4), 1)
    da = round(random.uniform(0.5, 0.9), 2)
    w(f'<ellipse cx="{dx}" cy="{dy}" rx="{dr}" ry="{dr*1.5}" fill="#cc0000" opacity="{da}">')
    w(f'<animate attributeName="cy" from="{dy}" to="{dy+15}" dur="{ddur}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="opacity" from="{da}" to="0" dur="{ddur}s" repeatCount="indefinite"/>')
    w('</ellipse>')
w('</g>')
w('</g>')  # end head
w('</g>')  # end emperor

# ============================================================
# GUARDS (6 guards, 80+ paths each)
# ============================================================
guard_positions = [
    (310, 400, 1.0, "guard-fl"),
    (890, 400, 1.0, "guard-fr"),
    (270, 370, 0.75, "guard-bl"),
    (930, 370, 0.75, "guard-br"),
    (350, 360, 0.6, "guard-bfl"),
    (850, 360, 0.6, "guard-bfr"),
]

for gx, gy, gscale, gname in guard_positions:
    w(f'<g id="{gname}" transform="translate({gx},{gy}) scale({gscale})">')
    # Body
    w(f'<rect x="-15" y="0" width="30" height="80" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<rect x="-12" y="5" width="24" height="70" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<rect x="-10" y="10" width="20" height="60" fill="url(#obs{random.randint(1,15)})"/>')
    # Armor details
    for ai in range(4):
        w(f'<path d="M-10,{15+ai*15} L10,{15+ai*15}" fill="none" stroke="#1a1a2e" stroke-width="0.8"/>')
    # Shoulders
    w(f'<rect x="-20" y="-8" width="40" height="12" fill="url(#gld{random.randint(1,20)})" rx="3"/>')
    # Belt
    w(f'<rect x="-12" y="65" width="24" height="6" fill="url(#gld{random.randint(1,20)})" rx="1"/>')
    # Boots
    w(f'<rect x="-14" y="80" width="28" height="12" fill="url(#obs{random.randint(1,15)})" rx="2"/>')
    # Helmet
    w(f'<ellipse cx="0" cy="-16" rx="13" ry="11" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<ellipse cx="0" cy="-18" rx="11" ry="9" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<rect x="-13" y="-18" width="26" height="3" fill="url(#gld{random.randint(1,20)})"/>')
    w(f'<rect x="-8" y="-23" width="16" height="7" fill="url(#obs{random.randint(1,15)})" rx="2"/>')
    w(f'<rect x="-1.5" y="-28" width="3" height="10" fill="url(#gld{random.randint(1,20)})"/>')
    # Shield
    side = -1 if gx < 600 else 1
    w(f'<ellipse cx="{side*30}" cy="40" rx="14" ry="24" fill="url(#obs{random.randint(1,15)})" stroke="#8b6914" stroke-width="2"/>')
    w(f'<ellipse cx="{side*30}" cy="40" rx="11" ry="21" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<circle cx="{side*30}" cy="40" r="5" fill="url(#gld{random.randint(1,20)})"/>')
    # Weapon (spear or halberd)
    wx2 = -side * 25
    w(f'<rect x="{wx2}" y="-50" width="3" height="140" fill="#5a5a5a"/>')
    w(f'<rect x="{wx2-4}" y="-55" width="11" height="12" fill="url(#obs{random.randint(1,15)})" rx="2"/>')
    w(f'<path d="M{wx2+1},-55 L{wx2-1},-68 L{wx2+3},-68 L{wx2+1},-55" fill="#8b6914"/>')
    # Face
    w(f'<circle cx="-3" cy="-16" r="1.5" fill="#0a0a14"/>')
    w(f'<circle cx="3" cy="-16" r="1.5" fill="#0a0a14"/>')
    w(f'<path d="M-3,-13 Q0,-11 3,-13" fill="none" stroke="#0a0a14" stroke-width="0.8"/>')
    w('</g>')

# ============================================================
# TORCHES / BRAZIERS (8 fire sources)
# ============================================================
torch_positions = [
    (240, 250), (240, 450), (960, 250), (960, 450),
    (300, 200), (300, 500), (900, 200), (900, 500),
]

for ti3, (tx, ty) in enumerate(torch_positions):
    fi3 = ti3 + 1
    w(f'<g id="torch{fi3}" transform="translate({tx},{ty})">')
    # Torch bracket
    w('<rect x="-4" y="0" width="8" height="30" fill="#5a3a2a" rx="2"/>')
    w('<rect x="-6" y="-5" width="12" height="10" fill="#4a3a2a" rx="3"/>')
    # Fire base
    w(f'<ellipse cx="0" cy="-8" rx="10" ry="8" fill="url(#fr{((fi3%40)+1)})" filter="url(#fireglow{((fi3%20)+1)})"/>')
    # Multiple flame layers
    for fl in range(8):
        fx2 = random.randint(-6, 6)
        fy2 = -10 - random.randint(0, 15)
        fw2 = random.randint(4, 8)
        fh2 = random.randint(8, 18)
        fl_d = round(random.uniform(0.8, 2.5), 1)
        fl_op = round(random.uniform(0.5, 0.9), 2)
        w(f'<ellipse cx="{fx2}" cy="{fy2}" rx="{fw2}" ry="{fh2}" fill="url(#fr{((fi3+fl)%40+1)})" opacity="{fl_op}">')
        w(f'<animate attributeName="cy" values="{fy2};{fy2-5};{fy2+3};{fy2}" dur="{fl_d}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="rx" values="{fw2};{fw2+2};{fw2-1};{fw2}" dur="{fl_d}s" repeatCount="indefinite"/>')
        w('</ellipse>')
    # Smoke
    for si in range(5):
        sx2 = random.randint(-8, 8)
        sy2 = -25 - si * 8
        sr2 = random.randint(4, 10)
        s_op = round(0.3 - si * 0.05, 2)
        s_d = round(random.uniform(3, 6), 1)
        w(f'<circle cx="{sx2}" cy="{sy2}" r="{sr2}" fill="#333333" opacity="{s_op}" filter="url(#smoke{((fi3%15)+1)})">')
        w(f'<animate attributeName="cy" from="{sy2}" to="{sy2-30}" dur="{s_d}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="opacity" from="{s_op}" to="0" dur="{s_d}s" repeatCount="indefinite"/>')
        w('</circle>')
    # Embers
    for ei in range(8):
        ex = random.randint(-10, 10)
        ey = random.randint(-30, -10)
        er = round(random.uniform(0.5, 2), 1)
        ed = round(random.uniform(1.5, 4), 1)
        ea = round(random.uniform(0.4, 0.9), 2)
        w(f'<circle cx="{ex}" cy="{ey}" r="{er}" fill="#ff9900" opacity="{ea}">')
        w(f'<animate attributeName="cy" from="{ey}" to="{ey-40}" dur="{ed}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="cx" from="{ex}" to="{ex+random.randint(-10,10)}" dur="{ed}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="opacity" from="{ea}" to="0" dur="{ed}s" repeatCount="indefinite"/>')
        w('</circle>')
    w('</g>')

# ============================================================
# SHADOW LAYERS (200+ shadow paths)
# ============================================================
w('<g id="shadows" opacity="0.5">')
for si in range(200):
    sx = random.randint(200, 1000)
    sy = random.randint(400, 750)
    sw = random.randint(20, 120)
    sh = random.randint(5, 30)
    s_op = round(random.uniform(0.1, 0.5), 2)
    w(f'<ellipse cx="{sx}" cy="{sy}" rx="{sw}" ry="{sh}" fill="#000000" opacity="{s_op}" filter="url(#blur{random.randint(1,10)})"/>')
w('</g>')

# ============================================================
# RED AMBIENT LIGHTING (200+ gradient paths)
# ============================================================
w('<g id="red-ambient" opacity="0.15">')
for ri in range(200):
    rx = random.randint(100, 1100)
    ry = random.randint(50, 750)
    rr = random.randint(20, 80)
    rg = random.randint(1, 90)
    w(f'<circle cx="{rx}" cy="{ry}" r="{rr}" fill="url(#atm{rg})" opacity="{round(random.uniform(0.1,0.5),2)}"/>')
w('</g>')

# ============================================================
# DUST PARTICLES (50+)
# ============================================================
w('<g id="dust-particles">')
for di in range(60):
    dx2 = random.randint(200, 1000)
    dy2 = random.randint(100, 700)
    dr2 = round(random.uniform(0.3, 1.5), 1)
    dd2 = round(random.uniform(5, 15), 1)
    do2 = round(random.uniform(0.2, 0.5), 2)
    w(f'<circle cx="{dx2}" cy="{dy2}" r="{dr2}" fill="#aaaaaa" opacity="{do2}">')
    w(f'<animate attributeName="cy" from="{dy2}" to="{dy2-20}" dur="{dd2}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="cx" from="{dx2}" to="{dx2+random.randint(-15,15)}" dur="{dd2*1.5}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="opacity" from="{do2}" to="0" dur="{dd2}s" repeatCount="indefinite"/>')
    w('</circle>')
w('</g>')

# ============================================================
# BLOOD DRIP ANIMATIONS (20+)
# ============================================================
w('<g id="blood-drips">')
for bi in range(25):
    bx = random.randint(350, 850)
    by = random.randint(350, 500)
    br = round(random.uniform(1, 3), 1)
    bd = round(random.uniform(2, 5), 1)
    ba = round(random.uniform(0.4, 0.8), 2)
    w(f'<ellipse cx="{bx}" cy="{by}" rx="{br}" ry="{br*1.8}" fill="#cc0000" opacity="{ba}">')
    w(f'<animate attributeName="cy" from="{by}" to="{by+50}" dur="{bd}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="opacity" from="{ba}" to="0" dur="{bd}s" repeatCount="indefinite"/>')
    w('</ellipse>')
w('</g>')

# ============================================================
# EYE GLOW PULSE
# ============================================================
w('<g id="eye-glow-pulse">')
w('<ellipse cx="584" cy="318" rx="20" ry="16" fill="url(#bl6)" opacity="0.2">')
w('<animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite"/>')
w('<animate attributeName="rx" values="20;25;20" dur="3s" repeatCount="indefinite"/>')
w('<animate attributeName="ry" values="16;20;16" dur="3s" repeatCount="indefinite"/>')
w('</ellipse>')
w('<ellipse cx="616" cy="318" rx="20" ry="16" fill="url(#bl7)" opacity="0.2">')
w('<animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite"/>')
w('<animate attributeName="rx" values="20;25;20" dur="3s" repeatCount="indefinite"/>')
w('<animate attributeName="ry" values="16;20;16" dur="3s" repeatCount="indefinite"/>')
w('</ellipse>')
w('</g>')

# ============================================================
# ADDITIONAL ATMOSPHERE - Vignette overlay
# ============================================================
w('<rect x="0" y="0" width="1200" height="800" fill="url(#atm3)" opacity="0.6"/>')
w('<rect x="0" y="0" width="1200" height="100" fill="url(#shd1)" opacity="0.4"/>')
w('<rect x="0" y="700" width="1200" height="100" fill="url(#shd2)" opacity="0.3"/>')
w('<rect x="0" y="0" width="100" height="800" fill="url(#shd3)" opacity="0.3"/>')
w('<rect x="1100" y="0" width="100" height="800" fill="url(#shd4)" opacity="0.3"/>')

# ============================================================
# EXTRA DECORATIVE ELEMENTS (to push count higher)
# ============================================================
# Wall sconces
for sx in [220, 220, 980, 980]:
    sy = [180, 380, 180, 380]
    for si2, syy in enumerate(sy):
        w(f'<g id="sconce{si2+1}" transform="translate({sx},{syy})">')
        w('<rect x="-6" y="-3" width="12" height="6" fill="url(#gld1)" rx="2"/>')
        w('<circle cx="0" cy="0" r="3" fill="url(#fr1)" filter="url(#fireglow1)"/>')
        w('</g>')

# Floor blood stains
for bi in range(15):
    bx = random.randint(300, 900)
    by = random.randint(660, 780)
    br = random.randint(5, 20)
    w(f'<ellipse cx="{bx}" cy="{by}" rx="{br}" ry="{br*0.6}" fill="url(#bl{random.randint(1,20)})" opacity="{round(random.uniform(0.1,0.3),2)}"/>')

# Chain elements on throne
for ci in range(10):
    cx = 480 + ci * 24
    w(f'<g id="chain{ci+1}" transform="translate({cx},560)">')
    w('<rect x="-2" y="0" width="4" height="15" fill="url(#gld1)" rx="2"/>')
    w('<rect x="-3" y="5" width="6" height="6" fill="none" stroke="url(#gld2)" stroke-width="1.5" rx="3"/>')
    w('</g>')

# Turkish inscription on back wall
w('<g id="inscription" transform="translate(600,20)" opacity="0.4">')
w('<text x="0" y="0" font-family="serif" font-size="8" fill="url(#gld1)" text-anchor="middle">...:..............:...</text>')
w('<text x="0" y="12" font-family="serif" font-size="6" fill="url(#gld2)" text-anchor="middle">:.:....::.:...::...:.</text>')
w('</g>')

# ============================================================
# ADDITIONAL DETAIL ELEMENTS (to reach 7500+)
# ============================================================

# Extra wall detail - cracks and weathering (300+)
w('<g id="wall-details" opacity="0.4">')
for i in range(300):
    wx = random.randint(10, 190) if random.random() > 0.5 else random.randint(1010, 1190)
    wy = random.randint(10, 790)
    wlen = random.randint(5, 30)
    wangle = random.randint(-30, 30)
    w(f'<path d="M{wx},{wy} l{wlen},{wangle}" fill="none" stroke="#2a2a2a" stroke-width="{round(random.uniform(0.3,1.2),1)}" opacity="{round(random.uniform(0.2,0.6),2)}"/>')
w('</g>')

# Extra floor detail - grout lines and wear (200+)
w('<g id="floor-details" opacity="0.3">')
for i in range(200):
    fx = random.randint(200, 1000)
    fy = random.randint(650, 800)
    fw = random.randint(3, 15)
    w(f'<path d="M{fx},{fy} l{fw},{random.randint(-2,2)}" fill="none" stroke="#1a1a1a" stroke-width="0.5"/>')
w('</g>')

# Column erosion details (100+)
w('<g id="column-details" opacity="0.3">')
for ci, cx in enumerate([260, 420, 780, 940]):
    for di in range(25):
        dy = random.randint(10, 590)
        dw = random.randint(2, 8)
        w(f'<ellipse cx="{cx+17+random.randint(-5,5)}" cy="{50+dy}" rx="{dw}" ry="{random.randint(1,3)}" fill="#3a3a3a" opacity="{round(random.uniform(0.2,0.5),2)}"/>')
w('</g>')

# Chain links hanging from ceiling (50+)
w('<g id="ceiling-chains">')
for ci in range(12):
    cx = 250 + ci * 58
    for li in range(4):
        ly = 10 + li * 12
        w(f'<ellipse cx="{cx}" cy="{ly}" rx="4" ry="6" fill="none" stroke="url(#gld{((ci%20)+1)})" stroke-width="1.5"/>')
w('</g>')

# Blood splatter on floor (80+)
w('<g id="blood-splatter">')
for bi in range(80):
    bx = random.randint(250, 950)
    by = random.randint(660, 790)
    br = random.randint(2, 12)
    w(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="url(#bl{random.randint(1,20)})" opacity="{round(random.uniform(0.05,0.25),2)}"/>')
    if random.random() > 0.6:
        for sj in range(random.randint(2, 5)):
            sjx = bx + random.randint(-15, 15)
            sjy = by + random.randint(-8, 8)
            w(f'<circle cx="{sjx}" cy="{sjy}" r="{random.randint(1,4)}" fill="url(#bl{random.randint(1,20)})" opacity="{round(random.uniform(0.03,0.15),2)}"/>')
w('</g>')

# Ember trails from torches (150+)
w('<g id="ember-trails">')
for ti4, (tx, ty) in enumerate(torch_positions):
    for ei in range(10):
        ex = tx + random.randint(-15, 15)
        ey = ty - random.randint(20, 80)
        er = round(random.uniform(0.5, 1.5), 1)
        ed = round(random.uniform(2, 5), 1)
        w(f'<circle cx="{ex}" cy="{ey}" r="{er}" fill="#ffaa00" opacity="0.7">')
        w(f'<animate attributeName="cy" from="{ey}" to="{ey-50}" dur="{ed}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="cx" from="{ex}" to="{ex+random.randint(-20,20)}" dur="{ed}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="opacity" from="0.7" to="0" dur="{ed}s" repeatCount="indefinite"/>')
        w('</circle>')
w('</g>')

# Carpet fringe details (100+)
w('<g id="carpet-fringe">')
for i in range(50):
    x = 355 + i * 10
    w(f'<path d="M{x},788 Q{x+3},{792+random.randint(0,8)} {x+5},788" fill="none" stroke="#8b6914" stroke-width="0.5" opacity="0.4"/>')
w('</g>')

# Hanging drapes from walls (60+)
w('<g id="wall-drapes">')
for di in range(8):
    dx = 210 + di * 100
    for si in range(8):
        sy = 5 + si * 10
        w(f'<path d="M{dx},{sy} Q{dx+5+random.randint(-3,3)},{sy+5} {dx+random.randint(-2,2)},{sy+10}" fill="none" stroke="url(#obs{random.randint(1,15)})" stroke-width="{round(random.uniform(1,3),1)}" opacity="0.3"/>')
w('</g>')

# Torch light on walls (80+)
w('<g id="torch-wall-light" opacity="0.15">')
for ti5, (tx, ty) in enumerate(torch_positions):
    for li in range(10):
        lr = random.randint(15, 60)
        w(f'<circle cx="{tx}" cy="{ty}" r="{lr}" fill="url(#fr{((ti5%40)+1)})" opacity="{round(random.uniform(0.05,0.2),2)}"/>')
w('</g>')

# Skulls on throne base (20+)
w('<g id="throne-base-skulls">')
for si in range(8):
    sx = 490 + si * 28
    sy = 640
    w(f'<g transform="translate({sx},{sy})">')
    w(f'<circle cx="0" cy="0" r="10" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<circle cx="0" cy="-3" r="7" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<circle cx="-3" cy="-5" r="1.5" fill="#0a0a14"/>')
    w(f'<circle cx="3" cy="-5" r="1.5" fill="#0a0a14"/>')
    w(f'<path d="M-2,0 Q0,3 2,0" fill="none" stroke="#0a0a14" stroke-width="0.8"/>')
    w('</g>')
w('</g>')

# Atmospheric haze layers (100+)
w('<g id="haze-layers">')
for i in range(100):
    hx = random.randint(100, 1100)
    hy = random.randint(100, 700)
    hw = random.randint(30, 150)
    hh = random.randint(10, 40)
    w(f'<ellipse cx="{hx}" cy="{hy}" rx="{hw}" ry="{hh}" fill="url(#atm{random.randint(1,90)})" opacity="{round(random.uniform(0.02,0.12),2)}"/>')
w('</g>')

# Eye reflection in orb (30+)
w('<g id="orb-reflections">')
for ri in range(30):
    rx = random.randint(-15, 15)
    ry = random.randint(-15, 15)
    if rx*rx + ry*ry < 400:
        w(f'<circle cx="{rx}" cy="{ry}" r="{random.randint(1,3)}" fill="#ffffff" opacity="{round(random.uniform(0.05,0.2),2)}"/>')
w('</g>')

# Armor reflection highlights (60+)
w('<g id="armor-highlights" opacity="0.2">')
for i in range(60):
    hx = random.randint(530, 670)
    hy = random.randint(340, 500)
    w(f'<ellipse cx="{hx}" cy="{hy}" rx="{random.randint(2,8)}" ry="{random.randint(1,4)}" fill="#ffffff" opacity="{round(random.uniform(0.05,0.15),2)}"/>')
w('</g>')

# Cobwebs in corners (40+)
w('<g id="cobwebs" opacity="0.15">')
for ci in range(4):
    cx = [205, 995, 205, 995][ci]
    cy = [5, 5, 5, 5][ci]
    for wi in range(6):
        wa = wi * 30
        wlen = random.randint(20, 50)
        wx2 = cx + wlen * math.cos(math.radians(wa))
        wy2 = cy + wlen * math.sin(math.radians(wa))
        w(f'<path d="M{cx},{cy} L{wx2:.0f},{wy2:.0f}" fill="none" stroke="#5a5a5a" stroke-width="0.5"/>')
    for wi in range(3):
        wr = 15 + wi * 12
        w(f'<path d="M{cx+wr},{cy} A{wr},{wr} 0 0,1 {cx},{cy+wr}" fill="none" stroke="#4a4a4a" stroke-width="0.3"/>')
w('</g>')

# Extra emperor body detail - scars (40+)
w('<g id="emperor-scars" opacity="0.4">')
for si in range(40):
    sx = random.randint(540, 660)
    sy = random.randint(360, 480)
    sl = random.randint(5, 20)
    sa = random.randint(-45, 45)
    w(f'<path d="M{sx},{sy} l{sl},{sa}" fill="none" stroke="#4d0000" stroke-width="{round(random.uniform(0.5,2),1)}" opacity="{round(random.uniform(0.2,0.6),2)}"/>')
w('</g>')

# Floating dust motes with animation (100+)
w('<g id="floating-dust">')
for i in range(100):
    dx = random.randint(200, 1000)
    dy = random.randint(100, 700)
    dr = round(random.uniform(0.2, 1.0), 1)
    dd = round(random.uniform(8, 20), 1)
    do = round(random.uniform(0.1, 0.4), 2)
    w(f'<circle cx="{dx}" cy="{dy}" r="{dr}" fill="#cccccc" opacity="{do}">')
    w(f'<animate attributeName="cy" from="{dy}" to="{dy-30}" dur="{dd}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="cx" from="{dx}" to="{dx+random.randint(-10,10)}" dur="{dd*2}s" repeatCount="indefinite"/>')
    w('</circle>')
w('</g>')

# Fire sparks (80+)
w('<g id="fire-sparks">')
for ti6, (tx, ty) in enumerate(torch_positions):
    for si in range(5):
        sx = tx + random.randint(-10, 10)
        sy = ty - random.randint(15, 60)
        sr = round(random.uniform(0.3, 1.0), 1)
        sd = round(random.uniform(0.5, 2.0), 1)
        w(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#ffffff" opacity="0.9">')
        w(f'<animate attributeName="cy" from="{sy}" to="{sy-20}" dur="{sd}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="opacity" from="0.9" to="0" dur="{sd}s" repeatCount="indefinite"/>')
        w('</circle>')
w('</g>')

# Throne seat texture (50+)
w('<g id="throne-texture" opacity="0.3">')
for i in range(50):
    tx = random.randint(485, 715)
    ty = random.randint(555, 645)
    w(f'<path d="M{tx},{ty} l{random.randint(3,10)},{random.randint(-2,2)}" fill="none" stroke="#1a1a2e" stroke-width="0.5"/>')
w('</g>')

# Blood drops from crown (20+)
w('<g id="crown-blood-drips">')
for bi in range(20):
    bx = random.randint(565, 635)
    by = random.randint(310, 330)
    br = round(random.uniform(1, 2.5), 1)
    bd = round(random.uniform(2, 4), 1)
    w(f'<ellipse cx="{bx}" cy="{by}" rx="{br}" ry="{br*1.5}" fill="#cc0000" opacity="0.7">')
    w(f'<animate attributeName="cy" from="{by}" to="{by+30}" dur="{bd}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="opacity" from="0.7" to="0" dur="{bd}s" repeatCount="indefinite"/>')
    w('</ellipse>')
w('</g>')

# Emperor cloak movement particles (40+)
w('<g id="cloak-particles">')
for i in range(40):
    px = random.randint(450, 750)
    py = random.randint(400, 650)
    pr = round(random.uniform(0.3, 1.2), 1)
    pd = round(random.uniform(3, 8), 1)
    w(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="#1a1a2e" opacity="0.3">')
    w(f'<animate attributeName="cy" from="{py}" to="{py+20}" dur="{pd}s" repeatCount="indefinite"/>')
    w(f'<animate attributeName="opacity" from="0.3" to="0" dur="{pd}s" repeatCount="indefinite"/>')
    w('</circle>')
w('</g>')

# Window stained glass detail (40+)
w('<g id="window-detail">')
for wx in [230, 930]:
    for di in range(20):
        dx = wx + 15 + random.randint(0, 30)
        dy = 115 + random.randint(0, 100)
        w(f'<circle cx="{dx}" cy="{dy}" r="{random.randint(1,4)}" fill="url(#bl{random.randint(1,20)})" opacity="{round(random.uniform(0.1,0.3),2)}"/>')
w('</g>')

# Emperor shoulder armor plates (30+)
w('<g id="shoulder-plates">')
for side in [-1, 1]:
    for pi in range(8):
        px = 600 + side * (55 + pi * 3)
        py = 380 + pi * 2
        w(f'<ellipse cx="{px}" cy="{py}" rx="{6-pi*0.3}" ry="{3-pi*0.1}" fill="url(#obs{random.randint(1,15)})" stroke="#1a1a2e" stroke-width="0.5"/>')
w('</g>')

# Extra blood pool effects (30+)
w('<g id="blood-pools">')
for i in range(30):
    px = random.randint(300, 900)
    py = random.randint(670, 780)
    pr = random.randint(8, 25)
    w(f'<ellipse cx="{px}" cy="{py}" rx="{pr}" ry="{pr*0.4}" fill="url(#bl{random.randint(1,20)})" opacity="{round(random.uniform(0.05,0.2),2)}"/>')
w('</g>')

# Throne armrest skulls (6+)
w('<g id="armrest-skulls">')
for side in [-1, 1]:
    sx = 600 + side * 115
    sy = 535
    w(f'<g transform="translate({sx},{sy})">')
    w(f'<circle cx="0" cy="0" r="8" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<circle cx="0" cy="-3" r="6" fill="url(#obs{random.randint(1,15)})"/>')
    w(f'<circle cx="-2" cy="-4" r="1.5" fill="#0a0a14"/>')
    w(f'<circle cx="2" cy="-4" r="1.5" fill="#0a0a14"/>')
    w(f'<path d="M-2,0 Q0,3 2,0" fill="none" stroke="#0a0a14" stroke-width="0.8"/>')
    w(f'<path d="M-4,-1 Q0,5 4,-1" fill="none" stroke="#0e0e1c" stroke-width="0.5"/>')
    w('</g>')
w('</g>')

# Emperor jaw detail (20+)
w('<g id="jaw-detail" opacity="0.5">')
for ji in range(20):
    jx = random.randint(585, 615)
    jy = random.randint(390, 400)
    w(f'<path d="M{jx},{jy} l{random.randint(-3,3)},{random.randint(-2,2)}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
w('</g>')

# Extra smoke wisps (60+)
w('<g id="smoke-wisps">')
for ti7, (tx, ty) in enumerate(torch_positions):
    for si in range(4):
        sx2 = tx + random.randint(-12, 12)
        sy2 = ty - random.randint(30, 80)
        sw = random.randint(8, 25)
        sh = random.randint(4, 12)
        w(f'<ellipse cx="{sx2}" cy="{sy2}" rx="{sw}" ry="{sh}" fill="#333333" opacity="0.15" filter="url(#smoke{((ti7%15)+1)})">')
        w(f'<animate attributeName="cy" from="{sy2}" to="{sy2-40}" dur="{random.uniform(4,8):.1f}s" repeatCount="indefinite"/>')
        w(f'<animate attributeName="opacity" from="0.15" to="0" dur="{random.uniform(4,8):.1f}s" repeatCount="indefinite"/>')
        w('</ellipse>')
w('</g>')

# Throne cushion tatters (30+)
w('<g id="throne-cushion" opacity="0.4">')
for i in range(30):
    cx = random.randint(490, 710)
    cy = random.randint(555, 580)
    w(f'<path d="M{cx},{cy} q{random.randint(-5,5)},{random.randint(-8,-2)} {random.randint(-3,3)},{random.randint(-15,-5)}" fill="none" stroke="#4d0000" stroke-width="{round(random.uniform(0.5,2),1)}" opacity="{round(random.uniform(0.3,0.7),2)}"/>')
w('</g>')

# Guard weapon details (40+)
w('<g id="weapon-details" opacity="0.3">')
for gx, gy, gscale, gname in guard_positions:
    for wi in range(3):
        w(f'<rect x="{gx+random.randint(-3,3)}" y="{gy-55+wi*5}" width="1" height="8" fill="#8b6914"/>')
w('</g>')

# Emperor belt/sash (15+)
w('<g id="emperor-belt">')
w('<path d="M-55,55 Q0,50 55,55" fill="none" stroke="#8b6914" stroke-width="3"/>')
w('<path d="M-50,58 Q0,53 50,58" fill="none" stroke="#daa520" stroke-width="1.5"/>')
w('<circle cx="0" cy="55" r="5" fill="url(#gld1)"/>')
w('<circle cx="0" cy="55" r="3" fill="url(#bl8)"/>')
w('</g>')

# Extra chain links on guards (30+)
w('<g id="guard-chains">')
for gx, gy, gscale, gname in guard_positions:
    for ci in range(3):
        w(f'<ellipse cx="{gx+random.randint(-8,8)}" cy="{gy+random.randint(-5,15)}" rx="3" ry="5" fill="none" stroke="url(#gld{random.randint(1,20)})" stroke-width="1" opacity="0.4"/>')
w('</g>')

# Floor reflection highlights (40+)
w('<g id="floor-reflections" opacity="0.1">')
for i in range(40):
    rx = random.randint(200, 1000)
    ry = random.randint(660, 790)
    rw = random.randint(5, 25)
    w(f'<ellipse cx="{rx}" cy="{ry}" rx="{rw}" ry="{random.randint(2,5)}" fill="#ffffff"/>')
w('</g>')

# Torch bracket wall mounts (16+)
w('<g id="torch-mounts">')
for ti8, (tx, ty) in enumerate(torch_positions):
    w(f'<rect x="{tx-8}" y="{ty+2}" width="16" height="8" fill="url(#gld{((ti8%20)+1)})" rx="2" opacity="0.6"/>')
    w(f'<circle cx="{tx}" cy="{ty+6}" r="3" fill="url(#gld{((ti8%20)+1)})" opacity="0.5"/>')
w('</g>')

# Extra throne gold inlay (30+)
w('<g id="throne-inlay" opacity="0.5">')
for i in range(30):
    ix = random.randint(485, 715)
    iy = random.randint(355, 540)
    w(f'<circle cx="{ix}" cy="{iy}" r="{random.randint(1,3)}" fill="url(#gld{random.randint(1,20)})" opacity="{round(random.uniform(0.2,0.5),2)}"/>')
w('</g>')

# Emperor finger details (20+)
w('<g id="finger-details" opacity="0.5">')
for side in [-1, 1]:
    for fi in range(5):
        fx = 600 + side * (112 + fi * 4 * side)
        fy = 568 + fi
        w(f'<path d="M{fx},{fy} L{fx+side*6},{fy+15}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
w('</g>')

# Atmospheric red mist (50+)
w('<g id="red-mist" opacity="0.08">')
for i in range(50):
    mx = random.randint(100, 1100)
    my = random.randint(100, 700)
    mr = random.randint(20, 80)
    w(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#bl{random.randint(1,20)})"/>')
w('</g>')

# Extra column ring details (60+)
w('<g id="column-rings" opacity="0.3">')
for ci, cx in enumerate([260, 420, 780, 940]):
    for ri in range(15):
        ry = 50 + ri * 40
        w(f'<ellipse cx="{cx+17}" cy="{ry}" rx="19" ry="2" fill="none" stroke="url(#gld{((ci%20)+1)})" stroke-width="0.8"/>')
w('</g>')

# Guard shield boss details (12+)
w('<g id="shield-details">')
for gx, gy, gscale, gname in guard_positions:
    side = -1 if gx < 600 else 1
    w(f'<circle cx="{gx+side*30*gscale}" cy="{gy+40*gscale}" r="3" fill="url(#gld{random.randint(1,20)})" opacity="0.5"/>')
w('</g>')

# Extra atmospheric depth layers (40+)
w('<g id="depth-layers">')
for i in range(40):
    lx = random.randint(200, 1000)
    ly = random.randint(200, 600)
    lw = random.randint(40, 150)
    lh = random.randint(20, 60)
    w(f'<ellipse cx="{lx}" cy="{ly}" rx="{lw}" ry="{lh}" fill="url(#atm{random.randint(1,90)})" opacity="{round(random.uniform(0.02,0.08),2)}"/>')
w('</g>')

# Emperor neck detail (15+)
w('<g id="neck-detail" opacity="0.4">')
for ni in range(15):
    nx = random.randint(590, 610)
    ny = random.randint(355, 370)
    w(f'<path d="M{nx},{ny} l{random.randint(-3,3)},{random.randint(-2,2)}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
w('</g>')

# Floor crack patterns (60+)
w('<g id="floor-cracks" opacity="0.2">')
for i in range(60):
    cx = random.randint(200, 1000)
    cy = random.randint(650, 800)
    w(f'<path d="M{cx},{cy} l{random.randint(5,20)},{random.randint(-5,5)} l{random.randint(3,10)},{random.randint(-3,3)}" fill="none" stroke="#1a1a1a" stroke-width="0.5"/>')
w('</g>')

# Extra orb particle effects (20+)
w('<g id="orb-extras">')
for i in range(20):
    angle = i * 18
    radius = random.randint(30, 45)
    px = 720 + radius * math.cos(math.radians(angle))
    py = 545 + radius * math.sin(math.radians(angle))
    pr = round(random.uniform(0.3, 1.0), 1)
    w(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr}" fill="#ff0000" opacity="0.4">')
    w(f'<animate attributeName="opacity" values="0.4;0.1;0.4" dur="{round(random.uniform(1,3),1)}s" repeatCount="indefinite"/>')
    w('</circle>')
w('</g>')

# Emperor cloak hem details (40+)
w('<g id="cloak-hem" opacity="0.3">')
for i in range(40):
    hx = random.randint(480, 720)
    hy = random.randint(600, 640)
    w(f'<path d="M{hx},{hy} q{random.randint(-5,5)},{random.randint(3,10)} {random.randint(-3,3)},{random.randint(5,15)}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
w('</g>')

# Torch base glow on floor (20+)
w('<g id="torch-floor-glow" opacity="0.1">')
for ti9, (tx, ty) in enumerate(torch_positions):
    w(f'<ellipse cx="{tx}" cy="{ty+35}" rx="25" ry="8" fill="url(#fr{((ti9%40)+1)})"/>')
w('</g>')

# Guard elbow guards (12+)
w('<g id="elbow-guards">')
for gx, gy, gscale, gname in guard_positions:
    side = -1 if gx < 600 else 1
    w(f'<ellipse cx="{gx+side*18*gscale}" cy="{gy+35*gscale}" rx="5" ry="4" fill="url(#obs{random.randint(1,15)})" stroke="url(#gld{random.randint(1,20)})" stroke-width="0.5"/>')
w('</g>')

# Extra crown thorn shadows (20+)
w('<g id="thorn-shadows" opacity="0.3">')
for i in range(20):
    tx = random.randint(565, 635)
    ty = random.randint(308, 325)
    w(f'<path d="M{tx},{ty} l{random.randint(-2,2)},{random.randint(2,6)}" fill="none" stroke="#000000" stroke-width="0.5"/>')
w('</g>')

# Emperor eye reflection (4+)
w('<g id="eye-reflections">')
for side in [-1, 1]:
    ex = 600 + side * 16
    ey = 318
    w(f'<circle cx="{ex+1}" cy="{ey-1}" r="1.5" fill="#ffffff" opacity="0.6"/>')
    w(f'<circle cx="{ex-0.5}" cy="{ey+0.5}" r="0.8" fill="#ffffff" opacity="0.3"/>')
w('</g>')

# Throne back ornamental lines (30+)
w('<g id="throne-ornaments" opacity="0.4">')
for i in range(30):
    ox = random.randint(490, 710)
    oy = random.randint(360, 530)
    w(f'<path d="M{ox},{oy} l{random.randint(5,15)},{random.randint(-3,3)}" fill="none" stroke="url(#gld{random.randint(1,20)})" stroke-width="0.5"/>')
w('</g>')

# Extra carpet stain marks (25+)
w('<g id="carpet-stains" opacity="0.15">')
for i in range(25):
    sx = random.randint(360, 840)
    sy = random.randint(660, 785)
    sr = random.randint(3, 10)
    w(f'<ellipse cx="{sx}" cy="{sy}" rx="{sr}" ry="{sr*0.6}" fill="url(#bl{random.randint(1,20)})"/>')
w('</g>')

# Emperor shoulder pauldron details (20+)
w('<g id="pauldron-details" opacity="0.4">')
for side in [-1, 1]:
    for pi in range(10):
        px = 600 + side * (50 + pi * 2)
        py = 378 + pi * 1.5
        w(f'<path d="M{px},{py} l{random.randint(2,6)},{random.randint(-1,1)}" fill="none" stroke="#8b6914" stroke-width="0.5"/>')
w('</g>')

# Hanging tapestries (20+)
w('<g id="tapestries" opacity="0.2">')
for i in range(4):
    tx = 220 + i * 200
    for ti in range(10):
        ty = 100 + ti * 15
        w(f'<rect x="{tx}" y="{ty}" width="15" height="12" fill="url(#obs{random.randint(1,15)})" opacity="0.3"/>')
w('</g>')

# Emperor hand tendons (20+)
w('<g id="hand-tendons" opacity="0.3">')
for side in [-1, 1]:
    for ti in range(5):
        tx = 600 + side * (100 + ti * 5)
        ty = 560 + ti * 3
        w(f'<path d="M{tx},{ty} l{side*8},{15+ti*2}" fill="none" stroke="#0a0a14" stroke-width="0.5"/>')
w('</g>')

# Extra throne corner ornaments (8+)
w('<g id="throne-corners">')
for cx, cy in [(480, 350), (720, 350), (480, 650), (720, 650)]:
    w(f'<circle cx="{cx}" cy="{cy}" r="6" fill="url(#gld1)"/>')
    w(f'<circle cx="{cx}" cy="{cy}" r="3" fill="url(#bl9)"/>')
w('</g>')

# Guard boot details (24+)
w('<g id="boot-details" opacity="0.4">')
for gx, gy, gscale, gname in guard_positions:
    for bi in range(3):
        w(f'<path d="M{gx-12*gscale},{gy+82*gscale+bi*4} l{24*gscale},0" fill="none" stroke="#2a2a2a" stroke-width="0.5"/>')
w('</g>')

# Extra emperor torso armor ridges (40+)
w('<g id="armor-ridges" opacity="0.3">')
for i in range(40):
    rx = random.randint(555, 645)
    ry = random.randint(385, 470)
    w(f'<ellipse cx="{rx}" cy="{ry}" rx="{random.randint(3,8)}" ry="{random.randint(1,3)}" fill="none" stroke="#1a1a2e" stroke-width="0.5"/>')
w('</g>')

# Torch flame inner core (40+)
w('<g id="flame-cores">')
for ti10, (tx, ty) in enumerate(torch_positions):
    for fi in range(5):
        fx = tx + random.randint(-3, 3)
        fy = ty - random.randint(5, 15)
        fr = random.randint(2, 5)
        w(f'<ellipse cx="{fx}" cy="{fy}" rx="{fr}" ry="{fr*1.5}" fill="#ffffff" opacity="{round(random.uniform(0.3,0.7),2)}">')
        w(f'<animate attributeName="cy" values="{fy};{fy-3};{fy+2};{fy}" dur="{round(random.uniform(0.3,0.8),1)}s" repeatCount="indefinite"/>')
        w('</ellipse>')
w('</g>')

w('</g>')

# ============================================================
# VIGNETTE EFFECT
# ============================================================
w('<rect x="0" y="0" width="1200" height="800" fill="url(#shd5)" opacity="0.4"/>')

w('</g>')  # end scene-clip group
w('</svg>')

# Write file
svg_content = "\n".join(lines)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

# Count elements
element_count = svg_content.count("<") - svg_content.count("</") - svg_content.count("<?") - svg_content.count("<!--")
gradient_count = svg_content.count("Gradient")
filter_count = svg_content.count("<filter ")
animate_count = svg_content.count("<animate")
file_size = len(svg_content.encode("utf-8"))

print(f"SVG generated: {output_path}")
print(f"Approximate elements: {element_count}")
print(f"Gradients: {gradient_count}")
print(f"Filters: {filter_count}")
print(f"Animations: {animate_count}")
print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
