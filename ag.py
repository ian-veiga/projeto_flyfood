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

def pop_inicial(map, pop_size):
    population = []
    permutation = list(permutations(map))
    for i in range(pop_size):
        population.append(permutation[i])
    return population


x = pop_inicial(delivery_points, 24 )
print (x)