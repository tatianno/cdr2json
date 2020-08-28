%matplotlib inline
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
plt.rc('figure', figsize = (50, 16))

#Mes de referencia
mes = '08'
ano = '2020'

#Tratando intervalos
lista_intervalos = ["08:40","10:00","11:20"]

#Arquivo utilizado para analisar dados
arquivo = 'json/cdr_{}-{}.json'.format(ano, mes)

#Minutos utilizados na amostragem
intervalo = 15

#Escala Y
escala_y = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

## Metodo para gerar resultado totalizado
def totalizar(chamadas_entrada, hora_inicial, intervalo_analisado=30):
    dados_totalizados = []
    data_inicial = datetime.strptime(
        '{}-{}-01 {}:00'.format(ano, mes, hora_inicial),
        '%Y-%m-%d %H:%M:%S'
    )
    
    while intervalo_analisado > 0:
        data_final = data_inicial + timedelta(minutes=intervalo)
        selecao = (chamadas_entrada['calldate'] >= data_inicial) & (chamadas_entrada['calldate'] <= data_final)
        periodo = chamadas_entrada[selecao]
        dados_totalizados.append(
            {
                'periodo' : data_inicial.strftime('%Y-%m-%d'),
                'dia' : data_inicial.strftime('%d/%m'),
                'chamadas': periodo.shape[0]
            }
        )
        intervalo_analisado -= 1
        data_inicial = data_inicial + timedelta(days=1)

    return pd.DataFrame(dados_totalizados)

##Recuperando dados
try:
    arq_json = open(arquivo, 'rb')
    dados = json.loads(arq_json.read())
    
except:
    dados = []
    
df = pd.DataFrame(dados)
df['calldate'] = pd.to_datetime(df['calldate'])

#Filtrando somente chamadas de entrada
selecao = (df['accountcode'] == 'ENT') & (df['dst'] == 'atendimento2')
chamadas_entrada = df[selecao]

