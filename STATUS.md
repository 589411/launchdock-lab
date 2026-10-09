# STATUS — launchdock-lab

> 單一真相。每次離開前更新（全域憲法收尾鐵律）。
**最後更新：** 2026-10-10
**整體狀態：** 🟢 進行中

## 一句話現況
課堂 AI 實例庫（資料驅動）。modules.yaml v3（M01–M09）已定稿；主站文章已可掛 `modules` 欄位並用
`npm run handout M0x` 抽組講義（講義線已打通）。covers 部署死結已修。**2026-10-10 起有英文版 lab.launchdock.app/en/**（同一份 yaml、條目 `en` 區塊）。

## 下一個具體動作 ⭐
補回 3 筆因 REPLACE 佔位符被 archived 的條目連結（gas-line-push、n8n-article-pipeline、openclaw），
填實際 URL 後把 status 改回 active。validate.py 現在會硬擋 active 條目的 REPLACE。

## 怎麼驗證這一步成功
`python3 scripts/validate.py` 通過且 active 數從 16 回到 19；push 後 lab.launchdock.app 卡片恢復。

## 卡點 / 待你決定
- gas-line-push 的 LINE 官方帳號連結與影片、n8n-article-pipeline 的影片、openclaw 的公開 repo URL——只有你有。

## 進度脈絡（新的在上）
- 2026-10-10 **英文版上線** `/en/`：projects.yaml 每筆加選填 `en`（title/summary/description/tomorrow/labels，18 筆 active 全補）；build.py 同時產 `dist/index.html` 與 `dist/en/index.html`，缺 en 退回中文；模板文字改 `{{佔位}}`＋右上中英切換＋hreflang；validate 檢 labels 數＝links 數、缺 en 警告；CLAUDE.md／lab-publish skill 已補規則。390px 實測無橫捲（英文篩選鈕原本會撐破，已加 flex-wrap）。deploy success，`/`、`/en/` 皆 200、18 張卡
  - 坑：headless Chrome `--window-size=390` 實際最小寬約 500，截圖會「看起來」橫捲；要驗手機寬用 390px iframe 包起來截
- 2026-10-05 hey-o-english 文案改為四級系列＋agy 流水線（level 2→3、modules 加 M09、platforms 加 Antigravity）；刪舊封面讓 Auto Covers 重截四級版首頁，轉 webp。
- 2026-10-05 新增 hey-o-english（🎧 Hey-O! 英聽口說，website/教學/L2，M02+M01，hey-o.launchdock.app）；Auto Covers 截圖後轉 webp 210KB、刪 PNG。validate 21 筆通過、deploy success、線上卡片與 `/covers/hey-o-english.webp` 皆 200（注意封面線上路徑是 `/covers/` 不是 `/assets/covers/`）
- 2026-09-03 新增 story-pipeline-spec（🎬 故事拆短片 — 可稽核的生成流程規格，repo/自動化/L3，M09+M01）；**M09（AI 內容與多媒體生成）的第一筆 demo**，此前 example_demos 是空的。封面是照該規格實跑 U-108 產出的四張劇照 2×2（同一角色跨四鏡，外型隨敘事改變但臉沒變），1600x900 webp 201KB。validate 20 筆通過、deploy success、線上實測卡片與封面皆 200
- 2026-08-15 新增 violin-lesson-analyse（🎻 女兒的小提琴課，repo/生活/L3，M05+M01）；封面用演講簡報 slide-5，壓成 webp 59KB（原 PNG 1005KB）。validate 19 筆通過、deploy 成功、卡片與封面已上線（16 張卡）
- 2026-08-15 全部封面轉 webp：14.5MB → 1.8MB（-88%，`cwebp -q 85`，尺寸不變、文字無糊化）。deploy 成功、14 張封面線上實測 200
  - 慣例：**封面圖一律先壓成 webp 再進 repo**（`cwebp -q 85`，約 50–200KB）。換副檔名時舊檔要 `git rm`，否則 repo 留兩份
  - screenshot.py 的 `has_cover()` 已認得 .webp，Auto Covers 不會把 PNG 補回來
- 2026-08-04 新增 sunlit-retail（🌤 日晴生活，website/資料/L2，sunlit.launchdock.app）；工研院課程教學範例，含模擬後台匯出動線。validate 18 筆通過、已 push
- 2026-07-19 header 加「← 回藍鴨 Launchdock 主站」導流 pill（templates/page.html）；push 後 CI 重建 dist 上線
- 2026-07-12 新增 swing-lab（🥁 爵士鼓節奏訓練場，website/遊戲/L2，swing.launchdock.app）；deploy 成功、卡片已上線
- 2026-07-05 修 covers.yml：截圖 commit 後自動 `gh workflow run deploy.yml`（解防遞迴死結）
- 2026-07-05 validate.py 新增 REPLACE 佔位符硬檢查；3 筆佔位條目暫轉 archived
- 2026-07-05 建 `.claude/skills/lab-publish/`（README 宣稱已久但一直不存在）
- 2026-07-05 刪除 `{data,assets` 死目錄（bash brace expansion 失誤產物）
- 2026-06-19 modules.yaml v3 與 Joseph review 定稿（M01–M09）
- 2026-06-14 gas-ordering 新增架構說明封面圖
- 2026-06-13 改名「藍鴨實驗室」、新增 mes-n-mfa demo

## 已知坑
- 只改 data/ 與 assets/covers/，dist/ 是產物。改完必跑 validate.py。
- `.DS_Store` 不該進 git，建議加進 .gitignore。
- ~~covers 截圖後封面不會自動上線~~ 已修（covers.yml 會自動觸發 deploy）。手動補截仍可用：
  `gh workflow run covers.yml -f force_id=<id>`。
- **帳號**：repo 屬 GitHub `589411`；本機 gh active 常是 `launchdockapp-beep`，push/dispatch 前先
  `gh auth switch --user 589411`，完再切回。
