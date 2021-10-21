import datetime
import avito_flat
import moex_bonds
import gold_price
import pskov_banki_ru_currency
import uralsib_coins
import csv
import pyexcel

avito_flat.avito_flat()
path_to_csv = 'home/ub/Documents/GIT/parsers/'

bond_price = moex_bonds.moex_bonds()
with open(path_to_csv + 'for_open_office2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows([
        (f"{bond_price['XS0893212398']}",),
        (f"{bond_price['XS0088543193']}",)
    ])

gold = gold_price.gold_price()
# print(f'gold price: bank {gold["bank_name"]} with price {gold["price"]} at {gold["update_timestamp"]}')
with open(path_to_csv + 'for_open_office3.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([f'{gold["price"]}', f'{gold["bank_name"]}', f'{gold["update_timestamp"]}'])

coin = uralsib_coins.uralsib_coin_price()
with open(path_to_csv + 'for_open_office4.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow((f'{coin}',))
# print(f'gold coin price = {coin}')


currency = pskov_banki_ru_currency.pskov_banki_ru_currency()
with open(path_to_csv + 'for_open_office5.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows([
        (f'{currency["usd_buy"]["price"]}', f'{currency["usd_buy"]["bank_name"]}',
         f'{currency["usd_buy"]["update_timestamp"]}'),
        (f'{currency["eur_buy"]["price"]}', f'{currency["eur_buy"]["bank_name"]}',
         f'{currency["eur_buy"]["update_timestamp"]}'),
        (f'{currency["usd_sell"]["price"]}', f'{currency["usd_sell"]["bank_name"]}',
         f'{currency["usd_sell"]["update_timestamp"]}'),
        (f'{currency["eur_sell"]["price"]}', f'{currency["eur_sell"]["bank_name"]}',
         f'{currency["eur_sell"]["update_timestamp"]}'),
        (f'{currency["cbr"]["usd"]}', "Central Bank USD", f'{currency["cbr"]["update_timestamp"]}'),
        (f'{currency["cbr"]["eur"]}', "Central Bank EUR", f'{currency["cbr"]["update_timestamp"]}')
    ])

path_to_excel = '/home/ub/Downloads/finance/finance2.ods'
value = pyexcel.get_book(file_name=path_to_excel).sheet_by_name('инвестиционный план')['B17']
with open(path_to_csv + 'for_open_office0.csv', 'a+') as f:
    writer = csv.writer(f)
    writer.writerow((value, datetime.datetime.now().isoformat()))
