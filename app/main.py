import websocket, json, pprint, numpy
import config
import operations
from operations import ClientOperations
from binance.enums import *
import requests
import schedule
import time


SYMBOL = 'AVAXBUSD'
LAST_DOWN = 100.0
LAST_UP = 0.0

IN_COIN = True

RSI_DOWN = 30
RSI_UP = 70
RSI_VALUE = 50
CONTINUE = True

Operations = operations.ClientOperations()


rsi_endpoint = config.TAAPI_API_BASE_URL + 'rsi'

rsi_parameters = {
    'secret': config.TAAPI_API_SECRET,
    'exchange': 'binance',
    'symbol': 'AVAX/BUSD',
    'interval': '1h'
    } 


def get_rsi_value():
    global RSI_VALUE
    response = requests.get(url = rsi_endpoint, params = rsi_parameters)
    rsi = response.json()['value']
    if rsi != RSI_VALUE:
        RSI_VALUE = rsi 
        print("rsi value : {}".format(RSI_VALUE))
     
    status = response.status_code
    if(status != 200):
        print("status warning ! {}".format(status))
    

def value_up():
    print("Value Up called !")
    global LAST_UP
    global CONTINUE

    if IN_COIN:
    
        order_success = Operations.process_order(SIDE_SELL, SYMBOL) 

        if order_success:
            print("Selling price : {}".format(Operations.COIN_PRICE))
            print("RSI sell value : {}".format(RSI_VALUE))
        else:
            CONTINUE = False

    if RSI_VALUE > LAST_UP:
        print("RSI value : {}".format(RSI_VALUE))
        LAST_UP = RSI_VALUE
    
    
def value_down():
    print("Value Down called !")
    global LAST_DOWN
    global CONTINUE 

    if not IN_COIN:
        
        order_success = Operations.process_order(SIDE_BUY, SYMBOL)

        if order_success:
            print("Buying price : {}".format(Operations.COIN_PRICE))
            print("RSI buy value : {}".format(RSI_VALUE))
        else:
            CONTINUE = False

    if RSI_VALUE < LAST_DOWN:
        print("RSI value : {}".format(RSI_VALUE))
        LAST_DOWN = RSI_VALUE
    


def process():

    get_rsi_value()

    if RSI_VALUE > RSI_UP:
        value_up()
    elif RSI_VALUE < RSI_DOWN:
        value_down()
    else:
        global LAST_UP
        global LAST_DOWN
        LAST_DOWN = 100.0
        LAST_UP = 0.0



schedule.every(2).seconds.do(process)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)

while CONTINUE:
    schedule.run_pending()
    time.sleep(1)