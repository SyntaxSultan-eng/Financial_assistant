import requests
from bs4 import BeautifulSoup as BS

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}


############################ url parcer ##############

#https://ru.tradingeconomics.com/commodities - сырье
#https://cbr.ru/currency_base/daily/ - валюта
#https://ru.tradingview.com/markets/stocks-russia/market-movers-gainers/ - акции

######################################################

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
    all_values = html_page.find_all(class_ = 'row-RdUXZpkv listRow')

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
    all_values = html_page.find_all(class_ ="row-RdUXZpkv listRow")

    # Возьмём первые 10 позиций
    counter = 0
    all_positions = []
    for item in all_values:
        counter += 1
        all_positions.append([item_info.text for item_info in item])
        if counter == 10:
            break
    return all_positions

######################################################

def get_all_material() -> dict:
    url = 'https://ru.tradingeconomics.com/commodities'
    page = requests.get(url,headers=headers)
    html_page = BS(page.content, features='lxml')

    all_names = html_page.find_all("td",{'class' : "datatable-item-first"})
    all_prices = html_page.find_all("td", {"class":"datatable-item","id":"p"})
    all_changes = html_page.find_all("td",{"class" : 'datatable-item', "id" : 'nch'})
    all_changes_percent = html_page.find_all("td",{"class":"datatable-item","id":"pch"})
    all_info = {}
    counter = 0

    for item in all_names:
        all_info[item.find('b').text.strip()] = (all_prices[counter].text.strip(),all_changes[counter].text.strip(),
        all_changes_percent[counter].text.strip())
        counter += 1

    return all_info

def energy() -> list:
    all_info = get_all_material()
    need_material = ["Нефть", "Нефть марки Brent","Газ","Бензин","Пропан","Каменный уголь"]
    energy_data = [[name,all_info[name]] for name in need_material]
    return energy_data

def metall() -> list:
    all_info = get_all_material()
    need_material = ["Золото","Серебро","Медь", "Сталь","Платина"]
    metal_data = [[name,all_info[name]] for name in need_material]
    return metal_data

def agriculture() -> list:
    all_info = get_all_material()
    need_material = ["Пшеница", "Молоко","Резина","Кофе","Картофель","Сахар"]
    agriculture_data = [[name,all_info[name]] for name in need_material]
    return agriculture_data

def industry() -> list:
    all_info = get_all_material()
    need_material = ["Алюминий", "Олово","полиэтилен","Никель","Полипропилен"]
    industry_data = [[name,all_info[name]] for name in need_material]
    return industry_data

########################################################

#0.1.1 version