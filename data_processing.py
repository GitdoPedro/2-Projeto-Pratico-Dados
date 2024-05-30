import pandas as pd
import googlemaps
from dotenv import load_dotenv
import os
from aux_functions import *

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API do Google Maps do arquivo .env
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Configurar o cliente do Google Maps API
gmaps = googlemaps.Client(key=api_key)

# URL do arquivo CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR-5K52INxakIsALdfReM9k1GZ5b4c89HhetS2Drd9H1ZvR4Ww6jrMUZc9WZafaytNSgfXVfGP9q3z2/pub?gid=10034961&single=true&output=csv'

# Importação da base de dados
alugueis = pd.read_csv(url)

# Adiciona uma nova coluna com os CEP's obtidos
alugueis['cep'] = alugueis.apply(lambda row: obter_cep(row['address'],row['district'], 'São Paulo'), axis=1)
cep_nao_encontrado_contagem = (alugueis['cep'] == 'CEP não encontrado').sum()

# Limpando registros com áreas desprezíveis
alugueis_area_desprezivel = alugueis['area'] < 10
registros_excluidos = alugueis[alugueis_area_desprezivel]
alugueis = alugueis[alugueis['area'] >= 10]

# Substituindo CEP's não encontrados por CEP's do mesmo bairro 
cep_nao_encontrado_contagem = (alugueis['cep'] == 'CEP não encontrado').sum()
alugueis['cep'] = alugueis.apply(lambda linha: substituir_cep_nao_encontrado(linha, alugueis), axis=1)

# Deletando registros sem CEP
registros_excluidos = pd.concat([registros_excluidos, alugueis[alugueis['cep'] == 'CEP não encontrado']])
alugueis = alugueis[alugueis['cep'] != 'CEP não encontrado']

# Ajustando CEP's incompletos
alugueis['cep'] = alugueis['cep'].astype(str).apply(ajustar_cep)

# Criar a nova coluna 'Zona'
alugueis['Zona'] = alugueis['cep'].apply(classificar_zona)

# Salvar o dataframe atualizado em um arquivo CSV
alugueis.to_csv('alugueis_dados_tratados.csv', index=False)
