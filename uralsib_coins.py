import requests
from bs4 import BeautifulSoup


def uralsib_coin_price():
    """
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
    uralsib_coin_price()
