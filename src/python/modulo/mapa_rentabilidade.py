import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

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
        

        #fig = px.density_heatmap(tabelao,
        #                labels = dict(x="Meses", y="Ano", color="Rendimento mensal"),
        #                x=['jan','fev','mar','jun','jul','ago','set','out','nov','dez'])
