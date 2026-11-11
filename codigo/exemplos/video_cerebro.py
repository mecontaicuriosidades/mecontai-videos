"""Cérebro: não sente dor e gasta 20% da sua energia."""
import math, sys
import numpy as np
from motor import render, pop, ease, AMARELO, CIANO
from desenhos import rotulo, contador, olhos, sorriso, brilhos, seta, O

ROSA = (250, 165, 185)


def cerebro(d, cx, cy, s, T, rosto=True, brilho=False):
    d.ellipse([cx - 230 * s, cy - 170 * s, cx + 230 * s, cy + 160 * s], fill=ROSA, outline=O, width=8)
    for k in range(6):
        d.arc([cx - 210 * s + k * 60 * s, cy - 150 * s, cx - 90 * s + k * 60 * s, cy + 40 * s], 200, 340, fill=(220, 120, 145), width=7)
    for k in range(5):
        d.arc([cx - 180 * s + k * 70 * s, cy - 10 * s, cx - 60 * s + k * 70 * s, cy + 140 * s], 20, 160, fill=(220, 120, 145), width=7)
    d.line([(cx, cy - 165 * s), (cx, cy + 150 * s)], fill=(220, 120, 145), width=6)
    if brilho:
        rng = np.random.default_rng(int(T * 5))
        for i in range(10):
            x, y = cx + rng.uniform(-190, 190) * s, cy + rng.uniform(-130, 120) * s
            d.line([(x, y), (x + rng.uniform(-50, 50) * s, y + rng.uniform(-50, 50) * s)], fill=AMARELO, width=6)
    if rosto:
        olhos(d, cx, cy - 20 * s, T, 120 * s, 24 * s); sorriso(d, cx, cy + 50 * s, 35 * s)


def c_neuronios(d, img, t, T):
    cerebro(d, 540, 720, 1.1, T, brilho=True)
    contador(d, 540, 1120, 86000000000, t, 2.5, 80, "", AMARELO)
    rotulo(d, 540, 1200, "NEURÔNIOS", 44)


def c_energia(d, img, t, T):
    cerebro(d, 360, 720, 0.6, T)
    # bateria 20%
    d.rounded_rectangle([640, 560, 900, 900], 30, outline=O, width=9, fill=(240, 240, 245))
    d.rectangle([730, 530, 810, 560], fill=O)
    h = 330 * 0.2 * ease(t / 1.5)
    d.rectangle([652, 888 - h, 888, 888], fill=(120, 230, 120))
    if t > 1: rotulo(d, 770, 980, "20% DA ENERGIA", 46, AMARELO)
    if t > 2: rotulo(d, 360, 980, "2% DO PESO", 46, CIANO)


def c_dor(d, img, t, T):
    cerebro(d, 540, 760, 1.0, T)
    if t > 0.8:
        d.rounded_rectangle([250, 1000, 830, 1090], 40, fill=(15, 20, 50), outline=(230, 60, 80), width=6)
        rotulo(d, 540, 1045, "SEM SENSOR DE DOR", 46, (255, 120, 130))
    if t > 2: rotulo(d, 540, 1180, "CIRURGIA ACORDADO!", 56, AMARELO)


def c_mito(d, img, t, T):
    cerebro(d, 540, 760, 1.0, T, brilho=True)
    if t > 0.8:
        rotulo(d, 540, 500, "SÓ 10%?", 90, (255, 120, 120))
        d.line([(330, 450), (750, 550)], fill=(230, 40, 40), width=16)
    if t > 2: rotulo(d, 540, 1150, "VOCÊ USA TUDO!", 64, AMARELO)


def c_velocidade(d, img, t, T):
    x = 140 + ((t * 500) % 800)
    d.line([(120, 820), (960, 820)], fill=(250, 200, 120), width=26)
    d.ellipse([x - 30, 790, x + 30, 850], fill=AMARELO, outline=O, width=5)
    for k in range(4): d.line([(x - 40 - k * 30, 820), (x - 60 - k * 30, 820)], fill="white", width=6)
    contador(d, 540, 1080, 430, t, 2, 100, " km/h", AMARELO)


def c_sonho(d, img, t, T):
    cerebro(d, 540, 820, 0.9, T, rosto=False)
    for sx in (-1, 1): d.arc([540 + sx * 55 - 25, 790, 540 + sx * 55 + 25, 830], 20, 160, fill=O, width=7)
    for k in range(4):
        x, y = 540 + math.cos(T + k * 1.6) * 330, 560 + math.sin(T + k * 1.6) * 80
        d.ellipse([x - 50, y - 35, x + 50, y + 35], fill=(200, 190, 255), outline=O, width=4)
    if t > 1.5: rotulo(d, 540, 1150, "ARRUMA A MEMÓRIA", 60, AMARELO)


def g_cer(d, img, t, T):
    cerebro(d, 600, 760, 1.15, T, brilho=True)
    brilhos(d, 600, 760, 380, T, 8)


NOITE = ((40, 20, 80), (12, 6, 30))
CENAS = [
    dict(tipo="gancho", titulo="O CÉREBRO NÃO SENTE DOR", desenho=g_cer, fundo=NOITE, estrelas=True,
         fala="O seu cérebro sente a dor do corpo inteiro, mas ele mesmo não sente dor nenhuma! E ainda tem um mito sobre ele que quase todo mundo acredita."),
    dict(tipo="fato", titulo="86 BILHÕES DE NEURÔNIOS", desenho=c_neuronios, fundo=NOITE, estrelas=True,
         fala="Ele tem uns oitenta e seis bilhões de neurônios, conectados por trilhões de ligações. É a estrutura mais complexa que a gente conhece."),
    dict(tipo="fato", titulo="UM GASTÃO DE ENERGIA", desenho=c_energia, fundo=((30, 70, 60), (10, 30, 25)),
         fala="O cérebro pesa só uns dois por cento do corpo, mas gasta uns vinte por cento de toda a energia que você consome. Pensar dá trabalho!"),
    dict(tipo="fato", titulo="NÃO SENTE DOR", desenho=c_dor, fundo=((70, 30, 50), (30, 10, 20)),
         fala="O tecido do cérebro não tem sensores de dor. Por isso algumas cirurgias são feitas com o paciente acordado, conversando com o médico!"),
    dict(tipo="fato", titulo="O MITO DOS 10%", desenho=c_mito, fundo=((20, 50, 100), (8, 20, 50)),
         fala="E aquela história de que a gente só usa dez por cento do cérebro é mito! Exames mostram que praticamente todas as áreas trabalham ao longo do dia."),
    dict(tipo="fato", titulo="SINAIS EM ALTA VELOCIDADE", desenho=c_velocidade, fundo=((50, 30, 90), (20, 10, 40)),
         fala="Os sinais nos nervos mais rápidos podem chegar a uns quatrocentos e trinta quilômetros por hora. Mais rápido que um carro de Fórmula 1!"),
    dict(tipo="fato", titulo="FAXINA DURANTE O SONO", desenho=c_sonho, fundo=((15, 15, 50), (5, 5, 20)), estrelas=True,
         fala="E o mais bizarro: enquanto você dorme, o cérebro organiza as memórias do dia e faz uma espécie de faxina, lavando resíduos. Dormir bem é manutenção!"),
    dict(tipo="cta", titulo="COMENTA AÍ!", subtitulo="Acreditava nos 10%?",
         fala="Confessa: você acreditava no mito dos dez por cento? Comenta aqui!"),
    dict(tipo="cta", titulo="SEGUE PRA MAIS!", subtitulo="Eu sou a Maia do Me ContAI",
         fala="Eu sou a Maia, e todo dia tem curiosidade nova. Segue o Me Conta Aí!"),
]

if __name__ == "__main__":
    print("duração:", render(CENAS, sys.argv[1] if len(sys.argv) > 1 else "cerebro.mp4"))
