from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.test import Client
from django.contrib import messages
from markdown2 import Markdown
from . import util
import re


markdowner = Markdown()

client = Client()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entries = util.list_entries()
    for item in entries:
        if item.lower() == title.lower():
            html = markdowner.convert(util.get_entry(item))
            return render(request, "encyclopedia/entry.html", {"title":item, "content":html})
    return HttpResponseNotFound()

def search(request):
    user_input = request.GET['q']
    response = client.get(f"/wiki/{user_input}")
    if response.status_code != 404:
        return HttpResponseRedirect(f"/wiki/{user_input}")
    
    else:
        entries = util.list_entries()
        results = []
        for item in entries:
            if user_input.lower() in item.lower():
                results.append(item)
        return render(request, "encyclopedia/search_results.html", {"found":results})

def new_page(request):
    pre_url = request.META.get('HTTP_REFERER')
    result = re.search(r".+/wiki/(\w+)", pre_url)
    if request.method == "GET":
        if result:
            return 
        

        # import pdb; pdb.set_trace()
        return render(request, "encyclopedia/new_page.html")
    
    else:
        title = request.POST['title']
        if title in util.list_entries():
            messages.error(request, "The title already exists!")
            return HttpResponseRedirect("/new")
        else:
            util.save_entry(title, request.POST['content'])
            return HttpResponseRedirect(f"/wiki/{title}")