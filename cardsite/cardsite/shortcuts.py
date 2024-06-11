from django.shortcuts import render

def generic_response( 
        request, 
        message, 
        header='',
        title = "Where's that Pokemon?",
        is_safe = False,
    ):
    """Provide a generic response page

    Arguments:
        request (django.http.HttpRequest): The request instance to operate on.
        message (str): A string of text to display to the user.
        header (str): A heading to put in `<h1></h1>` tags on the page.
        title (str): Content to put in the title of the page.
        is_safe (bool): Should this be output without escaping? Default is false
            and you should not set this to True unless you are displaying text
            that is not user-generated or have escaped prior to adding formatting.
    """
    return render(
            request,
            'generic_response.html',
            {
                'message': message,
                'header': header,
                'title': title,
                'is_safe': is_safe,
            }
        )
