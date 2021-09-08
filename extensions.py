import requests
import json
from config import keys

class ConversionExeption(Exception):
    pass

class ValConverter:
    @staticmethod
    def convert(quote:str, base:str, amount:str):

        if quote == base:
            raise ConversionExeption("Невозможно конвертировать одинаковые валюты")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionExeption(f"{quote} - данной валюты нет в списке")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionExeption(f"{base} - данной валюты нет в списке")

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionExeption(f"Не удалось обработать количество {amount}")
        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key=604fa999c3558f5d0d3cf57b640e90c7&base={base_ticker}&symbols={quote_ticker}")
        total_base = (json.loads(r.content)['rates'])[keys[quote]]
        return total_base