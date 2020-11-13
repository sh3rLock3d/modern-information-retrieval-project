from indexing import KGDictionary
from prepare_text import DictionaryProcess


class query_check:
    def __init__(self, my_index):
        self.indexing = my_index

    def spell_corrector(self, query, sub_section):
        modified_query = []
        query_words = query.split(" ")
        # query_tokens = DictionaryProcess(query).prepare_text()
        for word in query_words:
            modified_query.append(self.get_modified_word(word, sub_section))
        return " ".join(modified_query)

    def get_modified_word(self, word, sub_section):
        k_gram_dictionary_list = []
        selected_k_gram_dictionary = []
        if self.check_query_is_misspelled(word, sub_section):
            for k_gram in KGDictionary.get_k_grams(word):
                k_gram_dictionary_list.append(self.get_k_gram_dictionary(k_gram))

            for i in range(len(k_gram_dictionary_list) - 1):
                if self.jaccard_similarity(k_gram_dictionary_list[i], k_gram_dictionary_list[i + 1]) > 0.05:
                    selected_k_gram_dictionary.append(set(k_gram_dictionary_list[i]))

            intersection = set.intersection(*selected_k_gram_dictionary)
            word_min = ("", float('inf'))
            for selected_word in intersection:
                editDistance_value = self.editDistance(selected_word, word, len(selected_word), len(word))
                if editDistance_value < word_min[1]:
                    word_min = selected_word, editDistance_value
            return word_min[0]
        else:
            return word

    def check_query_is_misspelled(self, word, sub_section):
        ch = word[0]
        persian = DictionaryProcess.check_persian(ch)
        if persian:
            return self.indexing.persian_ii.dictionary.get(word + "-" + sub_section, None) is None
        else:
            return self.indexing.ted_talk_ii.dictionary.get(word + "-" + sub_section, None) is None

    def get_k_gram_dictionary(self, k_gram):
        ch = k_gram[0]
        persian = DictionaryProcess.check_persian(ch)
        if persian:
            return list(self.indexing.persian_kg.dictionary.get(k_gram, {}).keys())
        else:
            return list(self.indexing.ted_talk_kg.dictionary.get(k_gram, {}).keys())

    def jaccard_similarity(self, query, document):
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection) / len(union)

    @classmethod
    def editDistance(cls, str1, str2, m, n):
        if m == 0:
            return n
        if n == 0:
            return m

        if str1[m - 1] == str2[n - 1]:
            return cls.editDistance(str1, str2, m - 1, n - 1)

        return 1 + min(cls.editDistance(str1, str2, m, n - 1),  # Insert
                       cls.editDistance(str1, str2, m - 1, n),  # Remove
                       cls.editDistance(str1, str2, m - 1, n - 1)  # Replace
                       )
