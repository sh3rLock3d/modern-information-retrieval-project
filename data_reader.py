

def read_train_data():
    import pandas as pd
    ted_talk_data = pd.read_csv('phase2/phase2_data/train.csv')
    result_wikis = []
    for index, doc in enumerate(ted_talk_data[['title', 'description', 'views']].values):
        title = doc[0]
        description = doc[1]
        view = doc[2]
        result_wikis.append({'id': index, 'title': title, 'description': description, 'views': view})
    return result_wikis


def read_test_data():
    import pandas as pd
    ted_talk_data = pd.read_csv('phase2/phase2_data/test.csv')
    result_wikis = []
    for index, doc in enumerate(ted_talk_data[['title', 'description', 'views']].values):
        title = doc[0]
        description = doc[1]
        view = doc[2]
        result_wikis.append({'id': index, 'title': title, 'description': description, 'views': view})
    return result_wikis


def read_data():
    import pandas as pd
    ted_talk_data_1 = pd.read_csv('phase2/phase2_data/train.csv')
    ted_talk_data_2 = pd.read_csv('phase2/phase2_data/test.csv')
    dfs = []
    dfs.extend([ted_talk_data_1, ted_talk_data_2])
    ted_talk_data = pd.concat(dfs)
    result_wikis = []
    for index, doc in enumerate(ted_talk_data[['title', 'description', 'views']].values):
        title = doc[0]
        description = doc[1]
        view = doc[2]
        result_wikis.append({'id': index, 'title': title, 'description': description, 'views': view})
    return result_wikis


def reading_persian():
    import xmltodict
    with open("phase1/phase1_data/Persian.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    result_wikis = []
    for page in data_dict['mediawiki']['page']:
        text = page['revision']['text']['#text']
        title = page['title']
        result_wikis.append({'id': int(page['id']), 'title': title, 'text': text})
    return result_wikis


def reading_ted_talk():
    import pandas as pd
    ted_talk_data = pd.read_csv('phase1/phase1_data/ted_talks.csv')
    result_wikis = []
    for index, doc in enumerate(ted_talk_data[['title', 'description']].values):
        description = doc[1]
        title = doc[0]
        result_wikis.append({'id': index, 'title': title, 'description': description})
    return result_wikis

