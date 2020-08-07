%matplotlib inline
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt

#Tamanho do gráfico
plt.rc('figure', figsize = (50, 16))
#Mes de referencia
mes = '08'
ano = '2020'
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
#Tratando intervalos
dados_0840 = totalizar(chamadas_entrada, '08:40')
dados_1000 = totalizar(chamadas_entrada, '10:00')
dados_1120 = totalizar(chamadas_entrada, '11:20')
#Gerando grafico
imagem = plt.figure()
grafico = imagem.add_subplot(2, 2, 1)
grafico.plot(dados_0840['dia'], dados_0840['chamadas'], 'o-', linewidth=2)
grafico.plot(dados_1000['dia'], dados_1000['chamadas'], 'o-', linewidth=2)
grafico.plot(dados_1120['dia'], dados_1120['chamadas'], 'o-', linewidth=2)
grafico.grid(linestyle='-', linewidth=2)
grafico.set_title("Chamadas X Mídia (considerando intervalo de {} minutos)".format(intervalo))
grafico.set_xlabel("Dia")
grafico.set_ylabel("Chamadas")
grafico.set_yticks(escala_y)
grafico.legend(["08:40","10:00",'11:20'], loc=4)
#Salvando grafico em um arquivo png
imagem.savefig(
    'graficos/graf_{}-{}.png'.format(ano, mes), 
    dpi = 300, 
    bbox_inches = 'tight'
)