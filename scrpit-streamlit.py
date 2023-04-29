import streamlit as st
import requests as rq
import json
import pandas as pd
import plotly.express as px
import re


st.title("API Flask e Streamlit")

st.subheader("Busca de cotação de moeda")
opcoes = ['USD-BRL', 'EUR-BRL', 'BTC-BRL']
selecionado = st.selectbox('Selecione a moeda', opcoes)

cotacao = rq.post(f'http://127.0.0.1:3000/cotacao/{selecionado}').text
cotacao = json.loads(cotacao)
chave = selecionado.replace("-", "")
st.write('Moeda selecionada:', f'{selecionado} {cotacao["moedas_cotacao"]}')
st.write('Data da cotação:', cotacao["data_cotacao"])
st.write('Cotação da moeda em BRL máximo:', cotacao["valor_max"])
st.write('Cotação da moeda em BRL mínimo:', cotacao["valor_min"])
st.divider()

st.subheader(
    f'Conversão de valores {cotacao["moeda_saida"]} - {cotacao["moeda_entrada"]}')
brl_outra = st.number_input(
    'Digite um valor para conversão na moeda selecionada Ex: R$(1.50):')
conversao_brl_outra = round(brl_outra / float(cotacao["valor_max"]), 2)
st.write(
    f'O valor digitado, convertido para a moeda {selecionado}, é: {conversao_brl_outra} {cotacao["moeda_entrada"]}')
st.divider()

st.subheader(
    f'Conversão de valores {cotacao["moeda_entrada"]} - {cotacao["moeda_saida"]}')
outra_brl = st.number_input(
    f'Digite um valor para conversão na moeda selecionada Ex: {selecionado}(1.50):')
conversao_outra_brl = round(float(cotacao["valor_max"]) * outra_brl, 2)
st.write(
    f'O valor digitado, convertido para a moeda {selecionado}, é: {conversao_outra_brl} {cotacao["moeda_saida"]}')
st.divider()


quantidade_dias = st.number_input(
    'Digite a quantidade de dias para verificar a variação do valor da moeda:', 3)
st.subheader(
    f'Valor da moeda {cotacao["moeda_entrada"]} no últimos : {quantidade_dias} dias')
cotacao_datas = rq.post(
    f"http://127.0.0.1:3000/cotacao/{selecionado}/{quantidade_dias}").text
cotacao_datas = json.loads(cotacao_datas)
df = pd.DataFrame(cotacao_datas)
fig = px.line(df, x='data', y='valor')
st.plotly_chart(fig)
st.divider()


st.subheader(
    f'Busca de endereço por cep')
cep = st.text_input(
    'Digite seu cep', 00000000)

cep_regex = r"^\d{8}$"
if not re.match(cep_regex, cep):
    st.error('Digite o valor do cep com 8 dígitos: 0000000', icon="🚨")
else:
    cep_retorno = rq.post(
        f"http://127.0.0.1:3000/via-cep/{cep}").text
    cep_retorno = json.loads(cep_retorno)

    cep_retorno

st.divider()
