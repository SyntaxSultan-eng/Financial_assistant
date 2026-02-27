import os
from dotenv import load_dotenv

class BotConfig:
    """Класс для хранения ключей и т.д для телеграмм бота"""

    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.admin_id = int(os.getenv('Admin_ID'))
        self._validate()
        
    def _validate(self) -> None:
        if not self.api_key:
            raise ValueError('Отсутствует ключ бота.')

class ParcerCache:
    """Класс для хранения кэша для парсера"""

    def __init__(self):
        self.today_currency_cache = {}
        self.find_currency_cache = {}
        self.cache_TTL = {
            'popular' : 60, # 6 часов
            'find' : 3600
        }

class CBR_ParcerConfig:
    """Класс для хранения url парсера api Центробанка"""

    POPULAR_CURRENCY = (
        'USD',
        'EUR',
        'JPY',
        'GBP',
        'CHF',
        'CNY'
    )

    def __init__(self):
        self.currency_url = 'http://www.cbr.ru/scripts/XML_daily.asp'
        self.pdf_file_url = os.path.join('config','requirements','currency.pdf')

class AppConfig:
    """Класс настройки чувствительной информации"""

    def __init__(self):
        load_dotenv()
        self.bot = BotConfig()
        self.cache = ParcerCache()
        self.cbr = CBR_ParcerConfig()


config = AppConfig()