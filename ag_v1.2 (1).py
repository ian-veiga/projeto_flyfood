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
        caminho_rand = list(range(1, 53))
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
    """calculando as aptidoes de uma populacao"""
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

def mutacao(filhos: list[str], taxa_mutacao: float) -> list[list[int]]:
    """Mutação de todos os filhos"""
    return [
        [int(gene) for gene in mutacao_individuo(filho, taxa_mutacao)] if random.random()<= taxa_mutacao else [int(gene) for gene in filho]
        for filho in filhos

    ]

def elite_individuo(geracao, coordenadas, n_elite):
    melhores_individuos = []
    melhores_aptidao = []
    

    for individuo in geracao:
        aptidao_atual = aptidao_individuo(individuo, coordenadas)
        if len(melhores_individuos) < n_elite:
            melhores_individuos.append(individuo)
            melhores_aptidao.append(aptidao_atual)
        else:
            pior_idx = 0
            for i in range(1, len(melhores_individuos)):
                if melhores_aptidao[i] > melhores_aptidao[pior_idx]:
                    pior_idx = i
            if aptidao_atual < melhores_aptidao[pior_idx]:
                melhores_individuos[pior_idx] = individuo
                melhores_aptidao[pior_idx] = aptidao_atual
    
    return melhores_individuos
def selecao_pais(pop: list[str], apt: list[float], sel_func: callable) -> list[str]:
    """Seleção dos pais"""
    lista_pais: list[str] = [None] * len(pop)
    for i in range(len(pop)):
        idx_selecionado = sel_func(apt)
        lista_pais[i] = pop[idx_selecionado]
    return lista_pais
def torneio(geracao: list[list[int]], coordenadas: dict[int, tuple[float, float]]) -> list[list[int]]:
    """Seleciona sobreviventes usando torneio e elitismo."""
    sobreviventes = []
    pressao_sel = random.uniform(0.01, 0.03)  # Pressão seletiva de 1% a 3%
    n_elite = int(len(geracao) * pressao_sel)
    n_aleat_sobrev = 50 - n_elite
    # Selecionar a elite
    melhores_individuos = elite_individuo(geracao, coordenadas, n_elite)    
    sobreviventes += melhores_individuos 
    # Selecionar os indivíduos restantes via torneio
    for _ in range(n_aleat_sobrev):
        competidores = random.sample(geracao, k=3)  # Seleciona 3 indivíduos aleatórios para o torneio
        melhor = competidores[0]
        melhor_aptidao = aptidao_individuo(melhor, coordenadas)
        for competidor in competidores[1:]:
            aptidao_competidor = aptidao_individuo(competidor, coordenadas)
            if aptidao_competidor < melhor_aptidao:
                melhor = competidor
                melhor_aptidao = aptidao_competidor
        sobreviventes.append(melhor)

    return sobreviventes

def selecao_sobreviventes(
        pop: list[list[int]], 
        apt: list[float], 
        filhos: list[list[int]], 
        apt_filhos: list[float]
) -> tuple[list[list[int]], list[float]]:
    nova_populacao = pop + filhos
    nova_aptidao = apt + apt_filhos
    sobreviventes_indices = list(range(len(pop)))

    for i in range(len(pop), len(nova_populacao)):
        pior_idx = sobreviventes_indices[0] 
        
        for j in sobreviventes_indices[1:]:
            if nova_aptidao[j] > nova_aptidao[pior_idx]:
                pior_idx = j
        
        if nova_aptidao[i] < nova_aptidao[pior_idx]:
            sobreviventes_indices[sobreviventes_indices.index(pior_idx)] = i
    
    return ([nova_populacao[i] for i in sobreviventes_indices],
            [nova_aptidao[i] for i in sobreviventes_indices])

def imprimir_populacao(pop: list[list[int]], apt: list[float], geracao: int) -> None:
    """Imprime cada população e suas aptidoes e também o melhor individuo"""
    #for ind in zip(pop):
        #print(f"genótipo: {ind}, aptidão: {apt_}")
    print(
        f"Melhor solução da geracao {geracao} é {pop[apt.index(min(apt))]} e sua aptidão é {min(apt)}"
    )
    print("*****************************")

def evolucao(
    tam_pop: int,
    semente: int,
    taxa_cruzamento: float,
    taxa_mutacao: float,
    n_geracoes: int,
    torneio_func: callable,
    coordenadas: dict[int, tuple[float, float]]
) -> tuple[list[list[int]], list[float]]:
    """Algoritmo genético"""
    pop = pop_inicial(tam_pop, semente)
    apt = aptidao(pop, coordenadas) 
    melhor_aptidao_global = min(apt)
    melhor_individuo_global = pop[apt.index(melhor_aptidao_global)]
    
    for geracao in range(n_geracoes):
        imprimir_populacao(pop, apt, geracao)
        
        pais = torneio_func(pop, coordenadas)
        
        filhos = cruzamento(pais, taxa_cruzamento)
        
        filhos = mutacao(filhos, taxa_mutacao)
        
        apt_filhos = aptidao(filhos, coordenadas)
        
        pop, apt = selecao_sobreviventes(pop, apt, filhos, apt_filhos)
        melhor_aptidao_geracao = min(apt)
        
        if melhor_aptidao_geracao < melhor_aptidao_global:
            melhor_aptidao_global = melhor_aptidao_geracao
            melhor_individuo_global = pop[apt.index(melhor_aptidao_global)]
     
    
    return pop, apt,melhor_individuo_global,melhor_aptidao_geracao


def main():
    dado = 'berlin52.tsp'
    coordenadas = dic_posicoes(dado)
    semente = 11
    taxa_cruzamento = 0.9
    taxa_mutacao = 0.6
    n_geracoes = 1000
    tam_pop = 251
    torneio_func = torneio
    pop , apt, melhor_individuo_global, melhor_aptidao_global = evolucao(tam_pop, semente, taxa_cruzamento, taxa_mutacao, n_geracoes, torneio_func, coordenadas)
    
    print(
        f"\n\n>>>Melhor solução encontrada é {melhor_individuo_global} com distancia de {(melhor_aptidao_global)}\n\n"
    )
    
if __name__ == "__main__":
    main()

