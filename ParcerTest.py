import requests
from bs4 import BeautifulSoup as BS
#import json

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}







################## global currency ##############################
url = 'https://cbr.ru/currency_base/daily/'

page = requests.get(url,headers=headers)
need_class = 'data'
html = BS(page.content, features='lxml')
all_values = html.find_all('td')

world_currency_num = ['840','978','156','826','392','756']
info_world_currency = []

for index in range(0,len(all_values),5):
    if all_values[index].text in world_currency_num:
        info_world_currency.append([item.text for item in all_values[index:index+5]])
print(info_world_currency)
####################################################    
    
#https://yandex.ru/search/?text=курс+
#with open("cross-currency.json","w") as file:
#    json.dump(dict,file,indent = 4, ensure_ascii=False)