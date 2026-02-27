import aiohttp
import xml.etree.ElementTree as ET
import asyncio
import time
from datetime import date

# Для тестирования этого файла использовать
# python -m services.currency_service
# Так мы запускаем services 
# как модуль из корневого каталога
# И становится видно модуль config
from config import config 

#############################

class Cache:
    """Класс для работы с кэшем для парсера валют"""

    def __init__(self):
        self.today_cache = config.cache.today_currency_cache # Кэш для дат на сегодня
        self.find_cache = config.cache.find_currency_cache # Кэш для поиска валют

    def set_data_in_today_cache(self, data):
        today = date.today().strftime('%d.%m.%Y')

        self.today_cache[today] = {
            'data' : data,
            'ttl': time.time() + config.cache.cache_TTL['popular']
        }

    def set_data_in_find_cache(self, data, id_date, user_input):
        if id_date is None:
            id_date = date.today().strftime('%d.%m.%Y')

        self.find_cache[f'{user_input}|{id_date}'] = {
            'data' : data,
            'ttl': time.time() + config.cache.cache_TTL['find']
        }
    
    def get_data_from_today_cache(self, id_date):
        self.clear_old_cache()
        data = self.today_cache.get(id_date)

        if data and time.time() < data['ttl']:
            return data['data']
        return None

    def get_data_from_find_cache(self, info, id_date):
        self.clear_old_cache()
        data = self.find_cache.get(f'{info}|{id_date}')

        if data and time.time() < data['ttl']:
            return data['data']
        return None
    
    #TODO исправить данный метод(неэффективен)
    def clear_old_cache(self):
        bad_keys_today_cache = []
        bad_keys_find_cache = []
        for key in self.today_cache:
            if time.time() > self.today_cache[key]['ttl']:
                bad_keys_today_cache.append(key)
        
        for key in bad_keys_today_cache:
            self.today_cache.pop(key)

        for key in self.find_cache:
            if time.time() > self.find_cache[key]['ttl']:
                bad_keys_find_cache.append(key)

        for key in bad_keys_find_cache:
            self.find_cache.pop(key)


class CBRClient:
    """Класс для парсинга валют с Центробанка"""

    def __init__(self):
        self.session = None
        self.cache = Cache()

    async def __aenter__(self): # Функция для входа/выхода из контекстного менеджера
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def get_data_xml(self, date=None):
        url = config.cbr.currency_url

        if date:
            url = config.cbr.currency_url + f'?date_req={date}' # date = dd/mm/yy

        try:
            async with self.session.get(url) as response:
                return ET.fromstring(await response.text()) # Сразу парсим
        except Exception:
            return None
    
    async def get_popular_currency(self, id_date : str) -> list:
        print(self.cache.today_cache)

        data = self.cache.get_data_from_today_cache(id_date)
        if data:
            print('из кэша')
            return data

        root = await self.get_data_xml()

        if root is None:
            return None

        data = []
        for valute in root.findall('Valute'):
            if valute.find('CharCode').text in config.cbr.POPULAR_CURRENCY:
                information = (
                    valute.find('NumCode').text,
                    valute.find('CharCode').text,
                    valute.find('Nominal').text,
                    valute.find('Name').text,
                    valute.find('Value').text,
                    root.attrib['Date']
                )
                data.append(information)

        self.cache.set_data_in_today_cache(
            data=data,
        )
        print('не из кэша')
        return data
    
    async def find_currency(self, name: str, date: str) -> tuple:
        print(self.cache.find_cache)

        data = self.cache.get_data_from_find_cache(name.lower(), date)
        if data:
            print('кэш')
            return data
            
        root = await self.get_data_xml(date=date)

        if root is None:
            return None
        
        for valute in root.findall('Valute'):

            if (
                name.lower() == valute.find('CharCode').text.lower() or 
                name.lower() == valute.find('Name').text.lower() or
                name == valute.find('NumCode').text
            ):

                information = (
                    valute.find('NumCode').text,
                    valute.find('CharCode').text,
                    valute.find('Nominal').text,
                    valute.find('Name').text,
                    valute.find('Value').text,
                    root.attrib['Date']
                )

                self.cache.set_data_in_find_cache(
                    user_input=name.lower(),
                    id_date=date,
                    data=information
                )
                print(information, 'не кэш')
                return information
        return ()

        
async def main():
    async with CBRClient() as client:
        print(await client.get_popular_currency())
        #print(await client.find_currency('Usd','02/07/2022'))

        
if __name__ == '__main__':
    asyncio.run(main())


# <?xml version="1.0" encoding="windows-1251"?>
#     <ValCurs Date="11.02.2026" name="Foreign Currency Market">
#         <Valute ID="R01010">
#             <NumCode>036</NumCode>
#             <CharCode>AUD</CharCode>
#             <Nominal>1</Nominal>
#             <Name>Австралийский доллар</Name>
#             <Value>54,6254</Value>
#                 <VunitRate>54,6254</VunitRate>
#             </Valute><Valute ID="R01020A">

