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


if __name__ == '__main__':
    pass
    # TODO this main2.py file may merge later with main.py file to be used in indexing or ...
    train_data = read_train_data()
    test_data = read_test_data()
    vector_space_training = VectorSpaceConverter(train_data).get_vector_space_documents_and_tokens()
    nn_1 = KNN(1, train_data)
    nn_5 = KNN(5, train_data)
    nn_9 = KNN(9, train_data)
