"""MAIA – apresentadora do canal Me ContAI, desenhada em código (PIL).
draw_maia(t, boca, olhar=0) -> imagem RGBA 800x1000 (busto).
boca: 0..1 (abertura da boca, vinda do volume da voz)
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 800, 1000
CONTORNO = (45, 25, 30)
PELE = (252, 214, 188)
PELE_SOMBRA = (236, 184, 156)
CABELO = (150, 78, 40)
CABELO_CLARO = (205, 128, 64)
CABELO_ESCURO = (105, 50, 28)
IRIS = (120, 66, 28)
MOLETOM = (24, 30, 64)
CIANO = (35, 210, 225)
CAMISETA = (236, 236, 242)


def _onda(cx, cy, rx, ry, n, amp, fase, a0=0, a1=2 * math.pi, freq=7):
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        r = 1 + amp * math.sin(a * freq + fase)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return pts


def draw_maia(t, boca=0.0, olhar=0.0):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 400, 360  # centro do rosto
    sway = math.sin(t * 1.7) * 6

    # ---------- cabelo de trás (ondulado, longo) ----------
    pts = []
    for i in range(61):
        a = math.pi * 1.0 + math.pi * 2 * i / 60
        rx, ry = 285, 330
        r = 1 + 0.05 * math.sin(a * 9 + t * 2)
        x = cx + math.cos(a) * rx * r
        y = cy + 40 + math.sin(a) * ry * r
        if y > cy + 60:  # alonga para baixo, cachos nos ombros
            y += (y - cy - 60) * 0.55
            x += math.sin(y / 40 + t * 2) * 14 + (sway if x < cx else -sway) * 0.3
        pts.append((x, y))
    d.polygon(pts, fill=CABELO, outline=CONTORNO)
    d.line(pts + [pts[0]], fill=CONTORNO, width=8)
    for k in range(5):  # mechas claras
        x0 = cx - 230 + k * 115
        d.arc([x0 - 40, cy + 120, x0 + 60, cy + 520], 200, 330, fill=CABELO_CLARO, width=12)

    # ---------- corpo: moletom, camiseta, fones ----------
    d.rounded_rectangle([110, 700, 690, 1150], 140, fill=MOLETOM, outline=CONTORNO, width=8)
    d.polygon([(330, 700), (470, 700), (440, 1000), (360, 1000)], fill=CAMISETA)
    d.polygon([(300, 700), (360, 700), (400, 1000), (340, 1000)], fill=MOLETOM)
    d.polygon([(500, 700), (440, 700), (400, 1000), (460, 1000)], fill=MOLETOM)
    d.line([(370, 760), (370, 1000)], fill=(150, 150, 170), width=5)  # ziper
    d.line([(430, 760), (430, 1000)], fill=(150, 150, 170), width=5)
    d.polygon([(375, 850), (375, 900), (420, 875)], fill=None, outline=(60, 70, 120), width=6)  # icone play
    for xx in (150, 650):  # listras ciano
        d.rounded_rectangle([xx - 22, 820, xx + 22, 1000], 10, fill=CIANO)
    # pescoco
    d.rounded_rectangle([355, 560, 445, 720], 30, fill=PELE_SOMBRA)
    # gola ciano
    d.arc([270, 640, 530, 790], 190, 350, fill=CIANO, width=16)
    # fones no pescoco
    d.arc([255, 600, 545, 800], 160, 380, fill=(25, 25, 30), width=22)
    for sx in (-1, 1):
        ex = 400 + sx * 150
        d.ellipse([ex - 62, 640, ex + 62, 770], fill=(25, 25, 30), outline=CONTORNO, width=6)
        d.ellipse([ex - 40, 663, ex + 40, 747], outline=CIANO, width=9)

    # ---------- rosto ----------
    face = []
    for i in range(41):
        a = math.pi * 2 * i / 40
        rx, ry = 190, 215
        x = cx + math.cos(a) * rx
        y = cy + math.sin(a) * ry
        if math.sin(a) > 0:  # queixo mais fino
            x = cx + math.cos(a) * rx * (1 - 0.28 * math.sin(a) ** 2)
        face.append((x, y))
    d.polygon(face, fill=PELE)
    d.line(face + [face[0]], fill=CONTORNO, width=7)
    # orelhas + argolas
    for sx in (-1, 1):
        ox = cx + sx * 190
        d.ellipse([ox - 26, cy - 20, ox + 26, cy + 50], fill=PELE, outline=CONTORNO, width=6)
        d.ellipse([ox - 22, cy + 45, ox + 22, cy + 95], outline=(225, 200, 120), width=7)

    # bochechas e sardas
    for sx in (-1, 1):
        bx = cx + sx * 105
        d.ellipse([bx - 45, cy + 55, bx + 45, cy + 95], fill=(250, 170, 160))
        for k in range(5):
            fx = bx + (k - 2) * 16 + (k % 2) * 4
            fy = cy + 50 + (k % 3) * 10
            d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(200, 130, 100))

    # olhos
    piscar = (t % 3.4) < 0.13
    for sx in (-1, 1):
        ex, ey = cx + sx * 78, cy - 5
        if piscar:
            d.arc([ex - 48, ey - 20, ex + 48, ey + 25], 15, 165, fill=CONTORNO, width=9)
        else:
            d.ellipse([ex - 48, ey - 52, ex + 48, ey + 48], fill="white", outline=CONTORNO, width=6)
            ix = ex + olhar * 10
            d.ellipse([ix - 33, ey - 36, ix + 33, ey + 40], fill=IRIS)
            d.ellipse([ix - 18, ey - 18, ix + 18, ey + 22], fill=(40, 20, 12))
            d.ellipse([ix - 22, ey - 30, ix - 6, ey - 14], fill="white")
            d.ellipse([ix + 8, ey + 12, ix + 16, ey + 20], fill="white")
            # cilios
            d.arc([ex - 52, ey - 58, ex + 52, ey + 46], 195, 345, fill=CONTORNO, width=11)
            d.line([(ex + sx * 44, ey - 34), (ex + sx * 64, ey - 50)], fill=CONTORNO, width=8)
        # sobrancelhas
        sb = -2 + math.sin(t * 2.3) * 3
        d.arc([ex - 55, ey - 105 + sb, ex + 55, ey - 45 + sb], 200 if sx < 0 else 210, 330 if sx < 0 else 340,
              fill=CABELO_ESCURO, width=13)

    # nariz
    d.arc([cx - 18, cy + 40, cx + 18, cy + 72], 20, 160, fill=(200, 140, 115), width=6)

    # boca: sorriso + abertura pela fala
    my = cy + 112
    ab = max(0.0, min(1.0, boca))
    if ab < 0.08:
        d.chord([cx - 62, my - 40, cx + 62, my + 30], 15, 165, fill=(170, 50, 60), outline=CONTORNO, width=6)
        d.chord([cx - 50, my - 28, cx + 50, my - 2], 15, 165, fill="white")
    else:
        h = 18 + ab * 52
        d.ellipse([cx - 58, my - 18, cx + 58, my - 18 + h + 18], fill=(150, 35, 50), outline=CONTORNO, width=6)
        d.chord([cx - 50, my - 16, cx + 50, my + 8], 180, 360, fill="white")
        d.ellipse([cx - 28, my - 18 + h * 0.6, cx + 28, my - 18 + h + 10], fill=(235, 110, 120))

    # ---------- franja / cabelo da frente ----------
    franja = [(cx - 200, cy - 20), (cx - 205, cy - 150), (cx - 120, cy - 235), (cx + 20, cy - 250),
              (cx + 150, cy - 215), (cx + 210, cy - 120), (cx + 205, cy + 10),
              (cx + 175, cy - 90), (cx + 110, cy - 160), (cx - 10, cy - 165),
              (cx - 95, cy - 120), (cx - 150, cy - 60), (cx - 175, cy + 30)]
    d.polygon(franja, fill=CABELO)
    d.line(franja[:7], fill=CONTORNO, width=7, joint="curve")
    d.line(franja[6:], fill=CABELO_ESCURO, width=5, joint="curve")
    d.arc([cx - 150, cy - 230, cx + 60, cy - 60], 200, 300, fill=CABELO_CLARO, width=12)
    d.arc([cx - 20, cy - 240, cx + 200, cy - 40], 230, 330, fill=CABELO_CLARO, width=10)
    # mechas laterais na frente dos ombros
    for sx in (-1, 1):
        pts = []
        for k in range(12):
            y = cy + 20 + k * 38
            x = cx + sx * (205 + math.sin(k * 0.9 + t * 2.2) * 22 + k * 4)
            pts.append((x, y))
        for k in range(len(pts) - 1):
            w = 92 - k * 5
            d.line([pts[k], pts[k + 1]], fill=CONTORNO, width=w + 12)
        for k in range(len(pts) - 1):
            w = 92 - k * 5
            d.line([pts[k], pts[k + 1]], fill=CABELO, width=w)
            d.ellipse([pts[k][0] - w / 2, pts[k][1] - w / 2, pts[k][0] + w / 2, pts[k][1] + w / 2], fill=CABELO)
        for k in range(len(pts) - 1):
            d.line([(pts[k][0] - sx * 12, pts[k][1]), (pts[k + 1][0] - sx * 12, pts[k + 1][1])], fill=CABELO_CLARO, width=8)

    return img


def maia_pose(t, boca, escala=1.0):
    """Aplica balanço/inclinação suave e escala."""
    im = draw_maia(t, boca, olhar=math.sin(t * 0.7) * 0.6)
    ang = math.sin(t * 1.3) * 2.5
    im = im.rotate(ang, resample=Image.BICUBIC, center=(400, 600))
    if escala != 1.0:
        im = im.resize((int(W * escala), int(H * escala)), Image.LANCZOS)
    return im


if __name__ == "__main__":
    for i, (t, b) in enumerate([(0.5, 0.0), (1.0, 0.7), (3.38, 0.3)]):
        bg = Image.new("RGBA", (W, H), (14, 26, 64, 255))
        bg.alpha_composite(maia_pose(t, b))
        bg.convert("RGB").save(f"/home/claude/curiosidades/_maia{i}.jpg", quality=88)
