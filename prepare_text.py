from __future__ import unicode_literals
import hazm
import string
import nltk


# nltk.download('punkt')
# nltk.download('wordnet')
# print('done')

class dictionary_process:
    def __init__(self, document, is_persian):
        self.document = document
        self.tokens = []
        self.persian = is_persian

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

    def stop_words(self):
        pass

    def stemming(self):
        if self.persian:
            stemmer = hazm.Stemmer()
            lemmatizer = hazm.Lemmatizer()
            for i in range(len(self.tokens)):
                self.tokens[i] = lemmatizer.lemmatize(stemmer.stem(self.tokens[i]))
        else:
            porter = nltk.PorterStemmer()
            self.tokens = [porter.stem(word) for word in self.tokens]

            # lemma = nltk.WordNetLemmatizer()
            # self.tokens = [lemma.lemmatize(word, pos="v") for word in self.tokens]
            # self.tokens = [lemma.lemmatize(word, pos="n") for word in self.tokens]

    def prepare_text(self):
        self.normalization()
        self.tokenization()
        self.delete_punctuation()
        self.stop_words()
        self.stemming()

    def print(self):
        for i in self.tokens:
            print(i)

# fa = 'اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند.'
# en = """At eight o'clock on Thursday morning
# ... Arthur didn't feel very good."""
# a = dictionary_process(en)
# a.prepare_text()
# a.print()
