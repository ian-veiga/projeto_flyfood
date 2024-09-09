import numpy as np

# Carregar o arquivo .npz
dados = np.load('dicionario-de-resultados.npz',allow_pickle=True)


# Acessar um array específico pelo nome da chave
for chave in dados.files:
    print(f"Conteúdo de {chave}:")
    print(dados[chave])