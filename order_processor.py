import robin_client
import numpy
import logging




class Processor:

    def __init__(self, token=None, symbol=None, instrument=None, message_price=None, quote_price=None):
        self.token = token
        self.symbol = symbol
        self.message_price = message_price
        self.quote_price = quote_price
        self.instrument = instrument

    def calc_buy(self, token, symbol,  instrument,  message_price, quote_price):
        log_format = '%(asctime)-s [%(levelname)-s] (%(threadName)-s)  %(message)s'
        logging.basicConfig(format=log_format, filename='calc.log', level=logging.DEBUG)
        with open('order.txt', 'w') as f:
            robinhood = robin_client.RobinClient()
            msg_floats = []
            num_msg_prices = len(message_price)
            if num_msg_prices is 1:
                final_msg_price = message_price[0]

            else:
                for n in message_price:
                    flt = float(n)
                    msg_floats.append(flt)
                closest_float = min(msg_floats, key=lambda x: abs(x - float(quote_price)))
                final_msg_price = closest_float

            bid_price = float(quote_price)
            diff = float(final_msg_price) * 100 / bid_price
            percent = float(100.000 - diff)
            if percent <= (-3.5):
                buying_pwr = robinhood.get_buying_power(token)
                logging.info(str(buying_pwr))
                funds = float(buying_pwr[0]) / 10
                if float(quote_price) > float(funds):
                    pass
                else:
                    acct = buying_pwr[1]
                    logging.info(acct)
                    share_div = float(funds) / float(quote_price)
                    logging.info(str(share_div))
                    shares_to_buy = numpy.floor(share_div)
                    logging.info(str(shares_to_buy))
                    order_result = robinhood.buy_order(token=token,
                                                       account=acct,
                                                       symbol=symbol,
                                                       instrument=instrument,
                                                       bid_price=quote_price,
                                                       shares_num=shares_to_buy)
                    logging.info(order_result)

                    f.write(order_result)
                    return order_result
            else:
                pass








