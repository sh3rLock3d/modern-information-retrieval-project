from indexing import Indexing
from functools import reduce
import math
import pickle
import sys


class GammaCode:
    def gamma_encoder(self, postings):
        return "".join(
            [self.get_length(self.get_offset(gap)) + self.get_offset(gap) for gap in self.get_gaps_list(postings)])

    def gamma_decoder(self, gamma):
        length, offset, aux, res = "", "", 0, []
        while gamma != "":
            aux = gamma.find("0")
            length = gamma[:aux]
            if length == "":
                res.append(1)
                gamma = gamma[1:]
            else:
                offset = "1" + gamma[aux + 1:aux + 1 + self.unary_decoder(length)]
                res.append(int(offset, 2))
                gamma = gamma[aux + 1 + self.unary_decoder(length):]
        for i in range(1, len(res)):
            res[i] = res[i] + res[i - 1]
        return res

    def get_offset(self, gap):
        return bin(gap)[3:]

    def get_length(self, offset):
        return self.unary_encoder(len(offset)) + "0"

    def unary_encoder(self, gap):
        return "".join(["1" for _ in range(gap)])

    def unary_decoder(self, gap):
        return reduce(lambda x, y: int(x) + int(y), list(gap))

    def get_gaps_list(self, posting_list):
        res = [posting_list[0]]
        for i in range(1, len(posting_list)):
            res.append(posting_list[i] - posting_list[i - 1])
        return res


class VariableByteCode:
    def encode_number(self, number):
        bytes_list = []
        while True:
            bytes_list.insert(0, number % 128)
            if number < 128:
                break
            number = number // 128
        bytes_list[-1] += 128
        return bytes_list

    def encode(self, postings_list):
        bytes_list = []
        for number in self.get_gaps_list(postings_list):
            for num in self.encode_number(number):
                bytes_list.append(f'{num:08b}')
        return "".join(bytes_list)

    def decode(self, bytestream):
        numbers = []
        posting_list = []
        for i in range(len(bytestream) // 8):
            numbers.append(bytestream[8 * i:8 * (i + 1)])
        count = 0
        sum = 0
        for i in range(len(numbers)):
            if int(numbers[i], 2) < 128:
                count += 1
            else:
                for j in range(count, -1, -1):
                    if j != 0:
                        sum += int(numbers[i - j], 2) * 128 ** (j)
                    else:
                        sum += int(numbers[i - j], 2) * 128 ** (j) - 128
                posting_list.append(sum)
                count = 0
                sum = 0
        for i in range(1, len(posting_list)):
            posting_list[i] = posting_list[i] + posting_list[i - 1]
        return posting_list

    def get_gaps_list(self, posting_list):
        res = [posting_list[0]]
        for i in range(1, len(posting_list)):
            res.append(posting_list[i] - posting_list[i - 1])
        return res


class CompressUtils:
    @classmethod
    def compress_with_gamma(self, indexing):
        G = GammaCode()	
        gamma_list = []
        position_list = []
        for key in indexing.ted_talk_ii.dictionary.keys():
            postings = [indexing.ted_talk_ii.dictionary.get(key)[1][i].doc_id for i in range(len(indexing.ted_talk_ii.dictionary.get(key)[1]))]
            positions = [indexing.ted_talk_ii.dictionary.get(key)[1][i].positions for i in range(len(indexing.ted_talk_ii.dictionary.get(key)[1]))]
            for position in positions:
                position_list.append(int(G.gamma_encoder(position),2).to_bytes(math.ceil(len(G.gamma_encoder(position)) / 8),sys.byteorder))
            gamma_list.append(int(G.gamma_encoder(postings),2).to_bytes(math.ceil(len(G.gamma_encoder(postings)) / 8),sys.byteorder))
        gamma_file_ii = open('gamma_code_ii', 'ab')
        pickle.dump((position_list,gamma_list),gamma_file_ii)
        gamma_file_ii.close()
        gamma_file_kg = open('gamma_code_kg', 'ab')
        pickle.dump(indexing.ted_talk_kg.dictionary,gamma_file_kg)
        gamma_file_kg.close()
    @classmethod
    def decode_with_gamma(self,keys,doc_freq):
        G = GammaCode()
        my_index = Indexing()
        gamma_file_ii = open('gamma_code_ii', 'rb')      
        gamma_position_list,gamma_list = pickle.load(gamma_file_ii)
        gamma_file_ii.close()
        position_list = []
        posting_list = []
        for posting in gamma_list:
            posting_list.append(G.gamma_decoder(str(format(int.from_bytes(posting,sys.byteorder),'b'))))
        for position in gamma_position_list:
            posting_list.append(G.gamma_decoder(str(format(int.from_bytes(position,sys.byteorder),'b'))))
        for i in range(len(keys)):
            postingItem_list = []
            for j in len(posting_list[i]):
                posting_item = indexing.IIDictionary.PostingItem(posting_list[i][j])
                posting_item.positions = position_list[i][j]
                my_index.ted_talk_ii.dictionay[keys[i]] = [doc_freq[i], posting_item]

        gamma_file_kg = open('gamma_code_kg', 'rb') 
        ted_talk_kg_dictionary = pickle.load(gamma_file_kg)
        my_index.ted_talk_ii.dictionay = ted_talk_kg_dictionary
        return my_index

    @classmethod
    def compress_with_variable_code(self, indexing):
        # TODO use variable code class to compress and save indexing to a file
        pass

    @classmethod
    def decode_with_variable_code(self):
        # TODO decode and create an indexing object from a file
        # return indexing
        pass

