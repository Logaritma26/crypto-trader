from binance.client import Client
from binance.enums import *
from order_data import OrderData


def process_after_sell(order: OrderData):
    temp_fiat = order.COIN_PRICE * order.COIN_COUNT
    order.FIAT_COUNT += temp_fiat
    order.COIN_COUNT = 0.0
    order.IN_COIN = False


def process_after_buy(order: OrderData):
    total_price = order.QUANTITY * order.COIN_PRICE
    order.FIAT_COUNT -= total_price
    order.COIN_COUNT = order.QUANTITY
    order.QUANTITY = 0.0
    order.IN_COIN = True


def calculate_quantity(order: OrderData):
    temp_quantity = order.FIAT_COUNT / order.COIN_PRICE
    temp_quantity = round(temp_quantity, 2)
    order.QUANTITY = temp_quantity


class User:
    APIKEY: str
    APISECRET: str
    USER_UID: str
    client: Client

    ORDERS = []

    def __init__(self, api_key, api_secret, server_uid):
        self.APIKEY = api_key
        self.APISECRET = api_secret
        self.client = Client(self.APIKEY, self.APISECRET, tld='com')
        self.USER_UID = server_uid

    def add_order(self, symbol: str, symbol_gen: str, symbol_api: str, interval: str = "1h", in_coin=False,
                  rsi_down=30.0, rsi_up=70.0,
                  coin_count=0.0,
                  fiat_count=0.0):

        new_order = OrderData(self.USER_UID, symbol, symbol_gen, symbol_api, interval, in_coin, rsi_down, rsi_up,
                              coin_count,
                              fiat_count)
        self.ORDERS.append(new_order)

    def delete_order(self, order: OrderData):
        self.ORDERS.remove(order)

    def get_price(self, order: OrderData):
        try:
            exchange_info = self.client.get_symbol_ticker(symbol=order.SYMBOL_GLOBAL)
            order.COIN_PRICE = float(exchange_info['price'])
            print("price : {}".format(order.COIN_PRICE))
            return True
        except Exception as e:
            print("Getting price details failed ! -> {}".format(e))
            return False

    def order(self, side, order: OrderData, order_type=ORDER_TYPE_MARKET):
        try:
            print("Sending order . . .")
            order = self.client.create_order(symbol=order.SYMBOL_GLOBAL, side=side, type=order_type,
                                             quantity=order.QUANTITY)
            print("Order success : {}".format(order))
        except Exception as e:
            print("An exception occurred for order -> {}".format(e))
            return False

        return True

    def process_order(self, side, order: OrderData):

        if self.get_price(order):
            if side == SIDE_BUY:
                calculate_quantity(order)
                order_success = self.order(side=side, order=order)
                if order_success:
                    process_after_buy(order)
                    order.send_update_process(side)
                    return True
                else:
                    return False

            elif side == SIDE_SELL:
                order_success = self.order(side=side, order=order)
                if order_success:
                    count = order.COIN_COUNT
                    process_after_sell(order)
                    order.send_update_process(side, count)
                    return True
                else:
                    return False

            else:
                print("Unknown side - warning !")
                return False
