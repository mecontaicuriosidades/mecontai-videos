"""Vídeo monetizável (>60s): Polvo – o animal mais alienígena da Terra."""
import math, sys
import numpy as np
from motor import render, pop, ease, fnt, AMARELO, CIANO
from video_polvo import polvo, coracao

AZUL_MAR = ((40, 140, 220), (15, 50, 130))
FUNDO_MAR = ((20, 70, 140), (6, 20, 60))


def bolhas(d, T, n=14, seed=1):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = rng.uniform(60, 1020); r = rng.uniform(8, 22)
        y = 1250 - ((T * rng.uniform(60, 140) + rng.uniform(0, 1100)) % 1100)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(200, 235, 255), width=4)


def c_coracoes(d, img, t, T):
    bolhas(d, T)
    polvo(d, 540, 680, T)
    for i, x in enumerate((300, 540, 780)):
        ti = 1.0 + i * 0.5
        if t > ti:
            r = 72 * pop((t - ti) / 0.4) * (1 + 0.1 * math.sin(T * 9 + i))
            coracao(d, x, 1120, r)
            d.text((x, 1215), ["BRÂNQUIA", "CORPO", "BRÂNQUIA"][i], font=fnt(34), fill="white", anchor="mm",
                   stroke_width=5, stroke_fill=(10, 15, 40))


def c_nadar(d, img, t, T):
    bolhas(d, T, seed=4)
    x = 140 + ((t * 160) % 800)
    polvo(d, x + 100, 700, T * 2.2)
    # coração principal: bate, depois para quando ele nada
    bate = t < 2.2
    r = 85 * (1 + (0.12 * math.sin(T * 10) if bate else 0))
    coracao(d, 540, 1130, r, cor=(235, 40, 70) if bate else (120, 120, 135))
    if not bate:
        d.text((540, 1130), "PAUSA", font=fnt(46), fill="white", anchor="mm", stroke_width=6, stroke_fill=(10, 15, 40))


def c_sangue(d, img, t, T):
    bolhas(d, T, seed=7)
    polvo(d, 540, 680, T, cor=(110, 150, 255))
    for i in range(6):
        ti = 0.8 + i * 0.22
        if t > ti:
            gx, gy = 200 + i * 136, 1120 + math.sin(T * 4 + i) * 18
            r = 38 * pop((t - ti) / 0.4)
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(40, 120, 255), outline=(10, 30, 90), width=5)
            d.polygon([(gx - r * 0.7, gy - r * 0.7), (gx + r * 0.7, gy - r * 0.7), (gx, gy - r * 2)], fill=(40, 120, 255))
    if t > 2.5:
        s = pop((t - 2.5) / 0.5)
        d.rounded_rectangle([370, 1190, 710, 1260], 30, fill=(184, 115, 51))
        d.text((540, 1225), "Cu = COBRE", font=fnt(int(40 * max(s, .1))), fill="white", anchor="mm")


def c_neuronios(d, img, t, T):
    polvo(d, 540, 640, T, cor=(200, 100, 230))
    rng = np.random.default_rng(2)
    for i in range(70):  # pontinhos de neurônio nos braços
        k = rng.integers(3, 14); arm = rng.integers(0, 8)
        base = 540 - 170 + arm * 48
        x = base + math.sin(T * 4 + arm + k * 0.45) * (6 + k * 3)
        y = 640 + math.sin(T * 3) * 18 + 120 + k * 22
        a = 0.5 + 0.5 * math.sin(T * 6 + i)
        if t > 0.5 + i * 0.02:
            r = 5 + 4 * a
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 120))
    n = int(500_000_000 * ease(t / 2.5))
    txt = f"{n:,}".replace(",", ".")
    d.text((540, 1150), txt, font=fnt(92), fill=AMARELO, anchor="mm", stroke_width=9, stroke_fill=(10, 15, 40))
    d.text((540, 1235), "NEURÔNIOS", font=fnt(44), fill="white", anchor="mm", stroke_width=6, stroke_fill=(10, 15, 40))


def c_ventosas(d, img, t, T):
    bolhas(d, T, seed=9)
    # um braço grande em curva, cheio de ventosas
    pts = []
    for k in range(40):
        a = k / 39
        x = 120 + a * 860
        y = 800 + math.sin(a * 5 + T * 2) * 110 * (1 - a * 0.3)
        pts.append((x, y))
    for k in range(len(pts) - 1):
        w = int(120 - k * 2.2)
        d.line([pts[k], pts[k + 1]], fill=(240, 110, 160), width=w)
        d.ellipse([pts[k][0] - w / 2, pts[k][1] - w / 2, pts[k][0] + w / 2, pts[k][1] + w / 2], fill=(240, 110, 160))
    for k in range(2, 38, 3):
        x, y = pts[k]; r = 26 - k * 0.45
        d.ellipse([x - r, y + 10 - r, x + r, y + 10 + r], fill=(255, 205, 220), outline=(150, 50, 90), width=4)
        if t > 1.5 and (k // 3) % 3 == int(T * 3) % 3:  # "faíscas" de sabor
            for j in range(4):
                ang = j * math.pi / 2 + T * 3
                d.line([(x + math.cos(ang) * r * 1.3, y + 10 + math.sin(ang) * r * 1.3),
                        (x + math.cos(ang) * r * 2, y + 10 + math.sin(ang) * r * 2)], fill=AMARELO, width=5)
    # peixinho sendo "provado"
    fx = 900 - (t * 60) % 300
    d.ellipse([fx - 60, 1050, fx + 60, 1110], fill=(255, 170, 40), outline=(90, 50, 10), width=5)
    d.polygon([(fx + 55, 1080), (fx + 105, 1045), (fx + 105, 1115)], fill=(255, 170, 40), outline=(90, 50, 10))
    d.ellipse([fx - 38, 1066, fx - 22, 1082], fill=(30, 20, 20))
    if t > 1.0:
        d.text((540, 1210), "TATO + PALADAR", font=fnt(48), fill="white", anchor="mm", stroke_width=6, stroke_fill=(10, 15, 40))


def c_camuflagem(d, img, t, T):
    # pedras ao fundo
    rng = np.random.default_rng(5)
    for i in range(9):
        x, y, r = rng.uniform(80, 1000), rng.uniform(900, 1220), rng.uniform(60, 130)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(120, 110, 95), outline=(70, 60, 50), width=5)
    cores = [(240, 110, 160), (120, 110, 95), (230, 90, 40), (90, 160, 90), (240, 110, 160)]
    k = (t * 0.8) % (len(cores) - 1)
    i0 = int(k); f = k - i0
    cor = tuple(int(cores[i0][j] * (1 - f) + cores[i0 + 1][j] * f) for j in range(3))
    polvo(d, 540, 640, T, cor=cor)
    # olho com "?" (provavelmente não enxerga cores)
    if t > 2.0:
        s = pop((t - 2.0) / 0.4)
        d.ellipse([800 - 70 * s, 360 - 45 * s, 800 + 70 * s, 360 + 45 * s], fill="white", outline=(10, 15, 40), width=6)
        d.ellipse([800 - 22 * s, 360 - 22 * s, 800 + 22 * s, 360 + 22 * s], fill=(10, 15, 40))
        d.text((900, 300), "?", font=fnt(int(80 * max(s, .1))), fill=AMARELO, anchor="mm", stroke_width=6, stroke_fill=(10, 15, 40))


CENAS = [
    dict(tipo="gancho", titulo="O ANIMAL MAIS ALIENÍGENA DA TERRA",
         fala="Esse animal tem três corações, sangue azul e pensa com os braços. E fica até o final, porque o último fato é o mais bizarro!"),
    dict(tipo="fato", titulo="3 CORAÇÕES", desenho=c_coracoes, fundo=AZUL_MAR,
         fala="O polvo tem três corações. Dois deles empurram o sangue pelas brânquias, onde ele pega oxigênio, e o terceiro manda esse sangue pro corpo todo."),
    dict(tipo="fato", titulo="QUANDO NADA, UM CORAÇÃO PARA", desenho=c_nadar, fundo=AZUL_MAR,
         fala="Agora, olha que estranho: quando o polvo nada, o coração principal para de bater! Por isso nadar cansa muito, e ele prefere rastejar pelo fundo."),
    dict(tipo="fato", titulo="SANGUE AZUL", desenho=c_sangue, fundo=FUNDO_MAR,
         fala="E o sangue dele é azul! Em vez de ferro, como o nosso, ele usa cobre, numa proteína chamada hemocianina, que funciona melhor na água gelada."),
    dict(tipo="fato", titulo="PENSA COM OS BRAÇOS", desenho=c_neuronios, fundo=((60, 30, 110), (15, 10, 50)), estrelas=True,
         fala="O polvo tem uns quinhentos milhões de neurônios, e cerca de dois terços deles ficam nos braços. Cada braço consegue agir quase sozinho!"),
    dict(tipo="fato", titulo="AS VENTOSAS SENTEM GOSTO", desenho=c_ventosas, fundo=AZUL_MAR,
         fala="E as ventosas não servem só pra grudar. Elas têm receptores que sentem o gosto das coisas. É como lamber o mundo com as mãos!"),
    dict(tipo="fato", titulo="CAMUFLAGEM INSTANTÂNEA", desenho=c_camuflagem, fundo=((70, 120, 150), (25, 50, 70)),
         fala="Agora o mais bizarro: ele muda de cor em menos de um segundo pra se camuflar. Mas os cientistas acham que ele nem enxerga cores! Como ele faz isso ainda é um mistério."),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Qual superpoder você queria?",
         fala="E você, qual desses superpoderes do polvo queria ter? Comenta aqui embaixo!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova aqui no Me Conta Aí. Segue pra não perder!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "polvo_longo.mp4"))
