#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deai 去AI味 · 词句清零脚本（链路第 4 步的机器部分）。

只做【字面可定位】的 A 级子集：
  FAIL   —— 标点（破折号/省略号/提示冒号）、硬黑话、网文一级模板词
  REMIND —— 语境词、弱化副词密度、抒情词、总结/升华壳
语义级 A 项（翻案腔动作变体、假深刻、注水、相邻句同构）靠 references/passes.md
与 gates.md 人工判，不算脚本漏检。

词表与 references/hard-bans.md 同源。改词表必须同步本文件版本号。
版本: 1 (deai 0.1.0)

用法: python3 check_deai.py <稿件文件...>    # 无参数时从 stdin 读
"""

import re
import sys

try:  # 跨终端统一 UTF-8 输出，避免 Windows GBK 控制台乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VER = "1"

# ---------- FAIL 词表（与 hard-bans.md 4.2 / 4.4 同步） ----------

# 4.2 硬黑话（绝对）
HARD_HUA = [
    "赋能", "抓手", "商业闭环", "价值闭环", "能力沉淀", "拉通", "底层逻辑",
    "顶层设计", "认知跃迁", "价值释放", "能力建设", "降本增效", "内容矩阵",
    "全链路", "组合拳", "打开想象空间", "结构性机会", "关键命题", "深层逻辑",
    "技术底座", "公共底座", "技术主权", "单点风险", "材料锚点", "认知增量",
    "迭代闭环", "颗粒度", "生态位", "方法论", "范式",
]

# 4.4 网文一级模板词（出现即处理）
WEBNOBEL_T1 = [
    # 情态
    "仿佛", "犹如", "宛若", "如同", "一丝", "一抹", "些许", "几分", "隐约",
    "毫无征兆", "几不可闻", "微不可察",
    # 动作
    "深吸一口气", "不禁",
    # 表情
    "眼中闪过", "嘴角勾起", "眉头微皱", "眉眼低垂", "瞳孔微缩", "瞳孔收缩",
    "瞳孔一缩", "指节泛白", "眼神锐利", "目光锐利",
    # 心理
    "心中一动", "心头一震", "心下了然", "心中暗道", "心底泛起", "不由得", "心中一凛",
    # 判断
    "不容置疑", "不容置喙", "不易察觉", "显而易见", "毫无疑问", "不可否认", "前所未有",
    # 形容
    "闪烁", "狡黠", "深邃", "凛冽", "冰冷",
    # 过渡
    "不由自主", "情不自禁", "自然而然", "话锋一转",
]

# ---------- REMIND 词表 ----------

# 4.3 语境词
CONTEXT_WORDS = [
    "沉淀", "对齐", "协同", "链路", "心智", "核心变量", "打法", "想象空间",
    "闭环", "不丢",
]

# 4.5 弱化副词（密度：每千字合计 ≤3）
SOFT_ADV = ["缓缓", "微微", "轻轻", "淡淡"]

# 4.6 抒情装腔词
LYRIC_WORDS = [
    "安放", "抵达", "微光", "褶皱", "丰盈", "滚烫", "轻盈", "赤裸", "剥开",
    "锋利", "坚硬", "柔软", "勇敢", "温柔",
]

# 4.7 总结/升华壳
SUMMARY_SHELLS = [
    "这一刻", "他终于明白", "她终于明白", "他终于知道", "她终于知道",
    "这才意识到", "从这一刻开始", "才刚刚开始", "他不知道的是", "她不知道的是",
    "命运的齿轮", "命运的棋局", "命运的獠牙",
]

# 4.1 标点
DASH = re.compile(r"[—–]{1,2}|--")
ELLIPSIS = re.compile(r"…+|\.\.\.+")
PROMPT_COLON = re.compile(r"(?P<pre>[^：:]{0,8})[：:]")

PROMPT_HINT = (
    "总结|一句话|核心|关键|重点|本质上|本质|结论|说白了|真相是|原因|如下|"
    "要点|含义|意思是|答案是|答案是"
)
QUOTE_VERB = "说|道|问|答|喊|嚷|叫|应|回|想|念|写|叹|骂|夸|劝|求|威胁|提醒"

DUN_HAO_CHAIN = re.compile(r"[^。！？；\n，、]{0,12}[、][^、。！？；\n，]{1,8}[、]")
"""
简化判断句内顿号二连（三项并列的近似）。不精确，只提醒。
"""


def scan(text):
    fails = []
    reminds = []

    def report(bucket, item, pos):
        line = text[:pos].count("\n") + 1
        snippet = text[max(0, pos - 20): pos + 12].replace("\n", " ")
        bucket.append(f"  行 {line:<4} {item:<10} 「{snippet}」")

    # --- 标点 ---
    for m in DASH.finditer(text):
        report(fails, "破折号", m.start())
    for m in ELLIPSIS.finditer(text):
        report(fails, "省略号", m.start())
    for m in PROMPT_COLON.finditer(text):
        pre = m.group("pre")
        if re.search(PROMPT_HINT, pre):
            report(fails, "提示冒号", m.start())

    # --- 词 ---
    for w in HARD_HUA:
        for m in re.finditer(re.escape(w), text):
            report(fails, f"黑话:{w}", m.start())
    for w in WEBNOBEL_T1:
        for m in re.finditer(re.escape(w), text):
            report(fails, f"模板:{w}", m.start())
    for w in CONTEXT_WORDS:
        for m in re.finditer(re.escape(w), text):
            report(reminds, f"语境:{w}", m.start())
    for w in LYRIC_WORDS:
        for m in re.finditer(re.escape(w), text):
            report(reminds, f"抒情:{w}", m.start())
    for w in SUMMARY_SHELLS:
        for m in re.finditer(re.escape(w), text):
            report(reminds, f"总结壳:{w}", m.start())

    # 弱化副词密度
    chars = len(re.sub(r"\s", "", text))
    n_soft = sum(len(re.findall(w, text)) for w in SOFT_ADV)
    k_words = chars / 1000.0
    if k_words >= 0.3 and n_soft / max(k_words, 0.01) > 3:
        reminds.append(f"  [密度] 弱化副词 {n_soft} 处 / {chars}字，"
                       f"折 {n_soft/max(k_words,0.01):.1f}/千字 > 3，成串出现才处理")

    for m in DUN_HAO_CHAIN.finditer(text):
        report(reminds, "顿号二连?", m.start())

    return fails, reminds


def read_bytes_auto(b):
    """先按 UTF-8 解，失败再退回 GBK，覆盖 Windows 控制台两种输入。"""
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("gbk", errors="replace")


def main():
    if sys.argv[1:]:
        texts = []
        for p in sys.argv[1:]:
            with open(p, encoding="utf-8") as f:
                texts.append((p, f.read()))
    else:
        texts = [("<stdin>", read_bytes_auto(sys.stdin.buffer.read()))]

    total_fail = 0
    for name, text in texts:
        fails, reminds = scan(text)
        total_fail += len(fails)
        print(f"== {name} (词表 v{VER}) ==")
        if fails:
            print(f"  FAIL  {len(fails)} 处 —— 字面 A 级，需清零：")
            print("\n".join(fails))
        if reminds:
            print(f"  REMIND {len(reminds)} 处 —— 语境/B 级，人定：")
            print("\n".join(reminds))
        if not fails and not reminds:
            print("  干净：无字面 A 级命中，无提醒项。")
        print()

    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
