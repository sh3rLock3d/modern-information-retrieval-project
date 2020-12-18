import nltk

from phase1.prepare_text import DictionaryProcess


class VectorSpaceConverter:
    """ document as json"""

    def __init__(self, document):
        nltk.download('stopwords')
        self.json_document = document
        self.tokens = self.get_tokens()

    def get_tokens(self):
        res = dict()
        for doc in self.json_document:
            for subSection in doc.keys() - ["views", "id"]:
                dictionary_process = DictionaryProcess(doc[subSection]).prepare_text()
                dictionary_process = self.delete_stop_words(dictionary_process)
                for token in dictionary_process:
                    main_token: str = (token + "-" + subSection)
                    res[main_token] = res.get(main_token, set())
                    res[main_token].add(doc['id'])
        return res

    def get_vector_space_documents_and_tokens(self, docs):
        import math
        res = []
        words = list(self.tokens.keys())
        for doc in docs:
            doc_vector = [0] * len(words)
            doc_tokens_count = dict()
            for subSection in doc.keys() - ["views", "id"]:
                dictionary_process = DictionaryProcess(doc[subSection]).prepare_text()
                dictionary_process = self.delete_stop_words(dictionary_process)
                for token in dictionary_process:
                    main_token = token + "-" + subSection
                    try:
                        index = words.index(main_token)
                    except ValueError:
                        index = -1
                    if index != -1:
                        doc_tokens_count[main_token] = doc_tokens_count.get(main_token, 0) + 1
                        doc_vector[index] = math.log(len(self.json_document) / len(self.tokens[main_token]))
                """ tf part """
                for token in dictionary_process:
                    main_token = token + "-" + subSection
                    try:
                        index = words.index(main_token)
                    except ValueError:
                        index = -1
                    if index != -1:
                        doc_vector[index] *= doc_tokens_count.get(main_token, 0)

            res.append(doc_vector)
        return res

    @classmethod
    def delete_stop_words(self, dictionaey_process):
        stops = nltk.corpus.stopwords.words('english')
        res = []
        for w in dictionaey_process:
            lower_words = w.lower()
            if lower_words not in stops:
                res.append(lower_words)
        return res
