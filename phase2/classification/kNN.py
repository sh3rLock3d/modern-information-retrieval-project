class KNN:
    def __init__(self, k, documents, training_data_vector):
        self.k = k
        self.documents = documents
        self.training_data_vector = training_data_vector

    def predict(self, doc_vector, doc):
        score_list = []
        for index, train_vector in enumerate(self.training_data_vector):
            score = self.distance(train_vector, doc_vector)
            if len(score_list) < self.k:
                score_list.append([score, index])
            else:
                score_list.sort()
                min_score = score_list[0][0]
                if score > min_score:
                    del score_list[0]
                    score_list.append([score, index])
        result_dictionary = {}
        for score, index in score_list:
            predicted_doc = self.documents[index]
            result_dictionary[predicted_doc['views']] = result_dictionary.get(predicted_doc['views'], 0) + 1
        min_value = min(result_dictionary.values())
        for key in result_dictionary.keys():
            if result_dictionary[key] == min_value:
                return key
        return None

    def get_accuracy(self, test_vectors, test_documents):
        right_predicted_count = 0
        for index, test_vector in enumerate(test_vectors):
            print("test index:", index)
            predicted_views = self.predict(test_vector, test_documents[index])
            real_views = test_documents[index]['views']
            if real_views == predicted_views:
                right_predicted_count += 1
        return (right_predicted_count / len(test_documents)) * 100

    @classmethod
    def dot_product(cls, v1, v2):
        res = 0
        for i in range(len(v1)):
            res += v1[i] * v2[i]
        return res

    @classmethod
    def distance(cls, v1, v2):
        res = 0
        for i in range(len(v1)):
            res += (v1[i] - v2[i]) ** 2
        return res ** 0.5
