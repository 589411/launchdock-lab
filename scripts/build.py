#!/usr/bin/env python3
"""build.py — 讀取 data/projects.yaml,輸出 dist/index.html(中文)、dist/en/index.html(英文)與封面圖。"""
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

# 英文版標籤;條目文字來自各條目的 en 區塊,缺了就退回中文
TYPE_LABEL_EN = {
    "website": "Website", "gas-webapp": "GAS app", "gas-line": "LINE automation",
    "notion-template": "Notion template", "llm-tool": "AI tool",
    "n8n-workflow": "n8n workflow", "repo": "Open source", "other": "Other",
}
KIND_LABEL_EN = {
    "open": "Open demo", "admin": "Admin", "duplicate": "Duplicate",
    "line-add": "Try on LINE", "repo": "Source", "video": "Watch video", "doc": "Docs",
}
LEVEL_LABEL_EN = {1: "Prompt", 2: "Template", 3: "Automation"}
CATEGORY_EN = {"自動化": "Automation", "圖片": "Images", "寫作": "Writing", "教學": "Teaching",
               "遊戲": "Games", "資料": "Data", "生活": "Life"}

# 模板 {{...}} 文字;路徑相對於各自輸出的 index.html
PAGE_TEXT = {
    "zh": {
        "HTML_LANG": "zh-Hant", "PAGE_TITLE": "Launchdock Lab｜藍鴨 AI 實例庫",
        "META_DESC": "藍鴨 Launchdock 課堂實際案例庫:從提示詞到自動化工作流的可動手 demo。",
        "BACKHOME": "← 回藍鴨 Launchdock 主站", "HOME_URL": "https://launchdock.app",
        "LANG_SWITCH": '<a href="en/" class="langswitch" hreflang="en" lang="en">English</a>',
        "H1": "藍鴨 <em>AI 實例庫</em>",
        "SUB": "課堂上看到的每個 demo 都在這裡:從一句提示詞,到可複製的範本,到全自動工作流。每張卡片最後都有「明天就能做的一件事」。",
        "ALL": "全部", "LV_ALL": "所有 Level", "LV1": "L1 提示詞", "LV2": "L2 範本", "LV3": "L3 自動化",
        "CLOSE": "關閉", "FOOTER": "藍鴨 Launchdock · <a href=\"https://launchdock.app\">launchdock.app</a> · 本頁由 projects.yaml 自動建置",
    },
    "en": {
        "HTML_LANG": "en", "PAGE_TITLE": "Launchdock Lab | Hands-on AI demos",
        "META_DESC": "Real classroom demos from LaunchDock, an AI education studio in Taiwan: from a single prompt to fully automated workflows.",
        "BACKHOME": "← Back to LaunchDock", "HOME_URL": "https://launchdock.app/en/",
        "LANG_SWITCH": '<a href="../" class="langswitch" hreflang="zh-Hant" lang="zh-Hant">中文</a>',
        "H1": "LaunchDock <em>AI demo library</em>",
        "SUB": "Every demo from our classes lives here: from a single prompt, to a template you can copy, to a fully automated workflow. Each card ends with one thing you can do tomorrow.",
        "ALL": "All", "LV_ALL": "All levels", "LV1": "L1 Prompt", "LV2": "L2 Template", "LV3": "L3 Automation",
        "CLOSE": "Close", "FOOTER": "LaunchDock · <a href=\"https://launchdock.app/en/\">launchdock.app</a> · Built automatically from projects.yaml",
    },
}

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

def level_dots(level: int, lang: str = "zh") -> str:
    label = (LEVEL_LABEL_EN if lang == "en" else LEVEL_LABEL)[level]
    dots = "".join(f'<i class="{ "on" if i <= level else "" }"></i>' for i in (1, 2, 3))
    return f'<span class="lv" title="Level {level}: {label}">{dots}<b>L{level} {label}</b></span>'

def resolve_cover(p: dict) -> Optional[str]:
    """封面三層邏輯:明確指定 → 自動偵測 <id>.png/jpg/webp → None(佔位圖)"""
    if p.get("cover"):
        return p["cover"]
    for ext in ("png", "jpg", "jpeg", "webp"):
        if (COVERS_SRC / f"{p['id']}.{ext}").is_file():
            return f"{p['id']}.{ext}"
    return None

def text(p: dict, field: str, lang: str):
    """英文頁優先取 en 區塊,沒寫就退回中文。"""
    if lang == "en":
        return (p.get("en") or {}).get(field) or p.get(field)
    return p.get(field)

def card(p: dict, lang: str = "zh") -> str:
    pid = p["id"]
    en = lang == "en"
    found = resolve_cover(p)
    prefix = "../" if en else ""
    cover = f"{prefix}covers/{found}" if found else f"{prefix}covers/{pid}.svg"
    title = text(p, "title", lang)
    en_labels = (p.get("en") or {}).get("labels") or [] if en else []
    chips = "".join(f'<span class="chip">{esc(c)}</span>' for c in p.get("platforms", []))
    mods = " ".join(p.get("modules", []))
    broken = ' data-broken="1"' if p["status"] == "broken" else ""
    btns = []
    for i, l in enumerate(p["links"]):
        cls = "btn primary" if l["kind"] in ("open", "duplicate", "line-add") else "btn"
        if en:
            label = en_labels[i] if i < len(en_labels) else KIND_LABEL_EN[l["kind"]]
        else:
            label = l["label"] or KIND_LABEL[l["kind"]]
        btns.append(f'<a class="{cls}" href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(label)}</a>')
    if p.get("qr"):
        first = p["links"][0]["url"]
        btns.append(f'<button class="btn qr" data-url="{esc(first)}" data-title="{esc(title)}">QR</button>')
    tmr = text(p, "tomorrow", lang)
    tomorrow = f'<div class="tomorrow"><b>{"Do it tomorrow" if en else "明天就能做"}</b>{esc(tmr)}</div>' if tmr else ""
    d = text(p, "description", lang)
    desc = f'<p class="desc">{esc(d)}</p>' if d else ""
    type_label = (TYPE_LABEL_EN if en else TYPE_LABEL)[p["type"]]
    cat_label = CATEGORY_EN.get(p["category"], p["category"]) if en else p["category"]
    return f'''<article class="card" data-cat="{esc(p["category"])}" data-level="{p["level"]}" data-type="{esc(p["type"])}"{broken}>
  <div class="cover"><img src="{cover}" alt="{esc(title)}" loading="lazy">
    <span class="badge">{type_label}</span>
    {f'<span class="badge warn">{"Link issue" if en else "連結異常"}</span>' if p["status"] == "broken" else ""}
  </div>
  <div class="body">
    <div class="meta"><span class="cat">{"📌 " if p.get("pinned") else ""}{esc(cat_label)}</span>{level_dots(p["level"], lang)}</div>
    <h3>{esc(title)}</h3>
    <p class="summary">{esc(text(p, "summary", lang))}</p>
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
    tpl = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")
    for lang, out_path in (("zh", DIST / "index.html"), ("en", DIST / "en" / "index.html")):
        t = PAGE_TEXT[lang]
        filters = f'<button class="f on" data-f="*">{t["ALL"]}</button>' + "".join(
            f'<button class="f" data-f="{esc(c)}">{esc(CATEGORY_EN.get(c, c) if lang == "en" else c)}</button>'
            for c in cats)
        out = (tpl.replace("{{CARDS}}", "\n".join(card(p, lang) for p in visible))
                  .replace("{{FILTERS}}", filters)
                  .replace("{{COUNT}}", str(len(visible)))
                  .replace("{{UPDATED}}", date.today().isoformat()))
        for k, v in t.items():
            out = out.replace("{{" + k + "}}", v)
        out_path.parent.mkdir(exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
    missing_en = [p["id"] for p in visible if not p.get("en")]
    print(f"✅ 建置完成:dist/index.html + dist/en/index.html({len(visible)} 張卡片)"
          + (f"\n⚠️  缺英文、英文頁顯示中文:{', '.join(missing_en)}" if missing_en else ""))

if __name__ == "__main__":
    main()
