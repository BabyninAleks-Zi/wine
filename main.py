from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
from datetime import date
import pandas

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

company_age = date.today().year-1920


def get_wines():
    wines_data = pandas.read_excel('wine3.xlsx')
    wines_data = wines_data.fillna('')
    grouped_wines = defaultdict(list)
    for _, row in wines_data.iterrows():
        grouped_wines[row['Категория']].append({
            'Название': row['Название'],
            'Сорт': row['Сорт'],
            'Цена': row['Цена'],
            'Картинка': row['Картинка'],
            'Акция': row['Акция']
        })
    return dict(grouped_wines)


def years_word(company_age):
    if 11 <= company_age % 100 <= 14:
        return 'лет'
    if company_age % 10 == 1:
        return 'год'
    if 2 <= company_age % 10 <= 4:
        return 'года'
    return 'лет'


rendered_page = template.render(
    company_age=company_age,
    years_word=years_word(company_age),
    wines=get_wines()
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
