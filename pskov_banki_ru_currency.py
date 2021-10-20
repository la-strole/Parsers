import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def pskov_banki_ru_currency():
    """
    return: dict of dict
    structure:
    pskov_currency_dict:dict
    {'usd_sell':str : {'bank_name':str: bank_name:str,
                        'price':str : price:float,
                        'update_timestamp':str : timestamp: isoformat
                        }
    'usd_buy': str : {'bank_name':str: bank_name:str,
                        'price':str : price:float,
                        'update_timestamp':str : timestamp: isoformat
                        }
    'eur_sell': str : {'bank_name':str: bank_name:str,
                        'price':str : price:float,
                        'update_timestamp':str : timestamp: isoformat
                        }
    'eur_buy': str : {'bank_name':str: bank_name:str,
                        'price':str : price:float,
                        'update_timestamp':str : timestamp: isoformat
                        }
    'cbr': str : {'eur': str : value: float,
                  'usd': str : value: float
                  'update_timestamp': value: isoformat
                  }
    """
    url = "https://www.banki.ru/products/currency/cash/pskov/"
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

    class cur_exchange:
        def __init__(self, bank_name, usd_buy, usd_sell, eur_buy, eur_sell, update_time_date):
            self.bank_name = bank_name
            self.usd_buy = to_float(usd_buy)
            self.usd_sell = to_float(usd_sell)
            self.eur_buy = to_float(eur_buy)
            self.eur_sell = to_float(eur_sell)
            self.update_time_date = time_convert(update_time_date).isoformat()

        def __repr__(self):
            return f'{self.bank_name} usd {self.usd_buy} eur {self.eur_buy}'

    def time_convert(date_time: str):
        """
        Converts "* DD.MM.YYYY HH:MM*" to python datetime object
        ex: Время обновления: 11.10.2021 13:52 /t/t/t -> datetime.datetime
        :param date_time: DD.MM.YYYY HH:MM : String
        :return: python datetime object, else returns -1
        """
        assert type(date_time) == str
        u_date_time = re.search(r'(?P<u_date>\d{2}\.\d{2}\.\d{4}) +(?P<u_time>\d{2}:\d{2})', date_time)
        if u_date_time:
            u_date = u_date_time.group('u_date').split('.')[::-1]
            u_time = u_date_time.group('u_time').split(':')
            ret = datetime(*(map(int, u_date + u_time)))
            assert isinstance(ret, datetime)
            return ret
        else:
            return -1

    def to_float(s: str):
        """
        Convert string like '33,12' to float (replace ',' by '.')
        :param s: string like dd,dd
        :return: float dd.dd
        """
        assert isinstance(s, str)
        ret = s.strip()
        ret = s.replace(',', '.')
        ret = float(ret)
        return ret

    # assert that first 'USD' string is on currency exchange table
    currency_table = soup.select_one(".currency-table")

    upd_time = re.compile(r'Время обновления*')
    update_d_t_currency = str(currency_table.find(text=upd_time))

    central_bank = {
        'usd': float(((currency_table.find(text="USD")).findParent()).findNextSibling().text.replace(",", ".")),
        'eur': float(((currency_table.find(text="EUR")).findParent()).findNextSibling().text.replace(",", ".")),
        'update_timestamp': time_convert(update_d_t_currency).isoformat()
    }
    moex = {
        'usd': float(currency_table.find_all('span')[1].text.replace(",", ".")),
        'eur': float(currency_table.find_all('span')[2].text.replace(",", ".")),
        'update_timestamp': time_convert(update_d_t_currency).isoformat()
    }

    bank_section = soup.find("section", attrs={'class': 'widget', 'data-test': 'bank-rates-table'})
    str_bank = [*bank_section.find("tbody").stripped_strings]
    bank_list = []
    # "magic number" 6 here - count of arguments to initialize cur_exchange class instance
    for i in range(len(str_bank) // 6):
        bank_list.append(cur_exchange(*str_bank[(i * 6):((i + 1) * 6)]))

    best_buy_eur = max(bank_list, key=lambda _: _.eur_buy)
    best_buy_usd = max(bank_list, key=lambda _: _.usd_buy)
    best_sell_eur = min(bank_list, key=lambda _: _.eur_sell)
    best_sell_usd = min(bank_list, key=lambda _: _.usd_sell)

    usd_sell = {'bank_name': best_sell_usd.bank_name,
                'price': best_sell_usd.usd_sell,
                'update_timestamp': best_sell_usd.update_time_date
                }

    usd_buy = {'bank_name': best_buy_usd.bank_name,
               'price': best_buy_usd.usd_buy,
               'update_timestamp': best_buy_usd.update_time_date
               }

    eur_sell = {'bank_name': best_sell_eur.bank_name,
                'price': best_sell_eur.eur_sell,
                'update_timestamp': best_sell_eur.update_time_date
                }
    eur_buy = {'bank_name': best_buy_eur.bank_name,
               'price': best_buy_eur.eur_buy,
               'update_timestamp': best_buy_eur.update_time_date
               }

    pskov_currency_dict = {'usd_sell': usd_sell,
                           'usd_buy': usd_buy,
                           'eur_sell': eur_sell,
                           'eur_buy': eur_buy,
                           'cbr': central_bank}

    return pskov_currency_dict


if __name__ == '__main__':
    pskov_banki_ru_currency()
