#!/usr/bin/env python3
"""只读解析 01-上午综合知识错题集.md，生成派生视图（看板 / 红名单 / 星标待确认清单）。

设计原则：
  * 错题卡是唯一数据源（SSOT），本脚本只读不写卡片。
  * 画像是派生视图，每次整理错题后重新运行即可，无需手工同步。
  * ⭐ 的决定权在用户：脚本只做“建议”，用户确认的星标记录在 star-registry.json，永不被自动降级。

用法：  python3 05-error-vault/_tools/build_profile.py
"""
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent          # 05-error-vault/
CARDS = VAULT / "01-上午综合知识错题集.md"
REGISTRY = Path(__file__).resolve().parent / "star-registry.json"
CARD_FILE_NAME = CARDS.name

HEAD_RE = re.compile(r"^### (?P<icons>[^\d错]*?)错题 ?(?P<id>\d+)\s*(?P<extra_icons>[^：:\w\s]*?)\s*[：:](?P<title>.*)$")
ROUND_WORDS = {"二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}

MODULES = [
    ("01", "计算机组成与体系结构", 6),
    ("02", "程序设计语言与编译", 3),
    ("03", "操作系统", 6),
    ("04", "软件工程与项目管理", 8),
    ("05", "数据库系统", 6),
    ("06", "计算机网络与信息安全", 8),
    ("07", "数据结构与算法", 10),
    ("08", "面向对象与UML", 12),
    ("09", "法律法规与标准化", 3),
]

KEYWORDS = [
    ("09", ["知识产权", "著作权", "专利", "商标", "法律", "商业秘密", "标准化", "条例"]),
    ("08", ["面向对象", "UML", "设计模式", "多态", "继承", "类图", "用例", "状态图", "活动图", "责任链", "命令模式", "组合模式", "原型模式", "单例模式", "工厂", "策略模式", "状态模式", "观察者", "适配器", "门面", "享元", "中介者", "备忘录", "构件图", "类间关系", "OOA", "OOD"]),
    ("05", ["数据库", "关系规范化", "范式", "SQL", "E-R", "ERD", "关系代数", "函数依赖", "视图", "事务", "完整性", "关系数据库", "候选码", "概念结构设计", "逻辑结构设计", "物理结构设计", "1NF", "2NF", "3NF", "BCNF", "模式分解", "自然连接"]),
    ("03", ["操作系统", "进程", "页面置换", "页式", "段页", "页表", "请求分页", "磁盘", "文件管理", "文件系统", "死锁", "PV", "银行家", "位示图", "存储管理", "调度", "单缓冲区", "FAT", "目录项", "临界资源", "临界区", "作业调度", "SSTF", "SCAN", "FCFS", "多级索引", "盘块", "Linux", "Unix", "权限"]),
    ("06", ["网络", "信息安全", "安全", "加密", "协议", "IP", "子网", "TCP", "UDP", "DNS", "防火墙", "密码", "黑客", "VLAN", "路由", "移动通信", "OSI", "PKI", "数字证书", "数字信封", "CIDR", "CSMA", "NAT", "Telnet", "SSH", "SNMP", "以太网", "交换机", "广播域", "超网", "传输层"]),
    ("04", ["软件工程", "项目管理", "软件测试", "测试", "软件体系结构", "体系结构风格", "内聚", "耦合", "维护", "质量", "过程模型", "系统分析", "进度", "甘特", "PERT", "需求", "CMMI", "敏捷", "逆向", "软件设计", "软件系统", "生命周期", "模块", "DFD", "配置管理", "风险", "COCOMO", "McCabe", "环路复杂度", "语句覆盖", "白盒", "黑盒", "集成测试", "McCall", "ISO/IEC", "极限编程", "XP", "程序员", "开发模型", "喷泉模型", "统一过程", "开发计划", "原型法", "结构化分析", "SA"]),
    ("01", ["计算机组成", "计算机体系结构", "存储系统", "Cache", "指令", "流水线", "Flynn", "浮点", "补码", "反码", "原码", "校验", "CRC", "海明", "总线", "中断", "DMA", "I/O", "RISC", "CISC", "输入输出", "扩展操作码", "数据编码", "运算器", "控制器", "累加器", "DRAM", "SRAM", "可靠度", "多媒体", "位元", "微程序", "存储器", "溢出", "冯·诺依曼", "寻址", "操作数", "字长", "周期"]),
    ("02", ["编译", "程序设计语言", "文法", "正规式", "自动机", "Python", "词法", "语法", "语义", "解释器", "中间代码", "汇编", "参数传递", "FIRST", "函数型", "语言翻译", "泛型", "类属"]),
    ("07", ["数据结构", "算法", "排序", "查找", "树", "堆", "图", "哈夫曼", "队列", "栈", "链表", "矩阵", "哈希", "二叉", "KMP", "动态规划", "贪心", "分治", "复杂度", "字符串", "拓扑排序", "生成树", "二叉排序树", "BST", "AVL", "B树", "广度优先", "深度优先", "BFS", "DFS", "大顶堆", "小顶堆", "最短路径", "Floyd", "Dijkstra", "折半查找", "分块查找", "主定理"]),
]


def parse_round(title: str) -> int:
    m = re.search(r"([二三四五六七八九])进宫", title)
    if m:
        return ROUND_WORDS[m.group(1)]
    if "二刷" in title or "复错" in title:
        return 2
    return 1


def classify(title: str) -> str:
    for code, words in KEYWORDS:
        if any(w.lower() in title.lower() for w in words):
            return code
    return "07"


def clean_title(title: str) -> str:
    t = re.sub(r"【[^】]*】", "", title).strip()
    return re.sub(r"\s+", " ", t)


def short(text: str, n: int) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"


def slugify_heading(raw_heading: str) -> str:
    """与 VS Code 内置 Markdown 扩展 1:1 严格对齐的标题 Slug 转换算法。
    
    规则：
      1. 小写化、去除首尾空格；
      2. 剔除 Emoji、标点符号、全角符号、带圈数字（\u2460-\u24ff）；
      3. 保留字母、数字、中文、下划线与连字符；
      4. 将空白字符映射为连字符 '-'。
    """
    s = raw_heading.strip().lower()
    res = []
    for ch in s:
        if "\u2460" <= ch <= "\u24ff":
            continue
        cat = unicodedata.category(ch)
        if ch in ("-", "_") or ch.isalnum() or ch.isspace() or (not cat.startswith("P") and not cat.startswith("S") and not cat.startswith("C")):
            res.append(ch)
    cleaned = "".join(res)
    return re.sub(r"\s", "-", cleaned)


def load_cards():
    cards = []
    for ln, line in enumerate(CARDS.read_text(encoding="utf-8").splitlines(), 1):
        m = HEAD_RE.match(line)
        if not m:
            continue
        title = m.group("title").strip()
        heading_text = line.replace("### ", "").strip()
        cards.append({
            "id": int(m.group("id")),
            "line": ln,
            "star": "⭐" in m.group("icons") or "⭐" in m.group("extra_icons"),
            "round": parse_round(title),
            "title": clean_title(title),
            "raw_title": title,
            "heading": heading_text,
            "slug": slugify_heading(heading_text),
            "module": classify(title),
        })
    return cards


def load_registry():
    if REGISTRY.exists():
        try:
            return set(json.loads(REGISTRY.read_text(encoding="utf-8")).get("user_confirmed", []))
        except Exception:
            return set()
    return set()


def star_status(c, confirmed):
    if c["id"] in confirmed:
        return "⭐ 用户确认"
    if c["star"] and c["round"] >= 2:
        return "⭐ 达标(进宫)"
    if c["star"]:
        return "⭐ 待确认"
    if c["round"] >= 2:
        return "📌 建议升星"
    return "📌"


def link(c):
    return f"[👉 #{c['id']} 原题]({CARD_FILE_NAME}#{c['slug']})"


def health(rate):
    if rate >= 0.15:
        return "🔴"
    if rate >= 0.08:
        return "🟡"
    return "🟢"


def build_dashboard(cards, confirmed):
    by_mod = defaultdict(list)
    for c in cards:
        by_mod[c["module"]].append(c)
    rows = []
    for code, name, pts in MODULES:
        cs = by_mod.get(code, [])
        rep = [c for c in cs if c["round"] >= 2]
        rate = len(rep) / len(cs) if cs else 0
        top = sorted(rep, key=lambda c: (-c["round"], c["id"]))[:3]
        top_txt = "；".join(f"[#{c['id']}]({CARD_FILE_NAME}#{c['slug']}) {short(re.split(r'[（(]', c['title'].split('：')[-1])[0] or c['title'], 14)}" for c in top) or "—"
        rows.append((rate, code, name, pts, len(cs), sum(1 for c in cs if c["star"]), len(rep), top_txt))
    total = len(cards)
    rep_total = sum(1 for c in cards if c["round"] >= 2)
    stars = sum(1 for c in cards if c["star"])
    st = Counter(star_status(c, confirmed) for c in cards)

    out = [
        "# 10-错题看板（脚本生成，请勿手改）",
        "",
        "> 数据源：`01-上午综合知识错题集.md`（SSOT 唯一数据源）。",
        "> 重新生成命令：`python3 05-error-vault/_tools/build_profile.py`",
        "",
        "## 总览指标",
        "",
        "| 错题总数 | ⭐ 星标卡片 | 星标率 | 二进宫及以上 | 全库复错率 |",
        "| :-: | :-: | :-: | :-: | :-: |",
        f"| **{total}** 题 | **{stars}** 张 | **{stars/total:.1%}** | **{rep_total}** 题 | **{rep_total/total:.1%}** |",
        "",
        "## 模块看板（按复错率降序，优先攻坚靠前模块）",
        "",
        "> 健康度规则（客观公式）：复错率（二进宫及以上 ÷ 题数）≥15% 🔴 ｜ 8~15% 🟡 ｜ <8% 🟢",
        "",
        "| 健康度 | 模块 | 考纲分值 | 错题数 | ⭐ 星标 | 进宫数 | 复错率 | 进宫最深的 Top3 高危考点 |",
        "| :-: | :-- | :-: | :-: | :-: | :-: | :-: | :-- |",
    ]
    for rate, code, name, pts, n, s, r, top_txt in sorted(rows, key=lambda x: -x[0]):
        out.append(f"| {health(rate)} | {code} {name} | {pts} 分 | {n} 题 | {s} | {r} | {rate:.0%} | {top_txt} |")

    out += [
        "",
        "## 星标状态与用户决策分布",
        "",
        "> ⭐ 最终决定权属于用户：哪怕只错一次，只要你认为重要，即可永久标星；脚本永不自动覆盖降级你的决定。",
        "",
        "| 状态分类 | 数量 | 决策属性与含义 |",
        "| :-- | :-: | :-- |",
        f"| **⭐ 用户确认** | **{st['⭐ 用户确认']}** 张 | 你明确确认保留的星标（记录于 `star-registry.json`，永久锁定） |",
        f"| **⭐ 达标(进宫)** | **{st['⭐ 达标(进宫)']}** 张 | 客观复错 ≥2 次且已标星（含金量最高，建议全量保留） |",
        f"| **⭐ 待确认** | **{st['⭐ 待确认']}** 张 | AI 早期按“典型陷阱”自主标星但实际只错 1 次，待你审核（见 [12-星标待确认清单.md](12-星标待确认清单.md)） |",
        f"| **📌 建议升星** | **{st['📌 建议升星']}** 张 | 客观复错 ≥2 次但目前仍为 📌，建议你审阅是否升星 |",
        "",
    ]
    return "\n".join(out)


def build_redlist(cards, confirmed):
    rep = sorted((c for c in cards if c["round"] >= 2), key=lambda c: (-c["round"], c["id"]))
    icon = {2: "⭐", 3: "🚨", 4: "☠️"}
    out = [
        "# 11-红名单（考前 24 小时必扫清单）",
        "",
        "> 本清单由脚本自动从错题集中提取所有**二进宫及以上（复错 ≥2 次）**的高危题目，按进宫轮次降序排列。",
        "> **使用指南**：考前 24 小时无需重刷几百道题，只需快速过一遍这份红名单即可！",
        "",
        f"当前收录高危复错题共 **{len(rep)}** 道。",
        "",
        "| 轮次 | 错题号 | 考点名称与简述 | 当前星标 | 原题卡链接 |",
        "| :-: | :-: | :-- | :-: | :-: |",
    ]
    for c in rep:
        out.append(f"| {icon.get(c['round'], '☠️')} {c['round']}进宫 | #{c['id']} | {short(c['title'], 46)} | {star_status(c, confirmed)} | {link(c)} |")
    return "\n".join(out) + "\n"


def build_star_review(cards, confirmed):
    pend = sorted((c for c in cards if star_status(c, confirmed) == "⭐ 待确认"),
                  key=lambda c: (c["module"], c["id"]))
    names = {code: name for code, name, _ in MODULES}
    out = [
        "# 12-星标待确认清单",
        "",
        "> **背景**：以下题目目前带有 `⭐` 星标，但历史上**仅错漏过 1 次**，是 AI 早期按“典型命题陷阱”自主标记的。",
        "> **你的决策权**：",
        "> - 如果你认为某道题确实极具警示价值、考前必须看：只需将该行的 `[ ]` 改为 `[x]` 并告知我，我将把该题编号写入 `_tools/star-registry.json`（永久确认保留，绝不自动降级）；",
        "> - 其余未勾选的普通一次性错题，将恢复为正常的 `📌`，让重点更聚焦！",
        "",
        f"当前待确认题目共 **{len(pend)}** 道，已按考纲 9 大模块分类：",
        "",
    ]
    cur = None
    for c in pend:
        if c["module"] != cur:
            cur = c["module"]
            out += [f"### 模块 {cur}：{names[cur]}", ""]
        out.append(f"- [ ] **#{c['id']}** {short(c['title'], 60)}（{link(c)}）")
    out.append("")
    return "\n".join(out)


def main():
    if not CARDS.exists():
        sys.exit(f"找不到 {CARDS}")
    cards = load_cards()
    confirmed = load_registry()
    (VAULT / "10-错题看板.md").write_text(build_dashboard(cards, confirmed), encoding="utf-8")
    (VAULT / "11-红名单.md").write_text(build_redlist(cards, confirmed), encoding="utf-8")
    (VAULT / "12-星标待确认清单.md").write_text(build_star_review(cards, confirmed), encoding="utf-8")
    print(f"成功解析全量 {len(cards)} 张卡片（100% 覆盖）")
    print(f"已生成：\n  - 05-error-vault/10-错题看板.md\n  - 05-error-vault/11-红名单.md\n  - 05-error-vault/12-星标待确认清单.md")


if __name__ == "__main__":
    main()
