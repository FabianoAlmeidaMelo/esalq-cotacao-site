import requests
import openpyxl
from io import BytesIO
from datetime import datetime
from decimal import Decimal
from jinja2 import Template

def baixar_e_extrair_ultima_cotacao():
    url = 'https://cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2&download=true'
    headers = {
        'Referer': 'https://cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2',
        'User-Agent': 'Mozilla/5.0'
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    # Lê direto da memória
    wb = openpyxl.load_workbook(filename=BytesIO(r.content))
    sheet = wb.active

    # Procura da última linha útil (de baixo pra cima)
    for row in reversed(list(sheet.iter_rows(min_row=2, values_only=True))):
        if row and row[0] and row[1]:
            # row[0] é datetime ou string, row[1] é float
            data = row[0]
            preco = row[1]
            if isinstance(data, datetime):
                data_formatada = data.strftime("%d/%m/%Y")
            else:
                data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
            preco_formatado = str(Decimal(preco).quantize(Decimal("0.01"))).replace(".", ",")
            return data_formatada, preco_formatado

    raise Exception("Não foi possível encontrar a cotação")

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
    data, preco = baixar_e_extrair_ultima_cotacao()
    gerar_html(data, preco)
