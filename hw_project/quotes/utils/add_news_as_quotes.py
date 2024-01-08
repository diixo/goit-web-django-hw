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
                data['tags'] = ["tag-0", "tag-1"]
                data['author'] = author
                self.quotes.append(data)
            ##########################################################################
            self.data = self.quotes[-100:][::-1]
            ##########################################################################
            for item in self.data:
                ngrams = qq.str_to_ngrams(item['quote'], stopwords=stopwords)
                ngrams = [" ".join([w for w in grm]) for grm in ngrams]
                item['tags'] = ngrams
                #item['tags'] = [grm for grm in ngrams if grm.lower() in keywords]

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
