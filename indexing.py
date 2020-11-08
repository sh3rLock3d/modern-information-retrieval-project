from prepare_text import DictionaryProcess


# inverted index dictionary
class IIDictionary:
    class PostingItem:
        def __init__(self, doc_id):
            self.doc_id = doc_id
            self.positions = []

    class TokenKey:
        def __init__(self, token, sub_section):
            self.token = token
            self.sub_section = sub_section

        def key(self):
            return self.token + " subsection " + self.sub_section

    def __init__(self):
        """ ted_talk[TokenKey] = [PostingItem list] """
        self.dictionary: {IIDictionary.TokenKey: [IIDictionary.PostingItem]} = {}

    def merge_token_doc(self, token_key, posting_item):
        posting_list = self.dictionary.get(token_key, [])
        # TODO
        posting_list.append(posting_item)
        posting_list.sort(key=lambda pi: pi.doc_id)
        self.dictionary[token_key] = posting_list


class Indexing:

    def __init__(self):
        self.ted_talk = IIDictionary()
        self.persian = IIDictionary()
        self.indexing()

    def get_ted_talk_dictionary(self):
        return self.ted_talk

    def get_persian_dictionary(self):
        return self.persian

    @classmethod
    def reading_ted_talk(cls):
        import pandas as pd
        ted_talk_data = pd.read_csv('./data/ted_talks.csv')
        return ted_talk_data[['title', 'description']]

    def indexing_single_doc(self, doc, doc_id):
        tokens_position = {}
        for subSection in doc.keys():
            text = doc[subSection]
            dictionary_process = DictionaryProcess(text)
            # TODO fake tokens
            for pos, token in enumerate(['tt', 'th', 'dfgh', 'th']):
                token_key = IIDictionary.TokenKey(token, subSection)
                tokens_position[token_key.key()] = tokens_position.get(token_key.key(), []) + [pos]
        for token_key_string in tokens_position.keys():
            posting_item = IIDictionary.PostingItem(doc_id)
            posting_item.positions = tokens_position[token_key_string]
            self.ted_talk.merge_token_doc(token_key_string, posting_item)

    def indexing_ted_talk(self):
        data = Indexing.reading_ted_talk()
        for doc_index in range(data.shape[0]):
            self.indexing_single_doc(data.iloc[doc_index], doc_index)

    @classmethod
    def reading_persian(cls):
        import xmltodict
        with open("data/Persian.xml") as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        pages_dict = data_dict['mediawiki']['page']

    def indexing(self):
        self.indexing_ted_talk()
        self.reading_persian()
        # for on ducument : prepare text; add to dictionary
        pass
