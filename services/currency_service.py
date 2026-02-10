import aiohttp
import xml.etree.ElementTree as ET
import asyncio

# Для тестирования этого файла использовать
# python -m services.currency_service
# Так мы запускаем services 
# как модуль из корневого каталога
# И становится видно модуль config
from config import config 


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

    async def get_data_xml(self):
        async with self.session.get(config.cbr.currency_url) as response:
            return await response.text()
    
    async def get_current_currency(self):
        xml_data = await self.get_data_xml()

        root = ET.fromstring(xml_data)

        for valute in root.findall('Valute'):
            print(valute.find('Name').text, valute.find('Value').text)
        
async def main():
    async with CBRClient() as client:
        await client.get_current_currency()


if __name__ == '__main__':
    asyncio.run(main())


# <Valuta name="Foreign Currency Market Lib">
#   <Item ID="R01010">
#       <Name>Австралийский доллар</Name>
#       <EngName>Australian Dollar</EngName>
#       <Nominal>1</Nominal>
#       <ParentCode>R01010 </ParentCode>
#       <ISO_Num_Code>36</ISO_Num_Code>
#       <ISO_Char_Code>AUD</ISO_Char_Code>
#   </Item>
