import random

width = 1200
height = 450

svg_parts = []

# SVG Header & Defs
svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;family=Orbitron:wght@700;900&amp;display=swap');
      
      @keyframes float {{
        0%, 100% {{ transform: translateY(0) translateX(0); }}
        33% {{ transform: translateY(-10px) translateX(5px); }}
        66% {{ transform: translateY(5px) translateX(-5px); }}
      }}
      @keyframes floatSlow {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
      }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: 0.2; }}
        50% {{ opacity: 1; }}
      }}
      @keyframes drift {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-{height}px); }}
      }}
      @keyframes orbit-cw {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      @keyframes orbit-ccw {{
        0% {{ transform: rotate(360deg); }}
        100% {{ transform: rotate(0deg); }}
      }}
      @keyframes matrixRain {{
        0% {{ transform: translateY(-50px); opacity: 0; }}
        20% {{ opacity: 0.8; }}
        80% {{ opacity: 0.8; }}
        100% {{ transform: translateY(500px); opacity: 0; }}
      }}
      @keyframes typeRotate1 {{
        0%, 25%, 100% {{ opacity: 1; transform: translateY(0); }}
        30%, 95% {{ opacity: 0; transform: translateY(-20px); }}
      }}
      @keyframes typeRotate2 {{
        0%, 30%, 100% {{ opacity: 0; transform: translateY(20px); }}
        35%, 60% {{ opacity: 1; transform: translateY(0); }}
        65%, 95% {{ opacity: 0; transform: translateY(-20px); }}
      }}
      @keyframes typeRotate3 {{
        0%, 65%, 100% {{ opacity: 0; transform: translateY(20px); }}
        70%, 95% {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes glitch {{
        0% {{ transform: translate(0) }}
        20% {{ transform: translate(-2px, 2px) }}
        40% {{ transform: translate(-2px, -2px) }}
        60% {{ transform: translate(2px, 2px) }}
        80% {{ transform: translate(2px, -2px) }}
        100% {{ transform: translate(0) }}
      }}
      @keyframes pulse {{
        0% {{ stroke-opacity: 0.1; stroke-width: 1; }}
        50% {{ stroke-opacity: 0.8; stroke-width: 3; }}
        100% {{ stroke-opacity: 0.1; stroke-width: 1; }}
      }}
      @keyframes shootingStar {{
        0% {{ transform: translateX(0) translateY(0); opacity: 1; }}
        100% {{ transform: translateX(-800px) translateY(800px); opacity: 0; }}
      }}
      @keyframes gridMove {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 0 40px; }}
      }}

      .text-marways {{
        font-family: 'Orbitron', sans-serif;
        font-size: 110px;
        font-weight: 900;
        fill: url(#text-grad);
        filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.4)) drop-shadow(0 0 30px rgba(139, 92, 246, 0.6));
      }}
      
      .text-subtitle {{
        font-family: 'Fira Code', monospace;
        font-size: 24px;
        font-weight: 600;
        fill: #C9D1D9;
      }}
      
      .glow-orbit {{
        fill: none;
        stroke-linecap: round;
        stroke-width: 2;
      }}
    </style>
    
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0614" />
      <stop offset="50%" stop-color="#0e0a1f" />
      <stop offset="100%" stop-color="#050814" />
    </linearGradient>
    
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#67E8F9" />
      <stop offset="25%" stop-color="#06B6D4" />
      <stop offset="50%" stop-color="#8B5CF6" />
      <stop offset="75%" stop-color="#A78BFA" />
      <stop offset="100%" stop-color="#F472B6" />
    </linearGradient>

    <radialGradient id="glow-grad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0" />
    </radialGradient>
    
    <radialGradient id="glow-grad-cyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0" />
    </radialGradient>

    <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="url(#bg-grad)" />
''')

# Central Glowing Ambience
svg_parts.append(f'''
  <circle cx="20%" cy="50%" r="400" fill="url(#glow-grad)" style="mix-blend-mode: screen;" />
  <circle cx="80%" cy="50%" r="500" fill="url(#glow-grad-cyan)" style="mix-blend-mode: screen;" />
  <circle cx="50%" cy="50%" r="300" fill="url(#glow-grad)" style="mix-blend-mode: screen;" />
''')

# Starfield Generator
stars = []
for i in range(150):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.uniform(0.5, 2.5)
    duration = random.uniform(2, 6)
    delay = random.uniform(0, 5)
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" style="animation: twinkle {duration}s infinite {delay}s alternate; opacity: {random.uniform(0.1, 0.8)}" />')
svg_parts.append("\n  ".join(stars))

# Shooting Stars (multiple, animated natively)
for i in range(6):
    x_start = random.randint(600, width+400)
    y_start = random.randint(-200, height//2)
    delay = random.uniform(0, 10)
    dur = random.uniform(1.5, 3)
    svg_parts.append(f'''
  <g style="animation: shootingStar {dur}s infinite {delay}s linear; opacity: 0;">
    <line x1="{x_start}" y1="{y_start}" x2="{x_start-150}" y2="{y_start+150}" stroke="white" stroke-width="2" style="filter: blur(1px);" stroke-opacity="0.8" />
    <circle cx="{x_start-150}" cy="{y_start+150}" r="2" fill="#fff" />
  </g>
''')

# Neural Network / Constellation Generator (Floating nodes + edges)
nodes = []
for i in range(40):
    x = random.randint(50, width-50)
    y = random.randint(50, height-50)
    nodes.append((x, y))

edges_svg = []
nodes_svg = []
for i, n1 in enumerate(nodes):
    for j, n2 in enumerate(nodes):
        if i < j:
            dist = ((n1[0]-n2[0])**2 + (n1[1]-n2[1])**2)**0.5
            if dist < 120:
                op = max(0, 1 - dist/120) * 0.4
                delay = random.uniform(0, 4)
                edges_svg.append(f'<line x1="{n1[0]}" y1="{n1[1]}" x2="{n2[0]}" y2="{n2[1]}" stroke="#06B6D4" stroke-opacity="{op}" stroke-width="1" style="animation: pulse {random.uniform(3,7)}s infinite {delay}s" />')
    
    anim_delay = random.uniform(0, 5)
    dur = random.uniform(10, 20)
    nodes_svg.append(f'<g style="animation: float {dur}s infinite {anim_delay}s ease-in-out; transform-origin: {n1[0]}px {n1[1]}px;"><circle cx="{n1[0]}" cy="{n1[1]}" r="{random.uniform(1,3)}" fill="#8B5CF6" /></g>')

svg_parts.append("\n  ".join(edges_svg))
svg_parts.append("\n  ".join(nodes_svg))

# Floating Orbits / Cybernetic HUD Rings (Left & Right)
def make_orbit(cx, cy, color1, color2, reversed=False, delay=0):
    rot_anim = 'orbit-ccw' if reversed else 'orbit-cw'
    return f'''
  <g style="transform-origin: {cx}px {cy}px; animation: floatSlow 8s infinite {delay}s ease-in-out;">
    <g style="transform-origin: {cx}px {cy}px; animation: {rot_anim} {random.uniform(20, 40)}s infinite linear;">
      <circle cx="{cx}" cy="{cy}" r="{random.randint(80, 150)}" class="glow-orbit" stroke="{color1}" stroke-dasharray="{random.randint(10,40)} {random.randint(5,20)}" opacity="{random.uniform(0.3, 0.7)}" preserveAspectRatio="xMidYMid slice" />
      <circle cx="{cx}" cy="{cy}" r="{random.randint(160, 220)}" class="glow-orbit" stroke="{color2}" stroke-dasharray="2 4 {random.randint(20,60)} 10" opacity="{random.uniform(0.2, 0.5)}" />
    </g>
  </g>'''

svg_parts.append(make_orbit(150, 225, "#8B5CF6", "#06B6D4", False, 0))
svg_parts.append(make_orbit(1050, 225, "#06B6D4", "#F472B6", True, 2))


# Abstract Floating Hexagons / Boxes
svg_parts.append('''
  <g stroke="#06B6D4" fill="none" stroke-width="2" opacity="0.4" style="animation: float 15s infinite ease-in-out;">
    <polygon points="100,80 120,60 140,60 160,80 140,100 120,100" />
    <polygon points="1050,350 1070,330 1090,330 1110,350 1090,370 1070,370" />
    <polygon points="200,380 215,365 235,365 250,380 235,395 215,395" style="stroke: #8B5CF6; animation: glitch 3s infinite alternate;"/>
    <rect x="850" y="80" width="30" height="30" style="stroke: #A78BFA; transform: rotate(45deg); transform-origin: 865px 95px; animation: orbit-cw 10s infinite linear;" />
  </g>
''')

# Code rain/Matrix effect (faded in background)
rain = []
chars = "10{}()[]!@#$%=+*-/^~aBcDeFgHiJkLmNoPqRsTuVwXyZ"
for i in range(25):
    x = random.randint(50, width-50)
    delay = random.uniform(0, 15)
    dur = random.uniform(5, 12)
    s = "".join([random.choice(chars) + "\\n" for _ in range(10)]) # hacky vertical spacing in text isn't easy natively in SVG, we use separate text elements
    
    col = f'<g style="animation: matrixRain {dur}s infinite {delay}s linear; opacity: 0;">'
    for j in range(random.randint(4, 12)):
        y = j * 15
        char = random.choice(chars)
        col += f'<text x="{x}" y="{y}" font-family="monospace" font-size="12px" fill="#06B6D4" opacity="{1 - (j/15)}">{char}</text>'
    col += '</g>'
    rain.append(col)
svg_parts.append("\n  ".join(rain))


# MAIN TEXT & SUBTEXT
svg_parts.append('''
  <!-- Decorative Bracket Left -->
  <text x="50" y="270" font-family="'Orbitron', sans-serif" font-size="200px" font-weight="900" fill="#ffffff" opacity="0.05">&lt;</text>
  <!-- Decorative Bracket Right -->
  <text x="1050" y="270" font-family="'Orbitron', sans-serif" font-size="200px" font-weight="900" fill="#ffffff" opacity="0.05">&gt;</text>

  <!-- Title Text -->
  <g style="animation: float 10s infinite ease-in-out;">
    <text x="50%" y="220" text-anchor="middle" dominant-baseline="middle" class="text-marways" filter="url(#neon-glow)">
      MARWAYS
    </text>
    <text x="50%" y="220" text-anchor="middle" dominant-baseline="middle" class="text-marways" style="fill: transparent; stroke: #FFFFFF; stroke-width: 2px; stroke-dasharray: 2000; animation: pulse 4s infinite;">
      MARWAYS
    </text>
  </g>

  <!-- Dynamic Rotating Subtitles (Simulates Typing/Fading) -->
  <g style="animation: float 10s infinite 1s ease-in-out;">
    <rect x="250" y="280" width="700" height="50" fill="#0D1117" opacity="0.6" rx="10" stroke="#8B5CF6" stroke-width="1" />
    
    <!-- String 1 -->
    <text x="50%" y="312" text-anchor="middle" class="text-subtitle" style="animation: typeRotate1 15s infinite; opacity: 1;">
      <tspan fill="#A78BFA">✨ Vibe Coder · AI Alchemist · Full-Stack Builder ✨</tspan>
    </text>
    
    <!-- String 2 -->
    <text x="50%" y="312" text-anchor="middle" class="text-subtitle" style="animation: typeRotate2 15s infinite; opacity: 0;">
      <tspan fill="#F472B6">const</tspan> <tspan fill="#67E8F9">magic</tspan> = (<tspan fill="#A78BFA">idea</tspan>) =&gt; <tspan fill="#67E8F9">AI</tspan>.transform(<tspan fill="#A78BFA">idea</tspan>).deploy();
    </text>
    
    <!-- String 3 -->
    <text x="50%" y="312" text-anchor="middle" class="text-subtitle" style="animation: typeRotate3 15s infinite; opacity: 0;">
      <tspan fill="#06B6D4">🚀 AI × Creativity = Infinite Possibilities 🚀</tspan>
    </text>
  </g>
''')

# Close SVG
svg_parts.append('''
</svg>
''')

with open('assets/sota-hero.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Hero SVG generated at assets/sota-hero.svg")
