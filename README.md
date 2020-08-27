# Cdr2Json

Com esse script é possível extrair os dados da tabela cdr do asterisk para um arquivo json.

1- Configure os dados de conexão com o mysql no arquivo settings.py
2- Instale as dependências necessárias
> `$ pip3 install -r requeriments.txt`
3- Execute o script, temos 3 opções:
- Trazer os dados do mês corrente:
> `$ python3 main.py`
- Trazer os dados de um mês específico:
> `$ python3 main.py 2020-08`
- Trazer todos os dados do banco:
> `$ python3 main.py all`

O script analise.py foi escrito para analisar o volume de chamadas dentro do jupyter-notebook.
Podemos definir o mês de analise, dado usado também para abrir o arquivo json (linha 11)
```
mes = '08'
ano = '2020'
```
e também os horários desejados (linha 58)
```
dados_0840 = totalizar(chamadas_entrada, '08:40')
dados_1000 = totalizar(chamadas_entrada, '10:00')
dados_1120 = totalizar(chamadas_entrada, '11:20')
```