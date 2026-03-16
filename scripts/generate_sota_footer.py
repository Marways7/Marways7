import random

width = 1200
height = 250

svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&amp;family=Orbitron:wght@700;900&amp;display=swap');
      
      @keyframes neonPulse {{
        0%, 100% {{ filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.5)); }}
        50% {{ filter: drop-shadow(0 0 20px rgba(6, 182, 212, 0.8)); }}
      }}
      @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
      }}
      @keyframes slideIn {{
        0% {{ transform: translateX(-50px); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
      }}
      @keyframes codeRain {{
        0% {{ transform: translateY(-50px); opacity: 0; }}
        50% {{ opacity: 0.5; }}
        100% {{ transform: translateY({height}px); opacity: 0; }}
      }}
      
      .text-title {{
        font-family: 'Fira Code', monospace;
        font-size: 20px;
        font-weight: 600;
        fill: #A78BFA;
      }}
      .text-main {{
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        font-weight: 900;
        fill: url(#text-grad);
        letter-spacing: 2px;
        animation: neonPulse 3s infinite;
      }}
      .text-sub {{
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        fill: #C9D1D9;
      }}
      .accent {{
        fill: #06B6D4;
      }}
    </style>
    
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#67E8F9" />
      <stop offset="50%" stop-color="#A78BFA" />
      <stop offset="100%" stop-color="#F472B6" />
    </linearGradient>

    <radialGradient id="hole-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0a0614" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#1A1230" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="transparent" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="100%" height="100%" fill="#050814" />
''')

# Code Rain background
rain_chars = "10!@#$%&*+^~aBcDeFgHiJk"
for i in range(20):
    x = random.randint(50, width-50)
    delay = random.uniform(0, 10)
    dur = random.uniform(5, 12)
    col = f'<g style="animation: codeRain {dur}s infinite {delay}s linear; opacity: 0;">'
    for j in range(random.randint(4, 10)):
        y = j * 15
        char = random.choice(rain_chars)
        col += f'<text x="{x}" y="{y}" font-family="monospace" font-size="10px" fill="#8B5CF6" opacity="{1 - (j/15)}">{char}</text>'
    col += '</g>'
    svg_parts.append(col)

# Background Aura
svg_parts.append(f'''
  <circle cx="50%" cy="50%" r="300" fill="url(#hole-glow)" />
''')

# Central Monolith / Layout
svg_parts.append('''
  <g style="animation: float 6s infinite ease-in-out;">
    <rect x="200" y="30" width="800" height="190" fill="#0D1117" opacity="0.8" rx="15" stroke="#8B5CF6" stroke-width="1" />
    
    <!-- Top left accent corner -->
    <path d="M 190 45 L 210 45 L 210 25" fill="none" class="panel" stroke="#06B6D4" stroke-width="3" />
    <!-- Bottom right accent corner -->
    <path d="M 1010 205 L 990 205 L 990 225" fill="none" class="panel" stroke="#F472B6" stroke-width="3" />

    <!-- Text content inside -->
    <text x="50%" y="80" text-anchor="middle" class="text-title">
      &gt;_ MADE WITH <tspan fill="#F472B6">💜</tspan> &amp; <tspan class="accent">☕</tspan> &amp; <tspan fill="#67E8F9">AI</tspan> BY MARWAYS
    </text>
    
    <text x="50%" y="130" text-anchor="middle" class="text-main">
      THE BEST WAY TO PREDICT THE FUTURE
    </text>
    <text x="50%" y="170" text-anchor="middle" class="text-main">
      IS TO BUILD IT.
    </text>
    
    <text x="50%" y="205" text-anchor="middle" class="text-sub">
      Let's build the future together! 🚀 Star if inspired!
    </text>
  </g>
  
  <!-- Circuit lines -->
  <path d="M 0 125 L 180 125 L 200 105" fill="none" stroke="#A78BFA" stroke-width="2" stroke-opacity="0.3" />
  <path d="M 1200 125 L 1020 125 L 1000 145" fill="none" stroke="#A78BFA" stroke-width="2" stroke-opacity="0.3" />
''')

svg_parts.append('</svg>')

with open('assets/sota-footer.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Footer SVG generated at assets/sota-footer.svg")
