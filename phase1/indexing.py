# inverted index dictionary
from phase1.prepare_text import DictionaryProcess


class IIDictionary:
    class PostingItem:
        def __init__(self, doc_id):
            self.doc_id: int = doc_id
            self.positions: list = []

        def __str__(self):
            res = "# doc_id " + str(self.doc_id) + "-> "
            for pos in self.positions:
                res += " " + str(pos)
            return res

    class TokenKey:
        def __init__(self, token, sub_section):
            self.token = token
            self.frequency = 0
            self.sub_section = sub_section

        def key(self):
            return self.token + "-" + self.sub_section

        def __hash__(self):
            return hash(self.key())

    def __init__(self):
        """ ted_talk[TokenKey] = [token freq,PostingItem list] """
        self.dictionary: {IIDictionary.TokenKey: [int, [IIDictionary.PostingItem]]} = {}

    def merge_token_doc(self, token_key, posting_item):
        freq, posting_list = self.dictionary.get(token_key, [0, []])
        # TODO
        posting_list.append(posting_item)
        posting_list.sort(key=lambda pi: pi.doc_id)
        self.dictionary[token_key] = [freq + len(posting_item.positions), posting_list]


# k gram dictionary
class KGDictionary:
    k = 2

    @classmethod
    def get_k_grams(cls, txt: str):
        return [txt[i:i + cls.k] for i in range(len(txt))]

    def __init__(self):
        """ ted_talk[k_gram:str] = {word:str:set} """
        self.dictionary: {str: {str: set}} = {}

    def merge_token_doc(self, word, doc_id):
        for k_gram in self.get_k_grams(word):
            posting_dict = self.dictionary.get(k_gram, {})
            # TODO improving sort alg
            word_doc_ids = posting_dict.get(word, set())
            word_doc_ids.add(doc_id)
            posting_dict[word] = word_doc_ids

            # posting_dict.sort(key=lambda pi: pi.word)
            self.dictionary[k_gram] = posting_dict


class Indexing:
    @classmethod
    def reading_persian(cls):
        import xmltodict
        with open("phase1/phase1_data/Persian.xml") as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        result_wikis = []
        for page in data_dict['mediawiki']['page']:
            text = page['revision']['text']['#text']
            title = page['title']
            result_wikis.append({'id': int(page['id']), 'title': title, 'text': text})
        return result_wikis

    @classmethod
    def reading_ted_talk(cls):
        import pandas as pd
        ted_talk_data = pd.read_csv('phase1/phase1_data/ted_talks.csv')
        result_wikis = []
        for index, doc in enumerate(ted_talk_data[['title', 'description']].values):
            description = doc[1]
            title = doc[0]
            result_wikis.append({'id': index, 'title': title, 'description': description})
        return result_wikis

    def __init__(self):
        self.ted_talk_ii = IIDictionary()
        self.ted_talk_doc_ids = set()
        self.ted_talk_kg = KGDictionary()
        self.persian_ii = IIDictionary()
        self.persian_doc_ids = set()
        self.persian_kg = KGDictionary()

    def get_ted_talk_dictionary(self):
        return self.ted_talk_ii.dictionary

    def get_persian_dictionary(self):
        return self.persian_ii.dictionary

    def indexing_single_doc(self, doc, file):
        doc_id = doc['id']
        if file == "ted_talk":
            self.ted_talk_doc_ids.add(doc_id)
        elif file == "persian_wiki":
            self.persian_doc_ids.add(doc_id)
        print('indexing doc:', doc_id, ' in ', file)
        tokens_position = {}
        for subSection in doc.keys():
            if subSection == 'id':
                continue
            text = doc[subSection]
            dictionary_process = DictionaryProcess(text).prepare_text()
            for pos, token in enumerate(dictionary_process):
                token_key = IIDictionary.TokenKey(token, subSection)
                tokens_position[token_key.key()] = tokens_position.get(token_key.key(), []) + [pos]
        for token_key_string in tokens_position.keys():
            posting_item = IIDictionary.PostingItem(doc_id)
            posting_item.positions = tokens_position[token_key_string]
            if file == "ted_talk":
                self.ted_talk_ii.merge_token_doc(token_key_string, posting_item)
                self.ted_talk_kg.merge_token_doc(token_key_string.split("-")[0], doc_id)
            elif file == "persian_wiki":
                self.persian_ii.merge_token_doc(token_key_string, posting_item)
                self.persian_kg.merge_token_doc(token_key_string.split("-")[0], doc_id)

    def indexing_data(self, data, file):
        for doc_index in range(len(data)):
            self.indexing_single_doc(data[doc_index], file)

    def get_stop_words_set(self, dictionary):
        stop_words = []

        tokens = list(dictionary.keys())
        tokens.sort(key=lambda token_key: dictionary[token_key][0])
        tokens.reverse()
        try:
            max_freq = dictionary[tokens[0]][0]
            max_valid_token_freq = max_freq / 5
            for token in tokens:
                if dictionary[token][0] > max_valid_token_freq:
                    stop_words.append(token)
                else:
                    break
        except:
            pass
        return stop_words

    def delete_stops_from_dict(self, dict, stops):
        for stop in stops:
            del dict[stop]

    def update_index_from_files(self):
        self.indexing_data(self.reading_ted_talk(), 'ted_talk')
        self.indexing_data(self.reading_persian(), 'persian_wiki')
        print('indexing done')
        stops1 = self.get_stop_words_set(self.ted_talk_ii.dictionary)
        stops2 = self.get_stop_words_set(self.persian_ii.dictionary)
        print("stop words:\n", "\n".join(stops1 + stops2))
        self.delete_stops_from_dict(self.ted_talk_ii.dictionary, stops1)
        self.delete_stops_from_dict(self.persian_ii.dictionary, stops2)
