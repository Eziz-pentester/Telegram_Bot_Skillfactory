
# extensions.py
import requests
import json

class APIException(Exception):
 pass

class CurrencyConverter:
       @staticmethod
       def get_price(base: str, quote: str, amount: str):
           try:
               amount = float(amount)
           except ValueError:
               raise APIException(f"Не удалось обработать количество {amount}")

           base = base.upper()
           quote = quote.upper()

           if base == quote:
               raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

           try:
               response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}')
               data = json.loads(response.text)
               rate = data['rates'][quote]
           except KeyError:
               raise APIException(f"Валюта {base} не найдена.")
           except Exception as e:
               raise APIException(f"Ошибка при обработке запроса: {str(e)}")

           return rate * amount