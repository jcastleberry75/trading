import robin_client
import json

with open('creds.json', 'r') as creds:
    robin_creds = json.load(creds)

robinhood = robin_client.RobinClient()

u_name = robin_creds["username"]
passwd = robin_creds["password"]
robin_token = robinhood.robinhood_login(user_name=u_name, password=passwd)



positons = robinhood.get_positions(robin_token)

print(positons)
