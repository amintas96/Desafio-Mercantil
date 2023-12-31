import streamlit as st
import pandas as pd
import requests
import logging
from Utils import Constantes
from API import Urls as url
from datetime import datetime, timedelta
import inspect

logging.basicConfig(
    filename=r'C:\Users\amint\Documents\logs\log.txt',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s'
)


def formata_log(msg):
    frame = inspect.currentframe()
    info = inspect.getframeinfo(frame)
    function_name = info.function
    file_name = info.filename
    line_number = info.lineno
    return f"{line_number} {function_name}, {file_name}: {msg} "

    

def info(msg):
    try:
        logging.info(msg=formata_log(msg))
    except Exception as e:
        print(str(e))
        
def error(msg):
    try:
        print(formata_log(msg))
        logging.error(formata_log(msg))
    except Exception as e:
        print(str(e))
    

    
def consulta_url_vendas(url_vendas, periodo=None):
    info(Constantes.INICIA)
    try:
        if url_vendas and periodo is None:
        
            col1, col2 = st.columns(2) 
            json_data = requests.get(url=url_vendas).json() 
            time_series_data = json_data["Time Series (5min)"]
            st.write(json_data['Meta Data'])
            data_list = [
                {
                    "timestamp": timestamp,
                    "open": float(data["1. open"]),
                    "high": float(data["2. high"]),
                    "low": float(data["3. low"]),
                    "close": float(data["4. close"]),
                    "volume": int(data["5. volume"])
                }
                for timestamp, data in time_series_data.items()
            ]
            df = pd.DataFrame(data_list)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            with col1:
                st.title('Gráfico de Volume de Vendas')
                st.line_chart(df['volume'])
            with col2: 
                st.title('Base de dados')
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df)
                return json_data
        elif periodo is not None:
            pass   
    except Exception as e:
            error(str(e))
            

def obter_primeiro_e_ultimo_dia_do_mes(ano, mes):
    try:
        info(Constantes.INICIA)
        primeiro_dia = datetime(year=ano, month=mes, day=1)
        ultimo_dia = primeiro_dia.replace(month=primeiro_dia.month + 1, day=1) - timedelta(days=1)
        return primeiro_dia, ultimo_dia
    except Exception as e:
        error(str(e))


def filtrar_por_periodo(json_data, data_inicio, data_fim):
    resultado_filtrado = {}
    
    
    for timestamp, data in json_data["Time Series (5min)"].items():
        timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        
        if data_inicio <= timestamp_datetime <= data_fim:
            resultado_filtrado[timestamp] = data
    
    return resultado_filtrado


def retira_mes_ano(str_date):

    data_string = str(str_date)
    if '/' in str_date:
        data_datetime = datetime.strptime(data_string, "%Y/%m/%d")
    elif '-' in str_date:
        data_datetime = datetime.strptime(data_string, "%Y-%m-%d")

    mes = data_datetime.month
    ano = data_datetime.year
    return mes, ano

def busca_periodo(date):
    info(Constantes.INICIA)
    try:
        json_data =requests.get(url=url.url_Shanghai_Stock_Exchange).json()
        mes, ano = retira_mes_ano(date)
        primeiro_dia, ultimo_dia = obter_primeiro_e_ultimo_dia_do_mes(ano=ano, mes=mes)
        resultados_filtrado = filtrar_por_periodo(json_data=json_data, data_inicio=primeiro_dia, data_fim=ultimo_dia)
        if resultados_filtrado:
            consulta_url_vendas(json_data, True) 
        
    except Exception as e:
        error(str(e))
        return None


def create_user():
    st.title("Criar Usuário")

    # Adicione campos para entrada de dados
    nome = st.text_input("Nome:")
    email = st.text_input("Email:")

    # Botão para criar usuário
    if st.button("Criar Usuário"):

        if nome and email:
            st.success(f"Usuário criado com sucesso!\nNome: {nome}\nEmail: {email}")
        else:
            st.warning("Por favor, preencha todos os campos.")


def buscar_usuarios_por_nome(nome_pesquisado, lista_usuarios):
    resultados = [usuario for usuario in lista_usuarios if nome_pesquisado.lower() in usuario.nome.lower()]
    return resultados

@st.cache
def calcular_media_volume_gastos(df):
    return df['volume'].mean()