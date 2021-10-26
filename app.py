import streamlit as st
import warnings
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import numpy as np
import sqlalchemy
from src.python.modulo.markowitz import fronteira_eficiente
from src.python.modulo.filtra_banco import filtra_banco
from src.python.modulo.lista_ticker import lista_ticker
from src.python.modulo.time_series_plot import time_series_plot
from src.python.modulo.download_data import download_csv
from src.python.modulo.mapa_rentabilidade import heatmap_var_mensal
from src.python.modulo.CAPM import CAPM
import plotly.express as px

warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:, .4f}'.format

BASE_DIR = os.path.abspath(".")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
PYTHON_DIR = os.path.join(BASE_DIR, 'src', 'python')

str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'data.db') + '?check_same_thread=False'
engine = sqlalchemy.create_engine(str_conn)
conn = engine.connect()

#main function
if __name__ == "__main__":
    st.title('Análise de Criptomoedas')

    #filtra os dados por criptos
    st.sidebar.title("Parâmetros")
    list_of_tickers = lista_ticker(conn)
    options_tickers = st.sidebar.multiselect("Lista de Criptos", list_of_tickers, default=['ETH', 'ADA'])

    #filtra os dados pelo período
    periodo = st.sidebar.slider('Período analisado', 1, 5, value = 1)
    start = dt.datetime.now() - dt.timedelta(days=(365 * periodo))
    end = dt.datetime.now()
    data_filtrada = filtra_banco(options_tickers, start, end, conn)

    #Definir taxa selic
    selic = st.sidebar.number_input('Insere o valor da taxa selic atual', value = 6.25)
    ref_mercado = st.sidebar.multiselect("Crypto de referência", list_of_tickers, default=['BTC'])
    data_ref_mercado = filtra_banco(ref_mercado, start, end, conn)

    #Apresenta um resumo em tabelas
    st.header('Histórico de preços em Dólar')
    download_csv(data_filtrada)
    st.dataframe(data_filtrada)

    for ticket in options_tickers:
        time_series_plot(data_filtrada, ticket, f'Evolução do {ticket}')
        #st.experimental_show(fig)

    st.header('Variação Diária')
    data_rend_diarios = data_filtrada[options_tickers].pct_change()
    data_rend_diarios = data_rend_diarios[1:]
    download_csv(data_rend_diarios)
    st.dataframe(data_rend_diarios)

    #matriz de correlação
    st.subheader('Matriz de Correlação')
    correlação = data_rend_diarios.corr(method = "pearson")
    mask = np.zeros_like(correlação, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    fig = plt.figure(figsize=(12,5))
    sns.heatmap(correlação, annot=True, cmap="coolwarm", fmt = '.2f', mask=mask, center = 0, square=True, linewidths=.5)
    st.pyplot(fig)

    st.header('Retorno Acumulado')
    retorno_acumulado = (1 + data_rend_diarios).cumprod()
    retorno_acumulado = retorno_acumulado[1:]
    download_csv(retorno_acumulado)
    st.dataframe(retorno_acumulado)

    #Mapa de calor da rentabilidade mensal
    st.header('Mapa de calor da rentabilidade mensal')
    heatmap_var_mensal(data_filtrada, options_tickers)

    st.title("Fronteira Eficiente de Markowitz")
    sharpe_maximo, pesos, ret_arr, vol_arr, sharpe_arr, max_sr_ret, max_sr_vol = fronteira_eficiente(data_rend_diarios)

    fig = plt.figure(figsize=(12,8))
    plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.scatter(max_sr_vol, max_sr_ret,c='red', s=50) # red dot
    st.pyplot(fig)

    st.table(pesos)
    st.write(f'Retorno da carteira: {max_sr_ret:.2f}')
    st.write(f'Volatilidade da carteira: {max_sr_vol:.2f}')
    st.write(f'O sharp da carteira: {sharpe_maximo:.2f}')

    st.header("CAPM")
    st.text_area(label = "Explicação", value = "O modelo CAPM (Capital Asset Pricing Model) é utilizado para estimar o retorno esperado teórico de um ativo, ou melhor, a taxa de retorno esperada (custo de capital) que é apropriada para um determinado ativo. Se o ativo possui um beta maior do que 1, significando que ele possui uma maior sensibilidade às variações do mercado. De acordo com o CAPM, se o alfa de qualquer ativo ou fundo for maior que zero, significa que obteve um retorno acima do esperado. Do contrário, o ativo teve uma performance abaixo das expectativas.")
    tabela_capm = CAPM(data_filtrada, options_tickers, data_ref_mercado, ref_mercado, selic)
    st.dataframe(tabela_capm)