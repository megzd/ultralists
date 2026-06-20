from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.models import List, Item
from lists.forms import ItemForm, ExistingListItemForm

# views take requests, process data, and return responses
# they contain the business logic and interact with models and templates
# request is a required argument and the extra arguments are taken from URL patterns (urls.py)

def home_page(request):
    # returns an HTTP response object, containing a rendered HTML page and passes variables to the template
    # arguments: the HTTP request, the path to the template to render, a dictionary context data to inject into the template
    return render(request, "lists/home.html", {"form": ItemForm()})

# creates a unique list when the first item is added
def create_list(request):
    form = ItemForm(data=request.POST)

    if form.is_valid():
        createlist = List.objects.create()
        form.save(for_list=createlist)
        # returns an HTTP response redirect object
        # arguments: the URL (or its name), the URL's arguments
        # redirects to user_list
        return redirect(createlist)
    else:
        return render(request, "lists/home.html", {"form": form})

# displays a list and its items
def user_list(request, list_id):
    userlist = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=userlist)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=userlist, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(userlist)

    return render(request, "lists/list.html", {"list": userlist, "form": form})
