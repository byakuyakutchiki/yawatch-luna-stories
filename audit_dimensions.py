"""Audit des dimensions et formats des assets images."""

from pathlib import Path
from PIL import Image
import csv

ASSETS_DIR = Path("assets/luna_stories_assets")
OUTPUT_CSV = Path("audit_assets_dimensions.csv")

TARGET_RATIO = 9 / 16  # 0.5625
TOLERANCE = 0.05

results = []

for img_path in sorted(ASSETS_DIR.rglob("*")):
    if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue

    try:
        with Image.open(img_path) as img:
            w, h = img.size
            ratio = w / h
            is_portrait = h > w
            ratio_diff = abs(ratio - TARGET_RATIO)
            ratio_ok = ratio_diff <= TOLERANCE
            area = w * h

            results.append({
                "path": str(img_path),
                "filename": img_path.name,
                "width": w,
                "height": h,
                "ratio": round(ratio, 4),
                "is_portrait": is_portrait,
                "ratio_916_ok": ratio_ok,
                "ratio_diff": round(ratio_diff, 4),
                "megapixels": round(area / 1_000_000, 2),
            })
    except Exception as e:
        results.append({
            "path": str(img_path),
            "filename": img_path.name,
            "width": 0,
            "height": 0,
            "ratio": 0,
            "is_portrait": False,
            "ratio_916_ok": False,
            "ratio_diff": 999,
            "megapixels": 0,
            "error": str(e),
        })

# Trier par ratio_diff décroissant pour voir les problèmes en premier
results.sort(key=lambda x: x.get("ratio_diff", 0), reverse=True)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["path", "filename", "width", "height", "ratio", "is_portrait", "ratio_916_ok", "ratio_diff", "megapixels"])
    writer.writeheader()
    writer.writerows(results)

print(f"Audit terminé : {len(results)} images analysées")
print(f"Fichier CSV : {OUTPUT_CSV}")

# Résumé
not_portrait = [r for r in results if not r["is_portrait"]]
not_916 = [r for r in results if not r["ratio_916_ok"]]
print(f"\nImages non portrait : {len(not_portrait)}")
print(f"Images pas en ratio 9:16 (tolérance 5%) : {len(not_916)}")

print("\n--- Images avec ratio très différent de 9:16 ---")
for r in not_916[:20]:
    print(f"{r['filename']:60s} {r['width']}x{r['height']} ratio={r['ratio']}")
