from phase1.compressing import CompressUtils
from phase1.indexing import Indexing
from phase1.prepare_text import DictionaryProcess
from phase1.query_check import query_check
from phase1.search_and_retrieval import SearchAndRetrieval
from phase2.classification.kNN import KNN
from phase2.convertDataToVectorSpace import VectorSpaceConverter


def read_train_data():
    import pandas as pd
    ted_talk_data = pd.read_csv('phase2_data/train.csv')
    result_wikis = []
    for index, doc in enumerate(ted_talk_data[['title', 'description', 'views']].values):
        title = doc[0]
        description = doc[1]
        view = doc[2]
        result_wikis.append({'id': index, 'title': title, 'description': description, 'views': view})
    return result_wikis


def read_test_data():
    import pandas as pd
    ted_talk_data = pd.read_csv('phase2_data/test.csv')
    result_wikis = []
    for index, doc in enumerate(ted_talk_data[['title', 'description', 'views']].values):
        title = doc[0]
        description = doc[1]
        view = doc[2]
        result_wikis.append({'id': index, 'title': title, 'description': description, 'views': view})
    return result_wikis


def get_classifier():
    train_data = read_train_data()
    validation_data = train_data[:int(len(train_data) / 20)]
    test_data = read_test_data()
    ### creating vector space by tokenizing documents
    converter = VectorSpaceConverter(validation_data + test_data)
    ###  list of all available documents in space: taken from all tokens in documents tokens like this example: "token-subsection" - > "hello-title"
    words = list(converter.tokens)
    ## converting validation data to vectors in tokens vector space
    vector_space_validation = converter.get_vector_space_documents_and_tokens(validation_data)
    ## converting test data to vectors in tokens vector space
    vector_space_testing = converter.get_vector_space_documents_and_tokens(test_data)

    """ knn alg """
    nn_1 = KNN(1, validation_data, vector_space_validation)
    nn_5 = KNN(5, validation_data, vector_space_validation)
    nn_9 = KNN(9, validation_data, vector_space_validation)

    """ evaluation """
    print("K = 1, Accuracy: ", nn_1.get_accuracy(vector_space_testing, test_data))
    print("K = 5, Accuracy: ", nn_5.get_accuracy(vector_space_testing, test_data))
    print("K = 9, Accuracy: ", nn_9.get_accuracy(vector_space_testing, test_data))

    return nn_9


def main():
    """ create and train classifier"""
    knn_classifier = get_classifier()
    """ reading and indexing files """
    my_index = Indexing()
    my_index.update_index_from_files()

    """ compressing and saving index object to a file """
    # my_index.compress_with_variable_code()
    # my_index.compress_with_variable_code()
    """ modifing query """
    check_query = query_check(my_index)
    """ getting queries """
    search_and_retrieval = SearchAndRetrieval(my_index)

    """ user interface """
    user_interface(my_index, search_and_retrieval, check_query)


def user_interface(my_indexing, search, check_query):
    def showing_posting_list_of_a_word(word, sub_section):
        if DictionaryProcess.check_persian(word[0]):
            postings = my_indexing.persian_ii.dictionary.get(word + "-" + sub_section, [0, []])
        else:
            postings = my_indexing.ted_talk_ii.dictionary.get(word + "-" + sub_section, [0, []])
        print("doc freq:", postings[0])
        for posting in postings[1]:
            print(posting)

    def showing_every_word_that_contains_a_specific_bigram(bigram):
        if DictionaryProcess.check_persian(bigram[0]):
            postings = my_indexing.persian_kh.dictionary.get(bigram, {})
        else:
            postings = my_indexing.ted_talk_kg.dictionary.get(bigram, {})
        print("bigram:", bigram)
        for posting in postings.keys():
            print(posting)

    print('phase 1 of MIR project')
    while True:
        print("if you wanna search type 's'\n"
              "if you wanna test parts of project type 't'\n"
              "if you wanna exit type e")
        command = input()
        if command == 'e':
            break
        elif command == 't':
            print("witch part of project do you wanna test? ", end='')
            command = input()
            if command == '1':
                l = input('1:prepare a text\n2:showing most used words:\n')
                if l == '1':
                    print('enter your test and at the last line print "exit":')
                    text = ''
                    while True:
                        a = input()
                        if a == 'exit':
                            break
                        text = text + '\n' + a
                    result = DictionaryProcess(text).prepare_text()
                    print(result)
                if l == '2':
                    print("ted_talk:")
                    print(my_indexing.get_stop_words_set(my_indexing.ted_talk_ii.dictionary))
                    print("persian:")
                    print(my_indexing.get_stop_words_set(my_indexing.persian_ii.dictionary))
            if command == '2':
                l = input(
                    '2: showing post_list of a word\n3: showing index of a word in every doc\n4:showing every word that contains a specific bigram\n')
                if l == '2':
                    showing_posting_list_of_a_word(input("which word:"), input("which section:"))
                if l == '3':
                    showing_posting_list_of_a_word(input("which word:"), input("which section:"))
                if l == '4':
                    showing_every_word_that_contains_a_specific_bigram(input("which bigram:"))
            if command == '3':
                l = input('1: storage variable bytes\n2: storage gamma code\n3:store in file\n')
                if l == '1':
                    VB_size, size_without_compressing = CompressUtils.calculate_size_of_VBC(my_indexing)
                    print("size without compressing: " + str(size_without_compressing))
                    print("size after applying variable byye code: " + str(VB_size))
                if l == '2':
                    gamma_size, size_without_compressing = CompressUtils.calculate_size_of_gamma(my_indexing)
                    print("size without compressing: " + str(size_without_compressing))
                    print("size after applying gamma code: " + str(gamma_size))

                if l == '3':
                    # CompressUtils.compress_with_gamma(my_indexing)
                    # token_freq = []
                    # for key in my_indexing.ted_talk_ii.dictionary.keys():
                    # token_freq.append(my_indexing.ted_talk_ii.dictionary.get(key)[0])
                    # CompressUtils.decode_with_gamma(my_indexing.ted_talk_ii.dictionary.keys(),token_freq)
                    pass
            if command == '4':
                l = input(
                    '1: showing corrected query\n2: calculate jacard of two words\n3:calculate edit distance of two words\n')
                if l == '1':
                    res = check_query.spell_corrector(input('query: '), input('subsection: '))
                    print(res)
                if l == '2':
                    print(check_query.jaccard_similarity(input("first word: "), input("second word: ")))
                    pass
                if l == '3':
                    selected_word = input('selected_word: ')
                    word = input('word: ')
                    edit_distance_value = check_query.editDistance(selected_word, word, len(selected_word),
                                                                   len(word))
                    print(edit_distance_value)
            if command == '5':
                pass

        elif command == 's':
            search.run()


if __name__ == '__main__':
    main()
