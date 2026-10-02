# Ideas take shape

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
python scripts/validate_shape_profile.py
```

`scripts/refresh_public_data.py` 从 GitHub 的公开用户仓库接口获取元数据，可用 `GITHUB_TOKEN` 提高请求限额。失败时不会覆盖上一次成功的数据文件。数据包括公开仓库名、地址、主要语言、Star 和 Fork 数量，不读取私有仓库、事件或提交内容。

`Refresh Ideas take shape profile` 每日运行，也支持手动触发。刷新后只提交 `assets/shape/` 和 `data/public-profile.json`。展示的日期是成功获取快照的 UTC 日期。语言数量指各公开仓库主要语言的去重数，不代表完整技术栈。

旧版图形与生成脚本保留在 Git 历史和原路径中，旧版辅助工作流改为手动运行；新主页使用 `assets/shape/`。

## 字体

[Sora](https://github.com/google/fonts/tree/main/ofl/sora) 使用 SIL Open Font License。字体文件及许可证位于 `assets/fonts/Sora.ttf` 和 `assets/fonts/Sora-OFL.txt`。旧版 Orbitron 字体及其许可证保留。
