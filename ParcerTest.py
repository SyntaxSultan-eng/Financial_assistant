import requests
from bs4 import BeautifulSoup as BS
import json

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}

################## need currency ################
# url ='https://yandex.ru/search/?text=blockchain&lr=213&clid=2437996&src=suggest_Rec'

# need_class = 'ConverterInfo-Rate'
# page = requests.get(url,headers=headers)

# html_page = BS(page.content, features='lxml')
# info = html_page.find(class_=need_class)
# if info is None:
#     print('error')
################################################

################## global currency ##############################
# url = 'https://cbr.ru/currency_base/daily/'

# page = requests.get(url,headers=headers)
# need_class = 'data'
# html = BS(page.content, features='lxml')
# all_values = html.find_all('td')

# world_currency_num = ['840','978','156','826','392','756']
# info_world_currency = []

# for index in range(0,len(all_values),5):
#     if all_values[index].text in world_currency_num:
#         info_world_currency.append([item.text for item in all_values[index:index+5]])
# print(info_world_currency)
####################################################    

################## all currency #####################################

# url = 'https://cbr.ru/currency_base/daily/'

# page = requests.get(url,headers=headers)
# html = BS(page.content, features='lxml')
# all_values = html.find_all('td')
# dict_values = {all_values[i].text: [all_values[x].text for x in range(i+1,i+5)] for i in range(0,len(all_values),5)}

# with open("all-currency.json","w",encoding='utf-8') as file:
#    json.dump(dict_values,file,indent = 4, ensure_ascii=False)

############################ increase ##########################################

# url = 'https://ru.tradingview.com/markets/stocks-russia/market-movers-gainers/'

# page = requests.get(url,headers=headers)
# html = BS(page.content, features='lxml')
# all_values = html.find_all(class_='row-RdUXZpkv listRow')

# counter = 0
# for item in all_values:
#     counter += 1

#     info = item.find_all(class_='cell-RLhfr_y4')
#     print([text_info.text for text_info in info])
#     if counter == 10:
#         break


############################# drop ########################################

# url = "https://ru.tradingview.com/markets/stocks-russia/market-movers-losers/"
# page = requests.get(url,headers=headers)
# html_page = BS(page.content,features='lxml')
# all_values = html_page(class_ ="row-RdUXZpkv listRow")

# counter = 0
# for item in all_values:
#     counter += 1

#     info = item.find_all(class_='cell-RLhfr_y4')
#     print([text_info.text for text_info in info])
#     if counter == 10:
#         break

###########################################################################

# url = 'https://ru.tradingeconomics.com/commodities'
# page = requests.get(url,headers=headers)
# html_page = BS(page.content, features='lxml')

# all_names = html_page.find_all("td",{'class' : "datatable-item-first"})
# all_prices = html_page.find_all("td", {"class":"datatable-item","id":"p"})
# all_changes = html_page.find_all("td",{"class" : 'datatable-item', "id" : 'nch'})
# all_changes_percent = html_page.find_all("td",{"class":"datatable-item","id":"pch"})
# all_info = {}
# counter = 0

# for item in all_names:
#     all_info[item.find('b').text.strip()] = (all_prices[counter].text.strip(),all_changes[counter].text.strip(),
#     all_changes_percent[counter].text.strip())
#     counter += 1
# print(all_info)

######################################################################