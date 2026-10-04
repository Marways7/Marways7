# Marways — 好奇心，正在运行。

[互动主页](https://marways7.github.io/Marways7/) 是一个围绕真实项目的创意工作台。首页的立体装置连接书页、信号、电脑与光标；六个作品使用各自的概念图解。设计说明见 [PLAYGROUND.md](PLAYGROUND.md)。

## 浏览与交互

选择项目标签，或点击首页的项目入口。作品切换会同时更新图解、背景、介绍、探索路径和仓库链接。标签支持方向键、Home 和 End。每个场景提供一个小型概念演示；它们不接入实际项目服务。

暂停按钮停止自动动态和场景转场。减少动态偏好默认暂停，静态模式可从页脚进入。无 JavaScript 时，六个项目以连续内容展示，目录链接仍然可用。页面保持原生滚动，不锁定滚轮，也不劫持触摸手势。

## 实现

网站为原生 HTML、CSS 和 JavaScript，无外部运行时依赖。Sora 字体与图像保存在仓库内。作品图解使用可访问的 SVG，标题和项目介绍保持原生文本。作品选择同步生效，局部 CSS 转场只负责呈现；连续点击会结束前一段动画，立即呈现最后的选择。标签页隐藏后暂停装饰动画。

```sh
python -m pip install -r requirements-profile.txt
python scripts/build_playground_profile.py
python scripts/validate_shape_profile.py
node --check site/app.js
python -m http.server 8000 --directory site
```

页面模板是 `scripts/templates/playground.html`；项目内容和图解生成器是 `scripts/build_playground_profile.py`。修改后重新生成 `site/index.html` 并一并提交。

## GitHub 介绍页

README 使用专属封面、动态 SVG 图解、原生文字与项目链接。宽屏采用跨栏和双图编排，手机为封面、重点项目和工具箱提供单独构图。图片外层使用原生链接，点击后进入对应仓库或主页。减少动态时选用静态 SVG。

封面从 `site/profile-cover.html` 渲染，桌面为 1200 × 610，手机为 640 × 820。它们是固定设计资产，不由每日数据任务重新截图。主视觉生成提示保存在 [IMAGE-PROMPT.md](IMAGE-PROMPT.md)。

## 自动更新

每日工作流更新公开仓库元数据并验证本地 SVG。旧版本图形保留供历史设计参考，当前 README 使用 `assets/play/`，公开快照继续使用 `assets/shape/pulse.svg`。网站通过 GitHub Pages 工作流发布 `site/` 目录。

字体使用 SIL Open Font License，许可与字体文件保存在相同目录。没有追踪脚本或私有数据依赖。
