"""Rã-da-madeira, Parte 2 (BICHOS INSANOS #6). Formato v3 (25–35 s). Importa desenhos de video_ra_madeira_p1."""
import math, sys
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, seta, brilhos, O
from video_ra_madeira_p1 import etiqueta, selo, ra, coracao, GELO, GELO2, NEVE

FIGADO = (150, 50, 60); SANGUE = (200, 40, 55); ACUCAR = (250, 250, 245)
CELULA = (255, 190, 120); CELULA2 = (230, 140, 80); GRAMA = (90, 170, 80)


def g_revive(d, img, t, T, parte="P2"):
    etiqueta(d, parte)
    # gotas de gelo derretendo e a rã acordando
    k = 0.5 + 0.5 * math.sin(T * 1.0)
    d.ellipse([230, 1180, 890, 1260], fill=(120, 190, 230), outline=O, width=4)
    ra(d, 560, 1030, 1.1, gelo=1 - k, T=T, olho_aberto=k > 0.4)
    for i in range(6):
        f = (T * 0.9 + i / 6) % 1
        x = 330 + i * 85
        y = 760 + f * 420
        d.ellipse([x - 12, y - 18, x + 12, y + 18], fill=GELO, outline=O, width=3)
    # coração batendo no peito
    p = 1 + 0.18 * max(0, math.sin(T * 8))
    coracao(d, 560, 950, 0.55 * p, SANGUE)
    brilhos(d, 560, 960, 230, T, 6, AMARELO)


def c_acucar(d, img, t, T):
    selo(d)
    # fígado à esquerda, vaso sanguíneo atravessando, cubinhos de açúcar correndo
    d.polygon([(130, 700), (330, 640), (470, 700), (430, 860), (260, 900), (140, 830)], fill=FIGADO, outline=O)
    d.line([(130, 700), (330, 640), (470, 700), (430, 860), (260, 900), (140, 830), (130, 700)], fill=O, width=6)
    rotulo(d, 300, 770, "FÍGADO", 46, NEVE)
    d.rounded_rectangle([60, 1000, 1020, 1140], 70, fill=SANGUE, outline=O, width=6)
    n = 4 + int(10 * ease(t / 3.0))
    for i in range(n):
        x = 100 + ((i * 97 + T * 220) % 880)
        y = 1045 + (i % 3) * 22
        d.rectangle([x - 20, y - 20, x + 20, y + 20], fill=ACUCAR, outline=O, width=3)
    seta(d, 380, 880, 520, 990, AMARELO)
    rotulo(d, 780, 760, "GLICOSE", 60, AMARELO)
    rotulo(d, 780, 840, "ANTICONGELANTE", 44, GELO)


def c_celulas(d, img, t, T):
    selo(d)
    # espaço entre as células cheio de gelo; células inteiras por dentro
    k = min(1, ease(t / 2.4))
    for i in range(12):
        a = i * 0.9 + 0.4
        x = 140 + (i % 4) * 270 + 20 * math.sin(i)
        y = 560 + (i // 4) * 230
        r = 14 + 8 * k
        d.polygon([(x, y - r * 2), (x + r, y), (x, y + r * 2), (x - r, y)], fill=NEVE, outline=O)
    for i, (cx, cy) in enumerate(((330, 690), (750, 690), (540, 930), (300, 1150), (780, 1150))):
        d.ellipse([cx - 130, cy - 95, cx + 130, cy + 95], fill=CELULA, outline=O, width=6)
        d.ellipse([cx - 40, cy - 30, cx + 40, cy + 30], fill=CELULA2, outline=O, width=4)
        for j in range(3):
            x = cx - 80 + j * 70; y = cy + 50 - (j % 2) * 100
            d.rectangle([x - 11, y - 11, x + 11, y + 11], fill=ACUCAR, outline=O, width=2)


def c_ordem(d, img, t, T):
    selo(d)
    # sequência de descongelar: coração → cérebro → pernas
    etapa = min(3, int(t / 1.6) + 1)
    d.rectangle([0, 1170, 1080, 1320], fill=GRAMA)
    for i in range(10):
        x = 60 + i * 110
        d.polygon([(x, 1170), (x + 20, 1110), (x + 40, 1170)], fill=(120, 200, 100), outline=O)
    itens = [(220, "1", "CORAÇÃO"), (540, "2", "CÉREBRO"), (860, "3", "PERNAS")]
    for k, (x, n, nome) in enumerate(itens):
        ativo = k < etapa
        cor = AMARELO if ativo else (120, 130, 160)
        d.ellipse([x - 120, 560, x + 120, 800], fill=(30, 35, 70), outline=cor, width=10)
        if k == 0:
            p = 1 + (0.2 * max(0, math.sin(T * 8)) if ativo else 0)
            coracao(d, x, 670, 0.9 * p, SANGUE if ativo else (120, 160, 200))
        elif k == 1:
            c = (250, 170, 190) if ativo else (150, 170, 200)
            d.ellipse([x - 75, 610, x + 75, 730], fill=c, outline=O, width=5)
            d.line([(x, 615), (x, 725)], fill=O, width=4)
            if ativo:
                for j in range(3):
                    a = T * 4 + j * 2.1
                    d.line([(x + 80 * math.cos(a), 670 + 80 * math.sin(a)), (x + 105 * math.cos(a), 670 + 105 * math.sin(a))], fill=AMARELO, width=6)
        else:
            dy = -30 * abs(math.sin(T * 5)) if ativo else 0
            ra(d, x, 700 + dy, 0.33, gelo=0.0 if ativo else 1.0, T=T, olho_aberto=ativo)
        rotulo(d, x, 860, nome, 42, cor)
        rotulo(d, x, 530, n, 54, cor, traduzir=False)
        if k < 2:
            seta(d, x + 130, 680, x + 190, 680, cor, 10)
    ra(d, 540, 1150, 0.4, gelo=max(0, 1 - t / 4.5), T=T, olho_aberto=etapa >= 2)


def c_cta(d, img, t, T):
    g_revive(d, img, t, T, "P2")


CENAS = [
    dict(tipo="gancho", titulo="REVIVE!", titulo_y=400, desenho=g_revive, fundo=((50, 120, 110), (20, 55, 60)),
         fala="Essa rã congelada volta a viver sozinha na primavera! E o jeito é bizarro."),
    dict(tipo="fato", titulo="AÇÚCAR", desenho=c_acucar, fundo=((120, 50, 70), (60, 20, 35)),
         fala="O segredo é açúcar. Segue a Maia, que piora: no frio, o fígado enche o sangue de glicose, um anticongelante natural."),
    dict(tipo="fato", titulo="SÓ POR FORA", desenho=c_celulas, fundo=((60, 110, 160), (25, 50, 90)),
         fala="O gelo fica só do lado de fora das células. Por dentro, o açúcar impede que elas congelem e estourem."),
    dict(tipo="fato", titulo="NA ORDEM", desenho=c_ordem, fundo=((50, 60, 110), (20, 25, 55)),
         fala="Na primavera, ela descongela de dentro pra fora: primeiro volta o coração, depois o cérebro, e só então as pernas."),
    dict(tipo="cta", titulo="REVIVE!", titulo_y=400, subtitulo="Parte 1 no perfil", subtitulo_y=520, desenho=c_cta,
         fundo=((50, 120, 110), (20, 55, 60)),
         fala="Segue pra ver o próximo Bichos Insanos amanhã. Porque essa rã..."),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "ra_madeira_p2.mp4"))
