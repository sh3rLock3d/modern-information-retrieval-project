from phase1.indexing import Indexing
from phase1.prepare_text import DictionaryProcess


class LNC_LTC:
    def __init__(self, my_index):
        self.index: Indexing = my_index

    def get_query_results(self, query, sub_section):
        result_dict_score = {}
        docs_tokens, query_tokens_norm, tokens_raw_tf, tokens_raw_df = self.get_query_data(query, sub_section)
        query_vector_data = self._get_tokens_ltc(query_tokens_norm, tokens_raw_df)
        for doc_id in docs_tokens.keys():
            doc_vector_data = self._get_token_tokens_lnc(docs_tokens[doc_id], query_tokens_norm)
            score = self.dot_product(query_vector_data, doc_vector_data)
            result_dict_score[score] = result_dict_score.get(score, []) + [doc_id]
        score_values = list(result_dict_score.keys())
        score_values.sort()
        score_values.reverse()
        result = []
        for score in score_values:
            for doc in result_dict_score[score]:
                result.append(doc)
                if len(result) >= 10:
                    return result

    def get_token_raw_tf_and_postings(self, token, sub_section):
        if DictionaryProcess.check_persian(token[0]):
            raw_tf, posting = self.index.persian_ii.dictionary.get(token + "-" + sub_section, [0, []])
        else:
            raw_tf, posting = self.index.ted_talk_ii.dictionary.get(token + "-" + sub_section, [0, []])
        return raw_tf, posting

    def get_query_data(self, query, sub_section):
        docs_tokens = {}
        query_tokens_norm = {}
        tokens_raw_tf = {}
        tokens_raw_df = {}
        query_tokens = DictionaryProcess(query).prepare_text()
        for token in query_tokens:
            """ query tokens """
            query_tokens_norm[token] = query_tokens_norm.get(token, 0) + 1
            raw_tf, postings = self.get_token_raw_tf_and_postings(token, sub_section)
            """ tf """
            tokens_raw_tf[token] = raw_tf
            for posting in postings:
                """ doc tokens """
                doc_id = posting.doc_id
                doc_tokens = docs_tokens.get(doc_id, {})
                doc_tokens[token] = len(posting.positions)
                docs_tokens[doc_id] = doc_tokens
                """ df """
                tokens_docs = tokens_raw_df.get(token, set())
                tokens_docs.add(doc_id)
                tokens_raw_df[token] = tokens_docs
        return docs_tokens, query_tokens_norm, tokens_raw_tf, tokens_raw_df

    def _get_token_tokens_lnc(self, tokens, query_tokens):
        import math
        lnc = tokens
        """ tf part """
        for key in lnc.keys():
            lnc[key] = 1 + math.log(lnc.get(key, 0))
        """ idf part """

        """ norm part """
        lnc_weight = (self.dot_product(lnc, lnc)) ** 0.5
        for key in lnc.keys():
            lnc[key] = lnc[key] / lnc_weight
        return lnc

    def _get_tokens_ltc(self, tokens, tokens_df):
        import math
        ltc = tokens
        """ l part """
        for key in ltc.keys():
            ltc[key] = 1 + math.log(ltc.get(key, 0))
        """ idf part """
        try:
            ch = list(tokens.keys())[0][0]
        except:
            ch = False
        if DictionaryProcess.check_persian(ch):
            N = len(self.index.persian_doc_ids)
        else:
            N = len(self.index.ted_talk_doc_ids)
        for key in ltc.keys():
            ltc[key] = ltc[key] * math.log(N / len(tokens_df.get(key, set([1]))))
        """ norm part """
        ltc_weight = (self.dot_product(ltc, ltc)) ** 0.5
        for key in ltc.keys():
            ltc[key] = ltc[key] / ltc_weight
        return ltc

    @classmethod
    def dot_product(cls, lnc_dict: dict, ltc_dict: dict):
        res = 0
        for key in lnc_dict.keys():
            res += lnc_dict.get(key, 0) * ltc_dict.get(key, 0)
        return res
