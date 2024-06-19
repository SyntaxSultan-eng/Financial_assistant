import requests
from bs4 import BeautifulSoup as BS
#import json

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}
#Дописать headers (появляется капча при парсинге)


url = 'https://yandex.ru/search/?text=доллар'
#https://yandex.ru/search/?text=курс+
page = requests.get(url,headers=headers)
need_class = 'ConverterInfo-Rate'
html = BS(page.content, features='lxml')
all_values = html.find(class_=need_class).text
print(all_values)


#with open("cross-currency.json","w") as file:
#    json.dump(dict,file,indent = 4, ensure_ascii=False)