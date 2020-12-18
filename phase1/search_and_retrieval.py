from phase1.lnc_ltc import LNC_LTC
from phase1.query_check import query_check


class SearchAndRetrieval:
    def __init__(self, my_index):
        self.my_query_check = query_check(my_index)
        self.lnc_ltc = LNC_LTC(my_index)
        # self.run()

    def run(self):
        query = input("Enter search Query:")
        sub_section = input("Enter a subsection:")
        doc_class = int(input("Enter Document class views (1/-1):"))

        modified_query = self.my_query_check.spell_corrector(query, sub_section)
        print("Suggestion:", modified_query)
        results = self.lnc_ltc.get_query_results(modified_query, sub_section, doc_class)
        print("Result Docs:\n", ", ".join([str(i) for i in results]))
