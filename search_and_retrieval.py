from query_check import query_check


class SearchAndRetrieval:
    def __init__(self, my_index):
        self.my_query_check = query_check(my_index)
        self.run()

    def run(self):
        while True:
            query = input("Enter search Query: ")
            sub_section = input("Enter a subsection:")

            modified_query = self.my_query_check.spell_corrector(query, sub_section)
            print("Suggestion:", modified_query)

