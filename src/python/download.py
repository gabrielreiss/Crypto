#%%
#import pandas_datareader as web
import matplotlib.pyplot as plt
import mplfinance as mpf
import seaborn as sns
import datetime as dt
import os
import pandas as pd
import sqlalchemy
import yfinance as yf

BASE_DIR = '.'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')

str_conn = 'sqlite:///' + os.path.join(DATA_DIR, 'data.db')
engine = sqlalchemy.create_engine(str_conn)
conn = engine.connect()

currency = "USD"
metric = "Close"

end = dt.datetime.now()
start = dt.datetime.now() - dt.timedelta(365.25*5,0,0)

#df = pd.read_excel(os.path.join(DATA_DIR, 'simbolos.xls'))
df = pd.read_csv(os.path.join(DATA_DIR, 'simbolos2.csv'), header=0)

#crypto = ['BTC', 'ETH', 'LTC', 'XRP', 'DASH', 'SC']
crypto = list(df['symbol'])
colnames = []

first = True
#%%
for ticker in crypto:
    try:
        data = yf.download(f'{ticker}-{currency}', start = start, end = end)
        data.columns = data.columns.droplevel('Ticker')
        data.reset_index(level=None, drop=False, inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        data['ticker'] = ticker
        if first:
            print(f'Adicionando a moeda: {ticker}')
            data.to_sql('historico', conn, if_exists = 'replace', index = False)
            first = False
        else:
            print(f'Adicionando a moeda: {ticker}')
            data.to_sql('historico', conn, if_exists = 'append', index = False)
    except Exception as e:
        print(e)