import urllib.request
import json
import os

width = 1200
height = 600

# Target Repositories
repos = [
    {"name": "Marways7/ECG_IdentificationX", "desc": "Deep Learning ST-Segment Classification\\nSystem achieving SOTA in biomedical signals."},
    {"name": "Marways7/AiliaoX", "desc": "Intelligent Medical Healthcare System.\\nBridging AI and Real-world Medicine."},
    {"name": "Marways7/DeepReadX", "desc": "Autonomous Research Agent.\\nReads, digests, and outputs deep insights."},
    {"name": "Marways7/cua_desktop_operator_skill", "desc": "Computer Use Automation.\\nAI operating complete desktop via MCP."},
]

projects_data = []

print("Fetching real-time data from GitHub API...")
for repo_info in repos:
    repo_name = repo_info["name"]
    url = f"https://api.github.com/repos/{repo_name}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            lang = data.get("language", "Unknown")
            stars = str(data.get("stargazers_count", 0))
            
            # Simple color mapping for languages
            color = "#A78BFA"
            if lang == "Python": color = "#3572A5"
            elif lang == "TypeScript": color = "#3178C6"
            elif lang == "MATLAB": color = "#E16737"
            elif lang == "Jupyter Notebook": color = "#DA5B0B"
            
            projects_data.append({
                "name": repo_name.split("/")[-1],
                "desc": repo_info["desc"],
                "lang": lang,
                "color": color,
                "stars": stars
            })
    except Exception as e:
        print(f"Failed to fetch {repo_name}: {e}")
        # Fallback data if API fails (e.g. rate limit)
        projects_data.append({
            "name": repo_name.split("/")[-1],
            "desc": repo_info["desc"],
            "lang": "Unknown",
            "color": "#A78BFA",
            "stars": "—"
        })

svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;family=Orbitron:wght@700;900&amp;display=swap');
      
      @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-8px); }}
      }}
      @keyframes scanline {{
        0% {{ transform: translateY(-50px); }}
        100% {{ transform: translateY(200px); }}
      }}
      @keyframes neonPulse {{
        0%, 100% {{ filter: drop-shadow(0 0 5px rgba(103,232,249,0.5)); }}
        50% {{ filter: drop-shadow(0 0 15px rgba(103,232,249,0.9)); }}
      }}
      @keyframes blink {{
        0%, 96%, 100% {{ opacity: 1; }}
        98% {{ opacity: 0; }}
      }}

      .bg {{ fill: #050814; }}
      
      .hud-frame {{
        fill: #0D1117;
        stroke: #A78BFA;
        stroke-width: 1.5;
        filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.2));
      }}
      
      .hud-glow {{
        fill: none;
        stroke: #06B6D4;
        stroke-width: 2;
        filter: drop-shadow(0 0 8px rgba(6,182,212,0.8));
      }}

      .title-font {{
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        font-weight: 700;
        fill: #67E8F9;
      }}
      .desc-font {{
        font-family: 'Fira Code', monospace;
        font-size: 13px;
        fill: #C9D1D9;
      }}
      .lang-font {{
        font-family: 'Fira Code', monospace;
        font-size: 13px;
        font-weight: 600;
      }}
      
      .scan-group {{
        clip-path: url(#pad-clip);
      }}
    </style>
    
    <clipPath id="pad-clip">
      <rect width="360" height="220" rx="10" />
    </clipPath>
    
    <linearGradient id="scan-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0" />
      <stop offset="50%" stop-color="#06B6D4" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0" />
    </linearGradient>
  </defs>

  <!-- Deep space background -->
  <rect width="100%" height="100%" class="bg" rx="15" />
''')

# Grid configuration
cols = 2
pad_w = 400
pad_h = 240
start_x = (width - (cols * pad_w + (cols-1)*50)) // 2 + 20
start_y = 50

# Draw Data Pads
for i, p in enumerate(projects_data):
    row = i // cols
    col = i % cols
    x = start_x + col * (pad_w + 50)
    y = start_y + row * (pad_h + 30)
    delay = i * 0.5
    
    # Process description lines
    desc_lines = p['desc'].split('\\n')
    
    svg_parts.append(f'''
  <!-- Data Pad: {p['name']} -->
  <g transform="translate({x}, {y})" style="animation: float 6s infinite {delay}s ease-in-out;">
    <g class="scan-group">
      <rect width="{pad_w}" height="{pad_h}" rx="10" class="hud-frame" />
      <!-- Scanning Line inside Pad -->
      <rect width="100%" height="50" fill="url(#scan-grad)" style="animation: scanline 4s infinite linear;" />
    </g>
    
    <!-- Cybernetic Hud Corner Accents -->
    <path d="M 0 30 L 0 0 L 30 0" class="hud-glow" />
    <path d="M {pad_w} {pad_h-30} L {pad_w} {pad_h} L {pad_w-30} {pad_h}" class="hud-glow" />
    
    <!-- Decorative side ticks -->
    <rect x="{pad_w - 5}" y="40" width="10" height="2" fill="#8B5CF6" />
    <rect x="{pad_w - 5}" y="50" width="10" height="2" fill="#8B5CF6" />
    <rect x="{pad_w - 5}" y="60" width="10" height="2" fill="#8B5CF6" />
    
    <!-- Repo Icon -->
    <svg x="25" y="30" viewBox="0 0 16 16" width="20" height="20">
      <path fill="#8B5CF6" fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"></path>
    </svg>
    
    <!-- Title -->
    <text x="55" y="47" class="title-font" style="animation: neonPulse 3s infinite {delay}s;">{p['name']}</text>
    
    <!-- Description -->
    <text x="30" y="90" class="desc-font">{desc_lines[0]}</text>
    <text x="30" y="115" class="desc-font">{len(desc_lines) > 1 and desc_lines[1] or ""}</text>
    
    <!-- Status / Metrics Footer -->
    <g transform="translate(0, {pad_h - 40})">
        <!-- Language Circle -->
        <circle cx="35" cy="0" r="6" fill="{p['color']}" style="animation: blink 4s infinite;" />
        <text x="50" y="5" class="lang-font" fill="{p['color']}">{p['lang']}</text>
        
        <!-- Star Icon -->
        <svg x="250" y="-12" viewBox="0 0 16 16" width="16" height="16">
          <path fill="#C9D1D9" fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"></path>
        </svg>
        <text x="275" y="2" class="lang-font" fill="#C9D1D9">{p['stars']}</text>
    </g>
  </g>
''')

svg_parts.append('</svg>')

os.makedirs('assets', exist_ok=True)
with open('assets/sota-projects.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Live Cybernetic Projects SVG generated at assets/sota-projects.svg")
