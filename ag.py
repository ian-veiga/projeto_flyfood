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

def Pop_inicial(points, pop_size):
    population = []
    permutation =list(permutations(points))
    for i in range(pop_size):
        population.append(list(permutation[i]))
    return population

def Fitness(rota, coordinates):
   rota.insert(0, "R")  # Insere "R" no início
   rota.append("R")     # Adiciona "R" no final
   distance = 0
   for i in range(len(rota) - 1):
      l_cost = abs(coordinates[rota[i]][0] - coordinates[rota[i+1]][0])
      c_cost = abs(coordinates[rota[i]][1] - coordinates[rota[i+1]][1])
      distance += l_cost + c_cost
   return distance




x = Pop_inicial(delivery_points, 24)
print(x)
y = Fitness(x[22], coordinates)
print(y)