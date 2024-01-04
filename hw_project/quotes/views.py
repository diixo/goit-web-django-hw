from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.signals import request_finished 
# for request_finished.connect(stop_thread)

from .utils.add_news_as_quotes import get_json_db
import threading
import time 

class TimingThread(object):

    def __init__(self, interval=5):
        #super().__init__()
        self.interval = interval
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        #self.thread.start()

    def run(self):
        while not self._stop_event.is_set():
            # Do something
            print('Doing something imporant in the background, interval:', self.interval)
            time.sleep(self.interval)

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def start(self):
        self._stop_event.clear()
        self.thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("TimingThread::__exit__")
        self.stop()

#example = TimingThread()

def stop_thread(sender, **kwargs):
    pass
    #example.stop()

def main(request, page=1):
    db = get_json_db()
    quotes = db.data
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", 
        context={'quotes': quotes_on_page, "parsing_is_active": False})
