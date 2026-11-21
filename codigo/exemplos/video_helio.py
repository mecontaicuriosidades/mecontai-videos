"""Hélio superfluido (CIÊNCIA BIZARRA #2). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, termometro, O

SERIE = "CIÊNCIA BIZARRA #2"
LIQ = (120, 220, 255); LIQ2 = (60, 160, 230); VIDRO = (225, 245, 255); METAL = (150, 160, 180)
ROXO = (170, 120, 255)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def copo(d, cx, cy, w, h, nivel, T, filme=1.0):
    """Copo de vidro com líquido; 'filme' (0..1) desenha a película subindo pela parede e pingando fora."""
    topo, base = cy - h, cy + h
    yl = base - (2 * h - 20) * nivel
    # líquido
    d.rectangle([cx - w + 8, yl, cx + w - 8, base - 8], fill=LIQ)
    d.line([(cx - w + 8, yl), (cx + w - 8, yl)], fill=(240, 255, 255), width=6)
    # película subindo pelas paredes (por dentro e por fora)
    if filme > 0:
        for lado in (-1, 1):
            x = cx + lado * w
            alto = yl - (yl - topo) * min(1, filme)
            d.line([(x - lado * 10, yl), (x - lado * 10, alto)], fill=LIQ2, width=16)
            if filme >= 1:
                d.arc([x - 22, topo - 22, x + 22, topo + 22], 180 if lado < 0 else 270, 360 if lado < 0 else 450, fill=LIQ2, width=10)
                d.arc([x - 22, topo - 22, x + 22, topo + 22], 180, 360, fill=LIQ2, width=10)
                d.line([(x + lado * 14, topo), (x + lado * 14, base - 30)], fill=LIQ2, width=16)
                # gota pingando
                f = (T * 1.2 + (0.5 if lado > 0 else 0)) % 1
                gy = base - 20 + f * 160
                d.ellipse([x + lado * 12 - 16, gy - 22, x + lado * 12 + 16, gy + 22], fill=LIQ, outline=O, width=3)
    # vidro
    d.line([(cx - w, topo), (cx - w, base)], fill=O, width=14)
    d.line([(cx + w, topo), (cx + w, base)], fill=O, width=14)
    d.line([(cx - w, base), (cx + w, base)], fill=O, width=14)
    d.line([(cx - w, topo), (cx - w, base)], fill=VIDRO, width=6)
    d.line([(cx + w, topo), (cx + w, base)], fill=VIDRO, width=6)
    d.line([(cx - w, base), (cx + w, base)], fill=VIDRO, width=6)
    d.line([(cx - w + 30, topo + 40), (cx - w + 30, topo + 160)], fill=(255, 255, 255), width=8)


def g_foge(d, img, t, T):
    etiqueta(d)
    nivel = 0.55 + 0.15 * math.cos(T * 0.8)
    copo(d, 560, 960, 210, 230, nivel, T, 1.0)
    # poça no chão
    d.ellipse([260, 1225, 860, 1275], fill=LIQ, outline=O, width=4)
    for lado in (-1, 1):
        seta(d, 560 + lado * 300, 1000, 560 + lado * 300, 800, AMARELO, 12)
    rotulo(d, 900, 640, "-271 °C", 52, LIQ)


def c_frio(d, img, t, T):
    selo(d)
    termometro(d, 260, 1230, 0.05, (90, 170, 255), 640)
    rotulo(d, 260, 520, "-271 °C", 50, LIQ)
    # átomos de hélio em fila andando sem parar (sem atrito)
    for i in range(4):
        x = 420 + ((i * 150 + T * 260) % 600)
        y = 800 + 30 * math.sin(T * 3 + i)
        d.ellipse([x - 55, y - 55, x + 55, y + 55], fill=ROXO, outline=O, width=6)
        rotulo(d, x, y, "He", 46, (255, 255, 255), traduzir=False)
    rotulo(d, 720, 980, "HÉLIO", 64, ROXO)
    rotulo(d, 720, 1080, "ATRITO 0", 58, AMARELO)


def c_sobe(d, img, t, T):
    selo(d)
    k = min(1.0, t / 2.6)
    copo(d, 540, 950, 260, 260, 0.45 - 0.15 * k, T, k * 1.05)
    d.ellipse([220, 1205, 860, 1260], fill=LIQ, outline=O, width=4)
    if k > 0.3:
        rotulo(d, 880, 620, "PELÍCULA", 46, LIQ)
        seta(d, 870, 650, 815, 760, LIQ, 8)


def prensa(d, cx, cy, k, T):
    d.rectangle([cx - 230, cy - 360, cx + 230, cy - 320], fill=METAL, outline=O, width=6)
    d.rectangle([cx - 20, cy - 320, cx + 20, cy - 200 + 120 * k], fill=METAL, outline=O, width=5)
    d.rectangle([cx - 180, cy - 200 + 120 * k, cx + 180, cy - 150 + 120 * k], fill=METAL, outline=O, width=6)
    # caixa com hélio
    d.rectangle([cx - 190, cy - 150, cx + 190, cy + 150], outline=O, width=12)
    topo = cy - 150 + 120 * k + 10
    if k < 0.9:
        d.rectangle([cx - 180, max(topo, cy - 40), cx + 180, cy + 140], fill=LIQ)
        for i in range(4):
            x = cx - 140 + i * 90
            d.arc([x - 30, cy - 60 + 10 * math.sin(T * 5 + i), x + 30, cy - 20 + 10 * math.sin(T * 5 + i)], 0, 180, fill=LIQ2, width=6)
    else:
        for i in range(4):
            for j in range(2):
                x = cx - 135 + i * 90; y = cy + 10 + j * 75
                d.polygon([(x, y - 35), (x + 35, y), (x, y + 35), (x - 35, y)], fill=(235, 250, 255), outline=O)


def c_nao_congela(d, img, t, T):
    selo(d)
    termometro(d, 200, 1230, 0.0, (90, 170, 255), 600)
    rotulo(d, 200, 560, "0 K", 54, LIQ, traduzir=False)
    k = min(1, max(0, (t - 2.2) / 1.6))
    prensa(d, 640, 990, k, T)
    rotulo(d, 640, 1195, "PRESSÃO", 52, AMARELO)


def c_cta(d, img, t, T):
    g_foge(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="ELE FOGE!", titulo_y=400, desenho=g_foge, fundo=((40, 60, 130), (15, 20, 60)),
         fala="Esse líquido sobe sozinho pela parede do copo... e foge! E o último fato é o pior."),
    dict(tipo="fato", titulo="HÉLIO", desenho=c_frio, fundo=((70, 40, 120), (30, 15, 60)),
         fala="É hélio, a quase menos duzentos e setenta e um graus. Segue a Maia, que piora: aí ele vira superfluido, sem atrito."),
    dict(tipo="fato", titulo="ELE ESCALA", desenho=c_sobe, fundo=((30, 100, 140), (10, 45, 75)),
         fala="Uma película finíssima sobe pela parede, passa pela borda e pinga do lado de fora."),
    dict(tipo="fato", titulo="NÃO CONGELA", desenho=c_nao_congela, fundo=((50, 55, 95), (20, 22, 45)),
         fala="E nem no zero absoluto ele congela. Só vira sólido se for espremido com muita pressão."),
    dict(tipo="cta", titulo="ELE FOGE!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((40, 60, 130), (15, 20, 60)),
         fala="Segue a Maia: amanhã tem mais Ciência Bizarra. Porque esse líquido..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "helio.mp4"))
