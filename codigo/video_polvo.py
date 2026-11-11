"""Vídeo: o polvo tem 3 corações e sangue azul."""
import math, sys
from motor import render, pop

def polvo(d, cx, cy, T, cor=(240, 110, 160)):
    cy += math.sin(T * 3) * 18
    for i in range(8):
        base = cx - 170 + i * 48
        pts = [(base + math.sin(T * 4 + i + k * 0.45) * (6 + k * 3), cy + 120 + k * 22) for k in range(14)]
        for k in range(len(pts) - 1):
            w = int(30 - k * 1.8)
            d.line([pts[k], pts[k + 1]], fill=cor, width=max(6, w))
            d.ellipse([pts[k][0] - w / 2, pts[k][1] - w / 2, pts[k][0] + w / 2, pts[k][1] + w / 2], fill=cor)
    d.ellipse([cx - 200, cy - 230, cx + 200, cy + 170], fill=cor, outline=(90, 30, 70), width=10)
    for sx in (-1, 1):
        ex, ey = cx + sx * 75, cy + 10
        if (T % 2.7) < 0.12:
            d.line([ex - 30, ey, ex + 30, ey], fill=(40, 20, 50), width=10)
        else:
            d.ellipse([ex - 36, ey - 42, ex + 36, ey + 42], fill="white", outline=(90, 30, 70), width=6)
            d.ellipse([ex - 16, ey - 6, ex + 16, ey + 26], fill=(40, 20, 50))
    d.arc([cx - 45, cy + 40, cx + 45, cy + 110], 10, 170, fill=(90, 30, 70), width=9)

def coracao(d, cx, cy, r, cor=(235, 40, 70)):
    o = (60, 10, 30)
    d.ellipse([cx - r, cy - r * 0.9, cx, cy + r * 0.1], fill=cor, outline=o, width=5)
    d.ellipse([cx, cy - r * 0.9, cx + r, cy + r * 0.1], fill=cor, outline=o, width=5)
    d.polygon([(cx - r * 0.97, cy - r * 0.25), (cx + r * 0.97, cy - r * 0.25), (cx, cy + r)], fill=cor)
    d.line([(cx - r * 0.97, cy - r * 0.2), (cx, cy + r), (cx + r * 0.97, cy - r * 0.2)], fill=o, width=5)

def cena_coracoes(d, img, t, T):
    polvo(d, 540, 700, T)
    for i, x in enumerate((300, 540, 780)):
        ti = 1.2 + i * 0.6
        if t > ti:
            r = 70 * pop((t - ti) / 0.4) * (1 + 0.08 * math.sin(T * 9 + i))
            coracao(d, x, 1130, r)

def cena_sangue(d, img, t, T):
    polvo(d, 540, 700, T, cor=(110, 150, 255))
    for i in range(6):
        ti = 0.8 + i * 0.25
        if t > ti:
            gx, gy = 200 + i * 136, 1130 + math.sin(T * 4 + i) * 20
            r = 38 * pop((t - ti) / 0.4)
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(40, 120, 255), outline=(10, 30, 90), width=5)
            d.polygon([(gx - r * 0.7, gy - r * 0.7), (gx + r * 0.7, gy - r * 0.7), (gx, gy - r * 2)], fill=(40, 120, 255))

CENAS = [
    dict(tipo="gancho", titulo="VOCÊ SABIA?", fala="Você sabia? Esse bicho parece de outro planeta!"),
    dict(tipo="fato", titulo="O POLVO TEM 3 CORAÇÕES", desenho=cena_coracoes,
         fundo=((40, 140, 220), (15, 50, 130)),
         fala="O polvo tem três corações: dois bombeiam sangue para as brânquias, e um para o resto do corpo."),
    dict(tipo="fato", titulo="E O SANGUE DELE É AZUL!", desenho=cena_sangue,
         fundo=((25, 45, 115), (8, 16, 55)),
         fala="E tem mais: o sangue dele é azul! Isso por causa da hemocianina, uma proteína rica em cobre."),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Curiosidade nova todo dia",
         fala="Eu sou a Maia! Segue o Me Conta Aí pra mais curiosidades!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "polvo_v2.mp4"))
