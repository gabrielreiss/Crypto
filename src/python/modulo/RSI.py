import streamlit as st
import pandas as pd
import datetime as dt
from src.python.modulo.filtra_banco import filtra_banco

def rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi

def ultimo_rsi(df, periods = 14):
    return rsi(df, periods).iloc[[-1]].values.tolist()[0][0]

def rsi_acao(df, periods = 14):
    rsi = ultimo_rsi(df, periods)
    if rsi >= 50:
        return 'Compra'
    else:
        return 'Venda'

def rsi_tabela(options_tickers_uni, conn):
    options_tickers = [options_tickers_uni]
    #necessário baixar os dados novamente
    periodo = 1
    start = dt.datetime.now() - dt.timedelta(days=(365 * periodo))
    end = dt.datetime.now()
    df = filtra_banco(options_tickers, start, end, conn)

    df2 = pd.DataFrame(
        {
            'RSI(5)': [ultimo_rsi(df, 5),rsi_acao(df, 5)],
            'RSI(10)': [ultimo_rsi(df, 10),rsi_acao(df, 10)],
            'RSI(20)': [ultimo_rsi(df, 20),rsi_acao(df, 20)],
            'RSI(50)': [ultimo_rsi(df, 50),rsi_acao(df, 50)],
            'RSI(100)': [ultimo_rsi(df, 100),rsi_acao(df, 100)],
            'RSI(200)': [ultimo_rsi(df, 200),rsi_acao(df, 200)]
        },
        index = [
            'Índice', 'Ação'
        ]
    )

    return df2.transpose()