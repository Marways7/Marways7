import math

width = 1200
height = 600

# Base 64 representations of common logos for self-contained SVG
logos = {
    "python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
    "react": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
    "ts": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
    "js": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
    "java": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
    "nodejs": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg",
    "docker": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
    "pytorch": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg",
    "tensorflow": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg",
    "mongodb": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg"
}

svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&amp;display=swap');
      
      @keyframes spin-cw {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      @keyframes spin-ccw {{
        0% {{ transform: rotate(360deg); }}
        100% {{ transform: rotate(0deg); }}
      }}
      @keyframes counter-spin-cw {{
        0% {{ transform: rotate(360deg); }}
        100% {{ transform: rotate(0deg); }}
      }}
      @keyframes counter-spin-ccw {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      @keyframes pulse-core {{
        0%, 100% {{ filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.8)); transform: scale(1); }}
        50% {{ filter: drop-shadow(0 0 50px rgba(6, 182, 212, 1)); transform: scale(1.05); }}
      }}
      
      .orbit {{
        fill: none;
        stroke: rgba(139, 92, 246, 0.3);
        stroke-width: 1;
        stroke-dasharray: 4 8;
      }}
      
      .orbit-glow {{
        fill: none;
        stroke: rgba(6, 182, 212, 0.5);
        stroke-width: 2;
        stroke-dasharray: 100 200;
        filter: blur(2px);
      }}

      .core-text {{
        font-family: 'Orbitron', sans-serif;
        font-size: 24px;
        font-weight: 900;
        fill: #FFFFFF;
        text-anchor: middle;
        dominant-baseline: middle;
      }}
      
      .node-bg {{
        fill: #0D1117;
        stroke: #A78BFA;
        stroke-width: 2;
      }}
    </style>
    
    <radialGradient id="core-grad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </radialGradient>
    
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050814" />
      <stop offset="100%" stop-color="#0a0614" />
    </linearGradient>
  </defs>

  <!-- Deep Space Canvas -->
  <rect width="100%" height="100%" fill="url(#bg-grad)" rx="15" />
''')

cx, cy = width // 2, height // 2

orbits_data = [
    {"r_x": 180, "r_y": 70, "duration": 20, "dir": "cw", "tilt": 15, "items": ["python", "js", "ts"]},
    {"r_x": 300, "r_y": 100, "duration": 30, "dir": "ccw", "tilt": -10, "items": ["react", "nodejs", "java", "docker"]},
    {"r_x": 450, "r_y": 140, "duration": 45, "dir": "cw", "tilt": 5, "items": ["pytorch", "tensorflow", "mongodb"]}
]

for idx, orbit in enumerate(orbits_data):
    rx, ry = orbit["r_x"], orbit["r_y"]
    dur = orbit["duration"]
    direction = "spin-cw" if orbit["dir"] == "cw" else "spin-ccw"
    counter_dir = "counter-spin-cw" if orbit["dir"] == "cw" else "counter-spin-ccw"
    tilt = orbit["tilt"]
    
    # Draw Orbit Rings
    svg_parts.append(f'''
  <g style="transform-origin: {cx}px {cy}px; transform: rotate({tilt}deg);">
    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" class="orbit" />
    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" class="orbit-glow" style="animation: {direction} {dur*1.5}s infinite linear;" />
    
    <!-- Rotating Container for Items -->
    <g style="transform-origin: {cx}px {cy}px; animation: {direction} {dur}s infinite linear;">
''')
    
    # Draw Items on the orbit
    items = orbit["items"]
    n = len(items)
    for i, item in enumerate(items):
        angle = 2 * math.pi * i / n
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        
        # Each item needs its own counter-rotation to stay upright
        svg_parts.append(f'''
      <g style="transform-origin: {x}px {y}px; animation: {counter_dir} {dur}s infinite linear;">
        <!-- Counter native tilt to keep perfectly flat visually -->
        <g style="transform-origin: {x}px {y}px; transform: rotate({-tilt}deg);">
          <circle cx="{x}" cy="{y}" r="25" class="node-bg" />
          <image href="{logos[item]}" x="{x-15}" y="{y-15}" width="30" height="30" />
        </g>
      </g>
''')
        
    svg_parts.append('    </g>\n  </g>')

# Central Glowing AI Core (drawn last to be on top)
svg_parts.append(f'''
  <g style="transform-origin: {cx}px {cy}px; animation: pulse-core 4s infinite ease-in-out;">
    <circle cx="{cx}" cy="{cy}" r="50" fill="url(#core-grad)" />
    <circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="#F472B6" stroke-width="2" stroke-dasharray="10 10" style="animation: spin-cw 15s infinite linear;" />
    <circle cx="{cx}" cy="{cy}" r="75" fill="none" stroke="#06B6D4" stroke-width="1" stroke-dasharray="5 20 40 10" style="animation: spin-ccw 20s infinite linear;" />
    <text x="{cx}" y="{cy}" class="core-text">AI CORE</text>
  </g>
''')

svg_parts.append('</svg>')

with open('assets/sota-tech.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA 3D Tech Orbit SVG generated at assets/sota-tech.svg")
