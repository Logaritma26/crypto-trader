import requests
import json
from OrderData import OrderData
import User
from app import config


# 'AVAX/BUSD'

class MarketTracker:

    RSI_URL = config.TAAPI_API_BASE_URL + 'rsi'

    UPPER_VALUES = {}
    LOWER_VALUES = {}
    RSI_PARAMETERS = {}

    API_LIST = {}
    USERS = []

    def add_user(self, user: User):
        self.USERS.append(user)

        for order in user.ORDERS:
            api = order.SYMBOL.get("api")
            if api in self.API_LIST:
                self.API_LIST.get(api).append(order)
            else:
                self.API_LIST.update({api: [order]})
                parameter = {
                    'secret': config.TAAPI_API_SECRET,
                    'exchange': 'binance',
                    'symbol': api,
                    'interval': '1h'
                }
                self.RSI_PARAMETERS.update({api: parameter})

            if api in self.UPPER_VALUES:
                if self.UPPER_VALUES.get(api) > order.RSI_UP:
                    self.UPPER_VALUES.update({api: order.RSI_UP})
            else:
                self.UPPER_VALUES.update({api: order.RSI_UP})

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
                #get rsi
                rsi = res_object['value']
                print("this will execute")

                if rsi is not None:
                    if rsi >= self.UPPER_VALUES.get(parameter['symbol']):
                        #sell
                        pass

                    if rsi <= self.LOWER_VALUES.get(parameter['symbol']):
                        #buy
                        pass
        else:
            print("status warning ! {}".format(response.status_code))



    def fill_orders(self):
        pass
