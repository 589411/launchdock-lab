# STATUS — launchdock-lab

> 單一真相。每次離開前更新（全域憲法收尾鐵律）。
**最後更新：** 2026-06-19
**整體狀態：** 🟢 進行中

## 一句話現況
課堂 AI 實例庫（資料驅動，14 commits）。展示面成熟，但「教學複用」面尚未啟動——
`modules` 課程模組欄位全庫只用過 M03。

## 下一個具體動作 ⭐
啟動教學複用（見 dev-harness/LAUNCHDOCK-LAB-PLAN.md 步驟 1）：
建 `data/modules.yaml` 定義 M01–M13 模組地圖。先確認 M01–M13 的權威來源
（openclaw教案大綱 or booking-system/launchdock-student-plan.jsx），再草擬給 Joseph 確認。

## 怎麼驗證這一步成功
`python scripts/validate.py` 通過；modules.yaml 的 id 與 projects.yaml 既有 modules 引用一致。

## 卡點 / 待你決定
- M01–M13 的正式定義以哪份為準？（課程 30 集是另一套結構，需對齊）
- README 提到的 `.claude/skills/lab-publish/` 目前 repo 內找不到，需確認是否遺失。

## 進度脈絡（新的在上）
- 2026-06-19 起草此 STATUS
- 2026-06-14 gas-ordering 新增架構說明封面圖
- 2026-06-13 改名「藍鴨實驗室」、新增 mes-n-mfa demo

## 已知坑
- 只改 data/ 與 assets/covers/，dist/ 是產物。改完必跑 validate.py。
- `.DS_Store` 不該進 git，建議加進 .gitignore。
- **covers 工作流截圖後封面不會自動上線**：它用 Actions 內建 `GITHUB_TOKEN` commit/push，不觸發 deploy.yml（GitHub 防遞迴），dist 不重建、線上仍是舊 SVG 佔位圖。解法：`gh workflow run covers.yml -f force_id=<id>` 完成後，再 `gh workflow run deploy.yml` 手動重建。
- **帳號**：repo 屬 GitHub `589411`；本機 gh active 常是 `launchdockapp-beep`，push/dispatch 前先 `gh auth switch --user 589411`，完再切回。
