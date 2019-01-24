import json
import robin_client
import logging
import schedule
from time import sleep


def get_token():
    log_format = '%(asctime)-s [%(levelname)-s] (%(threadName)-s)  %(message)s'
    logging.basicConfig(format=log_format, filename='logins.log', level=logging.DEBUG)
    logging.info('#################### ROBINHOOD LOGIN FOR TOKEN  ####################')
    with open('creds.json', 'r') as creds:
        robin_creds = json.load(creds)

    u_name = robin_creds["username"]
    passwd = robin_creds["password"]
    robinhood = robin_client.RobinClient()
    robin_token = robinhood.robinhood_login(user_name=u_name, password=passwd)
    token_dict = dict()
    token_dict["token"] = robin_token
    logging.info('ACQUIRED TOKEN: ' + str(token_dict))
    with open("robin_token.json", "w") as f:
        json.dump(token_dict, f)

schedule.every(1).minute.do(get_token)
while True:
    sleep(1)
    schedule.run_pending()
