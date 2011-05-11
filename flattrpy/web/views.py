
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.generic.simple import *
from django.http import HttpResponse, HttpResponseRedirect

from flattrpy.flattrapi import FlattrAPI, oauth

KEY = "UcoQnGyfSbk6Jkzjoi2806psm4dQy3Lj50ZjxopfqzcZKB9YJ1XAYcSa6WRuPsDL"
SECRET = "jtUHHaNYAPNagMZQEMgsOYtLLa6rtA2DUNasONgesTeyw3e1GlkkaDWLES3XjWq3"


@csrf_protect
def index(request):
    if request.method == "POST":
        api = FlattrAPI(KEY,SECRET)
        return HttpResponseRedirect(api.request_access_token("http://flattrpy.ep.io/oauth_callback"))
    return direct_to_template(request, template="index.html")

def oauth_callback(request):
    token = request.GET["oauth_token"]
    verifier = request.GET["oauth_verifier"]
    api = FlattrAPI(KEY,SECRET)
    token = api.claim_access_token(token,verifier)
    return HttpResponse(token.to_string())

