from functools import reduce


class Compress:
    def __init__(self, indexing):
        self.indexing = indexing
        self.compress()

    def compress(self):
        pass


class Gamma_Code:
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


# if __name__ == '__main__':
#     c = Gamma_Code()
#     print(c.gamma_decoder(c.gamma_encoder([1, 2, 3])))
#     # print(c.gamma_decoding(c.gamma_encoding([10, 15, 22, 23, 34, 44, 50, 58])))
