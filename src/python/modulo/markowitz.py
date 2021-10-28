import numpy as np
import pandas as pd
import streamlit as st

def fronteira_eficiente(data_rend_diarios):
    np.random.seed(42)
    num_ports = 6000
    all_weights = np.zeros((num_ports, len(data_rend_diarios.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for x in range(num_ports):
        # Weights
        weights = np.array(np.random.random(len(data_rend_diarios.columns)))
        weights = weights/np.sum(weights)
        
        # Save weights
        all_weights[x,:] = weights
        
        # Expected return
        ret_arr[x] = np.sum( (data_rend_diarios.mean() * weights * 252))
        
        # Expected volatility
        vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(data_rend_diarios.cov()*252, weights)))
        
        # Sharpe Ratio
        sharpe_arr[x] = ret_arr[x]/vol_arr[x]

    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]
    pesos = pd.DataFrame(all_weights[sharpe_arr.argmax(),:], index =  list(data_rend_diarios.columns), columns = ['Pesos'])

    min_sr_ret = ret_arr[vol_arr.argmin()]
    min_sr_vol = vol_arr[vol_arr.argmin()]
    pesos_min = pd.DataFrame(all_weights[vol_arr.argmin(),:], index =  list(data_rend_diarios.columns), columns = ['Pesos'])
    
    return sharpe_arr.max(), pesos, ret_arr, vol_arr, sharpe_arr, max_sr_ret, max_sr_vol, min_sr_ret, min_sr_vol, pesos_min

