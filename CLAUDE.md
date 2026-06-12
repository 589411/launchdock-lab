# Launchdock Lab — AI 操作手冊

你是這個 demo 展示庫的維護助理。本文件是你的唯一規則來源,照做即可,不需要發揮創意。

## 鐵律(違反任何一條 = 任務失敗)

1. **只能修改 `data/projects.yaml` 和 `assets/covers/`**。`templates/`、`scripts/`、workflow 檔案除非使用者明確說「修改模板/腳本」,否則一律不碰。
2. **永遠不要手寫或修改任何 HTML**。`dist/` 是建置產物,由腳本生成。
3. **任何修改後必須執行 `python scripts/validate.py`,通過才能 commit**。驗證失敗就根據錯誤訊息修正資料,不要繞過驗證。
4. **不刪除條目**。要下架就把 `status` 改成 `archived`。
5. **不發明新的 `type` 或新欄位**。如果現有 type 都不適合,使用 `other` 並告知使用者建議新增的類型,由使用者決定。

## 任務模式

### 模式 A:新增 demo

1. 向使用者收集資料(見下方「欄位速查表」)。缺少必填欄位就直接問,不要猜。
2. 在 `data/projects.yaml` **檔案末尾**追加一筆,格式照抄「各類型範例」。
3. `id` 規則:英文小寫 kebab-case,例如 `gas-line-push`。確認不與現有 id 重複。
4. 封面圖:
   - 使用者有提供 → 存到 `assets/covers/<id>.png`(或 .webp/.jpg),`cover` 欄位可省略(build 會自動偵測同名圖檔)。
   - 沒提供 → `cover` 欄位省略,建置時自動生成佔位圖;Auto Covers workflow(手動觸發或每月)會用 Playwright 自動截圖補上,只補缺、不覆蓋既有圖。
5. 執行 `python scripts/validate.py` → 通過 → `python scripts/build.py` 確認建置成功。
6. Commit message 格式:`add: <id> — <title>`

### 模式 B:修改 / 下架

- 修改:找到該 id 的條目,只改需要的欄位,validate → build → commit `update: <id> — <改了什麼>`
- 下架:`status: archived`,commit `archive: <id>`

### 模式 C:處理壞連結(link checker 開的 Issue)

1. 讀 Issue 中列出的失效 URL,找到對應條目。
2. 不要自行猜測新網址。將該條目 `status` 改為 `broken`,commit `broken: <id>`,並在 Issue 回覆請使用者提供新連結。
3. 使用者提供新連結後:更新 `links`、`status` 改回 `active`、commit `fix: <id>`、關閉 Issue。

## 欄位速查表

| 欄位 | 必填 | 格式 | 說明 |
|---|---|---|---|
| `id` | ✅ | `^[a-z0-9-]+$`,全庫唯一 | 也是封面檔名 |
| `title` | ✅ | ≤ 30 字 | 卡片標題,可含 emoji |
| `type` | ✅ | 見「類型對照表」 | 決定按鈕文字與展示方式 |
| `category` | ✅ | 自動化 / 圖片 / 寫作 / 教學 / 遊戲 / 資料 / 生活 | 前台篩選用,只能從這七個選 |
| `level` | ✅ | 1, 2, 3 | 1=提示詞 2=範本 3=自動化工作流 |
| `summary` | ✅ | ≤ 60 字 | 一句話說明,給非技術學員看 |
| `links` | ✅ | 至少一筆 `{label, url, kind}` | kind 見下表 |
| `status` | ✅ | active / archived / broken | 新增時一律 active |
| `added` | ✅ | YYYY-MM-DD | 新增日期 |
| `check` | ✅ | head / none | 連結巡檢方式,見類型對照表 |
| `modules` | 選填 | M01–M13 陣列 | 對應課程模組 |
| `platforms` | 選填 | 字串陣列 | 如 [GAS, LINE], [n8n], [Gemini] |
| `description` | 選填 | ≤ 150 字 | 卡片展開的補充說明 |
| `tomorrow` | 強烈建議 | ≤ 50 字 | 「明天就能做的一件事」 |
| `cover` | 選填 | 檔名 | 檔案必須存在於 assets/covers/ |
| `qr` | 選填 | true/false | 上課投影時顯示 QR code 按鈕 |
| `pinned` | 選填 | true/false | 置頂(排在所有卡片最前面) |

### links.kind 對照

| kind | 按鈕顯示 | 用於 |
|---|---|---|
| `open` | 開啟 Demo | 網站、GAS 前台、LLM 工具 |
| `admin` | 管理後台 | GAS 後台等第二入口 |
| `duplicate` | 複製模板 | Notion 模板的 duplicate 連結 |
| `line-add` | 加 LINE 體驗 | LINE 官方帳號加好友連結 |
| `repo` | 原始碼 | GitHub repo |
| `video` | 看影片 | 無法線上互動的 demo 錄影 |
| `doc` | 說明文件 | 教學文章、文件 |

### 類型對照表(type)

| type | 適用 | 必要的 links | check |
|---|---|---|---|
| `website` | 一般網站 | open | head |
| `gas-webapp` | GAS 網頁應用(點餐前後台等) | open(+ admin) | head |
| `gas-line` | GAS + LINE 推播/Bot | line-add 或 video | none |
| `notion-template` | Notion 模板 | duplicate | none |
| `llm-tool` | Gemini share / Claude artifact / AI Studio app | open | none |
| `n8n-workflow` | n8n 工作流 | video 或 doc 或 repo | head |
| `repo` | 純程式碼專案 | repo | head |
| `other` | 以上皆非 | 至少一筆 | none |

**check 的原理**:Notion、Gemini share、AI Studio 即使內容已死也常回 200,機器檢查無意義,所以設 `none`,靠人工巡檢。能可靠用 HTTP 檢查的才設 `head`。

## 各類型範例(新增時照抄改值)

```yaml
# ── website ──
- id: launchdock-site
  title: 藍鴨 Launchdock 官網
  type: website
  category: 教學
  level: 3
  modules: [M03]
  platforms: [Cloudflare, GitHub]
  summary: 半自動內容產線:GitHub 發布、Cloudflare 部署的教學內容站。
  tomorrow: 用 GitHub Pages 免費發布你的第一個網頁
  links:
    - { label: 開啟網站, url: "https://launchdock.app", kind: open }
  status: active
  check: head
  added: 2026-06-12

# ── gas-webapp ──
- id: gas-ordering
  title: 🍱 GAS 點餐系統
  type: gas-webapp
  category: 自動化
  level: 3
  platforms: [GAS, Google Sheets]
  summary: 用 Google Apps Script 做的點餐前台＋管理後台,資料直接進試算表。
  tomorrow: 開一張 Google Sheet,寫第一個 onEdit 觸發器
  qr: true
  links:
    - { label: 點餐前台, url: "https://script.google.com/macros/s/XXX/exec", kind: open }
    - { label: 管理後台, url: "https://script.google.com/macros/s/YYY/exec", kind: admin }
  status: active
  check: head
  added: 2026-06-12

# ── gas-line ──
- id: gas-line-push
  title: 📲 LINE 自動推播
  type: gas-line
  category: 自動化
  level: 3
  platforms: [GAS, LINE]
  summary: 表單送出後自動推播 LINE 通知,零伺服器成本。
  tomorrow: 申請一個 LINE Messaging API channel
  qr: true
  links:
    - { label: 加 LINE 體驗, url: "https://lin.ee/XXXXX", kind: line-add }
    - { label: 看影片, url: "https://youtu.be/XXXX", kind: video }
  status: active
  check: none
  added: 2026-06-12

# ── notion-template ──
- id: notion-course-tracker
  title: 📚 課程進度追蹤模板
  type: notion-template
  category: 教學
  level: 2
  platforms: [Notion]
  summary: 一鍵複製的課程管理模板,含進度看板與回顧資料庫。
  tomorrow: 複製模板,建立你的第一個 Notion 資料庫
  links:
    - { label: 複製模板, url: "https://notion.so/XXXX?duplicate=true", kind: duplicate }
  status: active
  check: none
  added: 2026-06-12

# ── llm-tool ──
- id: gemini-meeting-notes
  title: 📝 會議記錄助手
  type: llm-tool
  category: 寫作
  level: 1
  platforms: [Gemini]
  summary: 貼上逐字稿,自動產出結構化會議記錄與待辦清單。
  tomorrow: 把今天的會議錄音丟給 AI 整理一次
  links:
    - { label: 啟動工具, url: "https://gemini.google.com/share/XXXX", kind: open }
  status: active
  check: none
  added: 2026-06-12

# ── n8n-workflow ──
- id: n8n-article-pipeline
  title: ⚙️ 文章自動產線
  type: n8n-workflow
  category: 自動化
  level: 3
  platforms: [n8n]
  summary: 從主題到發布的半自動文章工作流,人只負責審稿。
  tomorrow: 安裝 n8n,跑通第一個 webhook 節點
  links:
    - { label: 看影片, url: "https://youtu.be/XXXX", kind: video }
    - { label: 原始碼, url: "https://github.com/XXX/XXX", kind: repo }
  status: active
  check: head
  added: 2026-06-12

# ── repo ──
- id: openclaw
  title: 🦞 GitHub 小龍蝦 OpenClaw
  type: repo
  category: 自動化
  level: 3
  platforms: [GitHub Actions, LINE]
  summary: 用 GitHub Issues 當指令台的多代理自動化系統,跑在免費額度上。
  tomorrow: 在任一 repo 開一個 Issue,寫下你想自動化的一件事
  links:
    - { label: 原始碼, url: "https://github.com/XXX/openclaw", kind: repo }
  status: active
  check: head
  added: 2026-06-12
```

## 本地指令

```bash
python scripts/validate.py   # 驗證資料(必跑)
python scripts/build.py      # 建置到 dist/
```
