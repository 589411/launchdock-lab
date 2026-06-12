#!/usr/bin/env python3
"""build.py — 讀取 data/projects.yaml,輸出 dist/index.html 與封面圖。"""
import hashlib, html, shutil
from datetime import date
from pathlib import Path
from typing import Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
COVERS_SRC = ROOT / "assets" / "covers"
COVERS_DST = DIST / "covers"

TYPE_LABEL = {
    "website": "網站", "gas-webapp": "GAS 應用", "gas-line": "LINE 自動化",
    "notion-template": "Notion 模板", "llm-tool": "AI 小工具",
    "n8n-workflow": "n8n 工作流", "repo": "開源專案", "other": "其他",
}
KIND_LABEL = {
    "open": "開啟 Demo", "admin": "管理後台", "duplicate": "複製模板",
    "line-add": "加 LINE 體驗", "repo": "原始碼", "video": "看影片", "doc": "說明文件",
}
LEVEL_LABEL = {1: "提示詞", 2: "範本", 3: "自動化"}

def esc(s): return html.escape(str(s or ""), quote=True)

def placeholder_svg(pid: str, title: str) -> str:
    h = int(hashlib.md5(pid.encode()).hexdigest(), 16)
    hue = h % 360
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="hsl({hue},42%,28%)"/><stop offset="1" stop-color="hsl({(hue+40)%360},48%,16%)"/>
</linearGradient></defs>
<rect width="640" height="360" fill="url(#g)"/>
<circle cx="560" cy="60" r="120" fill="hsla({(hue+180)%360},60%,70%,0.12)"/>
<text x="40" y="200" font-family="'Noto Sans TC',sans-serif" font-size="40" font-weight="900" fill="#fff" opacity="0.92">{esc(title)}</text>
<text x="40" y="320" font-family="monospace" font-size="16" fill="#fff" opacity="0.45">launchdock.lab / {esc(pid)}</text>
</svg>'''

def level_dots(level: int) -> str:
    dots = "".join(f'<i class="{ "on" if i <= level else "" }"></i>' for i in (1, 2, 3))
    return f'<span class="lv" title="Level {level}:{LEVEL_LABEL[level]}">{dots}<b>L{level} {LEVEL_LABEL[level]}</b></span>'

def resolve_cover(p: dict) -> Optional[str]:
    """封面三層邏輯:明確指定 → 自動偵測 <id>.png/jpg/webp → None(佔位圖)"""
    if p.get("cover"):
        return p["cover"]
    for ext in ("png", "jpg", "jpeg", "webp"):
        if (COVERS_SRC / f"{p['id']}.{ext}").is_file():
            return f"{p['id']}.{ext}"
    return None

def card(p: dict) -> str:
    pid = p["id"]
    found = resolve_cover(p)
    cover = f"covers/{found}" if found else f"covers/{pid}.svg"
    chips = "".join(f'<span class="chip">{esc(c)}</span>' for c in p.get("platforms", []))
    mods = " ".join(p.get("modules", []))
    broken = ' data-broken="1"' if p["status"] == "broken" else ""
    btns = []
    for l in p["links"]:
        cls = "btn primary" if l["kind"] in ("open", "duplicate", "line-add") else "btn"
        btns.append(f'<a class="{cls}" href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"] or KIND_LABEL[l["kind"]])}</a>')
    if p.get("qr"):
        first = p["links"][0]["url"]
        btns.append(f'<button class="btn qr" data-url="{esc(first)}" data-title="{esc(p["title"])}">QR</button>')
    tomorrow = f'<div class="tomorrow"><b>明天就能做</b>{esc(p["tomorrow"])}</div>' if p.get("tomorrow") else ""
    desc = f'<p class="desc">{esc(p["description"])}</p>' if p.get("description") else ""
    return f'''<article class="card" data-cat="{esc(p["category"])}" data-level="{p["level"]}" data-type="{esc(p["type"])}"{broken}>
  <div class="cover"><img src="{cover}" alt="{esc(p["title"])}" loading="lazy">
    <span class="badge">{TYPE_LABEL[p["type"]]}</span>
    {f'<span class="badge warn">連結異常</span>' if p["status"] == "broken" else ""}
  </div>
  <div class="body">
    <div class="meta"><span class="cat">{"📌 " if p.get("pinned") else ""}{esc(p["category"])}</span>{level_dots(p["level"])}</div>
    <h3>{esc(p["title"])}</h3>
    <p class="summary">{esc(p["summary"])}</p>
    {desc}
    <div class="chips">{chips}{f'<span class="chip mod">{mods}</span>' if mods else ""}</div>
    <div class="actions">{"".join(btns)}</div>
    {tomorrow}
  </div>
</article>'''

def main():
    projects = yaml.safe_load((ROOT / "data" / "projects.yaml").read_text(encoding="utf-8")) or []
    visible = [p for p in projects if p["status"] != "archived"]
    # 排序:pinned 置頂 → 新到舊
    visible.sort(key=lambda p: str(p["added"]), reverse=True)
    visible.sort(key=lambda p: not p.get("pinned", False))

    DIST.mkdir(exist_ok=True)
    COVERS_DST.mkdir(exist_ok=True)
    for p in visible:
        found = resolve_cover(p)
        if found:
            shutil.copy(COVERS_SRC / found, COVERS_DST / found)
        else:
            (COVERS_DST / f"{p['id']}.svg").write_text(placeholder_svg(p["id"], p["title"]), encoding="utf-8")

    cats = sorted({p["category"] for p in visible})
    filters = '<button class="f on" data-f="*">全部</button>' + "".join(
        f'<button class="f" data-f="{esc(c)}">{esc(c)}</button>' for c in cats)

    tpl = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{CARDS}}", "\n".join(card(p) for p in visible))
              .replace("{{FILTERS}}", filters)
              .replace("{{COUNT}}", str(len(visible)))
              .replace("{{UPDATED}}", date.today().isoformat()))
    (DIST / "index.html").write_text(out, encoding="utf-8")
    print(f"✅ 建置完成:dist/index.html({len(visible)} 張卡片)")

if __name__ == "__main__":
    main()
