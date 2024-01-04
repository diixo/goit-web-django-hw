from django.shortcuts import render
from django.core.paginator import Paginator

from .utils.add_news_as_quotes import get_json_db
import threading
import time


class TimingThread(object):

    def __init__(self, interval=60):
        #super().__init__()
        self.interval = interval
        self._stop_event = threading.Event()
        self._stop_event.set()
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

parsing_thread = TimingThread()


def main(request, page=1):
    global parsing_thread

    is_active_parsing = False

    if request.method == 'POST':

        #form = MyForm(request.POST)
        #if form.is_valid():

        button_value = request.POST.get('action')

        if button_value == "activate_parsing":
            if parsing_thread._stop_event.is_set():
                parsing_thread.start()
                is_active_parsing = True
            else:
                print(">>> stopping")
                parsing_thread.stop()
                is_active_parsing = False
                print("<<< stopped")
                parsing_thread = TimingThread()


    db = get_json_db()
    quotes = db.data
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    return render(request, "quotes/index.html", 
        context={'quotes': quotes_on_page, "is_activated_parsing": is_active_parsing})
