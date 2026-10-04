"""Build project-specific illustrations and a progressively enhanced portfolio."""
from pathlib import Path
from html import escape
import math
from build_shape_profile import display, text

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/play'
OUT.mkdir(parents=True, exist_ok=True)
INK, BLUE = '#20234B', '#3548F5'
PROJECTS = [
    dict(id='ecg', name='ECG Identification', short='心电识别', color='#DDE4FF', accent='#3548F5', symbol='∿', title='心跳里，也有独特的你。', desc='从心电信号中寻找身份特征，结合信号处理与轻量 CNN，探索 ECG 生物特征身份识别。', stack='Python / PyTorch', flow=['心电信号', '特征提取', '身份识别'], repo='ECG_IdentificationX', demo='换一段信号', caption='换一段示意波形，看看信号中的不同形状。'),
    dict(id='ailiao', name='AiliaoX', short='对话与系统', color='#E9DFF9', accent='#7043B7', symbol='✳', title='从一句话，到一次连接。', desc='用 AI 对话和 MCP 工具，探索医院信息交互。把自然语言作为入口，连接信息与操作。', stack='TypeScript / AI / MCP', flow=['表达意图', '连接工具', '信息交互'], repo='AiliaoX', demo='连接工具', caption='把一句话，连接到工具与信息的交汇处。'),
    dict(id='read', name='DeepReadX', short='理解一页书', color='#FFE7D6', accent='#A5421F', symbol='⌑', title='读过一页，也读懂一点。', desc='一个 Android AI 辅助阅读项目。把 PDF、OCR 与可自定义风格的解释放在一起，为阅读多开一个理解的入口。', stack='Java / Android / PDF / OCR', flow=['打开 PDF', '提取文字', '换种解释'], repo='DeepReadX', demo='标记这一页', caption='标记一个重点，给理解留下一条新的线索。'),
    dict(id='desktop', name='Desktop Operator', short='让想法行动', color='#D7EFE7', accent='#196652', symbol='↖', title='让对话，走到桌面上。', desc='面向 AI 的桌面操作工具，提供 MCP 与 CLI 两种使用方式，探索从表达意图到操作界面的连接。', stack='Python / Desktop / MCP / CLI', flow=['理解任务', '操作界面', '观察结果'], repo='cua_desktop_operator_skill', demo='播放操作演示', caption='任务、操作、观察：走过一个行动的小循环。'),
    dict(id='sprint', name='Signal Sprint', short='找到好节奏', color='#FFE0DE', accent='#AE3346', symbol='▷', title='让每一次开始，更从容。', desc='围绕直播准备流程的小工具。结合实测与本地回放，改进扫码准备和启动节奏。', stack='JavaScript / Workflow', flow=['准备流程', '实测回放', '调整节奏'], repo='signal-sprint', demo='回放一轮', caption='沿着时间线，重新观察一次开始的节奏。'),
    dict(id='campus', name='Campus Guide', short='连接好知识', color='#E8EDCA', accent='#56691A', symbol='⌘', title='好资源，值得被更多人找到。', desc='面向大学生的学习资源网站。连接资源发现、管理与分享，让一个人的探索成为另一个人的起点。', stack='TypeScript / Web', flow=['发现资源', '整理收藏', '分享知识'], repo='college_student_self-rescue_guide_website', demo='连接知识', caption='让发现、整理、收藏与分享成为一张网。'),
]

STYLE = '''
text{font-family:Arial,"Microsoft YaHei","PingFang SC",sans-serif}
.drift{animation:drift 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.trace{stroke-dasharray:80 1100;animation:trace 6s linear infinite}
.turn{animation:turn 25s linear infinite;transform-box:fill-box;transform-origin:center}
.blink{animation:blink 4s ease-in-out infinite}
@keyframes drift{50%{transform:translateY(-8px)}}
@keyframes trace{to{stroke-dashoffset:-1180}}
@keyframes turn{to{transform:rotate(360deg)}}
@keyframes blink{50%{opacity:.45}}
@media(prefers-reduced-motion:reduce){.drift,.trace,.turn,.blink{animation:none!important}}
'''

def rect(x,y,w,h,fill,rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'

def line(d,color=INK,width=3,extra=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def circle(x,y,r,color,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'

def star(x,y,r,color):
    return '<g class="turn">'+''.join(rect(x-r,y-7,r*2,14,color,7,f'transform="rotate({a} {x} {y})"') for a in [0,60,120])+'</g>'

def svg(w,h,title,body,static=False):
    stop='*{animation:none!important}' if static else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>{STYLE}{stop}</style>{body}</svg>'

def illustration(p):
    k,c=p['id'],p['accent']
    s='<ellipse cx="324" cy="403" rx="215" ry="23" fill="'+c+'" opacity=".09"/>'
    if k=='ecg':
        s+=rect(67,96,495,280,'#B5BFF8',27)+rect(67,78,495,280,'#FFFFFF',27)
        s+=circle(91,101,5,c)+text('Signal / Identity',110,107,16,c)
        s+=rect(95,134,439,164,'#ECF0FF',12)
        for x in range(110,534,28):s+=line(f'M{x} 135V298',c,1,'opacity=".1"')
        for y in range(146,297,28):s+=line(f'M96 {y}H534',c,1,'opacity=".1"')
        wave='M105 224H148L163 211L176 226H204L217 171L233 272L250 149L267 222H306L320 210L335 224H372L385 182L400 259L419 163L434 224H522'
        s+=line(wave,c,4,'class="signal-shape"')+line(wave,'#FF9869',5,'class="trace"')
        s+=text('波形 → 特征 → 身份',108,331,19,INK)
        s+='<g class="drift">'+circle(489,338,51,'#FF9869')
        for r in [14,23,32]:s+=f'<path d="M{489-r} 347C{489-r-9} {307-r/3} {489+r+9} {307-r/3} {489+r} 347" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        s+=line('M489 326V360',INK,3)+'</g>'
        s+=star(72,344,24,c)
    elif k=='ailiao':
        s+=line('M318 149V214M318 214H142V281M318 214V294M318 214H506V281',c,4,'opacity=".45" class="connection"')
        s+='<g class="drift">'+rect(163,61,320,103,'#BA9BDD',23)+rect(163,48,320,103,'#FFFFFF',23)
        s+=text('一个想法，连接更多可能',185,107,21,INK)+f'<path d="M211 149V179L246 149" fill="#FFFFFF"/></g>'
        for x,word,sym in [(142,'对话','…'),(318,'工具','✳'),(506,'信息','≡')]:
            s+=rect(x-65,286,130,103,'#C8AEDF',24)+rect(x-65,274,130,103,'#FFFFFF',24)
            s+=circle(x,306,18,c)+text(sym,x,313,22,'#FFFFFF','text-anchor="middle"')+text(word,x,356,19,INK,'text-anchor="middle"')
            s+=circle(x,230,6,'#FF9869','class="blink"')
        s+=star(536,112,32,'#FF9869')
    elif k=='read':
        s+='<g transform="rotate(-9 291 224)">'+rect(152,66,265,316,'#D39875',14)+rect(144,47,265,316,'#FFFFFF',14)
        s+=display('Read.',173,110,40,INK)
        for y,w in [(142,178),(169,201),(196,173),(250,198),(278,175),(306,150)]:s+=rect(174,y,w,8,'#D7D5DE',4)
        s+=rect(169,213,211,22,'#FFBE77',3,'class="page-highlight"')+text('从读过，到读懂。',178,231,18,INK)
        s+='</g><g class="drift">'+rect(349,236,202,118,'#E6A47A',20)+rect(349,221,202,118,'#3548F5',20)
        s+=text('换个角度',373,261,24,'#FFFFFF','class="reading-line-one"')+text('理解这一页。',373,297,24,'#FFFFFF','class="reading-line-two"')+'</g>'
        s+=f'<path d="M415 48L445 52L438 100L421 84L405 96Z" fill="#FF9869"/>'+star(98,318,27,c)
    elif k=='desktop':
        s+=rect(105,88,428,273,'#91C6B5',22)+rect(105,70,428,273,'#FFFFFF',22)
        s+=rect(105,70,428,42,c,20)+rect(105,91,428,22,c)
        for x in [126,143,160]:s+=circle(x,90,4,'#D7EFE7')
        for y,txt in [(149,'理解任务'),(208,'操作界面'),(267,'观察结果')]:
            s+=rect(129,y-13,350,45,'#E8F5EE',9)+rect(145,y,15,15,c,4)+text(txt,177,y+14,19,INK)
            s+=line(f'M149 {y+7}l3 4 6-8','#FFFFFF',2,'class="check-mark"')
        s+='<g class="drift desktop-cursor">'+f'<path d="M389 219L393 345L429 319L451 365L481 350L458 306L501 298Z" fill="#FF9869" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>'
        s+=rect(186,363,266,19,c,9)+rect(280,344,65,28,c)+star(63,129,22,c)
    elif k=='sprint':
        s+=circle(320,218,157,'#E7A3A7')+circle(320,205,157,'#FFFFFF')
        s+=f'<circle cx="320" cy="205" r="126" fill="none" stroke="{c}" stroke-width="6" stroke-dasharray="2 21"/>'
        s+='<g class="turn">'+line('M320 205L319 97',c,6)+circle(320,205,11,c)+'</g>'
        s+=rect(136,239,360,121,'#3548F5',20)
        for i in range(25):
            h=20+45*abs(math.sin(i*1.14))
            s+=rect(157+i*13,290-h/2,6,round(h,1),'#FFFFFF' if i>8 else '#FF9869',3)
        s+=text('准备 · 回放 · 调整',214,346,16,'#FFFFFF')+star(515,106,33,'#FF9869')
        s+=line('M91 205L116 219L91 233Z',c,4)
    else:
        s+=line('M317 213L154 113M317 213L491 133M317 213L129 308M317 213L496 328',c,4,'opacity=".45" class="connection"')
        for x,y,word,col in [(154,113,'发现','#FFFFFF'),(491,133,'整理','#FFFFFF'),(129,308,'收藏','#FFFFFF'),(496,328,'分享','#FF9869')]:
            s+=circle(x,y+8,46,'#B6C48B')+circle(x,y,46,col)+text(word,x,y+7,20,INK,'text-anchor="middle"')
        s+='<g class="drift">'+rect(254,141,144,171,'#3548F5',18)+rect(239,128,144,171,'#FFFFFF',18)+rect(239,128,23,171,'#3548F5',10)
        s+=display('Keep',281,185,25,INK)+display('curious.',281,216,22,INK)
        for y in [241,255,269]:s+=rect(281,y,73,5,'#D9DBE9',2)
        s+='</g>'+star(355,71,24,c)
    return s

def card(p,wide=False,static=False):
    if wide:
        body=rect(0,0,1200,425,p['color'],25)+f'<g transform="translate(20,-9) scale(.94)">{illustration(p)}</g>'
        body+=display(p['name'],630,108,35,INK)+text(p['title'],631,162,25,INK)
        body+=text(p['stack'],631,212,18,p['accent'])
        for i,word in enumerate(p['flow']):body+=rect(632+i*163,264,151,48,'#FFFFFF',24)+text(word,707+i*163,294,18,INK,'text-anchor="middle"')
        body+=text('打开项目  →',634,373,19,p['accent'])
        return svg(1200,425,p['name']+' — '+p['title'],body,static)
    body=rect(0,0,640,612,p['color'],25)+illustration(p)
    body+=display(p['name'],40,471,33,INK)+text(p['title'],40,517,23,INK)
    body+=text(p['stack'],40,566,18,p['accent'])+text('→',592,569,28,p['accent'],'text-anchor="end"')
    return svg(640,612,p['name']+' — '+p['title'],body,static)

def ribbon(static=False):
    body=rect(0,0,1200,104,BLUE,19)
    body+=display('Curiosity',32,66,32,'#FFFFFF')+star(239,52,18,'#FF9869')
    body+=display('Code',292,66,32,'#FFFFFF')+star(441,52,18,'#BAA8F5')
    body+=display('Make it real.',489,66,32,'#FFFFFF')
    body+=line('M805 54H860L878 36L895 71L917 19L940 83L962 54H1170','#A9E5D2',3)
    body+=line('M805 54H860L878 36L895 71L917 19L940 83L962 54H1170','#FFFFFF',4,'class="trace"')
    return svg(1200,104,'好奇心、代码、把想法做出来。',body,static)

def toolkit(mobile=False):
    w,h=(640,720) if mobile else (1200,344)
    b=rect(0,0,w,h,'#F1EEFA',24)+display('My making kit',36,64,32,INK)
    entries=[('Signal & intelligence','Python · PyTorch','信号处理 / 模型实验','#DDE4FF'),('Interfaces & experiences','TypeScript · JavaScript','Web / 交互产品','#D7EFE7'),('Reading & action','Java · Android · MCP','AI 阅读 / 桌面工具','#FFE7D6')]
    for i,(a,t,d,col) in enumerate(entries):
        x,y,ww=(28,100+i*194,584) if mobile else (28+i*388,103,368)
        b+=rect(x,y,ww,174,col,18)+circle(x+34,y+33,9,BLUE)
        b+=display(a,x+24,y+75,20,INK)+text(t,x+24,y+112,20,INK)+text(d,x+24,y+146,18,INK)
    return svg(w,h,'我的工具与探索方向',b,True)

def main():
    for p in PROJECTS:
        for still in (False,True):
            suffix='-still' if still else ''
            (OUT/f'{p["id"]}{suffix}.svg').write_text(card(p,static=still),encoding='utf-8')
            if p['id'] in ('ecg','campus'):
                (OUT/f'{p["id"]}-wide{suffix}.svg').write_text(card(p,wide=True,static=still),encoding='utf-8')
    for still in (False,True):(OUT/f'ribbon{"-still" if still else ""}.svg').write_text(ribbon(still),encoding='utf-8')
    for mobile in (False,True):(OUT/f'toolkit{"-mobile" if mobile else ""}.svg').write_text(toolkit(mobile),encoding='utf-8')
    tabs=[];panels=[];directory=[]
    for i,p in enumerate(PROJECTS):
        tabs.append(f'<button id="tab-{p["id"]}" type="button" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="panel-{p["id"]}" tabindex="{0 if i==0 else -1}" data-project="{p["id"]}"><span aria-hidden="true">{p["symbol"]}</span>{p["short"]}</button>')
        illustration_svg=svg(640,460,p['name']+' 项目图解',illustration(p))
        secondary='<a class="secondary-link" href="https://github.com/Marways7/cua_desktop_operator_cli_skill" target="_blank" rel="noopener noreferrer">CLI 版本</a>' if p['id']=='desktop' else ''
        panels.append(f'''<article id="panel-{p['id']}" class="project-panel" role="tabpanel" aria-labelledby="tab-{p['id']}" tabindex="0" style="--scene:{p['color']};--accent:{p['accent']}" {'hidden' if i else ''}>
          <div class="project-visual"><div class="visual-art">{illustration_svg}</div><div class="demo-controls"><button class="demo-button" type="button" data-demo="{p['id']}">{p['demo']} <span aria-hidden="true">↻</span></button><span>交互图解</span></div></div>
          <div class="project-copy"><p class="project-name">{p['name']}</p><h3>{p['title']}</h3><p class="project-desc">{p['desc']}</p><ol class="project-flow">{''.join('<li>'+v+'</li>' for v in p['flow'])}</ol><p class="project-stack">{p['stack']}</p><div class="project-links"><a class="solid-link" href="https://github.com/Marways7/{p['repo']}" target="_blank" rel="noopener noreferrer">探索项目 <span aria-hidden="true">↗</span></a>{secondary}</div><p class="demo-caption">{p['caption']}</p></div></article>''')
        directory.append(f'<a class="directory-item" href="https://github.com/Marways7/{p["repo"]}" target="_blank" rel="noopener noreferrer"><span class="directory-icon" style="background:{p["color"]};color:{p["accent"]}" aria-hidden="true">{p["symbol"]}</span><span><strong>{p["name"]}</strong><small>{p["short"]} / {p["stack"]}</small></span><span class="directory-arrow" aria-hidden="true">↗</span></a>')
    template=(ROOT/'scripts/templates/playground.html').read_text(encoding='utf-8')
    for name,value in [('TABS',''.join(tabs)),('PANELS','\n'.join(panels)),('DIRECTORY','\n'.join(directory))]:template=template.replace('{{'+name+'}}',value)
    (ROOT/'site/index.html').write_text(template,encoding='utf-8')
    print('Built 20 playground SVGs and six project scenes.')

if __name__=='__main__':main()
