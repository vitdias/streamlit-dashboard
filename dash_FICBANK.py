import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

df = pd.read_csv(r'C:\Users\vitor\Documents\GitHub\streamlit-dashboard\base_dataset2.csv', index_col=0)
df['DT_PROPOSTA'] = pd.to_datetime(df['DT_PROPOSTA'])

start_dt = datetime(2021, 9, 1, 0, 0, 0, 0)
end_dt = datetime(2021, 9, 20, 0, 0, 0, 0)

# ---- SIDEBAR ----
st.sidebar.image('VIT_BANK_bg_transp.png')

st.sidebar.header('Período')
from_date = st.sidebar.date_input('De:', start_dt)
to_date = st.sidebar.date_input('Para:', end_dt)

st.sidebar.markdown("---")
multi_agencia = st.sidebar.multiselect(
    "Selecione as agências",
    options=df['agencia'].unique(),
    default=df['agencia'].unique()
)
st.sidebar.markdown("\n")

multi_decisao = st.sidebar.multiselect(
    "Selecione decisão do motor",
    options=df['decisao'].unique(),
    default=df['decisao'].unique()
)
st.sidebar.markdown("\n")

multi_canal = st.sidebar.multiselect(
    "Selecione o canal",
    options=df['canal'].unique(),
    default=df['canal'].unique()
)
st.sidebar.markdown("\n")

multi_regra = st.sidebar.multiselect(
    "Selecione a regra",
    options=df['regra'].unique(),
    default=df['regra'].unique()
)
st.sidebar.markdown("\n")

multi_publico = st.sidebar.multiselect(
    "Selecione o público",
    options=df['publico'].unique(),
    default=df['publico'].unique()
)
st.sidebar.markdown("\n")

multi_segmento = st.sidebar.multiselect(
    "Selecione o segmento",
    options=df['segmento'].unique(),
    default=df['segmento'].unique()
)
st.sidebar.markdown("\n")

selectionScoreA = st.sidebar.slider("Selecione o range do Score A",
                                    value=[0, 999])
st.sidebar.markdown("\n")

selectionScoreB = st.sidebar.slider("Selecione o range do Score B",
                                    value=[0, 100])
st.sidebar.markdown("\n")

multi_cheque_especial = st.sidebar.multiselect(
    "Selecione se a proposta tem aceite de cheque especial",
    options=df['cheque_especial'].unique(),
    default=df['cheque_especial'].unique()
)
st.sidebar.markdown("\n")

checkb = st.sidebar.checkbox("Carregar dataframe")

df_filtered = df.query(
"agencia == @multi_agencia & decisao == @multi_decisao & canal == @multi_canal & regra == @multi_regra & publico ==@multi_publico & segmento == @multi_segmento & cheque_especial == @multi_cheque_especial & (DT_PROPOSTA >= @from_date & DT_PROPOSTA <= @to_date) & (Score_A >= @selectionScoreA[0] & Score_A <= @selectionScoreA[1]) & (Score_B >= @selectionScoreB[0] & Score_B <= @selectionScoreB[1])"
)

# ---- MAIN ----
if checkb == True:
    st.dataframe(df_filtered)
