import json

import requests

# Você foi contratado como freelancer por uma empresa de análise de dados que precisa de uma solução para o seguinte problema:
# Todos os dias a instituição precisa saber qual moeda possui a menor cotação frente ao dólar. Essa informação é importante para uma outra aplicação de ranking de moedas que eles irão desenvolver.
# A instituição te passou o link do banco central (https://www.bcb.gov.br/) como referência. A empresa em si também não conhece o site do BC detalhadamente para indicar o lugar exato da fonte de dados.
# Neste momento, o que eles precisam é um programa que receba uma data no formato YYYYMMDD via terminal e exiba na saída o símbolo da moeda, o nome do país de origem e o valor da cotação desta moeda frente ao dólar na data especificada. Caso não haja cotação no dia especificado, o caracter 'x' deve ser impresso na tela.
# Escreva um programa em python que atenda aos requisitos acima.

dicionario = {}
data = input(str("digite a tada de pesquisa (formato YYYYMMDD): "))
data_formatada = f'{data[4:6]}-{data[6:9]}-{data[0:4]}'
url_moedas = requests.get("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json")

if url_moedas.status_code == 200:
    dicionario = json.loads(url_moedas.text)

    for i in dicionario['value']:
        simbolo = i['simbolo']
        nome_moeda = i['nomeFormatado']
        url_valores = requests.get(
            f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda='{simbolo}'&@dataCotacao='{data_formatada}'&$top=1&$format=json&$select=cotacaoCompra")
        if not url_valores.json()['value']:
            print('x')
            break

        print(simbolo, nome_moeda ,url_valores.json()['value'][0]['cotacaoCompra'])

else:
    print("sem comunicação com a base de dados")
