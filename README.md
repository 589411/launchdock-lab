# 🦆 Launchdock Lab

藍鴨 Launchdock 的課堂 AI 實例庫。所有 demo(網站、GAS 應用、LINE 自動化、Notion 模板、LLM 小工具、n8n 工作流、開源專案)集中在一個資料檔,自動建置成展示頁。

**這個 repo 本身就是教材**:新增一個 demo = 改五行 YAML → push → 網站自動更新。

## 架構

```
data/projects.yaml   ← 唯一資料來源(人或 AI 只改這裡)
data/schema.json     ← 欄位規則(機器驗證)
scripts/validate.py  ← 驗證:schema、id 唯一、封面存在
scripts/build.py     ← 生成 dist/index.html(無封面自動產佔位圖)
templates/page.html  ← 頁面模板(含篩選、QR code)
CLAUDE.md            ← AI 助理操作手冊(新增/維護/壞連結處理)
.github/workflows/
  deploy.yml         ← push → 驗證 → 建置 → 部署 GitHub Pages
  linkcheck.yml      ← 每週一巡檢連結,失效自動開 Issue
```

## 本地開發

```bash
pip install pyyaml jsonschema
python scripts/validate.py
python scripts/build.py
open dist/index.html
```

## 部署

**GitHub Pages(預設)**:Settings → Pages → Source 選 *GitHub Actions*,push 即部署。

**改用 Cloudflare Pages(建議,可綁 lab.launchdock.app)**:
1. Cloudflare Pages 連接此 repo
2. Build command:`pip install pyyaml jsonschema && python scripts/build.py`
3. Output directory:`dist`
4. 自訂網域加 `lab.launchdock.app`

## 用 AI 維護

把任務丟給 Claude(Sonnet 即可),指示它先讀 `CLAUDE.md`:

> 讀 CLAUDE.md,然後新增一個 demo:Gemini 做的履歷健檢工具,連結是 https://...,分類寫作,Level 1。

## Skill:一句話上架

repo 內建 Claude Code skill(`.claude/skills/lab-publish/`)。在 repo 目錄開 Claude Code,直接說:

> 上架 https://daily-bread.launchdock.app,讀經進度 PWA,repo 在 https://github.com/589411/daily-bread

它會自動:分析網站 → 推斷類型 → 起草條目給你確認 → 驗證 → 建置 → commit → push → 觸發自動截圖。
