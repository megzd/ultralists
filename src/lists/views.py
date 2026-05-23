from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.models import List, Item

# views take requests, process data, and return responses
# they contain the business logic and interact with models and templates
# request is a required argument and the extra arguments are taken from URL patterns (urls.py)

def home_page(request):
    # returns an HTTP response object, containing a rendered HTML page and passes variables to the template
    # arguments: the HTTP request, the path to the template to render, a dictionary context data to inject into the template
    return render(request, "lists/home.html")

# creates a unique list when the first item is added
def create_list(request):
    createlist = List.objects.create()
    # POST[] accesses the dictionary-like data within the POST's body
    new_item = Item.objects.create(text=request.POST["item_text"], list=createlist)
    try:
        new_item.full_clean()
        new_item.save()
    except ValidationError:
        createlist.delete()
        error = "You can't have an empty list item"
        return render(request, "lists/home.html", {"error": error})

    # returns an HTTP response redirect object
    # arguments: the URL (or its name), the URL's arguments
    # redirects to view_list
    return redirect(f"/lists/{createlist.id}/")

# displays a list and its items
def view_list(request, list_id):
    viewlist = List.objects.get(id=list_id)
    return render(request, "lists/list.html", {"list": viewlist})

# adds an item to an existing list
def add_item(request, list_id):
    viewlist = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=viewlist)
    # redirects to view_list
    return redirect(f"/lists/{viewlist.id}/")
