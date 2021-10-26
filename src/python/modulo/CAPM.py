from numpy.core.numeric import outer
import pandas as pd
import datetime as dt
from src.python.modulo.filtra_banco import filtra_banco
import numpy as np
import statsmodels.api as sm
pd.options.display.float_format = '{:.4f}'.format
import streamlit as st

def CAPM(data_filtrada, options_tickers, data_ref_mercado, ref_mercado, selic):

    data_CAPM = data_filtrada.merge(data_ref_mercado, how = 'outer', left_index= True, right_index = True)

    data_rend = data_CAPM[options_tickers].pct_change()
    data_rend = data_rend[1:]

    #transformando em array
    selic_diaria = (1+ (selic / 100)) ** (1/365) - 1 
    vetor_selic = np.repeat(selic_diaria, data_rend.shape[0])

    retorno_mercado = data_CAPM[ref_mercado].pct_change()
    retorno_mercado = retorno_mercado[1:]

    moeda_df = []
    beta = []
    alfa = []

    for moeda in options_tickers:
        #print(moeda)
        #Calculando o excesso de retorno e o prêmio de risco de mercado
        #para dataframe
        #excesso_retorno = data_rend[moeda].iloc[:,0].to_numpy() - vetor_selic
        #premio_risco_mercado = retorno_mercado.iloc[:,0].to_numpy() - vetor_selic

        #para series
        excesso_retorno = data_rend[moeda].to_numpy() - vetor_selic

        #talvez dê erro aqui se referencia_mercado nao for uma lista
        premio_risco_mercado = retorno_mercado.iloc[:,0].to_numpy() - vetor_selic

        #criando matriz com constante
        premio_risco_mercado_matriz = sm.add_constant(premio_risco_mercado, prepend=False)

        #estimando modelo
        model = sm.OLS(excesso_retorno, premio_risco_mercado_matriz)
        res = model.fit()

        moeda_df.append(''.join(moeda))
        beta.append(res.params[0])
        alfa.append(res.params[1])


    df = pd.DataFrame(
        {
            'ticket': moeda_df,
            'beta': beta,
            'alfa': alfa
        },
    )

    return df
