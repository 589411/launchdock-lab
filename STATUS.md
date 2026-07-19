# STATUS — launchdock-lab

> 單一真相。每次離開前更新（全域憲法收尾鐵律）。
**最後更新：** 2026-07-12
**整體狀態：** 🟢 進行中

## 一句話現況
課堂 AI 實例庫（資料驅動）。modules.yaml v3（M01–M09）已定稿；主站文章已可掛 `modules` 欄位並用
`npm run handout M0x` 抽組講義（講義線已打通）。covers 部署死結已修。

## 下一個具體動作 ⭐
補回 3 筆因 REPLACE 佔位符被 archived 的條目連結（gas-line-push、n8n-article-pipeline、openclaw），
填實際 URL 後把 status 改回 active。validate.py 現在會硬擋 active 條目的 REPLACE。

## 怎麼驗證這一步成功
`python scripts/validate.py` 通過且 active 數回到 15；push 後 lab.launchdock.app 卡片恢復。

## 卡點 / 待你決定
- gas-line-push 的 LINE 官方帳號連結與影片、n8n-article-pipeline 的影片、openclaw 的公開 repo URL——只有你有。

## 進度脈絡（新的在上）
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
