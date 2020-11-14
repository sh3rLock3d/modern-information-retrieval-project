from indexing import Indexing
from search_and_retrieval import SearchAndRetrieval
from prepare_text import DictionaryProcess
from compressing import CompressUtils

def main():
    """ reading and indexing files """
    my_index = Indexing()
    my_index.update_index_from_files()

    """ compressing and saving index object to a file """
    #my_index.compress_with_variable_code()
    #my_index.compress_with_variable_code()

    """ getting queries """
    search_and_retrieval = SearchAndRetrieval(my_index)

    """ user interface """
    user_interface(my_index, search_and_retrieval)


def user_interface(my_indexing, search):
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
                    # todo namayeshe loghate por tekrar
                    pass
            if command == '2':
                l = input('2: showing post_list of a word\n3: showing index of a word in every doc\n4:showing every word that contains a specific bigram\n')
                if l == '2':
                    # todo
                    pass
                if l == '3':
                    # todo
                    pass
                if l == '4':
                    # todo
                    pass
            if command == '3':
                l = input('1: storage variable bytes\n2: storage gamma code\n3:store in file\n')
                if l == '1':
                    # todo
                    pass
                if l == '2':
                    # todo
                    pass
                if l == '3':
                    CompressUtils.compress_with_gamma(my_indexing)
                    token_freq = []
                    for key in my_indexing.ted_talk_ii.dictionary.keys():
                        token_freq.append(my_indexing.ted_talk_ii.dictionary.get(key)[0])
                    CompressUtils.decode_with_gamma(my_indexing.ted_talk_ii.dictionary.keys(),token_freq)
                    pass
            if command == '4':
                l = input('1: showing corrected query\n2: calculate jacard of two words\n3:calculate edit distance of two words\n')
                if l == '1':
                    res = search.my_query_check.spell_corrector(input('query: '), input('subsection: '))
                    print(res)
                if l == '2':
                    # todo jacard of two words
                    pass
                if l == '3':
                    selected_word = input('selected_word: ')
                    word = input('word: ')
                    edit_distance_value = search.my_query_check.editDistance(selected_word, word, len(selected_word), len(word))
                    print(edit_distance_value)
            if command == '5':
                pass

        elif command == 's':
            search.run()


if __name__ == '__main__':
    main()
