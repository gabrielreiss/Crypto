import streamlit as st
import warnings
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyfolio as pf
import datetime as dt

warnings.filterwarnings('ignore')

BASE_DIR = os.path.abspath(".")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
PYTHON_DIR = os.path.join(BASE_DIR, 'src', 'python')

os.environ['TZ'] = 'UTC'

#carrega os dados
data = pd.read_csv(os.path.join(DATA_DIR, 'data.csv'),index_col="Date", infer_datetime_format= True, parse_dates=['Date'])
print(data)

#main function
if __name__ == "__main__":
    st.title('Análise de Criptomoedas')

    #filtra os dados por criptos
    st.sidebar.title("Parâmetros")
    list_of_tickers = list(data.columns)
    options_tickers = st.sidebar.multiselect("Lista de Criptos", list_of_tickers, default=['BTC', 'ETH', 'LTC', 'XRP', 'DASH', 'SC'])

    #filtra os dados pelo período
    periodo = st.sidebar.slider('Período analisado', 1, 5, value = 5)
    start = dt.datetime.now() - dt.timedelta(days=(365 * periodo))
    end = dt.datetime.now()
    data_filtrada = data[options_tickers].loc[start:end]

    os.environ['TZ'] = 'UTC'

    #Apresenta um resumo em tabelas
    st.header('Histórico de preços em Dólar')
    st.dataframe(data_filtrada)

    #Imprime gráfico dos valores
    for ticket in options_tickers:
        plt.figure(figsize=(12,5))
        ax = sns.lineplot(data=data_filtrada, x=data_filtrada.index, y= ticket,palette="tab10", linewidth=2.5)
        ax.set(xlabel='Ano', ylabel='USD')
        plt.title(f'Evolução do {ticket}')
        st.pyplot()

    st.header('Variação Diária')
    data_rend_diarios = data_filtrada[options_tickers].pct_change()
    data_rend_diarios = data_rend_diarios[1:]
    st.dataframe(data_rend_diarios)

    st.header('Retorno Acumulado')
    retorno_acumulado = (1 + data_rend_diarios).cumprod()
    retorno_acumulado = retorno_acumulado[1:]
    st.dataframe(retorno_acumulado)

