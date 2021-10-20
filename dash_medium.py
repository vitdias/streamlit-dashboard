import pandas as pd #pip install pandas openpyxl
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Dash - Prevenção a Fraudes",
                   page_icon=":bar_chart",  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

if 'login_state' not in st.session_state:
    st.session_state['login_state'] = 0

st.sidebar.image('safra_logo_removebg.png')

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
        df_imp = pd.read_csv(r"C:\Users\vitor\Desktop\Python Programs\Dash com Streamlit\Lib\base_dataset2.csv")
        df = df_imp.iloc[:, 3:]
        df['DT_REF'] = pd.to_datetime(df['DT_REF'])
        df['ScoreHeartBeat'] = np.random.random_integers(999, size=(1000, 1))
        df['ScoreBiocatch'] = np.random.random_integers(999, size=(1000, 1))
        df['TimeOut_HB'] = np.where(df['ScoreHeartBeat'] > 95, 'TimeOut', 'Consulta OK')
        df['TimeOut_BC'] = np.where(df['ScoreBiocatch'] > 900, 'TimeOut', 'Consulta OK')

        keep = ['PIX_PAGAMENTO_CELULAR', 'PAGAMENTO', 'PAGAMENTO_DDA']

        df['Transacao_pix'] = np.where(df['tipoTransacao'] == 'PIX_PAGAMENTO_CELULAR', True, False)
        df['transacao_login'] = np.where(df['tipoTransacao'] == 'LOGIN_SUCESSO', True, False)

        df['MOD_TSC'] = df['tipoTransacao'].isin(keep)
        df['MOD_TSC'] = np.where(df['MOD_TSC'] == True, "Financeira", "Ñ Financeira")

        df['valorFinal'] = np.where(df['Transacao_pix'] == True, np.random.randint(500, 2000, size=(1000)) * df['qtd'], 0)


        df['lat'] = np.random.randn(1000) / 5 + -23.53
        df['lon'] = np.random.randn(1000) / 5 + -46.62

        return df
    df = get_dataframe()

    start_dt = datetime(2021, 9, 1, 0, 0, 0, 0)
    end_dt = datetime(2021, 9, 20, 0, 0, 0, 0)

    #  ---- SIDEBAR ----

    # st.sidebar.image('safra_logo_removebg.png')

    #button_reset = st.sidebar.button('Resetar Filtros')

    st.sidebar.header('Período')
    from_date = st.sidebar.date_input('De:', start_dt)
    to_date = st.sidebar.date_input('Para:', end_dt)

    st.sidebar.markdown("---")
    multi_mod_tsc = st.sidebar.multiselect(
        "Selecione a modalidade da transação",
        options=df['MOD_TSC'].unique(),
        default=df['MOD_TSC'].unique()
    )
    st.sidebar.markdown("\n")

    multi_agencia = st.sidebar.multiselect(
        "Selecione as agências",
        options=df['agencia'].unique(),
        default=df['agencia'].unique()
    )
    st.sidebar.markdown("\n")

    multi_decisao = st.sidebar.multiselect(
        "Selecione decisão do OSA",
        options=df['decisão'].unique(),
        default=df['decisão'].unique()
    )
    st.sidebar.markdown("\n")

    multi_canal = st.sidebar.multiselect(
        "Selecione o canal",
        options=df['canal'].unique(),
        default=df['canal'].unique()
    )
    st.sidebar.markdown("\n")

    multi_device_tag = st.sidebar.multiselect(
        "Selecione a device tag",
        options=df['device_diebold_tag'].unique(),
        default=df['device_diebold_tag'].unique()
    )
    st.sidebar.markdown("\n")

    multi_publico = st.sidebar.multiselect(
        "Selecione o publico",
        options=df['público'].unique(),
        default=df['público'].unique()
    )
    st.sidebar.markdown("\n")

    multi_tipoTransacao = st.sidebar.multiselect(
        "Selecione o tipo de transação",
        options=df['tipoTransacao'].unique(),
        default=df['tipoTransacao'].unique()
    )
    st.sidebar.markdown("\n")

    selectionScoreHeartBeat = st.sidebar.slider("Selecione o range de ScoreHeartBeat",
        value=[0,100])
    st.sidebar.markdown("\n")

    selectionScoreBiocatch = st.sidebar.slider("Selecione o range de ScoreBiocatch ",
        value=[0,500])
    st.sidebar.markdown("\n")

    multi_Transacao_pix = st.sidebar.multiselect(
        "Selecione se a transação é PIX",
        options=df['Transacao_pix'].unique(),
        default=df['Transacao_pix'].unique()
    )
    st.sidebar.markdown("\n")

    checkb = st.sidebar.checkbox("Carregar dataframe")

    df_filtered = df.query(
        "agencia == @multi_agencia & decisão == @multi_decisao & canal == @multi_canal & device_diebold_tag == @multi_device_tag & público ==@multi_publico & tipoTransacao == @multi_tipoTransacao & Transacao_pix == @multi_Transacao_pix & (DT_REF >= @from_date & DT_REF <= @to_date) & (ScoreHeartBeat >= @selectionScoreHeartBeat[0] & ScoreHeartBeat <= @selectionScoreHeartBeat[1]) & (ScoreBiocatch >= @selectionScoreBiocatch[0] & ScoreBiocatch >= @selectionScoreBiocatch[1]) & MOD_TSC == @multi_mod_tsc"
    )

    df_map = df_filtered[['lat', 'lon']]

    # if button_reset:
    #     pass

    # ---- MAINPAGE ----
    # st.title('Dashboard OSA - Transacional')
    st.markdown("<h1 style='text-align: center; color: white;'>Dashboard OSA - Transacional</h1>", unsafe_allow_html=True)
    st.markdown("\n")
    st.markdown("\n")
    # st.header('colocar tsc financeiras ou não financeiras aqui')

    # --- TOP KPI's ----
    qtd_tsc = int(df_filtered["qtd"].sum())
    med_tsc = int(df_filtered.groupby(by=["DT_REF"]).sum()[["qtd"]].mean())
    tx_negat = "{0:.2f}".format(float(df_filtered.loc[df['decisão'] == 'NEGAR', 'qtd'].sum() / df_filtered['qtd'].sum()) * 100)
    qtd_tsc_fin = df_filtered.loc[df['MOD_TSC'] == 'Financeira', 'qtd'].sum()
    qtd_tsc_nfin = df_filtered.loc[df['MOD_TSC'] == 'Ñ Financeira', 'qtd'].sum()
    valorTransacionado = int(df_filtered['valorFinal'].sum())

    left_column, center_column, right_column = st.columns(3)
    with left_column:
        # st.subheader("Quantidade de transações")
        # st.info(f"{qtd_tsc:,}")
        st.markdown(f"<h4 style='text-align: center; color: white;'>Quantidade de transações</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white;'>{qtd_tsc:,}</h3>", unsafe_allow_html=True)

    with center_column:
        # st.subheader("Média diária de transações")
        st.markdown(f"<h4 style='text-align: center; color: white;'>Média diária de transações</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white;'>{med_tsc:,}</h3>", unsafe_allow_html=True)
        # st.subheader(f"{med_tsc:,}")

    with right_column:
        # st.subheader("Taxa de Negativa")
        st.markdown(f"<h4 style='text-align: center; color: white;'>Taxa de Negativa</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white;'>{tx_negat}%</h3>", unsafe_allow_html=True)
        # st.subheader(f"{tx_negat}%")

    st.markdown('---')
    left_column2, center_column2, right_column2 = st.columns(3)

    with left_column2:
        st.markdown(f"<h4 style='text-align: center; color: white;'>Tsc Financeiras</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white;'>{qtd_tsc_fin:,}</h3>", unsafe_allow_html=True)

    with center_column2:
        st.markdown(f"<h4 style='text-align: center; color: white;'>Valor Transacionado</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white;'>{valorTransacionado:,}</h3>", unsafe_allow_html=True)

    with right_column2:
        st.markdown(f"<h4 style='text-align: center; color: white;'>Tsc ñ Financeiras</h4>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white;'>{qtd_tsc_nfin:,}</h3>", unsafe_allow_html=True)


    st.markdown('---')

    # ---- CREATE GRAPHS ----
    g1_left_column, g1_right_column = st.columns(2)
    st.markdown('---')
    g2_left_column, g2_right_column = st.columns(2)

    # Transações por canal
    qtd_por_canal = (
        df_filtered.groupby(by=["canal"]).sum()[["qtd"]].sort_values(by="qtd")
        )

    qtd_por_agencia = (
        df_filtered.groupby(by=["agencia"]).sum()[["qtd"]].sort_values(by="qtd")
    )

    qtd_por_dia = df_filtered.groupby(by=["DT_REF", "decisão"]).sum()[["qtd"]].reset_index()
    qtd_por_dia['percentage'] = df_filtered.groupby(["DT_REF", "decisão"]).size().groupby(level=0).apply(
        lambda x: 100 * x / float(x.sum())).values

    qtd_por_decisao = df_filtered.groupby(by=["decisão"]).sum()[["qtd"]]

    tpTsc_canal = df_filtered.groupby(by=["canal", "tipoTransacao"]).sum()[["qtd"]].sort_values(by="canal").reset_index()
    decisao_canal = df_filtered.groupby(by=["canal", "decisão"]).sum()[["qtd"]].sort_values(by="canal").reset_index()
    decisao_canal['percentage'] = df_filtered.groupby(['canal', 'decisão']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values

    qtd_ScoreHeartBeat = df_filtered.groupby(by=["ScoreHeartBeat"]).sum()[["qtd"]].sort_values(by="ScoreHeartBeat")
    qtd_ScoreBiocatch = df_filtered.groupby(by=["ScoreBiocatch"]).sum()[["qtd"]].sort_values(by="ScoreBiocatch")
    qtd_TMOHB = df_filtered.groupby(by=["DT_REF", "TimeOut_HB"]).sum()[["qtd"]].reset_index()
    qtd_TMOHB['percentage'] = df_filtered.groupby(['DT_REF', 'TimeOut_HB']).size().groupby(level=0).apply(
        lambda x: 100 * x / float(x.sum())).values

    qtd_TMOBC = df_filtered.groupby(by=["DT_REF", "TimeOut_BC"]).sum()[["qtd"]].reset_index()
    qtd_TMOBC['percentage'] = df_filtered.groupby(['DT_REF', 'TimeOut_BC']).size().groupby(level=0).apply(
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

    cor_aprovado = azul_sb
    cor_negado = brink_pink
    cor_derivado = dourado_principal

    # Gráfico Donut
    fig_qtd_por_decisao = px.pie(
        qtd_por_decisao,
        values="qtd",
        names=qtd_por_decisao.index,
        title = "<b>Quantidade por decisão</b>",
        hole=.3,
        color_discrete_sequence=[cor_derivado, cor_negado, cor_aprovado]
    )

    fig_qtd_por_decisao.update_layout(
        title_x =0.5
    )

    # Gráfico Barras diário
    fig_qtd_por_dia = px.bar(
        qtd_por_dia,
        x='DT_REF',
        y=['qtd'],
        orientation='v',
        title="<b>Quantidade por dia </b>",
        color='decisão',
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

    # Gráfico Tipo transação por canal
    fig_tpTsc_canal = px.bar(
        tpTsc_canal,
        x='canal',
        y='qtd',
        title = "<b>Quantidade de Tipo de transação x canal</b>",
        color='tipoTransacao',
        barmode='group'
    )

    fig_tpTsc_canal.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x =0.5
    )

    # Gráfico decisão, transação por canal
    fig_decisao_canal = px.bar(
        decisao_canal,
        x='canal',
        y='qtd',
        title = "<b>Quantidade de decisão x canal</b>",
        color='decisão',
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

    # Gráfico Barras ScoreBiocatch
    fig_qtd_ScoreBiocatch = px.bar(
        qtd_ScoreBiocatch,
        x=qtd_ScoreBiocatch.index,
        y='qtd',
        orientation='v',
        title = "<b> Volume Score Biocatch </b>",
        color_discrete_sequence=[cor_derivado]
    )

    fig_qtd_ScoreBiocatch.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Gráfico Barras ScoreHeartBeat
    fig_qtd_ScoreHeartBeat = px.bar(
        qtd_ScoreHeartBeat,
        x=qtd_ScoreHeartBeat.index,
        y='qtd',
        orientation='v',
        title = "<b>Volume Score Heartbeat </b>",
        color_discrete_sequence=[cor_derivado]
    )

    fig_qtd_ScoreHeartBeat.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Gráfico Barras TMO ScoreHeartBeat
    fig_qtd_TMOHB = px.bar(
        qtd_TMOHB,
        x='DT_REF',
        y='qtd',
        orientation='v',
        title = "<b> Volume de Time Out HeartBeat x Dia</b>",
        color='TimeOut_HB',
        barmode='stack',
        color_discrete_map=
        {
            'TimeOut': cor_negado,
            'Consulta OK': cor_aprovado
        }
    )

    fig_qtd_TMOHB.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Gráfico Barras TMO ScoreBiocatch
    fig_qtd_TMOBC = px.bar(
        qtd_TMOBC,
        x='DT_REF',
        y='qtd',
        orientation='v',
        title = "<b> Volume de Time Out Biocatch x Dia</b>",
        color='TimeOut_BC',
        barmode='stack',
        color_discrete_map=
        {
            'TimeOut': cor_negado,
            'Consulta OK': cor_aprovado
        }
    )

    fig_qtd_TMOBC.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False)),
        title_x=0.5
    )

    # Cria estilo do botão radio na horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center}</style>', unsafe_allow_html=True)

    g1_left_column.plotly_chart(fig_qtd_por_decisao, use_container_width=True)
    g1_right_column.plotly_chart(fig_qtd_por_dia, use_container_width=True)
    g1_right_column.radio('', ['Quantidade de transações', 'Valor Financeiro (R$)'])

    g2_left_column.plotly_chart(fig_decisao_canal, use_container_width=True)
    g2_right_column.plotly_chart(fig_tpTsc_canal, use_container_width=True)

    with st.expander("Dados de Time Out HeartBeat"):
        st.plotly_chart(fig_qtd_ScoreHeartBeat, use_container_width=True)
        st.plotly_chart(fig_qtd_TMOHB, use_container_width=True)

    with st.expander("Dados de Time Out Biocatch"):
        st.plotly_chart(fig_qtd_ScoreBiocatch, use_container_width=True)
        st.plotly_chart(fig_qtd_TMOBC, use_container_width=True)

    st.map(df_map)

    if checkb:
        st.dataframe(df_filtered)



if st.session_state.login_state == 0:
    try:
        # st.sidebar.image('safra_logo_removebg.png')
        pw = st.sidebar.text_input("Insira a senha", type='password')
        if pw != '' and pw != 'safra258':
            st.sidebar.warning('Senha incorreta')
        if pw == 'safra258':
            st.session_state.login_state = 1
    except:
        pass

if st.session_state.login_state == 1:
    main()




