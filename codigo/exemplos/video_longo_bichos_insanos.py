"""VÍDEO LONGO (16:9): Os 10 bichos mais insanos do planeta (série Bichos Insanos).
Roteiro novo, com mais contexto e fatos novos; desenhos dos Shorts ampliados + fichas novas.
Uso: python3 video_longo_bichos_insanos.py saida.mp4   |   folha: python3 video_longo_bichos_insanos.py --folha f.jpg [inicio]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from motor_longo import render_longo, folha
import video_peixe_bruxa as pb, video_acaros as ac, video_formigas as fo, video_tubarao as tu, video_peixe_pedra as pp
import video_baiacu as ba, video_fungo_zumbi as fz, video_vespa_do_mar as vm, video_camarao_pistola as cp, video_tardigrado as ta

MAR = ((20, 90, 140), (5, 30, 60))
ROXO = ((70, 40, 120), (20, 10, 45))
VERDE = ((50, 110, 60), (15, 40, 20))
FOGO = ((150, 60, 30), (50, 15, 10))
NOITE = ((20, 20, 70), (5, 5, 25))
ROSA = ((150, 40, 90), (50, 10, 35))


def item(n, nome, sub, fundo, abre, fatos, ficha, cap=None):
    """Monta as cenas de um item: abertura (#n + nome), fatos e uma ficha com número."""
    vert_abre, fala_abre = abre
    cenas = [dict(tipo="abre", item=n, nome=nome, subtitulo=sub, vert=vert_abre, fundo=fundo,
                  fala=fala_abre, capitulo=cap or f"#{n} " + nome.title().replace("-Da-", "-da-").replace("-Do-", "-do-"))]
    for titulo, vert, f, fala in fatos:
        cenas.append(dict(tipo="fato", item=n, titulo=titulo, vert=vert, fundo=f or fundo, fala=fala))
    num, titulo, vert, fala, extra = ficha
    cenas.append(dict(tipo="ficha", item=n, numero=num, titulo=titulo, vert=vert, fundo=fundo, fala=fala, **extra))
    return cenas


CENAS = [
    dict(tipo="abre", item=None, nome="OS 10 BICHOS MAIS INSANOS DO PLANETA", subtitulo="e o número 1 sobreviveu ao espaço",
         vert=ta.g_espaco, fundo=NOITE, capitulo="Abertura",
         fala="Um bicho que aguenta o vácuo do espaço. Um peixe que vira gosma. E um camarão que dispara bolhas quase tão quentes quanto o Sol. "
              "Hoje são os dez bichos mais insanos do planeta, do menos ao mais absurdo. E o número um vai te fazer olhar diferente pro musgo do seu quintal."),
]

CENAS += item(10, "PEIXE-BRUXA", "a fábrica de gosma", MAR,
    (pb.g_gosma, "Número dez: o peixe-bruxa. Parece uma enguia, mas não é. E ele tem a defesa mais nojenta do oceano."),
    [("BALDE DE GOSMA", pb.c_balde, ((60, 90, 150), (20, 30, 70)),
      "Quando um predador ataca, ele solta um muco cheio de fibras que incha em contato com a água. Em poucos segundos, um único peixe-bruxa transforma a água em volta num balde de gosma."),
     ("TUBARÃO ENGASGADO", pb.c_tubarao, None,
      "Cientistas já filmaram tubarões mordendo um peixe-bruxa e cuspindo na hora, com as guelras entupidas. O caçador vira a vítima."),
     ("NÓ DE LIMPEZA", pb.c_no, ((120, 70, 130), (40, 20, 60)),
      "E pra não se afogar na própria meleca, ele dá um nó no próprio corpo e escorrega por dentro dele, raspando a gosma. Ele não tem coluna vertebral de verdade, por isso é tão flexível."),
     ],
    (300, "MILHÕES DE ANOS NO PLANETA", pb.g_gosma,
     "E esse visual de outro mundo é antigo: o peixe-bruxa existe há mais de trezentos milhões de anos, desde antes dos dinossauros. Mas o próximo bicho está muito mais perto de você do que parece.",
     dict(sufixo=" mi")),
)

CENAS += item(9, "ÁCARO DEMODEX", "mora na sua cara", ROSA,
    (ac.g_poros, "Número nove. Agora mesmo, enquanto você assiste, tem bichinhos morando nos poros do seu rosto. São os ácaros Demodex."),
    [("QUASE TODO MUNDO", ac.c_todos, ((40, 110, 90), (10, 45, 35)),
      "Quase todo adulto tem. Eles medem um terço de milímetro, têm oito perninhas curtas e vivem de cabeça pra baixo, dentro dos folículos dos pelos."),
     ("COMEM SUA PELE", ac.c_oleo, ((150, 100, 40), (60, 35, 10)),
      "A comida deles é a oleosidade da sua pele. Eles vivem só umas duas semanas, e passam a vida inteira no mesmo rosto."),
     ("ENCONTRO NOTURNO", ac.c_noite, ((30, 25, 90), (8, 5, 35)),
      "E à noite, enquanto você dorme, eles saem do poro, andam pela sua cara procurando um par e depois voltam pra toca."),
     ],
    (0.3, "MILÍMETRO DE TAMANHO", ac.c_mae,
     "Um estudo de dois mil e vinte e dois mostrou que eles dependem tanto da gente que perderam genes e já não sobrevivem longe da pele humana. E você pegou os seus da sua mãe, logo depois de nascer. Mas se eles são muitos, espera até ver o número oito.",
     dict(sufixo=" mm")),
)

CENAS += item(8, "FORMIGAS", "as donas do planeta", VERDE,
    (fo.g_form, "Número oito: as formigas. Parecem comuns, mas juntas elas fazem coisas que nenhum outro bicho faz."),
    [("20 QUATRILHÕES", fo.c_numero, ((20, 20, 50), (5, 5, 20)),
      "Um estudo de dois mil e vinte e dois estimou vinte quatrilhões de formigas na Terra. Somadas, elas pesam mais do que todas as aves e mamíferos selvagens juntos."),
     ("AGRICULTORAS", fo.c_fungos, ((110, 80, 50), (50, 30, 15)),
      "As cortadeiras não comem as folhas que carregam. Elas usam as folhas pra cultivar uma horta de fungos, e comem o fungo. Fazem agricultura há uns cinquenta milhões de anos, muito antes da gente."),
     ("PONTE VIVA", fo.c_ponte, ((140, 200, 240), (80, 140, 200)),
      "E as formigas-de-correição usam o próprio corpo como tijolo: se seguram umas nas outras e montam pontes vivas pra colônia inteira passar."),
     ],
    (2.5, "MILHÕES DE FORMIGAS POR PESSOA", fo.c_forca,
     "Fazendo a conta, são uns dois milhões e meio de formigas pra cada ser humano. Mas o próximo bicho não ganha no número. Ele ganha no tempo.",
     dict(sufixo=" mi")),
)

CENAS += item(7, "TUBARÃO-DA-GROENLÂNDIA", "o vertebrado mais velho do mundo", ((60, 90, 120), (15, 25, 45)),
    (tu.g_tub, "Número sete. Os tubarões existem antes das árvores. E um deles pode ter nascido antes do Brasil virar país."),
    [("MAIS VELHOS QUE AS ÁRVORES", tu.c_idade, MAR,
      "Os primeiros tubarões surgiram há uns quatrocentos e cinquenta milhões de anos. As primeiras árvores só apareceram dezenas de milhões de anos depois."),
     ("DEVAGAR QUASE PARANDO", tu.c_groenlandia, None,
      "O tubarão-da-Groenlândia vive no mar gelado do Ártico, nada a pouco mais de um quilômetro por hora e cresce só uns um centímetro por ano."),
     ("A IDADE PELO OLHO", tu.c_eletrico, ((30, 120, 170), (10, 50, 90)),
      "Em dois mil e dezesseis, cientistas descobriram a idade deles analisando o cristalino do olho, que se forma antes do nascimento. O maior tinha, provavelmente, perto de quatrocentos anos."),
     ],
    (150, "ANOS PARA VIRAR ADULTO", tu.g_tub,
     "E o mais louco: ele só fica adulto por volta dos cento e cinquenta anos. Ou seja, um adolescente de cem anos. Mas o próximo da lista é o tipo de bicho que você nunca quer encontrar na praia.",
     dict(prefixo="~")),
)

CENAS += item(6, "PEIXE-PEDRA", "o peixe mais venenoso do mundo", ((40, 150, 170), (10, 50, 80)),
    (pp.g_pisada, "Número seis: o peixe-pedra. Ele é considerado o peixe mais venenoso do mundo. E o perigo é que dá pra pisar nele sem ver."),
    [("DISFARCE PERFEITO", pp.c_disfarce, ((50, 120, 160), (15, 40, 70)),
      "Ele fica parado no fundo raso, coberto de algas, igualzinho a uma pedra, esperando um peixinho passar. O bote dele leva uma fração de segundo."),
     ("AGULHAS NAS COSTAS", pp.c_espinhos, ((90, 60, 130), (30, 20, 60)),
      "Nas costas, ele tem treze espinhos. Quando alguém pisa, a pressão empurra o veneno direto pra dentro do pé."),
     ("DOR NÍVEL 10", pp.c_dor, ((170, 60, 50), (60, 20, 20)),
      "Quem já passou por isso descreve uma das piores dores que existem. O pé incha rápido, e sem atendimento pode ser grave."),
     ],
    (13, "ESPINHOS COM VENENO", pp.c_agua,
     "O primeiro socorro é estranho: água bem quente, sem queimar, porque o calor ajuda a quebrar o veneno. E existe um soro específico pra ele. Mas o próximo veneno não tem soro nenhum.",
     dict()),
)

CENAS += [dict(tipo="cta", titulo="CHEGAMOS NA METADE!", subtitulo="Se inscreve no canal",
               fala="Chegamos na metade! Se você está curtindo, se inscreve no canal, que a Maia posta curiosidade todo dia. Agora, o top cinco.")]

CENAS += item(5, "BAIACU", "1.200 vezes mais forte que cianeto", ((20, 60, 70), (5, 20, 30)),
    (ba.g_baiacu, "Número cinco: o baiacu, o fugu do Japão. Ele carrega um veneno mil e duzentas vezes mais forte que cianeto. E mesmo assim, tem gente que paga caro pra comer."),
    [("ONDE FICA O VENENO", ba.c_onde, ((40, 120, 150), (10, 40, 70)),
      "O veneno, a tetrodotoxina, fica principalmente no fígado, nos ovários, nos olhos e na pele. E o mais curioso: o baiacu não fabrica o veneno sozinho. Ele vem de bactérias que entram pela comida."),
     ("NÃO TEM ANTÍDOTO", ba.c_antidoto, ((70, 30, 90), (25, 10, 40)),
      "Não existe antídoto. O veneno bloqueia os nervos e paralisa os músculos, mas a pessoa continua acordada. O tratamento é manter a respiração até o corpo eliminar o veneno."),
     ("SÓ COM LICENÇA", ba.c_licenca, ((150, 90, 40), (70, 35, 15)),
      "Por isso, no Japão, só cozinheiros com licença especial podem preparar o fugu, depois de anos de treino e de uma prova."),
     ],
    (1200, "VEZES MAIS FORTE QUE CIANETO", ba.c_imperador,
     "E por tradição, é a única comida que o imperador do Japão não pode comer. Mas o próximo bicho não te mata. Ele te transforma num zumbi.",
     dict(sufixo="x")),
)

CENAS += item(4, "FUNGO ZUMBI", "controla formigas", ((40, 90, 50), (10, 35, 20)),
    (fz.g_zumbi, "Número quatro. Na verdade, um fungo. Ele transforma formigas em zumbis, e faz isso sem nem tocar no cérebro delas."),
    [("A INVASÃO", fz.c_invasao, ((90, 60, 120), (30, 15, 50)),
      "O esporo gruda na formiga, atravessa a casca e se espalha pelo corpo, formando uma rede em volta dos músculos. O cérebro fica inteiro, mas o corpo passa a obedecer o fungo."),
     ("SOBE 25 CM", fz.c_sobe, ((60, 120, 90), (15, 45, 30)),
      "A formiga abandona a colônia e sobe numa planta, até uns vinte e cinco centímetros do chão, onde a umidade e a temperatura são perfeitas pro fungo crescer."),
     ("MORDIDA FINAL", fz.c_mordida, ((110, 150, 60), (35, 60, 20)),
      "Perto do meio-dia, ela morde a nervura de uma folha com toda a força e fica travada ali até morrer."),
     ],
    (48, "MILHÕES DE ANOS DE FOLHAS MORDIDAS", fz.c_chuva,
     "Dias depois, uma haste brota da cabeça dela e solta esporos nas formigas que passam embaixo. E acharam uma folha fóssil com essas marcas de mordida de quarenta e oito milhões de anos. Mas o próximo bicho não precisa de cérebro pra ser mortal.",
     dict(sufixo=" mi")),
)

CENAS += item(3, "VESPA-DO-MAR", "a água-viva que mata em minutos", ((10, 90, 150), (5, 25, 60)),
    (vm.g_vespa, "Número três: a vespa-do-mar, uma água-viva quase transparente da Austrália e do Sudeste Asiático. Ela pode matar uma pessoa em minutos."),
    [("SEM CÉREBRO", vm.c_olhos, ((20, 120, 140), (5, 40, 60)),
      "Ela não tem cérebro, mas tem vinte e quatro olhos, e alguns deles têm até lente. E ela não fica só boiando: nada atrás das presas."),
     ("3 METROS DE VENENO", vm.c_tentaculos, ((60, 40, 130), (15, 10, 50)),
      "São até quinze tentáculos em cada canto do corpo, com uns três metros cada, cobertos de milhões de arpõezinhos cheios de veneno."),
     ("ATACA O CORAÇÃO", vm.c_coracao, ((120, 20, 50), (40, 5, 20)),
      "O veneno ataca o coração e o sistema nervoso tão rápido que tem vítima que não consegue nem sair da água."),
     ],
    (24, "OLHOS E NENHUM CÉREBRO", vm.c_vinagre,
     "Por isso, nas praias do norte da Austrália tem vinagre em postes: ele desarma os arpões que ainda não dispararam. Mas a arma do próximo bicho não é veneno. É uma bolha.",
     dict()),
)

CENAS += item(2, "CAMARÃO-PISTOLA", "o atirador do fundo do mar", ((20, 90, 130), (5, 30, 60)),
    (cp.g_tiro, "Número dois: o camarão-pistola. Ele tem poucos centímetros, mas dispara um tiro sem nem encostar na presa."),
    [("A GARRA-PISTOLA", cp.c_garra, ((30, 140, 160), (10, 60, 90)),
      "Uma das garras é gigante. Ele fecha essa garra tão rápido que lança um jato de água e cria uma bolha de vapor."),
     ("QUASE UM SOL", cp.c_sol, ((120, 50, 20), (40, 15, 10)),
      "Quando a bolha estoura, por um instante, ela chega a uns quatro mil e setecentos graus, quase a temperatura da superfície do Sol. E ainda solta um flash de luz."),
     ("BARULHO ABSURDO", cp.c_barulho, ((40, 40, 110), (10, 10, 45)),
      "O estalo passa de duzentos decibéis perto da garra, um dos sons mais fortes do oceano. A onda de choque deixa os peixinhos atordoados."),
     ],
    (4700, "GRAUS DENTRO DA BOLHA", cp.c_sonar,
     "Na Segunda Guerra, colônias desses camarões faziam tanto barulho que atrapalhavam o sonar dos submarinos. E agora, o número um. O bicho mais resistente que existe.",
     dict(sufixo=" °C")),
)

CENAS += item(1, "TARDÍGRADO", "sobreviveu ao espaço", ((120, 190, 130), (40, 90, 60)),
    (ta.g_espaco, "Número um: o tardígrado, o urso-d'água. Ele mede meio milímetro, tem oito patinhas, e pode estar agora no musgo do seu quintal."),
    [("MODO BARRIL", ta.c_barril, ((220, 170, 90), (110, 70, 30)),
      "Quando falta água, ele seca quase inteiro, encolhe as patas e vira um barrilzinho, quase sem metabolismo. Nesse modo, ele espera o tempo que for."),
     ("GELO E FOGO", ta.c_extremos, ((100, 80, 160), (30, 20, 60)),
      "Assim, ele aguenta frio perto do zero absoluto, calor de cento e cinquenta graus por alguns minutos, e pressões maiores que as do fundo do oceano."),
     ("TESTE NO ESPAÇO", ta.c_foguete, NOITE,
      "Em dois mil e sete, cientistas deixaram tardígrados dez dias expostos ao espaço, do lado de fora de uma cápsula. Muitos voltaram vivos e ainda tiveram filhotes."),
     ],
    (30, "ANOS CONGELADO E VOLTOU", ta.c_musgo,
     "E no Japão, tardígrados congelados por mais de trinta anos voltaram à vida e se reproduziram. Por isso ele é o bicho mais insano do planeta.",
     dict()),
)

CENAS += [
    dict(tipo="cta", titulo="QUAL É O MAIS INSANO?", subtitulo="Comenta o seu top 1", capitulo="Fechamento",
         fala="E aí, qual desses é o mais insano pra você? Comenta o seu top um. Se inscreve no canal, que tem curiosidade nova todo dia, e domingo que vem tem outro vídeo longo da Maia!"),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--folha":
        ini = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        tot, durs = folha(CENAS, sys.argv[2], inicio=ini, n=12)
        print("total", round(tot, 1), "s", durs)
    else:
        tot, caps = render_longo(CENAS, sys.argv[1] if len(sys.argv) > 1 else "longo.mp4")
        print("duração:", round(tot, 1))
        for s, txt in caps:
            print(f"{int(s // 60):02d}:{int(s % 60):02d} {txt}")
