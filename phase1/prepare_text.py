from __future__ import unicode_literals

import string

import hazm
import nltk


# nltk.download('punkt')
# nltk.download('wordnet')
# print('done')


class DictionaryProcess:
    def __init__(self, document):
        self.persian = False
        self.document = document
        self.tokens = []
        self.set_language()

    def set_language(self):
        ch = self.document[0]
        self.persian = self.check_persian(ch)

    @classmethod
    def check_persian(cls, ch):
        if ('\u0600' <= ch <= '\u06FF' or
                '\u0750' <= ch <= '\u077F' or
                '\u08A0' <= ch <= '\u08FF' or
                '\uFB50' <= ch <= '\uFDFF' or
                '\uFE70' <= ch <= '\uFEFF' or
                '\U00010E60' <= ch <= '\U00010E7F' or
                '\U0001EE00' <= ch <= '\U0001EEFF'):
            return True
        return False

    def normalization(self):
        if self.persian:
            normalizer = hazm.Normalizer()
            self.document = normalizer.normalize(self.document)
        else:
            self.document = self.document.lower()

    def tokenization(self):
        if self.persian:
            self.tokens = hazm.word_tokenize(self.document)
        else:
            self.tokens = nltk.word_tokenize(self.document)

    def delete_punctuation(self):
        def is_punctuation(word):
            if word in string.punctuation:
                return False
            if word in '!٬٫﷼٪×،*)(ـ+=-][}{|»«:؛><؟/\\':
                return False
            return True

        self.tokens = [value for value in self.tokens if is_punctuation(value)]

    def stemming(self):
        if self.persian:
            stemmer = hazm.Stemmer()
            lemmatizer = hazm.Lemmatizer()
            for i in range(len(self.tokens)):
                self.tokens[i] = lemmatizer.lemmatize(stemmer.stem(self.tokens[i]))
        else:
            porter = nltk.PorterStemmer()
            self.tokens = [porter.stem(word) for word in self.tokens]

            lemma = nltk.WordNetLemmatizer()
            self.tokens = [lemma.lemmatize(word, pos="v") for word in self.tokens]
            self.tokens = [lemma.lemmatize(word, pos="n") for word in self.tokens]

    def prepare_text(self):
        self.normalization()
        self.tokenization()
        self.delete_punctuation()
        self.stemming()
        return self.tokens

    def print(self):
        for i in self.tokens:
            print(i)

# fa = 'اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند.'
# en = """At eight o'clock on Thursday morning
# ... Arthur didn't feel very good."""
#a = DictionaryProcess(en)
#a.prepare_text()
#a.print()
