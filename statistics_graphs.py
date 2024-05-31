import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from aux_functions import formatar_reais

# 50 bairros com mais imóveis 
bairro_contagem = alugueis['district'].value_counts().reset_index()
bairro_contagem.columns = ['bairro', 'qtd_imoveis']
bairro_contagem = bairro_contagem.head(50)
print(bairro_contagem)
plt.figure(figsize=(15, 10))
plt.bar(bairro_contagem['bairro'], bairro_contagem['qtd_imoveis'], color='skyblue')
plt.xlabel('Bairro')
plt.ylabel('Quantidade de Imóveis')
plt.title('50 bairros com mais imóveis')
plt.xticks(rotation=90)
plt.show()

# Média, valor mínimo e máximo de valores (aluguel e total)
estatisticas_globais = alugueis[['rent', 'total']].agg(['min', 'mean', 'max'])
bairro_max_rent = alugueis.loc[alugueis['rent'].idxmax(), 'district']
bairro_min_rent = alugueis.loc[alugueis['rent'].idxmin(), 'district']
estatisticas_globais['bairro'] = [bairro_min_rent,None, bairro_max_rent]
print(estatisticas_globais.applymap(formatar_reais))
plt.figure(figsize=(10, 6))
plt.plot(estatisticas_globais.index, estatisticas_globais['rent'], marker='o', linestyle='-', color='b', label='Aluguel')
for i, txt in enumerate(estatisticas_globais['bairro']):
    if txt is not None:
        plt.annotate(txt, (estatisticas_globais.index[i], estatisticas_globais['rent'][i]), textcoords="offset points", xytext=(0,5), ha='center')
plt.plot(estatisticas_globais.index, estatisticas_globais['total'], marker='x', linestyle='-', color='r', label='Total')
for i, txt in enumerate(estatisticas_globais['bairro']):
    if txt is not None:
        plt.annotate(txt, (estatisticas_globais.index[i], estatisticas_globais['total'][i]), textcoords="offset points", xytext=(0,5), ha='center')
plt.xlabel('Estatísticas')
plt.ylabel('Valor (R$)')
plt.title('Estatísticas de Aluguel e Total')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Média de área por tipo de imóvel
estatisticas_area_por_tipo = alugueis.groupby('type')['area'].agg(['min','mean','max'])
print(estatisticas_area_por_tipo)
estatisticas_area_por_tipo.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Tipo de Imóvel')
plt.ylabel('Área (m²)')
plt.title('Estatísticas de Área por Tipo de Imóvel')
plt.legend(title='Estatísticas')
plt.grid(True)
plt.tight_layout()
plt.show()

# Contagem de imóveis por tipo de imóvel
contagem_por_tipo = alugueis['type'].value_counts()
print(contagem_por_tipo)
plt.figure(figsize=(8, 8))
plt.pie(contagem_por_tipo, labels=contagem_por_tipo.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Tipos de Imóveis')
plt.axis('equal')
plt.show()

# Média, mínimo e máximo por região
estatisticas_por_zona = alugueis.groupby('Zona')[['rent', 'total']].agg(['min', 'mean', 'max'])
print(estatisticas_por_zona.applymap(formatar_reais))
zonas = estatisticas_por_zona.index
mean_rent = estatisticas_por_zona['rent']['mean']
min_rent = estatisticas_por_zona['rent']['min']
max_rent = estatisticas_por_zona['rent']['max']
mean_total = estatisticas_por_zona['total']['mean']
min_total = estatisticas_por_zona['total']['min']
max_total = estatisticas_por_zona['total']['max']
plt.figure(figsize=(12, 8))
plt.plot(zonas, mean_rent, label='Aluguel Médio', marker='o')
plt.plot(zonas, min_rent, label='Aluguel Mínimo', marker='o')
plt.plot(zonas, max_rent, label='Aluguel Máximo', marker='o')
plt.plot(zonas, mean_total, label='Total Médio', marker='x')
plt.plot(zonas, min_total, label='Total Mínimo', marker='x')
plt.plot(zonas, max_total, label='Total Máximo', marker='x')
plt.xlabel('Zona')
plt.ylabel('Valores (R$)')
plt.title('Estatísticas de Aluguel por Região')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Preço (aluguel e total) por metro quadrado de cada região
preco_por_sqm_zona = alugueis.groupby('Zona').apply(
    lambda x: pd.Series({
        'rent_per_sqm': (x['rent'] / x['area']).mean(),
        'total_per_sqm': (x['total'] / x['area']).mean()
    })
)
preco_por_sqm_zona_ordenado = preco_por_sqm_zona.sort_values(by='rent_per_sqm', ascending=False)
print("Preço por Metro Quadrado por Zona:")
print(preco_por_sqm_zona_ordenado.applymap(formatar_reais))
zonas = preco_por_sqm_zona_ordenado.index
rent_per_sqm = preco_por_sqm_zona_ordenado['rent_per_sqm']
total_per_sqm = preco_por_sqm_zona_ordenado['total_per_sqm']
x = np.arange(len(zonas))  # Posições no eixo x
width = 0.35  # Largura das barras
fig, ax = plt.subplots(figsize=(12, 8))
bars1 = ax.bar(x - width/2, rent_per_sqm, width, label='Aluguel por m²', color='lightblue')
bars2 = ax.bar(x + width/2, total_per_sqm, width, label='Total por m²', color='dodgerblue')
ax.set_xlabel('Zona')
ax.set_ylabel('Preço por Metro Quadrado (R$)')
ax.set_title('Preço por Metro Quadrado por Região')
ax.set_xticks(x)
ax.set_xticklabels(zonas)
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
