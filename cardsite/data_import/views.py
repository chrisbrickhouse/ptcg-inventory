from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import TabularLoaderForm


def import_tabular(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TabularLoaderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TabularLoaderForm().render( 'cardstash/bootstrap_form_group_snippet.html' )

    return render(request, "data_import/tabular.html", {"form": form})
