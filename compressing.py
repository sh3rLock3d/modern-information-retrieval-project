from functools import reduce
from indexing import KGDictionary


class Compress:
    def __init__(self, indexing):
        self.indexing = indexing
        self.compress()

    def compress(self):
        pass


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
        for i in range(len(bytestream)//8):
            numbers.append(bytestream[8*i:8*(i+1)])
        count = 0
        sum = 0
        for i in range(len(numbers)):
            if int(numbers[i],2) <128:
                count += 1
            else:
                for j in range(count,-1,-1):
                    if j !=0:
                        sum +=int(numbers[i-j],2) * 128 ** (j)
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

if __name__ == '__main__':
    pass
    # TODO
    #c = VariableByteCode()
    #print(c.decode(c.encode([824, 829, 215406])))
    # print(c.gamma_decoding(c.gamma_encoding([10, 15, 22, 23, 34, 44, 50, 58])))
