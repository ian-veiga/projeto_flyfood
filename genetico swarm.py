import numpy as np
import random
from math import sqrt

try:
    with open('berlin52.tsp', 'r') as arquivo:
     linhas = [linha.split() for linha in arquivo.readlines()[6:58]]
except FileNotFoundError:
        print("Erro: arquivo 'documento.txt' não encontrado.")
        exit()

coordenadas = {}

for linha in linhas:
    coordenadas[int(linha[0])] = (float(linha[1]), float(linha[2]))

# Função para calcular a distância euclidiana
def calcular_distancia(cidade1, cidade2):

    delta_x = ((cidade1[0] - cidade2[0]))
    delta_y = ((cidade1[1] - cidade2[1]))
    distancia = sqrt((delta_x ** 2) + (delta_y ** 2))
    
    return round(distancia, 4)

# Função para calcular o custo da rota
def calcular_custo(rota, distancias):
    custo = 0
    for i in range(len(rota) - 1):
        custo += distancias[rota[i]][rota[i + 1]]
    
    return custo

# Geração inicial de partículas
def gerar_particulas(n_cidades, n_particulas):
    return [random.sample(range(n_cidades), n_cidades) for _ in range(n_particulas)]

# Função de busca local (2-opt)
def busca_local_2opt(rota, distancias):
    melhor = rota[:]
    melhor_custo = calcular_custo(melhor, distancias)
    for i in range(1, len(rota) - 2):
        for j in range(i + 1, len(rota)):
            nova_rota = rota[:i] + rota[i:j][::-1] + rota[j:]
            novo_custo = calcular_custo(nova_rota, distancias)
            if novo_custo < melhor_custo:
                melhor = nova_rota
                melhor_custo = novo_custo
    return melhor

def encontrar_indice_minimo(lista):

    min_valor = lista[0]
    min_indice = 0
    for i, valor in enumerate(lista):
        if valor < min_valor:
            min_valor = valor
            min_indice = i
    return min_indice

def rotacionar_lista(lista, indice_rotacao):

    nova_lista = lista.copy()
    for i in range(len(lista)):
        nova_lista[(i + indice_rotacao) % len(lista)] = lista[i]
    return nova_lista

# Função principal PSO com GA e busca local
def PSO_TSP(coordenadas, n_particulas, n_iteracoes):
    n_cidades = len(coordenadas)
    # Inicializando matriz de distâncias
    distancias = [[0] * n_cidades for _ in range(n_cidades)]
    for i in range(n_cidades):
     for j in range(i+1, n_cidades):
        dist = calcular_distancia(coordenadas[i+1], coordenadas[j+1])
        distancias[i][j] = dist
        distancias[j][i] = dist

    # Geração inicial de partículas (soluções possíveis)
    particulas = gerar_particulas(n_cidades, n_particulas)
    velocidades = [np.random.randint(-1, 2, size= n_cidades) for _ in range(n_particulas)]  # Velocidade inicial
    
    # Definindo melhores locais (BLS) e global (BGS)
    BLS = particulas[:]
    BGS = min(particulas, key=lambda p: calcular_custo(p, distancias))
    
    # Gerar números aleatórios para atualizar a velocidade
    for iteracao in range(n_iteracoes):
        random_updates = np.random.randint(-1, 2, size=(n_particulas, n_cidades))
    
    # Atualizar velocidades
    velocidades += random_updates

    # Encontrar o índice do menor valor de velocidade para cada partícula
    min_indices = []
    for i in range(n_particulas):
        min_indices.append(encontrar_indice_minimo(velocidades[i]))

    # Reorganizar as partículas
    for i in range(n_particulas):
        particulas[i] = rotacionar_lista(particulas[i], min_indices[i])

            
    # Encontrar o índice do menor valor de velocidade manualmente
    min_valor = min(velocidades[i].tolist())  # Convertemos o array NumPy para lista
    min_index = velocidades[i].tolist().index(min_valor)  # Encontramos o índice do menor valor
            
     # Reorganizar a partícula com base no índice do menor valor
    particulas[i] = particulas[i][min_index:] + particulas[i][:min_index]
            
    # Aplicando busca local (2-opt)
    particulas[i] = busca_local_2opt(particulas[i], distancias)
            
    # Atualizando melhores locais e global
    if calcular_custo(particulas[i], distancias) < calcular_custo(BLS[i], distancias):
        BLS[i] = particulas[i][:]
    if calcular_custo(BLS[i], distancias) < calcular_custo(BGS, distancias):
                BGS = BLS[i][:]
        
    print(f"Iteração {iteracao + 1}/{n_iteracoes}, Melhor custo: {calcular_custo(BGS, distancias)}")
    
    return BGS, calcular_custo(BGS, distancias)

# Executando o PSO para o problema Berlin52
def main():
    semente = 10
    random.seed(semente)
    coord = coordenadas
    n_particulas = 10000
    n_iteracoes = 1000

    melhor_rota, melhor_custo = PSO_TSP(coord, n_particulas, n_iteracoes)
    print("Melhor rota:", melhor_rota)
    print("Melhor custo:", melhor_custo)

    dict_results = {"semente" : semente,
                    "numero_de_particulas" : n_particulas,
                    "numero_de_iteracoes" : n_iteracoes,
                    "melhor_individuo" : melhor_rota,
                    "melhor_aptidao" : melhor_custo
                    }

    np.savez("dicionario-de-resultados", dict_results)

if __name__ == '__main__':
    main()