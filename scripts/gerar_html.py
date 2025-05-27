# -*- coding: utf-8 -*-
import requests
import xlrd
from datetime import datetime
from decimal import Decimal
from jinja2 import Template
import os

def baixar_arquivo():
    url = 'https://cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2&download=true'
    headers = {
        'Referer': 'https://cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2',
        'User-Agent': 'Mozilla/5.0'
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    with open('cotacao.xls', 'wb') as f:
        f.write(r.content)

def extrair_ultima_cotacao():
    workbook = xlrd.open_workbook('cotacao.xls')
    sheet = workbook.sheet_by_index(0)
    for i in reversed(range(sheet.nrows)):
        row = sheet.row(i)
        if any(cell.value for cell in row):
            raw_date = row[0].value
            raw_price = row[1].value
            break
    cote_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
    quote_price = Decimal(str(raw_price)).quantize(Decimal("0.01"))
    return cote_date.strftime("%d/%m/%Y"), str(quote_price).replace(".", ",")

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
