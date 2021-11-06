import bs4.element
import requests
from bs4 import BeautifulSoup
import re
import argparse
import csv


def gold_price():
    """
    :return: gold_price_dict: dict
    structure: {'price':str : best_price:float,
                'bank_name':str: bank_name:str,
                'update_timestamp': 'date_like_dd.mm.yyyy':str}
    """
    url = 'https://bankinform.ru/services/metals/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    mask_buy_cost = re.compile(r"buyCostLabel")
    mask_update_date = re.compile(r"updateDateLabel")
    mask_metal_abbr = re.compile(r"MetalAbbr")
    mask_weight_label = re.compile(r"weightLabel")

    class bank_gold_price:
        def __init__(self, row):
            assert isinstance(row, bs4.element.Tag)
            self.price = float(row.find("span", id=mask_buy_cost).text.replace(' ', ''))
            self.bank_name = row.find("a").text
            self.update_timestamp = row.find("span", id=mask_update_date).text

    def satisfy_conditions(row):
        assert isinstance(row, bs4.element.Tag)
        return row.find("span", id=mask_metal_abbr) and \
               row.find("span", id=mask_metal_abbr).text == 'Au' and \
               row.find("span", id=mask_weight_label) and \
               row.find("span", id=mask_weight_label).text == '1'

    session = requests.session()
    responce = session.get(url, headers=headers)
    assert responce.ok

    soup = BeautifulSoup(responce.content, 'lxml')

    rows = soup.find_all("tr")
    the_best_bargin = max([bank_gold_price(row) for row in rows if satisfy_conditions(row)], key=(lambda x: x.price))

    gold_price_dict = {'price': the_best_bargin.price,
                       'bank_name': the_best_bargin.bank_name,
                       'update_timestamp': the_best_bargin.update_timestamp}

    return gold_price_dict


if __name__ == '__main__':

    # get path from command line (to run without libreoffice calc file)
    parser = argparse.ArgumentParser(description='get path to working directory')
    parser.add_argument('-path', type=str, required=True, help='/path/to/workingdir/')
    args = parser.parse_args()
    if args.path:
        path_to_working_directory = args.path
        gold = gold_price()
        with open(path_to_working_directory + 'best_gold_price.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([f'{gold["price"]}', f'{gold["bank_name"]}', f'{gold["update_timestamp"]}'])
