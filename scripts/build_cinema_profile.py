"""Cinematic README assets; interactive experience lives in site/."""
import math
from pathlib import Path
from build_shape_profile import display, text, path, motif, PROJECTS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/shape'
BG='#070B18'
FG='#F5F6FF'


def shell(w,h,title,body,styles='',static=False):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{title}</title><defs>
<linearGradient id="metal" x1="0" y1="0" x2=".75" y2="1"><stop stop-color="#9FF4E3"/><stop offset=".27" stop-color="#738AFF"/><stop offset=".52" stop-color="#F2CAFF"/><stop offset=".74" stop-color="#B2A1ED"/><stop offset="1" stop-color="#FFBD94"/></linearGradient>
<linearGradient id="type" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#6C7098" stop-opacity=".24"/></linearGradient>
<radialGradient id="light"><stop stop-color="#5260AF" stop-opacity=".24"/><stop offset="1" stop-color="#070B18" stop-opacity="0"/></radialGradient>
<clipPath id="clip"><rect width="{w}" height="{h}" rx="22"/></clipPath>
</defs><style>text{{font-family:Arial,'Microsoft YaHei','PingFang SC',sans-serif}}{styles}
@media(prefers-reduced-motion:reduce){{.motion{{animation:none!important}}}}
{'.motion{animation:none!important}' if static else ''}</style><g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="{BG}"/>{body}</g></svg>'''


def tube(t,theta,mode):
    if mode==0:
        # Rounded seven, with a horizontal upper stroke and sweeping diagonal.
        if t<.38:
            u=t/.38;x=-1+u*1.9;y=1.1+.08*math.sin(u*math.pi)
            tx,ty=1.9,.08*math.pi*math.cos(u*math.pi)
        else:
            u=(t-.38)/.62;x=.9-1.5*u+.03*math.sin(u*math.pi);y=1.1-2.5*u
            tx,ty=-1.5+.03*math.pi*math.cos(u*math.pi),-2.5
        ll=math.hypot(tx,ty);nx,ny=-ty/ll,tx/ll
        r=.24;return x+nx*r*math.cos(theta),y+ny*r*math.cos(theta),r*math.sin(theta)
    a=t*math.tau
    r=.95+.31*math.cos(3*a)
    x=r*math.cos(2*a);y=r*math.sin(2*a);z=.42*math.sin(3*a)
    return x+.17*math.cos(theta)*math.cos(2*a),y+.17*math.cos(theta)*math.sin(2*a),z+.17*math.sin(theta)


def sculpture(mobile=False):
    cx,cy,s=(333,446,180) if mobile else (842,377,200)
    strings=[];rules=[]
    for j in range(64):
        theta=j/64*math.tau
        ds=[]
        for mode in (0,1):
            points=[]
            for i in range(89):
                x,y,z=tube(i/88,theta,mode)
                # Perspective rotation turns a line drawing into a volume.
                xx=x*.95+z*.31;zz=-x*.31+z*.95;yy=y*.985-zz*.174;zz=y*.174+zz*.985
                perspective=4.8/(4.8-zz)
                points.append((cx+xx*s*perspective,cy-yy*s*perspective))
            ds.append('M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in points))
        # Long hold at either end, smooth continuous transformation between forms.
        rules.append(f'@keyframes strand{j}{{0%,18%,100%{{d:path("{ds[0]}")}}42%,65%{{d:path("{ds[1]}")}}}}')
        strings.append(path(ds[0],'url(#metal)',1.7,f'class="motion" opacity="{.34+.6*(math.sin(theta)+1)/2:.2f}" style="animation:strand{j} 15s cubic-bezier(.65,0,.35,1) infinite"'))
    return ''.join(strings),''.join(rules)


def hero(mobile=False,static=False):
    w,h=(640,990) if mobile else (1200,770)
    art,css=sculpture(mobile)
    body=f'<ellipse cx="{w*.64}" cy="{h*.48}" rx="480" ry="380" fill="url(#light)"/>'
    body+=display('Marways',26 if mobile else 32,171 if mobile else 210,112 if mobile else 209,'url(#type)',-5)
    body+=art
    if mobile:
        body+=display('Curiosity,',36,805,66)
        body+=display('in motion.',36,880,66)
        body+=text('让好奇心，发生一点什么。',40,932,28,'#D2D5ED')
        body+=text('点击封面，进入交互展厅 ↗',40,968,20,'#9FF4E3')
    else:
        body+=text('你好，我是 Marways。',55,313,21,'#A1A8C4')
        body+=display('Curiosity,',50,407,76)
        body+=display('in motion.',50,490,76)
        body+=text('让好奇心，发生一点什么。',55,546,26,'#D2D5ED')
        body+='<rect x="52" y="592" width="309" height="61" rx="30" fill="#F5F6FF"/>'
        body+=text('进入交互展厅',81,631,24,BG)
        body+=text('↗',310,633,28,BG)
        body+=path('M55 705 H1145','#30354C',1)
        body+=text('AI tools / Signal intelligence / Creative code',55,743,18,'#A1A8C4')
        body+=text('拖动 · 变形 · 探索作品',917,743,18,'#A1A8C4')
    return shell(w,h,'Marways — Curiosity, in motion. 点击进入交互展厅',body,'' if static else css,static)


def card(index,mobile=False,static=False):
    name,repo,tagline,cn,stack,color,kind=PROJECTS[index]
    questions=['心跳能成为身份吗？','对话能成为界面吗？','难懂的一页能变清晰吗？','AI 能真正动手吗？','直播能再快一点吗？','知识能找到需要它的人吗？']
    if mobile:
        body='<ellipse cx="470" cy="105" rx="250" ry="155" fill="url(#light)"/>'
        body+=text(questions[index],32,52,27,'#A8AEC8')
        body+=f'<g transform="translate(505,62) scale(.55)">{motif(kind,color)}</g>'
        body+=display(name,30,137,39 if index in (0,3) else 46)
        body+=text(cn,33,184,27,'#BFC4DD')
        body+=text('打开项目  ↗',33,237,24,'#9FF4E3')
        return shell(640,276,name+' — '+cn+'，点击打开项目',body,static=static)
    body=f'<ellipse cx="965" cy="142" rx="280" ry="185" fill="url(#light)"/>'
    body+=text(questions[index],45,56,23,'#A8AEC8')
    body+=display(name,42,118,43)
    body+=text(cn+'  /  '+stack,46,163,20,'#BFC4DD')
    body+=f'<g transform="translate(832,78) scale(1.35)"><g class="motion" style="animation:breathe 6s ease-in-out infinite;animation-delay:-{index}s">{motif(kind,color)}</g></g>'
    body+=text('打开项目  ↗',46,211,18,'#9FF4E3')
    body+=path('M690 38 V211','#2A304A',1)
    return shell(1200,245,name+' — '+cn+'，点击打开项目',body,'@keyframes breathe{0%,100%{transform:translateY(4px)}50%{transform:translateY(-9px)}}',static)


def main():
    for mobile in (False,True):
        for static in (False,True):
            suffix=('-mobile' if mobile else '')+('-still' if static else '')
            (OUT/f'cinema-hero{suffix}.svg').write_text(hero(mobile,static),encoding='utf-8')
    for i in range(6):
        (OUT/f'project-{i+1}.svg').write_text(card(i),encoding='utf-8')
        (OUT/f'project-{i+1}-mobile.svg').write_text(card(i,mobile=True),encoding='utf-8')
    print('Built cinematic morphing covers and six individually linked project cards.')


if __name__=='__main__':main()
