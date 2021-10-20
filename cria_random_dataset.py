import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")

df = pd.DataFrame(np.random.random_integers(20, size=(1000, 16)),
    columns=['agencia', 'decisão', 'biocatch_IsBot', 'biocatch_IsMalware', 'biocatchIsRat', 'canal', 'DT_REF',
             'device_diebold_tag', 'público', 'segmento', 'tipoContaBeneficiario', 'tipoContaPagador',
             'tipoTransacao',
             'transacao_Login', 'Transacao_pix', 'qtd'])


df['decisão'] = np.random.random_integers(3, size=(1000, 1))
df['biocatch_IsBot'] = np.random.random_integers(2, size=(1000, 1))
df['biocatch_IsMalware'] = np.random.random_integers(2, size=(1000, 1))
df['biocatchIsRat'] = np.random.random_integers(2, size=(1000, 1))
df['canal'] = np.random.random_integers(7, size=(1000, 1))
df['device_diebold_tag'] = np.random.random_integers(10, size=(1000, 1))
df['público'] = np.random.random_integers(3, size=(1000, 1))
df['segmento'] = np.random.random_integers(20, size=(1000, 1))
df['tipoContaBeneficiario'] = np.random.random_integers(4, size=(1000, 1))
df['tipoContaPagador'] = np.random.random_integers(4, size=(1000, 1))
df['tipoTransacao'] = np.random.random_integers(10, size=(1000, 1))
df['transacao_Login'] = np.random.random_integers(2, size=(1000, 1))
df['Transacao_pix'] = np.random.random_integers(2, size=(1000, 1))
df['qtd'] = np.random.random_integers(7000, size=(1000, 1))


df['decisão'] = df['decisão'].astype(str)
df['decisão'] = df['decisão'].replace(['1', '2', '3'],['APROVAR', 'NEGAR', 'DERIVAR'])

df['biocatch_IsBot'] = df['biocatch_IsBot'].astype(str)
df['biocatch_IsBot'] = df['biocatch_IsBot'].replace(['1', '2'],['TRUE', 'FALSE'])

df['biocatch_IsMalware'] = df['biocatch_IsMalware'].astype(str)
df['biocatch_IsMalware'] = df['biocatch_IsMalware'].replace(['1', '2'],['TRUE', 'FALSE'])

df['biocatchIsRat'] = df['biocatchIsRat'].astype(str)
df['biocatchIsRat'] = df['biocatchIsRat'].replace(['1', '2'],['TRUE', 'FALSE'])

df['canal'] = df['canal'].astype(str)
df['canal'] = df['canal'].replace(['1', '2', '3', '4', '5', '6', '7'],['BCD', 'CDF', 'IBF', 'IBJ', 'MBF', 'MBJ', 'SPD'])

df['device_diebold_tag'] = df['device_diebold_tag'].astype(str)
df['device_diebold_tag'] = df['device_diebold_tag'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],['app_acesso_remoto', 'sfr_acesso_nrecomendado', 'sfr_acesso_nrecomendado_v2', 'sfr_device_recorrente_sup30d', 'sfr_device_recorrente_ate30d', 'sfr_device_recorrente_sup60d', 'sfr_device_recorrente_ate60d', 'sfr_device_recorrente_sup90d', 'sfr_device_recorrente_ate90d', 'novo_usuario'])

df['público'] = df['público'].astype(str)
df['público'] = df['público'].replace(['1', '2', '3'],['ND', 'PF', 'PJ'])

df['tipoContaBeneficiario'] = df['tipoContaBeneficiario'].astype(str)
df['tipoContaBeneficiario'] = df['tipoContaBeneficiario'].replace(['1', '2', '3', '4'],['Conta Corrente', 'Conta Poupança', 'Conta Salário', 'Conta Pagamento'])

df['tipoContaPagador'] = df['tipoContaPagador'].astype(str)
df['tipoContaPagador'] = df['tipoContaPagador'].replace(['1', '2', '3', '4'],['Conta Corrente', 'Conta Poupança', 'Conta Salário', 'Conta Pagamento'])

df['tipoTransacao'] = df['tipoTransacao'].astype(str)
df['tipoTransacao'] = df['tipoTransacao'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],['CONSULTA_SENHA_TSC', 'HABILITA_SENHA', 'LOGIN_SUCESSO', 'OPBK_CONSENT_APROV', 'PAGAMENTO', 'PAGAMENTO_DDA', 'PAGAMENTO_DDA', 'PIX_CONFIRMAR_PORTAB', 'PIX_INCLUIR_CHAVE', 'PIX_PAGAMENTO_CELULAR'])

df['DT_REF'] = df['DT_REF'].astype(str)
df['DT_REF'] = df['DT_REF'].replace(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],['01/09/2021', '02/09/2021', '03/09/2021', '04/09/2021', '05/09/2021', '06/09/2021', '07/09/2021', '08/09/2021', '09/09/2021', '10/09/2021', '11/09/2021', '12/09/2021', '13/09/2021', '14/09/2021', '15/09/2021', '16/09/2021', '17/09/2021', '18/09/2021', '19/09/2021', '20/09/2021'])
df['DT_REF'] = pd.to_datetime(df['DT_REF'], format='%d/%m/%Y')

df['transacao_Login'] = df['transacao_Login'].astype(str)
df['transacao_Login'] = df['transacao_Login'].replace(['1', '2'],['TRUE', 'FALSE'])

df['Transacao_pix'] = df['Transacao_pix'].astype(str)
df['Transacao_pix'] = df['Transacao_pix'].replace(['1', '2'],['TRUE', 'FALSE'])

print(df)

df.to_csv(r'C:\Users\vitor\Desktop\Python Programs\Dash com Streamlit\Lib\base_dataset2.csv')