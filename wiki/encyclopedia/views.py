from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from django.core.files.storage import default_storage
from . import util
from markdown2 import Markdown


markdowner = Markdown()

template = '''{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{ title }}
{% endblock %}

{% block body %}

    {{ content | safe }}

{% endblock %}'''

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):

    for item in util.list_entries():
        if title.lower() == item.lower():
            requested_entry = util.get_entry(title)
            html = markdowner.convert(requested_entry)
            util.write_html(title, template)        
            return render(request, f"encyclopedia/{title}.html", {"title":item, "content":html})
    
    return HttpResponseNotFound()


def search(request, user_input):
    
    get_entry_result = entry(request, user_input)
    
    if not isinstance(get_entry_result, HttpResponse):
        return get_entry_result()
            
    
    
    
        
    

