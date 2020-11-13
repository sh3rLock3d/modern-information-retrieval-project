from SearchAnsRetrival import SearchAnsRetrival
from compressing import Compress
from indexing import Indexing
from query_check import query_check


def main():
    my_index = Indexing()
    my_compress = Compress(my_index)
    my_query_check = query_check(my_compress)
    SearchAnsRetrival(my_query_check)


if __name__ == '__main__':
    main()
