import requests
from bs4 import BeautifulSoup as BS
#import json

page = requests.get("https://www.banki.ru/products/currency/cb")
html = BS(page.content, 'lxml')

all_values = html.find("Text__sc-j452t5-0 jxxlPG")
    



print(all_values)
#how_much = html.find_all('tbody')[3].find("strong").text.strip()
#print(how_much)
#answer = ""
#for item in all_values:
#    item_value = item.text.strip()
#    print(item_value)

#    answer += item_value.strip() + "\n"
#    if item_value is None:
#        dict[str(item_name)] = None
#        continue
#    else:
#        dict[str(item_name)] = "https://www.banki.ru"+str(item_value.get("href"))
#print(answer)

#dict = {
    #"USD": "Американский Доллар",
    #"EUR": "Евро",
    #"CNY": "Китайский Юань",
    #"GBP": "Британский Фунт",
    #"CHF": "Швейцарский Франк",
    #"JPY": "Японская Йена"
#}


#with open("cross-currency.json","w") as file:
#    json.dump(dict,file,indent = 4, ensure_ascii=False)