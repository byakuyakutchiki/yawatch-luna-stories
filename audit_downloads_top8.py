"""Génère une planche des 8 images les plus récentes en plus grand."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

DOWNLOADS_DIR = Path("/media/windows/Users/saint/Downloads")
OUTPUT_DIR = Path("/home/ludo/PROJETS/YAWATCH_LUNA_STORIES/audit_downloads")

images = []
for f in DOWNLOADS_DIR.iterdir():
    if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        if "ChatGPT Image" in f.name:
            mtime = f.stat().st_mtime
            images.append((f, mtime))

images.sort(key=lambda x: x[1], reverse=True)
top8 = images[:8]

cols = 2
rows = 4
thumb_w = 500
thumb_h = 890
margin = 15

sheet_w = cols * thumb_w + (cols + 1) * margin
sheet_h = rows * (thumb_h + 90) + (rows + 1) * margin + 60

sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 30, 30))
draw = ImageDraw.Draw(sheet)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except Exception:
    font = ImageFont.load_default()
    title_font = font

draw.text((margin, margin), "TOP 8 — Dernières images ChatGPT", fill=(255, 255, 255), font=title_font)

for i, (img_path, mtime) in enumerate(top8):
    col = i % cols
    row = i // cols
    x = margin + col * (thumb_w + margin)
    y = margin + 60 + row * (thumb_h + 90 + margin)

    img = Image.open(img_path)
    img = img.convert("RGB")
    img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    paste_x = x + (thumb_w - img.width) // 2
    paste_y = y + (thumb_h - img.height) // 2
    sheet.paste(img, (paste_x, paste_y))

    dt = datetime.fromtimestamp(mtime)
    label = f"{dt.strftime('%H:%M:%S')} — {img_path.name[:45]}"
    draw.text((x, y + thumb_h + 10), label, fill=(220, 220, 220), font=font)

    w, h = img.size
    ratio = w / h
    draw.text((x, y + thumb_h + 38), f"{w}x{h} ratio={ratio:.3f}", fill=(180, 180, 180), font=font)

output_path = OUTPUT_DIR / "downloads_top8_detail.jpg"
sheet.save(output_path, quality=95)
print(f"Planche sauvegardée : {output_path}")
