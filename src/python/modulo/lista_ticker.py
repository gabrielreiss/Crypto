import os
import pandas as pd

BASE_DIR = os.path.abspath(".")
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
DATA_DIR = os.path.join(BASE_DIR,'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
PYTHON_DIR = os.path.join(BASE_DIR, 'src', 'python')

def lista_ticker(conn):
    with open( os.path.join(SQL_DIR, 'lista_ticker.sql'), 'rb') as query_file:
        query = query_file.read().decode("UTF-8")

    data = pd.read_sql_query(query, conn)
    return list(data['ticker'])