import math
import urllib.request
import re
import os

width = 1200
height = 650

logos = {
    "python": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg",
    "js": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
    "ts": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg",
    "react": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg",
    "nodejs": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original.svg",
    "java": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg",
    "docker": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg",
    "pytorch": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pytorch/pytorch-original.svg",
    "tensorflow": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tensorflow/tensorflow-original.svg",
    "mongodb": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original.svg",
    "mysql": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg",
    "redis": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original.svg",
    "git": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original.svg",
    "vscode": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original.svg",
    "html": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg",
    "css": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original.svg",
    "nextjs": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nextjs/nextjs-original.svg"
}

def extract_svg_content(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            svg_data = response.read().decode('utf-8')
            
            # Very crude but effective regex to extract everything inside the <svg> tags
            # We want to keep paths, polygons, linearGradients, etc., but discard the outer <svg>
            match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_data, re.IGNORECASE | re.DOTALL)
            if match:
                inner_content = match.group(1)
                
                # Check for viewBox to properly scale the inner content
                vb_match = re.search(r'viewBox="([^"]+)"', svg_data)
                scale = 1.0
                translate = (0,0)
                if vb_match:
                    parts = [float(p) for p in vb_match.group(1).split()]
                    # Assume icons are typically 128x128 max in devicons
                    w = parts[2]
                    h = parts[3]
                    scale = 40.0 / max(w, h) # We want icons to be ~40px
                    translate = (-parts[0], -parts[1])
                else:
                    scale = 40.0 / 128.0 # fallback assumption
                
                return inner_content, scale, translate
            return None, 1.0, (0,0)
            
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None, 1.0, (0,0)

print("Fetching raw SVGs and extracting vector paths (immune to CSP)...")
raw_icons = {}
for name, url in logos.items():
    content, scale, translate = extract_svg_content(url)
    if content:
        raw_icons[name] = {"content": content, "scale": scale, "translate": translate}

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
        stroke: rgba(139, 92, 246, 0.2);
        stroke-width: 1.5;
        stroke-dasharray: 6 12;
      }}
      
      .orbit-glow {{
        fill: none;
        stroke: rgba(6, 182, 212, 0.6);
        stroke-width: 2.5;
        stroke-dasharray: 100 250;
        filter: blur(2px);
      }}

      .core-text {{
        font-family: 'Orbitron', sans-serif;
        font-size: 26px;
        font-weight: 900;
        fill: #FFFFFF;
        text-anchor: middle;
        dominant-baseline: middle;
        letter-spacing: 2px;
      }}
      
      .node-bg {{
        fill: #0D1117;
        stroke: #A78BFA;
        stroke-width: 2.5;
        filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.5));
      }}
      
      .hex-bg {{
        fill: none;
        stroke: rgba(255, 255, 255, 0.05);
        stroke-width: 1;
      }}
    </style>
    
    <radialGradient id="core-grad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </radialGradient>
    
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#050814" />
      <stop offset="50%" stop-color="#0f0c29" />
      <stop offset="100%" stop-color="#050814" />
    </linearGradient>

    <pattern id="stars" width="100" height="100" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.5" fill="#fff" opacity="0.1"/>
      <circle cx="50" cy="80" r="1" fill="#fff" opacity="0.2"/>
      <circle cx="90" cy="40" r="2" fill="#fff" opacity="0.15"/>
    </pattern>
    
  </defs>

  <!-- Deep Space Canvas -->
  <rect width="100%" height="100%" fill="url(#bg-grad)" rx="15" />
  <rect width="100%" height="100%" fill="url(#stars)" rx="15" />
''')

cx, cy = width // 2, height // 2

# Draw highly technical background hex grid
hex_size = 40
for row in range(-10, 10):
    for col in range(-15, 15):
        x = cx + col * hex_size * 1.5
        y = cy + row * hex_size * math.sqrt(3)
        if col % 2 != 0:
            y += hex_size * math.sqrt(3) / 2
        
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg
            px = x + hex_size * math.cos(angle_rad)
            py = y + hex_size * math.sin(angle_rad)
            points.append(f"{px},{py}")
        svg_parts.append(f'<polygon points="{", ".join(points)}" class="hex-bg"/>')


orbits_data = [
    {"r_x": 220, "r_y": 80, "duration": 22, "dir": "cw", "tilt": 18, "items": ["python", "js", "ts", "react", "html", "css"]},
    {"r_x": 380, "r_y": 120, "duration": 35, "dir": "ccw", "tilt": -12, "items": ["nodejs", "java", "nextjs", "docker", "mongodb", "mysql"]},
    {"r_x": 550, "r_y": 180, "duration": 50, "dir": "cw", "tilt": 8, "items": ["pytorch", "tensorflow", "redis", "git", "vscode"]}
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
        icon_data = raw_icons.get(item)
        if not icon_data: continue
        
        angle = 2 * math.pi * i / n
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        
        s = icon_data["scale"]
        tx = icon_data["translate"][0]
        ty = icon_data["translate"][1]
        
        svg_parts.append(f'''
      <g style="transform-origin: {x}px {y}px; animation: {counter_dir} {dur}s infinite linear;">
        <!-- Counter native tilt to keep perfectly flat visually -->
        <g style="transform-origin: {x}px {y}px; transform: rotate({-tilt}deg);">
          <!-- Connection lines to core (ghostly) -->
          <line x1="{x}" y1="{y}" x2="{cx - (x - cx)}" y2="{cy - (y - cy)}" stroke="rgba(139, 92, 246, 0.1)" stroke-width="1" />
          <circle cx="{x}" cy="{y}" r="28" class="node-bg" />
          
          <!-- NATIVE EMBEDDED PATHS (Immune to CSP) -->
          <g transform="translate({x-20}, {y-20}) scale({s}) translate({tx}, {ty})">
             {icon_data["content"]}
          </g>
        </g>
      </g>
''')
        
    svg_parts.append('    </g>\n  </g>')

# Central Glowing AI Core
svg_parts.append(f'''
  <g style="transform-origin: {cx}px {cy}px; animation: pulse-core 4s infinite ease-in-out;">
    <circle cx="{cx}" cy="{cy}" r="65" fill="url(#core-grad)" />
    <!-- Outer Spinners -->
    <circle cx="{cx}" cy="{cy}" r="75" fill="none" stroke="#F472B6" stroke-width="3" stroke-dasharray="15 30" style="animation: spin-cw 10s infinite linear;" />
    <circle cx="{cx}" cy="{cy}" r="90" fill="none" stroke="#06B6D4" stroke-width="2" stroke-dasharray="5 20 40 10" style="animation: spin-ccw 15s infinite linear;" />
    <!-- Geometric inner glow -->
    <polygon points="{cx},{cy-50} {cx+43},{cy-25} {cx+43},{cy+25} {cx},{cy+50} {cx-43},{cy+25} {cx-43},{cy-25}" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2" style="animation: spin-cw 20s infinite linear;" />
    
    <text x="{cx}" y="{cy}" class="core-text">AI CORE</text>
  </g>
''')

svg_parts.append('</svg>')

os.makedirs('assets', exist_ok=True)
with open('assets/sota-tech.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Native Vector Tech Orbit SVG generated at assets/sota-tech.svg")
