from compressing import compress
from indexing import indexing
from query_check import query_check


def main():
    my_index = indexing()
    my_compress = compress(my_index)
    my_query_check = query_check(my_compress)
    # jostoju va bazyabi asnad


if __name__ == '__main__':
    main()
