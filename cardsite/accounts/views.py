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
        return generic_response( request, 'Log out successful!' )
    else:
        return generic_response( request, 'You are not logged in' )


def start_session( request ):
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate( request, username=username, password=password )
    if user is not None:
        auth.login( request, user )
        return redirect('/')
    else:
        return login()

def join( request ):
    return render(
            request,
            'base.html',
            {}
        )
