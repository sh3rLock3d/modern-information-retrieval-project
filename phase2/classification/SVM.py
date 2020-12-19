from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC

from data_reader import read_test_data, read_train_data, read_data
from phase2.convertDataToVectorSpace import VectorSpaceConverter


def SVM(c):
    train_data = read_train_data()
    test_data = read_test_data()
    data = read_data()
    vector_space = VectorSpaceConverter(data).get_vector_space_documents_and_tokens(data)
    vector_space_train = vector_space[0:len(train_data)]
    vector_space_test = vector_space[len(train_data):]
    y_train = [data[i]['views'] for i in range(len(train_data))]
    y_test = [test_data[i]['views'] for i in range(len(test_data))]
    classifier = SVC(C=c, kernel='linear')
    classifier.fit(vector_space_train, y_train)
    y_pred = classifier.predict(vector_space_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))
