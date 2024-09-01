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

def pop_inicial(tam_pop: int, semente: int | float | bytes | bytearray) -> list[list[int]]:
    """"""
    caminhos = []
    random.seed(semente)

    for _ in range(tam_pop):
        caminho_rand = list(range(1, 52))
        random.shuffle(caminho_rand)
        caminhos.append(caminho_rand)
    
    return caminhos

def aptidao_individuo(caminho: list[int], coordenadas: dict[int, tuple[float, float]]) -> float:
    """Calculando a aptidao (distancia percorrida) de cada individuo"""
    distancia = 0
    
    i = 0
    while i < (len(caminho) - 1):
        atual = caminho[i]
        seguinte = caminho[i + 1]
        delta_x = (coordenadas[atual][0] - coordenadas[seguinte][0])
        delta_y = (coordenadas[atual][1] - coordenadas[seguinte][1])
        distancia += math.sqrt((delta_x ** 2) + (delta_y ** 2))
        i += 1
    
    return round(distancia, 4)

def aptidao(populacao: list[list[int]], coordenadas) -> list[float]:
    """calculando a aptidao de uma populacao"""
    aptidao_populacao: list[float] = [0] * len(populacao)

    for i, ind in enumerate(populacao):
        aptidao_populacao[i] = aptidao_individuo(ind, coordenadas)

    return aptidao_populacao


def pmx(pai1: list[int], pai2: list[int]) -> tuple[list[int], list[int]]:
    """Partially Mapped Crossover (PMX) adaptado para o TSP"""
    tamanho = len(pai1)
    
    while True:
        inicio = random.randint(0, tamanho - 1)
        final = random.randint(0, tamanho - 1)
        if inicio != final:
            break
    
    if inicio > final :
        inicio, final = final, inicio
    
    filho1, filho2 = [None] * tamanho, [None] * tamanho
    
    filho1[inicio:final + 1] = pai1[inicio:final + 1]
    filho2[inicio:final + 1] = pai2[inicio:final + 1]
    
    def mapear(pai: list[int], filho: list[int]):
        for i in range(inicio, final + 1):
            if pai[i] not in filho:
                j = i
                while inicio <= j <= final:
                    j = pai.index(filho[j])
                filho[j] = pai[i]

    mapear(pai2, filho1)
    mapear(pai1, filho2)
    
    for i in range(tamanho):
        if filho1[i] is None:
            filho1[i] = pai2[i]
        if filho2[i] is None:
            filho2[i] = pai1[i]

    return filho1, filho2


def cruzamento(populacao: list[list[int]], taxa_cruzamento: float) -> list[list[int]]:
    """Gerar a nova população apos o cruzamento"""
    nova_populacao = []
    
    for i in range(0, len(populacao), 2):
        pai1 = populacao[i]
        pai2 = populacao[i + 1]
        if random.random() < taxa_cruzamento:
            filho1, filho2 = pmx(pai1, pai2)
        else:
            filho1, filho2 = pai1, pai2
        nova_populacao.append(filho1)
        nova_populacao.append(filho2)
    
    return nova_populacao

def mutacao_individuo(filho: list[int], taxa_mutacao: float) -> str:
    """mutação de um individuo"""
    filho_mutado = filho.copy()
    
    if random.random() <= taxa_mutacao:
        while True:
            pos1 = random.randint(0, len(filho_mutado) - 1)
            pos2 = random.randint(0, len(filho_mutado) - 1)
            if pos1 != pos2:
                break
        if pos1 > pos2 :
            pos1, pos2 = pos2, pos1
        
        filho_mutado = filho_mutado[:pos1] + filho_mutado[pos1:pos2 + 1][::-1] + filho_mutado[pos2 + 1:]
        return filho_mutado

    return filho_mutado

def mutacao(filhos: list[str], taxa_mutacao: float) -> list[str]:
    """Mutação de todos os filhos"""
    for i, ind in enumerate(filhos):
        filhos[i] = mutacao_individuo(ind, taxa_mutacao)
    return filhos


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

