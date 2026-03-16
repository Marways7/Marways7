import random

width = 1200
height = 200

svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@600&amp;display=swap');
      
      .bar {{
        fill: url(#bar-grad);
        rx: 4;
      }}
      
      .vibe-text {{
        font-family: 'Fira Code', monospace;
        font-size: 16px;
        font-weight: 600;
        fill: #C9D1D9;
        letter-spacing: 4px;
        text-anchor: middle;
      }}
    </style>
    
    <linearGradient id="bar-grad" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#06B6D4" />
      <stop offset="50%" stop-color="#8B5CF6" />
      <stop offset="100%" stop-color="#F472B6" />
    </linearGradient>
  </defs>
  
  <rect width="100%" height="100%" fill="#0a0614" rx="10"/>
''')

# Generate 50 bars for the audio spectrum
num_bars = 60
bar_width = 8
spacing = 4
total_w = num_bars * (bar_width + spacing)
start_x = (width - total_w) // 2

for i in range(num_bars):
    x = start_x + i * (bar_width + spacing)
    
    # We create unique CSS keyframes for each bar so they bounce randomly
    dur = random.uniform(0.5, 1.5)
    h_min = random.randint(10, 30)
    h_max = random.randint(50, 120)
    
    # Increase height towards middle (bell curve-ish)
    dist_from_center = abs(i - num_bars/2) / (num_bars/2)
    multiplier = max(1 - dist_from_center, 0.2)
    h_max = int(h_max * 1.5 * multiplier)
    if h_max < 20: h_max = 20
    
    anim_name = f"bounce-{i}"
    
    svg_parts.append(f'''
  <style>
    @keyframes {anim_name} {{
      0%, 100% {{ height: {h_min}px; y: {height//2 - h_min//2 - 10}px; }}
      50% {{ height: {h_max}px; y: {height//2 - h_max//2 - 10}px; filter: drop-shadow(0 0 8px rgba(244,114,182,0.8)); }}
    }}
  </style>
  <rect x="{x}" y="{height//2 - h_min//2 - 10}" width="{bar_width}" height="{h_min}" class="bar" style="animation: {anim_name} {dur}s infinite ease-in-out;" />
''')

svg_parts.append(f'''
  <text x="50%" y="{height - 30}" class="vibe-text">/// VIBE_SYS.PROCESS(LIVE_DATA) ///</text>
  <circle cx="{width//2 - 160}" cy="{height - 35}" r="4" fill="#67E8F9">
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" />
  </circle>
''')

svg_parts.append('</svg>')

with open('assets/sota-vibe.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Vibe Visualizer SVG generated at assets/sota-vibe.svg")
