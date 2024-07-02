from django.shortcuts import render, redirect
from django.contrib import auth

from cardsite.shortcuts import generic_response

# Create your views here.
def index( request ):
    return render(
            request,
            'base.html',
            {}
        )

def login( request ):
    # TODO: Migrate to LoginView https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.LoginView
    return render(
            request,
            'accounts/login_form.html',
            {}
        )

def logout( request ):
    if request.user.is_authenticated:
        auth.logout( request )
        return generic_response( 
                request, 
                message = '<p>Log out successful!</p>',
                header = 'Logged out',
                is_safe = True,
            )
    else:
        return generic_response( 
                request,
                message = '<p>You are not logged in</p>',
                header = "Cannot log out",
                is_safe = True,
            )


def start_session( request ):
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate( request, username=username, password=password )
    if user is not None:
        auth.login( request, user )
        return redirect('/')
    else:
        return login(request)

def join( request ):
    message = "<p><em>Where's that Pokemon?</em> is currently in closed beta. As of 1 June 2024, accounts are granted on an invite-only basis. There are no plans for an open beta yet, but in the near future we may set up a waiting list for account requests. Check this page later for a request form!</p>"
    header = "Interested in joining?"
    return generic_response(
            request,
            message,
            header,
            title = "Join!",
            is_safe = True,
        )
