
import httplib
import urlparse
import oauth.oauth as oauth
import dexml.fields

class FlattrError(Exception):
    pass


class FlattrAPI(object):
    """Top-level object for accessing the Flattr API."""

    SERVER = "https://api.flattr.com"
    REQUEST_TOKEN_URL = "/oauth/request_token"
    ACCESS_TOKEN_URL = "/oauth/access_token"
    AUTHORIZATION_URL = "/oauth/authenticate"

    def __init__(self,key,secret,token=None):
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.sigmethod = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.token = None
        self._connection = None
        self._user = None

    @property
    def connection(self):
        if self._connection is None:
            hostname = urlparse.urlparse(self.SERVER).hostname
            self._connection = httplib.HTTPSConnection(hostname)
        return self._connection

    @property
    def user(self):
        if self._user is None:
            r = self.request("GET","/rest/0.5/user/me")
            e = envelope.parse(r.read())
            self._user = e.data
        return self._user

    def request(self,method,url,body="",headers={},**kwds):
        """Make a request to the Flattr web API.

        This method is performs a raw HTTP request to the Flattr web API.
        You'll want to give an oauth token before you can do must.
        """
        #  Grab any optional oauth parameters for the call
        callback = kwds.pop("callback",None)
        token = kwds.pop("token",self.token)
        verifier = kwds.pop("verifier",None)
        if kwds:
            raise TypeError("unexpected kwds: " + kwds)
        #  Flattr doesn't like full URLs in request line, only paths.
        u = urlparse.urlsplit(url)
        reqpath = u.path
        if u.query:
            reqpath += "?" + u.query
        if not u.hostname:
            if not url.startswith("/"):
                url = "/" + url
            url = self.SERVER + url
        #  Do the requisite request signing
        oa = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,
            token = token,
            verifier = verifier,
            callback = callback,
            http_method = method,
            http_url = url,
        )
        oa.sign_request(self.sigmethod, self.consumer, token)
        headers.update(oa.to_header())
        #  Actually send the request.
        self.connection.request(method, reqpath, body=body, headers=headers)
        return self.connection.getresponse()

    def make_token(self,key,secret):
        """Make a token object from a key and secret."""
        return oauth.OAuthToken(key,secret)

    def request_access_token(self,callback,access_scope="read"):
        """Begin the OAuth access-requesting dance.

        This method will return a temporary access token and a URL to which
        the user should be redirected.  This URL will ask them to grant the
        requested access, and then redirect them to the specified callback URL.
        """
        response = self.request("GET",self.REQUEST_TOKEN_URL,callback=callback)
        if not 200 <= response.status < 300:
            raise FlattrError(response.read())
        token = oauth.OAuthToken.from_string(response.read())
        request = oauth.OAuthRequest.from_token_and_callback(token=token, http_url=self.SERVER+self.AUTHORIZATION_URL)
        request.parameters["access_scope"] = access_scope
        return (token,request.to_url())

    def claim_access_token(self,token,verifier):
        """Complete the OAuth access-requesting dance.

        This method will convert a request token into an access token,
        assuming the user as granted the necessary permissions.
        """
        kwds = dict(token=token,verifier=verifier) 
        response = self.request("GET",self.ACCESS_TOKEN_URL,**kwds)
        if not 200 <= response.status < 300:
            raise FlattrError(response.read())
        self.token = oauth.OAuthToken.from_string(response.read())
        return self.token


class envelope(dexml.Model):
    class meta:
        tagname = "flattr"
    version = dexml.fields.String(tagname=True)
    data = dexml.fields.Choice("user")


class user(dexml.Model):
    id = dexml.fields.Integer(tagname=True)
    username = dexml.fields.String(tagname=True)
    gravatar = dexml.fields.String(tagname=True)
    email = dexml.fields.String(tagname=True)

    

