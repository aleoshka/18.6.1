import requests
import json
from api import currency


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'невозможно перевести одинаковые валюты «{base}»')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту «{quote}»')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f'не удалось обработать валюту «{base}»')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'не удалось обработать кол-во «{amount}»')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base * amount
