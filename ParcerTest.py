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

url = 'https://cbr.ru/currency_base/daily/'

page = requests.get(url,headers=headers)
html = BS(page.content, features='lxml')
all_values = html.find_all('td')
dict_values = {all_values[i].text: [all_values[x].text for x in range(i+1,i+5)] for i in range(0,len(all_values),5)}

with open("all-currency.json","w",encoding='utf-8') as file:
   json.dump(dict_values,file,indent = 4, ensure_ascii=False)

######################################################################