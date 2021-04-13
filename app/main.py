import json, pprint
from binance.enums import *
import requests
import schedule
import time





def process():
    pass


schedule.every(2).seconds.do(process)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)