import aiohttp
import xml.etree.ElementTree as ET
import asyncio
import time

# Для тестирования этого файла использовать
# python -m services.currency_service
# Так мы запускаем services 
# как модуль из корневого каталога
# И становится видно модуль config
from config import config 

#############################

class CBRClient:
    """Класс для парсинга валют с Центробанка"""

    def __init__(self):
        self.session = None
        self.cache = config.cbr.cache # Простой кэш

    async def __aenter__(self): # Функция для входа/выхода из контекстного менеджера
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    def set_data_in_cache(self, data, id):
        self.cache[id] = {
            'data' : data,
            'ttl': time.time() + 3600 # Время жизни - 1 час.
        }

    def get_data_from_cache(self, id=None):
        if time.time() > self.cache[id]['ttl']:
            return None
        return self.cache[id]['data']

    async def get_data_xml(self, date=None):
        url = config.cbr.currency_url

        if date:
            url = config.cbr.currency_url + f'?date_req={date}' # date = dd/mm/yy

        try:
            async with self.session.get(url) as response:
                return ET.fromstring(await response.text()) # Сразу парсим
        except Exception:
            return None
    
    async def get_popular_currency(self) -> list:
        id = 'today-currency'

        if id in self.cache:
            data = self.get_data_from_cache(id)
            if data:
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
                    valute.find('Value').text
                )
                data.append(information)

        self.set_data_in_cache(
            data=data,
            id=id
        )
        return data
    
    async def find_currency(self, name: str) -> tuple:
        id = name.lower()

        if id in self.cache:
            data = self.get_data_from_cache(id)
            if data:
                return data
            
        root = await self.get_data_xml()

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
                    valute.find('Value').text
                )

                self.set_data_in_cache(
                    data=information,
                    id=id
                )
                return information
        return ()

        
async def main():
    async with CBRClient() as client:
        print(await client.find_currency('012'))

        
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

