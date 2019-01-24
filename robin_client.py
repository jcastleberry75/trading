import requests
import logging
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class RobinClient:

    def __init__(self,
                 user_name=None,
                 password=None,
                 account=None,
                 symbol=None,
                 bid_price=None,
                 shares_num=None,
                 instrument=None):

        self.user_name = user_name
        self.password = password
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

    def get_instrument_quote(self, symbol):
        def read_token():
            with open('creds/robin_token.json', 'r') as t:
                token_data = json.load(t)
            token = token_data['token']
            return token
        token = read_token()
        params = {'symbols': symbol}
        url = "https://api.robinhood.com/quotes/"
        token = token
        auth_str = 'Bearer ' + token
        headers = {'Authorization': auth_str}
        quote = requests.get(url, headers=headers, params=params, verify=False)
        quote_result = (quote.json())
        quote_data = (quote_result['results'])
        return quote_data

    def get_account_info(self):
        def read_token():
            with open('creds/robin_token.json', 'r') as t:
                token_data = json.load(t)
            token = token_data['token']
            return token
        token = read_token()
        url = "https://api.robinhood.com/accounts/"
        auth_str = 'Bearer ' + token
        headers = {'Authorization': auth_str}
        resp_data = requests.get(url, headers=headers, verify=False)
        acct_info = (resp_data.json())
        res = acct_info['results'][0]
        return res

    def get_positions(self):
        def read_token():
            with open('creds/robin_token.json', 'r') as t:
                token_data = json.load(t)
            token = token_data['token']
            return token
        token = read_token()
        url = 'https://api.robinhood.com/applications/'
        auth_str = 'Bearer ' + token
        headers = {'Authorization': auth_str}
        resp_data = requests.get(url, headers=headers, verify=False)
        acct_info = (resp_data.json())
        res = acct_info
        return res

    def buy_order(self, account_url, symbol, instrument,  bid_price, shares_num):
        logging.info(str(account_url))
        logging.info(str(instrument))
        logging.info(str(symbol))
        logging.info(str(bid_price))
        logging.info(str(shares_num))

        data = {"account": account_url,
                "symbol": symbol,
                "instrument": instrument,
                "price": bid_price,
                "quantity": shares_num,
                "side": "buy",
                "time_in_force": "gfd",
                "trigger": "immediate",
                "type": "market"}
        logging.info(data)
        url = "https://api.robinhood.com/orders/"

        def read_token():
            with open('creds/robin_token.json', 'r') as t:
                token_data = json.load(t)
            token = token_data['token']
            return token

        token = read_token()
        auth_str = 'Bearer ' + token
        headers = {"Accept": "*/*",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
                   "Authorization": auth_str, "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)",
                   "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        logging.info(str(headers))
        order_req = requests.post(url, headers=headers, data=data, verify=False, timeout=6)
        logging.info(str(order_req.text))
        logging.info(str(order_req.json))
        logging.info(str(order_req.status_code))
        logging.info(str(order_req.headers))
        logging.info(str(order_req.content))
        status = order_req.status_code()
        return str(status)
