from django.shortcuts import render
from django.core.paginator import Paginator

from .utils.add_news_as_quotes import get_json_db
import threading

class TimingThread(object):

    def __init__(self, interval, callback, context = {}):
        #super().__init__()
        self.interval = interval
        self._callback = callback
        self._context = context
        self._stop_event = threading.Event()
        self._stop_event.set()
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True

    def run(self):
        while not self._stop_event.is_set():
            is_set = self._stop_event.wait(timeout=self.interval)
            #print(f'TimingThread::TimeOut {self.interval} has ended')
            
            if self._stop_event.is_set():
                print("<< is_set: exit from Thread by event")
                break

            if is_set:
                print('TimingThread::Event processing code by WAIT_TIMEOUT()')
            else:
                self._callback(self._context)

        if self._stop_event.is_set():
            print("<< exit from Thread by event")


    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def start(self):
        self._stop_event.clear()
        self.thread.start()

def some_callback_1(context):
    context['count'] += 1
    print('callback:' + " count: " + str(context['count']))

#############################

parsing_thread = None


def main(request, page=1):
    global parsing_thread

    if request.method == 'POST':

        #form = MyForm(request.POST)
        #if form.is_valid():

        button_value = request.POST.get('action')

        if button_value == "activate_parsing":
            if parsing_thread == None:
                parsing_thread = TimingThread(interval=3, callback=some_callback_1, context={'count': 0})
                parsing_thread.start()
                print(">>> started")
            else:
                print(">>> stopping")
                parsing_thread.stop()
                parsing_thread = None
                print("<<< stopped")


    db = get_json_db()
    quotes = db.data
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    is_active_parsing = parsing_thread != None

    return render(request, "quotes/index.html", 
        context={'quotes': quotes_on_page, "is_activated_parsing": is_active_parsing})
