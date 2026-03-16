import math
import os

width = 800
height = 280
svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&amp;family=Fira+Code:wght@600&amp;display=swap');
      
      .bg {{ fill: #0D1117; }}
      
      .hex-frame {{
        fill: rgba(139, 92, 246, 0.05);
        stroke: #A78BFA;
        stroke-width: 2;
        filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.4));
      }}
      .hex-frame:hover {{
        fill: rgba(6, 182, 212, 0.1);
        stroke: #06B6D4;
        filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.8));
      }}
      
      .value {{
        font-family: 'Orbitron', sans-serif;
        font-size: 34px;
        font-weight: 900;
        fill: #67E8F9;
        text-anchor: middle;
      }}
      .label {{
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        font-weight: 600;
        fill: #8B949E;
        text-anchor: middle;
      }}
      
      @keyframes float-hex {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-6px); }}
      }}
      
      @keyframes pulse-ring {{
        0% {{ stroke-dasharray: 0 100; opacity: 0.8; }}
        100% {{ stroke-dasharray: 100 0; opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Background Canvas -->
  <rect width="100%" height="100%" class="bg" rx="15" />
''')

# Define exactly 4 hex panels
metrics = [
    {"label": "TOTAL REPOSITORIES", "value": "18", "cx": 140, "cy": 140, "delay": 0},
    {"label": "STARS EARNED", "value": "51", "cx": 310, "cy": 140, "delay": 0.4},
    {"label": "CONTRIBUTIONS/YR", "value": "850+", "cx": 480, "cy": 140, "delay": 0.8},
    {"label": "VIBE SINCE", "value": "2020", "cx": 650, "cy": 140, "delay": 1.2}
]

def draw_hexagon(cx, cy, r):
    points = []
    for i in range(6):
        # Pointy topped hex
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append(f"{cx + r * math.cos(angle_rad)},{cy + r * math.sin(angle_rad)}")
    return " ".join(points)

for m in metrics:
    cx, cy, d = m["cx"], m["cy"], m["delay"]
    hex_str = draw_hexagon(cx, cy, 75)
    outer_hex = draw_hexagon(cx, cy, 85)
    
    svg_parts.append(f'''
  <!-- Metric Box: {m["label"]} -->
  <g style="animation: float-hex 4s infinite {d}s ease-in-out; transform-origin: {cx}px {cy}px;">
    <!-- Outer scanning ring -->
    <polygon points="{outer_hex}" fill="none" class="hex-frame" style="animation: pulse-ring 3s infinite {d}s linear;" />
    <!-- Inner Core Hex -->
    <polygon points="{hex_str}" class="hex-frame" />
    
    <!-- Data -->
    <text x="{cx}" y="{cy + 10}" class="value">{m["value"]}</text>
    <text x="{cx}" y="{cy + 40}" class="label">{m["label"]}</text>
  </g>
''')

svg_parts.append('</svg>')

os.makedirs('assets', exist_ok=True)
with open('assets/sota-metrics.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Hexagonal Metrics Hologram generated at assets/sota-metrics.svg")
