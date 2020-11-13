from indexing import KGDictionary
from prepare_text import DictionaryProcess


class query_check:
    def __init__(self, my_index):
        self.indexing = my_index

    def spell_corrector(self, query):
        modified_query = []
        k_gram_dictionary_list = []
        selected_k_gram_dictionary = []
        query_words = query.split(" ")
        for word in query_words:
            if self.check_query_is_misspelled(word):
                for k_gram in KGDictionary.get_k_grams(word):
                    k_gram_dictionary_list.append(self.get_k_gram_dictionary(k_gram))

                for i in range(len(k_gram_dictionary_list) - 1):
                    if self.jaccard_similarity(k_gram_dictionary_list[i], k_gram_dictionary_list[i + 1]) > 0.5:
                        selected_k_gram_dictionary.extend(list(set(k_gram_dictionary_list[i])),
                                                          set(k_gram_dictionary_list[i]))

                intersection = set.intersection(*selected_k_gram_dictionary)
                word_min = ("", float('inf'))
                for selected_word in intersection:
                    editDistance_value = self.editDistance(selected_word, word, len(selected_word), len(word))
                    if editDistance_value < word_min[1]:
                        word_min = selected_word, editDistance_value
                modified_query.append(word_min[0])
            else:
                modified_query.append(word)
        return " ".join(modified_query)

    def check_query_is_misspelled(self, word):
        ch = word[0]
        persian = DictionaryProcess.check_persian(ch)
        if persian:
            return not self.indexing.persian_ii.dictionary.get(word, None) is None
        else:
            return not self.indexing.ted_talk_ii.dictionary.get(word, None) is None

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

        if str1[m - 1] == str2[n - 1]:
            return cls.editDistance(str1, str2, m - 1, n - 1)

        return 1 + min(cls.editDistance(str1, str2, m, n - 1),  # Insert
                       cls.editDistance(str1, str2, m - 1, n),  # Remove
                       cls.editDistance(str1, str2, m - 1, n - 1)  # Replace
                       )
