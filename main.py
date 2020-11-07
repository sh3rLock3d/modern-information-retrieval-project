from compressing import compress
from indexing import indexing
from prepare_text import prepare_text

ted_talk = 'data/ted_talk.csv'
persian = 'data/Persion.xml'


def main():
    prepare_text()
    indexing()
    compress()
    # eslahe porseman
    # jostoju va bazyabi asnad



if __name__ == '__main__':
    main()
