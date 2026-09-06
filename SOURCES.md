# SOURCES

deai 把下述项目的**方法**（规则、判断依据、门禁框架）重写整合成一套带 A/B/C 等级的单一流程。本仓库不含上游代码副本，规则文本为原创重写，但在方法与思路上受以下项目启发：

| 来源 | 仓库 | 许可 | deai 用了它的什么 |
|---|---|---|---|
| human-writing | [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing) | 见上游 | 词句禁令、材料门槛、改稿七遍（段落删剪层骨架） |
| lieflat（less-ai-tone） | 作者 shiujan（本地参考实现） | MIT | 句级触发标记、反误伤表、信息守恒硬边界 |
| sepia | [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | MIT | 叙事架构七组诊断（`architecture.md` 的源）、校准哲学（挑 3-5 动作、留白、不反转 AI 特征）、破折号按模型浮动的证据 |
| oh-story claudecode | [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode) | MIT | 网文门禁 A-G、禁词量化表、过度清理保护与退化检查（`gates.md` 网文特化部分的源） |

人类带复算方法参考：`style-stats`（自研句式统计工具，未开源，思路见 `references/calibration.md` 0.8）。

## 版权说明

- 各上游保留各自版权与许可。
- 本仓库新增内容与整合编排：Copyright (c) 2026 wei125775-lab，MIT。
