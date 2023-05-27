from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.test import Client
from django.contrib import messages
from markdown2 import Markdown
import random
from . import util
import re


markdowner = Markdown()

client = Client()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if entry_found := util.compare_input_entry(title):
        html = markdowner.convert(util.get_entry(entry_found))
        return render(request, "encyclopedia/entry.html", {"title":entry_found, "content":html})
    else:
        return HttpResponseNotFound()

    if request.GET.get("edit"):
        return render(request, "encyclopedia/new_page.html", {"title":entry_found, "content": util.get_entry(entry_found)})

def search(request):
    user_input = request.GET['q']
    response = client.get(f"/wiki/{user_input}")
    if response.status_code != 404:
        return HttpResponseRedirect(f"/wiki/{user_input}")
    
    else:
        results = []
        if entry_found := util.compare_input_entry(user_input):
                results.append(entry_found)
        return render(request, "encyclopedia/search_results.html", {"found":results})

def new_page(request):

    # if request.method == "GET" and request.GET.get("edit"):
    #     pre_url = request.META.get('HTTP_REFERER')
    #     result = re.search(r".+/wiki/(\w+)", pre_url)
    #     if entry_found := util.compare_input_entry(result.group(1)):
    #         return render(request, "encyclopedia/new_page.html", {"result":result, "title": entry_found, "content": util.get_entry(entry_found)})
    #     else:
    #         return render(request, "encyclopedia/new_page.html")
        
    # else:
    if request.method == "POST":
        title = request.POST['title']
        if request.POST.get("save"):
            if util.compare_input_entry(title):
                messages.error(request, "The title already exists!")
                return render(request, "encyclopedia/new_page.html", {"title":title, "content":request.POST["content"]})

        util.save_entry(title, request.POST['content'])
        return HttpResponseRedirect(f"/wiki/{title}")
    
def random_page(request):
    return HttpResponseRedirect(f"/wiki/{random.choice(util.list_entries())}")