from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# CoinMarketCap Crypto listing lastest tab for paramerters

# https://blog.tati.digital/2020/11/30/python-flask-web-application-tutorial-2020-display-coinmarketcap-api-data/


class Crypto:

    def get_top_50(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "start": "1",
            "limit": "50",
            "convert": "USD"
        }

        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8f0aba7f-9416-48b3-8cf9-e2b39fdc49f1",
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data["data"]
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


    def get_name(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            "start": "1",
            "limit": "50",
        }

        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8f0aba7f-9416-48b3-8cf9-e2b39fdc49f1",
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data["data"]
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


# Taken from Coin Market Cap API documentation
