from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from . import util
from django.test import Client

client = Client()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    func_output = util.create_template(title)
    if func_output:
        return render(request, f"encyclopedia/{func_output['filename']}.html",
                      {"title":func_output["html_title"], "content":func_output["content"]})   
    return HttpResponseNotFound()


def search(request):
    user_input = request.GET['q']
    response = client.get(f"/wiki/{user_input}")
    if response.status_code != 404:
        return entry(request, user_input)
    
    else:
        entries = util.list_entries()
        results = []
        for item in entries:
            if user_input.lower() in item.lower():
                results.append(item)
        return render(request, "encyclopedia/search_results.html", {"found":results})

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")

    