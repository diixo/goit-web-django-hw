import json
import core.qq_grammar as qq

class QuotesProvider:

    def __init__(self) -> None:

        self.unigrams = set()
        self.bigrams = set()
        self.trigrams = set()

        self.quotes = list()
        self.data = []

        # the same as: ./quotes/utils/allainews-news.json
        with open('quotes/utils/allainews-news.json', 'r', encoding='utf-8') as fd:
            content = json.load(fd)
            headings = content.get("headings", dict())
            keywords = content.get("keywords", dict())

            ##########################################################################
            stopwords = set()
            with open('quotes/utils/stopwords.txt', 'r', encoding='utf-8') as fsw:
                stopwords.update([line.replace('\n', '') for line in fsw.readlines()])
            ##########################################################################

            for string in keywords:
                string = qq.translate(string)
                ngrams = qq.str_to_ngrams(string, stopwords)
                for tokens in ngrams:
                    self.add_tokens(tokens)
            ##########################################################################
            print(f"QuotesProvider::uni={len(self.unigrams)}, bi={len(self.bigrams)}, tri={len(self.trigrams)}")

            i = 0
            for heading in headings.keys():
                i = i + 1
                author = "author-" + str(i)
                data = dict()
                data['quote'] = heading
                data['author'] = author
                self.quotes.append(data)
            ##########################################################################
            self.data = self.quotes[-100:][::-1]
            ##########################################################################
            for item in self.data:
                heading = item['quote']
                item['tags'] = self.calculate_tags_ngrams(heading=heading, stopwords=stopwords)
                #item['tags'] = self.calculate_tags(heading=heading, stopwords=stopwords)

    def calculate_tags_ngrams(self, heading, stopwords=set()):
        ngrams = qq.str_to_ngrams(heading, stopwords=stopwords)
        ngrams = [" ".join([w for w in grm]) for grm in ngrams]
        return ngrams

    def calculate_tags(self, heading, stopwords=set()):
        grams = qq.str_to_ngrams(heading, stopwords)
        result = []
        for tokens in grams:
            ngrams_1 = qq.ngrams(tokens, 1)
            result.extend([" ".join(gram) for gram in ngrams_1 if gram in self.unigrams])
            
            ngrams_2 = qq.ngrams(tokens, 2)
            result.extend([" ".join(gram) for gram in ngrams_2 if gram in self.bigrams])
            
            ngrams_3 = qq.ngrams(tokens, 3)
            result.extend([" ".join(gram) for gram in ngrams_3 if gram is self.trigrams])
        return result

    def add_tokens(self, tokens: list):
        ngrams_1 = qq.ngrams(tokens, 1)
        ngrams_2 = qq.ngrams(tokens, 2)
        ngrams_3 = qq.ngrams(tokens, 3)

        self.unigrams.update(ngrams_1)  # unique inserting
        self.bigrams.update(ngrams_2)   # unique inserting
        self.trigrams.update(ngrams_3)  # unique inserting

db_client = QuotesProvider()


def get_json_db():
    return db_client
