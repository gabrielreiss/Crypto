import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#Imprime gráfico dos valores
def series_plot(data_filtrada, options_tickers):
    for ticket in options_tickers:
        fig = plt.figure(figsize=(12,5))
        ax = sns.lineplot(data=data_filtrada, x=data_filtrada.index, y= ticket,palette="tab10", linewidth=2.5)
        ax.set(xlabel='Ano', ylabel='USD')
        plt.title(f'Evolução do {ticket}')
        st.pyplot(fig)