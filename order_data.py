import requests
import config


class OrderData:
    UPDATE_PAIR_SHORT_URL = "/update_pair_short"
    UPDATE_PROCESS_URL = "/process_update"

    INTERVAL: str

    USER_UID: str

    SYMBOL_GLOBAL: str
    SYMBOL_API: str
    SYMBOL: str

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

    def __init__(self, user_uid: str, symbol: str, symbol_gen: str, symbol_api: str, interval: str = "1h", in_coin=False, rsi_down=30.0,
                 rsi_up=70.0,
                 coin_count=0.0,
                 fiat_count=0.0):
        self.USER_UID = user_uid
        self.SYMBOL = symbol
        self.SYMBOL_GLOBAL = symbol_gen
        self.SYMBOL_API = symbol_api
        self.INTERVAL = interval
        self.IN_COIN = in_coin
        self.RSI_DOWN = rsi_down
        self.RSI_UP = rsi_up
        self.COIN_COUNT = coin_count
        self.FIAT_COUNT = fiat_count

    def update_price(self, price: float):
        self.COIN_PRICE = price
        self.send_update_data()

    def send_update_data(self):
        url = config.CORE_FUNCTIONS + self.UPDATE_PAIR_SHORT_URL

        data = {
            'user_id': self.USER_UID,
            'symbol': self.SYMBOL,
            'symbol_api': self.SYMBOL_API,
            'symbol_global': self.SYMBOL_GLOBAL,
            'rsi_down': self.RSI_DOWN,
            'rsi_up': self.RSI_UP,
            'rsi': self.RSI_VALUE,
            'coin_count': self.COIN_COUNT,
            'fiat_count': self.FIAT_COUNT,
            'coin_price': self.COIN_PRICE,
            'in_coin': self.IN_COIN
        }

        try:
            res = requests.post(url=url, data=data)
            if res.status_code != 201:
                print("Status code warning: {}".format(res.status_code))
        except Exception as e:
            print("Exception : {}".format(e))

    def send_update_process(self, side: str, count: float = 0.0):
        url = config.CORE_FUNCTIONS + self.UPDATE_PROCESS_URL

        message: str
        if side == 'SELL':
            message = 'Sell order executed for {} {}'.format(count, self.SYMBOL)
        elif side == 'BUY':
            message = 'Buy order executed for {} {}'.format(self.COIN_COUNT, self.SYMBOL)

        data = {
            'user_id': self.USER_UID,
            'symbol': self.SYMBOL,
            'symbol_api': self.SYMBOL_API,
            'symbol_global': self.SYMBOL_GLOBAL,
            'rsi_down': self.RSI_DOWN,
            'rsi_up': self.RSI_UP,
            'rsi': self.RSI_VALUE,
            'coin_count': self.COIN_COUNT,
            'fiat_count': self.FIAT_COUNT,
            'coin_price': self.COIN_PRICE,
            'in_coin': self.IN_COIN,
            'title': side + " order executed !",
            'message': message
        }
        try:
            res = requests.post(url=url, data=data)
            if res.status_code != 201:
                print("Status code warning: {}".format(res.status_code))
        except Exception as e:
            print("Exception : {}".format(e))
