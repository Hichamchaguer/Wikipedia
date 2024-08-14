from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
import markdown2
from django.urls import reverse


from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,entry):
    mark=Markdown()
    pages=util.get_entry(entry)
    if pages is None:
        return render(request,'encyclopedia/nonExistingEntry.html',{
            "entrytile":entry
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "entry":mark.convert(pages),
            'entrytitle':entry
        })

def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry' : value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/index.html",{
            "entries": subStringEntries,
            "search": True,
            "value": value
        })

