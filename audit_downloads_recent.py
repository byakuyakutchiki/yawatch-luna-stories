"""Génère une planche de contact des images récentes dans Downloads Windows."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

DOWNLOADS_DIR = Path("/media/windows/Users/saint/Downloads")
OUTPUT_DIR = Path("/home/ludo/PROJETS/YAWATCH_LUNA_STORIES/audit_downloads")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Récupérer les images ChatGPT les plus récentes
images = []
for f in DOWNLOADS_DIR.iterdir():
    if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        if "ChatGPT Image" in f.name:
            mtime = f.stat().st_mtime
            images.append((f, mtime))

# Trier par date de modification décroissante
images.sort(key=lambda x: x[1], reverse=True)

# Prendre les 15 plus récentes
recent = images[:15]

print(f"{len(recent)} images récentes trouvées")
for f, mtime in recent:
    dt = datetime.fromtimestamp(mtime)
    print(f"  {dt.strftime('%Y-%m-%d %H:%M:%S')}  {f.name}")

# Créer la planche
cols = 3
rows = (len(recent) + cols - 1) // cols
thumb_w = 360
thumb_h = 640
margin = 10

sheet_w = cols * thumb_w + (cols + 1) * margin
sheet_h = rows * (thumb_h + 80) + (rows + 1) * margin + 60

sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 30, 30))
draw = ImageDraw.Draw(sheet)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
except Exception:
    font = ImageFont.load_default()
    title_font = font

draw.text((margin, margin), "DOWNLOADS RECENTS — ChatGPT Images", fill=(255, 255, 255), font=title_font)

for i, (img_path, mtime) in enumerate(recent):
    col = i % cols
    row = i // cols
    x = margin + col * (thumb_w + margin)
    y = margin + 50 + row * (thumb_h + 80 + margin)

    try:
        img = Image.open(img_path)
        img = img.convert("RGB")
        img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        paste_x = x + (thumb_w - img.width) // 2
        paste_y = y + (thumb_h - img.height) // 2
        sheet.paste(img, (paste_x, paste_y))

        dt = datetime.fromtimestamp(mtime)
        label = f"{dt.strftime('%H:%M')} — {img_path.name[:40]}"
        draw.text((x, y + thumb_h + 8), label, fill=(220, 220, 220), font=font)

        w, h = img.size
        ratio = w / h
        draw.text((x, y + thumb_h + 28), f"{w}x{h} ratio={ratio:.3f}", fill=(180, 180, 180), font=font)
    except Exception as e:
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(255, 0, 0), width=2)
        draw.text((x + 10, y + 10), f"ERREUR\n{img_path.name}", fill=(255, 0, 0), font=font)
        print(f"[ERROR] {img_path}: {e}")

output_path = OUTPUT_DIR / "downloads_recents_contact_sheet.jpg"
sheet.save(output_path, quality=90)
print(f"\nPlanche sauvegardée : {output_path}")
