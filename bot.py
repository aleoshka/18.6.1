import telebot
from api import currency, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = 'Чтобы начать работу - введите команду боту:\n<имя валюты> \
 <в какую валюту перевести> \
 <кол-во переводимой валюты>.\nУвидеть доступные валюты: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступная валюта:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('cлишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'ОШИБКА ПОЛЬЗОВАТЕЛЯ:\n\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()