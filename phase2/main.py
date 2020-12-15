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
    print("K = 1, Accuracy: ", nn_1.get_accuracy(vector_space_testing, test_data))
    nn_5 = KNN(5, validation_data, vector_space_validation)
    print("K = 5, Accuracy: ", nn_5.get_accuracy(vector_space_testing, test_data))
    nn_9 = KNN(9, validation_data, vector_space_validation)
    print("K = 9, Accuracy: ", nn_9.get_accuracy(vector_space_testing, test_data))
