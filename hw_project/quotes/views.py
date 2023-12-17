from django.shortcuts import render
from django.core.paginator import Paginator

from .utils.add_news_as_quotes import get_json_db

# Create your views here.

def main(request, page=1):
    db = get_json_db()
    quotes = db.quotes
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={'quotes': quotes_on_page})
