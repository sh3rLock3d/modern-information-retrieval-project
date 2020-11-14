from prepare_text import DictionaryProcess


class LNC_LTC:
    def __index__(self, my_index):
        self.index = my_index

    def get_query_results(self, query):
        query_tokens = DictionaryProcess(query).prepare_text()


    def _get_token_tokens_lnc(self, tokens, query_tokens):
        import math
        lnc = {}
        """ tf part """
        for token in tokens:
            if token in query_tokens:
                lnc[token] = lnc.get(token, 0) + 1
        for key in lnc.keys():
            lnc[key] = 1 + math.log(lnc.get(key, 0))
        """ idf part """

        """ norm part """
        lnc_values = list(lnc.values())
        lnc_weight = (self.dot_product(lnc_values, lnc_values)) ** 2
        for key in lnc.keys():
            lnc[key] = lnc[key] / lnc_weight
        return lnc

    def _get_tokens_ltc(self, tokens, query_tokens):
        import math
        ltc = {}
        """ l part """
        for token in tokens:
            if token in query_tokens:
                ltc[token] = ltc.get(token, 0) + 1
        for key in ltc.keys():
            ltc[key] = 1 + math.log(ltc.get(key, 0))
        """ idf part """
        idf = 1  # TODO
        for key in ltc.keys():
            ltc[key] = ltc[key] * idf
        """ norm part """
        lnc_values = list(ltc.values())
        lnc_weight = (self.dot_product(lnc_values, lnc_values)) ** 2
        for key in ltc.keys():
            ltc[key] = ltc[key] / lnc_weight
        return ltc

    @classmethod
    def dot_product(cls, lnc, ltc):
        res = 0
        for i in range(len(lnc)):
            res += lnc[i] * ltc[i]
        return res
