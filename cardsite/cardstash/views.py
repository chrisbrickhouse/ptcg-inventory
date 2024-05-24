from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse

from .models import CardStash

def index( 
          request, 
          StashModel, 
          context_name, 
          template_name,
          order_by = "created", 
        ):
    list_of_stashes = StashModel.objects.order_by( order_by )
    context = { context_name: list_of_stashes }
    return render(
            request,
            template_name,
            context = context,
        )

def new_stash( 
              request, 
              StashModel, 
              fields,
              labels,
              form_snippet = "cardstash/bootstrap_form_group_snippet.html",
              template_name = "cardstash/new_stash_form.html",
        ):
    NewStashForm = modelform_factory(
            StashModel,
            fields = fields,
            labels = labels,
        )
    context = { "form": NewStashForm().render( form_snippet ) }
    return render(
            request,
            template_name,
            context
        )

def create_stash_entry( request, StashModel, headers ):
    kwargs = { k: v for k,v in request.POST.items() if k in headers }
    new_entry = StashModel.objects.create( **kwargs )
    return HttpResponse( "Deck created" )
