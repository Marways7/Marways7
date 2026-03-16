import math

width = 1200
height = 250

svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;family=Orbitron:wght@700;900&amp;display=swap');
      
      .panel {{
        fill: #0D1117;
        stroke: #A78BFA;
        stroke-width: 2;
        transition: all 0.5s ease;
      }}
      .panel:hover {{
        fill: #1A1230;
        stroke: #F472B6;
        filter: drop-shadow(0 0 15px rgba(244,114,182,0.8));
      }}
      
      @keyframes pulse-border {{
        0% {{ stroke-opacity: 0.3; }}
        50% {{ stroke-opacity: 1; }}
        100% {{ stroke-opacity: 0.3; }}
      }}
      
      @keyframes float-up {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
      }}
      
      @keyframes glow-text {{
        0%, 100% {{ filter: drop-shadow(0 0 5px rgba(103,232,249,0.5)); }}
        50% {{ filter: drop-shadow(0 0 15px rgba(103,232,249,0.9)); }}
      }}
      
      @keyframes radar-spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}

      .title-text {{
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        fill: #A78BFA;
        letter-spacing: 2px;
        text-transform: uppercase;
      }}
      
      .value-text {{
        font-family: 'Orbitron', sans-serif;
        font-size: 48px;
        font-weight: 900;
        fill: #67E8F9;
        animation: glow-text 3s infinite;
      }}
      
      .sub-text {{
        font-family: 'Fira Code', monospace;
        font-size: 12px;
        fill: #8B5CF6;
        opacity: 0.8;
      }}
    </style>
    
    <linearGradient id="panel-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0.05"/>
    </linearGradient>

    <radialGradient id="ring-grad" cx="50%" cy="50%" r="50%">
      <stop offset="90%" stop-color="transparent" />
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.5" />
    </radialGradient>
  </defs>

  <!-- Background grid for tech feel -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#A78BFA" stroke-width="0.5" stroke-opacity="0.1"/>
  </pattern>
  <rect width="100%" height="100%" fill="url(#grid)" />
''')

# Radar / Target circles behind panels
for i in range(4):
    cx = 150 + i * 300
    cy = 125
    svg_parts.append(f'''
  <g style="transform-origin: {cx}px {cy}px; animation: radar-spin {10 + i*2}s infinite linear reverse;">
    <circle cx="{cx}" cy="{cy}" r="90" fill="url(#ring-grad)" stroke="#06B6D4" stroke-width="1" stroke-dasharray="2 10 20 5" stroke-opacity="0.4" />
    <circle cx="{cx}" cy="{cy}" r="100" fill="none" stroke="#F472B6" stroke-width="0.5" stroke-dasharray="5 50" stroke-opacity="0.3" />
  </g>
''')

# 4 Panels
panels = [
    {"title": "PROJECTS", "value": "20+", "sub": "Open Source Repos", "color": "#F472B6"},
    {"title": "AI FOCUS", "value": "65%", "sub": "Dev Time on AI", "color": "#06B6D4"},
    {"title": "COMMITS", "value": "500+", "sub": "Total Contributions", "color": "#818CF8"},
    {"title": "VIBE SINCE", "value": "2023", "sub": "Coding with AI", "color": "#F472B6"}
]

for i, p in enumerate(panels):
    x_center = 150 + i * 300
    y_center = 125
    delay = i * 0.2
    
    # Hexagon path
    r = 100
    points = []
    for j in range(6):
        angle = math.radians(60 * j - 30)
        px = x_center + r * math.cos(angle)
        py = y_center + r * math.sin(angle)
        points.append(f"{px},{py}")
    poly_pts = " ".join(points)
    
    # Square with cut corners as alternative tech shape
    w, h = 220, 140
    x, y = x_center - w//2, y_center - h//2
    # path = M x+15,y L x+w-15,y L x+w,y+15 L x+w,y+h-15 L x+w-15,y+h L x+15,y+h L x,y+h-15 L x,y+15 Z
    path = f"M {x+20},{y} L {x+w-20},{y} L {x+w},{y+20} L {x+w},{y+h-20} L {x+w-20},{y+h} L {x+20},{y+h} L {x},{y+h-20} L {x},{y+20} Z"
    
    svg_parts.append(f'''
  <g style="animation: float-up 4s infinite {delay}s ease-in-out;">
    <path d="{path}" fill="url(#panel-grad)" class="panel" style="animation: pulse-border 3s infinite {delay}s;"/>
    
    <!-- Top left corner detail -->
    <path d="M {x},{y+30} L {x},{y+20} L {x+20},{y}" fill="none" class="panel" stroke-width="3" style="stroke: {p['color']};" />
    <!-- Bottom right corner detail -->
    <path d="M {x+w},{y+h-30} L {x+w},{y+h-20} L {x+w-20},{y+h}" fill="none" class="panel" stroke-width="3" style="stroke: {p['color']};" />

    <text x="{x_center}" y="{y_center - 30}" text-anchor="middle" class="title-text">{p['title']}</text>
    <text x="{x_center}" y="{y_center + 15}" text-anchor="middle" class="value-text" style="fill: {p['color']};">{p['value']}</text>
    <text x="{x_center}" y="{y_center + 45}" text-anchor="middle" class="sub-text">{p['sub']}</text>
  </g>
''')

svg_parts.append('</svg>')

with open('assets/sota-metrics.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Metrics SVG generated at assets/sota-metrics.svg")
