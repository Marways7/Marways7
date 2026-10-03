# Marways — 把好奇，变成作品。

[个人主页](https://marways7.github.io/Marways7/) 将个人介绍和六个项目连接成一段可往返浏览的体验。首屏、项目与关于我共享一件连续变形的参数化形态，颜色、光线和形态随内容变化。详细的视觉取舍见 [设计说明](LIVING-ATLAS.md)。

## 交互

- 原生滚动控制场景变化，可以随时反向；右侧导航和作品索引可直接跳转。
- 拖动形态或旋转按钮改变角度；旋转按钮支持方向键，空格展开。
- “绽放”展开形态；暂停时再次点击收束。动态模式下会缓慢回归。
- “暂停动态”停止呼吸与自动运动，保留手动操作和导航。
- “纯粹观看”隐藏正文，保留返回按钮与章节导航；Escape 返回介绍。
- 项目入口始终使用普通链接，包括 Desktop Operator 的 MCP 与 CLI 两个仓库。

## 实现

`site/` 是无需构建的静态网站。一个 WebGL 画布绘制七种共享拓扑的曲面，使用预计算顶点与法线进行连续插值。原生滚动不被劫持；页面未设置强制加载动画、鼠标替代光标或声音自动播放。

Sora 字体随站点提供。网站没有外部运行时库、分析脚本或访客追踪。图形尺寸根据窗口调整，限制像素比；持续长帧时降低渲染分辨率，标签页隐藏后暂停绘制。实际流畅度取决于设备与浏览器。

减少动态设置默认暂停自动运动并直接切换场景；访客仍可主动开启动态。没有 WebGL 时显示静态插图并保留文字与项目链接。没有 JavaScript 时按普通文档阅读。

```sh
python -m http.server 8000 --directory site
```

## GitHub 介绍页

README 使用自包含 SVG。英文标题在生成时转为路径，中文保留系统字体。首图、六个项目和静态阅读页都有手机排版。动画遵循减少动态偏好，另有明确的静态首图。

完整互动通过首图或“进入互动主页”链接进入。项目图片外层的链接指向各仓库；不依赖图片内部交互。旧版生成器与资源保留，当前 README 使用 `living-` 系列资源。

```sh
python -m pip install -r requirements-profile.txt
python scripts/build_shape_profile.py
python scripts/build_cinema_profile.py
python scripts/build_living_profile.py
python scripts/validate_shape_profile.py
node --check site/app.js
```

## 公开数据与发布

`refresh_public_data.py` 读取 GitHub 公开仓库元数据。失败时保留上次成功的数据；不获取私有仓库或提交内容。每日刷新工作流生成图像与公开快照。统计说明、日期和来源随数据展示，默认收在 README 的展开区域。

GitHub Pages 工作流仅发布 `site/` 目录。字体使用 SIL Open Font License，许可证与字体位于同一目录；原始字体见 [Sora](https://github.com/google/fonts/tree/main/ofl/sora)。
