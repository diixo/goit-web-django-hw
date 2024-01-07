import json
from core.qq_grammar import str_to_ngrams

class QuotesProvider:
    def __init__(self) -> None:
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

            i = 0
            for k in headings.keys():
                i = i+1
                author = "author-" + str(i)
                data = dict()
                data['quote'] = k
                data['tags'] = ["tag-0", "tag-1"]
                data['author'] = author
                self.quotes.append(data)
            ##########################################################################
            self.data = self.quotes[-100:][::-1]
            ##########################################################################
            for item in self.data:
                ngrams = str_to_ngrams(item['quote'], stopwords=stopwords)
                ngrams = [" ".join([w for w in grm]) for grm in ngrams]
                item['tags'] = ngrams
                #item['tags'] = [grm for grm in ngrams if grm.lower() in keywords]

db_client = QuotesProvider()


def get_json_db():
    return db_client
