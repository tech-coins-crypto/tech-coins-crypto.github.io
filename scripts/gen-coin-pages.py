#!/usr/bin/env python3
"""產生 33 枚幣的 Hugo content 檔（SEO 靜態預渲染用）。

從 static/data/subjects.csv 讀取，每枚幣產生 content/coins/<basename>.md，
frontmatter 帶 year/state/nickname/img/keywords，給 layouts/coins/single.html 用。
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "static", "data", "subjects.csv")
OUT_DIR = os.path.join(ROOT, "content", "coins")

def state_en(img, year, state_zh):
    mapping = {
        "美國": "United States", "南卡羅萊納": "South Carolina", "俄亥俄": "Ohio",
        "北卡羅萊納": "North Carolina", "佛蒙特": "Vermont", "印地安納": "Indiana",
        "肯塔基": "Kentucky", "羅德島": "Rhode Island", "賓州": "Pennsylvania",
        "密西西比": "Mississippi", "緬因": "Maine", "康乃狄克": "Connecticut",
        "紐約": "New York", "維吉尼亞": "Virginia", "田納西": "Tennessee",
        "路易斯安那": "Louisiana", "紐澤西": "New Jersey", "阿肯色": "Arkansas",
        "密西根": "Michigan", "明尼蘇達": "Minnesota", "德拉瓦": "Delaware",
        "馬里蘭": "Maryland", "阿拉巴馬": "Alabama", "佛羅里達": "Florida",
        "德州": "Texas", "喬治亞": "Georgia", "伊利諾": "Illinois",
        "密蘇里": "Missouri", "愛荷華": "Iowa", "麻薩諸塞": "Massachusetts",
        "新罕布夏": "New Hampshire", "加州": "California", "威斯康辛": "Wisconsin",
    }
    return mapping.get(state_zh, state_zh)

with open(CSV, encoding="utf-8") as f:
    coins = list(csv.DictReader(f))

os.makedirs(OUT_DIR, exist_ok=True)
for c in coins:
    img = c["img"].strip()
    year = c["year"].strip()
    base = img.rsplit(".", 1)[0]
    nickname = c["nickname"].strip()
    state = c["state"].strip()
    se = state_en(img, year, state)
    keywords = c["keywords"].strip()
    title = f"{year} {state} {nickname}"

    # YAML 跳脫
    def q(s):
        return '"' + s.replace('"', '\\"') + '"'
    fm = (
        "---\n"
        f"title: {q(title)}\n"
        f"year: {q(year)}\n"
        f"state: {q(state)}\n"
        f"state_en: {q(se)}\n"
        f"nickname: {q(nickname)}\n"
        f"img: {q(img)}\n"
        f"basename: {q(base)}\n"
        f"keywords: {q(keywords)}\n"
        "---\n"
    )
    path = os.path.join(OUT_DIR, base + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(fm)
    print(f"wrote {base}.md")

print(f"\n共 {len(coins)} 個檔案")
