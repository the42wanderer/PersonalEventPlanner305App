"""Cut the six box faces out of a flat dieline render, for the 3D comparison mock-ups.

Usage: python3 tools/crop_faces.py IMAGE PX_PER_PT X_OFFSET_PT OUT_DIR
Panel rectangles are the fold-to-fold faces of the supplied dieline (2.pdf positions, points).
1.pdf-based files sit 19.98 pt further left, so pass -19.98 for those.
"""
import os
import sys
from PIL import Image

PANELS = {
    'front': (145.46, 390.86, 393.94, 631.07), 'sideA': (393.94, 390.86, 633.68, 631.07),
    'back': (633.68, 390.86, 881.95, 631.07), 'sideB': (881.95, 390.86, 1122.45, 631.07),
    'top': (145.50, 149.85, 393.53, 390.72), 'bottom': (633.68, 631.07, 881.70, 870.00),
}
src, scale, dx, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
Image.MAX_IMAGE_PIXELS = None
im = Image.open(src).convert('RGB')
os.makedirs(out, exist_ok=True)
for name, (x0, y0, x1, y1) in PANELS.items():
    box = tuple(round(v * scale) for v in (x0 + dx, y0, x1 + dx, y1))
    face = im.crop(box)
    if face.width > 1600:
        face = face.resize((1600, round(face.height * 1600 / face.width)), Image.LANCZOS)
    face.save(os.path.join(out, f'face-{name}.jpg'), quality=90)
print(out, 'done')
