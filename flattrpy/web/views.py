
import urllib

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.generic.simple import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect,\
                        HttpResponseForbidden

from django.contrib.auth import login, logout

from flattrpy.api import FlattrAPI
from flattrpy import secrets

from flattrpy.web.models import APIToken, User, Project


def login_required(view):
    """Work-alike for @login_required, using OAuth tokens rather than passwords.

    If we find that the user is not logged in, we make them go through the
    Flattr OAuth dance and obtain a new token as proof of who they are.
    """
    def check_login(request,*args,**kwds):
        if not request.user.is_authenticated():
            api = FlattrAPI(secrets.FLATTR_API_KEY,secrets.FLATTR_API_SECRET)
            callback = reverse(oauth_callback)
            callback += "?next=" + urllib.quote(request.get_full_path(),"")
            callback = request.build_absolute_uri(callback)
            (token,url) = api.request_access_token(callback,"click")
            print "OBTAINING REQ TOKEN", token.key, token.secret
            t = APIToken.objects.create(id=token.key,secret=token.secret)
            t.save()
            print "REDIRECTING TO", url
            return HttpResponseRedirect(url)
        return view(request,*args,**kwds)
    return check_login


def index(request):
    return direct_to_template(request, template="index.html")


@csrf_protect
@login_required
def flattrit(request):
    if request.method != "POST":
        return HttpResponseForbidden()
    return direct_to_template(request, template="flattrit.html")


def oauth_callback(request):
    api = FlattrAPI(secrets.FLATTR_API_KEY,secrets.FLATTR_API_SECRET)
    #  Grab the request token and verifier
    verifier = request.GET["oauth_verifier"]
    key = request.GET["oauth_token"]
    secret = APIToken.objects.get(id=key).secret
    print "USING REQ TOKEN", key, secret
    token = api.make_token(key,secret)
    #  Convert it into an access token
    token = api.claim_access_token(token,verifier)
    #  Record the token with the current user, creating if necessary.
    try:
        user = User.objects.get(id=api.user.id)
    except User.DoesNotExist:
        user = User.objects.create(id=api.user.id,
                                   username=api.user.username,
                                   email=api.user.email)
                                   
        user.set_unusable_password()
        user.save()
    t = APIToken.objects.create(id=token.key,
                                secret=token.secret,
                                user=api.user.id)
    t.save()
    #  Log them in as this user.
    login(request,user)
    #  Redirect to wherever they wanted to go.
    next = request.GET.get("next","/")
    return HttpResponseRedirect(request.build_absolute_uri(next))


