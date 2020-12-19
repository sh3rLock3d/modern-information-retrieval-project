import math
from convertDataToVectorSpace import VectorSpaceConverter
from data_reader import read_train_data, read_test_data, read_data


def computeTF(wordDict, total_len):
    tfDict = []
    for i in range(len(wordDict)):
        tfDict.append(wordDict[i] / float(total_len))
    return tfDict


def computeIDF(N, vector, df):
    idfDict = []

    for i in range(len(vector)):
        idfDict.append(math.log10(N / (float(df))))
    return idfDict


def TF_IDF():
    train_data = read_train_data()
    test_data = read_test_data()
    data = read_data()
    vector_space = VectorSpaceConverter(data).get_vector_space_documents_and_tokens()
    tf = []
    idf = []
    for i in range(len(data)):
        tf.append(computeTF(vector_space[i], len(vector_space[i])))
    df = [0] * len(vector_space[0])
    for vector in vector_space:
        for i in range(len(vector)):
            if vector[i] != 0:
                df[i] += 1
    for i in range(len(data)):
        idf.append(computeIDF(len(data), vector_space[i], df[i]))
    TF_IDF = []
    for i in range(len(tf)):
        multiply = []
        for j in range(len(idf[0])):
            multiply.append(tf[i][j] * idf[i][j])
        TF_IDF.append(multiply)


    return TF_IDF