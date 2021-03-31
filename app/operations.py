
import config
from binance.client import Client
import math
from binance.enums import *




class ClientOperations:

    COIN_COUNT = 1.27
    FIAT_COUNT = 0.0
    QUANTITY = 0.0   
    COIN_PRICE = 1000.0



    client = Client(config.API_KEY, config.API_SECRET, tld='com')


    def getprice(self):
        exchange_info = self.client.get_symbol_ticker(symbol = config.SYMBOL)
        self.COIN_PRICE = exchange_info['price']
        print("price : {}".format(self.COIN_PRICE))


    def calculate_after_sell(self):
        temp_fiat = self.COIN_PRICE * self.COIN_COUNT
        self.FIAT_COUNT += temp_fiat
        self.COIN_COUNT = 0.0


    def calculate_after_buy(self):
        total_price = self.QUANTITY * self.COIN_PRICE
        self.FIAT_COUNT -= total_price
        self.COIN_COUNT = self.QUANTITY
        self.QUANTITY = 0.0


    def calculate_quantity(self):
        temp_quantity = self.FIAT_COUNT / self.COIN_PRICE
        temp_quantity = round(temp_quantity, 2)
        self.QUANTITY = temp_quantity


    def order(self, side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print("Sending order . . .")
            order = self.client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            print("Order success : {}".format(order))
        except Exception as e:
            print("An exception occured -> {}".format(e))
            return False

        return True


    def process_order(self, side, symbol):
        self.getprice()

        if side == SIDE_BUY:   
            self.calculate_quantity()
            order_success = self.order(side=side, quantity=self.QUANTITY, symbol=symbol) 
            if order_success:
                self.calculate_after_buy()
                return True
            else:
                return False

        elif side == SIDE_SELL:
            order_success = self.order(side=side, quantity=self.COIN_COUNT, symbol=symbol)
            if order_success:
                self.calculate_after_sell()
                return True
            else:
                return False

        else: 
            print("Unknown side - warning !")
            return False


