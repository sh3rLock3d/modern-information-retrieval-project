from phase1.prepare_text import DictionaryProcess


class VectorSpaceConverter:
    """ document as json"""

    def __init__(self, document):
        self.json_document = document
        self.tokens = self.get_tokens()

    def get_tokens(self):
        res = set()
        for doc in self.json_document:
            for subSection in doc.keys() - ["views", "id"]:
                dictionary_process = DictionaryProcess(doc[subSection]).prepare_text()
                for token in dictionary_process:
                    res.add(token + "-" + subSection)
        return res

    def get_vector_space_documents_and_tokens(self):
        res = []
        words = list(self.tokens)
        for doc in self.json_document:
            doc_vector = [0] * len(words)
            for subSection in doc.keys() - ["views", "id"]:
                dictionary_process = DictionaryProcess(doc[subSection]).prepare_text()
                for token in dictionary_process:
                    main_token = token + "-" + subSection
                    doc_vector[words.index(main_token)] += 1
            res.append(doc_vector)
        return res
