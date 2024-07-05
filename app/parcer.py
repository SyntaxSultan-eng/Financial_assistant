import requests
from bs4 import BeautifulSoup as BS

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}

######################################################

def get_currency(url : str) -> str:
    need_class = 'ConverterInfo-Rate'
    page = requests.get(url,headers=headers)

    html_page = BS(page.content, features='lxml')
    info = html_page.find(class_=need_class)
    if info is None:
        return 'error'
    return info.text

def get_all_currency() -> list:
    
    url = 'https://cbr.ru/currency_base/daily/'

    page = requests.get(url,headers=headers)
    html = BS(page.content, features='lxml')
    all_values = html.find_all('td')

    world_currency_num = ['840','978','156','826','392','756']
    info_world_currency = []

    for index in range(0,len(all_values),5):
        if all_values[index].text in world_currency_num:
            info_world_currency.append([item.text for item in all_values[index:index+5]])
    return info_world_currency
    
######################################################

def growth_stocks() -> list:

    url = 'https://ru.tradingview.com/markets/stocks-russia/market-movers-gainers/'
    page = requests.get(url,headers=headers)
    html_page = BS(page.content,features='lxml')
    all_values = html_page(class_ = 'row-RdUXZpkv listRow')

    # Возьмём первые 10 позиций
    counter = 0
    all_positions = []
    for item in all_values:
        counter += 1
        all_positions.append([item_info.text for item_info in item])
        if counter == 10:
            break
    return all_positions

def drop_stocks() -> list:

    url = "https://ru.tradingview.com/markets/stocks-russia/market-movers-losers/"
    page = requests.get(url,headers=headers)
    html_page = BS(page.content,features='lxml')
    all_values = html_page(class_ ="row-RdUXZpkv listRow")

    # Возьмём первые 10 позиций
    counter = 0
    all_positions = []
    for item in all_values:
        counter += 1
        all_positions.append([item_info.text for item_info in item])
        if counter == 10:
            break
    return all_positions


########################################################

