# Importa as Libs
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta
import warnings

# Desativa os warnings chatos que vão aparecer no log devido ao método random_integers
warnings.filterwarnings(action="ignore")

# Cria o dataframe com números randomicos, já nomeando as colunas. No exemplo abaixo, eu crio 9 colunas com 10mil linhas cada que vão receber valores randômicos de 1 a 20
# Estou fazendo isso só para entenderem melhor como funciona os atributos do np.random.random_integers(), pq na verdade eu só precisava fazer isso para a variável agencia e DT_PROPOSTA
df = pd.DataFrame(np.random.random_integers(20, size=(10000, 9)),
    columns=['agencia', 'decisao', 'canal', 'DT_PROPOSTA', 'regra', 'publico', 'segmento', 'cheque_especial', 'qtd'])

# Adiciona novos números randômicos para cada variável, dependendo do que queremos para cada uma delas
df['decisao'] = np.random.random_integers(3, size=(10000, 1))
df['canal'] = np.random.random_integers(6, size=(10000, 1))
df['regra'] = np.random.random_integers(10, size=(10000, 1))
df['publico'] = np.random.random_integers(2, size=(10000, 1))
df['segmento'] = np.random.random_integers(4, size=(10000, 1))
df['cheque_especial'] = np.random.random_integers(2, size=(10000, 1))
df['qtd'] = np.random.random_integers(7000, size=(10000, 1))

# Substitui os números criados anteriormente pelas respostas desejadas em cada variável
df['decisao'] = df['decisao'].astype(str)
# df['decisao'] = df['decisao'].replace(['1', '2', '3'],['APROVAR', 'NEGAR', 'DERIVAR'])

df['canal'] = df['canal'].astype(str)
df['canal'] = df['canal'].replace(['1', '2', '3', '4', '5', '6'],['Internet Banking PF', 'Internet Banking PJ', 'Mobile Banking PF', 'Mobile Banking PJ', 'Agência Física PF', 'Agência Física PJ'])

df['regra'] = df['regra'].astype(str)
df['regra'] = df['regra'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'])

df['segmento'] = df['segmento'].astype(str)
df['segmento'] = df['segmento'].replace(['1', '2', '3', '4'],['Altíssima Renda', 'Alta Renda', 'Média Renda', 'Massificado'])

df['DT_PROPOSTA'] = df['DT_PROPOSTA'].astype(str)
df['DT_PROPOSTA'] = df['DT_PROPOSTA'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],['01/09/2021', '02/09/2021', '03/09/2021', '04/09/2021', '05/09/2021', '06/09/2021', '07/09/2021', '08/09/2021', '09/09/2021', '10/09/2021', '11/09/2021', '12/09/2021', '13/09/2021', '14/09/2021', '15/09/2021', '16/09/2021', '17/09/2021', '18/09/2021', '19/09/2021', '20/09/2021'])
df['DT_PROPOSTA'] = pd.to_datetime(df['DT_PROPOSTA'], format='%d/%m/%Y')

df['cheque_especial'] = df['cheque_especial'].astype(str)
df['cheque_especial'] = df['cheque_especial'].replace(['1', '2'],['TRUE', 'FALSE'])

# Aqui eu crio outras variáveis utilizando outro método randômico, só pra mostrart outra forma que  também funciona
df['Score_A'] = np.random.random_integers(550, size=(10000, 1))
df['Score_B'] = np.random.random_integers(110, size=(10000, 1))

# Aqui eu começo a criar variáveis com condições
df['TimeOut_A'] = np.where(df['Score_A'] > 500, 'TimeOut', 'Consulta OK')
df['TimeOut_B'] = np.where(df['Score_B'] > 100, 'TimeOut', 'Consulta OK')

keep_canal = ['Internet Banking PF', 'Mobile Banking PF', 'Agência Física PF']

df['publico'] = df['canal'].isin(keep_canal)
df['publico'] = np.where(df['publico'] == True, "PF", "PJ")

keep_neg = ['01', '02', '03', '04', '05']
keep_drv = ['06', '07', '08', '09']

df['decisao'] = np.where(df['regra'].isin(keep_neg), 'NEGAR', df['decisao'])
df['decisao'] = np.where(df['regra'].isin(keep_drv), 'DERIVAR', df['decisao'])
df['decisao'] = np.where(df['regra'] == '10', 'APROVAR', df['decisao'])

df['Limite'] = np.where(df['decisao'] == 'APROVAR', np.random.randint(500, 2000, size=(10000)) * df['qtd'], 0)

df['lat'] = np.random.randn(10000) / 5 + -23.53
df['lon'] = np.random.randn(10000) / 5 + -46.62

# print(df)

# E por fim, aqui eu crio um csv em uma pasta local
df.to_csv(r'C:\Users\vitor\Documents\GitHub\streamlit-dashboard\base_dataset2.csv')
print('Rodei')