import re
import logging


def extract_data_transaction(transaction):
    # Identificar linhas com data, descrição, valor e número do documento (se houver)
    data = transaction.split("|")

    #extrair dados da transação
    index = data[0]
    date = data[1]
    description = data[2]
    doc_num = data[3]
    movement = data[4]

    # Formatar os dados

    #aglutinar a descrição e o número do documento
    description = description + " " + doc_num

    #separar o valor do número do documento e formatar o valor se no final tiver " - " será negativo e se não tiver será positivo
    value = movement.split("-")[0]

    #separar o número do documento do valor
    doc_num = movement.split("-")[1]

    # Agglutinar as descrições
    if description == "-":
        description = data[2]
    else:
        if data[2] != "-":
            description = description + " " + data[2]

    # Retornar os dados
    return (index, date, description, doc_num, value)



statement = """
02/01 PIX ENVIADO
GLEIDSON AMARO DE SANTANA
- 743,81-
COMPRA CARTAO DEB MC
31/12 ILHA DA KOSTA RUI B
223982 870,52-
TARIFA MANUTENCAO PAGFOR 490096 5,00-
TARIFA AVULSA ENVIO PIX - 8,34-
"""

data = extract_data_transaction(statement)
for d in data:
    print(d)

