"""Build self-contained profile illustrations from the site's parametric forms.

No raster images, scripts, network calls or externally hosted rendering services.
"""
import math
from html import escape
from pathlib import Path
from build_shape_profile import display, text

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/shape'
TAU = math.tau
PALETTES = [('#ECEEE9','#183D35',(156,186,119)),('#281D29','#F5E7E5',(217,117,147)),
            ('#DEE7DF','#1E433D',(120,169,160)),('#F0EDDF','#4B472B',(201,182,106)),
            ('#172B36','#E4E9E7',(137,177,200)),('#E6EAC9','#37462B',(151,177,78)),
            ('#DCE6ED','#28465A',(137,180,211))]


def point(kind,k,u,v):
    b=k/23;a=k/24*TAU
    if kind==0:
        r=.24+2.35*math.sin(u*math.pi*.77); theta=a+u*1.55
        w=(.04+.57*max(0,math.sin(math.pi*u))**.8)*v
        return [math.cos(theta)*r-math.sin(theta)*w,math.sin(theta)*r+math.cos(theta)*w,
                .8*math.cos(u*math.pi*1.45)+.38*math.cos(v*math.pi*.6)*math.sin(u*math.pi)+.16*math.sin(a*3)]
    if kind==1:
        t=u*TAU;pulse=.6*math.exp(-((u-.25)/.027)**2)-.23*math.exp(-((u-.30)/.04)**2)+.18*math.exp(-((u-.66)/.09)**2)
        r=1.45+b*.7+v*.035
        return [math.cos(t)*r,math.sin(t)*r+math.sin(t*3+b*3)*.1+pulse,(b-.5)*1.35+.32*math.sin(t*2+b*4)+v*.08]
    if kind==2:
        group=k//8;f=(k%8)/7;t=u*TAU;theta=group*TAU/3
        x=(1.33+f*.27+v*.032)*math.cos(t)+.45;y=(1.33+f*.27+v*.032)*math.sin(t)
        return [x*math.cos(theta)-y*math.sin(theta),x*math.sin(theta)+y*math.cos(theta),.58*math.sin(t*2)+(f-.5)*.38+.25*group]
    if kind==3:
        theta=(b-.5)*2.45;r=.18+u*2.75
        return [math.sin(theta)*r,v*(.95+.13*math.sin(math.pi*u))+.20*math.sin(u*3+b*2),math.cos(theta)*r-1.25+.17*math.sin(u*math.pi)*math.cos(v*2)]
    if kind==4:
        t=u*TAU*1.65+a*.12;r=1.1+.75*b+v*.07
        return [math.cos(t)*r,(u-.5)*3.65+(b-.5)*.38,math.sin(t)*r]
    if kind==5:
        return [(u-.5)*4.9,(b-.5)*2.65+v*.055+.23*math.sin(u*7+b*3),.7*math.sin(u*6.5+b*3.5)+.20*math.cos(b*8)+v*.06]
    t=u*TAU;r=(.45+1.7*math.sin(u*math.pi))*(1+.10*math.sin(t*3))
    return [math.cos(a)*r+v*.07*math.sin(a),math.sin(a)*r-v*.07*math.cos(a),1.45*math.cos(u*math.pi)+.25*math.sin(t+b*3)]


def rotate(p,kind=0):
    x,y,z=p
    x,y=x*math.cos(-.27)-y*math.sin(-.27),x*math.sin(-.27)+y*math.cos(-.27)
    y,z=y*math.cos(-.08)-z*math.sin(-.08),y*math.sin(-.08)+z*math.cos(-.08)
    r=kind*.2
    return [x*math.cos(r)+z*math.sin(r),y,-x*math.sin(r)+z*math.cos(r)]


def sculpture(kind=0,detail=40):
    color=PALETTES[kind][2];faces=[]
    for k in range(24):
        for i in range(detail):
            for j in range(8):
                ps=[rotate(point(kind,k,u,v),kind) for u,v in [(i/detail,j/4-1),((i+1)/detail,j/4-1),((i+1)/detail,(j+1)/4-1),(i/detail,(j+1)/4-1)]]
                a=[ps[1][q]-ps[0][q] for q in range(3)];b=[ps[3][q]-ps[0][q] for q in range(3)]
                n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
                length=math.sqrt(sum(q*q for q in n)) or 1;n=[q/length for q in n]
                if n[2]<0:n=[-q for q in n]
                diffuse=max(0,(-.5*n[0]+n[1]+1.8*n[2])/2.12)
                spec=max(0,(-.2*n[0]+.3*n[1]+n[2])/1.063)**24
                shade=.27+.70*diffuse
                fill='#'+''.join(f'{min(255,int((c*.68+240*.32)*shade+spec*65)):02x}' for c in color)
                coords=' '.join(f'{p[0]*100*7.8/(7.8-p[2]):.1f},{-p[1]*100*7.8/(7.8-p[2]):.1f}' for p in ps)
                faces.append((sum(p[2] for p in ps),f'<polygon points="{coords}" fill="{fill}" stroke="{fill}" stroke-width=".35"/>'))
    return '<g class="form">'+''.join(f[1] for f in sorted(faces))+'</g>'


def silk(kind=0):
    """Smooth vector ribbons for the small GitHub image; no faceted raster proxy."""
    parts=[]
    for k in range(24):
        ps=[rotate(point(kind,k,i/80,v),kind) for v in (-1,1) for i in (range(81) if v==-1 else range(80,-1,-1))]
        d='M'+' L'.join(f'{p[0]*100*7.8/(7.8-p[2]):.2f},{-p[1]*100*7.8/(7.8-p[2]):.2f}' for p in ps)+'Z'
        angle=k/24*TAU
        x,y=50+50*math.cos(angle),50+50*math.sin(angle)
        colors=['#3c5542','#9aaf79','#ecf2d6','#bbcea0','#4a6249']
        if kind:
            base=PALETTES[kind][2]
            colors=['#'+''.join(f'{int(c*s+(255-c)*t):02x}' for c in base) for s,t in [(.4,0),(.9,.1),(1,.78),(1,.4),(.5,0)]]
        grad=f'<linearGradient id="silk{k}" x1="{x:.1f}%" y1="{y:.1f}%" x2="{100-x:.1f}%" y2="{100-y:.1f}%">'+''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in zip(['0','.25','.49','.62','1'],colors))+'</linearGradient>'
        lines=[]
        for v in (-.8,-.4,0,.4,.8):
            lp=[rotate(point(kind,k,i/64,v),kind) for i in range(65)]
            ld='M'+' L'.join(f'{p[0]*100*7.8/(7.8-p[2]):.1f},{-p[1]*100*7.8/(7.8-p[2]):.1f}' for p in lp)
            lines.append(f'<path d="{ld}" fill="none" stroke="#f4f9e6" stroke-width=".45" opacity=".24"/>')
        parts.append((sum(p[2] for p in ps)/len(ps),grad+f'<path d="{d}" fill="url(#silk{k})" stroke="#d4e1bc" stroke-width=".3"/>'+''.join(lines)))
    return '<g class="form">'+''.join(p[1] for p in sorted(parts))+'</g>'


def svg(w,h,title,body,kind=0,still=False):
    bg,ink,_=PALETTES[kind]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Marways 的个人介绍与开源作品。原创参数化褶皱形态，完整互动体验请打开个人主页。</desc>
<defs><radialGradient id="shadow"><stop stop-color="{ink}" stop-opacity=".15"/><stop offset="1" stop-color="{ink}" stop-opacity="0"/></radialGradient><clipPath id="bounds"><rect width="{w}" height="{h}" rx="3"/></clipPath></defs>
<style>text{{font-family:Arial,'Microsoft YaHei','PingFang SC',sans-serif}}.form{{animation:breathe 12s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}@keyframes breathe{{0%,100%{{transform:rotate(-2deg) scale(.98)}}50%{{transform:rotate(3deg) scale(1.02)}}}}@media(prefers-reduced-motion:reduce){{.form{{animation:none!important}}}}{'.form{animation:none!important}' if still else ''}</style>
<g clip-path="url(#bounds)"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</g></svg>'''


def hero(mobile=False,still=False):
    w,h=(640,920) if mobile else (1200,700);ink=PALETTES[0][1]
    if mobile:
        body=''
        body+='<ellipse cx="330" cy="495" rx="260" ry="35" fill="url(#shadow)"/>'
        body+='<g transform="translate(330 335) scale(.85)">'+silk()+'</g>'
        body+=display('Marways',29,156,134,ink,-8)
        body+=text('你好，我是 Marways。',38,590,19,ink)+text('把好奇，变成作品。',34,656,40,ink)
        body+=text('探索 AI、信号与交互的可能。',38,710,21,ink)
        body+=text('让一个“能不能”，有一个看得见的答案。',38,747,19,ink)
        body+=text('点击进入互动主页',38,840,23,ink)+text('↗',560,842,32,ink)
        body+='<path d="M38 864H602" stroke="#183d35" stroke-width="1"/>'
    else:
        body=''
        body+='<ellipse cx="835" cy="624" rx="285" ry="38" fill="url(#shadow)"/>'
        body+='<g transform="translate(846 391) scale(1.04)">'+silk()+'</g>'
        body+=display('Marways',40,250,235,ink,-14)
        body+=text('你好，我是 Marways。',48,327,17,ink)
        body+=text('把好奇，',43,393,49,ink)+text('变成作品。',43,459,49,ink)
        body+=text('探索 AI、信号与交互的可能。',48,520,17,ink)
        body+=text('让一个“能不能”，有一个看得见的答案。',48,552,17,ink)
        body+=text('点击进入互动主页',48,635,19,ink)+text('↗',336,637,26,ink)
        body+='<path d="M48 654H369" stroke="#183d35" stroke-width="1"/>'
        body+=text('Always curious. Always making.',828,664,12,ink)
    return svg(w,h,'Marways — 把好奇，变成作品。点击进入互动主页。',body,still=still)


def card(i,mobile=False):
    names=['ECG Identification','AiliaoX','DeepReadX','Desktop Operator','Signal Sprint','Campus Guide']
    subtitles=['从一次心跳，探索身份的独特。','让一句话，连接复杂的系统。','翻过一页，也跨过一个不懂。','想法的下一步，是行动。','发现流程里的摩擦，然后改进。','让有用的知识，遇到需要的人。']
    stacks=['Python / PyTorch','TypeScript / AI / MCP','Java / Android / OCR','Python / MCP / CLI','JavaScript / Workflow','TypeScript / Learning']
    kind=i+1;bg,ink,_=PALETTES[kind];w,h=(640,330) if mobile else (1200,285)
    shape=silk(kind)
    if mobile:
        body=f'<g opacity=".90" transform="translate(534 116) scale(.46)">{shape}</g>'
        body+=display(names[i],30,177,31,ink,-1)+text(subtitles[i],30,228,20,ink)+text(stacks[i],30,287,14,ink)
    else:
        body=f'<g transform="translate(962 142) scale(.59)">{shape}</g>'
        body+=display(names[i],44,102,48,ink,-2)+text(subtitles[i],45,158,25,ink)+text(stacks[i],46,233,15,ink)
    return svg(w,h,f'{names[i]} — {subtitles[i]}',body,kind)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        for still in (False,True):
            path=OUT/f'living-hero{suffix}{"-still" if still else ""}.svg'
            path.write_text(hero(mobile,still),encoding='utf-8')
        for i in range(6):(OUT/f'living-project-{i+1}{suffix}.svg').write_text(card(i,mobile),encoding='utf-8')
    fallback=svg(640,640,'Marways 的褶皱形态','<g transform="translate(320 320)">'+silk()+'</g>',still=True)
    fallback=fallback.replace('<rect width="640" height="640" fill="#ECEEE9"/>','')
    (ROOT/'site/art/living-still.svg').write_text(fallback,encoding='utf-8')
    print('Built 16 profile illustrations and the static website fallback.')


if __name__=='__main__':main()
