/* Marways / Living possibilities. Native scrolling; one continuous WebGL surface. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const chapters = [...document.querySelectorAll('.chapter')];
  const rail = [...document.querySelectorAll('.scene-rail a')];
  const root = document.documentElement, canvas = $('#sculpture');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const staticView = new URLSearchParams(location.search).get('view')==='static';
  const clamp = (v, a=0, b=1) => Math.max(a, Math.min(b, v));
  const mix = (a,b,t) => a+(b-a)*t;
  const smooth = t => t*t*(3-2*t);
  const luminance = c => c.map(v=>{v/=255;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4);}).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
  const rgb = hex => [1,3,5].map(i => parseInt(hex.slice(i,i+2),16)/255);
  const scenes = [
    ['#eceee9','#183d35','#9cba77','Possibility','让好奇，生长。'],
    ['#281d29','#f5e7e5','#d97593','Heartbeat','ECG Identification'],
    ['#dee7df','#1e433d','#78a9a0','Dialogue','AiliaoX'],
    ['#f0eddf','#4b472b','#c9b66a','Understanding','DeepReadX'],
    ['#172b36','#e4e9e7','#89b1c8','Intention','Desktop Operator'],
    ['#e6eac9','#37462b','#97b14e','Momentum','Signal Sprint'],
    ['#dce6ed','#28465a','#89b4d3','Connection','Campus Guide'],
    ['#eceee9','#183d35','#9cba77','What’s next?','保持好奇。']
  ].map(([bg,ink,material,word,label]) => ({bg:rgb(bg),ink:rgb(ink),material:rgb(material),word,label}));
  let paused = reduced.matches||staticView, watching=false, active=-1, dirty=true, raf=0;
  document.body.classList.toggle('static-view',staticView);
  let bounds=[], catalogueTop=0, target=0, progress=0, time=0, previous=0, bloom=0;
  let rotation=.0, targetRotation=.0, tilt=-.08, targetTilt=-.08, mx=0, my=0;
  let focusBlend=0, glReady=false, quality=1, slow=0, lastUI=-999, dragging=null;
  const dialog = $('#project-index');
  function requestFrame() { dirty=true; if(!raf&&!document.hidden) raf=requestAnimationFrame(frame); }
  function resize() {
    bounds=chapters.map(el => el.offsetTop);
    catalogueTop=$('#projects').offsetTop;
    if(glReady) {
      const dpr=Math.min(devicePixelRatio||1,innerWidth<761?1.5:1.75)*quality;
      canvas.width=Math.round(innerWidth*dpr); canvas.height=Math.round(innerHeight*dpr);
    }
    updateTarget(); requestFrame();
  }
  function updateTarget() {
    const y=scrollY;
    let i=0; while(i<7&&y>=bounds[i+1]) i++;
    const fraction=i===7?0:clamp((y-bounds[i])/(bounds[i+1]-bounds[i]));
    // Stable reading phase, then one reversible transition between chapters.
    target=i+smooth(clamp((fraction-.20)/.68));
    if(reduced.matches||staticView) target=Math.round(target);
    const atCatalogue=y>catalogueTop-innerHeight*.3;
    document.body.classList.toggle('at-catalogue',atCatalogue);
    $('.scene-rail').inert=atCatalogue;
    $('.experience-bar').inert=atCatalogue;
    $('#rotate').inert=atCatalogue;
  }
  addEventListener('scroll',()=>{updateTarget();requestFrame();},{passive:true});
  addEventListener('resize',resize,{passive:true});
  document.addEventListener('visibilitychange',()=>{previous=0;if(document.hidden){cancelAnimationFrame(raf);raf=0;}else requestFrame();});
  function setPaused(v) {
    paused=v; $('#pause').setAttribute('aria-pressed',String(v));
    $('#pause').textContent=v?'继续动态':'暂停动态'; requestFrame();
  }
  $('#pause').addEventListener('click',()=>setPaused(!paused));
  reduced.addEventListener('change',()=>{setPaused(reduced.matches||staticView);updateTarget();requestFrame();});
  function unfold() {
    bloom=reduced.matches||paused?(bloom>.1?0:.6):1.3;
    $('#scene-status').textContent=bloom?'形态已展开。':'形态已收束。'; requestFrame();
  }
  $('#bloom').addEventListener('click',unfold);
  function setWatching(v) {
    watching=v; document.body.classList.toggle('watching',v);
    $('#focus-mode').setAttribute('aria-pressed',String(v));
    $('#focus-mode').innerHTML=v?'返回介绍 <span aria-hidden="true">⤡</span>':'纯粹观看 <span aria-hidden="true">⤢</span>';
    requestFrame();
  }
  $('#focus-mode').addEventListener('click',()=>setWatching(!watching));
  addEventListener('keydown',e=>{if(e.key==='Escape'&&watching)setWatching(false);});
  $('.index-trigger').addEventListener('click',()=>{
    dialog.showModal(); document.body.style.overflow='hidden';
    if(!reduced.matches) dialog.animate([{opacity:0,transform:'translateY(22px) scale(.98)'},{opacity:1,transform:'none'}],{duration:400,easing:'cubic-bezier(.2,.8,.2,1)'});
    requestFrame();
  });
  function closeIndex(){dialog.close();document.body.style.overflow='';requestFrame();}
  $('#close-index').addEventListener('click',closeIndex);
  dialog.addEventListener('close',()=>{document.body.style.overflow='';requestFrame();});
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeIndex();}});
  dialog.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{closeIndex();if(watching)setWatching(false);}));
  // The canvas keeps vertical touch scrolling native. The small rotation handle allows two-axis drag.
  function down(e) {
    if(e.pointerType==='mouse'&&e.button!==0)return;
    dragging={id:e.pointerId,x:e.clientX,y:e.clientY,handle:e.currentTarget.id==='rotate'};
    e.currentTarget.setPointerCapture(e.pointerId); requestFrame();
  }
  function move(e) {
    mx=e.clientX/innerWidth*2-1;my=e.clientY/innerHeight*2-1;
    if(dragging&&dragging.id===e.pointerId) {
      targetRotation+=(e.clientX-dragging.x)*.008;
      if(dragging.handle||e.pointerType==='mouse')targetTilt=clamp(targetTilt+(e.clientY-dragging.y)*.004,-.65,.65);
      dragging.x=e.clientX;dragging.y=e.clientY;
    }
    requestFrame();
  }
  function up(){dragging=null;}
  [canvas,$('#rotate')].forEach(el=>{el.addEventListener('pointerdown',down);el.addEventListener('pointermove',move);el.addEventListener('pointerup',up);el.addEventListener('pointercancel',up);});
  addEventListener('pointermove',e=>{if(e.pointerType==='mouse'&&!dragging){mx=e.clientX/innerWidth*2-1;my=e.clientY/innerHeight*2-1;requestFrame();}},{passive:true});
  $('#rotate').addEventListener('keydown',e=>{
    if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(e.key)){
      e.preventDefault();
      if(e.key==='ArrowLeft')targetRotation-=.2;if(e.key==='ArrowRight')targetRotation+=.2;
      if(e.key==='ArrowUp')targetTilt=clamp(targetTilt-.1,-.65,.65);if(e.key==='ArrowDown')targetTilt=clamp(targetTilt+.1,-.65,.65);
      if(e.key===' ')unfold();requestFrame();
    }
  });

  const TAU=Math.PI*2,BANDS=24,STEPS=96,ACROSS=14;
  // All shapes share topology. Normals are derived from each parametric surface.
  function point(kind,k,u,v) {
    const b=k/(BANDS-1),a=k/BANDS*TAU;
    if(kind===7)kind=0;
    if(kind===0) {
      const r=.24+2.35*Math.sin(u*Math.PI*.77),theta=a+u*1.55;
      const w=(.04+.57*Math.pow(Math.sin(Math.PI*u),.8))*v;
      return [Math.cos(theta)*r-Math.sin(theta)*w,Math.sin(theta)*r+Math.cos(theta)*w,.8*Math.cos(u*Math.PI*1.45)+.38*Math.cos(v*Math.PI*.6)*Math.sin(u*Math.PI)+.16*Math.sin(a*3)];
    }
    if(kind===1) {
      const t=u*TAU;const pulse=.6*Math.exp(-Math.pow((u-.25)/.027,2))-.23*Math.exp(-Math.pow((u-.30)/.04,2))+.18*Math.exp(-Math.pow((u-.66)/.09,2));
      const r=1.45+b*.7+v*.035;
      return [Math.cos(t)*r,Math.sin(t)*r+Math.sin(t*3+b*3)*.10+pulse,(b-.5)*1.35+.32*Math.sin(t*2+b*4)+v*.08];
    }
    if(kind===2) {
      const group=Math.floor(k/8),f=k%8/7,t=u*TAU,theta=group*TAU/3;
      let x=(1.33+f*.27+v*.032)*Math.cos(t)+.45,y=(1.33+f*.27+v*.032)*Math.sin(t),z=.58*Math.sin(t*2)+(f-.5)*.38;
      return [x*Math.cos(theta)-y*Math.sin(theta),x*Math.sin(theta)+y*Math.cos(theta),z+.25*group];
    }
    if(kind===3) {
      const theta=(b-.5)*2.45,r=.18+u*2.75;
      return [Math.sin(theta)*r, v*(.95+.13*Math.sin(Math.PI*u))+.20*Math.sin(u*3+b*2),Math.cos(theta)*r-1.25+.17*Math.sin(u*Math.PI)*Math.cos(v*2)];
    }
    if(kind===4) {
      const t=u*TAU*1.65+a*.12,r=1.1+.75*b+v*.07;
      return [Math.cos(t)*r, (u-.5)*3.65+(b-.5)*.38,Math.sin(t)*r];
    }
    if(kind===5) {
      const x=(u-.5)*4.9,y=(b-.5)*2.65+v*.055;
      return [x,y+.23*Math.sin(u*7+b*3),.7*Math.sin(u*6.5+b*3.5)+.20*Math.cos(b*8)+v*.06];
    }
    const t=u*TAU,theta=a,r=(.45+1.7*Math.sin(u*Math.PI))*(1+.10*Math.sin(t*3));
    return [Math.cos(theta)*r+v*.07*Math.sin(theta),Math.sin(theta)*r-v*.07*Math.cos(theta),1.45*Math.cos(u*Math.PI)+.25*Math.sin(t+b*3)];
  }
  function makeShape(kind) {
    const positions=[],normals=[];
    for(let k=0;k<BANDS;k++)for(let i=0;i<=STEPS;i++)for(let j=0;j<=ACROSS;j++) {
      const u=clamp(i/STEPS,.0001,.9999),v=j/ACROSS*2-1;
      const p=point(kind,k,u,v),a=point(kind,k,clamp(u+.0001,.00001,.99999),v),b=point(kind,k,u,v+.0001);
      const dx=a[0]-p[0],dy=a[1]-p[1],dz=a[2]-p[2],ex=b[0]-p[0],ey=b[1]-p[1],ez=b[2]-p[2];
      let nx=dy*ez-dz*ey,ny=dz*ex-dx*ez,nz=dx*ey-dy*ex,l=Math.hypot(nx,ny,nz)||1;
      positions.push(...p);normals.push(nx/l,ny/l,nz/l);
    }
    return {p:new Float32Array(positions),n:new Float32Array(normals)};
  }
  let gl,program,loc={},shapes=[],indexBuffer,uvBuffer,indexCount=0,boundPair='';
  const vertex=`
    precision highp float;
    attribute vec3 aPosition,aNext,aNormal,aNextNormal;attribute vec2 aUv;
    uniform float uMorph,uTime,uRotation,uTilt,uBloom,uAspect,uScale,uMobile,uFocus,uTravel;
    uniform vec2 uPointer;varying vec3 vNormal,vPosition;varying vec2 vUv;varying float vBand;
    mat3 ry(float a){return mat3(cos(a),0.,-sin(a),0.,1.,0.,sin(a),0.,cos(a));}
    mat3 rx(float a){return mat3(1.,0.,0.,0.,cos(a),sin(a),0.,-sin(a),cos(a));}
    mat3 rz(float a){return mat3(cos(a),sin(a),0.,-sin(a),cos(a),0.,0.,0.,1.);}
    void main(){
      float m=smoothstep(0.,1.,uMorph);vec3 p=mix(aPosition,aNext,m);vec3 n=normalize(mix(aNormal,aNextNormal,m));
      float envelope=sin(m*3.14159265);float breath=sin(uTime*.7+aUv.x*5.)*.018;
      p*=1.+breath+uBloom*.22+envelope*.14;
      p+=n*(uBloom*.32+envelope*.13)*sin(aUv.x*6.+aUv.y*2.);
      mat3 spin=ry(uRotation+uPointer.x*.06+uTravel*.20+envelope*.65)*rx(uTilt+uPointer.y*.035)*rz(-.27+envelope*.23);
      p=spin*p;n=spin*n;
      p.y+=sin(uTime*.55)*.045;
      float camera=7.8-envelope*.55,depth=camera-p.z,projection=2.35;
      vec2 offset=mix(vec2(.33,-.03),vec2(0.,.28),uMobile);
      offset=mix(offset,vec2(0.,0.),uFocus);
      gl_Position=vec4(p.x*projection/uAspect*uScale+offset.x*depth,p.y*projection*uScale+offset.y*depth,(depth-4.)*.5,depth);
      vNormal=n;vPosition=p;vUv=aUv;
    }`;
  const fragment=`
    precision highp float;varying vec3 vNormal,vPosition;varying vec2 vUv;
    uniform vec3 uMaterial,uInk;uniform float uTime;uniform vec2 uPointer;
    void main(){
      vec3 n=normalize(vNormal);if(!gl_FrontFacing)n=-n;
      vec3 eye=normalize(vec3(0.,0.,7.8)-vPosition);
      vec3 light=normalize(vec3(-.5+uPointer.x*.15,1.,1.8));
      float diffuse=max(dot(n,light),0.);float rim=pow(1.-abs(dot(n,eye)),2.5);
      vec3 reflected=reflect(-eye,n);
      float softbox=pow(max(0.,dot(reflected,normalize(vec3(-.4,.6,1.)))),12.);
      float stripe=pow(.5+.5*sin(reflected.y*13.+reflected.x*5.),16.);
      float threads=.985+.015*sin(vUv.y*36.);
      float edge=smoothstep(.86,1.,abs(vUv.y));
      vec3 base=mix(uMaterial,vec3(.92,.95,.88),.32);
      float fill=max(dot(n,normalize(vec3(1.,-.4,2.))),0.);
      vec3 color=base*(.30+diffuse*.62+fill*.23)*threads;
      color+=vec3(.98,.97,.86)*softbox*.64+mix(uMaterial,vec3(.9),.5)*stripe*.10;
      color=mix(color,vec3(.96,.97,.91),rim*.24+edge*.20);
      float sheen=pow(max(0.,dot(n,normalize(vec3(1.,-.3,.6)))),3.);
      color+=uMaterial*sheen*.14;
      gl_FragColor=vec4(color,1.);
    }`;
  function compile(type,source) {
    const shader=gl.createShader(type);gl.shaderSource(shader,source);gl.compileShader(shader);
    if(!gl.getShaderParameter(shader,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(shader));return shader;
  }
  function buffer(data) {const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,data,gl.STATIC_DRAW);return b;}
  function attribute(name,b,size) {gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.enableVertexAttribArray(loc[name]);gl.vertexAttribPointer(loc[name],size,gl.FLOAT,false,0,0);}
  function fallback() {
    glReady=false;canvas.hidden=true;$('#fallback').hidden=false;
    $('#bloom').disabled=true;$('#rotate').hidden=true;
    $('.art-hint').textContent='向下浏览，探索作品。';
  }
  function initGL() {
    try {
      gl=canvas.getContext('webgl',{alpha:true,antialias:true,powerPreference:'default'});if(!gl)throw Error('WebGL unavailable');
      program=gl.createProgram();gl.attachShader(program,compile(gl.VERTEX_SHADER,vertex));gl.attachShader(program,compile(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);
      if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));gl.useProgram(program);
      ['aPosition','aNext','aNormal','aNextNormal','aUv'].forEach(n=>loc[n]=gl.getAttribLocation(program,n));
      ['uMorph','uTime','uRotation','uTilt','uBloom','uAspect','uScale','uMobile','uFocus','uPointer','uMaterial','uInk','uTravel'].forEach(n=>loc[n]=gl.getUniformLocation(program,n));
      for(let i=0;i<7;i++){const s=makeShape(i);shapes.push({p:buffer(s.p),n:buffer(s.n)});}shapes.push(shapes[0]);
      const uv=[],indices=[],row=ACROSS+1,strip=(STEPS+1)*row;
      for(let k=0;k<BANDS;k++)for(let i=0;i<=STEPS;i++)for(let j=0;j<=ACROSS;j++)uv.push(i/STEPS,j/ACROSS*2-1);
      for(let k=0;k<BANDS;k++)for(let i=0;i<STEPS;i++)for(let j=0;j<ACROSS;j++){const a=k*strip+i*row+j,b=a+row;indices.push(a,b,a+1,b,b+1,a+1);}
      uvBuffer=buffer(new Float32Array(uv));attribute('aUv',uvBuffer,2);
      indexBuffer=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,indexBuffer);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint16Array(indices),gl.STATIC_DRAW);indexCount=indices.length;
      gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.clearColor(0,0,0,0);glReady=true;
    } catch(error) {console.warn('Showing static illustration:',error.message);fallback();}
  }
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();fallback();requestFrame();});
  canvas.addEventListener('webglcontextrestored',()=>{canvas.hidden=false;$('#fallback').hidden=true;$('#rotate').hidden=false;$('#bloom').disabled=false;boundPair='';shapes=[];initGL();resize();});
  function draw(a,b,m) {
    gl.viewport(0,0,canvas.width,canvas.height);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    const pair=a+':'+b;if(boundPair!==pair){attribute('aPosition',shapes[a].p,3);attribute('aNext',shapes[b].p,3);attribute('aNormal',shapes[a].n,3);attribute('aNextNormal',shapes[b].n,3);boundPair=pair;}
    const mobile=innerWidth<761?1:0;
    gl.uniform1f(loc.uMorph,m);gl.uniform1f(loc.uTime,time);gl.uniform1f(loc.uRotation,rotation+Math.sin(time*.1)*.10);
    gl.uniform1f(loc.uTilt,tilt);gl.uniform1f(loc.uBloom,bloom);gl.uniform1f(loc.uAspect,innerWidth/innerHeight);
    gl.uniform1f(loc.uScale,mobile?.55:1.02);gl.uniform1f(loc.uMobile,mobile);gl.uniform1f(loc.uFocus,focusBlend);
    gl.uniform1f(loc.uTravel,progress);gl.uniform2f(loc.uPointer,mx,my);
    gl.uniform3fv(loc.uMaterial,scenes[a].material.map((x,i)=>mix(x,scenes[b].material[i],m)));
    gl.drawElements(gl.TRIANGLES,indexCount,gl.UNSIGNED_SHORT,0);
  }
  function updateUI(a,b,m) {
    const c=Math.round(progress);if(c!==active){active=c;$('#ambient-word').textContent=scenes[c].word;$('#scene-caption').textContent=scenes[c].label;$('#scene-status').textContent='当前：'+(c===0?'首页':scenes[c].label)+'。';rail.forEach((r,i)=>{if(i===c)r.setAttribute('aria-current','location');else r.removeAttribute('aria-current');});}
    if(Math.abs(progress-lastUI)<.0001&&!dirty)return;
    lastUI=progress;
    let bg=scenes[a].bg.map((x,i)=>Math.round(mix(x,scenes[b].bg[i],m)*255));
    let ink=scenes[a].ink.map((x,i)=>Math.round(mix(x,scenes[b].ink[i],m)*255));
    if(scrollY>catalogueTop-innerHeight*.3){bg=[236,238,233];ink=[24,61,53];}
    const lb=luminance(bg),li=luminance(ink);
    if((Math.max(lb,li)+.05)/(Math.min(lb,li)+.05)<4.5) ink=lb>.179?[0,0,0]:[255,255,255];
    root.style.setProperty('--paper',`rgb(${bg})`);root.style.setProperty('--ink',`rgb(${ink})`);root.style.setProperty('--scene-ink',ink.join(','));
    root.style.setProperty('--halo',a===1||a===4?'.08':'.8');
    $('#journey-progress').style.transform=`scaleX(${.03+progress/7*.97})`;
    const envelope=Math.sin(m*Math.PI);
    $('#ambient-word').style.transform=`translate(${-15-envelope*12}%, -50%) scale(${1+envelope*.15})`;
  }
  function frame(now) {
    raf=0;if(document.hidden)return;
    const dt=previous?Math.min((now-previous)/1000,.05):.016;
    if(previous&&now-previous>38&&now-previous<250)slow++;else slow=Math.max(0,slow-1);
    if(slow>100&&quality>.65){quality-=.15;slow=0;resize();}
    previous=now;
    const moving=!paused&&!dialog.open&&scrollY<catalogueTop;
    if(moving){time+=dt;bloom*=Math.exp(-dt*1.8);}
    const ease=reduced.matches||staticView?1:1-Math.exp(-dt*10);
    progress=mix(progress,target,ease);if(Math.abs(progress-target)<.0001)progress=target;
    rotation=mix(rotation,targetRotation,ease);tilt=mix(tilt,targetTilt,ease);
    focusBlend=mix(focusBlend,watching?1:0,ease);
    const a=Math.floor(clamp(progress,0,7)),b=Math.min(a+1,7),m=progress-a;
    updateUI(a,b,m);
    if(glReady&&scrollY<catalogueTop+innerHeight)draw(a,b,m);
    dirty=false;
    if(moving||Math.abs(progress-target)>.0001||Math.abs(rotation-targetRotation)>.0001||Math.abs(tilt-targetTilt)>.0001||Math.abs(focusBlend-(watching?1:0))>.0001)raf=requestAnimationFrame(frame);
  }
  if(staticView)fallback();else initGL();setPaused(paused);resize();
})();
