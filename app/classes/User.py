from binance.client import Client
from OrderData import OrderData


class User:
    APIKEY: str
    APISECRET: str
    client: Client

    ORDERS = []

    def __init__(self, api_key, api_secret):
        self.APIKEY = api_key
        self.APISECRET = api_secret

        self.client = Client(self.APIKEY, self.APISECRET, tld='com')

    def add_order(self, symbol_gen: str, symbol_api: str, in_coin=False, rsi_down=30.0, rsi_up=70.0, coin_count=0.0,
                  fiat_count=0.0):
        new_order = OrderData(self, symbol_gen, symbol_api, in_coin, rsi_down, rsi_up, coin_count, fiat_count)
        self.ORDERS.append(new_order)

    def delete_order(self, order: OrderData):
        self.ORDERS.remove(order)
