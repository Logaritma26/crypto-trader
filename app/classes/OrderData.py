
class OrderData:
    SYMBOL: str = "NONE"

    RSI_DOWN: float = 30.0
    RSI_UP: float = 70.0
    RSI_VALUE: float = 50.0
    LAST_DOWN: float = 100.0
    LAST_UP: float = 0.0

    QUANTITY: float = 0.0
    COIN_PRICE: float = -1.0
    IN_COIN: bool = False

    CONTINUE: bool = True

    def __init__(self, symbol, in_coin=False, rsi_down=30.0, rsi_up=70.0):
        self.SYMBOL = symbol
        self.IN_COIN = in_coin
        self.RSI_DOWN = rsi_down
        self.RSI_UP = rsi_up
