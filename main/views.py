from django.http import (HttpResponse,
                         HttpResponseForbidden, 
                         HttpResponseNotFound)
from django.shortcuts import redirect 
from djangohelpers import (rendered_with,
                           allow_http)

@allow_http("GET")
@rendered_with("main/home.html")
def home(request):
    return {}
