#!/usr/bin/env python3
"""
Architect Quiz App Generator for Ruankao Senior System Architect
Generates a 100% self-contained, offline single-file HTML quiz practice app
from data/bank.json with Markdown & LaTeX Math rendering, table support,
and custom theme styling.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BANK_FILE = BASE_DIR / "03-system-architect" / "04-quiz-data" / "bank.json"
OUTPUT_HTML = BASE_DIR / "quiz-architect.html"

MODULE_NAMES = {
    "architecture": "🏛️ 系统架构设计",
    "software_engineering": "⚙️ 软件工程与生命周期",
    "computer_foundation": "💻 计算机与嵌入式系统",
    "database": "🗄️ 数据库系统与大数据",
    "network": "🌐 计算机网络",
    "security": "🔒 信息安全与可靠性",
    "project_management": "📋 项目管理与法律法规",
    "legal_ip": "⚖️ 知识产权与标准化",
    "english": "🔤 专业英语",
    "embedded": "🔌 嵌入式物联网",
    "new_technology": "🚀 前沿新兴技术",
    "other": "📚 综合基础"
}


def load_questions():
    if not BANK_FILE.exists():
        raise FileNotFoundError(f"Bank file not found at: {BANK_FILE}")
    
    with open(BANK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    raw_choices = data.get("choices", [])
    questions = []
    
    for idx, c in enumerate(raw_choices, start=1):
        mod_key = c.get("module", "other")
        mod_name = MODULE_NAMES.get(mod_key, "📚 综合基础")
        
        # Clean stem
        stem = c.get("stem", "").strip()
        if stem.startswith("题目:"):
            stem = stem[3:].strip()
        if stem.startswith("题目："):
            stem = stem[3:].strip()
            
        questions.append({
            "id": c.get("id", f"q-{idx}"),
            "index": idx,
            "term": c.get("term", "历年真题"),
            "paper": c.get("paper", ""),
            "questionNo": c.get("questionNo", idx),
            "sourceType": c.get("sourceType", "real"),
            "module_code": mod_key,
            "module_name": mod_name,
            "knowledge": c.get("knowledge", ""),
            "stem": stem,
            "options": c.get("options", {}),
            "answer": c.get("answer", "").strip().upper(),
            "analysis": c.get("analysis", "").strip()
        })
        
    return questions


def generate_html(questions):
    questions_json = json.dumps(questions, ensure_ascii=False)
    
    # Use standard format with {{ and }} escaped for Python formatting
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>软考高级·系统架构设计师 离线全真题刷题站 (1822题)</title>
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --primary-light: #eef2ff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --border-focus: #818cf8;
      --success: #10b981;
      --success-light: #ecfdf5;
      --danger: #ef4444;
      --danger-light: #fef2f2;
      --warning: #f59e0b;
      --warning-light: #fffbeb;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
      --table-header-bg: #f1f5f9;
      --table-zebra: #f8fafc;
      --math-font: "Cambria Math", "Latin Modern Math", "STIX Two Math", Georgia, serif;
    }

    [data-theme="dark"] {
      --bg: #0b0f19;
      --card-bg: #111827;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --primary-light: #1e1b4b;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --border: #1f2937;
      --border-focus: #6366f1;
      --success: #10b981;
      --success-light: #064e3b;
      --danger: #ef4444;
      --danger-light: #7f1d1d;
      --warning: #f59e0b;
      --warning-light: #78350f;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);
      --table-header-bg: #1f2937;
      --table-zebra: #161e2e;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Navigation */
    header {
      background-color: var(--card-bg);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: var(--shadow-sm);
    }
    .header-content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0.75rem 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }
    .brand-icon {
      font-size: 1.4rem;
      background: var(--primary-light);
      padding: 0.3rem 0.5rem;
      border-radius: 8px;
    }
    .brand-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
      line-height: 1.2;
    }
    .brand-subtitle {
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      padding: 0.45rem 0.85rem;
      font-size: 0.85rem;
      font-weight: 500;
      border-radius: 6px;
      border: 1px solid var(--border);
      background-color: var(--card-bg);
      color: var(--text);
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .btn:hover {
      background-color: var(--bg);
      border-color: var(--border-focus);
    }
    .btn-primary {
      background-color: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }
    .btn-primary:hover {
      background-color: var(--primary-hover);
    }
    .btn-star.active {
      color: var(--warning);
      border-color: var(--warning);
      background-color: var(--warning-light);
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 1rem;
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 1.25rem;
    }

    @media (max-width: 900px) {
      main {
        grid-template-columns: 1fr;
      }
      .sidebar {
        display: none;
      }
    }

    /* Sidebar Filter Panel */
    .sidebar {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .side-box {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem;
      box-shadow: var(--shadow-sm);
    }
    .side-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.65rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .filter-list {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .filter-pill {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.45rem 0.65rem;
      font-size: 0.825rem;
      border-radius: 6px;
      color: var(--text);
      cursor: pointer;
      transition: all 0.15s ease;
      border: 1px solid transparent;
    }
    .filter-pill:hover {
      background-color: var(--bg);
    }
    .filter-pill.active {
      background-color: var(--primary-light);
      color: var(--primary);
      font-weight: 600;
      border-color: var(--primary-light);
    }
    .pill-count {
      font-size: 0.75rem;
      color: var(--text-muted);
      background: var(--bg);
      padding: 0.1rem 0.4rem;
      border-radius: 10px;
    }
    .filter-pill.active .pill-count {
      background: var(--card-bg);
      color: var(--primary);
    }

    /* Search Input */
    .search-input {
      width: 100%;
      padding: 0.5rem 0.75rem;
      font-size: 0.85rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      background-color: var(--bg);
      color: var(--text);
      outline: none;
      transition: border-color 0.15s;
    }
    .search-input:focus {
      border-color: var(--primary);
    }

    /* Content Area */
    .content-area {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    /* Progress Stats Bar */
    .stats-card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.75rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      box-shadow: var(--shadow-sm);
    }
    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .stat-value {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
    }
    .stat-label {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    .progress-bar-wrap {
      flex: 1;
      height: 8px;
      background-color: var(--bg);
      border-radius: 4px;
      overflow: hidden;
      margin: 0 1rem;
    }
    .progress-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--primary) 0%, #a855f7 100%);
      width: 0%;
      transition: width 0.3s ease;
    }

    /* Main Question Card */
    .question-card {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
    }
    .q-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      margin-bottom: 1rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--border);
    }
    .meta-tags {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .badge-term {
      background-color: var(--primary-light);
      color: var(--primary);
    }
    .badge-module {
      background-color: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
    }
    .badge-type {
      background-color: var(--success-light);
      color: #065f46;
    }
    .badge-type-mock {
      background-color: var(--warning-light);
      color: #92400e;
    }

    .q-body {
      font-size: 1.05rem;
      line-height: 1.75;
      margin-bottom: 1.5rem;
      word-break: break-word;
    }

    /* Options */
    .options-list {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }
    .opt-item {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      padding: 0.85rem 1rem;
      border-radius: 8px;
      border: 1.5px solid var(--border);
      background-color: var(--card-bg);
      cursor: pointer;
      transition: all 0.15s ease;
      font-size: 0.95rem;
      line-height: 1.5;
    }
    .opt-item:hover {
      border-color: var(--primary);
      background-color: var(--primary-light);
    }
    .opt-letter {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 26px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.85rem;
      background-color: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
      flex-shrink: 0;
    }
    .opt-text {
      flex: 1;
    }

    /* Option States */
    .opt-item.selected-correct {
      border-color: var(--success);
      background-color: var(--success-light);
    }
    .opt-item.selected-correct .opt-letter {
      background-color: var(--success);
      color: #ffffff;
      border-color: var(--success);
    }
    .opt-item.selected-wrong {
      border-color: var(--danger);
      background-color: var(--danger-light);
    }
    .opt-item.selected-wrong .opt-letter {
      background-color: var(--danger);
      color: #ffffff;
      border-color: var(--danger);
    }
    .opt-item.show-correct {
      border-color: var(--success);
      background-color: var(--success-light);
    }
    .opt-item.show-correct .opt-letter {
      background-color: var(--success);
      color: #ffffff;
      border-color: var(--success);
    }

    /* Feedback Banner */
    .result-banner {
      display: none;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.95rem;
      margin-bottom: 1.25rem;
      align-items: center;
      justify-content: space-between;
    }
    .result-banner.correct {
      display: flex;
      background-color: var(--success-light);
      color: #065f46;
      border: 1px solid #a7f3d0;
    }
    .result-banner.wrong {
      display: flex;
      background-color: var(--danger-light);
      color: #991b1b;
      border: 1px solid #fecaca;
    }

    /* Explanation Box */
    .explanation-drawer {
      background-color: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      display: none;
      animation: fadeIn 0.2s ease-in;
    }
    .explanation-drawer.show {
      display: block;
    }
    .exp-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .exp-body {
      font-size: 0.95rem;
      line-height: 1.7;
      color: var(--text);
    }

    /* Card Controls Footer */
    .q-controls {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* Typography, Math, and Markdown Elements */
    .math-inline {
      font-family: var(--math-font);
      font-style: italic;
      padding: 0 0.15rem;
    }
    .math-block {
      margin: 0.75rem 0;
      padding: 0.75rem 1rem;
      background: var(--card-bg);
      border-left: 3px solid var(--primary);
      border-radius: 4px;
      text-align: center;
      font-family: var(--math-font);
      font-size: 1.05rem;
      overflow-x: auto;
    }
    .frac {
      display: inline-flex;
      flex-direction: column;
      vertical-align: middle;
      text-align: center;
      padding: 0 0.2rem;
      font-size: 0.88em;
      line-height: 1.1;
    }
    .frac-num {
      border-bottom: 1.5px solid currentColor;
      padding-bottom: 1px;
    }
    .frac-den {
      padding-top: 1px;
    }
    .kbd-inline {
      background: var(--bg);
      border: 1px solid var(--border);
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
      font-family: monospace;
      font-size: 0.85em;
    }
    .quiz-ul {
      margin: 0.5rem 0 0.75rem 1.25rem;
      padding-left: 0.5rem;
    }
    .quiz-li {
      margin-bottom: 0.35rem;
      line-height: 1.65;
    }
    .quiz-p {
      margin-bottom: 0.6rem;
      line-height: 1.65;
    }

    /* Modal Sheet Grid */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(2px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 100;
    }
    .modal-overlay.show {
      display: flex;
    }
    .modal-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      width: 90%;
      max-width: 780px;
      max-height: 80vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
    }
    .modal-header {
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .modal-body {
      padding: 1rem 1.25rem;
      overflow-y: auto;
    }
    .sheet-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(42px, 1fr));
      gap: 0.5rem;
    }
    .sheet-bubble {
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      border: 1px solid var(--border);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      background: var(--bg);
      transition: all 0.15s ease;
    }
    .sheet-bubble:hover {
      border-color: var(--primary);
    }
    .sheet-bubble.correct {
      background: var(--success);
      color: #fff;
      border-color: var(--success);
    }
    .sheet-bubble.wrong {
      background: var(--danger);
      color: #fff;
      border-color: var(--danger);
    }
    .sheet-bubble.current {
      box-shadow: 0 0 0 2px var(--primary);
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-4px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="header-content">
      <div class="brand">
        <span class="brand-icon">🏛️</span>
        <div>
          <div class="brand-title">软考高级·系统架构设计师 刷题站</div>
          <div class="brand-subtitle">历年官方真题 + 模拟卷 · 离线单文件全解</div>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn" id="btn-theme" title="切换暗黑模式">🌓 主题</button>
        <button class="btn" id="btn-sheet">📑 答题卡</button>
        <button class="btn" id="btn-reset" title="清空本机刷题记录">🗑️ 重置</button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main>
    <!-- Sidebar: Filters -->
    <aside class="sidebar">
      <div class="side-box">
        <div class="side-title">🔍 关键词搜索</div>
        <input type="text" id="search-input" class="search-input" placeholder="输入题干、考点或选项...">
      </div>

      <div class="side-box">
        <div class="side-title">
          <span>📅 考期筛选</span>
        </div>
        <div class="filter-list" id="term-filters">
          <!-- Filled by JS -->
        </div>
      </div>

      <div class="side-box">
        <div class="side-title">
          <span>🏛️ 考点模块</span>
        </div>
        <div class="filter-list" id="module-filters">
          <!-- Filled by JS -->
        </div>
      </div>

      <div class="side-box">
        <div class="side-title">📌 状态过滤</div>
        <div class="filter-list" id="status-filters">
          <div class="filter-pill active" data-status="all">全部题目 <span class="pill-count" id="count-all">0</span></div>
          <div class="filter-pill" data-status="unanswered">未作答 <span class="pill-count" id="count-unanswered">0</span></div>
          <div class="filter-pill" data-status="wrong">错题本 <span class="pill-count" id="count-wrong">0</span></div>
          <div class="filter-pill" data-status="starred">标星收藏 <span class="pill-count" id="count-starred">0</span></div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <section class="content-area">
      <!-- Stats Bar -->
      <div class="stats-card">
        <div class="stat-item">
          <div class="stat-value" id="stat-progress">0 / 0</div>
          <div class="stat-label">当前进度</div>
        </div>
        <div class="progress-bar-wrap">
          <div class="progress-bar-fill" id="progress-fill"></div>
        </div>
        <div class="stat-item">
          <div class="stat-value" style="color:var(--success);" id="stat-correct">0</div>
          <div class="stat-label">正确数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value" style="color:var(--danger);" id="stat-wrong">0</div>
          <div class="stat-label">错题数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value" id="stat-rate">0%</div>
          <div class="stat-label">正确率</div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="question-card" id="q-card">
        <div class="q-meta">
          <div class="meta-tags">
            <span class="badge badge-term" id="meta-term">2024年下半年</span>
            <span class="badge badge-module" id="meta-module">系统架构设计</span>
            <span class="badge badge-type" id="meta-type">真题</span>
            <span class="badge" style="background:var(--bg); color:var(--text-muted);" id="meta-index">#1</span>
          </div>
          <button class="btn btn-star" id="btn-star" title="收藏此题 (快捷键 S)">⭐ 收藏</button>
        </div>

        <!-- Question Body -->
        <div class="q-body" id="q-body">
          题目加载中...
        </div>

        <!-- Options Container -->
        <div class="options-list" id="options-container">
          <!-- Filled by JS -->
        </div>

        <!-- Answer Result Banner -->
        <div class="result-banner" id="result-banner">
          <span id="banner-text"></span>
          <span style="font-size:0.85rem; font-weight:normal;" id="banner-ans"></span>
        </div>

        <!-- Explanation Box -->
        <div class="explanation-drawer" id="exp-drawer">
          <div class="exp-title">💡 考点解析与推导：</div>
          <div class="exp-body" id="exp-body"></div>
        </div>

        <!-- Card Controls -->
        <div class="q-controls">
          <button class="btn" id="btn-toggle-exp">💡 查看解析</button>
          <div class="nav-actions">
            <button class="btn" id="btn-prev" title="上一题 (←)">上一题</button>
            <button class="btn btn-primary" id="btn-next" title="下一题 (→)">下一题</button>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Answer Sheet Modal -->
  <div class="modal-overlay" id="modal-sheet">
    <div class="modal-card">
      <div class="modal-header">
        <div style="font-weight:700;">📑 答题卡导航</div>
        <button class="btn" id="btn-close-sheet">✕ 关闭</button>
      </div>
      <div class="modal-body">
        <div class="sheet-grid" id="sheet-grid"></div>
      </div>
    </div>
  </div>

  <!-- Question Bank Embedded Data -->
  <script>
    const ALL_QUESTIONS = """ + questions_json + """;
  </script>

  <!-- Rich Renderer Engine -->
  <script>
    const RichRenderer = {
      formatMath(mathStr) {
        let s = mathStr;
        const syms = [
          [/\\Theta/g, 'Θ'], [/\\alpha/g, 'α'], [/\\beta/g, 'β'], [/\\gamma/g, 'γ'],
          [/\\delta/g, 'δ'], [/\\lambda/g, 'λ'], [/\\mu/g, 'μ'], [/\\sigma/g, 'σ'],
          [/\\omega/g, 'ω'], [/\\pi/g, 'π'],
          [/\\implies/g, ' ⇒ '], [/\\to/g, ' → '], [/\\times/g, ' × '], [/\\div/g, ' ÷ '],
          [/\\le/g, ' ≤ '], [/\\ge/g, ' ≥ '], [/\\ne/g, ' ≠ '], [/\\approx/g, ' ≈ '],
          [/\\in/g, ' ∈ '], [/\\notin/g, ' ∉ '], [/\\cup/g, ' ∪ '], [/\\cap/g, ' ∩ '],
          [/\\cdot/g, ' · '], [/\\pm/g, ' ± '], [/\\mid/g, ' | ']
        ];
        syms.forEach(([re, rep]) => { s = s.replace(re, rep); });

        s = s.replace(/\\mathbf\{([^}]+)\}/g, '<strong>$1</strong>');
        s = s.replace(/\\mathit\{([^}]+)\}/g, '<em>$1</em>');
        s = s.replace(/\\text\{([^}]+)\}/g, '$1');

        // Fractions
        s = s.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '<span class="frac"><span class="frac-num">$1</span><span class="frac-den">$2</span></span>');

        // Logarithms
        s = s.replace(/\\log_([a-zA-Z0-9]+)/g, 'log<sub>$1</sub>');
        s = s.replace(/\\log_\{([^}]+)\}/g, 'log<sub>$1</sub>');
        s = s.replace(/\\log/g, 'log');

        // Subscripts & Superscripts
        s = s.replace(/_\{([^}]+)\}/g, '<sub>$1</sub>');
        s = s.replace(/_([a-zA-Z0-9])/g, '<sub>$1</sub>');
        s = s.replace(/\\^\{([^}]+)\}/g, '<sup>$1</sup>');
        s = s.replace(/\\^([a-zA-Z0-9])/g, '<sup>$1</sup>');

        return '<span class="math-inline">' + s + '</span>';
      },

      renderText(raw) {
        if (!raw) return '';
        let text = raw;

        // Block math $$...$$
        text = text.replace(/\\$\\$([\\s\\S]*?)\\$\\$/g, (m, c) => {
          return '<div class="math-block">' + this.formatMath(c.trim()) + '</div>';
        });

        // Inline math $...$
        text = text.replace(/\\$([^$\\n]+?)\\$/g, (m, c) => {
          return this.formatMath(c.trim());
        });

        // Bold & Code
        text = text.replace(/\\*\\*([^\\*\\n]+?)\\*\\*/g, '<strong>$1</strong>');
        text = text.replace(/`([^`\\n]+?)`/g, '<code class="kbd-inline">$1</code>');

        return text;
      },

      renderMarkdown(md) {
        if (!md) return '<p style="color:var(--text-muted);">（暂无解析）</p>';
        const rawLines = md.split('\\n');
        let out = [];
        let inList = false;

        const closeList = () => {
          if (inList) { out.push('</ul>'); inList = false; }
        };

        for (let i = 0; i < rawLines.length; i++) {
          let line = rawLines[i].trim();
          if (!line) { closeList(); continue; }

          // Bullet list items
          const listMatch = line.match(/^[-*]\\s+(.*)$/);
          if (listMatch) {
            let content = listMatch[1].trim();
            if (!content || content === '**' || content === '*') continue;
            if (!inList) { out.push('<ul class="quiz-ul">'); inList = true; }
            out.push('<li class="quiz-li">' + this.renderText(content) + '</li>');
            continue;
          } else {
            closeList();
          }

          // Block math
          if (line.startsWith('$$') && line.endsWith('$$')) {
            out.push('<div class="math-block">' + this.formatMath(line.slice(2, -2).trim()) + '</div>');
          } else {
            out.push('<p class="quiz-p">' + this.renderText(line) + '</p>');
          }
        }

        closeList();
        return out.join('');
      }
    };
  </script>

  <!-- Quiz Engine Logic -->
  <script>
    (function() {
      // LocalStorage Key
      const STORAGE_KEY = 'ruankao_architect_quiz_state_v1';
      let userState = {
        answered: {},    // id -> { choice: 'A', correct: true/false }
        stars: {}        // id -> true/false
      };

      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) userState = JSON.parse(saved);
      } catch(e) {}

      function saveState() {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(userState));
        } catch(e) {}
      }

      // App Filter State
      let currentTerm = 'all';
      let currentModule = 'all';
      let currentStatus = 'all';
      let searchQuery = '';
      let filteredList = [...ALL_QUESTIONS];
      let currentIndex = 0;

      // DOM Elements
      const termFiltersContainer = document.getElementById('term-filters');
      const moduleFiltersContainer = document.getElementById('module-filters');
      const statusFilters = document.querySelectorAll('#status-filters .filter-pill');
      const searchInput = document.getElementById('search-input');

      const statProgress = document.getElementById('stat-progress');
      const statCorrect = document.getElementById('stat-correct');
      const statWrong = document.getElementById('stat-wrong');
      const statRate = document.getElementById('stat-rate');
      const progressFill = document.getElementById('progress-fill');

      const countAll = document.getElementById('count-all');
      const countUnanswered = document.getElementById('count-unanswered');
      const countWrong = document.getElementById('count-wrong');
      const countStarred = document.getElementById('count-starred');

      const metaTerm = document.getElementById('meta-term');
      const metaModule = document.getElementById('meta-module');
      const metaType = document.getElementById('meta-type');
      const metaIndex = document.getElementById('meta-index');
      const btnStar = document.getElementById('btn-star');

      const qBody = document.getElementById('q-body');
      const optContainer = document.getElementById('options-container');
      const resultBanner = document.getElementById('result-banner');
      const bannerText = document.getElementById('banner-text');
      const bannerAns = document.getElementById('banner-ans');
      const expDrawer = document.getElementById('exp-drawer');
      const expBody = document.getElementById('exp-body');

      const btnToggleExp = document.getElementById('btn-toggle-exp');
      const btnPrev = document.getElementById('btn-prev');
      const btnNext = document.getElementById('btn-next');
      const btnSheet = document.getElementById('btn-sheet');
      const modalSheet = document.getElementById('modal-sheet');
      const sheetGrid = document.getElementById('sheet-grid');
      const btnCloseSheet = document.getElementById('btn-close-sheet');
      const btnReset = document.getElementById('btn-reset');
      const btnTheme = document.getElementById('btn-theme');

      // Build Filter Lists
      function initFilters() {
        // Terms Grouping
        const termGroups = [
          { key: 'all', label: '全部真题与模拟', filter: () => true },
          { key: '2025', label: '🌟 2025年最新真题', filter: q => q.term.includes('2025') },
          { key: '2024', label: '📅 2024年统考真题', filter: q => q.term.includes('2024') },
          { key: '2023', label: '🚀 2023年新大纲真题', filter: q => q.term.includes('2023') },
          { key: '2020-2022', label: '📜 2020-2022年历年真题', filter: q => ['2020', '2021', '2022'].some(y => q.term.includes(y)) },
          { key: '2014-2018', label: '📚 2014-2018年经典真题', filter: q => ['2014','2015','2016','2017','2018'].some(y => q.term.includes(y)) },
          { key: 'mock', label: '🎯 考前冲刺模拟卷', filter: q => q.sourceType === 'mock' }
        ];

        termFiltersContainer.innerHTML = '';
        termGroups.forEach(g => {
          const count = ALL_QUESTIONS.filter(g.filter).length;
          const div = document.createElement('div');
          div.className = `filter-pill ${g.key === 'all' ? 'active' : ''}`;
          div.dataset.term = g.key;
          div.innerHTML = `<span>${g.label}</span><span class="pill-count">${count}</span>`;
          div.addEventListener('click', () => {
            termFiltersContainer.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            div.classList.add('active');
            currentTerm = g.key;
            applyFilters();
          });
          termFiltersContainer.appendChild(div);
        });

        // Module Filters
        const modMap = {};
        ALL_QUESTIONS.forEach(q => {
          modMap[q.module_code] = (modMap[q.module_code] || 0) + 1;
        });

        moduleFiltersContainer.innerHTML = '';
        const allModDiv = document.createElement('div');
        allModDiv.className = 'filter-pill active';
        allModDiv.dataset.module = 'all';
        allModDiv.innerHTML = `<span>全部模块</span><span class="pill-count">${ALL_QUESTIONS.length}</span>`;
        allModDiv.addEventListener('click', () => {
          moduleFiltersContainer.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
          allModDiv.classList.add('active');
          currentModule = 'all';
          applyFilters();
        });
        moduleFiltersContainer.appendChild(allModDiv);

        Object.keys(modMap).sort((a,b) => modMap[b] - modMap[a]).forEach(k => {
          const sample = ALL_QUESTIONS.find(q => q.module_code === k);
          const name = sample ? sample.module_name : k;
          const div = document.createElement('div');
          div.className = 'filter-pill';
          div.dataset.module = k;
          div.innerHTML = `<span>${name}</span><span class="pill-count">${modMap[k]}</span>`;
          div.addEventListener('click', () => {
            moduleFiltersContainer.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            div.classList.add('active');
            currentModule = k;
            applyFilters();
          });
          moduleFiltersContainer.appendChild(div);
        });
      }

      function updateStatusCounts() {
        const total = ALL_QUESTIONS.length;
        const answeredIds = Object.keys(userState.answered);
        const wrongCount = answeredIds.filter(id => !userState.answered[id].correct).length;
        const starCount = Object.keys(userState.stars).filter(id => userState.stars[id]).length;
        const unansweredCount = total - answeredIds.length;

        countAll.textContent = total;
        countUnanswered.textContent = unansweredCount;
        countWrong.textContent = wrongCount;
        countStarred.textContent = starCount;
      }

      function applyFilters() {
        filteredList = ALL_QUESTIONS.filter(q => {
          // Term
          if (currentTerm === '2025' && !q.term.includes('2025')) return false;
          if (currentTerm === '2024' && !q.term.includes('2024')) return false;
          if (currentTerm === '2023' && !q.term.includes('2023')) return false;
          if (currentTerm === '2020-2022' && !['2020', '2021', '2022'].some(y => q.term.includes(y))) return false;
          if (currentTerm === '2014-2018' && !['2014','2015','2016','2017','2018'].some(y => q.term.includes(y))) return false;
          if (currentTerm === 'mock' && q.sourceType !== 'mock') return false;

          // Module
          if (currentModule !== 'all' && q.module_code !== currentModule) return false;

          // Status
          const ans = userState.answered[q.id];
          const isStarred = !!userState.stars[q.id];
          if (currentStatus === 'unanswered' && ans) return false;
          if (currentStatus === 'wrong' && (!ans || ans.correct)) return false;
          if (currentStatus === 'starred' && !isStarred) return false;

          // Search
          if (searchQuery) {
            const query = searchQuery.toLowerCase();
            const inStem = q.stem.toLowerCase().includes(query);
            const inOpts = Object.values(q.options).some(t => t.toLowerCase().includes(query));
            const inAnalysis = q.analysis.toLowerCase().includes(query);
            if (!inStem && !inOpts && !inAnalysis) return false;
          }

          return true;
        });

        currentIndex = 0;
        renderQuestion();
        updateStats();
      }

      function renderQuestion() {
        if (filteredList.length === 0) {
          qBody.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 2rem;">没有找到符合当前筛选条件的题目。<br>可尝试切换分类、清空搜索框或切回“全部题目”。</p>';
          optContainer.innerHTML = '';
          resultBanner.style.display = 'none';
          expDrawer.classList.remove('show');
          metaTerm.textContent = '--';
          metaModule.textContent = '--';
          metaIndex.textContent = '#0';
          btnStar.classList.remove('active');
          return;
        }

        const q = filteredList[currentIndex];
        const ansRecord = userState.answered[q.id];
        const isStarred = !!userState.stars[q.id];

        // Meta tags
        metaTerm.textContent = q.term;
        metaModule.textContent = q.module_name;
        metaType.textContent = q.sourceType === 'real' ? '真题' : '模拟';
        metaType.className = `badge ${q.sourceType === 'real' ? 'badge-type' : 'badge-type-mock'}`;
        metaIndex.textContent = `#${currentIndex + 1} / ${filteredList.length}`;
        btnStar.classList.toggle('active', isStarred);

        // Body
        qBody.innerHTML = RichRenderer.renderText(q.stem);

        // Options
        optContainer.innerHTML = '';
        const keys = ['A', 'B', 'C', 'D'];
        keys.forEach(k => {
          if (!q.options[k]) return;
          const optDiv = document.createElement('div');
          optDiv.className = 'opt-item';

          if (ansRecord) {
            if (ansRecord.choice === k) {
              optDiv.classList.add(ansRecord.correct ? 'selected-correct' : 'selected-wrong');
            }
            if (k === q.answer && !ansRecord.correct) {
              optDiv.classList.add('show-correct');
            }
          }

          optDiv.innerHTML = `
            <div class="opt-letter">${k}</div>
            <div class="opt-text">${RichRenderer.renderText(q.options[k])}</div>
          `;

          optDiv.addEventListener('click', () => chooseOption(k));
          optContainer.appendChild(optDiv);
        });

        // Banner & Explanation
        if (ansRecord) {
          resultBanner.className = `result-banner ${ansRecord.correct ? 'correct' : 'wrong'}`;
          resultBanner.style.display = 'flex';
          bannerText.textContent = ansRecord.correct ? '🎉 回答正确！' : `❌ 回答错误！正确答案是【 ${q.answer} 】`;
          bannerAns.textContent = `你的选择: ${ansRecord.choice}`;
          expDrawer.classList.add('show');
          btnToggleExp.textContent = '🙈 折叠解析';
        } else {
          resultBanner.style.display = 'none';
          expDrawer.classList.remove('show');
          btnToggleExp.textContent = '💡 查看解析';
        }

        expBody.innerHTML = RichRenderer.renderMarkdown(q.analysis);

        // Nav Buttons
        btnPrev.disabled = currentIndex <= 0;
        btnNext.disabled = currentIndex >= filteredList.length - 1;
      }

      function chooseOption(letter) {
        const q = filteredList[currentIndex];
        const isCorrect = letter === q.answer;
        userState.answered[q.id] = {
          choice: letter,
          correct: isCorrect,
          answeredAt: Date.now()
        };
        saveState();
        renderQuestion();
        updateStats();
        updateStatusCounts();
      }

      function updateStats() {
        const total = filteredList.length;
        let answeredCount = 0;
        let correctCount = 0;

        filteredList.forEach(q => {
          const ans = userState.answered[q.id];
          if (ans) {
            answeredCount++;
            if (ans.correct) correctCount++;
          }
        });

        const wrongCount = answeredCount - correctCount;
        const rate = answeredCount > 0 ? Math.round((correctCount / answeredCount) * 100) : 0;

        statProgress.textContent = `${currentIndex + 1} / ${total}`;
        statCorrect.textContent = correctCount;
        statWrong.textContent = wrongCount;
        statRate.textContent = `${rate}%`;

        const pct = total > 0 ? ((currentIndex + 1) / total) * 100 : 0;
        progressFill.style.width = `${pct}%`;
      }

      function openSheet() {
        sheetGrid.innerHTML = '';
        filteredList.forEach((q, idx) => {
          const div = document.createElement('div');
          div.className = 'sheet-bubble';
          div.textContent = idx + 1;
          const ans = userState.answered[q.id];
          if (ans) {
            div.classList.add(ans.correct ? 'correct' : 'wrong');
          }
          if (idx === currentIndex) {
            div.classList.add('current');
          }
          div.addEventListener('click', () => {
            currentIndex = idx;
            renderQuestion();
            updateStats();
            modalSheet.classList.remove('show');
          });
          sheetGrid.appendChild(div);
        });
        modalSheet.classList.add('show');
      }

      // Event Listeners
      statusFilters.forEach(pill => {
        pill.addEventListener('click', () => {
          statusFilters.forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          currentStatus = pill.dataset.status;
          applyFilters();
        });
      });

      let searchTimer = null;
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => {
          searchQuery = e.target.value.trim();
          applyFilters();
        }, 250);
      });

      btnStar.addEventListener('click', () => {
        if (filteredList.length === 0) return;
        const q = filteredList[currentIndex];
        const nextState = !userState.stars[q.id];
        userState.stars[q.id] = nextState;
        saveState();
        btnStar.classList.toggle('active', nextState);
        updateStatusCounts();
      });

      btnPrev.addEventListener('click', () => {
        if (currentIndex > 0) {
          currentIndex--;
          renderQuestion();
          updateStats();
        }
      });

      btnNext.addEventListener('click', () => {
        if (currentIndex < filteredList.length - 1) {
          currentIndex++;
          renderQuestion();
          updateStats();
        }
      });

      btnToggleExp.addEventListener('click', () => {
        const isShow = expDrawer.classList.toggle('show');
        btnToggleExp.textContent = isShow ? '🙈 折叠解析' : '💡 查看解析';
      });

      btnSheet.addEventListener('click', openSheet);
      btnCloseSheet.addEventListener('click', () => modalSheet.classList.remove('show'));
      modalSheet.addEventListener('click', (e) => {
        if (e.target === modalSheet) modalSheet.classList.remove('show');
      });

      btnReset.addEventListener('click', () => {
        if (confirm('确定要清空所有的作答记录与收藏记录吗？此操作无法撤销。')) {
          userState = { answered: {}, stars: {} };
          saveState();
          renderQuestion();
          updateStats();
          updateStatusCounts();
        }
      });

      // Theme toggle
      btnTheme.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
        try { localStorage.setItem('theme_mode', isDark ? 'light' : 'dark'); } catch(e) {}
      });

      try {
        const savedTheme = localStorage.getItem('theme_mode');
        if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);
      } catch(e) {}

      // Keyboard Shortcuts
      window.addEventListener('keydown', (e) => {
        if (['input', 'textarea'].includes(document.activeElement.tagName.toLowerCase())) return;
        const key = e.key.toUpperCase();
        if (['A', 'B', 'C', 'D'].includes(key)) {
          chooseOption(key);
        } else if (e.key === 'ArrowLeft' || key === 'H') {
          btnPrev.click();
        } else if (e.key === 'ArrowRight' || key === 'L') {
          btnNext.click();
        } else if (e.key === ' ' || key === 'P') {
          e.preventDefault();
          btnToggleExp.click();
        } else if (key === 'S') {
          btnStar.click();
        }
      });

      // Init
      initFilters();
      updateStatusCounts();
      applyFilters();
    })();
  </script>
</body>
</html>"""
    return html_template


def main():
    print(f"Loading questions from: {BANK_FILE}")
    questions = load_questions()
    print(f"Loaded {len(questions)} architect questions.")
    
    html_content = generate_html(questions)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"Generated single-file offline architect quiz app: {OUTPUT_HTML}")
    print(f"File size: {len(html_content.encode('utf-8')) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
