from binance.client import Client
from OrderData import OrderData
import math
from binance.enums import *


class User:
    APIKEY: str
    APISECRET: str
    client: Client  # = Client("APIKEY", "APISECRET", tld='com')

    COIN_COUNT: float = 0.0
    FIAT_COUNT: float = 0.0

    ORDERS = []

    def __init__(self, api_key, api_secret):
        self.APIKEY = api_key
        self.APISECRET = api_secret

        self.client = Client(self.APIKEY, self.APISECRET, tld='com')

    def add_order(self, symbol: str, in_coin=False, rsi_down=30.0, rsi_up=70.0):
        new_order = OrderData(symbol, in_coin, rsi_down, rsi_up)
        self.ORDERS.append(new_order)

    def delete_order(self, order: OrderData):
        self.ORDERS.remove(order)
