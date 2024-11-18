# Acessando o app

Se tudo der certo, o aplicativo pode ser acessado através deste link: [Link do app](https://gabrielreiss-crypto-app-98revn.streamlit.app/)

## Como rodar em seu computador

abra o cmd na pasta onde quer instalar o app
```
git clone https://github.com/gabrielreiss/Crypto.git
cd crypto
download.bat
run.bat
```

versão alternativa utilizando conda
```
git clone https://github.com/gabrielreiss/Crypto.git
cd crypto
conda create -n "app" python=3.13.0
conda activate app
conda install --file requirements.txt
pip install -r requirements.txt
python src\python\modulo\as100maiores_moedas.py
python src\python\download.py
streamlit run app.py
```

versão utilizando venv
```
git clone https://github.com/gabrielreiss/Crypto.git
cd crypto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src\python\modulo\as100maiores_moedas.py
python src\python\download.py
streamlit run app.py
```
