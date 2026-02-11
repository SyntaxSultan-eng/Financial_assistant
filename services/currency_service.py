import aiohttp
import xml.etree.ElementTree as ET
import asyncio

# Для тестирования этого файла использовать
# python -m services.currency_service
# Так мы запускаем services 
# как модуль из корневого каталога
# И становится видно модуль config
from config import config 

#############################

POPULAR_CURRENCY = (
    'USD',
    'EUR',
    'JPY',
    'GBP',
    'CHF',
    'CNY'
)

#############################

class CBRClient:
    """Класс для парсинга валют с Центробанка"""

    def __init__(self):
        self.session = None
        self.cache = {} # Простой кэш

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

        async with self.session.get(url) as response:
            return ET.fromstring(await response.text()) # Сразу парсим
    
    async def get_popular_currency(self) -> list:
        root = await self.get_data_xml()

        data = []

        for valute in root.findall('Valute'):
            if valute.find('CharCode').text in POPULAR_CURRENCY:
                information = (
                    valute.find('NumCode').text,
                    valute.find('CharCode').text,
                    valute.find('Nominal').text,
                    valute.find('Name').text,
                    valute.find('Value').text
                )
                data.append(information)
        return data
        
        
async def main():
    async with CBRClient() as client:
        print(await client.get_popular_currency())
        

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

