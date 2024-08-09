# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
# import texts
import csv

# -------------
def set_up(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # загрузка сырого массива данных из подвала страницы сайта:
    review = soup.find('script', {'id': '__NEXT_DATA__'})
    return json.loads(review.text)


def write_cmc_top(data):
    initialState = json.loads(data['props']['initialState'])
    initialState['cryptocurrency']['listingLatest']['data'].pop(0)   # удаляем заголовки таблицы
    data_1 = initialState['cryptocurrency']['listingLatest']['data']

    # Каждый следующий файл при записи должен иметь название в следующем формате:
    # H.M dd.mm.yyyy, где H - Часы, M-минуты, dd- день, mm-месяц, yyyy-год.
    # file_name = '15.56 15.07.2024.csv'
    symbol_date = data_1[0][10]
    # print('date =', symbol_date)
    file_name = f'{symbol_date[11:13]}.{symbol_date[14:16]} {symbol_date[8:10]}.{symbol_date[5:7]}.{symbol_date[:4]}.csv'

    # подсчет глобальной капитализации на странице
    global_cap_page = 0
    for el in data_1:
        global_cap_page += el[18]
    # print('global_cap_page =', global_cap_page)

    # формирование выходных табличных данных и запись в файл .csv
    header = ['NAME', 'MC', 'MP']
    with open(file_name, 'w', newline='') as out_csv:
        writer = csv.writer(out_csv, delimiter=' ')
        writer.writerow(header)
        for el in data_1:
            outrow = [el[-4].capitalize(), f'{el[18]:,.0f}', f'{el[18] / global_cap_page * 100:.0f}%']
            writer.writerow(outrow)


url = 'https://coinmarketcap.com/ru/'
data = set_up(url)

write_cmc_top(data)

