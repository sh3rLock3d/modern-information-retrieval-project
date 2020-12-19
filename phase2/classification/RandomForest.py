from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from phase2.convertDataToVectorSpace import VectorSpaceConverter


class RandomForest:
    def __init__(self,converter):
        self.converter = converter
        self.classifier = None

    def train(self, train_data):
        print("Training Random Forest ...")
        vector_space_train = self.converter.get_vector_space_documents_and_tokens(train_data)
        y_train = [train_data[i]['views'] for i in range(len(train_data))]
        self.classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
        self.classifier.fit(vector_space_train, y_train)
        print("Random Forest Training Done! ")

    def get_accuracy(self, vector_space_test, test_data):
        y_test = [test_data[i]['views'] for i in range(len(test_data))]
        y_pred = self.classifier.predict(vector_space_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        print(accuracy_score(y_test, y_pred))

    def predict(self, vector_space):
        y_pred = self.classifier.predict([vector_space])
        return y_pred[0]
