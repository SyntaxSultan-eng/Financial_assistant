import requests
from bs4 import BeautifulSoup as BS

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}

def get_currency(url : str) -> str:
    need_class = 'ConverterInfo-Rate'
    page = requests.get(url,headers=headers)

    html_page = BS(page.content, features='lxml')
    info = html_page.find(class_=need_class).text
    return info

print(get_currency('https://yandex.ru/search/?text=доллар'))

