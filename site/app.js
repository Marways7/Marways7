(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  const panels = [...document.querySelectorAll('.project-panel')];
  const stage = document.querySelector('.scene-stage');
  const status = document.querySelector('.scene-status');
  const demoStatus = document.querySelector('.demo-status');
  const motionButton = document.querySelector('.motion-toggle');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const staticMode = new URLSearchParams(location.search).get('view') === 'static';
  const oldRoutes = {heartbeat:'ecg',conversation:'ailiao',reading:'read',action:'desktop',momentum:'sprint',connection:'campus'};
  let active = 0;
  let targetScene = 0;
  let paused = reduced.matches || staticMode;
  let sceneGhost = null;
  let sceneTimer = null;
  let userMotionChoice = false;
  const demoTimers = new Map();

  function applyMotion() {
    root.classList.toggle('paused', paused);
    root.classList.toggle('motion-on', !paused);
    root.classList.toggle('static-mode', staticMode);
    motionButton.hidden = staticMode;
    motionButton.setAttribute('aria-pressed', String(paused));
    motionButton.querySelector('.motion-label').textContent = paused ? '开启动效' : '暂停动态';
    motionButton.querySelector('[aria-hidden]').textContent = paused ? '▷' : 'Ⅱ';
    motionButton.setAttribute('aria-label', paused ? '开启动效' : '暂停动态');
    if (paused) clearSceneAnimation();
    if (paused) demoTimers.forEach(timer => clearTimeout(timer));
    if (staticMode) {
      const staticLink = document.querySelector('.footer-bottom a');
      staticLink.href = './';
      staticLink.textContent = '返回动态浏览';
    }
  }
  applyMotion();
  motionButton.addEventListener('click', () => { userMotionChoice = true; paused = !paused; applyMotion(); });
  reduced.addEventListener('change', () => { if (!userMotionChoice) { paused = reduced.matches || staticMode; applyMotion(); } });

  function updateScene(index) {
    active = (index + panels.length) % panels.length;
    panels.forEach((panel,i) => {
      panel.hidden = i !== active;
      panel.classList.remove('scene-enter', 'demo-active');
      clearTimeout(demoTimers.get(panel));
      panel.querySelector('.demo-button').setAttribute('aria-pressed','false');
      if(panel.id === 'panel-read'){panel.querySelector('.reading-line-one').textContent='换个角度';panel.querySelector('.reading-line-two').textContent='理解这一页。';}
    });
    tabs.forEach((tab,i) => {
      tab.setAttribute('aria-selected',String(i === active));
      tab.tabIndex = i === active ? 0 : -1;
    });
    status.textContent = '正在探索：' + panels[active].querySelector('.project-name').textContent;
    document.querySelector('.scene-back').style.background = panels[active].style.getPropertyValue('--scene');
  }

  function clearSceneAnimation() {
    clearTimeout(sceneTimer);
    if (sceneGhost) { sceneGhost.remove(); sceneGhost = null; }
    panels.forEach(panel => panel.classList.remove('scene-enter'));
  }

  function showScene(index, options = {}) {
    index = (index + panels.length) % panels.length;
    targetScene = index;
    clearSceneAnimation();
    if (options.route !== false) history.replaceState(null, '', '#' + tabs[index].dataset.project);
    if (options.focus) tabs[index].focus({preventScroll:true});
    if (index === active) return;
    const animate = !paused && !options.instant;
    if (animate) {
      sceneGhost = panels[active].cloneNode(true);
      sceneGhost.className = 'scene-ghost';
      sceneGhost.removeAttribute('id');
      sceneGhost.removeAttribute('role');
      sceneGhost.removeAttribute('aria-labelledby');
      sceneGhost.removeAttribute('tabindex');
      sceneGhost.setAttribute('aria-hidden','true');
      sceneGhost.setAttribute('inert','');
      sceneGhost.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
      sceneGhost.style.height = panels[active].getBoundingClientRect().height + 'px';
    }
    // Commit the selection synchronously; decorative animation never owns state.
    updateScene(index);
    if (options.focus) tabs[index].focus({preventScroll:true});
    if (animate) {
      stage.append(sceneGhost);
      panels[index].classList.add('scene-enter');
      sceneTimer = setTimeout(clearSceneAnimation,680);
    }
  }

  tabs.forEach((tab,i) => {
    tab.addEventListener('click', () => showScene(i));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = i + 1;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = i - 1;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      showScene(next,{focus:true});
    });
  });
  document.querySelector('.scene-prev').addEventListener('click', () => showScene(targetScene - 1));
  document.querySelector('.scene-next').addEventListener('click', () => showScene(targetScene + 1));

  function routeScene(hash, scroll = true) {
    const id = oldRoutes[hash] || hash;
    const index = tabs.findIndex(tab => tab.dataset.project === id);
    if (index < 0) return;
    showScene(index, {instant:true,route:false});
    if (scroll) document.querySelector('#work').scrollIntoView({behavior:paused?'instant':'smooth',block:'start'});
  }
  document.querySelectorAll('.hotspot').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    history.pushState(null,'',link.hash);
    routeScene(link.hash.slice(1));
  }));
  window.addEventListener('hashchange', () => routeScene(location.hash.slice(1)));
  routeScene(location.hash.slice(1));

  const demoMessages = {
    ecg:['信号描绘中：观察波形与特征。','信号图解已复位。'],
    ailiao:['对话、工具与信息已连接。','连接图解已复位。'],
    read:['这一页已标记，试着换个角度理解。','书页标记已复位。'],
    desktop:['正在播放任务、操作、观察的概念演示。','操作演示已复位。'],
    sprint:['正在回放示意时间线。','示意回放已复位。'],
    campus:['发现、整理、收藏与分享已连接。','知识连接已复位。']
  };
  panels.forEach(panel => {
    const button = panel.querySelector('.demo-button');
    button.setAttribute('aria-pressed','false');
    button.addEventListener('click', () => {
      clearTimeout(demoTimers.get(panel));
      const enabled = panel.classList.toggle('demo-active');
      if (button.dataset.demo === 'ecg') {
        const wave = panel.querySelector('.signal-shape');
        if (!panel.dataset.originalWave) panel.dataset.originalWave = wave.getAttribute('d');
        const alternative = 'M105 224H145L158 206L172 224H214L227 190L239 259L256 160L273 224H334L345 210L355 224H385L399 174L412 260L430 146L447 224H522';
        const next = wave.getAttribute('d') === alternative ? panel.dataset.originalWave : alternative;
        wave.setAttribute('d',next);
        panel.querySelector('.trace').setAttribute('d',next);
      }
      if (button.dataset.demo === 'read') {
        panel.querySelector('.reading-line-one').textContent = enabled ? '抓住重点' : '换个角度';
        panel.querySelector('.reading-line-two').textContent = enabled ? '再读一遍。' : '理解这一页。';
      }
      button.setAttribute('aria-pressed',String(enabled));
      demoStatus.textContent = demoMessages[button.dataset.demo][enabled?0:1];
      if (enabled && !paused) demoTimers.set(panel,setTimeout(() => {
        panel.classList.remove('demo-active');
        if(button.dataset.demo === 'read'){panel.querySelector('.reading-line-one').textContent='换个角度';panel.querySelector('.reading-line-two').textContent='理解这一页。';}
        button.setAttribute('aria-pressed','false');
      },4500));
    });
  });

  // Small pointer-linked depth; native scrolling and touch gestures stay unchanged.
  const world = document.querySelector('.hero-world');
  const machine = document.querySelector('.machine-wrap');
  world.addEventListener('pointermove', event => {
    if (paused || event.pointerType !== 'mouse') return;
    const bounds = world.getBoundingClientRect();
    machine.style.setProperty('--rx', ((.5 - (event.clientY - bounds.top)/bounds.height)*5).toFixed(2)+'deg');
    machine.style.setProperty('--ry', (((event.clientX - bounds.left)/bounds.width - .5)*7).toFixed(2)+'deg');
  });
  world.addEventListener('pointerleave', () => { machine.style.setProperty('--rx','0deg');machine.style.setProperty('--ry','0deg'); });
  document.addEventListener('visibilitychange', () => root.classList.toggle('page-hidden',document.hidden));
})();
