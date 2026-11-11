#!/usr/bin/env python3
"""
Quiz Studio Generator for Ruankao Error Vault
Generates a 100% self-contained, offline single-file HTML quiz practice app
with beautiful Markdown & LaTeX Math rendering, table support, and callout styling.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_FILE = REPO_ROOT / "01-shared-core" / "05-error-vault" / "01-上午综合知识错题集.md"
OUTPUT_HTML = REPO_ROOT / "quiz.html"

HEAD_RE = re.compile(r"^###\s+(?P<icons>[^\d错]*?)错题\s*(?P<id>\d+)\s*(?P<extra_icons>[^：:\w\s]*?)\s*[：:](?P<title>.*)$")

MODULES = [
    ("01", "计算机组成与体系结构"),
    ("02", "程序设计语言与编译"),
    ("03", "操作系统知识"),
    ("04", "软件工程与项目管理"),
    ("05", "数据库系统技术"),
    ("06", "计算机网络与信息安全"),
    ("07", "数据结构与算法基础"),
    ("08", "面向对象与UML建模"),
    ("09", "法律法规与标准化"),
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

ROUND_WORDS = {"二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def parse_round(title: str) -> int:
    m = re.search(r"([二三四五六七八九])进宫", title)
    if m:
        return ROUND_WORDS[m.group(1)]
    if "二刷" in title or "复错" in title:
        return 2
    return 1


def classify(title: str) -> tuple[str, str]:
    for code, words in KEYWORDS:
        if any(w.lower() in title.lower() for w in words):
            name = next(n for c, n in MODULES if c == code)
            return code, name
    return "07", "数据结构与算法基础"


def clean_section_text(s: str) -> str:
    # 1. Strip residual leading colon or header remnants like "**：\n", "：\n", "* **：\n"
    s = re.sub(r"^\s*[*_]*[：:]\s*", "", s)
    # 2. Remove trailing 【关联母本】 and the bullet marker before it
    s = re.sub(r"\n?\s*[*_\-]*\s*【关联母本】.*", "", s, flags=re.DOTALL)
    # 3. Strip trailing divider lines like \n---
    s = re.sub(r"\n---\s*$", "", s)
    # 4. Strip trailing dangling bullet marker lines like '\n* **' or '\n- ' or '\n*'
    s = re.sub(r"\n\s*[*_\-]+\s*[*_]*\s*$", "", s)
    return s.strip()


def extract_questions():
    raw_text = VAULT_FILE.read_text(encoding="utf-8")
    card_chunks = re.split(r"\n(?=###\s+[^\d错]*?错题\s*\d+)", raw_text)[1:]
    
    questions = []
    OPT_LINE_RE = re.compile(r"^[>\s*-]*\b([A-D])[.、\s]+(.*)$")
    
    for idx, chunk in enumerate(card_chunks, 1):
        lines = chunk.strip().splitlines()
        first_line = lines[0]
        m = HEAD_RE.match(first_line)
        if not m:
            continue
        cid = int(m.group("id"))
        raw_title = m.group("title").strip()
        is_star = "⭐" in m.group("icons") or "⭐" in m.group("extra_icons")
        round_num = parse_round(raw_title)
        mod_code, mod_name = classify(raw_title)
        clean_title = re.sub(r"【[^】]*】", "", raw_title).strip()
        
        parts_diag = chunk.split("【作答诊断】", 1)
        q_chunk = parts_diag[0]
        rest = parts_diag[1] if len(parts_diag) > 1 else ""
        
        parts_analysis = rest.split("【15秒秒杀与正解推导】", 1)
        if len(parts_analysis) == 1:
            parts_analysis = rest.split("【秒杀推导】", 1)
            
        diag_chunk = parts_analysis[0] if len(parts_analysis) > 1 else rest
        analysis_chunk = parts_analysis[1] if len(parts_analysis) > 1 else ""
        
        # Extract Answer
        ans = "A"
        ans_m = re.search(r"🎯\s*[*_]*正解[*_]*[：:]\s*(?:[#*_` ]*)([A-D])\b", rest)
        if not ans_m:
            ans_m = re.search(r"[*_]*正解[*_]*[：:]\s*(?:[#*_` ]*)([A-D])\b", rest)
        if not ans_m:
            ans_m = re.search(r"[*_]*正确答案[*_]*[：:]\s*(?:[#*_` ]*)([A-D])\b", rest)
        if ans_m:
            ans = ans_m.group(1)
        else:
            comp_m = re.search(r"正解[：:]\s*([^\n|]+)", rest)
            if comp_m:
                cand = comp_m.group(1).strip()
                m_single = re.search(r"\b([A-D])\b", cand)
                if m_single:
                    ans = m_single.group(1)
        
        # Parse question text and options
        q_lines = []
        options = {}
        source_note = ""
        
        for ql in q_chunk.splitlines()[1:]:
            ql_strip = ql.strip()
            if not ql_strip:
                continue
            if "【真题回溯】" in ql:
                sm = re.search(r"【真题回溯】[（(]([^）)]+)[）)]", ql)
                if sm:
                    source_note = sm.group(1).strip()
                continue
            
            opt_m = OPT_LINE_RE.match(ql_strip)
            if opt_m:
                letter = opt_m.group(1)
                text = opt_m.group(2).strip()
                text = re.sub(r"^[*_]+|[*_]+$", "", text).strip()
                if letter not in options:
                    options[letter] = text
            else:
                clean_ql = re.sub(r"^[> ]+", "", ql).strip()
                if clean_ql and clean_ql not in ["*", "* **", "-", ">", "---"]:
                    q_lines.append(clean_ql)
                    
        for k in ["A", "B", "C", "D"]:
            if k not in options:
                options[k] = f"选项 {k}（参见解析）"
                
        diag_clean = clean_section_text(diag_chunk)
        analysis_clean = clean_section_text(analysis_chunk)
        
        questions.append({
            "id": cid,
            "title": clean_title,
            "star": is_star,
            "round": round_num,
            "module_code": mod_code,
            "module_name": mod_name,
            "source": source_note,
            "question": "\n".join(q_lines).strip(),
            "options": options,
            "answer": ans if ans in ["A", "B", "C", "D"] else "A",
            "diagnosis": diag_clean,
            "analysis": analysis_clean
        })
        
    questions.sort(key=lambda x: x["id"])
    return questions


def generate_html(questions):
    questions_json = json.dumps(questions, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>软考通关·智能离线刷题站 (Ruankao Quiz Studio)</title>
  <style>
    :root {{
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --primary-light: #eef2ff;
      --success: #10b981;
      --success-light: #ecfdf5;
      --danger: #ef4444;
      --danger-light: #fef2f2;
      --warning: #f59e0b;
      --warning-light: #fffbeb;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
      --table-header-bg: #f1f5f9;
      --table-zebra: #f8fafc;
      --math-font: "Cambria Math", "Latin Modern Math", "STIX Two Math", "KaTeX_Math", Georgia, serif;
    }}

    [data-theme="dark"] {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --border: #334155;
      --primary-light: #312e81;
      --success-light: #064e3b;
      --danger-light: #7f1d1d;
      --warning-light: #78350f;
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);
      --table-header-bg: #1e293b;
      --table-zebra: #0f172a;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.2s, color 0.2s;
    }}

    /* Top Nav */
    header {{
      background-color: var(--card-bg);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 30;
      box-shadow: var(--shadow);
    }}
    .header-content {{
      max-width: 1000px;
      margin: 0 auto;
      padding: 0.75rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }}
    .logo-area {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .logo-badge {{
      background: linear-gradient(135deg, #4f46e5, #7c3aed);
      color: white;
      padding: 0.25rem 0.5rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.85rem;
      letter-spacing: 0.5px;
    }}
    .site-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      padding: 0.45rem 0.85rem;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      border: 1px solid var(--border);
      background-color: var(--card-bg);
      color: var(--text);
      transition: all 0.15s ease;
      user-select: none;
    }}
    .btn:hover {{
      background-color: var(--border);
    }}
    .btn-primary {{
      background-color: var(--primary);
      color: white;
      border-color: var(--primary);
    }}
    .btn-primary:hover {{
      background-color: var(--primary-hover);
    }}
    .btn-icon {{
      padding: 0.45rem;
      line-height: 1;
    }}

    /* Filter & Controls Bar */
    .controls-bar {{
      max-width: 1000px;
      margin: 0 auto;
      padding: 0.75rem 1rem 0;
      width: 100%;
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      align-items: center;
      justify-content: space-between;
    }}
    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
    }}
    .pill {{
      padding: 0.35rem 0.7rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      cursor: pointer;
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text-muted);
      transition: all 0.15s;
    }}
    .pill:hover {{
      color: var(--text);
      border-color: var(--primary);
    }}
    .pill.active {{
      background-color: var(--primary);
      color: white;
      border-color: var(--primary);
      font-weight: 600;
    }}
    .pill.pill-star.active {{
      background-color: var(--warning);
      border-color: var(--warning);
    }}
    .pill.pill-danger.active {{
      background-color: var(--danger);
      border-color: var(--danger);
    }}

    .search-box {{
      position: relative;
      min-width: 180px;
      flex: 1;
      max-width: 240px;
    }}
    .search-input {{
      width: 100%;
      padding: 0.35rem 0.65rem 0.35rem 1.8rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      background-color: var(--card-bg);
      color: var(--text);
      font-size: 0.825rem;
    }}
    .search-input:focus {{
      outline: none;
      border-color: var(--primary);
    }}
    .search-icon {{
      position: absolute;
      left: 0.5rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    /* Stats bar */
    .stats-bar {{
      max-width: 1000px;
      margin: 0.5rem auto 0;
      padding: 0 1rem;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .stats-badges {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .stat-badge {{
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }}
    .stat-val {{
      font-weight: 700;
      color: var(--text);
    }}
    .stat-val.stat-correct {{ color: var(--success); }}
    .stat-val.stat-wrong {{ color: var(--danger); }}

    .progress-track {{
      width: 120px;
      height: 6px;
      background-color: var(--border);
      border-radius: 9999px;
      overflow: hidden;
    }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, #10b981, #4f46e5);
      width: 0%;
      transition: width 0.3s;
    }}

    /* Main Container */
    main {{
      max-width: 1000px;
      margin: 0.75rem auto 2rem;
      padding: 0 1rem;
      width: 100%;
      flex: 1;
    }}

    .question-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: var(--shadow);
      position: relative;
      margin-bottom: 1rem;
    }}

    .card-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1rem;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    .meta-tags {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .tag {{
      font-size: 0.75rem;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-weight: 600;
      background-color: var(--border);
      color: var(--text-muted);
    }}
    .tag-id {{
      background-color: var(--primary-light);
      color: var(--primary);
    }}
    .tag-star {{
      background-color: var(--warning-light);
      color: var(--warning);
    }}
    .tag-danger {{
      background-color: var(--danger-light);
      color: var(--danger);
    }}

    .star-btn {{
      background: none;
      border: none;
      font-size: 1.25rem;
      cursor: pointer;
      color: #cbd5e1;
      transition: transform 0.15s, color 0.15s;
    }}
    .star-btn.active {{
      color: #f59e0b;
      transform: scale(1.1);
    }}

    .question-title {{
      font-size: 1.05rem;
      font-weight: 700;
      margin-bottom: 0.85rem;
      line-height: 1.4;
      color: var(--text);
    }}

    .question-body {{
      font-size: 0.95rem;
      line-height: 1.7;
      margin-bottom: 1.5rem;
      word-break: break-word;
    }}

    /* Options */
    .options-grid {{
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      margin-bottom: 1.5rem;
    }}
    .option-item {{
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      padding: 0.85rem 1rem;
      border: 1.5px solid var(--border);
      border-radius: 8px;
      cursor: pointer;
      background-color: var(--card-bg);
      transition: all 0.15s ease;
      user-select: none;
    }}
    .option-item:hover:not(.locked) {{
      border-color: var(--primary);
      background-color: var(--primary-light);
    }}
    .option-key {{
      width: 26px;
      height: 26px;
      border-radius: 50%;
      border: 1.5px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
      flex-shrink: 0;
      transition: all 0.15s;
    }}
    .option-text {{
      font-size: 0.925rem;
      line-height: 1.5;
      flex: 1;
    }}

    /* Selected state */
    .option-item.selected-correct {{
      border-color: var(--success);
      background-color: var(--success-light);
    }}
    .option-item.selected-correct .option-key {{
      background-color: var(--success);
      color: white;
      border-color: var(--success);
    }}
    .option-item.selected-wrong {{
      border-color: var(--danger);
      background-color: var(--danger-light);
    }}
    .option-item.selected-wrong .option-key {{
      background-color: var(--danger);
      color: white;
      border-color: var(--danger);
    }}

    /* Rich Explanation Drawer */
    .explanation-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      margin-top: 1.25rem;
      display: none;
      box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.02);
    }}
    .explanation-card.show {{
      display: block;
      animation: fadeIn 0.2s ease-in;
    }}

    /* Diagnosis Dashboard */
    .diag-dashboard {{
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      margin-bottom: 1.25rem;
      padding-bottom: 1rem;
      border-bottom: 1px dashed var(--border);
    }}
    .diag-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
    }}
    .diag-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.4rem 0.75rem;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 600;
    }}
    .diag-badge-correct {{
      background-color: var(--success-light);
      color: #065f46;
      border: 1px solid #a7f3d0;
    }}
    .diag-badge-wrong {{
      background-color: var(--danger-light);
      color: #991b1b;
      border: 1px solid #fecaca;
    }}
    .diag-rootcause {{
      background-color: var(--warning-light);
      border: 1px solid #fde68a;
      border-left: 4px solid var(--warning);
      border-radius: 6px;
      padding: 0.65rem 0.85rem;
      font-size: 0.875rem;
      line-height: 1.6;
      color: var(--text);
    }}
    .diag-rootcause-title {{
      font-weight: 700;
      color: #92400e;
      margin-bottom: 0.2rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}

    /* Rich Analysis Content */
    .analysis-body {{
      font-size: 0.925rem;
      line-height: 1.7;
      color: var(--text);
    }}
    .analysis-body p {{
      margin-bottom: 0.75rem;
    }}

    /* Math Rendering */
    .math-inline {{
      font-family: var(--math-font);
      font-size: 1.05em;
      padding: 0 0.15rem;
      color: var(--text);
      letter-spacing: 0.2px;
    }}
    .math-block {{
      font-family: var(--math-font);
      font-size: 1.1em;
      text-align: center;
      margin: 0.75rem 0;
      padding: 0.65rem;
      background-color: var(--bg);
      border-radius: 6px;
      border: 1px solid var(--border);
      overflow-x: auto;
    }}
    .frac {{
      display: inline-flex;
      flex-direction: column;
      vertical-align: middle;
      text-align: center;
      font-size: 0.9em;
      padding: 0 0.15rem;
    }}
    .frac-num {{ border-bottom: 1px solid currentColor; line-height: 1; padding-bottom: 1px; }}
    .frac-den {{ line-height: 1; padding-top: 1px; }}

    /* Tables */
    .table-wrap {{
      width: 100%;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
    .quiz-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
      text-align: left;
    }}
    .quiz-table th {{
      background-color: var(--table-header-bg);
      padding: 0.65rem 0.85rem;
      font-weight: 700;
      border-bottom: 2px solid var(--border);
      color: var(--text);
      white-space: nowrap;
    }}
    .quiz-table td {{
      padding: 0.6rem 0.85rem;
      border-bottom: 1px solid var(--border);
      line-height: 1.5;
    }}
    .quiz-table tr:nth-child(even) {{
      background-color: var(--table-zebra);
    }}
    .quiz-table tr:last-child td {{
      border-bottom: none;
    }}

    /* Callout Alert Boxes */
    .callout {{
      border-radius: 8px;
      padding: 0.75rem 1rem;
      margin: 0.85rem 0;
      font-size: 0.875rem;
      line-height: 1.6;
    }}
    .callout-header {{
      font-weight: 700;
      margin-bottom: 0.35rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .callout-gold {{
      background-color: var(--warning-light);
      border: 1px solid #fde68a;
      border-left: 4px solid var(--warning);
      color: var(--text);
    }}
    .callout-gold .callout-header {{
      color: #b45309;
    }}
    .callout-rose {{
      background-color: var(--danger-light);
      border: 1px solid #fecaca;
      border-left: 4px solid var(--danger);
      color: var(--text);
    }}
    .callout-rose .callout-header {{
      color: #b91c1c;
    }}
    .callout-indigo {{
      background-color: var(--primary-light);
      border: 1px solid #c7d2fe;
      border-left: 4px solid var(--primary);
      color: var(--text);
    }}
    .callout-indigo .callout-header {{
      color: #3730a3;
    }}

    .quiz-ul {{
      padding-left: 1.35rem;
      margin-bottom: 0.75rem;
    }}
    .quiz-li {{
      margin-bottom: 0.35rem;
      line-height: 1.6;
    }}
    .kbd-inline {{
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
      background-color: var(--bg);
      border: 1px solid var(--border);
      font-size: 0.85em;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}

    /* Bottom Bar */
    .nav-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .shortcut-hints {{
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .kbd {{
      padding: 0.15rem 0.35rem;
      border: 1px solid var(--border);
      border-radius: 3px;
      font-size: 0.7rem;
      background-color: var(--card-bg);
      box-shadow: 0 1px 1px rgb(0 0 0 / 0.1);
    }}

    /* Sheet Drawer Modal */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(2px);
      z-index: 50;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }}
    .modal-overlay.open {{
      display: flex;
      animation: fadeIn 0.15s ease-out;
    }}
    .sheet-modal {{
      background-color: var(--card-bg);
      border-radius: 12px;
      width: 100%;
      max-width: 800px;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border);
    }}
    .sheet-header {{
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .sheet-body {{
      padding: 1rem 1.25rem;
      overflow-y: auto;
      flex: 1;
    }}
    .sheet-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(44px, 1fr));
      gap: 0.45rem;
    }}
    .sheet-bubble {{
      height: 44px;
      border-radius: 6px;
      border: 1px solid var(--border);
      background-color: var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.1s;
      position: relative;
    }}
    .sheet-bubble:hover {{
      transform: scale(1.08);
      border-color: var(--primary);
    }}
    .sheet-bubble.current {{
      box-shadow: 0 0 0 2px var(--primary);
    }}
    .sheet-bubble.b-correct {{
      background-color: var(--success);
      color: white;
      border-color: var(--success);
    }}
    .sheet-bubble.b-wrong {{
      background-color: var(--danger);
      color: white;
      border-color: var(--danger);
    }}
    .sheet-bubble.b-star::after {{
      content: "★";
      position: absolute;
      top: -3px;
      right: -2px;
      font-size: 0.65rem;
      color: #f59e0b;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}

    @media (max-width: 640px) {{
      .controls-bar {{ flex-direction: column; align-items: stretch; }}
      .search-box {{ max-width: 100%; }}
      .nav-bar {{ flex-direction: column; align-items: stretch; }}
      .nav-actions {{ justify-content: space-between; }}
      .diag-row {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>

  <!-- Top Nav -->
  <header>
    <div class="header-content">
      <div class="logo-area">
        <span class="logo-badge">软考通关</span>
        <span class="site-title">智能离线刷题站</span>
      </div>
      <div class="header-actions">
        <button class="btn" id="btn-sheet" title="展开答题卡">
          <span>📋 答题卡</span>
        </button>
        <button class="btn btn-icon" id="btn-theme" title="切换暗色/亮色模式">
          <span id="theme-icon">🌙</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Controls & Filters -->
  <div class="controls-bar">
    <div class="filter-pills" id="filter-container">
      <span class="pill active" data-filter="all">🌟 全量 (397)</span>
      <span class="pill pill-star" data-filter="star">⭐ 重点标星</span>
      <span class="pill pill-danger" data-filter="repeat">🚨 进宫高危</span>
      <span class="pill" data-filter="wrong">❌ 我的错题</span>
      <span class="pill" data-filter="unanswered">⚪ 未做题</span>
      <span class="pill" data-filter="random20">🎲 抽20题</span>
      <span class="pill" data-filter="random50">🎲 抽50题</span>
    </div>
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" class="search-input" id="search-input" placeholder="搜索考点/题干...">
    </div>
  </div>

  <!-- Stats -->
  <div class="stats-bar">
    <div class="stats-badges">
      <span class="stat-badge">进度: <span class="stat-val" id="stat-progress">0/397</span></span>
      <span class="stat-badge">正确率: <span class="stat-val" id="stat-rate">0%</span></span>
      <span class="stat-badge"><span class="stat-val stat-correct" id="stat-correct">0</span> 正确</span>
      <span class="stat-badge"><span class="stat-val stat-wrong" id="stat-wrong">0</span> 错误</span>
    </div>
    <div class="progress-track" title="完成进度">
      <div class="progress-fill" id="progress-fill"></div>
    </div>
  </div>

  <!-- Main Question Card -->
  <main>
    <div class="question-card" id="card-view">
      <div class="card-meta">
        <div class="meta-tags">
          <span class="tag tag-id" id="meta-id">#1</span>
          <span class="tag" id="meta-module">数据结构与算法</span>
          <span class="tag tag-star" id="meta-star" style="display: none;">⭐ 重点标星</span>
          <span class="tag tag-danger" id="meta-round" style="display: none;">🚨 二进宫复错</span>
        </div>
        <button class="star-btn" id="btn-star" title="标记此题">★</button>
      </div>

      <div class="question-title" id="q-title">题目加载中...</div>
      <div class="question-body" id="q-body"></div>

      <!-- Options -->
      <div class="options-grid" id="options-container">
        <!-- Rendered by JS -->
      </div>

      <!-- Rich Explanation Drawer -->
      <div class="explanation-card" id="exp-drawer">
        <div class="diag-dashboard" id="exp-diag-box"></div>
        <div class="analysis-body" id="exp-analysis-box"></div>
      </div>

      <!-- Nav Bar -->
      <div class="nav-bar">
        <div class="shortcut-hints">
          按 <span class="kbd">A</span> <span class="kbd">B</span> <span class="kbd">C</span> <span class="kbd">D</span> 作答，<span class="kbd">←</span> <span class="kbd">→</span> 切题，<span class="kbd">Space</span> 展开解析
        </div>
        <div class="nav-actions">
          <button class="btn" id="btn-toggle-exp">💡 查看解析</button>
          <button class="btn" id="btn-prev">⬅ 上一题</button>
          <button class="btn btn-primary" id="btn-next">下一题 ➡</button>
        </div>
      </div>
    </div>
  </main>

  <!-- Sheet Drawer Modal -->
  <div class="modal-overlay" id="modal-sheet">
    <div class="sheet-modal">
      <div class="sheet-header">
        <div style="font-weight: 700;">📋 答题卡快速定位 (<span id="sheet-count">397</span> 题)</div>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
          <button class="btn" id="btn-reset-data" style="font-size: 0.8rem; color: var(--danger);">🗑️ 重置答题记录</button>
          <button class="btn btn-icon" id="btn-close-sheet">✕</button>
        </div>
      </div>
      <div class="sheet-body">
        <div class="sheet-grid" id="sheet-grid">
          <!-- Filled by JS -->
        </div>
      </div>
    </div>
  </div>

  <!-- Embedded Question Bank JSON -->
  <script>
    const ALL_QUESTIONS = {questions_json};
  </script>

  <!-- Rich Markdown & Formula Rendering Engine -->
  <script>
    const RichRenderer = {{
      formatMath(mathStr) {{
        let s = mathStr;
        const syms = [
          [/\\\\Theta/g, 'Θ'], [/\\\\alpha/g, 'α'], [/\\\\beta/g, 'β'], [/\\\\gamma/g, 'γ'],
          [/\\\\delta/g, 'δ'], [/\\\\lambda/g, 'λ'], [/\\\\mu/g, 'μ'], [/\\\\sigma/g, 'σ'],
          [/\\\\omega/g, 'ω'], [/\\\\pi/g, 'π'],
          [/\\\\implies/g, ' ⇒ '], [/\\\\to/g, ' → '], [/\\\\times/g, ' × '], [/\\\\div/g, ' ÷ '],
          [/\\\\le/g, ' ≤ '], [/\\\\ge/g, ' ≥ '], [/\\\\ne/g, ' ≠ '], [/\\\\approx/g, ' ≈ '],
          [/\\\\in/g, ' ∈ '], [/\\\\notin/g, ' ∉ '], [/\\\\cup/g, ' ∪ '], [/\\\\cap/g, ' ∩ '],
          [/\\\\cdot/g, ' · '], [/\\\\pm/g, ' ± '], [/\\\\mid/g, ' | ']
        ];
        syms.forEach(([re, rep]) => {{ s = s.replace(re, rep); }});

        s = s.replace(/\\\\mathbf\{{([^}}]+)\}}/g, '<strong>$1</strong>');
        s = s.replace(/\\\\mathit\{{([^}}]+)\}}/g, '<em>$1</em>');
        s = s.replace(/\\\\text\{{([^}}]+)\}}/g, '$1');

        // Fractions
        s = s.replace(/\\\\frac\{{([^}}]+)\}}\{{([^}}]+)\}}/g, '<span class="frac"><span class="frac-num">$1</span><span class="frac-den">$2</span></span>');

        // Logarithms
        s = s.replace(/\\\\log_([a-zA-Z0-9]+)/g, 'log<sub>$1</sub>');
        s = s.replace(/\\\\log_\{{([^}}]+)\}}/g, 'log<sub>$1</sub>');
        s = s.replace(/\\\\log/g, 'log');

        // Subscripts & Superscripts
        s = s.replace(/_\{{([^}}]+)\}}/g, '<sub>$1</sub>');
        s = s.replace(/_([a-zA-Z0-9])/g, '<sub>$1</sub>');
        s = s.replace(/\\^\{{([^}}]+)\}}/g, '<sup>$1</sup>');
        s = s.replace(/\\^([a-zA-Z0-9])/g, '<sup>$1</sup>');

        return '<span class="math-inline">' + s + '</span>';
      }},

      renderText(raw) {{
        if (!raw) return '';
        let text = raw;

        // Block math $$...$$
        text = text.replace(/\\$\\$([\\s\\S]*?)\\$\\$/g, (m, c) => {{
          return '<div class="math-block">' + this.formatMath(c.trim()) + '</div>';
        }});

        // Inline math $...$
        text = text.replace(/\\$([^$\\n]+?)\\$/g, (m, c) => {{
          return this.formatMath(c.trim());
        }});

        // Bold & Code
        text = text.replace(/\\*\\*([^\\*\\n]+?)\\*\\*/g, '<strong>$1</strong>');
        text = text.replace(/`([^`\\n]+?)`/g, '<code class="kbd-inline">$1</code>');

        return text;
      }},

      renderTable(lines) {{
        if (lines.length < 2) return '';
        const headerRow = lines[0].split('|').map(c => c.trim()).filter((c, i, a) => i > 0 && i < a.length - 1);
        const bodyRows = lines.slice(2).map(line => {{
          return line.split('|').map(c => c.trim()).filter((c, i, a) => i > 0 && i < a.length - 1);
        }});

        let html = '<div class="table-wrap"><table class="quiz-table"><thead><tr>';
        headerRow.forEach(h => {{ html += '<th>' + this.renderText(h) + '</th>'; }});
        html += '</tr></thead><tbody>';

        bodyRows.forEach(row => {{
          if (row.length === 0) return;
          html += '<tr>';
          row.forEach(cell => {{ html += '<td>' + this.renderText(cell) + '</td>'; }});
          html += '</tr>';
        }});
        html += '</tbody></table></div>';
        return html;
      }},

      renderMarkdown(md) {{
        if (!md) return '';
        const rawLines = md.split('\\n');
        let out = [];
        let inTable = false;
        let tableLines = [];
        let inList = false;

        const closeList = () => {{
          if (inList) {{ out.push('</ul>'); inList = false; }}
        }};
        const closeTable = () => {{
          if (inTable) {{ out.push(this.renderTable(tableLines)); inTable = false; tableLines = []; }}
        }};

        for (let i = 0; i < rawLines.length; i++) {{
          const line = rawLines[i].trim();

          // Table line
          if (line.startsWith('|') && line.endsWith('|')) {{
            closeList();
            inTable = true;
            tableLines.push(line);
            continue;
          }} else {{
            closeTable();
          }}

          if (!line) {{
            closeList();
            continue;
          }}

          // Callout Banners
          if (line.includes('【考场避坑口诀】') || line.includes('【避坑口诀】')) {{
            closeList();
            const content = line.replace(/^.*?【(?:考场)?避坑口诀】[*_\\s]*[：:]\\s*/, '').trim();
            out.push('<div class="callout callout-gold"><div class="callout-header">🛡️ 考场避坑口诀</div><div class="callout-body">' + this.renderText(content) + '</div></div>');
            continue;
          }}

          if (line.includes('【考场避坑决斗速记表】') || line.includes('【决斗速记表】') || line.includes('【速记对比表】')) {{
            closeList();
            out.push('<div style="font-weight:700; margin-top:1.25rem; margin-bottom:0.4rem; color:var(--primary); font-size: 0.95rem;">📊 考场决斗速记表：</div>');
            continue;
          }}

          // Bullet list items
          const listMatch = line.match(/^[-*]\\s+(.*)$/);
          if (listMatch) {{
            let content = listMatch[1].trim();
            if (!content || content === '**' || content === '*') continue;
            if (!inList) {{ out.push('<ul class="quiz-ul">'); inList = true; }}
            out.push('<li class="quiz-li">' + this.renderText(content) + '</li>');
            continue;
          }} else {{
            closeList();
          }}

          // Standard paragraph or block math
          if (line.startsWith('$$') && line.endsWith('$$')) {{
            out.push('<div class="math-block">' + this.formatMath(line.slice(2, -2).trim()) + '</div>');
          }} else {{
            out.push('<p class="quiz-p">' + this.renderText(line) + '</p>');
          }}
        }}

        closeList();
        closeTable();
        return out.join('');
      }},

      renderDiagnosis(diagStr) {{
        if (!diagStr) return '';
        const parts = diagStr.split(/\\s*[｜|]\\s*/);
        let correctText = '';
        let wrongText = '';
        let rootCause = '';

        parts.forEach(p => {{
          const clean = p.trim();
          if (clean.includes('正解')) {{
            correctText = clean.replace(/^.*?[🎯]?\\s*正解\\s*[*_]*[：:]\\s*/, '').trim();
          }} else if (clean.includes('错选') || clean.includes('作答')) {{
            wrongText = clean.replace(/^.*?[❌]?\\s*(?:错选|作答)\\s*[*_]*[：:]\\s*/, '').trim();
          }} else if (clean.includes('根因')) {{
            rootCause = clean.replace(/^.*?[💥]?\\s*根因\\s*[*_]*[：:]\\s*/, '').trim();
          }} else if (!correctText) {{
            correctText = clean;
          }}
        }});

        let html = '<div class="diag-dashboard">';
        html += '<div class="diag-row">';
        if (correctText) {{
          html += '<div class="diag-badge diag-badge-correct"><span>🎯 标准正解:</span> <span>' + this.renderText(correctText) + '</span></div>';
        }}
        if (wrongText) {{
          html += '<div class="diag-badge diag-badge-wrong"><span>❌ 常见错因/错选:</span> <span>' + this.renderText(wrongText) + '</span></div>';
        }}
        html += '</div>';

        if (rootCause) {{
          html += '<div class="diag-rootcause"><div class="diag-rootcause-title">💥 失分根因深度剖析</div><div class="diag-rootcause-body">' + this.renderText(rootCause) + '</div></div>';
        }}
        html += '</div>';
        return html;
      }}
    }};
  </script>

  <!-- Main Quiz Engine Script -->
  <script>
    (function() {{
      // State
      let filteredList = [...ALL_QUESTIONS];
      let currentIndex = 0;
      let currentFilter = 'all';
      let searchQuery = '';

      // LocalStorage Key
      const STORAGE_KEY = 'ruankao_quiz_app_v1';
      let userState = {{
        answered: {{}},
        customStars: {{}}
      }};

      try {{
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) userState = JSON.parse(saved);
      }} catch(e) {{}}

      function saveState() {{
        try {{
          localStorage.setItem(STORAGE_KEY, JSON.stringify(userState));
        }} catch(e) {{}}
      }}

      // DOM Elements
      const qTitle = document.getElementById('q-title');
      const qBody = document.getElementById('q-body');
      const optContainer = document.getElementById('options-container');
      const expDrawer = document.getElementById('exp-drawer');
      const expDiagBox = document.getElementById('exp-diag-box');
      const expAnalysisBox = document.getElementById('exp-analysis-box');
      const metaId = document.getElementById('meta-id');
      const metaModule = document.getElementById('meta-module');
      const metaStar = document.getElementById('meta-star');
      const metaRound = document.getElementById('meta-round');
      const btnStar = document.getElementById('btn-star');
      const btnPrev = document.getElementById('btn-prev');
      const btnNext = document.getElementById('btn-next');
      const btnToggleExp = document.getElementById('btn-toggle-exp');
      const statProgress = document.getElementById('stat-progress');
      const statRate = document.getElementById('stat-rate');
      const statCorrect = document.getElementById('stat-correct');
      const statWrong = document.getElementById('stat-wrong');
      const progressFill = document.getElementById('progress-fill');
      const modalSheet = document.getElementById('modal-sheet');
      const sheetGrid = document.getElementById('sheet-grid');
      const btnSheet = document.getElementById('btn-sheet');
      const btnCloseSheet = document.getElementById('btn-close-sheet');
      const btnResetData = document.getElementById('btn-reset-data');
      const searchInput = document.getElementById('search-input');
      const btnTheme = document.getElementById('btn-theme');
      const themeIcon = document.getElementById('theme-icon');

      // Theme toggle
      const savedTheme = localStorage.getItem('ruankao_quiz_theme') || 'light';
      document.documentElement.setAttribute('data-theme', savedTheme);
      themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

      btnTheme.addEventListener('click', () => {{
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const nextTheme = isDark ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', nextTheme);
        themeIcon.textContent = nextTheme === 'dark' ? '☀️' : '🌙';
        localStorage.setItem('ruankao_quiz_theme', nextTheme);
      }});

      // Filter Logic
      function applyFilter(filter, query = '') {{
        currentFilter = filter;
        searchQuery = query.toLowerCase().trim();

        if (filter.startsWith('random')) {{
          const count = parseInt(filter.replace('random', ''), 10) || 20;
          const shuffled = [...ALL_QUESTIONS].sort(() => 0.5 - Math.random());
          filteredList = shuffled.slice(0, count);
        }} else {{
          filteredList = ALL_QUESTIONS.filter(q => {{
            const isUserStar = userState.customStars[q.id] !== undefined ? userState.customStars[q.id] : q.star;
            const ansInfo = userState.answered[q.id];

            if (filter === 'star' && !isUserStar) return false;
            if (filter === 'repeat' && q.round < 2) return false;
            if (filter === 'wrong' && (!ansInfo || ansInfo.correct)) return false;
            if (filter === 'unanswered' && ansInfo) return false;

            if (searchQuery) {{
              const matchTitle = q.title.toLowerCase().includes(searchQuery);
              const matchBody = q.question.toLowerCase().includes(searchQuery);
              const matchId = String(q.id) === searchQuery;
              if (!matchTitle && !matchBody && !matchId) return false;
            }}
            return true;
          }});
        }}

        currentIndex = 0;
        updateStats();
        renderQuestion();
      }}

      // Render Question
      function renderQuestion() {{
        if (filteredList.length === 0) {{
          qTitle.textContent = '暂无符合筛选条件的题目';
          qBody.innerHTML = '<p style="color:var(--text-muted);">可尝试切换上方分类标签或清空搜索关键词。</p>';
          optContainer.innerHTML = '';
          expDrawer.classList.remove('show');
          metaId.textContent = '#--';
          metaModule.textContent = '--';
          metaStar.style.display = 'none';
          metaRound.style.display = 'none';
          return;
        }}

        if (currentIndex < 0) currentIndex = 0;
        if (currentIndex >= filteredList.length) currentIndex = filteredList.length - 1;

        const q = filteredList[currentIndex];
        const isStarred = userState.customStars[q.id] !== undefined ? userState.customStars[q.id] : q.star;
        const ansInfo = userState.answered[q.id];

        // Meta tags
        metaId.textContent = `#${{q.id}}`;
        metaModule.textContent = q.module_name;
        metaStar.style.display = isStarred ? 'inline-block' : 'none';
        metaRound.style.display = q.round >= 2 ? 'inline-block' : 'none';
        metaRound.textContent = `🚨 ${{q.round}}进宫高危`;

        btnStar.classList.toggle('active', isStarred);

        // Render Title & Body with Rich Text & Math
        qTitle.innerHTML = RichRenderer.renderText(q.title);
        qBody.innerHTML = RichRenderer.renderMarkdown(q.question);

        // Render Options
        optContainer.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D'];
        letters.forEach(letter => {{
          const optText = q.options[letter] || '';
          if (!optText) return;

          const optDiv = document.createElement('div');
          optDiv.className = 'option-item';
          optDiv.dataset.key = letter;

          if (ansInfo) {{
            optDiv.classList.add('locked');
            if (letter === q.answer) {{
              optDiv.classList.add('selected-correct');
            }} else if (ansInfo.choice === letter && !ansInfo.correct) {{
              optDiv.classList.add('selected-wrong');
            }}
          }}

          optDiv.innerHTML = `
            <div class="option-key">${{letter}}</div>
            <div class="option-text">${{RichRenderer.renderText(optText)}}</div>
          `;

          optDiv.addEventListener('click', () => handleChoice(letter));
          optContainer.appendChild(optDiv);
        }});

        // Render Rich Explanation Drawer
        expDiagBox.innerHTML = RichRenderer.renderDiagnosis(q.diagnosis);
        expAnalysisBox.innerHTML = RichRenderer.renderMarkdown(q.analysis);

        if (ansInfo) {{
          expDrawer.classList.add('show');
          btnToggleExp.textContent = '🙈 折叠解析';
        }} else {{
          expDrawer.classList.remove('show');
          btnToggleExp.textContent = '💡 查看解析';
        }}

        // Button states
        btnPrev.disabled = currentIndex === 0;
        btnNext.disabled = currentIndex === filteredList.length - 1;

        updateStats();
      }}

      // Handle user choosing an option
      function handleChoice(letter) {{
        const q = filteredList[currentIndex];
        if (!q) return;

        const isCorrect = letter === q.answer;
        userState.answered[q.id] = {{
          choice: letter,
          correct: isCorrect,
          timestamp: Date.now()
        }};
        saveState();

        renderQuestion();
      }}

      // Update Statistics
      function updateStats() {{
        const total = ALL_QUESTIONS.length;
        const answeredIds = Object.keys(userState.answered);
        const answeredCount = answeredIds.length;
        const correctCount = answeredIds.filter(id => userState.answered[id].correct).length;
        const wrongCount = answeredCount - correctCount;
        const rate = answeredCount > 0 ? Math.round((correctCount / answeredCount) * 100) : 0;

        statProgress.textContent = `${{currentIndex + 1}}/${{filteredList.length}} (已答:${{answeredCount}}/${{total}})`;
        statRate.textContent = `${{rate}}%`;
        statCorrect.textContent = correctCount;
        statWrong.textContent = wrongCount;

        const fillPct = (answeredCount / total) * 100;
        progressFill.style.width = `${{fillPct}}%`;
      }}

      // Render Sheet Modal Grid
      function openSheet() {{
        sheetGrid.innerHTML = '';
        document.getElementById('sheet-count').textContent = filteredList.length;

        filteredList.forEach((q, idx) => {{
          const bubble = document.createElement('div');
          bubble.className = 'sheet-bubble';
          bubble.textContent = q.id;
          if (idx === currentIndex) bubble.classList.add('current');

          const ans = userState.answered[q.id];
          if (ans) {{
            if (ans.correct) bubble.classList.add('b-correct');
            else bubble.classList.add('b-wrong');
          }}

          const isStar = userState.customStars[q.id] !== undefined ? userState.customStars[q.id] : q.star;
          if (isStar) bubble.classList.add('b-star');

          bubble.addEventListener('click', () => {{
            currentIndex = idx;
            renderQuestion();
            modalSheet.classList.remove('open');
          }});
          sheetGrid.appendChild(bubble);
        }});

        modalSheet.classList.add('open');
      }}

      // Event Listeners
      btnStar.addEventListener('click', () => {{
        const q = filteredList[currentIndex];
        if (!q) return;
        const cur = userState.customStars[q.id] !== undefined ? userState.customStars[q.id] : q.star;
        userState.customStars[q.id] = !cur;
        saveState();
        renderQuestion();
      }});

      btnPrev.addEventListener('click', () => {{
        if (currentIndex > 0) {{
          currentIndex--;
          renderQuestion();
        }}
      }});

      btnNext.addEventListener('click', () => {{
        if (currentIndex < filteredList.length - 1) {{
          currentIndex++;
          renderQuestion();
        }}
      }});

      btnToggleExp.addEventListener('click', () => {{
        const isShow = expDrawer.classList.toggle('show');
        btnToggleExp.textContent = isShow ? '🙈 折叠解析' : '💡 查看解析';
      }});

      btnSheet.addEventListener('click', openSheet);
      btnCloseSheet.addEventListener('click', () => modalSheet.classList.remove('open'));
      modalSheet.addEventListener('click', (e) => {{
        if (e.target === modalSheet) modalSheet.classList.remove('open');
      }});

      // Reset data
      btnResetData.addEventListener('click', () => {{
        if (confirm('确认清空所有答题记录与错题标记吗？')) {{
          userState = {{ answered: {{}}, customStars: {{}} }};
          saveState();
          modalSheet.classList.remove('open');
          renderQuestion();
        }}
      }});

      // Filter pills
      document.getElementById('filter-container').addEventListener('click', (e) => {{
        const pill = e.target.closest('.pill');
        if (!pill) return;
        document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        applyFilter(pill.dataset.filter, searchInput.value);
      }});

      // Search
      let searchTimer = null;
      searchInput.addEventListener('input', (e) => {{
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => {{
          applyFilter(currentFilter, e.target.value);
        }}, 200);
      }});

      // Keyboard Shortcuts
      window.addEventListener('keydown', (e) => {{
        if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

        const key = e.key.toUpperCase();
        if (['A', 'B', 'C', 'D'].includes(key)) {{
          handleChoice(key);
        }} else if (e.key === 'ArrowLeft' || key === 'H') {{
          btnPrev.click();
        }} else if (e.key === 'ArrowRight' || key === 'L') {{
          btnNext.click();
        }} else if (e.key === ' ' || key === 'P') {{
          e.preventDefault();
          btnToggleExp.click();
        }}
      }});

      // Init
      applyFilter('all');
    }})();
  </script>
</body>
</html>
"""
    return html


def main():
    print(f"Parsing cards from: {VAULT_FILE}")
    questions = extract_questions()
    print(f"Extracted {len(questions)} cards.")
    
    html_content = generate_html(questions)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"Regenerated rich single-file offline quiz app: {OUTPUT_HTML}")
    print(f"File size: {len(html_content.encode('utf-8')) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
