from User import User
from binance.enums import *


class OrderData:
    SYMBOL: dict = {}

    RSI_DOWN: float = 30.0
    RSI_UP: float = 70.0
    RSI_VALUE: float = 50.0

    LAST_DOWN: float = 100.0
    LAST_UP: float = 0.0

    COIN_COUNT: float = 0.0
    FIAT_COUNT: float = 0.0

    QUANTITY: float = 0.0
    COIN_PRICE: float = -1.0
    IN_COIN: bool = False

    CONTINUE: bool = True
    USER: User

    def __init__(self, user: User, symbol_gen: str, symbol_api: str, in_coin=False, rsi_down=30.0, rsi_up=70.0,
                 coin_count=0.0,
                 fiat_count=0.0):
        self.USER = user
        self.SYMBOL["global"] = symbol_gen
        self.SYMBOL["api"] = symbol_api
        self.IN_COIN = in_coin
        self.RSI_DOWN = rsi_down
        self.RSI_UP = rsi_up
        self.COIN_COUNT = coin_count
        self.FIAT_COUNT = fiat_count

    def get_price(self):
        exchange_info = self.USER.client.get_symbol_ticker(symbol=self.SYMBOL["global"])
        self.COIN_PRICE = exchange_info['price']
        print("price : {}".format(self.COIN_PRICE))

    def calculate_after_sell(self):
        temp_fiat = self.COIN_PRICE * self.COIN_COUNT
        self.FIAT_COUNT += temp_fiat
        self.COIN_COUNT = 0.0
        self.IN_COIN = False

    def calculate_after_buy(self):
        total_price = self.QUANTITY * self.COIN_PRICE
        self.FIAT_COUNT -= total_price
        self.COIN_COUNT = self.QUANTITY
        self.QUANTITY = 0.0
        self.IN_COIN = True

    def calculate_quantity(self):
        temp_quantity = self.FIAT_COUNT / self.COIN_PRICE
        temp_quantity = round(temp_quantity, 2)
        self.QUANTITY = temp_quantity

    def order(self, side, quantity, order_type=ORDER_TYPE_MARKET):
        try:
            print("Sending order . . .")
            order = self.USER.client.create_order(symbol=self.SYMBOL["global"], side=side, type=order_type, quantity=quantity)
            print("Order success : {}".format(order))
        except Exception as e:
            print("An exception occured -> {}".format(e))
            return False

        return True

    def process_order(self, side):
        self.get_price()

        if side == SIDE_BUY:
            self.calculate_quantity()
            order_success = self.order(side=side, quantity=self.QUANTITY)
            if order_success:
                self.calculate_after_buy()
                return True
            else:
                return False

        elif side == SIDE_SELL:
            order_success = self.order(side=side, quantity=self.COIN_COUNT)
            if order_success:
                self.calculate_after_sell()
                return True
            else:
                return False

        else:
            print("Unknown side - warning !")
            return False
