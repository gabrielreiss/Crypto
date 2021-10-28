import streamlit as st
import pandas as pd
import datetime as dt
from src.python.modulo.filtra_banco import filtra_banco

def MA_table(options_tickers, conn, preco_atual):
    options_tickers_uni = options_tickers
    options_tickers = [options_tickers]
    #necessário baixar os dados novamente
    periodo = 1
    start = dt.datetime.now() - dt.timedelta(days=(365 * periodo))
    end = dt.datetime.now()
    data_filtrada = filtra_banco(options_tickers, start, end, conn)

    def MA(number):
        MA_5 = data_filtrada.rolling(window=number).mean()
        MA_5 = MA_5.iloc[[-1]]
        MA_5 = MA_5.transpose()
        MA_5 = MA_5.iloc[:,0].values.tolist()
        return MA_5

    def acao(number):
        media = MA(number)[0]

        list = []
        if preco_atual < media:
            #venda
            list = [MA(number)[0], 'Venda']
        else:
            #compra
            list = [MA(number)[0], 'Compra']
        return list

    df = pd.DataFrame(
        data = {
            'MA(5)': acao(5),
            'MA(10)': acao(10),
            'MA(20)': acao(20),
            'MA(50)': acao(50),
            'MA(100)': acao(100),
            'MA(200)': acao(200)
        }, 
        index=[options_tickers_uni, 'Ação']
    )

    df = df.transpose()
    return df

