import robin_client
import sms_parser
import order_processor
import json
import logging
from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse


def main():
    log_format = '%(asctime)-s [%(levelname)-s] (%(threadName)-s)  %(message)s'
    logging.basicConfig(format=log_format, filename='trading_automation.log', level=logging.DEBUG)
    logging.info('#################### FLASK SMS SERVER STARTED  ####################')
    app = Flask(__name__)
    robinhood = robin_client.RobinClient()
    processor = order_processor.Processor()

    @app.route("/sms", methods=['GET', 'POST'])
    def sms():
        if request.method == 'POST':
            """Respond to incoming message"""
            from_number = request.form['From']
            logging.info('Incoming MSG from: ' + from_number)
            incoming_msg_body = request.form['Body']
            logging.info('Incoming MSG content: ' + incoming_msg_body)
            msg_words = incoming_msg_body.split(" ")
            bad_words = ["Option", "option", "Options", "options", "Sold", "sold",
                         "Selling", "selling"]
            word_check = set(msg_words).intersection(bad_words)
            if len(word_check) is 0:
                logging.info("No Bad Words in Message")
                msg_parsed_data = sms_parser.Parser()
                stk_and_price = msg_parsed_data.msg_words_parse(message_words=msg_words)
                logging.info("Parsed: " + str(stk_and_price))
                symbol = stk_and_price[0]
                stk_quote = robinhood.get_instrument_quote(symbol=symbol)
                stk_data = (stk_quote[0])
                logging.info(str(stk_data))
                bid_price = stk_data['bid_price']
                logging.info('Current Bid Price: ' + bid_price)
                instrument = stk_data['instrument']
                logging.info('Instrument: ' + instrument)
                msg_stock_price = stk_and_price[1]
                account_info = robinhood.get_account_info()
                logging.info(str(account_info))
                buy_order = processor.calc_buy(symbol=symbol,
                                               instrument=instrument,
                                               message_price=msg_stock_price,
                                               quote_price=bid_price,
                                               buying_power=account_info['buying_power'],
                                               account_url=account_info['url'])
                logging.info(buy_order)

            else:
                logging.info("Bad Words Found in Message: " + str(word_check) + " - IGNORING")

            resp = MessagingResponse()
            # Add a message
            resp.message('Hello {}, you said: {}'.format(from_number, incoming_msg_body))
            logging.info('Response MSG: ' + str(resp))
            return str(resp)

        elif request.method == 'GET':
            return render_template('sms.html', title='SMS STATUS')

    while True:
        app.run(host='0.0.0.0', debug=True, port=10001)


if __name__ == "__main__":
    main()
