# Curiosity, in motion

第二版将主页分为两个相连的展示界面：GitHub README 展示可自动变形的封面和整块可点击的作品图；[交互展厅](https://marways7.github.io/Marways7/) 提供可拖动的立体雕塑、形态切换、粒子扩散和项目浏览。

## 交互展厅

源码位于 `site/`，无需打包工具和外部运行时依赖。使用自托管 Sora 字体、自定义 WebGL 材质与几何、Canvas 作品图形。数字 7、折叠轨道和流动信号共用顶点结构，切换时连续插值。拖动和方向键调整视角，空格或按钮暂停动态。

支持 `prefers-reduced-motion`，后台标签页停止刷新，无 WebGL 时展示静态备用图。作品导航支持鼠标、触摸、方向键和 Home/End。所有外链保持原生链接行为。页面不收集访客数据，也不加载追踪脚本。

`Deploy interactive exhibition` 将 `site/` 目录发布至 GitHub Pages。README 本身不会运行 WebGL 或 JavaScript；完整交互通过封面链接进入。作品链接由 README 中包在图片外的 `<a>` 提供，不依赖图片内部链接。

```sh
python -m http.server 8000 --directory site
```

打开本地地址即可预览。字体授权随网站源文件附带。

## 第一版视觉基础

Marways 的 GitHub 主页围绕一个视觉动作展开：一束光线弯折成数字 **7**，再延伸为各个项目的图形。心电波形、书页、对话框、指针、信号线和知识层叠，对应六个真实的探索方向。

## 视觉与内容

- 深海蓝 `#081C2C`、冰白 `#EDF7FA`、钴蓝 `#527CFF`、珊瑚色 `#FFAA8A`、水绿色 `#93E5DD`。
- Sora 英文标题在构建时转成路径。中文短句使用系统字体，正文保留可选择、可复制的 Markdown。
- 桌面与手机分别构图；`picture` 根据浏览器视口选择资源。
- 主视觉使用缓慢的呼吸与流光，遵循 `prefers-reduced-motion`；另提供显式的[静态版本](STATIC.md)。
- 项目介绍以公开仓库为依据，不用装饰性百分比描述能力或时间投入。
- 所有展示图片都保存在本仓库，无外部统计图片服务、追踪像素或运行时字体请求。

## 本地构建

```sh
python -m pip install -r requirements-profile.txt
python scripts/build_shape_profile.py
python scripts/build_cinema_profile.py
python scripts/validate_shape_profile.py
```

`scripts/refresh_public_data.py` 从 GitHub 的公开用户仓库接口获取元数据，可用 `GITHUB_TOKEN` 提高请求限额。失败时不会覆盖上一次成功的数据文件。数据包括公开仓库名、地址、主要语言、Star 和 Fork 数量，不读取私有仓库、事件或提交内容。

`Refresh Ideas take shape profile` 每日运行，也支持手动触发。刷新后只提交 `assets/shape/` 和 `data/public-profile.json`。展示的日期是成功获取快照的 UTC 日期。语言数量指各公开仓库主要语言的去重数，不代表完整技术栈。

旧版图形与生成脚本保留在 Git 历史和原路径中，旧版辅助工作流改为手动运行；新主页使用 `assets/shape/`。

## 字体

[Sora](https://github.com/google/fonts/tree/main/ofl/sora) 使用 SIL Open Font License。字体文件及许可证位于 `assets/fonts/Sora.ttf` 和 `assets/fonts/Sora-OFL.txt`。旧版 Orbitron 字体及其许可证保留。
