from django.shortcuts import render
from django.core.paginator import Paginator

from .utils.add_news_as_quotes import get_json_db

import threading, time 

class ThreadingExample(object):

    def __init__(self, interval=5):

        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):

        while True:
            # Do something
            print('Doing something imporant in the background, interval:', self.interval)
            time.sleep(self.interval)

# example = ThreadingExample()


def main(request, page=1):
    db = get_json_db()
    quotes = db.data
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={'quotes': quotes_on_page})
