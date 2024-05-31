from django.shortcuts import render

def generic_response( request, message ):
    return render(
            request,
            'base.html',
            {
                'message': message
            }
        )
