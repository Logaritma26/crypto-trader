import requests
from binance.enums import *
import userData
import config


def get_price(user: userData.User, symbol_global: str):
    try:
        exchange_info = user.client.get_symbol_ticker(symbol=symbol_global)
        price = float(exchange_info['price'])
        return price, True

    except Exception as e:
        print("Getting price details failed ! -> {}".format(e))
        return 0.0, False


class MarketTracker:
    RSI_URL = config.TAAPI_API_BASE_URL + 'rsi'

    UPPER_VALUES = {}  # symbol_api -> order.RSI_UP
    LOWER_VALUES = {}  # symbol_api -> order.RSI_DOWN
    RSI_PARAMETERS = {}  # symbol_api -> parameter

    ORDER_LIST = {}  # symbol_api -> [order]
    ORDER_TO_USER = {}  # order -> user
    USERS = []

    RSI = 0.0

    def add_user(self, user: userData):
        self.USERS.append(user)
        for order in user.ORDERS:
            self.ORDER_TO_USER[order] = user
            api = order.SYMBOL_API
            if api in self.ORDER_LIST:
                self.ORDER_LIST.get(api).append(order)
            else:
                self.ORDER_LIST.update({api: [order]})
                parameter = {
                    'secret': config.TAAPI_API_SECRET,
                    'exchange': 'binance',
                    'symbol': api,
                    'interval': order.INTERVAL
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

    def update_orders_short(self):
        for symbol in self.ORDER_LIST:
            for order in self.ORDER_LIST[symbol]:
                user = self.ORDER_TO_USER.get(order)
                price, res = get_price(user, order.SYMBOL_GLOBAL)
                if res:
                    order.update_price(price)

    def operate_rsi(self):
        for parameter in self.RSI_PARAMETERS:
            self.get_rsi_value(self.RSI_PARAMETERS[parameter])

    def get_rsi_value(self, parameter):

        try:
            response = requests.get(url=self.RSI_URL, params=parameter)
            res_json = response.json()
            # res_object = json.loads(response)
        except ValueError as e:
            print("Error !")
            return False

        if response.status_code == 200:

            if "value" in res_json:
                rsi = res_json['value']
                # print("RSI : {}".format(rsi))
                self.RSI = rsi

                # get price
                #order = self.ORDER_LIST[parameter['symbol']][0]
                #user = self.ORDER_TO_USER.get(order)
                #price, res = get_price(user, order.SYMBOL['global'])

                if rsi is not None:

                    self.update_order_rsi(parameter['symbol'], rsi)
                    #if res:
                     #   self.update(symbol=parameter['symbol'], rsi=rsi, coin_price=price)

                    if self.UPPER_VALUES.get(parameter['symbol']) is not None:
                        if rsi >= self.UPPER_VALUES.get(parameter['symbol']):
                            self.fill_sell_orders(parameter['symbol'], rsi)

                    if self.LOWER_VALUES.get(parameter['symbol']) is not None:
                        if rsi <= self.LOWER_VALUES.get(parameter['symbol']):
                            self.fill_buy_orders(parameter['symbol'], rsi)

        else:
            print("status warning ! {}".format(response.status_code))

    def update(self, symbol: str, rsi: float, coin_price: float):
        for order in self.ORDER_LIST.get(symbol):
            order.update_data(rsi, coin_price)

    def update_order_rsi(self, symbol: str, rsi: float):
        for order in self.ORDER_LIST.get(symbol):
            order.RSI_VALUE = rsi

    def fill_sell_orders(self, symbol: str, rsi: float):
        sell: bool = False

        for order in self.ORDER_LIST.get(symbol):
            if order.IN_COIN and order.RSI_UP <= rsi:
                user: userData.User = self.ORDER_TO_USER.get(order)
                success: bool = user.process_order(side=SIDE_SELL, order=order)
                if success:
                    sell = True
                else:
                    print("An order failed !")

        if sell:
            self.set_uppers(symbol)

    def set_uppers(self, symbol: str):
        value: float = 100.0
        for order in self.ORDER_LIST.get(symbol):
            if order.IN_COIN and order.RSI_UP < value:
                value = order.RSI_UP

        self.UPPER_VALUES.update({symbol: value})

    def fill_buy_orders(self, symbol: str, rsi: float):
        buy: bool = False

        for order in self.ORDER_LIST.get(symbol):
            if not order.IN_COIN:
                if order.RSI_DOWN >= rsi:
                    user: userData.User = self.ORDER_TO_USER.get(order)
                    success: bool = user.process_order(side=SIDE_BUY, order=order)
                    if success:
                        buy = True
                    else:
                        print("An order failed !")

        if buy:
            self.set_lowers(symbol)

    def set_lowers(self, symbol: str):
        value: float = 100.0
        for order in self.ORDER_LIST.get(symbol):
            if not order.IN_COIN:
                if order.RSI_DOWN > value:
                    value = order.RSI_DOWN

        self.LOWER_VALUES.update({symbol: value})
