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

class CBR_ParcerConfig:
    """Класс для хранения url парсера api Центробанка"""

    def __init__(self):
        self.currency_url = 'http://www.cbr.ru/scripts/XML_daily.asp'

class AppConfig:
    """Класс настройки чувствительной информации"""

    def __init__(self):
        load_dotenv()
        self.bot = BotConfig()
        self.cbr = CBR_ParcerConfig()


config = AppConfig()