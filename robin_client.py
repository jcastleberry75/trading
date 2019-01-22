import requests
import json
import schedule
import numpy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
import random
from time import sleep


class RobinClient:

    def __init__(self,
                 user_name=None,
                 password=None,
                 account=None,
                 token=None,
                 symbol=None,
                 bid_price=None,
                 shares_num=None,
                 instrument=None):

        self.user_name = user_name
        self.password = password
        self.token = token
        self.symbol = symbol
        self.price = bid_price
        self.shares_num = shares_num
        self.instrument = instrument
        self.account_url = account

    def robinhood_login(self, user_name, password):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # Connects to The Robinhood to log in and get auth token
        url = "https://api.robinhood.com/oauth2/token/"
        data = {"client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
                "expires_in": "86400",
                "grant_type": "password",
                "password": password,
                "scope": "internal",
                "username": user_name}

        auth_req = requests.post(url, data=data, verify=False)

        json_data = auth_req.json()
        token = (json_data['access_token'])
        return token

    def get_instrument_quote(self, token, symbol):
        params = {'symbols': symbol}
        url = "https://api.robinhood.com/quotes/"
        auth_str = 'Bearer ' + token
        headers = {'Authorization': auth_str}
        quote = requests.get(url, headers=headers, params=params, verify=False)
        quote_result = (quote.json())
        quote_data = (quote_result['results'])
        return quote_data

    def get_buying_power(self, token):
        url = "https://api.robinhood.com/accounts/"
        auth_str = 'Bearer ' + token
        headers = {'Authorization': auth_str}
        resp_data = requests.get(url, headers=headers, verify=False)

        acct_info = (resp_data.json())
        res = acct_info['results'][0]
        buying_power = res['buying_power']
        act_url = res['url']
        return (buying_power, act_url)

    def buy_order(self, token, account, symbol, instrument,  bid_price, shares_num):
        data = {"account": account,
                "extended_hours": "false",
                "instrument": {
                    "url": instrument,
                    "symbol": symbol},

                "price": bid_price,
                "quantity": shares_num,
                "side": "buy",
                "time_in_force": "gtd",
                "trigger": "immediate",
                "type": "market"}
        url = "https://api.robinhood.com/orders"
        auth_str = 'Bearer ' + token
        headers = {"Accept": "*/*",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
                   "Authorization": auth_str, "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)",
                   "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        print(headers)
        order_req = requests.post(url, headers=headers, data=data, verify=False, timeout=6)
        with open('request_order.txt', 'w') as f:
            f.write(str(order_req.headers) + "\n")
            f.write(str(order_req.status_code + "\n"))
            f.write(str(order_req.text + "\n"))
        return order_req.text()





#
#
# def get_account_info(session_token):
#     print()
#     print('########## Account Info ##########')
#     logging.info('########## Account Info ##########')
#     url = "https://api.robinhood.com/accounts/"
#     auth_str = 'Bearer ' + session_token
#     headers = {'Authorization': auth_str}
#     resp_data = requests.get(url, headers=headers, verify=False)
#     logging.debug(resp_data)
#     acct_info = (resp_data.json())
#     res = acct_info['results'][0]
#     for key, value in res.items():
#         print(key, value)
#         data = (key, value)
#         logging.info(str(data))
#     return res
#
#
# acct_data = get_account_info(session_token)
# print(acct_data)
# global buying_power
# buying_power = (acct_data['buying_power'])
# print()
# print('########## Current Buying Power ##########')
# print(buying_power)
# logging.info('########## Current Buying Power ##########')
# logging.info(buying_power)
#
# global account
# account = acct_data['url']
#
# sym_to_trade = "BPMX"
# def get_instrument_quote(session_token, stk_sym):
#     print()
#     params = {'symbols': stk_sym}
#     url = "https://api.robinhood.com/quotes/"
#     headers = {'Authorization': session_token}
#     quote = requests.get(url, headers=headers, params=params, verify=False)
#     logging.debug(quote)
#     quote_result = (quote.json())
#     quote_data = (quote_result['results'])
#     print('########## Quote Data: ' + stk_sym + ' ##########X')
#     logging.info('########## Quote Data: ' + stk_sym + ' ##########')
#     for key, value in quote_data[0].items():
#         print(key, value)
#         data = (key, value)
#         logging.info(str(data))
#     return quote_data
#
#
# stock_quote = get_instrument_quote(session_token, sym_to_trade)
# global bid_price
# bid_price = stock_quote[0]['bid_price']
# global instrument
# instrument = stock_quote[0]['instrument']
# print()
# print('Last Trade Price: ' + bid_price)
# logging.info('Last Trade Price: ' + bid_price)

# STOCK_ORDER_ENDPOINT = 'https://api.robinhood.com/orders/'
# STOCK_ORDER_CANCEL_ENDPOINT = 'https://api.robinhood.com/orders/%s/cancel/'
#
# def get_order(request, order_id, timeout=5):
#     url = '%s%s/' % (STOCK_ORDER_ENDPOINT, order_id)
#     res = request.get(url, timeout=timeout)
#     res.raise_for_status()
#     res = res.json()
#     return res
#
# def place_order(tk,
#                 account,
#                 instrument,
#                 symbol,
#                 price,
#                 quantity,
#                 side,
#                 order_type='market',
#                 time_in_force='gfd',
#                 trigger='immediate',
#                 timeout=5):
#     order = {
#         'account': account,
#         'instrument': instrument,
#         'symbol': symbol,
#         'price': price,
#         'quantity': quantity,
#         'side': side,
#         'type': order_type,
#         'time_in_force': time_in_force,
#         'trigger': trigger
#     }
#     auth_str = 'Bearer ' + tk
#     headers = {"Accept": "*/*",
#                "Accept-Encoding": "gzip, deflate",
#                "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
#                "Authorization": auth_str, "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)",
#                }
#
#     res = requests.post(STOCK_ORDER_ENDPOINT, headers=headers, json=order, timeout=timeout)
#     res.raise_for_status()
#     order_res = res.json()
#     logging.info(str(order_res))
#
#
# print()
# print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
# print()
#
# def calc_margin(sym, buy_price):
#     logging.info('SYMBOL: ' + sym)
#     price = float(buy_price)
#     quote = get_instrument_quote(session_token, sym)
#     current_bid_price = quote[0]['bid_price']
#     cur_price = float(current_bid_price)
#     print()
#     print("Buy Price: " + str(price)[0:6])
#     logging.info("Buy Price: " + str(price)[0:6])
#     print("Current Price: " + str(cur_price)[0:6])
#     logging.info("Current Price: " + str(cur_price)[0:6])
#     diff = price * 100 / cur_price
#     percent = float(100.000 - diff)
#     print("Percent Difference: " + str(percent)[0:5])
#     logging.info("Percent Difference: " + str(percent)[0:5])
#     if percent <= (-3.5):
#         print("Percent is less than -3.5% | SELLING AT LOSS")
#         logging.info("Percent is less than -3.5% | SELLING AT LOSS")
#     elif percent >= (-3.5) and percent <= int(5):
#         print("Percent Between 5% and -3.5% | WAITING")
#         logging.info("Percent Between 5% and -3.5% | WAITING")
#     elif percent >= (5.0):
#         print("Percent is more than -5.0% | SELLING AT GAIN")
#         logging.info("Percent is more than -5.0% | SELLING AT GAIN")
#

# def timed_calc():
#     logging.info('XXXXXXXXXX   Call for Quote   XXXXXXXXXX')
#     rand_num = random.uniform(.107000, .12)
#     logging.info('Random Bought at Price: ' + str(rand_num))
#     print('Random Price: ' + str(rand_num))
#     calc_margin(sym_to_trade, rand_num)
#
# timed_calc()
#
# print('Buy Price: ' + str(buy_price))
# print('Current Price: ') + str(current_bid_price)
# price_diff_per = float(price) * float(100.00) / float(current_bid_price)
# print(price_diff_per)
#
# logging.info('Placing Order')
# place_order(session_token, "https://api.robinhood.com/accounts/858649452/", instrument, sym_to_trade, bid_price, '1', 'buy')
# place_order(session_token, "https://api.robinhood.com/accounts/858649452/", instrument, sym_to_trade, bid_price, '1', 'sell')
#
# end_time = datetime.now()
# finish_time = str(end_time - start_time)
# logging.info('Time to Obtain Price, Acct. Info, and Order: ' + finish_time[:-3])
# print(finish_time[:-3])
    #def order(tk, sym):
    #     print('########## Placing Order for ' + sym + ' ##########')
    #     logging.info('########## Placing Order for ' + sym + ' ##########')
    #
    #     def get_funds(buying_power):
    #         return float(buying_power) / 10
    #     funds = get_funds(buying_power)
    #     print(funds)
    #     logging.info('Funds for Order based on 10% of Buying Power: ' + str(funds))
    #
    #     def calc_shares(funds_amt, price):
    #         print(funds_amt)
    #         print(price)
    #         logging.info('Price of Stock: ' + price)
    #         print()
    #         if float(price) > float(funds_amt):
    #             pass
    #         else:
    #             z = float(funds_amt) / float(price)
    #             x = numpy.floor(z)
    #             logging.info('Shares to Buy: ' + str(x))
    #             return int(x)
    #     stk_symbol = str(sym)
    #     shares_to_buy = calc_shares(funds, bid_price)
    #     shares_num_buy = str(shares_to_buy)
    #     print(shares_to_buy)
    #     act = str(account)
    #     inst = str(instrument)
    #     data = {"account": "https://api.robinhood.com/accounts/858649452/",
    #             "extended_hours": "false",
    #             "instrument": {
    #                 "url": "https://api.robinhood.com/instruments/d4343b04-5522-4ff6-a892-4fc97dc61b68/",
    #                 "symbol": "BPMX"},
    #
    #             "price": bid_price,
    #             "quantity": shares_num_buy,
    #             "side": "buy",
    #             "time_in_force": "gtd",
    #             "trigger": "immediate",
    #             "type": "market"}
    #     for item in data.items():
    #         print(type(item))
    #     logging.info(data)
    #     url = "https://api.robinhood.com/orders"
    #     auth_str = 'Bearer ' + tk
    #     headers = {"Accept": "*/*",
    #                "Accept-Encoding": "gzip, deflate",
    #                "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
    #                "Authorization": auth_str, "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)",
    #                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
    #     print(headers)
    #     order_req = requests.post(url, headers=headers, data=data, verify=False, timeout=6)
    #     s = order_req.raise_for_status()
    #     print(s)
    #     print(order_req.status_code())
    #     logging.info(str(order_req.status_code))
    #     print(order_req.headers())
    #     logging.info(str(order_req.headers))
    #     print(order_req.content())
    #     logging.info(str(order_req.content))
    #     return order_req.content()
    #
    #
    # try:
    #     hit = order(session_token, sym_to_trade)
    #     print(hit)
    #     logging.info(str(hit))
    # except:
    #     print("Order Fail")
    #     logging.error('########## !!! Order Fail !!! ##########')

#
# schedule.every(1).second.do(main)
# while True:
#     sleep(.100)
#     schedule.run_pending()

