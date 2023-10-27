import re
import logging

logging.basicConfig(level=logging.DEBUG)

def extract_data_from_statement(statement):
    lines = statement.split("\n")
    transactions = []
    current_date = None
    idx = len(lines) - 1  # Começamos do final
    month_of_statement = None
    transaction_id = 0

    # Identificar o mês do extrato
    for line in lines:
        date_match = re.match(r'^(\d{2}/\d{2})', line)
        if date_match:
            month_of_statement = date_match.group(1).split("/")[1]
            break

    while idx >= 0:
        line = lines[idx].strip()

        movement_match = re.search(r'(-?\d+,\d{2}-)', line)
        if movement_match:
            movement = movement_match.group(1)
            description_lines = [line.split(movement)[0].strip()]
            idx -= 1
            while idx >= 0 and not re.search(r'(-?\d+,\d{2}-)', lines[idx]) and not re.match(r'^(\d{2}/\d{2})', lines[idx]):
                description_lines.insert(0, lines[idx].strip())  # Adicionamos ao início para manter a ordem correta
                idx -= 1
            description = " ".join(description_lines)
            
            doc_num_match = re.search(r'(\d+)', description)
            doc_num = doc_num_match.group(1) if doc_num_match else '-'
            description = description.replace(doc_num, '').strip()
            
            transactions.append({"date": current_date, "description": description, "movement": movement, "doc_num": doc_num})
        else:
            idx -= 1

    formatted_data = []
    for transaction in reversed(transactions):  # Revertendo a ordem das transações
        transaction_id += 1
        date = transaction["date"]
        description = transaction["description"]
        movement = transaction["movement"]
        if movement.endswith('-'):
            movement = "-" + movement[:-1]
        doc_num = transaction["doc_num"]
        formatted_data.append((f"{transaction_id:04}", date, description, doc_num, movement))
    
    logging.debug(f"Formatted data: {formatted_data}")
    return formatted_data

statement = """
02/01 PIX ENVIADO
GLEIDSON AMARO DE SANTANA
- 743,81-
COMPRA CARTAO DEB MC
31/12 ILHA DA KOSTA RUI B
223982 870,52-
03/01 TARIFA AVULSA ENVIO PIX2 - 18,34-
TARIFA MANUTENCAO PAGFOR 490096 5,00-
TARIFA AVULSA ENVIO PIX - 8,34-
"""

data = extract_data_from_statement(statement)

for d in data:
    print(d)
