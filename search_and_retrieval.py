from query_check import query_check


class SearchAndRetrieval:
    def __init__(self, my_index):
        self.my_query_check = query_check(my_index)
        self.run()

    def run(self):
        # todo create user interface
        pass
