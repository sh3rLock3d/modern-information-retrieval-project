class query_check:
	def __init__(self, compress):
		pass

	def spell_corrector(self,query):
		modified_query = []
		k_gram_dictionary_list = []
		selected_k_gram_dictionary = []
		query_words = query.split(" ")
		for word in query_words:
			if check_query_is_misspelled(word):
				for k_gram in KGDictionary.get_k_grams(word):
					k_gram_dictionary_list.append(get_k_gram_dictionary(k_gram))

				for i in range(len(k_gram_dictionary_list) - 1):
					if jaccard_similarity(k_gram_dictionary_list[i],k_gram_dictionary_list[i+1]) > 0.5:
						selected_k_gram_dictionary.extend(list(set(k_gram_dictionary_list[i])), set(k_gram_dictionary_list[i]))

				intersection = set.intersection(*selected_k_gram_dictionary)
				word_min = ("",float('inf')) 	
				for selected_word in intersection:
					editDistance_value = editDistance(selected_word,word,len(selected_word),len(word))
					if editDistance_value < word_min[1]:
						word_min = selected_word,editDistance_value
				modified_query.append(word_min[0])
			else:
				modified_query.append(word)
		return " ".join(modified_query)
			
		

	def check_query_is_misspelled(self,word):
		# TODO check if query is in IIDictionary
		pass

	def get_k_gram_dictionary(self,k_gram):
		# TODO get k_gram dictionary
		pass
				

	def jaccard_similarity(self,query, document):
		intersection = set(query).intersection(set(document))
		union = set(query).union(set(document))
		return len(intersection)/len(union)
	def editDistance(str1, str2, m, n): 

		if str1[m-1]== str2[n-1]: 
		    return editDistance(str1, str2, m-1, n-1) 
	 
		return 1 + min(editDistance(str1, str2, m, n-1),    # Insert 
		               editDistance(str1, str2, m-1, n),    # Remove 
		               editDistance(str1, str2, m-1, n-1)    # Replace 
		               ) 
