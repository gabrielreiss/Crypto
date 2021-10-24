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

warnings.filterwarnings('ignore')

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
    options_tickers = st.sidebar.multiselect("Lista de Criptos", list_of_tickers, default=['BTC', 'ETH', 'LTC', 'XRP', 'DASH', 'SC'])

    #filtra os dados pelo período
    periodo = st.sidebar.slider('Período analisado', 1, 5, value = 1)
    start = dt.datetime.now() - dt.timedelta(days=(365 * periodo))
    end = dt.datetime.now()
    data_filtrada = filtra_banco(options_tickers, start, end, conn)

    #Apresenta um resumo em tabelas
    st.header('Histórico de preços em Dólar')
    st.dataframe(data_filtrada)

    #Imprime gráfico dos valores
    for ticket in options_tickers:
        fig = plt.figure(figsize=(12,5))
        ax = sns.lineplot(data=data_filtrada, x=data_filtrada.index, y= ticket,palette="tab10", linewidth=2.5)
        ax.set(xlabel='Ano', ylabel='USD')
        plt.title(f'Evolução do {ticket}')
        st.pyplot(fig)

    st.header('Variação Diária')
    data_rend_diarios = data_filtrada[options_tickers].pct_change()
    data_rend_diarios = data_rend_diarios[1:]
    st.dataframe(data_rend_diarios)

    #matriz de correlação
    st.subheader('Matriz de Correlação')
    correlação = data_rend_diarios.corr(method = "pearson")
    fig = plt.figure(figsize=(12,5))
    sns.heatmap(correlação, annot=True, cmap="coolwarm")
    st.pyplot(fig)


    st.header('Retorno Acumulado')
    retorno_acumulado = (1 + data_rend_diarios).cumprod()
    retorno_acumulado = retorno_acumulado[1:]
    st.dataframe(retorno_acumulado)


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

