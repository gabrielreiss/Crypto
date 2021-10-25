import streamlit as st
#import warnings
#import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import datetime as dt
import numpy as np
#import sqlalchemy
#from src.python.modulo.filtra_banco import filtra_banco
#import plotly.express as px

#warnings.filterwarnings('ignore')
#
#BASE_DIR = os.path.abspath(".")
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#DATA_DIR = os.path.join(BASE_DIR,'data')
#SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
#PYTHON_DIR = os.path.join(BASE_DIR, 'src', 'python')

#str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'data.db') + '?check_same_thread=False'
#engine = sqlalchemy.create_engine(str_conn)
#conn = engine.connect()

#options_tickers = ['BTC', 'ETH', 'LTC', 'XRP', 'DASH', 'SC']
#periodo = 5
#start = dt.datetime.now() - dt.timedelta(days=(365 * periodo))
#end = dt.datetime.now()
#data_filtrada = filtra_banco(options_tickers, start, end, conn)


def heatmap_var_mensal(data_filtrada, options_tickers):
    for moeda in options_tickers:
        data_rend_diarios = data_filtrada[[moeda]].pct_change()
        data_rend_diarios = data_rend_diarios[1:]
        data_rend_diarios['ano'] = list(data_rend_diarios.index.year)
        data_rend_diarios['mes'] = list(data_rend_diarios.index.month)

        #aqui deveria ser cumprod mas como não deu certo, coloquei soma, fica um valor aproximado
        tabelao = pd.pivot_table(   data_rend_diarios, 
                                    values = moeda, 
                                    #aggfunc = 'cumprod',
                                    aggfunc = np.sum,
                                    index = 'ano',
                                    columns= 'mes',
                                    fill_value = 0
                                    
                                    )

        fig, ax = plt.subplots()
        fig = plt.figure(figsize=(12,5))
        ax = sns.heatmap(tabelao, cmap="viridis", annot = True).set_title(f'Variação mensal - {moeda}')
        st.pyplot(fig)

        #cmap="RdBu"
        #coolwarm
        #viridis
        

        #fig = px.imshow(tabelao,
        #                labels = dict(x="Meses", y="Ano", color="Rendimento mensal"),
        #                x=['jan','fev','mar','jun','jul','ago','set','out','nov','dez'])
        #st.plotly_chart(fig)