# deai · 去 AI 味总刀

> De-AI writing for Chinese text. A self-contained Agent Skill that strips AI flavor from web-novel prose, fiction, articles and titles — at the layer that actually gives AI away, not just word choice.

把"像 AI 写的"中文改成人写的。覆盖网文/小说正文、知乎回答、公众号、评论、标题。**自包含**：一个目录即一个 Agent Skill（仓库根是标准 SKILL.md），无运行时依赖。

它不是又一摞禁令，而是一条**纵深链 + 一套仲裁**：四家去 AI 味方法的规则被重写整合成一套带等级的单一流程，规则冲突按等级裁，避免各家规则互相打脸。

## 为什么跟别的去 AI 味工具不同

- **抓结构，不只抓词句。** AI 味最深藏在叙事架构（主题被角色亲口点破、每章恰好圆满、情绪全靠身体渲染、配角全对主角有好感），句子只是表层。结构层只在你授权"重构"时动刀，否则只标注。
- **分档操作。** 清理（只清语言、剧情一字不动，默认）／重构（允许动结构骨架）／检测（只报告不改）／新写。
- **反误伤。** 一条明确的 C 级禁动表：看着像 AI 味但实测站不住的东西（句长离散度、被动句、句内排比、问句、比喻本身），以及网文行业规范（强因果、伏笔全回收、主角主动），一律不碰。
- **校准哲学：对准人类带，不是反转 AI 特征。** 每条规则都上满会造出新的指纹；架构层每篇只挑 2–5 个动作，句级命中即改但保持最小改动。

## 安装

仓库根是标准 Agent Skill（`SKILL.md` + `references/` + `scripts/`）。

- **手动复制（任意 agent）**：把整个目录复制到你的 skills 目录，如 `~/.claude/skills/deai/`。
- **Skills CLI（77+ 个 agent）**：`npx skills add wei125775-lab/deai`

装好后，对任意文本说「帮我去了 AI 味」「这段太 AI 了」「重写这段」即触发。不支持触发词时，显式问它「用 deai 处理这段」。

## 用法：四档

| 档 | 说 | 行为 |
|---|---|---|
| **清理**（默认） | 「帮我去了 AI 味」 | 只清语言层，剧情结构一字不动；结构症状照标照提醒但不动刀 |
| **重构** | 「结构也能变」 | 允许动结构骨架；先给诊断报告 + 手术清单，授权后动刀 |
| **检测** | 「查下有没有 AI 味」 | 只报告，不改文 |
| **新写** | 「用去 AI 味的写法写」 | 从零写，落点即去 AI 味 |

## 怎么工作：纵深五步

| 步 | 层 | 读 | 档 |
|---|---|---|---|
| 0 | 预检：材料/信息守恒、说话位置、网文别误伤 | `references/calibration.md` | 全部 |
| 1 | 架构（虚构）：结构诊断，挑 2-5 个动作 | `references/architecture.md` | 重构/新写 |
| 2 | 段落删剪：假深刻/注水/结尾早一拍 | `references/passes.md` | 清理+重构 |
| 3 | 句级门禁：A-G 触发标记，最小改动 | `references/gates.md` | 清理+重构 |
| 4 | 清零：硬禁词+标点，跑脚本量化 | `references/hard-bans.md` + `scripts/check_deai.py` | 清理+重构 |
| 5 | 冷读：忘掉规则重读，抓"像模型完成任务"的段 | `references/passes.md` 末节 | 改稿类 |

顺序铁律：先结构后词句，删除/重排优先于改写，脚本最后。结构有缺陷时只做句级修改，AI 味反而更显。

## 规则分级（仲裁层）

| 级 | 含义 | 动作 |
|---|---|---|
| **A 硬信号** | 多源独立一致或实测稳定 | 命中必须改 |
| **B 软信号** | 单源/需语境/分模型/作者风格 | 标出，由作者定，不擅动 |
| **C 禁动** | 实测站不住或网文行业规范/作者风格 | 一律不碰 |

优先级：**作者风格文档 ＞ C 禁动 ＞ A 硬改 ＞ B 软判**。例如破折号在不同后端模型上量级差 10 倍，等级按执行模型浮动（见 `references/calibration.md` 0.7）。

## 词表与脚本

`references/hard-bans.md` 与 `scripts/check_deai.py` 同源（词表版本号互锁，改一处必须同步另一处）。

```bash
# 文件模式
python3 scripts/check_deai.py 稿件.md

# 或管道
echo '你的文字' | python3 scripts/check_deai.py
```

脚本只检**字面可定位**的 A 级子集（标点/黑话/网文模板词 → FAIL；语境词/弱化副词密度/总结壳 → REMIND）。语义级（翻案腔动作变体、假深刻、注水、相邻句同构）靠人工层判，不算脚本漏检。

## 测试

```bash
python3 scripts/check_deai.py test/01-ai-prose.md test/02-ai-webnovel.md   # 应报 FAIL
```

`test/` 下三个样例（AI 腔正文、AI 味网文章节、标题批）带预期标注，可作为验收基准。

## 来源与许可

四家上游方法被重写整合（非代码副本），明细见 [SOURCES.md](SOURCES.md)。本仓库 MIT。

## 已知边界（诚实标注）

`references/calibration.md` 0.8 节列出的"网文人类带"数值，部分来自英文文学语料或单源推断——**方向可用，绝对值待中文语料复算**。复算方法在该节说明。文档本身不假装有它没有的数据。
