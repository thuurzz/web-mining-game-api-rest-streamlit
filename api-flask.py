import requests as req
from flask import jsonify
import pandas as pd
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health():
    return {'health': "server on-line"}


@app.route('/via-cep/<cep>', methods=['POST'])
def welcome():
    


    return {'health': "server on-line"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
