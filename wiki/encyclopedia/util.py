import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown

markdowner = Markdown()

template = '''{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{ title }}
{% endblock %}

{% block body %}

    {{ content | safe }}

{% endblock %}'''

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def write_html(title, content):
    
    filename = f"templates/encyclopedia/{title}.html"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    

def create_template(user_input):
    
    entries = list_entries()
    for entry in entries:
        if entry == user_input.lower():
            requested_entry = get_entry(entry)
            html = markdowner.convert(requested_entry)
            write_html(entry, template)    
            return {"filename":entry, "html_title":entry, "content":html}
    return None
    