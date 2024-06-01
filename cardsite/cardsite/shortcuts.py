from django.shortcuts import render

def generic_response( request, message, header='' ):
    return render(
            request,
            'generic_response.html',
            {
                'message': message,
                'header': header,
            }
        )
