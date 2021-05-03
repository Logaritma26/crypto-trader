from classes.User import User
from classes.MarketTracker import MarketTracker
import config
import schedule
import time


market = MarketTracker()

user1 = User(config.API_KEY, config.API_SECRET)
user1.add_order("AVAXBUSD", "AVAX/BUSD", rsi_down=55, fiat_count=20.0)

market.add_user(user1)


def process():
    market.operate_rsi()


schedule.every(3).seconds.do(process)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
