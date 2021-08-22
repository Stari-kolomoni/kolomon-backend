from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Returns a Hello World to browser
def hello_world(request: HttpRequest):
    return HttpResponse("Hello world")
