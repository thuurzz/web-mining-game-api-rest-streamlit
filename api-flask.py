from flask import Flask
import requests as req
import json
from datetime import datetime
import pytz

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health():
    return {'health': "server on-line"}


@app.route('/via-cep/<cep>', methods=['POST'])
def buscaCep(cep):
    # 00000000
    resp = req.get(f'https://viacep.com.br/ws/{cep}/json/')
    return resp.text


@app.route('/cotacao/<moeda>', methods=['POST'])
def buscaCotacao(moeda):
    # USD-BRL,EUR-BRL,BTC-BRL
    resp = req.get(
        f'https://economia.awesomeapi.com.br/last/{moeda}').text
    resp = json.loads(resp)
    chave = moeda.replace("-", "")
    retorno = {
        "moeda_entrada": resp[chave]["code"],
        "moeda_saida": resp[chave]["codein"],
        "moedas_cotacao": resp[chave]["name"],
        "valor_max": resp[chave]["high"],
        "valor_min": resp[chave]["low"],
        "data_cotacao": resp[chave]["create_date"],
    }
    return retorno


@app.route('/cotacao/<moeda>/<dias>', methods=['POST'])
def buscaCotacaoDias(moeda, dias=1):
    # USD-BRL,EUR-BRL,BTC-BRL
    resp = req.get(
        f"https://economia.awesomeapi.com.br/json/daily/{moeda}/{dias}").text
    resp = json.loads(resp)
    retorno = []
    for data in resp:
        dt = datetime.fromtimestamp(int(data['timestamp']))
        br_tz = pytz.timezone('America/Sao_Paulo')
        dt_br = dt.astimezone(br_tz)
        data_formata = dt_br.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        retorno.append(
            {
                "valor": data['high'],
                "data": data_formata.split(" ")[0]
            }
        )
    return retorno


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
