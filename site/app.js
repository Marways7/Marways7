'use strict';

(() => {
  const $ = (s) => document.querySelector(s);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const canvas = $('#sculpture');
  const hero = $('.hero');
  const pauseButton = $('#pause');
  let paused = reduced.matches;
  let visible = true;
  let raf = 0;
  let last = 0;
  let elapsed = 0;
  let form = 0;
  let morph = 1;
  let burst = 0;
  let drag = false;
  let lastPointer = {x: 0, y: 0};
  let rotation = {x: -.12, y: -.32};
  let targetRotation = {...rotation};
  let light = {x: 0, y: 0};
  let selectedProject = 0;
  const labels = ['标识 7', '折叠轨道', '流动信号'];
  const gl = canvas.getContext('webgl', {alpha: true, antialias: true, premultipliedAlpha: false, powerPreference: 'low-power'});
  const steps = 224, sides = 40, vertexCount = (steps + 1) * (sides + 1);
  const clamp = (n,a,b) => Math.max(a,Math.min(b,n));
  const norm = (v) => {const l=Math.hypot(...v)||1;return v.map(n=>n/l);};
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const add = (a,b) => a.map((n,i)=>n+b[i]);
  const sub = (a,b) => a.map((n,i)=>n-b[i]);
  const mul = (v,n) => v.map(x=>x*n);
  const points = [[-.9,1.07,0],[-.48,1.14,0],[.3,1.12,0],[.88,.99,0],[.43,.3,.02],[-.10,-.54,.03],[-.46,-1.3,0]];
  function catmull(t) {
    const p=clamp(t,0,1)*(points.length-1),i=Math.min(points.length-2,Math.floor(p)),s=p-i;
    const a=points[Math.max(0,i-1)],b=points[i],c=points[i+1],d=points[Math.min(points.length-1,i+2)];
    return b.map((v,k)=>.5*((2*v)+(-a[k]+c[k])*s+(2*a[k]-5*v+4*c[k]-d[k])*s*s+(-a[k]+3*v-3*c[k]+d[k])*s*s*s));
  }
  function center(t,mode) {
    if(mode===0)return catmull(t);
    const a=t*Math.PI*2;
    if(mode===1)return [(.87+.27*Math.cos(3*a))*Math.cos(2*a),(.87+.27*Math.cos(3*a))*Math.sin(2*a),.40*Math.sin(3*a)];
    return [(t-.5)*2.55,.6*Math.sin(a*1.1)+.22*Math.sin(a*2.8),.30*Math.cos(a*1.5)];
  }
  function geometry(mode) {
    const p=new Float32Array(vertexCount*3),n=new Float32Array(vertexCount*3),uv=new Float32Array(vertexCount*2);
    for(let i=0;i<=steps;i++){
      const t=i/steps,c=center(t,mode),tangent=norm(sub(center(Math.min(1,t+.001),mode),center(Math.max(0,t-.001),mode)));
      const guide=Math.abs(tangent[2])>.9?[0,1,0]:[0,0,1],normal=norm(cross(tangent,guide)),binormal=norm(cross(tangent,normal));
      for(let j=0;j<=sides;j++){
        const a=j/sides*Math.PI*2,nn=add(mul(normal,Math.cos(a)),mul(binormal,Math.sin(a)));
        const radius=mode===1?.19:mode===2?.19+.045*Math.sin(t*20):.245;
        const at=(i*(sides+1)+j);p.set(add(c,mul(nn,radius)),at*3);n.set(nn,at*3);uv.set([t,j/sides],at*2);
      }
    }
    return {p,n,uv};
  }

  const shapes=[0,1,2].map(geometry);
  let from=shapes[0],to=shapes[0];
  let program, uniforms, buffers, particleProgram, particleUniforms, particleBuffer, glReady=false;
  function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
  function link(v,f){const p=gl.createProgram();gl.attachShader(p,shader(gl.VERTEX_SHADER,v));gl.attachShader(p,shader(gl.FRAGMENT_SHADER,f));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));return p;}
  const common=`
    uniform float uTime,uMorph,uAspect,uMobile,uBurst; uniform vec2 uRotation;
    mat3 rotation(){float x=uRotation.x,y=uRotation.y;return mat3(cos(y),0.,-sin(y),0.,1.,0.,sin(y),0.,cos(y))*mat3(1.,0.,0.,0.,cos(x),sin(x),0.,-sin(x),cos(x));}
    vec4 project(vec3 p){p*=mix(1.12,.62,uMobile);p+=vec3(mix(1.03,0.,uMobile),mix(.22,1.04,uMobile),-4.75);float f=2.4;return vec4(p.x*f/uAspect,p.y*f,-p.z-0.2,-p.z);}
  `;
  function setupGL(){
    program=link(`precision highp float;attribute vec3 aFrom,aTo,aNormalFrom,aNormalTo;attribute vec2 aUv;varying vec3 vN,vP;varying vec2 vUv;${common}
      void main(){float m=uMorph*uMorph*(3.-2.*uMorph);vec3 n=normalize(mix(aNormalFrom,aNormalTo,m));vec3 p=mix(aFrom,aTo,m);p+=n*.009*sin(aUv.x*90.+uTime*.8);p+=n*uBurst*.12;mat3 r=rotation();vP=r*p;vN=r*n;vUv=aUv;gl_Position=project(vP);}`,`
      precision highp float;varying vec3 vN,vP;varying vec2 vUv;uniform float uTime;uniform vec2 uLight;
      void main(){vec3 n=normalize(vN),view=normalize(vec3(0.,0.,5.)-vP),refl=reflect(-view,n);
        vec3 pearl=.53+.39*cos(6.28318*(vec3(.05,.27,.49)+refl.y*.28+refl.x*.14+vUv.x*.19+uTime*.009));
        float diffuse=.23+.50*max(0.,dot(n,normalize(vec3(-.5+uLight.x*.4,.8+uLight.y*.3,1.4))));
        float fres=pow(1.-max(0.,dot(n,view)),2.8);
        float strip1=pow(max(0.,1.-abs(refl.y-.48)*2.8),14.);
        float strip2=pow(max(0.,1.-abs(refl.x+.58)*3.),20.);
        float sheen=pow(max(0.,dot(n,normalize(vec3(-.8,1.5,2.6)))),26.);
        float lines=.94+.06*smoothstep(.15,.25,fract(vUv.x*148.));
        vec3 color=pearl*diffuse*.87+vec3(.83,.90,1.)*(strip1*.78+strip2*.35+sheen*.85)+vec3(.44,.55,.91)*fres*.65;
        color*=lines;gl_FragColor=vec4(pow(color,vec3(.88)),1.);
      }`);
    buffers={};for(const name of ['aFrom','aTo','aNormalFrom','aNormalTo','aUv'])buffers[name]=gl.createBuffer();
    const indices=[];for(let i=0;i<steps;i++)for(let j=0;j<sides;j++){const a=i*(sides+1)+j,b=a+sides+1;indices.push(a,b,a+1,b,b+1,a+1);}
    buffers.indices=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,buffers.indices);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint16Array(indices),gl.STATIC_DRAW);buffers.count=indices.length;
    uniforms={};for(const name of ['uTime','uMorph','uAspect','uMobile','uBurst','uRotation','uLight'])uniforms[name]=gl.getUniformLocation(program,name);
    upload();
    particleProgram=link(`precision highp float;attribute vec3 aSeed;varying float vAlpha;${common}
      void main(){float a=aSeed.x*6.28318+uTime*.035;float b=aSeed.y*3.14159;float rad=1.3+aSeed.z*.9+uBurst*(.5+aSeed.x)*1.6;vec3 p=vec3(cos(a)*sin(b)*rad,cos(b)*rad,sin(a)*sin(b)*rad);p=rotation()*p;gl_Position=project(p);gl_PointSize=(1.+aSeed.z*2.)*(1.+uBurst*.5);vAlpha=.16+aSeed.z*.45;}`,`
      precision mediump float;varying float vAlpha;void main(){float d=length(gl_PointCoord-.5);gl_FragColor=vec4(.74,.8,1.,(1.-smoothstep(.1,.5,d))*vAlpha);}`);
    particleUniforms={};for(const name of ['uTime','uMorph','uAspect','uMobile','uBurst','uRotation'])particleUniforms[name]=gl.getUniformLocation(particleProgram,name);
    const seeds=new Float32Array(240*3);let seed=7;for(let i=0;i<seeds.length;i++){seed=(seed*1664525+1013904223)>>>0;seeds[i]=seed/4294967296;}
    particleBuffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,particleBuffer);gl.bufferData(gl.ARRAY_BUFFER,seeds,gl.STATIC_DRAW);
  }
  function attr(name,arr,size){const loc=gl.getAttribLocation(program,name);gl.bindBuffer(gl.ARRAY_BUFFER,buffers[name]);gl.bufferData(gl.ARRAY_BUFFER,arr,gl.DYNAMIC_DRAW);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,size,gl.FLOAT,false,0,0);}
  function upload(){gl.useProgram(program);attr('aFrom',from.p,3);attr('aTo',to.p,3);attr('aNormalFrom',from.n,3);attr('aNormalTo',to.n,3);attr('aUv',to.uv,2);}
  function bindMesh(){for(const [name,size] of [['aFrom',3],['aTo',3],['aNormalFrom',3],['aNormalTo',3],['aUv',2]]){const loc=gl.getAttribLocation(program,name);gl.bindBuffer(gl.ARRAY_BUFFER,buffers[name]);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,size,gl.FLOAT,false,0,0);}gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,buffers.indices);}
  function uniformsFor(u,time){gl.uniform1f(u.uTime,time);gl.uniform1f(u.uMorph,morph);gl.uniform1f(u.uAspect,canvas.clientWidth/canvas.clientHeight);gl.uniform1f(u.uMobile,innerWidth<=850?1:0);gl.uniform1f(u.uBurst,burst);gl.uniform2f(u.uRotation,rotation.x+(!paused?Math.sin(time*.2)*.04:0),rotation.y+(!paused?Math.sin(time*.16)*.12:0));}
  function renderGL(){
    if(!glReady)return;gl.viewport(0,0,canvas.width,canvas.height);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.disable(gl.BLEND);
    gl.useProgram(program);bindMesh();uniformsFor(uniforms,elapsed);gl.uniform2f(uniforms.uLight,light.x,light.y);gl.drawElements(gl.TRIANGLES,buffers.count,gl.UNSIGNED_SHORT,0);
    gl.useProgram(particleProgram);gl.bindBuffer(gl.ARRAY_BUFFER,particleBuffer);const loc=gl.getAttribLocation(particleProgram,'aSeed');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,3,gl.FLOAT,false,0,0);uniformsFor(particleUniforms,elapsed);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);gl.depthMask(false);gl.drawArrays(gl.POINTS,0,240);gl.depthMask(true);gl.disable(gl.BLEND);
  }
  function resize(){const ratio=Math.min(devicePixelRatio||1,1.7);canvas.width=Math.round(canvas.clientWidth*ratio);canvas.height=Math.round(canvas.clientHeight*ratio);resizeProject();renderGL();}
  function wake(){if(!raf&&!document.hidden)raf=requestAnimationFrame(tick);}
  function tick(t){raf=0;const dt=Math.min(.04,(t-last)/1000||.016);last=t;
    if(!paused&&visible){elapsed+=dt;morph=Math.min(1,morph+dt*.7);burst=Math.max(0,burst-dt*.55);rotation.x+=(targetRotation.x-rotation.x)*.1;rotation.y+=(targetRotation.y-rotation.y)*.1;}
    renderGL();drawProject();if(!paused&&visible&&!document.hidden)wake();
  }
  function chooseForm(next){
    if(next===form)return;const m=morph*morph*(3-2*morph);from={p:from.p.map((v,i)=>v*(1-m)+to.p[i]*m),n:from.n.map((v,i)=>v*(1-m)+to.n[i]*m)};to=shapes[next];form=next;morph=paused?1:0;if(program)upload();
    document.querySelectorAll('[data-form]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.form)===form)));$('#scene-status').textContent=`当前形态：${labels[form]}。`;renderGL();wake();
  }
  function syncPause(){pauseButton.textContent=paused?'继续动态':'暂停动态';pauseButton.setAttribute('aria-pressed',String(paused));if(paused){morph=1;burst=0;rotation={...targetRotation};}renderGL();drawProject();wake();}
  pauseButton.addEventListener('click',()=>{paused=!paused;syncPause();});
  reduced.addEventListener('change',e=>{paused=e.matches;syncPause();});
  document.querySelectorAll('[data-form]').forEach(b=>b.addEventListener('click',()=>chooseForm(Number(b.dataset.form))));
  $('#burst').addEventListener('click',()=>{burst=paused?.7:1;renderGL();wake();$('#scene-status').textContent=paused?'已展开粒子。':'灵感粒子已散开，正在回归。';});
  canvas.addEventListener('pointerdown',e=>{drag=true;lastPointer={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointerup',()=>{drag=false;});canvas.addEventListener('pointercancel',()=>{drag=false;});
  canvas.addEventListener('pointermove',e=>{const rect=canvas.getBoundingClientRect();light={x:(e.clientX-rect.left)/rect.width*2-1,y:1-(e.clientY-rect.top)/rect.height*2};if(drag){targetRotation.y+=(e.clientX-lastPointer.x)*.009;targetRotation.x=clamp(targetRotation.x+(e.clientY-lastPointer.y)*.006,-1.1,1.1);lastPointer={x:e.clientX,y:e.clientY};if(paused)rotation={...targetRotation};}renderGL();});
  canvas.addEventListener('keydown',e=>{let handled=true;switch(e.key){case'ArrowLeft':targetRotation.y-=.16;break;case'ArrowRight':targetRotation.y+=.16;break;case'ArrowUp':targetRotation.x-=.12;break;case'ArrowDown':targetRotation.x+=.12;break;case' ':paused=!paused;syncPause();break;default:handled=false;}if(handled){e.preventDefault();targetRotation.x=clamp(targetRotation.x,-1.1,1.1);if(paused)rotation={...targetRotation};renderGL();wake();}});
  document.addEventListener('visibilitychange',()=>{last=0;if(document.hidden){cancelAnimationFrame(raf);raf=0;}else wake();});

  const projects=[
    {name:'ECG Identification',tech:'Python / PyTorch / Signal processing',desc:'从一段心电信号出发，探索人体自身的身份特征。结合信号处理与轻量 CNN 的心电身份识别实验。',repo:'ECG_IdentificationX',symbol:'ECG',color:[255,185,159]},
    {name:'AiliaoX',tech:'TypeScript / MCP / AI',desc:'把自然语言带进医院信息管理。通过 MCP 连接 AI 与数据，让对话成为探索信息与执行任务的入口。',repo:'AiliaoX',symbol:'AI',color:[159,244,227]},
    {name:'DeepReadX',tech:'Java / Android / OCR',desc:'读到难懂的一页时，换一种讲法。集 PDF 阅读、OCR 与自定义风格 AI 讲解于一体的 Android 应用原型。',repo:'DeepReadX',symbol:'Read',color:[185,183,255]},
    {name:'Desktop Operator',tech:'Python / MCP / CLI',desc:'让意图走出聊天框，进入桌面。为 AI Agent 提供桌面操作能力，分别提供 MCP 和 CLI 两种接入方式。',repo:'cua_desktop_operator_skill',symbol:'Do',color:[168,204,255]},
    {name:'Signal Sprint',tech:'JavaScript / Browser / Measurement',desc:'观察直播播放链路，测量并优化本地播放体验。让优化发生在可观察、可比较的指标之上。',repo:'signal-sprint',symbol:'Live',color:[166,223,240]},
    {name:'Campus Guide',tech:'TypeScript / Web / Resource sharing',desc:'把散落的学习资源汇聚成一个可发现、可管理、可分享的地方。面向校园学习场景的全栈 Web 项目。',repo:'college_student_self-rescue_guide_website',symbol:'Share',color:[238,195,172]}
  ];
  const projectCanvas=$('#project-canvas'),ctx=projectCanvas.getContext('2d');
  function resizeProject(){const d=Math.min(devicePixelRatio||1,1.7);projectCanvas.width=projectCanvas.clientWidth*d;projectCanvas.height=projectCanvas.clientHeight*d;}
  function drawProject(){if(!ctx)return;const w=projectCanvas.width,h=projectCanvas.height,col=projects[selectedProject].color;ctx.clearRect(0,0,w,h);ctx.save();ctx.translate(w*.5,h*.53);const scale=Math.min(w/650,h/300);ctx.scale(scale,scale);ctx.lineWidth=.8;const time=elapsed;
    for(let j=0;j<46;j++){const o=(j-23)/23;ctx.beginPath();for(let k=0;k<=210;k++){const t=k/210;let x=(t-.5)*420,y=0;
      if(selectedProject===0){const beat=Math.exp(-Math.pow((t-.43)*35,2))*-77+Math.exp(-Math.pow((t-.49)*38,2))*113-Math.exp(-Math.pow((t-.54)*30,2))*41;y=beat+o*42+Math.sin(t*15+time*.6+o)*3;}
      else if(selectedProject===1){const a=t*Math.PI*2;x=Math.cos(a)*150*(1+o*.12);y=Math.sin(a)*64+o*36+Math.sin(a*3+time*.35)*8;x+=Math.sin(o*2)*30;}
      else if(selectedProject===2){x=(t-.5)*360;y=-Math.abs(Math.sin(t*Math.PI*2))*65+o*(20+Math.abs(t-.5)*60)+Math.sin(t*5+o+time*.3)*10;}
      else if(selectedProject===3){const coords=[[-70,-90],[-36,85],[8,31],[64,82],[83,60],[26,12],[101,-5],[-70,-90]];const pos=t*(coords.length-1),i=Math.min(coords.length-2,Math.floor(pos)),f=pos-i;x=coords[i][0]*(1-f)+coords[i+1][0]*f+o*40;y=coords[i][1]*(1-f)+coords[i+1][1]*f+o*12;}
      else if(selectedProject===4){y=Math.sin(t*13-time*.9+o*.6)*65*Math.sin(t*Math.PI)+o*35;}
      else{const a=t*Math.PI*2;x=Math.cos(a)*170;y=Math.sin(a)*48+o*55+Math.cos(a*2+time*.3)*8;}
      if(k===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
      ctx.strokeStyle=`rgba(${col.join(',')},${.16+(1-Math.abs(o))*.52})`;ctx.stroke();
    }ctx.restore();
  }
  function selectProject(index,focus=false){selectedProject=index;const p=projects[index];document.querySelectorAll('[data-project]').forEach((b,i)=>{b.setAttribute('aria-selected',String(i===index));b.tabIndex=i===index?0:-1;});$('#project-panel').setAttribute('aria-labelledby',`tab-${index}`);$('#project-number').textContent=String(index+1).padStart(2,'0');$('#project-title').textContent=p.name;$('#project-tech').textContent=p.tech;$('#project-description').textContent=p.desc;$('#project-link').href=`https://github.com/Marways7/${p.repo}`;$('#project-symbol').textContent=p.symbol;$('#project-secondary').hidden=index!==3;const info=$('.project-info');info.classList.remove('changing');void info.offsetWidth;info.classList.add('changing');if(focus)$(`#tab-${index}`).focus();drawProject();}
  document.querySelectorAll('[data-project]').forEach(b=>{b.addEventListener('click',()=>selectProject(Number(b.dataset.project)));b.addEventListener('keydown',e=>{let i=Number(b.dataset.project);if(e.key==='ArrowDown'||e.key==='ArrowRight')i=(i+1)%6;else if(e.key==='ArrowUp'||e.key==='ArrowLeft')i=(i+5)%6;else if(e.key==='Home')i=0;else if(e.key==='End')i=5;else return;e.preventDefault();selectProject(i,true);});});
  function fallback(){glReady=false;canvas.hidden=true;$('#fallback').hidden=false;$('#gesture-hint').textContent='当前设备显示静态主视觉';document.querySelectorAll('[data-form],#burst').forEach(b=>b.disabled=true);}
  if(gl){try{setupGL();glReady=true;}catch(error){console.error('Sculpture unavailable:',error.message);fallback();}}else fallback();
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();fallback();});
  new ResizeObserver(resize).observe(hero);new ResizeObserver(()=>{resizeProject();drawProject();}).observe($('.project-art'));
  const intersections=new Map();
  const observer=new IntersectionObserver(entries=>{entries.forEach(e=>intersections.set(e.target,e.isIntersecting));visible=[...intersections.values()].some(Boolean);if(visible){last=0;wake();}},{rootMargin:'120px'});observer.observe(hero);observer.observe($('#work'));
  resize();syncPause();wake();
})();
