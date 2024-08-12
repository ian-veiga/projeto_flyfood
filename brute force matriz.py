#listas e importações
from itertools import permutations
coordinates  = {}
delivery_points =[]

#abrindo arquivo que contem a matriz e separando numero de linhas e colunas
file = open('input_matriz.txt','r')
nlinhas , ncolunas  = file.readline().split()
lines = file.read().splitlines()


#separando elementos da matriz e pegando sua posicao
for l in range(int(nlinhas)):
    line = lines[l].split()
    for j in line:
        if j != '0':
            coordinates[j] = (l, line.index(j))
            delivery_points.append(j)       


delivery_points.remove('R')
menor_custo = float('inf')


#permutacao distancias iniciando e terminando em r
for k in list(permutations(delivery_points)):
    custo_atual = 0
    
    k = list(k)
    k.append('R')
    k.insert(0, 'R')
#calculando todas as distancias possiveis
    for i in range(len(k) - 1):
        y_cost = abs(coordinates[k[i]][0] - coordinates[k[i+1]][0])
        x_cost = abs(coordinates[k[i]][1] - coordinates[k[i+1]][1])
        custo_atual += x_cost + y_cost    
#separando menor custo
    if custo_atual < menor_custo:
        menor_custo = custo_atual
        route = k
print ("rota:",''.join(route[1:-1]))
print(f"custo:{menor_custo}")

