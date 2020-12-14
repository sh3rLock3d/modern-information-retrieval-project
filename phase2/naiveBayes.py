import math
import pandas as pd

from phase1.prepare_text import DictionaryProcess


def read_csv(file_path):
    train_data = pd.read_csv(file_path)
    unnecessary_data = [ele for ele in list(train_data.columns) if ele not in ['description', 'title', 'views']]
    train_data = train_data.drop(unnecessary_data, axis=1)
    return train_data


def naive_bayes(data):
    dictionary_description = dict()
    dictionary_title = dict()
    count_y = 0
    count_n = 0
    total_y_des = 0
    total_n_des = 0
    total_y_title = 0
    total_n_title = 0
    for index, row in data.iterrows():
        view = row['views']
        if view == 1:
            count_y += 1
        else:
            count_n += 1
        # description
        description_vector = DictionaryProcess(row['description']).prepare_text()
        for token in description_vector:
            if token not in dictionary_description:
                dictionary_description[token] = [0, 0]
            if view == 1:
                total_y_des += 1
                dictionary_description[token][0] = dictionary_description[token][0] + 1
            else:
                total_n_des += 1
                dictionary_description[token][1] = dictionary_description[token][1] + 1
        # title
        title_vector = DictionaryProcess(row['title']).prepare_text()
        for token in title_vector:
            if token not in dictionary_title:
                dictionary_title[token] = [0, 0]
            if view == 1:
                total_y_title += 1
                dictionary_title[token][0] = dictionary_title[token][0] + 1
            else:
                total_n_title += 1
                dictionary_title[token][1] = dictionary_title[token][1] + 1

    # p(view = 1) & p(view = -1)
    pvy = count_y / (count_n + count_y)
    pvn = count_n / (count_n + count_y)

    return (dictionary_description, total_y_des, total_n_des), (dictionary_title, total_y_title, total_n_title), (
        pvy, pvn)


def train():
    train_data = read_csv("train.csv")
    des_table, title_table, p_view = naive_bayes(train_data)
    return des_table, title_table, p_view


def test(des_table, title_table, p_view):
    test_data = read_csv('test.csv')
    correct = 0
    total = 0
    for index, row in test_data.iterrows():
        view = row['views']
        description_vector = DictionaryProcess(row['description']).prepare_text()
        title_vector = DictionaryProcess(row['title']).prepare_text()
        # if view is 1
        P_is_1 = math.log(p_view[0])
        for token in description_vector:
            Tct = 0
            if token in des_table[0]:
                Tct = des_table[0][token][0]
            p = (Tct + 1) / (des_table[1] + len(des_table[0]))
            P_is_1 += math.log(p)

        for token in title_vector:
            Tct = 0
            if token in title_table[0]:
                Tct = title_table[0][token][0]
            p = (Tct + 1) / (title_table[1] + len(title_table[0]))
            P_is_1 += math.log(p)
        # if view is -1
        P_is_not_1 = math.log(p_view[1])
        for token in description_vector:
            Tct = 0
            if token in des_table[0]:
                Tct = des_table[0][token][1]
            p = (Tct + 1) / (des_table[2] + len(des_table[0]))
            P_is_not_1 += math.log(p)

        for token in title_vector:
            Tct = 0
            if token in title_table[0]:
                Tct = title_table[0][token][1]
            p = (Tct + 1) / (title_table[2] + len(title_table[0]))
            P_is_not_1 += math.log(p)

        # classify
        result = 1
        if P_is_not_1 > P_is_1:
            result = -1
        if result == view:
            correct += 1
        total += 1

    return correct, total


def main():
    des_table, title_table, p_view = train()
    correct, total = test(des_table, title_table, p_view)
    print(correct, 'correct test from', total)
    print('accuracy:', correct / total)


if __name__ == '__main__':
    main()

print('done')
