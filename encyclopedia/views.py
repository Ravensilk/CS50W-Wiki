from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.http import HttpResponse
from django.contrib import messages
from .util import get_entry, list_entries, save_entry
from markdown2 import Markdown
import random
from . import util

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}), label="")


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border border-secondary', 'placeholder': 'Title'}), label="")
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control addbody mt-2 border border-secondary', 'placeholder': 'Markdown'}), label="")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control addbody mt-2 border border-secondary', 'placeholder': 'Markdown'}), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 'form': SearchForm()
    })

markdowner = Markdown()

def title(request, keyword):
    entry = get_entry(keyword)
    if entry:
        entry = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry, 'form': SearchForm(), 'title': keyword
        })
    else:
        return redirect(reverse("entry_error"))

def entry_error(request):
    return render(request, "encyclopedia/error.html", {
        'form': SearchForm()
    })

def search(request):
    if request.method == "POST":
        titles = list_entries()
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query in titles:
                return redirect(reverse("title", kwargs={'keyword': query}))
            else:
                query_list = []
                for title in titles:
                    if str(query).lower() in title.lower():
                        query_list.append(title)
                return render(request, "encyclopedia/search.html", {
                    'query_list': query_list, 'form': SearchForm(), 'query': query
                })
        else:
            return render(request, "encyclopedia/search.html", {
                    'query_list': query_list, 'form': SearchForm()
                })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            titles = list_entries()
            titles = [entry.lower() for entry in titles]

            if title.lower() in titles:
                messages.error(request, f"This entry already exists! Try searching {title} using the Search box to read about it.")
                return render(request, "encyclopedia/add.html", {
                'form': SearchForm(), 'addform': form
            })

            try:
                save_entry(title, content)
                messages.success(request, "Your entry was successfully added!")
                return redirect(reverse("title", kwargs={'keyword': title}))

            except:
                messages.error(request, "Something went wrong while adding your entry. Try again later.")
                return render(request, "encyclopedia/add.html", {
                'form': SearchForm(), 'addform': form
            })

        else:
            messages.error(request, "Invalid entry! Try again.")
            return render(request, "encyclopedia/add.html", {
                'form': SearchForm(), 'addform': form
            })


    else:
        return render(request, "encyclopedia/add.html", {
            'form': SearchForm(), 'addform': NewEntryForm()
        })

def edit(request, title):

    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():

            content = form.cleaned_data["content"]

            try:
                save_entry(title, content)
                messages.success(request, "Your entry was successfully edited!")
                return redirect(reverse("title", kwargs={'keyword': title}))

            except:
                messages.error(request, "Something went wrong while editing your entry. Try again later.")
                return render(request, "encyclopedia/add.html", {
                'form': SearchForm(), 'editform': form, 'title': title
            })

    else:
        content = get_entry(title)
        form = EditEntryForm(initial={'title': title, 'content': content})
        return render(request, "encyclopedia/edit.html", {
            'editform': form, 'title': title, 'form': SearchForm()
        })

def random_entry(request):
    titles = list_entries()
    title = random.choice(titles)
    return redirect(reverse("title", kwargs={'keyword': title}))
