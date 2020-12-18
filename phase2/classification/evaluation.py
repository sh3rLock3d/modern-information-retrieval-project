from main import read_test_data, read_train_data
from phase2 import naiveBayes
from phase2.classification.kNN import KNN
from phase2.convertDataToVectorSpace import VectorSpaceConverter


def main():
    train_data = read_train_data()
    test_data = read_test_data()
    trues = find_trues(test_data)
    print('Naive Bayes:')
    naiveBayes.train()
    correct, total = 0, len(test_data)
    true_positive = 0
    for row in test_data:
        view = naiveBayes.classsify(row['description'], row['title'])
        if view == row['views']:
            correct += 1
        if view == 1 and row['views'] == 1:
            true_positive += 1

    print('\t accuracy:', correct / total)
    print('\t precision:', true_positive / correct)
    print('\t recall:', true_positive / len(trues))

    print('K-NN:')
    validation_data = train_data[:int(len(train_data) / 20)]
    converter = VectorSpaceConverter(validation_data + test_data)
    words = list(converter.tokens)
    vector_space_validation = converter.get_vector_space_documents_and_tokens(validation_data)
    vector_space_testing = converter.get_vector_space_documents_and_tokens(test_data)

    for k in [1, 5, 9]:
        knn = KNN(k, validation_data, vector_space_validation)
        # print("K = 1, Accuracy: ", nn.get_accuracy(vector_space_testing, test_data))
        correct, total = 0, len(test_data)
        true_positive = 0
        for row in test_data:
            view = knn.predict(vector_space_testing, row) # todo predict with row = {id, description, title, views}
            if view == row['views']:
                correct += 1
            if view == 1 and row['views'] == 1:
                true_positive += 1

        print('\t knn with k =', k)
        print('\t accuracy:', correct / total)
        print('\t precision:', true_positive / correct)
        print('\t recall:', true_positive / len(trues))

    print('SVM:')

    print('Random Forest:')

def find_trues(data):  # view = 1
    trues = []
    for row in data:
        if row['views'] == 1:
            trues.append(row['id'])
    return trues


if __name__ == '__main__':
    main()
