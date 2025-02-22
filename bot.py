# bot.py
import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Введите запрос в формате: <валюта1> <валюта2> <количество>")

@bot.message_handler(commands=['values'])
def send_values(message):
       bot.reply_to(message, "Доступные валюты: USD, EUR, RUB")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
       try:
           values = message.text.split(' ')

           if len(values) != 3:
               raise APIException("Неверное количество параметров.")

           base, quote, amount = values
           total = CurrencyConverter.get_price(base, quote, amount)
           text = f'Цена {amount} {base} в {quote} : {total}'
           bot.send_message(message.chat.id, text)

       except APIException as e:
           bot.reply_to(message, f"Ошибка пользователя.\n{e}")
       except Exception as e:
           bot.reply_to(message, f"Не удалось обработать команду\n{e}")

bot.polling()