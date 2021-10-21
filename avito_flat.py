import json
import csv
import os
import requests
import re
import itertools
from bs4 import BeautifulSoup
from datetime import datetime


def avito_flat():
    current_date_time = datetime.now().isoformat()
    path_to_json_file = '/home/ub/Documents/GIT/parsers/'
    path_to_csv_file = 'home/ub/Documents/GIT/parsers/'

    def avito_price_convert(price: str):
        """
        Convert avito format numbers (like 2 222 222) to float format
        assert that cost for this flat is between 1 000 000 and 9 000 000
        :param price: string like 2 222 222
        :return: int like 2222222
        """
        assert type(price) == str
        mask_spaces = re.compile(r'\d \d{3} \d{3}')
        mask_no_brake_spaces = re.compile(r'(\d)\xa0(\d{3})\xa0(\d{3})')
        ret_s = re.findall(mask_spaces, price)
        ret_nbs = re.findall(mask_no_brake_spaces, price)
        if ret_s:
            return int(ret_s[0].replace(" ", ""))
        elif ret_nbs:
            return int(''.join(ret_nbs[0]))
        else:
            raise ValueError

    class flat:
        # for id dynamic generation (for future private key in DB?)
        new_id = itertools.count().__next__

        allowed_attrs = {'id': int, 'room_count': int, 'flat_area': float, 'floor': int, 'address': str,
                         'development_name': str, 'district': str, 'description': list, 'total_floors': int,
                         'avito_id': list, 'price': list, 'maybe_sold': bool}

        def __init__(self, attributes: dict):

            # area and floor, room_count are necessary for __eq__ and __hash__ and __repr__
            self.id = flat.new_id()
            self.flat_area = 0
            self.floor = 0
            self.room_count = 0
            self.maybe_sold = False
            self.room_count = 1
            self.maybe_sold = False
            assert isinstance(attributes, dict)
            self.__dict__.update((k, v) for k, v in attributes.items() if k in flat.allowed_attrs.keys())
            self.control_dict()

        def set_maybe_sold(self):
            """
            change may_be_sold (if it was False)to true and upgrade timestamps, else - do nothing
            :return: None
            """
            if self.maybe_sold:
                return
            else:
                self.maybe_sold = True
                for attribute in ('description', 'avito_id', 'price'):
                    if self.__dict__.get(attribute):
                        self.attribute[-1][1] = current_date_time
                self.control_dict()

        def control_dict(self):
            """
            check if  data types in class attributes are correct
            :return: nothing if that's OK, else raise exception
            """
            for k, v in flat.allowed_attrs.items():
                if self.__dict__.get(k):
                    assert isinstance(self.__dict__[f'{k}'], v)
                    if v == list:
                        for item in self.__dict__[f'{k}']:
                            assert isinstance(item, list)
                            assert len(item) == 2
                            if k == 'price':
                                assert isinstance(item[0], int)
                            else:
                                assert isinstance(item[0], str)
                            assert isinstance(item[1], str)

        def __repr__(self):
            return f'{self.room_count}к {self.flat_area} м2 {self.floor} этаж'

        def __eq__(self, other):
            if isinstance(other, flat):
                return self.floor == other.floor and self.flat_area == other.flat_area
            else:
                return False

        def __hash__(self):
            return hash((self.floor, self.flat_area))

    # get page from avito

    url = 'https://www.avito.ru/pskov/kvartiry/prodam/1-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ' \
          '?q=%D0%BA%D1%80%D0%B5%D1%81%D1%82%D0%BA%D0%B8+3%D0%B0'
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

    avito_flats_set = set()
    # looking for flats div css
    flat_div = soup.find("div", attrs={'class': "items-items-kAJAg", 'data-marker': 'catalog-serp'})
    flats = [_ for _ in flat_div.contents if _.attrs.get('data-marker') == 'item']
    # get info from flats
    for item in flats:
        # get room_count, floor, area
        # source - '1-к. квартира, 39,2\xa0м², 1/10\xa0эт.'
        # result - ('1', '39,2', '1/10')
        room_floor_line = re.match(r'(\d)-к\..+(\d\d.*)\xa0.*(\d\/\d.*)\xa0', item.find("h3",
                                                                                        attrs={
                                                                                            'itemprop': 'name'}).text)
        if room_floor_line:
            room_count = int(room_floor_line.groups()[0])
            flat_area = float(room_floor_line.groups()[1].replace(',', '.'))
            floor = int(room_floor_line.groups()[2].split('/')[0])
            total_floors = int(room_floor_line.groups()[2].split('/')[1])
        else:
            raise ValueError
        # get price
        price_line = item.find("span", attrs={'data-marker': 'item-price'}).text
        assert price_line
        price = avito_price_convert(price_line)
        # get address
        address_line = [*item.find("div", attrs={'data-marker': 'item-address'}).strings]
        assert address_line
        address = str(address_line[1])
        development_name = str(address_line[0])
        district = str(address_line[2].split(' ')[1])
        # get description
        description_line = item.find("div",
                                     attrs={'class': 'iva-item-text-_s_vh iva-item-description-S2pXQ text-text-LurtD '
                                                     'text-size-s-BxGpL'})
        assert description_line
        description = description_line.text
        # get id from avito
        avito_id = item['id']

        avito_flats_set.add(flat({'price': [[price, current_date_time]],
                                  'flat_area': flat_area,
                                  'floor': floor,
                                  'total_floors': total_floors,
                                  'address': address,
                                  'avito_id': [[avito_id, current_date_time]],
                                  'development_name': development_name,
                                  'district': district,
                                  'description': [[description, current_date_time]]}))

    # open json with flats - form list F, verify correct json decode with control_dict()
    file_flat_set = list()
    try:
        with open(path_to_json_file + 'avito_flat_krest.json', "r") as f:
            if os.path.getsize("/home/ub/Documents/GIT/parsers/avito_flat_krest.json") > 0:
                line = json.load(f)
                file_flat_set = []
                for item in line:
                    file_flat_set.append(flat(item))
                    file_flat_set[-1].control_dict()
            else:
                file_flat_set = []
    except FileNotFoundError:
        file_flat_set = []
    # F - A  mark as may_be_sold
    maybe_sold_set = [i for i in file_flat_set if i not in avito_flats_set]
    if maybe_sold_set:
        for item in maybe_sold_set:
            item.set_maybe_sold()
    # F & A - update price and timestamps
    update_set_flat = [i for i in file_flat_set if i in avito_flats_set]
    update_set_avito = [i for i in avito_flats_set if i in file_flat_set]
    for f_item in update_set_flat:
        for a_item in update_set_avito:
            if f_item == a_item:
                if f_item.maybe_sold and not a_item.maybe_sold:
                    f_item.maybe_sold = False
                if f_item.description[-1][0] != a_item.description[-1][0]:
                    f_item.description.append(a_item.description[-1])
                f_item.avito_id.append(a_item.avito_id[-1])
                f_item.price.append(a_item.price[-1])
                f_item.control_dict()
    # A - F - add to json file
    file_flat_set.extend([i for i in avito_flats_set if i not in file_flat_set])
    # write to  json file json dump
    with open(path_to_json_file + 'avito_flat_krest.json', "w") as f:
        f.write(json.dumps([i.__dict__ for i in file_flat_set]))
    # write to csv for export to open office
    with open(path_to_csv_file + 'avito_flat_kres.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([(i.maybe_sold, i.id, i.price[-1][0], i.price[-1][1]) for i in file_flat_set])
    with open(path_to_csv_file + 'for_open_office1.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        prices = []
        for i in file_flat_set:
            p = [str(p[0]) for p in i.price]
            p.insert(0, i.__repr__())
            p.insert(0, i.maybe_sold)
            prices.append(p)
        max_len = len(max(prices, key=len))
        for i in prices:
            while len(i) < max_len:
                i.insert(2, '0')
        writer.writerow((f'{len(file_flat_set)}', f'{max_len}'))
        writer.writerows(prices)


if __name__ == '__main__()':
    avito_flat()
