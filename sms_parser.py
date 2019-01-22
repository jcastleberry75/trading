import re


class Parser:
    def __init__(self,
                 message_words=None,
                 ):

        self.message_words = message_words

    def msg_words_parse(self, message_words):
        stks = []
        clean_words = []
        with open('stock_symbols.txt', 'r') as stock_file:
            for l in stock_file:
                sym = l.rstrip()
                stks.append(sym)
        for w in message_words:
            if ',' in w:
                clean_word = w.replace(',', '')
                clean_words.append(clean_word)
            else:
                clean_words.append(w)

        def find_sym():
            sym_check = set(clean_words).intersection(stks)
            if len(sym_check) is 0:
                return None
            else:
                return sym_check.pop()

        def price_find():
            prices = []
            for word in clean_words:
                pattern = r'\d*\.?\d+'
                num = re.compile(pattern)
                decimal_result = num.search(word)
                if decimal_result:
                    result_number = str(decimal_result[0])
                    if '.' in result_number:
                        prices.append(result_number)
            return prices

        prices_found = price_find()
        stk_sym = find_sym()
        data = (stk_sym, prices_found)
        return data






