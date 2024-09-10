import random
import numpy as np
from typing import Any

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

def shuffler(arr: list[int], n: int) -> list[int]:
    """Embaralha a ordem da lista de pontos"""
    arr = np.array(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr.tolist()

def calcular_distancia(cidade1, cidade2):
    """Função para calcular a distância entre duas cidades"""
    return float(np.sqrt((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2))

def aptidao(caminho, coordenadas):
    """Função de aptidão (custo do caminho)"""
    distancia_total = 0
    for i in range(len(caminho) - 1):
        cidade_atual = coordenadas[caminho[i]]
        proxima_cidade = coordenadas[caminho[i + 1]]
        distancia_total += calcular_distancia(cidade_atual, proxima_cidade)
    return round(distancia_total, 4)

def pmx(pai1, pai2, taxa_de_cruzamento):
    """Partially Mapped Crossover (PMX)"""
    if random.random() >= taxa_de_cruzamento:
        return pai1, pai2
    
    tamanho = len(pai1)
    while True :
        inicio, final = random.randint(0, tamanho - 1), random.randint(0, tamanho - 1)
        if inicio != final:
            break
    
    if inicio > final:
        inicio, final = final, inicio
    
    filho1, filho2 = [None]*tamanho, [None]*tamanho
    filho1[inicio:final + 1] = pai1[inicio:final + 1]
    filho2[inicio:final + 1] = pai2[inicio:final + 1]

    def mapear(pai, filho):
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

def mutacao_2opt(caminho, taxa_mutacao):
    """Função de mutação (2-opt)"""
    filho_mutado = caminho.copy()
    tam = len(caminho)
    if random.random() <= taxa_mutacao:
        while True:
            pos1 = random.randint(0, tam - 1)
            pos2 = random.randint(0, tam - 1)
            if pos1 != pos2:
                break
        if pos1 > pos2 :
            pos1, pos2 = pos2, pos1

        filho_mutado = filho_mutado[:pos1] + filho_mutado[pos1:pos2 + 1][::-1] + filho_mutado[pos2 + 1:]
    return filho_mutado

def encontrar_melhor(particulas, coordenadas):
    """Função para encontrar a melhor partícula"""
    melhor_particula = particulas[0]
    melhor_aptidao = aptidao(melhor_particula, coordenadas)
    for particula in particulas[1:]:
        aptidao_atual = aptidao(particula, coordenadas)
        if aptidao_atual < melhor_aptidao:
            melhor_particula = particula
            melhor_aptidao = aptidao_atual
    return melhor_particula

def calcular_velocidade(velocidade_atual, vmax, dBLS, dBGS, c1=0.7, c2=0.3):
    """Atualiza a velocidade da partícula com base nas distâncias BLS e BGS"""
    r1, r2 = random.random(), random.random()
    velocidade_nova = c1 * r1 * dBLS + c2 * r2 * dBGS
    return valor_minimo([velocidade_nova, velocidade_atual, vmax]) # Adicionar a vel atual

def valor_minimo(lista: list[Any]) -> tuple[Any, int]:
    """Retorna o valor minimo de uma lista"""
    valor_min =int(10000000000000000000000000000)
    for valor in lista:
        if valor < valor_min :
            valor_min = valor
    
    return valor_min

def pso_tsp(coordenadas, num_particulas, num_iteracoes, taxa_de_mutacao, taxa_de_cruzamento, vmax=0.1):
    """PSO para o problema do caixeiro viajante, incluindo PMX e colisão"""
    num_cidades = len(coordenadas)
    cidades = list(range(1, num_cidades))

    particulas = [shuffler(cidades.copy(), len(cidades)) for _ in range(num_particulas)]
    melhores_locais = particulas.copy()
    melhor_global = encontrar_melhor(melhores_locais, coordenadas)

    velocidades = [random.uniform(0, vmax) for _ in range(num_particulas)]
    
    for iteracao in range(num_iteracoes):
        for i in range(num_particulas):
            aptidao_local = aptidao(particulas[i], coordenadas)
            aptidao_BLS = aptidao(melhores_locais[i], coordenadas)
            aptidao_BLG = aptidao(melhor_global, coordenadas)
            dBLS = aptidao_local - aptidao_BLS
            dBGS = aptidao_local - aptidao_BLG
            
            velocidades[i] = calcular_velocidade(velocidades[i], vmax, dBLS, dBGS)

            pai1, pai2 = particulas[i], melhor_global
            nova_particula, _ = pmx(pai1, pai2, taxa_de_cruzamento)
            
            nova_particula = mutacao_2opt(nova_particula, taxa_de_mutacao)
            
            if aptidao(nova_particula, coordenadas) < aptidao_local:
                particulas[i] = nova_particula

            if aptidao_local < aptidao_BLS:
                melhores_locais[i] = particulas[i]
            if aptidao_local < aptidao_BLG:
                melhor_global = particulas[i]
                
        print(f"Iteração {iteracao + 1}, Melhor distância global: {aptidao_BLG}")
    
    return melhor_global, aptidao_BLG

def main():
    semente = 10
    random.seed(semente)
    coord = dic_posicoes('berlin52.tsp')
    n_particulas = 100
    n_iteracoes = 1000
    taxa_mutacao = 0.05
    taxa_cruzamento = 0.75
    melhor_caminho, melhor_distancia = pso_tsp(coord, n_particulas, n_iteracoes, taxa_mutacao, taxa_cruzamento)
    print(f"Melhor caminho encontrado: {melhor_caminho} com distância total de {melhor_distancia}")

if __name__ == '__main__':
    main()
