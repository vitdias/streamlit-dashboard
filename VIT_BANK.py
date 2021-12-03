import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Dash - VIT BANK",
                   page_icon=":bar_chart",  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

if 'login_state' not in st.session_state:
    st.session_state['login_state'] = 0

st.sidebar.image('VIT_BANK_bg_transp.png')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def main():

    @st.cache
    def get_dataframe():
        df = pd.read_csv(r'C:\Users\vitor\Documents\GitHub\streamlit-dashboard\base_dataset2.csv', index_col=0)
        df['DT_PROPOSTA'] = pd.to_datetime(df['DT_PROPOSTA'])

        return df
    df = get_dataframe()

    start_dt = datetime(2021, 9, 1, 0, 0, 0, 0)
    end_dt = datetime(2021, 9, 20, 0, 0, 0, 0)

    #  ---- SIDEBAR ----

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
        "Selecione decisao do motor",
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
                                        value=[0, 550])
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

    df_map = df_filtered[['lat', 'lon']]

    # ---- MAINPAGE ----
    st.markdown("<h1 style='text-align: center; color: white;'>Originação de cartões VIT BANK</h1>",
                unsafe_allow_html=True)
    st.markdown("\n")
    st.markdown("\n")

    # --- TOP KPI's ----
    qtd_tsc = int(df_filtered["qtd"].sum())
    med_tsc = int(df_filtered.groupby(
        by=["DT_PROPOSTA"]).sum()[["qtd"]].mean())
    tx_aprov = "{0:.2f}".format(float(
        df_filtered.loc[df['decisao'] == 'APROVAR', 'qtd'].sum() / df_filtered['qtd'].sum()) * 100)
    qtd_tsc_pf = df_filtered.loc[df['publico'] == 'PF', 'qtd'].sum()
    qtd_tsc_pj = df_filtered.loc[df['publico'] == 'PJ', 'qtd'].sum()
    exposicao = int(df_filtered['Limite'].sum())

    left_column, center_column, right_column = st.columns(3)
    with left_column:
        # st.subheader("Quantidade de transações")
        # st.info(f"{qtd_tsc:,}")
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Quantidade de propostas</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: white;'>{qtd_tsc:,}</h3>", unsafe_allow_html=True)

    with center_column:
        # st.subheader("Média diária de transações")
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Média diária de propostas</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: white;'>{med_tsc:,}</h3>", unsafe_allow_html=True)
        # st.subheader(f"{med_tsc:,}")

    with right_column:
        # st.subheader("Taxa de Negativa")
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Taxa de Aprovação</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: white;'>{tx_aprov}%</h3>", unsafe_allow_html=True)
        # st.subheader(f"{tx_negat}%")

    st.markdown('---')
    left_column2, center_column2, right_column2 = st.columns(3)

    with left_column2:
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Propostas Pessoa Física</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: white;'>{qtd_tsc_pf:,}</h3>", unsafe_allow_html=True)

    with center_column2:
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Exposição Financeira</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: white;'>{exposicao:,}</h3>", unsafe_allow_html=True)

    with right_column2:
        st.markdown(
            f"<h4 style='text-align: center; color: white;'>Propostas Pessoa Jurídica</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: white;'>{qtd_tsc_pj:,}</h3>", unsafe_allow_html=True)

    st.markdown('---')

    # ---- CREATE GRAPHS ----
    g1_left_column, g1_right_column = st.columns(2)
    st.markdown('---')
    g2_left_column, g2_right_column = st.columns(2)

    # Propostas por canal
    qtd_por_canal = (
        df_filtered.groupby(by=["canal"]).sum()[["qtd"]].sort_values(by="qtd")
        )

    qtd_por_agencia = (
        df_filtered.groupby(by=["agencia"]).sum()[["qtd"]].sort_values(by="qtd")
    )

    qtd_por_dia = df_filtered.groupby(by=["DT_PROPOSTA", "decisao"]).sum()[["qtd"]].reset_index()
    qtd_por_dia['percentage'] = df_filtered.groupby(["DT_PROPOSTA", "decisao"]).size().groupby(level=0).apply(
        lambda x: 100 * x / float(x.sum())).values

    qtd_por_decisao = df_filtered.groupby(by=["decisao"]).sum()[["qtd"]]

    segmento_canal = df_filtered.groupby(by=["canal", "segmento"]).sum()[["qtd"]].sort_values(by="canal").reset_index()
    decisao_canal = df_filtered.groupby(by=["canal", "decisao"]).sum()[["qtd"]].sort_values(by="canal").reset_index()
    decisao_canal['percentage'] = df_filtered.groupby(['canal', 'decisao']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values

    qtd_Score_A = df_filtered.groupby(by=["Score_A"]).sum()[["qtd"]].sort_values(by="Score_A")
    qtd_Score_B = df_filtered.groupby(by=["Score_B"]).sum()[["qtd"]].sort_values(by="Score_B")
    qtd_TMO_A = df_filtered.groupby(by=["DT_PROPOSTA", "TimeOut_A"]).sum()[["qtd"]].reset_index()
    qtd_TMO_A['percentage'] = df_filtered.groupby(['DT_PROPOSTA', 'TimeOut_A']).size().groupby(level=0).apply(
        lambda x: 100 * x / float(x.sum())).values

    qtd_TMO_B = df_filtered.groupby(by=["DT_PROPOSTA", "TimeOut_B"]).sum()[["qtd"]].reset_index()
    qtd_TMO_B['percentage'] = df_filtered.groupby(['DT_PROPOSTA', 'TimeOut_B']).size().groupby(level=0).apply(
        lambda x: 100 * x / float(x.sum())).values

    #Cores
    azul_bg = '#17214E'
    azul_sb = "#141D44"
    dourado = "#C2AB6B"
    azul_medio = "#2A3D91"
    azul_iceberg = "#79A9D1"
    brink_pink = "#FF4D80"

    # Monocromático com dourado principal
    dourado_claro = '#CCC4AD'
    dourado_principal = '#C2AB6B'
    dourado_escuro = '#8F7E4F'
    dourado_darker = '#424038'
    dourado_darkest = '#423A24'

    # Cores guanabara
    azulzao_base = '#2222FF'
    tiffany = '#01EBEC'
    azul_escuro = '#1C0051'
    tiffany_claro = '#D7F8F9'
    
    # Cores padrão
    verde_padrao = "#00CC96"
    roxo_padrao  = "#AB63FA"
    azul_padrao  = "#636EFA"
    

    cor_aprovado = azul_sb
    cor_negado = brink_pink
    cor_derivado = dourado_principal

    # Gráfico Donut
    fig_qtd_por_decisao = px.pie(
        qtd_por_decisao,
        values="qtd",
        names=qtd_por_decisao.index,
        title = "<b>Quantidade por decisao</b>",
        hole=.3,
        color_discrete_sequence=[cor_derivado, cor_negado, cor_aprovado]
    )

    fig_qtd_por_decisao.update_layout(
        title_x =0.5
    )

    # Gráfico Barras diário
    fig_qtd_por_dia = px.bar(
        qtd_por_dia,
        x='DT_PROPOSTA',
        y=['qtd'],
        orientation='v',
        title="<b>Quantidade por dia </b>",
        color='decisao',
        #     barmode='stack',
        text=qtd_por_dia['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)),
        color_discrete_map=
        {
            "APROVAR": cor_aprovado,
            "DERIVAR": cor_derivado,
            "NEGAR": cor_negado
        }
    )

    fig_qtd_por_dia.add_hline(y=med_tsc, line_width=4, line_dash='dash', line_color=tiffany, annotation_text='Média diária', annotation_position='bottom left')

    fig_qtd_por_dia.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x =0.5,
    )

    # Gráfico Tipo segmento por canal
    fig_segmento_canal = px.bar(
        segmento_canal,
        x='canal',
        y='qtd',
        title = "<b>Quantidade segmento x canal</b>",
        color='segmento',
        barmode='group'
    )

    fig_segmento_canal.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x =0.5
    )

    # Gráfico decisao, transação por canal
    fig_decisao_canal = px.bar(
        decisao_canal,
        x='canal',
        y='qtd',
        title = "<b>Quantidade de decisao x canal</b>",
        color='decisao',
        #barmode='stack',
        text=decisao_canal['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)),
        color_discrete_map=
        {
            "APROVAR": cor_aprovado,
            "DERIVAR": cor_derivado,
            "NEGAR": cor_negado
        }
    )

    fig_decisao_canal.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x =0.5
    )

    # Gráfico Barras Score_B
    fig_qtd_Score_B = px.bar(
        qtd_Score_B,
        x=qtd_Score_B.index,
        y='qtd',
        orientation='v',
        title = "<b> Volume Score B </b>",
        color_discrete_sequence=[cor_derivado]
    )

    fig_qtd_Score_B.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Gráfico Barras Score_A
    fig_qtd_Score_A = px.bar(
        qtd_Score_A,
        x=qtd_Score_A.index,
        y='qtd',
        orientation='v',
        title = "<b>Volume Score A </b>",
        color_discrete_sequence=[cor_derivado]
    )

    fig_qtd_Score_A.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Gráfico Barras TMO Score_A
    fig_qtd_TMO_A = px.bar(
        qtd_TMO_A,
        x='DT_PROPOSTA',
        y='qtd',
        orientation='v',
        title = "<b> Volume de Time Out Score A x Dia</b>",
        color='TimeOut_A',
        barmode='stack',
        color_discrete_map=
        {
            'TimeOut': cor_negado,
            'Consulta OK': cor_aprovado
        }
    )

    fig_qtd_TMO_A.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Gráfico Barras TMO Score_B
    fig_qtd_TMO_B = px.bar(
        qtd_TMO_B,
        x='DT_PROPOSTA',
        y='qtd',
        orientation='v',
        title = "<b> Volume de Time Out Score B x Dia</b>",
        color='TimeOut_B',
        barmode='stack',
        color_discrete_map=
        {
            'TimeOut': cor_negado,
            'Consulta OK': cor_aprovado
        }
    )

    fig_qtd_TMO_B.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # # Cria estilo do botão radio na horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center}</style>', unsafe_allow_html=True)

    g1_left_column.plotly_chart(fig_qtd_por_decisao, use_container_width=True)
    g1_right_column.plotly_chart(fig_qtd_por_dia, use_container_width=True)
    g1_right_column.radio('', ['Quantidade de transações', 'Valor Financeiro (R$)'])

    g2_left_column.plotly_chart(fig_decisao_canal, use_container_width=True)
    g2_right_column.plotly_chart(fig_segmento_canal, use_container_width=True)

    with st.expander("Dados de Time Out Score A"):
        st.plotly_chart(fig_qtd_Score_A, use_container_width=True)
        st.plotly_chart(fig_qtd_TMO_A, use_container_width=True)

    with st.expander("Dados de Time Out Score B"):
        st.plotly_chart(fig_qtd_Score_B, use_container_width=True)
        st.plotly_chart(fig_qtd_TMO_B, use_container_width=True)

    st.map(df_map)

    if checkb:
        st.dataframe(df_filtered)


if st.session_state.login_state == 0:
    try:
        pw = st.sidebar.text_input("Insira a senha", type='password')
        if pw != '' and pw != '1234':
            st.sidebar.warning('Senha incorreta')
        if pw == '1234':
            st.session_state.login_state = 1
            del pw
    except:
        pass

if st.session_state.login_state == 1:
    main()
