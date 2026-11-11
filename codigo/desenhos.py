"""Biblioteca de desenhos reutilizáveis (estilo cartoon, contorno escuro)."""
import math
import numpy as np
from motor import fnt, pop, ease, AMARELO, CIANO

O = (20, 15, 40)  # contorno padrão


def rotulo(d, x, y, txt, tam=44, cor=(255, 255, 255)):
    d.text((x, y), txt, font=fnt(tam), fill=cor, anchor="mm", stroke_width=max(4, tam // 8), stroke_fill=O)


def contador(d, x, y, alvo, t, dur=2.0, tam=96, sufixo="", cor=AMARELO):
    n = alvo * ease(t / dur)
    s = f"{n:,.0f}".replace(",", ".") if (alvo >= 100 or isinstance(alvo, int)) else f"{n:.1f}".replace(".", ",")
    rotulo(d, x, y, s + sufixo, tam, cor)


def olhos(d, cx, cy, T, esp=60, r=26, piscada=3.1):
    for sx in (-1, 1):
        ex = cx + sx * esp / 2
        if (T % piscada) < 0.12:
            d.line([ex - r, cy, ex + r, cy], fill=O, width=8)
        else:
            d.ellipse([ex - r, cy - r * 1.2, ex + r, cy + r * 1.2], fill="white", outline=O, width=5)
            d.ellipse([ex - r * 0.45, cy - r * 0.2, ex + r * 0.45, cy + r * 0.7], fill=O)


def sorriso(d, cx, cy, w=40):
    d.arc([cx - w, cy - w * 0.6, cx + w, cy + w * 0.8], 20, 160, fill=O, width=7)


def sol(d, cx, cy, r, T, cor=(255, 205, 40), rosto=True):
    for i in range(12):
        a = i * math.pi / 6 + T * 0.6
        d.line([(cx + math.cos(a) * r * 1.15, cy + math.sin(a) * r * 1.15),
                (cx + math.cos(a) * r * 1.55, cy + math.sin(a) * r * 1.55)], fill=cor, width=int(r * 0.14))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor, outline=O, width=7)
    if rosto:
        olhos(d, cx, cy - r * 0.1, T, esp=r * 0.7, r=r * 0.14)
        sorriso(d, cx, cy + r * 0.3, r * 0.3)


def planeta(d, cx, cy, r, cor, cor2=None, T=0, aneis=False, rosto=True, faixas=3):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor, outline=O, width=7)
    if cor2:
        for k in range(faixas):
            yy = cy - r * 0.5 + k * r * 0.45
            w = math.sqrt(max(0, r ** 2 - (yy - cy) ** 2))
            d.line([(cx - w * 0.9, yy), (cx + w * 0.9, yy)], fill=cor2, width=int(r * 0.12))
    if aneis:
        d.arc([cx - r * 1.7, cy - r * 0.4, cx + r * 1.7, cy + r * 0.4], 0, 180, fill=(230, 200, 140), width=12)
    if rosto:
        olhos(d, cx, cy - r * 0.1, T, esp=r * 0.7, r=r * 0.13)
        sorriso(d, cx, cy + r * 0.3, r * 0.25)


def termometro(d, x, y, nivel, cor=(235, 50, 50), h=420):
    d.rounded_rectangle([x - 34, y - h, x + 34, y], 34, fill="white", outline=O, width=7)
    d.ellipse([x - 62, y - 40, x + 62, y + 84], fill=cor, outline=O, width=7)
    hh = (h - 60) * max(0, min(1, nivel))
    d.rounded_rectangle([x - 18, y - 20 - hh, x + 18, y + 10], 18, fill=cor)


def seta(d, x0, y0, x1, y1, cor=AMARELO, w=14):
    d.line([(x0, y0), (x1, y1)], fill=cor, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    p = [(x1, y1), (x1 - math.cos(a - 0.5) * w * 3, y1 - math.sin(a - 0.5) * w * 3),
         (x1 - math.cos(a + 0.5) * w * 3, y1 - math.sin(a + 0.5) * w * 3)]
    d.polygon(p, fill=cor)


def terra(d, cx, cy, r, T, rosto=True):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 120, 220), outline=O, width=7)
    rng = np.random.default_rng(11)
    for i in range(6):
        a = rng.uniform(0, 6.28) + T * 0.2
        x = cx + math.cos(a) * r * rng.uniform(0.2, 0.6); y = cy + math.sin(a) * r * rng.uniform(0.2, 0.6)
        rr = r * rng.uniform(0.15, 0.3)
        d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=(70, 180, 90))
    if rosto:
        olhos(d, cx, cy - r * 0.1, T, esp=r * 0.7, r=r * 0.13)
        sorriso(d, cx, cy + r * 0.3, r * 0.25)


def brilhos(d, cx, cy, raio, T, n=8, cor=AMARELO):
    for i in range(n):
        a = i * 2 * math.pi / n + T
        x, y = cx + math.cos(a) * raio, cy + math.sin(a) * raio
        s = 10 + 6 * math.sin(T * 5 + i)
        d.polygon([(x, y - s * 2), (x + s * 0.5, y - s * 0.5), (x + s * 2, y), (x + s * 0.5, y + s * 0.5),
                   (x, y + s * 2), (x - s * 0.5, y + s * 0.5), (x - s * 2, y), (x - s * 0.5, y - s * 0.5)], fill=cor)


def atomo(d, cx, cy, r, T, cor=(120, 255, 120)):
    for k in range(3):
        ang = k * math.pi / 3
        pts = []
        for i in range(41):
            a = i / 40 * 2 * math.pi
            x, y = math.cos(a) * r, math.sin(a) * r * 0.35
            pts.append((cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)))
        d.line(pts, fill=cor, width=6)
        a = T * 3 + k * 2
        x, y = math.cos(a) * r, math.sin(a) * r * 0.35
        ex, ey = cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)
        d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=cor, outline=O, width=3)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(255, 120, 60), outline=O, width=5)
