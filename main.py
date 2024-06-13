import telebot
import requests
from bs4 import BeautifulSoup
import time
#import json

###########################################################

token = "6271098507:AAE9MbgC7n2O-4JkcYsNTBO3ZH3L7AEChGM"
bot = telebot.TeleBot(token, parse_mode = None)

###########################################################

#settings (important variables)

#with open("Financial_bot\world_currency_LINKS_dict.json") as file:
#    all_world_currency = json.load(file)

#windows terminal don't see json file

headers = {
    "Accept" : "*/*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}

all_world_currency = {
    "USD": "https://www.banki.ru/products/currency/usd/",
    "EUR": "https://www.banki.ru/products/currency/eur/",
    "CNY": "https://www.banki.ru/products/currency/cny/",
    "GBP": "https://www.banki.ru/products/currency/gbp/",
    "CHF": "https://www.banki.ru/products/currency/chf/",
    "JPY": "https://www.banki.ru/products/currency/jpy/"
}

decoding = {
    "USD": "Американский Доллар",
    "EUR": "Евро",
    "CNY": "Китайский Юань",
    "GBP": "Британский Фунт",
    "CHF": "Швейцарский Франк",
    "JPY": "Японская Йена"
}

###########################################################

def get_all_currency():
    website = requests.get("https://www.banki.ru/products/currency/cb/", headers=headers)
    html_soup = BeautifulSoup(website.content, 'lxml')
    
    all_currency = html_soup.find("tbody").find_all("tr")
    information = ""

    for currency in all_currency:

        currency_name = currency.get("data-currency-name")
        сurrency_codename = currency.get("data-currency-code")
        currency_value = currency.find_all("td")[3].text
        currency_nums = currency.find_all("td")[1].text

        output = f"💵 {currency_nums} {сurrency_codename} ({currency_name}) - {currency_value}₽"
            
        information += "\n" + output + "\n"

    return information

def world_currency_info(country):
    global all_world_currency
    global history

    link = all_world_currency[country]
    website = requests.get(link, headers=headers)
    soup = BeautifulSoup(website.content, "lxml")
    all_values = soup.find_all("table")[1].find("tbody").find_all("td")
    
    counter = 0
    information = []
    symbols = []
    
    for _ in range(6):
        if counter >= 3:
            symbols.append(all_values[counter].text)
        else:
            information.append(all_values[counter].text)
        counter += 1 

    if country == "USD":
        countries = soup.find_all("p")[4].text.strip()
        history = soup.find_all("p")[5].text.strip()
    elif country == "EUR":
        countries = soup.find_all("p")[2].text.strip()
        history = soup.find_all("p")[3].text.strip()
    else:
        countries = soup.find_all("p")[1].text.strip()
        history = soup.find_all("p")[2].text.strip()

    return symbols,information,countries,history

def converter(value):
    website = requests.get("https://www.banki.ru/products/currency/cb/", headers=headers)
    html_soup = BeautifulSoup(website.content, 'lxml')
    
    all_currency = html_soup.find("tbody").find_all("tr")

    for currency in all_currency:
        сurrency_codename = currency.get("data-currency-code")
        if сurrency_codename == value:
            return float(currency.find_all("td")[3].text)

def news():
    website = requests.get("https://www.banki.ru/products/currency/cb/", headers=headers)
    html_soup = BeautifulSoup(website.content, 'lxml')

    all_news = html_soup.find_all("li", class_="text-list-item")
    news_and_links = {}

    for news in all_news:
        news_title = news.find('a').text
        news_link = 'https://www.banki.ru'+news.find('a').get("href")

        news_and_links[news_title] = news_link
    return news_and_links

def is_number(n):
    check = True
    try:
        num = float(n)
        # check for "nan" floats
        check = (num == num)
    except ValueError:
        check = False
    return check

###########################################################


@bot.message_handler(commands=['start'])

def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
    item_2 = telebot.types.KeyboardButton("📋Информация")
    item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
    item_4 = telebot.types.KeyboardButton("Новости 📰")
    item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

    markup.add(item_1, item_2, item_3, item_4, item_5)

    bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name}! Этот бот должен упростить мониторинг финансовых изменений на рынке валют. Ориентируйтесь по кнопкам!'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands=['news'])

def news_command(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
    item_2 = telebot.types.KeyboardButton("📋Информация")
    item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
    item_4 = telebot.types.KeyboardButton("Новости 📰")
    item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

    markup.add(item_1, item_2, item_3, item_4, item_5)

    bot.send_message(message.chat.id,  "Ожидайте...⏳", reply_markup= markup)

    news_dict = news()

    for item in news_dict:
        bot.send_message(message.chat.id, f"{item} ({news_dict[item]})")
        time.sleep(1)

@bot.message_handler(commands=['info'])

def give_info(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_1 = telebot.types.KeyboardButton("Назад 🔙")
    item_2 = telebot.types.KeyboardButton("О боте 🤖")

    markup.add(item_1, item_2)

    bot.send_message(message.chat.id, "Здесь вы можете увидеть официальные курсы иностранных валют, которые Банк России устанавливает по отношению к рублю ежедневно (по рабочим дням).К примеру, официальный курс обмена доллара США, евро, шведской кроны, фунтов стерлингов, швейцарского франка, китайского юаня, украинской гривны, белорусского рубля и так далее. Установленные Центробанком котировки вступают в силу на следующий календарный день после дня их определения и действуют до следующего их изменения.",reply_markup = markup)

@bot.message_handler(commands=['currency'])

def give_currency(message):
    bot.send_message(message.chat.id, "Ожидайте...⏳")
            
    currency = get_all_currency()
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
    item_2 = telebot.types.KeyboardButton("📋Информация")
    item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
    item_4 = telebot.types.KeyboardButton("Новости 📰")
    item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

    markup.add(item_1, item_2, item_3, item_4, item_5)

    time.sleep(1)

    bot.send_message(message.chat.id, currency, reply_markup= markup)

@bot.message_handler(commands=['history'])

def info_currency(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = telebot.types.KeyboardButton("Доллар 💲")
    item_2 = telebot.types.KeyboardButton("Евро 💶")
    item_3 = telebot.types.KeyboardButton("Британский Фунт 💂")
    item_4 = telebot.types.KeyboardButton("Японская Йена 🎌")
    item_5 = telebot.types.KeyboardButton("Китайский Юань 🀄️")
    item_6 = telebot.types.KeyboardButton("Швейцарский Франк 🏰")
    item_7 = telebot.types.KeyboardButton("Назад 🔙")

    markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)

    bot.send_message(message.chat.id, "Выберите валюту, которая вам интересна", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global num
    if call.data == "RUB":
        bot.edit_message_text("Режим выбран",call.message.chat.id,call.message.message_id)

        markup_line = telebot.types.InlineKeyboardMarkup()
        item_1 = telebot.types.InlineKeyboardButton("Доллар 💲", callback_data = "RUB-USD")
        item_2 = telebot.types.InlineKeyboardButton("Евро 💶", callback_data = 'RUB-EUR')
        item_3 = telebot.types.InlineKeyboardButton("Фунт 💂", callback_data = "RUB-GBP")
        item_4 = telebot.types.InlineKeyboardButton("Йена 🎌", callback_data = "RUB-JPY")
        item_5 = telebot.types.InlineKeyboardButton("Юань 🀄️", callback_data = "RUB-CNY")
        item_6 = telebot.types.InlineKeyboardButton("Франк 🏰", callback_data = "RUB-CHF")

        markup_line.add(item_1,item_2,item_3,item_4,item_5,item_6)

        bot.send_message(call.message.chat.id, "Выберете нужную валюту", reply_markup=markup_line)
    if call.data == "RUB-USD":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id) 
        
        currency = converter("USD")
        answer = float(num) / currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма рублей {num}₽ - это {format(answer, '.2f')}💲USD (Долларов)")
    if call.data == "RUB-EUR":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id) 

        currency = converter("EUR")
        answer = float(num) / currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма рублей {num}₽ - это {format(answer, '.2f')}💶EUR (Евро)")
    if call.data == "RUB-GBP":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)      

        currency = converter("GBP")
        answer = float(num) / currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма рублей {num}₽ - это {format(answer, '.2f')}💂GBP (Фунт стерлингов)")
    if call.data == "RUB-JPY":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("JPY")
        answer = (float(num) / currency)*100
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма рублей {num}₽ - это {format(answer, '.2f')}🎌JPY (Йена)")
    if call.data == "RUB-CNY":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("CNY")
        answer = int(num) / int(currency)
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма рублей {num}₽ - это {format(answer, '.2f')}🀄️CNY (Юань)")
    if call.data == "RUB-CHF":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("CHF")
        answer = float(num) / currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма рублей {num}₽ - это {format(answer, '.2f')}🏰CHF (Франк)")
    if call.data == "NORUB":
        bot.edit_message_text("Режим выбран",call.message.chat.id,call.message.message_id)

        markup_line = telebot.types.InlineKeyboardMarkup()
        item_1 = telebot.types.InlineKeyboardButton("Доллар 💲", callback_data = "USD-RUB")
        item_2 = telebot.types.InlineKeyboardButton("Евро 💶", callback_data = 'EUR-RUB')
        item_3 = telebot.types.InlineKeyboardButton("Фунт 💂", callback_data = "GBP-RUB")
        item_4 = telebot.types.InlineKeyboardButton("Йена 🎌", callback_data = "JPY-RUB")
        item_5 = telebot.types.InlineKeyboardButton("Юань 🀄️", callback_data = "CNY-RUB")
        item_6 = telebot.types.InlineKeyboardButton("Франк 🏰", callback_data = "CHF-RUB")

        markup_line.add(item_1,item_2,item_3,item_4,item_5,item_6)

        bot.send_message(call.message.chat.id, "Выберете нужную валюту", reply_markup=markup_line)
    if call.data == "USD-RUB":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("USD")
        answer = float(num) * currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма Долларов {num}💲 - это {format(answer, '.2f')}₽ (Рублей)")
    if call.data == "EUR-RUB":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("EUR")
        answer = float(num) * currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма Евро {num}💶 - это {format(answer, '.2f')}₽ (Рублей)")
    if call.data == "GBP-RUB":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("GBP")
        answer = float(num) * currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма Фунтов {num}💂 - это {format(answer, '.2f')}₽ (Рублей)")
    if call.data == "JPY-RUB":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("JPY")
        answer = float(num) * currency / 100
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма Йен {num}🎌 - это {format(answer, '.2f')}₽ (Рублей)")
    if call.data == "CNY-RUB":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)         

        currency = converter("CNY")
        answer = float(num) * currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма Юаней {num}🀄️ - это {format(answer, '.2f')}₽ (Рублей)")
    if call.data == "CHF-RUB":
        
        bot.edit_message_text("валюта выбрана",call.message.chat.id,call.message.message_id)        

        currency = converter("CHF")
        answer = float(num) * currency
       
        bot.send_message(call.message.chat.id,f"По курсу ЦБ РФ такая сумма Франков {num}🏰 - это {format(answer, '.2f')}₽ (Рублей)")

@bot.message_handler(content_types= ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == "Курс валют(ЦБ РФ)🏛️":
            bot.send_message(message.chat.id, "Ожидайте...⏳")
            
            currency = get_all_currency()
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
            item_2 = telebot.types.KeyboardButton("📋Информация")
            item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
            item_4 = telebot.types.KeyboardButton("Новости 📰")
            item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

            markup.add(item_1, item_2, item_3, item_4, item_5)

            time.sleep(1)

            bot.send_message(message.chat.id, currency, reply_markup= markup)
        elif message.text == "Назад 🔙":

            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
            item_2 = telebot.types.KeyboardButton("📋Информация")
            item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
            item_4 = telebot.types.KeyboardButton("Новости 📰")
            item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

            markup.add(item_1, item_2, item_3, item_4, item_5)

            bot.send_message(message.chat.id, "Возвращаю вас в главное меню! ↩", reply_markup = markup)
        elif message.text == "📋Информация":
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("О боте 🤖")

            markup.add(item_1, item_2)

            bot.send_message(message.chat.id, "Здесь вы можете увидеть официальные курсы иностранных валют, которые Банк России устанавливает по отношению к рублю ежедневно (по рабочим дням).К примеру, официальный курс обмена доллара США, евро, шведской кроны, фунтов стерлингов, швейцарского франка, китайского юаня, украинской гривны, белорусского рубля и так далее. Установленные Центробанком котировки вступают в силу на следующий календарный день после дня их определения и действуют до следующего их изменения.",reply_markup = markup)
        elif message.text == "О боте 🤖":
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
            item_2 = telebot.types.KeyboardButton("📋Информация")
            item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
            item_4 = telebot.types.KeyboardButton("Новости 📰")
            item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

            markup.add(item_1, item_2, item_3, item_4, item_5)

            bot.send_message(message.chat.id, "Версия бота - 0.1(релиз)")
            bot.send_message(message.chat.id, "Были добавлены функции: новости, курс ЦБ, конвертер валют, Информация о валютах; добавлены косметические улучшения бота.", reply_markup=markup)
        elif message.text == "Новости 📰":
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
            item_2 = telebot.types.KeyboardButton("📋Информация")
            item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
            item_4 = telebot.types.KeyboardButton("Новости 📰")
            item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

            markup.add(item_1, item_2, item_3, item_4, item_5)

            bot.send_message(message.chat.id,  "Ожидайте...⏳", reply_markup= markup)

            news_dict = news()

            for item in news_dict:
                bot.send_message(message.chat.id, f"{item} ({news_dict[item]})")
                time.sleep(1)
        elif message.text == "Конвертер валют 🔄":
            markup_return = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            return_button = telebot.types.KeyboardButton("Назад 🔙")

            markup_return.add(return_button)

            bot.send_message(message.chat.id,"Добро Пожаловать! Это простой конвертер мировых валют. Просто введите число!",reply_markup=markup_return)
        elif is_number(message.text):
            if int(message.text) < 0:
                markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                item_1 = telebot.types.KeyboardButton("Курс валют(ЦБ РФ)🏛️")
                item_2 = telebot.types.KeyboardButton("📋Информация")
                item_3 = telebot.types.KeyboardButton("💲 Информация о валютах 💲")
                item_4 = telebot.types.KeyboardButton("Новости 📰")
                item_5 = telebot.types.KeyboardButton("Конвертер валют 🔄")

                markup.add(item_1, item_2, item_3, item_4, item_5)
                bot.send_message(message.chat.id, "⛔ Ошибка!!! Отрицательное значение. Попробуйте снова", reply_markup=markup)
            else:
                global num 
                num = message.text
                markup_line = telebot.types.InlineKeyboardMarkup()
                item_1 = telebot.types.InlineKeyboardButton("Рубль ==> валюта", callback_data = 'RUB')
                item_2 = telebot.types.InlineKeyboardButton("валюта ==> Рубль", callback_data = "NORUB")

                markup_line.add(item_1,item_2)

                bot.send_message(message.chat.id, "Добро пожаловать в конвертер валют🔄! Выберете режим", reply_markup=markup_line)
        elif message.text == "💲 Информация о валютах 💲":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Доллар 💲")
            item_2 = telebot.types.KeyboardButton("Евро 💶")
            item_3 = telebot.types.KeyboardButton("Британский Фунт 💂")
            item_4 = telebot.types.KeyboardButton("Японская Йена 🎌")
            item_5 = telebot.types.KeyboardButton("Китайский Юань 🀄️")
            item_6 = telebot.types.KeyboardButton("Швейцарский Франк 🏰")
            item_7 = telebot.types.KeyboardButton("Назад 🔙")

            markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)

            bot.send_message(message.chat.id, "Выберите валюту, которая вам интересна", reply_markup=markup)
        elif message.text == "К выбору валют 💱":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Доллар 💲")
            item_2 = telebot.types.KeyboardButton("Евро 💶")
            item_3 = telebot.types.KeyboardButton("Британский Фунт 💂")
            item_4 = telebot.types.KeyboardButton("Японская Йена 🎌")
            item_5 = telebot.types.KeyboardButton("Китайский Юань 🀄️")
            item_6 = telebot.types.KeyboardButton("Швейцарский Франк 🏰")
            item_7 = telebot.types.KeyboardButton("Назад 🔙")

            markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)

            bot.send_message(message.chat.id, "Выберите валюту, которая вам интересна", reply_markup=markup)
        elif message.text == "Доллар 💲":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("К выбору валют 💱")

            markup.add(item_1, item_2)

            symbols, information, countries, history = world_currency_info("USD")

            bot.send_message(message.chat.id,f"{information[0]} - {symbols[0]} \n{information[1]} - {symbols[1]} \n{information[2]} - {symbols[2]}")
            bot.send_message(message.chat.id,f"Страны обращения валюты: \n{countries}")
            bot.send_message(message.chat.id,history,reply_markup = markup)
        elif message.text == "Евро 💶":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("К выбору валют 💱")

            markup.add(item_1, item_2)

            symbols, information, countries, history = world_currency_info("EUR")

            bot.send_message(message.chat.id,f"{information[0]} - {symbols[0]} \n{information[1]} - {symbols[1]} \n{information[2]} - {symbols[2]}")
            bot.send_message(message.chat.id,f"Страны обращения валюты: \n{countries}")
            bot.send_message(message.chat.id,history,reply_markup = markup)
        elif message.text == "Британский Фунт 💂":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("К выбору валют 💱")

            markup.add(item_1, item_2)

            symbols, information, countries, history = world_currency_info("GBP")

            bot.send_message(message.chat.id,f"{information[0]} - {symbols[0]} \n{information[1]} - {symbols[1]} \n{information[2]} - {symbols[2]}")
            bot.send_message(message.chat.id,f"Страны обращения валюты: \n {countries}")
            bot.send_message(message.chat.id,history,reply_markup = markup)
        elif message.text == "Японская Йена 🎌":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("К выбору валют 💱")

            markup.add(item_1, item_2)

            symbols, information, countries, history = world_currency_info("JPY")

            bot.send_message(message.chat.id,f"{information[0]} - {symbols[0]} \n{information[1]} - {symbols[1]} \n{information[2]} - {symbols[2]}")
            bot.send_message(message.chat.id,f"Страны обращения валюты: \n{countries}")
            bot.send_message(message.chat.id,history,reply_markup = markup)
        elif message.text == "Китайский Юань 🀄️":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("К выбору валют 💱")

            markup.add(item_1, item_2)

            symbols, information, countries, history = world_currency_info("CNY")

            bot.send_message(message.chat.id,f"{information[0]} - {symbols[0]} \n{information[1]} - {symbols[1]} \n{information[2]} - {symbols[2]}")
            bot.send_message(message.chat.id,f"Страны обращения валюты: \n{countries}")
            bot.send_message(message.chat.id,history,reply_markup = markup)
        elif message.text == "Швейцарский Франк 🏰":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1 = telebot.types.KeyboardButton("Назад 🔙")
            item_2 = telebot.types.KeyboardButton("К выбору валют 💱")

            markup.add(item_1, item_2)

            symbols, information, countries, history = world_currency_info("CHF")

            bot.send_message(message.chat.id,f"{information[0]} - {symbols[0]} \n{information[1]} - {symbols[1]} \n{information[2]} - {symbols[2]}")
            bot.send_message(message.chat.id,f"Страны обращения валюты: \n{countries}")
            bot.send_message(message.chat.id,history,reply_markup = markup)
        else:
            bot.send_message(message.chat.id, "⚠️ ⚠️ ⚠️ \n \n Бот не знает такой команды \n \n ❗Ориентируйтесь по кнопкам❗ \n \n ⚠️ ⚠️ ⚠️")
bot.infinity_polling()
