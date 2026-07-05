---
name: lab-publish
description: 一句話上架 demo 到 lab.launchdock.app。使用者給一個 URL 加簡短描述,就分析網站、推斷 type/category/level/modules、起草 projects.yaml 條目、驗證、建置、commit。Use when: 上架、新增 demo、加到 lab、publish to lab。
---

# lab-publish — 一句話上架

把使用者給的 URL + 描述變成 `data/projects.yaml` 的一筆合格條目並上線。

## 前提

先讀 `CLAUDE.md`(欄位規範、五項鐵律)與 `data/modules.yaml`(M01–M13 模組定義與邊界決議)。
嚴禁手寫 HTML、嚴禁改 `dist/`。

## 步驟

1. **分析目標**:抓取使用者給的 URL(或讀 repo README),判斷這是什麼、給誰用。
2. **推斷欄位**:
   - `type`:對照 CLAUDE.md 的 type 表(static-site / gas-webapp / gas-line / notion-template / llm-tool / n8n-workflow / repo …)
   - `category`(7 選 1)、`level`(1 提示詞 / 2 範本 / 3 自動化)
   - `modules`:對照 `data/modules.yaml` 的 goal 與邊界決議(如 Gems/GPTs → M01 不是 M03;Firebase → M08)
   - `summary` ≤60 字、`tomorrow` 一句「明天就能做的一件事」
   - `links`:1–4 筆,kind 對照表在 CLAUDE.md。**絕不留 REPLACE 佔位符**——沒有的連結就不要列;
     若必要連結拿不到,把 status 設 archived 並告知使用者缺什麼。
   - `check`:公開 http(s) 頁面用 `head`,LINE/GAS 這類擋 HEAD 的用 `none`
3. **起草給使用者確認**:貼出完整 YAML 條目,等確認再寫入。
4. **寫入並驗證**:append 到 `data/projects.yaml` → `python scripts/validate.py` 必須 exit 0。
5. **建置**:`python scripts/build.py`,確認卡片數 +1。
6. **commit + push**(訊息格式:`lab: 上架 <id>`)。push 後 deploy.yml 自動部署。
7. **封面**:若使用者沒給封面圖,提醒:月初 covers workflow 會自動補截圖,
   或手動觸發 `gh workflow run covers.yml`(截圖後會自動觸發重新部署)。

## 驗收

- validate.py exit 0、build.py 卡片數正確
- 條目無 REPLACE、無空欄位
- 回報使用者:條目 id、上線網址 lab.launchdock.app、封面處理方式
