from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse

from .models import CardAllocation, CardStash

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

def __get_headers( request, headers ):
    return { k:v for k,v in request.POST.items() if k in headers }

def create_stash_entry( request, StashModel, headers ):
    kwargs = __get_headers( request, headers )
    new_entry = StashModel.objects.create( **kwargs )
    return HttpResponse( "Deck created" )

def update_calloc( request, stash_uuid ):
    try:
        card_id = request.POST['card_id']
        quantity = request.POST['quantity']
    except KeyError:
        return HttpResponse( "JavaScript didn't send expected POST data?" ) 
    if int(quantity) < 1:
        try:
            CardAllocation.objects.get(
                    stash_id=stash_uuid,
                    card_id=card_id
                ).delete()
            return HttpResponse( "Removed from deck" )
        except ObjectDoesNotExist:
            return HttpResponse( "Moot" )
    # JS should avoid POST if nothing changed to avoid pointless SQL
    obj, created = CardAllocation.objects.update_or_create(
            stash_id = stash_uuid,
            card_id = card_id,
            defaults = { "n_card_in_stash": quantity },
        )
    return HttpResponse( "Entry updated!" )
