from django.shortcuts import redirect, render
from lists.models import List, Item

# views take requests, process data, and return responses
# they contain the business logic and interact with models and templates
# request is a required argument and the extra arguments are taken from URL patterns (urls.py)

def home_page(request):
    # returns an HTTP response object, containing a rendered HTML page and passes variables to the template
    # arguments: the HTTP request, the path to the template to render, a dictionary context data to inject into the template
    return render(request, "home.html")

# creates a unique list when the first item is added
def create_list(request):
    createlist = List.objects.create()
    # POST[] accesses the dictionary-like data within the POST's body
    Item.objects.create(text=request.POST["item_text"], list=createlist)
    # returns an HTTP response redirect object
    # arguments: the URL (or its name), the URL's arguments
    # redirects to view_list
    return redirect(f"/lists/{createlist.id}/")

# displays a list and its items
def view_list(request, list_id):
    viewlist = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": viewlist})

# adds an item to an existing list
def add_item(request, list_id):
    viewlist = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=viewlist)
    # redirects to view_list
    return redirect(f"/lists/{viewlist.id}/")
