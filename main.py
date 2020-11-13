from indexing import Indexing
from search_and_retrieval import SearchAndRetrieval


def main():
    """ reading and indexing files """
    my_index = Indexing()
    my_index.update_index_from_files()

    """ compressing and saving index object to a file """
    my_index.compress_with_variable_code()
    my_index.compress_with_variable_code()

    """ getting queries """
    SearchAndRetrieval(my_index)


if __name__ == '__main__':
    main()
