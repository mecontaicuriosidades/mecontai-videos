"""Idiomas dos canais da MAIA.

O português é o idioma original dos roteiros. Para os outros idiomas, cada tema tem
`traducoes/<tema>.json` no formato {"es": {"texto em pt": "texto traduzido", ...}, "en": {...}}.
`tr()` é chamado pelo motor e pelos desenhos em todo texto mostrado ou falado.
Uso: veja traduzir.py.
"""
import json, os

CONF = {
    "pt": dict(voz="xMGbstDe7gGBMg3DqxOc", marca="Me ContAI", milhar=".", decimal=",", tz="America/Sao_Paulo"),
    # Vozes gratuitas Kokoro (escolhidas em 12/11/2026): "kokoro:<voz>@<idioma>"
    # (alternativas ElevenLabs já na biblioteca: ES Lizy br0MPoLVxuslVxf61qHn, EN Tessa BAdH0bMfq6VleQGLXj38,
    #  FR Agathe SptHT9PQ49isQvxFm28t)
    "es": dict(voz="kokoro:ef_dora@es", marca="Cuéntame MAIA", milhar=".", decimal=",", tz="America/Mexico_City", velocidade=1.05),
    "en": dict(voz="kokoro:af_heart@en-us", marca="MAIA", milhar=",", decimal=".", tz="America/New_York"),
    "fr": dict(voz="kokoro:ff_siwis@fr-fr", marca="MAIA", milhar=" ", decimal=",", tz="Europe/Paris"),
}

LANG = "pt"
TAB = {}
FALTANDO = []


def ativar(lang, tema=None, pasta=None):
    """Liga o idioma `lang` e carrega a tabela de tradução do tema."""
    global LANG, TAB
    LANG, TAB = lang, {}
    FALTANDO.clear()
    if lang != "pt" and tema:
        pasta = pasta or os.path.join(os.path.dirname(os.path.abspath(__file__)), "traducoes")
        arq = os.path.join(pasta, f"{tema}.json")
        if os.path.exists(arq):
            TAB = json.load(open(arq, encoding="utf-8")).get(lang, {})


def conf():
    return CONF[LANG]


def tr(s):
    """Traduz um texto (mantém espaços nas pontas, ex.: sufixo ' DIAS')."""
    if LANG == "pt" or not isinstance(s, str):
        return s
    core = s.strip()
    if sum(ch.isalpha() for ch in core) <= 2:  # números, unidades (m, °C, km)
        return s
    if core in TAB:
        return s.replace(core, TAB[core])
    if core not in FALTANDO:
        FALTANDO.append(core)
    return s


def num(n, casas=0):
    """Formata número no padrão do idioma (milhar e decimal)."""
    c = CONF[LANG]
    s = f"{n:,.{casas}f}"  # 1,234.5
    return s.replace(",", "\0").replace(".", c["decimal"]).replace("\0", c["milhar"])
