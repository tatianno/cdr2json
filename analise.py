#Script usado no jupyter-notebook
%matplotlib inline
import pandas as pd
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
plt.rc('figure', figsize = (50, 16))

#Mes de referencia
mes = '08'
ano = '2020'
#Arquivo utilizado para analisar dados
arquivo = 'json/cdr_{}-{}.json'.format(ano, mes)
#Minutos utilizados na amostragem
intervalo = 15

## Metodo para gerar grafico
def gerar_grafico(dados, legenda):
    grafico = plt.figure()
    g1 = grafico.add_subplot(2, 2, 1)
    g1.bar(dados['dia'], dados['chamadas'])
    g1.set_title(
        'Quantidade de chamadas X Dia do Mês - Mídia das {} (intervalo de {} minutos)'.format(
            legenda,
            intervalo
        )
    )


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

    dados = pd.DataFrame(dados_totalizados)
    gerar_grafico(dados, hora_inicial)

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

#Intervalo das 08:40
totalizar(chamadas_entrada, '08:40')
#Intervalo das 10:00
totalizar(chamadas_entrada, '10:00')
#Intervalo das 11:00
totalizar(chamadas_entrada, '11:00')