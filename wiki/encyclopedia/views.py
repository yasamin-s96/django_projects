from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpRequest
from django.core.files.storage import default_storage
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    
    func_output = util.create_template(title)
    if func_output:
        return render(request, f"encyclopedia/{func_output['filename']}.html", {"title":func_output["html_title"], "content":func_output["content"]})
    # for item in util.list_entries():
    #     if title.lower() == item.lower():
    #         requested_entry = util.get_entry(title)
    #         html = markdowner.convert(requested_entry)
    #         util.write_html(title, template)            
    return HttpResponseNotFound()


def search(request):
    
    get_entry_result = entry(request, request.GET["q"])
    
    if not isinstance(get_entry_result, HttpResponse):
        return get_entry_result()
            
    
    
    
        
    

