width = 800
height = 400

svg_parts = []

svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&amp;display=swap');
      
      .bg {{ fill: #0D1117; }}
      .header {{ fill: #161B22; }}
      
      .text-font {{
        font-family: 'Fira Code', monospace;
        font-size: 14px;
      }}
      
      .prompt {{ fill: #7EE787; font-weight: 700; }}
      .dir {{ fill: #79C0FF; font-weight: 700; }}
      .command {{ fill: #D2A8FF; }}
      .output {{ fill: #C9D1D9; }}
      .cursor {{ fill: #C9D1D9; animation: blink 1s step-end infinite; }}
      
      .highlight {{ fill: #F78166; font-weight: 700; }}
      .accent {{ fill: #A5D6FF; }}
      .success {{ fill: #3FB950; }}
      
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
      
      /* Typing effect delays (Significantly slower for readability) */
      .typing-1 {{ opacity: 0; animation: type-in 0.1s forwards 1.0s; }}
      .typing-1-out {{ opacity: 0; animation: type-in 0.1s forwards 3.5s; }}
      
      .typing-2 {{ opacity: 0; animation: type-in 0.1s forwards 6.5s; }}
      .typing-2-out {{ opacity: 0; animation: type-in 0.1s forwards 9.0s; }}
      
      .typing-3 {{ opacity: 0; animation: type-in 0.1s forwards 12.0s; }}
      .typing-3-out {{ opacity: 0; animation: type-in 0.1s forwards 14.5s; }}
      
      .typing-4 {{ opacity: 0; animation: type-in 0.1s forwards 16.5s; }}
      .typing-4-out {{ opacity: 0; animation: type-in 0.1s forwards 18.0s; }}
      
      @keyframes type-in {{
        to {{ opacity: 1; }}
      }}
      
      /* The final blinking cursor */
      .final-cursor {{
        opacity: 0;
        animation: type-in 0.1s forwards 18.0s, blink 1s step-end infinite 18.0s;
      }}
      
      /* Hide previous cursors as we move down */
      .c1 {{ animation: cursor-hide 0.1s forwards 3.3s; }}
      .c2 {{ opacity: 0; animation: type-in 0.1s forwards 3.3s, blink 1s step-end infinite 3.3s, cursor-hide 0.1s forwards 6.3s; }}
      .c3 {{ opacity: 0; animation: type-in 0.1s forwards 6.3s, blink 1s step-end infinite 6.3s, cursor-hide 0.1s forwards 8.8s; }}
      .c4 {{ opacity: 0; animation: type-in 0.1s forwards 8.8s, blink 1s step-end infinite 8.8s, cursor-hide 0.1s forwards 11.8s; }}
      .c5 {{ opacity: 0; animation: type-in 0.1s forwards 11.8s, blink 1s step-end infinite 11.8s, cursor-hide 0.1s forwards 14.3s; }}
      .c6 {{ opacity: 0; animation: type-in 0.1s forwards 14.3s, blink 1s step-end infinite 14.3s, cursor-hide 0.1s forwards 16.3s; }}
      .c7 {{ opacity: 0; animation: type-in 0.1s forwards 16.3s, blink 1s step-end infinite 16.3s, cursor-hide 0.1s forwards 17.8s; }}
      
      @keyframes cursor-hide {{
        to {{ opacity: 0; }}
      }}
      
    </style>
  </defs>

  <!-- Terminal Window -->
  <rect width="100%" height="100%" class="bg" rx="8" />
  
  <!-- Terminal Header -->
  <rect width="100%" height="30" class="header" rx="8" />
  <rect width="100%" height="15" y="15" class="header" /> <!-- Square bottom corners -->
  
  <!-- Mac Buttons -->
  <circle cx="20" cy="15" r="6" fill="#FF5F56" />
  <circle cx="40" cy="15" r="6" fill="#FFBD2E" />
  <circle cx="60" cy="15" r="6" fill="#27C93F" />
  
  <text x="50%" y="20" class="text-font" fill="#8B949E" style="text-anchor: middle; font-size: 13px;">root@marways:~</text>

  <!-- Terminal Body Content -->
  <g class="text-font" transform="translate(20, 60)">
  
    <!-- LINE 1: Command -->
    <text x="0" y="0">
      <tspan class="prompt">root@marways</tspan>:<tspan class="dir">~/brain</tspan>$ <tspan class="command typing-1">cat identity.json</tspan>
    </text>
    <rect x="0" y="-12" width="8" height="15" fill="#C9D1D9" class="c1"/> <!-- Cursor dummy start -->
    <rect x="290" y="-12" width="8" height="15" fill="#C9D1D9" class="c2"/> <!-- Cursor after command 1 -->
    
    <!-- LINE 1: Output -->
    <g class="typing-1-out" transform="translate(0, 25)">
      <text x="0" y="0"><tspan class="accent">{{</tspan></text>
      <text x="20" y="22">"name": <tspan class="success">"Marways"</tspan>,</text>
      <text x="20" y="44">"title": <tspan class="success">"SOTA Vibe Coder &amp; AI Architect"</tspan>,</text>
      <text x="20" y="66">"superpower": <tspan class="success">"Turning Wild Ideas -> Production Software"</tspan></text>
      <text x="0" y="88"><tspan class="accent">}}</tspan></text>
    </g>

    <!-- LINE 2: Command -->
    <g class="typing-2" transform="translate(0, 140)">
      <text x="0" y="0">
        <tspan class="prompt">root@marways</tspan>:<tspan class="dir">~/brain</tspan>$ <tspan class="command">neofetch --skills</tspan>
      </text>
      <rect x="0" y="-12" width="8" height="15" fill="#C9D1D9" class="c3"/>
      <rect x="295" y="-12" width="8" height="15" fill="#C9D1D9" class="c4"/>
    </g>
    
    <!-- LINE 2: Output -->
    <g class="typing-2-out" transform="translate(0, 165)">
      <text x="0" y="0" class="highlight">OS:</text><text x="120" y="0" class="output">Ubuntu / Kali Linux (Live)</text>
      <text x="0" y="22" class="highlight">Specialty:</text><text x="120" y="22" class="output">AI Agents &amp; Deep Learning</text>
      <text x="0" y="44" class="highlight">Core Env:</text><text x="120" y="44" class="output">Python, TS, React, PyTorch</text>
      <text x="0" y="66" class="highlight">Philosophy:</text><text x="120" y="66" class="output">Open Source everything.</text>
    </g>

    <!-- LINE 3: Command -->
    <g class="typing-3" transform="translate(0, 260)">
      <text x="0" y="0">
        <tspan class="prompt">root@marways</tspan>:<tspan class="dir">~/brain</tspan>$ <tspan class="command">./execute_future.sh</tspan>
      </text>
      <rect x="0" y="-12" width="8" height="15" fill="#C9D1D9" class="c5"/>
      <rect x="300" y="-12" width="8" height="15" fill="#C9D1D9" class="c6"/>
    </g>
    
    <!-- LINE 3: Output -->
    <g class="typing-3-out" transform="translate(0, 285)">
      <text x="0" y="0" class="success">[+] Connecting to neural matrix...</text>
      <text x="0" y="22" class="success">[+] Bypassing limits... OK</text>
      <text x="0" y="44" class="success">[+] Future built successfully.</text>
    </g>
    
    <!-- LINE 4: Final Prompt -->
    <g class="typing-4" transform="translate(0, 360)">
      <text x="0" y="0">
        <tspan class="prompt">root@marways</tspan>:<tspan class="dir">~/brain</tspan>$ <tspan class="command"></tspan>
      </text>
      <rect x="0" y="-12" width="8" height="15" fill="#C9D1D9" class="c7"/>
      <rect x="235" y="-12" width="8" height="15" class="final-cursor"/>
    </g>

  </g>
</svg>
''')

with open('assets/terminal-bio.svg', 'w', encoding='utf-8') as f:
    f.write("".join(svg_parts))
print("SOTA Terminal Bio generated at assets/terminal-bio.svg")
