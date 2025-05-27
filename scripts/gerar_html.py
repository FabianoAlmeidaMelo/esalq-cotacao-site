from playwright.sync_api import sync_playwright
from jinja2 import Template

def raspar_cotacao():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://fabianoalmeidamelo.github.io/cotacao/")
        page.wait_for_timeout(5000)  # espera 5 segundos para JS carregar

        html = page.content()
        browser.close()

    import re
    match = re.search(r'(\d{2}/\d{2}/\d{4}).*?class="maior">([\d,]+)<', html, re.DOTALL)
    if not match:
        raise Exception("Cotação não encontrada")

    data = match.group(1)
    preco = match.group(2)
    return data, preco

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
    data, preco = raspar_cotacao()
    gerar_html(data, preco)
