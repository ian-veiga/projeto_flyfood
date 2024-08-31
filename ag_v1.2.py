from itertools import permutations
import random, math

def dic_posicoes(dado: str) -> dict[int, tuple[float, float]]:
    """Criar um dicinario das posicoes """
    try:
        with open(dado, 'r') as arquivo:
            linhas = [linha.split() for linha in arquivo.readlines()[6:58]]
    except FileNotFoundError:
        print("Erro: arquivo 'documento.txt' não encontrado.")
        exit()
    
    coordenadas = {}
    for linha in linhas:
        coordenadas[int(linha[0])] = (float(linha[1]), float(linha[2]))

    return coordenadas

def pop_inicial(tam_pop: int, semente: int | float | bytes | bytearray):
    caminhos = []
    random.seed(semente)

    for _ in range(tam_pop):
        caminho_rand = list(range(1, 52))
        random.shuffle(caminho_rand)
        caminhos.append(caminho_rand)
    
    return caminhos

def aptidao_individuo(caminho: list[int], coordenadas: dict[int, tuple[float, float]]) -> float:
    distancia = 0
    i = 0
    while i < (len(caminho) - 1):
        atual = caminho[i]
        seguinte = caminho[i + 1]
        delta_x = (coordenadas[atual][0] - coordenadas[seguinte][0])
        delta_y = (coordenadas[atual][1] - coordenadas[seguinte][1])
        distancia += math.sqrt((delta_x ** 2) + (delta_y ** 2))
        i += 1
    
    distancia = round(distancia, 4)

    return distancia

def aptidao(populacao: list[list[int]], coordenadas) -> list[float]:
    lista_aptidao: list[float] = [0] * len(populacao)
    for i, ind in enumerate(populacao):
        lista_aptidao[i] = aptidao_individuo(ind, coordenadas)
    return lista_aptidao

def main():
    dado = 'berlin52.tsp'
    coordenadas = dic_posicoes(dado)
    print(coordenadas)
    print()
    qtd_pop = 10000
    semente = 15
    popul = pop_inicial(qtd_pop, semente)
    print(min(aptidao(popul, coordenadas)))
    

main()

