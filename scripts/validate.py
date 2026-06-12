#!/usr/bin/env python3
"""validate.py — 驗證 data/projects.yaml。任何修改後必跑,exit 0 才能 commit。"""
import json, sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.yaml"
SCHEMA = ROOT / "data" / "schema.json"
COVERS = ROOT / "assets" / "covers"

def main() -> int:
    errors: list[str] = []

    try:
        projects = yaml.safe_load(DATA.read_text(encoding="utf-8")) or []
    except yaml.YAMLError as e:
        print(f"❌ YAML 解析失敗:\n{e}")
        return 1

    # YAML 會把未加引號的 2026-06-12 解析成 date 物件,先正規化為字串
    import datetime
    for p in projects:
        if isinstance(p, dict) and isinstance(p.get("added"), datetime.date):
            p["added"] = p["added"].isoformat()

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(projects), key=lambda e: e.json_path):
        errors.append(f"[schema] {err.json_path}: {err.message}")

    # id 唯一性
    ids = [p.get("id") for p in projects if isinstance(p, dict)]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errors.append(f"[dup] id 重複: {dup}")

    # 封面檔案存在性
    for p in projects:
        if isinstance(p, dict) and p.get("cover"):
            if not (COVERS / p["cover"]).is_file():
                errors.append(f"[cover] {p.get('id')}: assets/covers/{p['cover']} 不存在")

    # 類型與連結的搭配建議(警告不擋)
    warn = []
    for p in projects:
        if not isinstance(p, dict):
            continue
        kinds = {l["kind"] for l in p.get("links", []) if isinstance(l, dict)}
        t = p.get("type")
        if t == "notion-template" and "duplicate" not in kinds:
            warn.append(f"[warn] {p.get('id')}: notion-template 建議提供 duplicate 連結")
        if t == "gas-line" and not kinds & {"line-add", "video"}:
            warn.append(f"[warn] {p.get('id')}: gas-line 建議提供 line-add 或 video 連結")
        if t == "gas-line" and p.get("check") == "head":
            warn.append(f"[warn] {p.get('id')}: gas-line 通常無法 HTTP 檢查,建議 check: none")

    for w in warn:
        print(w)
    if errors:
        print("\n".join(errors))
        print(f"\n❌ 驗證失敗,共 {len(errors)} 個錯誤。請修正後重跑。")
        return 1

    print(f"✅ 驗證通過:{len(projects)} 筆條目"
          f"(active {sum(1 for p in projects if p.get('status') == 'active')} / "
          f"archived {sum(1 for p in projects if p.get('status') == 'archived')} / "
          f"broken {sum(1 for p in projects if p.get('status') == 'broken')})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
