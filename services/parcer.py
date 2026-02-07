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
#https://ru.tradingeconomics.com/forecast/crypto - крипта
#https://ru.tradingeconomics.com/stocks -индексы
#https://rosstat.gov.ru/ - индикаторы

######################################################

all_currency_status = True
growthstk_status = True
dropstk_status = True
all_material_status = True
crypto_status = True
index_status = True
economy_rus_status = True

######################################################

def get_all_currency() -> list:
    global all_currency_status
    
    if all_currency_status:

        url = 'https://cbr.ru/currency_base/daily/'

        page = requests.get(url,headers=headers)
        html = BS(page.content, features='lxml')
        all_values = html.find_all('td')

        world_currency_num = ['840','978','156','826','392','756']
        info_world_currency = []

        for index in range(0,len(all_values),5):
            if all_values[index].text in world_currency_num:
                info_world_currency.append([item.text for item in all_values[index:index+5]])

        if len(info_world_currency) == 0:
            all_currency_status = False
            return 'error_status'                
        return info_world_currency
    return 'error_status'
    
######################################################

def growth_stocks() -> list:

    global growthstk_status

    if growthstk_status:
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
        if len(all_positions) == 0:
            growthstk_status = False
            return 'error_status'
        return all_positions
    return 'error_status'

def drop_stocks() -> list:

    global dropstk_status

    if dropstk_status:
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
        if len(all_positions) == 0:
            dropstk_status = False
            return 'error_status'
        return all_positions
    return 'error_status'

######################################################

def get_all_material() -> dict:
    global all_material_status

    if all_material_status:
        try:
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
            if len(all_info) == 0:
                all_material_status = False
                return 'error_status'
            return all_info
        except:
            all_material_status = False
            return 'error_status'
    else:
        return 'error_status'

def energy() -> list:
    all_info = get_all_material()

    if all_info == "error_status":
        return "error_status"
    
    need_material = ["Нефть", "Нефть марки Brent","Газ","Бензин","Пропан","Каменный уголь"]
    energy_data = [[name,all_info[name]] for name in need_material]
    return energy_data

def metall() -> list:
    all_info = get_all_material()

    if all_info == "error_status":
        return "error_status"

    need_material = ["Золото","Серебро","Медь", "Сталь","Платина"]
    metal_data = [[name,all_info[name]] for name in need_material]
    return metal_data

def agriculture() -> list:
    all_info = get_all_material()

    if all_info == "error_status":
        return "error_status"

    need_material = ["Пшеница", "Молоко","Резина","Кофе","Картофель","Сахар"]
    agriculture_data = [[name,all_info[name]] for name in need_material]
    return agriculture_data

def industry() -> list:
    all_info = get_all_material()

    if all_info == "error_status":
        return "error_status"

    need_material = ["Алюминий", "Олово","полиэтилен","Никель","Полипропилен"]
    industry_data = [[name,all_info[name]] for name in need_material]
    return industry_data

########################################################

def crypto() -> list:
    global crypto_status

    if crypto_status:
        url = 'https://ru.tradingeconomics.com/forecast/crypto'
        page = requests.get(url,headers=headers)
        crypto_currency = BS(page.content,features='lxml').find("tbody")

        if crypto_currency is None:
            crypto_status = False
            return "error_status1", "error_status2"

        all_crypto_names = [item.find('b').text.strip() for item in crypto_currency.find_all("td",{'class' : "datatable-item-first"})]
        all_crypto_prices = [item.text.strip() for item in crypto_currency.find_all("td", {"class":"datatable-item","id":"p"})]
        
        if len(all_crypto_names) == 0 or len(all_crypto_prices) == 0:
            crypto_status = False
            return "error_status1", "error_status2"
        return all_crypto_names, all_crypto_prices
    else:
        return "error_status1", "error_status2"
    
########################################################

def index() -> list:
    url = "https://ru.tradingeconomics.com/stocks"
    page = requests.get(url,headers=headers)
    html_page = BS(page.content,features="lxml")

    return html_page.find_all("tbody")

def index_europe() -> list:
    global index_status
    
    if index_status:

        europe_indices = index()[1]

        index_names = [item.find('b').text.strip() for item in europe_indices.find_all("td", {'class' : "datatable-item-first"})]
        index_prices = [item.text.strip() for item in europe_indices.find_all("td", {'class' : "datatable-item", "id" : 'p'})]
        index_change_day = [item.text.strip() for item in europe_indices.find_all("td", {'class' : "datatable-item", "id" : 'nch'})]
        index_change_day_percent = [item.text.strip() for item in europe_indices.find_all("td", {'class' : "datatable-item", "id" : 'pch'})]
        if len(index_names) == 0 or len(index_prices) == 0 or len(index_change_day) == 0 or len(index_change_day_percent) == 0:
            index_status = False
            return "error_status1", "error_status2","error_status3", "error_status4"
        return index_names,index_prices,index_change_day,index_change_day_percent
    else:
        return "error_status1", "error_status2","error_status3", "error_status4"
    
def index_USA() -> list:
    global index_status
    
    if index_status:
        usa_indices = index()[2]

        index_names = [item.find('b').text.strip() for item in usa_indices.find_all("td", {'class' : "datatable-item-first"})]
        index_prices = [item.text.strip() for item in usa_indices.find_all("td", {'class' : "datatable-item", "id" : 'p'})]
        index_change_day = [item.text.strip() for item in usa_indices.find_all("td", {'class' : "datatable-item", "id" : 'nch'})]
        index_change_day_percent = [item.text.strip() for item in usa_indices.find_all("td", {'class' : "datatable-item", "id" : 'pch'})]

        if len(index_names) == 0 or len(index_prices) == 0 or len(index_change_day) == 0 or len(index_change_day_percent) == 0:
            index_status = False
            return "error_status1", "error_status2","error_status3", "error_status4"
        return index_names,index_prices,index_change_day,index_change_day_percent
    else:
        return "error_status1", "error_status2","error_status3", "error_status4"
    

def index_Asia() -> list:
    global index_status

    if index_status:
        asia_indices = index()[3]

        index_names = [item.find('b').text.strip() for item in asia_indices.find_all("td", {'class' : "datatable-item-first"})]
        index_prices = [item.text.strip() for item in asia_indices.find_all("td", {'class' : "datatable-item", "id" : 'p'})]
        index_change_day = [item.text.strip() for item in asia_indices.find_all("td", {'class' : "datatable-item", "id" : 'nch'})]
        index_change_day_percent = [item.text.strip() for item in asia_indices.find_all("td", {'class' : "datatable-item", "id" : 'pch'})]

        if len(index_names) == 0 or len(index_prices) == 0 or len(index_change_day) == 0 or len(index_change_day_percent) == 0:
            index_status = False
            return "error_status1", "error_status2","error_status3", "error_status4"
        return index_names,index_prices,index_change_day,index_change_day_percent
    else:
        return "error_status1", "error_status2","error_status3", "error_status4"
    

########################################################

def inflation() -> dict:
    global economy_rus_status

    if economy_rus_status:
    
        url = "https://www.cbr.ru/key-indicators/"
        second_url = "https://www.cbr.ru/"

        page = requests.get(url, headers=headers)
        html = BS(page.content, features='lxml')

        indicators_name = [item.text.strip() for item in html.find_all(class_ = "title")[:2]]
        indicators_subname = [item.text.strip() for item in html.find_all(class_ ="denotement")[:3]]
        indicators_value = [item.text.strip() for item in html.find_all(class_ ='value')[:3]]
        if len(indicators_name) == 0 or len(indicators_subname) == 0 or len(indicators_value) == 0:
            economy_rus_status = False
            return 'error_status', 'error_status'
        indicators_dict = {indicators_name[0] : {indicators_subname[0]:indicators_value[0], indicators_subname[1]:indicators_value[1]},indicators_name[1] : indicators_value[2]}

        second_page = requests.get(url=second_url,headers=headers)
        second_html = BS(second_page.content, features='lxml')

        if second_html.find(class_="main-indicator_comment-text") is None or second_html.find(class_="main-indicator_comment-date") is None:
            economy_rus_status = False
            return 'error_status', 'error_status'

        next_meeting = {second_html.find(class_="main-indicator_comment-text").text.strip() : second_html.find(class_='main-indicator_comment-date').text.strip()}

        return indicators_dict, next_meeting
    return 'error_status'
def info_economy_rus() -> dict:
    global economy_rus_status

    try:
        if economy_rus_status:
            url = "https://rosstat.gov.ru/"

            page = requests.get(url, headers=headers)
            html_page = BS(page.content,features='lxml')

            indicators_all = html_page.find_all(class_="indicators__cols")
            
            if len(indicators_all) == 0:
                economy_rus_status = False
                return 'error_status'

            indicators_info_dict = {}

            for index in range(1,len(indicators_all)):
                columns = indicators_all[index].find_all("div",{"class" :"indicators__col"})
                info_data = []
                for second_index in range(len(columns)):
                    str_data = columns[second_index].find("div", {"class" : "indicators__data"})
                    info_data.append(str_data.text.strip())
                indicators_info_dict[info_data[0]] = (info_data[1],info_data[2])

            return indicators_info_dict
    except Exception:
        return 'error_status'
    return 'error_status'


########################################################

def admin_info() -> list:
    return [all_currency_status,growthstk_status,dropstk_status,all_material_status,crypto_status,index_status,economy_rus_status]

def admin_currency_switch() -> bool:
    global all_currency_status
    all_currency_status = not all_currency_status
    return all_currency_status

def admin_stocks_up_switch() -> bool:
    global growthstk_status
    growthstk_status = not growthstk_status
    return growthstk_status

def admin_stocks_down_switch() -> bool:
    global dropstk_status
    dropstk_status = not dropstk_status
    return dropstk_status

def admin_material_switch() -> bool:
    global all_material_status
    all_material_status = not all_material_status
    return all_material_status

def admin_crypto_switch() -> bool:
    global crypto_status
    crypto_status = not crypto_status
    return crypto_status

def admin_index_switch() -> bool:
    global index_status
    index_status = not index_status
    return index_status

def admin_economy_switch() -> bool:
    global economy_rus_status
    economy_rus_status = not economy_rus_status
    return economy_rus_status

########################################################

#TODO
#Разделить логику на разные файлы(модули)