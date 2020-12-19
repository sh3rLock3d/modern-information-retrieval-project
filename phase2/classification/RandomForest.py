from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from data_reader import read_train_data, read_test_data, read_data
from phase2.convertDataToVectorSpace import VectorSpaceConverter


class RandomForest:
    def __init__(self, train_data, test_data, ):
        self.classifier = None

    def train(self):
        train_data = read_train_data()
        test_data = read_test_data()
        data = read_data()
        vector_space = VectorSpaceConverter(data).get_vector_space_documents_and_tokens(data)
        vector_space_train = vector_space[0:len(train_data)]
        vector_space_test = vector_space[len(train_data):]
        y_train = [data[i]['views'] for i in range(len(train_data))]
        self.classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
        self.classifier.fit(vector_space_train, y_train)

    def get_accuracy(self, vector_space_test, test_data):
        y_test = [test_data[i]['views'] for i in range(len(test_data))]
        y_pred = self.classifier.predict(vector_space_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        print(accuracy_score(y_test, y_pred))

    def predict(self, vector_space):
        y_pred = self.classifier.predict(vector_space)
        return y_pred
