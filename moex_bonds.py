from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import re


def moex_bonds():
    """
    moex bonds parser
    :return: moex_bonds:dict
    structure: moex_bonds ={XS0893212398:str : price of  XS0893212398: float,
                            XS0088543193:str : price of of  XS0088543193: float
                            }
    """
    url_1 = 'https://www.moex.com/ru/issue.aspx?code=XS0893212398'
    url_2 = 'https://www.moex.com/ru/issue.aspx?code=XS0088543193#/bond_1'

    driver = webdriver.Firefox()
    driver.get(url_1)
    driver.find_element_by_link_text('Согласен').click()
    try:
        price_1 = (WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,
                                                                                                  'last')))).text

        # if no cells today than price would be "-" - we have to get price from yesterday.
        try:
            price_1 = float(price_1.replace(',', '.'))
        except ValueError:
            right_panel = driver.find_element_by_id('desc_container2')
            row = [_ for _ in right_panel.find_elements_by_tag_name('tr') if re.match(r'Цена последней', _.text)]
            assert len(row) == 1
            price_1 = row[0].find_element_by_tag_name('td').text
            """price_1 = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div/div[1]/div/div/div/div/div[3]/'
                                                   'div/div[2]/div[2]/div[1]/div/div[2]/div/table/tbody/tr[26]/td').text
            """
            price_1 = float(price_1.replace(',', '.'))
        driver.get(url_2)
        price_2 = (WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,
                                                                                                     'last')))).text
        # if no cells today than price would be "-" - we have to get price from yesterday.
        try:
            price_2 = float(price_2.replace(',', '.'))
        except ValueError:
            right_panel = driver.find_element_by_id('desc_container2')
            row = [_ for _ in right_panel.find_elements_by_tag_name('tr') if re.match(r'Цена последней', _.text)]
            assert len(row) == 1
            price_2 = row[0].find_element_by_tag_name('td').text
            price_2 = float(price_2.replace(',', '.'))
    finally:
        driver.quit()

    moex_bonds_dict = {'XS0893212398': price_1, 'XS0088543193': price_2}
    return moex_bonds_dict


if __name__ == '__main__':
    moex_bonds()
