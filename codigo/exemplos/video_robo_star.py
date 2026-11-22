"""Robô STAR que operou sozinho (TECNOLOGIA INSANA #1). Formato v3 (25–35 s)."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O

SERIE = "TECNOLOGIA INSANA #1"
METAL = (190, 200, 215); METAL2 = (130, 140, 160); LUZ = (80, 255, 200); TRIPA = (240, 150, 150); TRIPA2 = (200, 100, 110)
VERDE_CIR = (60, 150, 140)


def etiqueta(d):
    rotulo(d, 540, 300, SERIE, 44, CIANO)


def selo(d):
    rotulo(d, 540, 420, "SEGUE A MAIA +", 52, AMARELO)


def braco(d, bx, by, ang1, ang2, T, s=1.0):
    """Braço robótico de 2 segmentos saindo de uma base; devolve a ponta (agulha)."""
    d.rounded_rectangle([bx - 90 * s, by - 20 * s, bx + 90 * s, by + 60 * s], int(18 * s), fill=METAL2, outline=O, width=6)
    x1 = bx + math.cos(ang1) * 260 * s; y1 = by + math.sin(ang1) * 260 * s
    x2 = x1 + math.cos(ang2) * 230 * s; y2 = y1 + math.sin(ang2) * 230 * s
    d.line([(bx, by), (x1, y1)], fill=O, width=int(58 * s))
    d.line([(bx, by), (x1, y1)], fill=METAL, width=int(44 * s))
    d.line([(x1, y1), (x2, y2)], fill=O, width=int(46 * s))
    d.line([(x1, y1), (x2, y2)], fill=METAL, width=int(32 * s))
    for (x, y) in ((bx, by), (x1, y1)):
        d.ellipse([x - 34 * s, y - 34 * s, x + 34 * s, y + 34 * s], fill=METAL2, outline=O, width=5)
        on = (T * 2) % 1 < 0.5
        d.ellipse([x - 12 * s, y - 12 * s, x + 12 * s, y + 12 * s], fill=LUZ if on else (40, 120, 100))
    # ponta com agulha
    d.line([(x2, y2), (x2, y2 + 70 * s)], fill=O, width=int(12 * s))
    d.line([(x2, y2), (x2, y2 + 70 * s)], fill=(230, 235, 240), width=int(6 * s))
    return x2, y2 + 70 * s


def tripa(d, x0, x1, y, T, pontos=0, s=1.0):
    """Dois pedaços de intestino sendo unidos; 'pontos' = quantos pontos já costurados."""
    meio = (x0 + x1) / 2
    for a, b in ((x0, meio - 6), (meio + 6, x1)):
        d.rounded_rectangle([a, y - 55 * s, b, y + 55 * s], int(50 * s), fill=TRIPA, outline=O, width=6)
        for k in range(3):
            xx = a + (b - a) * (k + 1) / 4
            d.arc([xx - 30, y - 40 * s, xx + 30, y + 40 * s], 100, 260, fill=TRIPA2, width=5)
    for i in range(pontos):
        yy = y - 40 * s + i * (80 * s / max(1, 5))
        d.line([(meio - 22, yy), (meio + 22, yy + 12)], fill=(40, 40, 70), width=6)


def g_sozinho(d, img, t, T):
    etiqueta(d)
    # mesa de cirurgia
    d.rectangle([180, 1120, 1000, 1170], fill=VERDE_CIR, outline=O, width=6)
    d.rectangle([560, 1170, 620, 1300], fill=METAL2, outline=O, width=5)
    pontos = int((T * 1.5) % 6)
    tripa(d, 340, 940, 1050, T, pontos)
    a = -0.55 + 0.08 * math.sin(T * 2)
    braco(d, 900, 640, math.pi - 0.9 + 0.05 * math.sin(T * 3), math.pi / 2 - 0.25 + a * 0.2, T, 0.95)
    # placa SEM HUMANOS
    rotulo(d, 300, 620, "0 HUMANOS", 52, AMARELO)
    brilhos(d, 640, 1000, 60, T, 5, LUZ)


def c_star(d, img, t, T):
    selo(d)
    # robô com "rosto" de tela e o nome STAR
    k = pop(min(1, t / 0.7))
    cx, cy = 400, 860
    d.rounded_rectangle([cx - 170 * k, cy - 220 * k, cx + 170 * k, cy + 200 * k], int(40 * k) + 1, fill=METAL, outline=O, width=7)
    d.rounded_rectangle([cx - 130 * k, cy - 180 * k, cx + 130 * k, cy - 20 * k], int(24 * k) + 1, fill=(15, 30, 40), outline=O, width=5)
    for sx in (-1, 1):
        d.ellipse([cx + sx * 60 * k - 22 * k, cy - 120 * k, cx + sx * 60 * k + 22 * k, cy - 76 * k], fill=LUZ)
    d.arc([cx - 50 * k, cy - 100 * k, cx + 50 * k, cy - 40 * k], 20, 160, fill=LUZ, width=6)
    rotulo(d, cx, cy + 80 * k, "STAR", int(70 * k) + 1, AMARELO, traduzir=False)
    d.line([(cx, cy - 220 * k), (cx, cy - 280 * k)], fill=O, width=8)
    d.ellipse([cx - 18, cy - 300 * k, cx + 18, cy - 264 * k], fill=(255, 80, 80) if (T * 2) % 1 < 0.5 else (120, 30, 30), outline=O, width=4)
    # ao lado: intestino de porco + ano
    tripa(d, 620, 960, 760, T, int(min(5, t * 2)), 0.8)
    rotulo(d, 790, 880, "INTESTINO DE PORCO", 38, TRIPA)
    rotulo(d, 790, 1000, "2022", 80, AMARELO, traduzir=False)
    rotulo(d, 790, 1090, "EUA", 48, (255, 255, 255))


def c_furo(d, img, t, T):
    selo(d)
    # barriga vista de cima com 3 furinhos e ferramentas finas entrando
    d.ellipse([150, 700, 930, 1240], fill=(245, 190, 200), outline=O, width=7)
    furos = [(380, 900), (540, 860), (700, 900)]
    for i, (x, y) in enumerate(furos):
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(120, 40, 60), outline=O, width=4)
        k = min(1, max(0, t - 0.3 * i) / 1.0)
        topo = y - 330 + 140 * k
        d.line([(x + (i - 1) * 60, topo), (x, y)], fill=O, width=16)
        d.line([(x + (i - 1) * 60, topo), (x, y)], fill=METAL, width=8)
    # câmera no tubo do meio
    d.rounded_rectangle([500, 520, 580, 600], 14, fill=(40, 40, 60), outline=O, width=5)
    d.ellipse([520, 540, 560, 580], fill=LUZ if (T * 3) % 1 < 0.6 else (60, 160, 140))
    rotulo(d, 790, 560, "CÂMERA 3D", 46, CIANO)
    rotulo(d, 540, 1120, "LAPAROSCOPIA", 54, AMARELO)


def c_melhor(d, img, t, T):
    selo(d)
    # placar: pontos alinhados (robô) vs tortos (humano)
    for i, (nome, alinhado, x) in enumerate((("ROBÔ", True, 300), ("HUMANO", False, 780))):
        d.rounded_rectangle([x - 200, 560, x + 200, 1000], 30, fill=(250, 250, 255), outline=O, width=7)
        d.rounded_rectangle([x - 200, 560, x + 200, 650], 30, fill=(40, 170, 90) if alinhado else (200, 80, 80), outline=O, width=7)
        rotulo(d, x, 606, nome, 48, (255, 255, 255))
        d.rounded_rectangle([x - 150, 680, x + 150, 880], 70, fill=TRIPA, outline=O, width=5)
        for j in range(6):
            if t > 0.25 * j:
                yy = 700 + j * 30
                dx = 0 if alinhado else 22 * math.sin(j * 2.7)
                dy = 0 if alinhado else 10 * math.cos(j * 1.9)
                d.line([(x - 26 + dx, yy + dy), (x + 26 + dx, yy + 12 - dy)], fill=(40, 40, 70), width=7)
    if t > 1.8:
        k = pop(min(1, (t - 1.8) / 0.5))
        rotulo(d, 300, 940, "MELHOR!", int(54 * k) + 1, (40, 170, 90))
    rotulo(d, 540, 1100, "SÓ EM PORCOS (POR ENQUANTO)", 40, CIANO)


def c_cta(d, img, t, T):
    g_sozinho(d, img, t, T)


CENAS = [
    dict(tipo="gancho", titulo="SOZINHO!", titulo_y=400, desenho=g_sozinho, fundo=((20, 70, 90), (8, 25, 40)),
         fala="Esse robô operou sozinho... e costurou melhor que cirurgiões! E o último fato é o mais louco."),
    dict(tipo="fato", titulo="O ROBÔ STAR", desenho=c_star, fundo=((30, 60, 100), (10, 25, 50)),
         fala="É o robô STAR, dos Estados Unidos. Segue a Maia pra mais tecnologia insana: em 2022, ele costurou intestino de porcos sem ajuda humana."),
    dict(tipo="fato", titulo="POR UM FURO", desenho=c_furo, fundo=((40, 80, 90), (15, 35, 45)),
         fala="E fez tudo por furinhos na barriga, guiado por uma câmera 3D."),
    dict(tipo="fato", titulo="MELHOR QUE NÓS", desenho=c_melhor, fundo=((30, 50, 80), (10, 20, 40)),
         fala="Segundo os cientistas, o resultado foi melhor que o de cirurgiões humanos. Por enquanto, só em porcos."),
    dict(tipo="cta", titulo="SOZINHO!", titulo_y=400, subtitulo="Segue a Maia +", subtitulo_y=520, desenho=c_cta,
         fundo=((20, 70, 90), (8, 25, 40)),
         fala="Segue a Maia: amanhã tem mais Tecnologia Insana. Porque esse robô..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "robo_star.mp4"))
