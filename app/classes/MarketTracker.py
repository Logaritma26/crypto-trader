import requests
import json
from OrderData import OrderData
from binance.enums import *
import User
from app import config


# 'AVAX/BUSD'

class MarketTracker:
    RSI_URL = config.TAAPI_API_BASE_URL + 'rsi'

    UPPER_VALUES = {}
    LOWER_VALUES = {}
    RSI_PARAMETERS = {}

    ORDER_LIST = {}
    USERS = []

    def add_user(self, user: User):
        self.USERS.append(user)

        for order in user.ORDERS:
            api = order.SYMBOL.get("api")
            if api in self.ORDER_LIST:
                self.ORDER_LIST.get(api).append(order)
            else:
                self.ORDER_LIST.update({api: [order]})
                parameter = {
                    'secret': config.TAAPI_API_SECRET,
                    'exchange': 'binance',
                    'symbol': api,
                    'interval': '1h'
                }
                self.RSI_PARAMETERS.update({api: parameter})

            if order.IN_COIN:
                if api in self.UPPER_VALUES:
                    if self.UPPER_VALUES.get(api) > order.RSI_UP:
                        self.UPPER_VALUES.update({api: order.RSI_UP})
                else:
                    self.UPPER_VALUES.update({api: order.RSI_UP})
            else:
                if api in self.LOWER_VALUES:
                    if self.LOWER_VALUES.get(api) < order.RSI_DOWN:
                        self.LOWER_VALUES.update({api: order.RSI_DOWN})
                else:
                    self.LOWER_VALUES.update({api: order.RSI_DOWN})

    def get_rsi_value(self, parameter):

        try:
            response = requests.get(url=self.RSI_URL, params=parameter)
            res_json = response.json()
            res_object = json.loads(res_json)
        except ValueError as e:
            print("Error !")
            return False

        if response.status_code == 200:

            if "value" in res_object:
                # get rsi
                rsi = res_object['value']
                print("this will execute")

                if rsi is not None:
                    if rsi >= self.UPPER_VALUES.get(parameter['symbol']):
                        self.fill_sell_orders(parameter['symbol'], rsi)

                    if rsi <= self.LOWER_VALUES.get(parameter['symbol']):
                        self.fill_buy_orders(parameter['symbol'], rsi)

        else:
            print("status warning ! {}".format(response.status_code))

    def fill_sell_orders(self, symbol: str, rsi: float):
        sell: bool = False

        for order in self.ORDER_LIST.get(symbol):
            if order.IN_COIN and order.RSI_UP <= rsi:
                success: bool = order.process_order(SIDE_SELL)
                if success:
                    sell = True
                else:
                    print("An order failed !")

        if sell:
            self.set_uppers(symbol)

    def set_uppers(self, symbol: str):
        value: float = 100.0
        for order in self.ORDER_LIST.get(symbol):
            if order.RSI_UP < value:
                value = order.RSI_UP

        self.UPPER_VALUES.update({symbol: value})

    def fill_buy_orders(self, symbol: str, rsi: float):
        buy: bool = False

        for order in self.ORDER_LIST.get(symbol):
            if not order.IN_COIN:
                if order.RSI_DOWN >= rsi:
                    success: bool = order.process_order(SIDE_BUY)
                    if success:
                        buy = True
                    else:
                        print("An order failed !")

        if buy:
            self.set_lowers(symbol)

    def set_lowers(self, symbol: str):
        value: float = 100.0
        for order in self.ORDER_LIST.get(symbol):
            if order.RSI_DOWN > value:
                value = order.RSI_DOWN

        self.LOWER_VALUES.update({symbol: value})
