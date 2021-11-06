import requests
from bs4 import BeautifulSoup
import argparse
import csv


def uralsib_coin_price():
    """
    Get price of coin from Uralsib bank web site.
    :return: coin_price: float
    """
    url = 'https://www.uralsib.ru/investments-and-insurance/ivestitsii/invest-money/georgiy-pobedonosec-mmd-6497/'
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

    session = requests.session()
    response = session.get(url, headers=headers)
    assert response.ok

    soup = BeautifulSoup(response.text, 'lxml')
    coin_price = soup.select_one(".coin-price span").text
    clear_price = float((coin_price.strip()).replace(" ", ""))

    return clear_price


if __name__ == '__main__':

    # get path from command line (to run without libreoffice calc file)
    parser = argparse.ArgumentParser(description='get path to working directory')
    parser.add_argument('-path', type=str, required=True, help='/path/to/workingdir/')
    args = parser.parse_args()
    if args.path:
        path_to_working_directory = args.path
        coin = uralsib_coin_price()
        with open(path_to_working_directory + 'uralsib_coin_price.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow((f'{coin}',))

