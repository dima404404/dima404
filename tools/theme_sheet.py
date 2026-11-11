# Превью всех тем: 6 скриншотов + контактный лист
import subprocess, os, io
from PIL import Image, ImageDraw, ImageFont

EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = r"F:\Dima\Documents\Ai\dima404-site\out"
THEMES = ["oneui", "cyber", "glass", "material", "brutal", "retro"]
W, H = 760, 620

paths = []
for t in THEMES:
    p = os.path.join(OUT, f"theme_{t}.png")
    subprocess.run([EXE, "--headless=new", "--disable-gpu", "--no-first-run",
                    rf"--user-data-dir={os.environ['TEMP']}\cr-{t}", "--hide-scrollbars",
                    "--virtual-time-budget=5000", f"--window-size={W},{H}",
                    f"--screenshot={p}", f"http://127.0.0.1:8099/?theme={t}&v=3"],
                   capture_output=True, timeout=90)
    paths.append(p)

imgs = [Image.open(p) for p in paths]
cols, rows = 3, 2
pad = 12
label_h = 30
sheet = Image.new("RGB", (cols * W + (cols + 1) * pad, rows * (H + label_h) + (rows + 1) * pad), "#141420")
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
except Exception:
    font = ImageFont.load_default()

for i, (t, im) in enumerate(zip(THEMES, imgs)):
    c, r = i % cols, i // cols
    x = pad + c * (W + pad)
    y = pad + r * (H + label_h + pad)
    draw.text((x + 4, y + 4), t, fill="#ffffff", font=font)
    sheet.paste(im, (x, y + label_h))

out = os.path.join(OUT, "themes_sheet.png")
sheet.save(out)
print(out, sheet.size)
