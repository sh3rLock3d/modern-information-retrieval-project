from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC


class SVM:
    def __init__(self, converter):
        self.converter = converter
        self.classifier = None

    def train(self, c, train_data):
        print("Training SVM ...")
        vector_space_train = self.converter.get_vector_space_documents_and_tokens(train_data)
        y_train = [train_data[i]['views'] for i in range(len(train_data))]
        self.classifier = SVC(C=c, kernel='linear')
        self.classifier.fit(vector_space_train, y_train)
        print("SVM Training Done! ")

    def get_accuracy(self, vector_space_test, test_data):
        y_test = [test_data[i]['views'] for i in range(len(test_data))]
        y_pred = self.classifier.predict(vector_space_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        return accuracy_score(y_test, y_pred)

    def predict(self, vector_space):
        y_pred = self.classifier.predict([vector_space])
        return y_pred[0]
