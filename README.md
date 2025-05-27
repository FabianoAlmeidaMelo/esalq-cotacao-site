# esalq-cotacao-site

Repositório que publica automaticamente a última cotação do Boi Gordo da ESALQ.

## Como funciona

- Um GitHub Actions diário baixa o XLS do site da ESALQ.
- Extrai a última cotação e data.
- Gera um HTML simples e atualiza `index.html`.
- Publicado em: https://<seu-usuario>.github.io/esalq-cotacao-site/

## Formato do HTML

```html
<span class="cotacao">21/05/2025: R$ 305,00</span>
