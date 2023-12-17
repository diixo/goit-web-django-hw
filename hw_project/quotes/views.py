from django.shortcuts import render

from .utils.add_news_as_quotes import get_json_db

# Create your views here.

def main(request):
    db = get_json_db()
    quotes = db.quotes
    return render(request, "quotes/index.html", context={'quotes': quotes})
