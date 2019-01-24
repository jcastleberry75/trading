import robin_client
import numpy
import logging


class Processor:

    def __init__(self, token=None,
                 symbol=None,
                 instrument=None,
                 message_price=None,
                 quote_price=None,
                 buying_power=None,
                 account_url=None):

        self.token = token
        self.symbol = symbol
        self.instrument = instrument
        self.message_price = message_price
        self.quote_price = quote_price
        self.buying_power = buying_power
        self.account_url = account_url

    def calc_buy(self, symbol,  instrument,  message_price, quote_price, buying_power, account_url):
        logging.info('ORDER-PROCESSOR: token=' + token)
        logging.info('ORDER-PROCESSOR: symbol=' + symbol)
        logging.info('ORDER-PROCESSOR: instrument=' + str(instrument))
        logging.info('ORDER-PROCESSOR: message_price=' + str(message_price))
        logging.info('ORDER-PROCESSOR: quote_price=' + str(quote_price))
        logging.info('ORDER-PROCESSOR: buying_power=' + str(buying_power))
        logging.info('ORDER-PROCESSOR: account=' + str(account_url))
        with open('order.txt', 'w') as f:
            robinhood = robin_client.RobinClient()
            msg_floats = []
            num_msg_prices = len(message_price)
            if num_msg_prices is 1:
                final_msg_price = message_price[0]
                logging.info('ORDER-PROCESSOR: Final Price Parsed from Message: ' + str(final_msg_price))
            else:
                for n in message_price:
                    flt = float(n)
                    msg_floats.append(flt)
                closest_float = min(msg_floats, key=lambda x: abs(x - float(quote_price)))
                final_msg_price = closest_float
                logging.info('ORDER-PROCESSOR: Final Price Parsed from Message: ' + str(final_msg_price))

            bid_price = float(quote_price)
            msg_price = float(final_msg_price)
            diff = msg_price * 100 / bid_price
            percent = float(100.000 - diff)
            logging.info('Difference between Bid and Message Price: ' + str(percent))

            def calc_shares(funds_amt, price):
                    print()
                    if float(price) > float(funds_amt):
                        return None
                    else:
                        ten_percent = funds_amt / 10
                        z = float(ten_percent) / float(price)
                        x = numpy.floor(z)
                        return int(x)

            if percent <= (-3.5):
                buy_pow = buying_power
                logging.info('Buying Power: ' + str(buy_pow))

                if float(quote_price) > float(buying_power):
                    logging.info("Bid Price of " + quote_price + " is greater than " + str(float(buying_power)))
                else:

                    shares_to_buy = calc_shares(float(buying_power), float(bid_price))
                    logging.info('Shares to Buy: ' + str(shares_to_buy))
                    order_result = robinhood.buy_order(account_url=account_url,
                                                       symbol=symbol,
                                                       instrument=instrument,
                                                       bid_price=quote_price,
                                                       shares_num=str(shares_to_buy))
                    logging.info(order_result)
                    return order_result
            else:
                pass
