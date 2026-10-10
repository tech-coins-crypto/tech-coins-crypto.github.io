#!/usr/bin/env python3
"""上架前檢查：比對 subjects.csv ↔ webp 圖檔 ↔ txt 介紹文三邊是否齊全。

用法：python3 scripts/check-content.py
退出碼 0 = 全部齊全；1 = 有缺漏。
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "static", "data", "subjects.csv")
IMG_DIR = os.path.join(ROOT, "static", "coins")
TXT_DIR = os.path.join(ROOT, "static", "txts")

errors = []

with open(CSV, encoding="utf-8") as f:
    coins = list(csv.DictReader(f))

print(f"CSV 共 {len(coins)} 枚幣")
print("=" * 50)

csv_bases = set()
for c in coins:
    img = c["img"].strip()
    base = img.rsplit(".", 1)[0]
    csv_bases.add(base)
    nickname = c["nickname"].strip()

    webp_path = os.path.join(IMG_DIR, img)
    if not os.path.exists(webp_path):
        errors.append(f"缺圖檔：{nickname} ({img})")
        print(f"  ✗ {nickname}: 缺 webp")
    else:
        print(f"  ✓ {nickname}: 圖檔 ok", end="")

    txt_path = os.path.join(TXT_DIR, f"txt-{base}.txt")
    if not os.path.exists(txt_path):
        # 2018 有大小寫兩種檔名，特別處理
        alt = os.path.join(TXT_DIR, "txt-coin-2018-Introductory.txt")
        if not (base == "coin-2018-introductory" and os.path.exists(alt)):
            errors.append(f"缺介紹文：{nickname} (txt-{base}.txt)")
            print("，缺介紹文")
        else:
            print("，介紹文 ok")
    else:
        print("，介紹文 ok")

print("=" * 50)

# 反向檢查：孤兒檔案
for fn in sorted(os.listdir(TXT_DIR)):
    if fn.startswith("txt-coin-") and fn.endswith(".txt"):
        base = fn[4:-4]
        if base not in csv_bases and base != "coin-2018-Introductory":
            errors.append(f"孤兒介紹文：{fn}（CSV 沒有對應幣）")

for fn in sorted(os.listdir(IMG_DIR)):
    if fn.startswith("coin-") and fn.endswith(".webp"):
        base = fn[:-5]
        # coin-2018-l / coin-250y 是特殊用途圖，不算孤兒
        if base not in csv_bases and base not in ("coin-2018-l", "coin-250y"):
            errors.append(f"孤兒圖檔：{fn}（CSV 沒有對應幣）")

if errors:
    print(f"\n發現 {len(errors)} 個問題：")
    for e in errors:
        print(f"  ! {e}")
    sys.exit(1)

print("\n全部齊全，可以上架。")
sys.exit(0)
