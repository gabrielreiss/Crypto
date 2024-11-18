#pegar os simbolos das 100 moedas com mais marketcap no site https://coinmarketcap.com/
#salvar no xls dos simbolos
#substituir codigo no download.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://coinmarketcap.com/"
driver.get(url)

vetor = []

try:
    symbols = driver.find_elements(By.CLASS_NAME, "coin-item-symbol")
    for symbol in symbols:
        print(symbol.text)
        vetor.append(symbol.text)
finally:
    driver.quit()
    
BASE_DIR = '.'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')

df = pd.DataFrame({
    "symbol": vetor
})

df.to_csv(os.path.join(DATA_DIR, 'simbolos2.csv'), mode='a', index=False, header=None)

df = pd.read_csv(os.path.join(DATA_DIR, 'simbolos2.csv'), header=0)
df = pd.DataFrame({"symbol": df['symbol'].unique()})

df.to_csv(os.path.join(DATA_DIR, 'simbolos2.csv'), mode='w', index=False)
