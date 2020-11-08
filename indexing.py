# ted_talk = 'data/ted_talk.csv'
# persian = 'data/Persion.xml'

class indexing:
    def __init__(self):
        self.ted_talk = {}  # ted_talk['school:title'] = [2 , 3, 4, ...]
        self.persian = {}  #
        self.indexing()

    def get_ted_talk_dictionary(self):
        return self.ted_talk

    def get_persian_dictionary(self):
        return self.persian

    def indexing(self):
        # for on ducument : prepare text; add to dictionary
        pass