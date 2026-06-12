#!/usr/bin/env python3
"""screenshot.py — 自動補封面(極簡版)。

規則:
- 只處理 active 且「沒有封面」的條目(沒有 cover 欄位、assets/covers/ 也沒有同名圖)
- 對第一個 kind=open 的連結截圖,存成 assets/covers/<id>.png
- 不修改 projects.yaml(build.py 會自動偵測同名圖檔)
- 用 --force <id> 可強制重截某一筆

需求:pip install playwright && playwright install chromium
"""
import sys
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
COVERS = ROOT / "assets" / "covers"

def has_cover(p: dict) -> bool:
    if p.get("cover"):
        return True
    return any((COVERS / f"{p['id']}.{ext}").is_file() for ext in ("png", "jpg", "jpeg", "webp"))

def main():
    force_id = sys.argv[sys.argv.index("--force") + 1] if "--force" in sys.argv else None
    projects = yaml.safe_load((ROOT / "data" / "projects.yaml").read_text(encoding="utf-8")) or []

    targets = []
    for p in projects:
        if p.get("status") != "active":
            continue
        if force_id and p["id"] != force_id:
            continue
        if not force_id and has_cover(p):
            continue
        url = next((l["url"] for l in p.get("links", []) if l["kind"] == "open"), None)
        if url:
            targets.append((p["id"], url, "PWA" in (p.get("platforms") or [])))

    if not targets:
        print("沒有需要截圖的條目")
        return

    COVERS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for pid, url, mobile in targets:
            # PWA / 行動優先的站用手機視窗,其餘用 16:9 桌面視窗
            vp = {"width": 390, "height": 844} if mobile else {"width": 1280, "height": 720}
            ctx = browser.new_context(viewport=vp, device_scale_factor=2,
                                      is_mobile=mobile, locale="zh-TW")
            page = ctx.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(1500)  # 等字型與動畫
                page.screenshot(path=str(COVERS / f"{pid}.png"))
                print(f"📸 {pid} ← {url}")
            except Exception as e:
                print(f"⚠️ {pid} 截圖失敗:{type(e).__name__}: {e}")
            finally:
                ctx.close()
        browser.close()

if __name__ == "__main__":
    main()
