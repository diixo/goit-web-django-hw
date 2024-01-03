import json

class QuotesProvider:
    def __init__(self) -> None:
        self.quotes = list()

        # the same as: ./quotes/utils/allainews-news.json
        with open('quotes/utils/allainews-news.json', 'r', encoding='utf-8') as fd:
            content = json.load(fd)
            headings = content.get("headings", dict())

            i = 0
            for k in headings.keys():
                i = i+1
                author = "author-" + str(i)
                data = dict()
                data['quote'] = k
                data['tags'] = ["tag-0", "tag-1"]
                data['author'] = author
                self.quotes.append(data)

        self.data = self.quotes[-100:][::-1]

db_client = QuotesProvider()


def get_json_db():
    return db_client
