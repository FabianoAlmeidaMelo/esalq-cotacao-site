import requests
import openpyxl
from datetime import datetime
from decimal import Decimal
from jinja2 import Template

def baixar_arquivo():
    url = 'https://cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2&download=true'
    headers = {
        'Referer': 'https://cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2',
        'User-Agent': 'Mozilla/5.0'
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    with open('cotacao.xlsx', 'wb') as f:
        f.write(r.content)

def extrair_ultima_cotacao():
    wb = openpyxl.load_workbook('cotacao.xlsx')
    sheet = wb.active

    for row in reversed(list(sheet.iter_rows(min_row=2, values_only=True))):
        if row and row[0] and row[1]:
            data_str = row[0].strftime('%d/%m/%Y') if isinstance(row[0], datetime) else str(row[0])
            preco_str = str(row[1])
            break

    data_formatada = datetime.strptime(data_str, "%d/%m/%Y").strftime("%d/%m/%Y")
    preco_formatado = str(Decimal(preco_str.replace(",", ".")).quantize(Decimal("0.01"))).replace(".", ",")

    return data_formatada, preco_formatado

def gerar_html(data, preco):
    template_str = """<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="UTF-8"><title>Cotação do Boi Gordo</title></head>
<body>
<span class="cotacao">{{ data }}: R$ {{ preco }}</span>
</body>
</html>"""
    html = Template(template_str).render(data=data, preco=preco)
    with open("index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    baixar_arquivo()
    data, preco = extrair_ultima_cotacao()
    gerar_html(data, preco)
