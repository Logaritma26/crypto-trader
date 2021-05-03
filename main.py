from userData import User
from market_tracker import MarketTracker
import config
import schedule
import time

market = MarketTracker()

user1 = User(config.API_KEY, config.API_SECRET, config.USER1_UID)
user1.add_order(symbol='BNB', symbol_gen="BNBBUSD", symbol_api="BNB/BUSD", rsi_down=40, in_coin=True, coin_count=0.52, interval="15m",
                fiat_count=300)
user1.add_order(symbol='CAKE', symbol_gen="CAKEBUSD", symbol_api="CAKE/BUSD", interval="15m", rsi_down=26, rsi_up=71,
                fiat_count=100)

market.add_user(user1)


def process_scheduled():
    print("RSI : {}".format(market.RSI))


def check_rsi():
    market.operate_rsi()


def update_short():
    market.update_orders_short()


schedule.every(3).seconds.do(check_rsi)
schedule.every(15).seconds.do(update_short)
schedule.every(5).minutes.do(process_scheduled)
# schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
