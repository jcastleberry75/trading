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

