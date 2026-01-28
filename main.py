from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
from datetime import date
import pandas
import argparse


def build_page(wine_database):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    company_age = date.today().year - 1920

    return template.render(
        company_age=company_age,
        years_word=get_years_word(company_age),
        wines=get_wines(wine_database)
    )


def get_years_word(company_age):
    if 11 <= company_age % 100 <= 14:
        return 'лет'
    if company_age % 10 == 1:
        return 'год'
    if 2 <= company_age % 10 <= 4:
        return 'года'
    return 'лет'


def get_wines(wine_database):
    wines_data = pandas.read_excel(wine_database)
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


def main():
    parser = argparse.ArgumentParser(
        description='Сайт винодельни, введите путь к файлу с данными о винах'
    )
    parser.add_argument(
        '--wine_database',
        help='Путь к файлу с данными о винах',
        default='wine.xlsx'
    )
    args = parser.parse_args()
    wine_database = args.wine_database
    rendered_page = build_page(wine_database)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
