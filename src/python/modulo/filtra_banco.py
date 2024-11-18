import streamlit as st
import os
import pandas as pd
from src.python.modulo.apply_sql_template import apply_sql_template

BASE_DIR = os.path.abspath(".")
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
PYTHON_DIR = os.path.join(BASE_DIR, 'src', 'python')

def filtra_banco(ticker, start, end, conn):
    start = str(start)
    end = str(end)

    first = True
    for ticker1 in ticker:
        
        params = {
            'ticker': f'"{ticker1}"',
            'start': f'"{start}"',
            'end': f'"{end}"'
        }

        with open( os.path.join(SQL_DIR, 'select_dados.sql'), 'rb') as query_file:
            query = query_file.read().decode("UTF-8")

        query = apply_sql_template(query, params)

        data = pd.read_sql_query(query, conn, index_col="Date", parse_dates=['Date'])
        #del data['ticker']
        #data.columns = [ticker1]
        data.columns = [ticker1]
        #print(data.head())

        if first:
            base = data
            first = False
        else:
            base = base.merge(data, how='outer', left_index= True, right_index=True)
        
    return base
