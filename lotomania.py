import requests
import random

TODOS_NUMEROS = list(range(0, 100))
PRIMOS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
FIBONACCI = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

def obter_ultimos_resultados_lotomania(quantidade=100):
    url_ultimo = 'https://loteriascaixa-api.herokuapp.com/api/lotomania/latest'
    try:
        resposta = requests.get(url_ultimo)
        resposta.raise_for_status()
        ultimo_concurso = resposta.json()['concurso']
    except requests.exceptions.RequestException:
        return []

    resultados = []
    for numero in range(ultimo_concurso, ultimo_concurso - quantidade, -1):
        url = f'https://loteriascaixa-api.herokuapp.com/api/lotomania/{numero}'
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            dados = resposta.json()
            dezenas = sorted([int(d) for d in dados.get("dezenas", [])])
            if len(dezenas) == 20:
                resultados.append({"concurso": numero, "dezenas": dezenas})
        except requests.exceptions.RequestException:
            continue

    return resultados

def validar_dicas(dezenas):
    pares = len([d for d in dezenas if d % 2 == 0])
    if not (6 <= pares <= 14): return False
    primos = len([d for d in dezenas if d in PRIMOS])
    if not (2 <= primos <= 8): return False
    fib = len([d for d in dezenas if d in FIBONACCI])
    if not (0 <= fib <= 4): return False
    soma = sum(dezenas)
    if not (785 <= soma <= 1203): return False
    return True

def gerar_20_dezenas_validas(excluir=[]):
    while True:
        pool = [d for d in TODOS_NUMEROS if d not in excluir]
        if len(pool) < 20: return []
        dezenas = sorted(random.sample(pool, 20))
        if validar_dicas(dezenas):
            return dezenas

def gerar_cartao_completo(excluir=[]):
    base_20 = gerar_20_dezenas_validas(excluir)
    restante = list(set(TODOS_NUMEROS) - set(base_20))
    complemento = random.sample(restante, 30)
    cartela = sorted(base_20 + complemento)
    return cartela

def gerar_cartelas(qtd=10, excluir=[]):
    return [gerar_cartao_completo(excluir) for _ in range(qtd)]

def conferir_jogos(jogos, resultados):
    conferencias = []
    for jogo in jogos:
        conferencias_por_concurso = []
        for resultado in resultados:
            acertos = len(set(jogo).intersection(set(resultado["dezenas"])))
            conferencias_por_concurso.append({
                "concurso": resultado["concurso"],
                "acertos": acertos
            })
        conferencias.append({
            "jogo": jogo,
            "resultados": conferencias_por_concurso
        })
    return conferencias

def salvar_jogos_em_txt(jogos, arquivo="jogos_lotomania.txt"):
    with open(arquivo, "w") as f:
        for idx, jogo in enumerate(jogos, 1):
            f.write(f"Jogo {idx:03}: " + ", ".join(f"{d:02}" for d in jogo) + "\n")