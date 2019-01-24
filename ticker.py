import robin_client
import logging
import schedule
from time import sleep

robinhood = robin_client.RobinClient()

logging.basicConfig(filename='ticker.log', level=logging.INFO, format='%(asctime)s %(message)s')

sym = 'BPMX'

def watch_price():
    logging.info('########## QUOTE CALL FOR ' + sym + ' ##########')
    stk_data = robinhood.get_instrument_quote(symbol=sym)
    price = stk_data[0]['bid_price']
    logging.info('SYMBOL: ' + sym + ' BID PRICE: ' + str(price))


schedule.every(2).seconds.do(watch_price)
while True:
    sleep(1)
    schedule.run_pending()
