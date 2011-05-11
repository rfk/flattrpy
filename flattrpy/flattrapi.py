
import httplib
import urlparse
import time
import oauth.oauth as oauth


KEY = "UcoQnGyfSbk6Jkzjoi2806psm4dQy3Lj50ZjxopfqzcZKB9YJ1XAYcSa6WRuPsDL"
SECRET = "jtUHHaNYAPNagMZQEMgsOYtLLa6rtA2DUNasONgesTeyw3e1GlkkaDWLES3XjWq3"
CALLBACK_URL = 'http://flattrpy.ep.io/ready'


class FlattrAPI(object):

    REQUEST_TOKEN_URL = 'https://api.flattr.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.flattr.com/oauth/access_token'
    AUTHORIZATION_URL = 'https://api.flattr.com/oauth/authenticate'

    def __init__(self,key,secret,token=None):
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.sigmethod = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.token = None
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = httplib.HTTPSConnection("api.flattr.com")
        return self._connection

    def request(self,method,url,body="",headers={},**kwds):
        #  Grab any optional oauth parameters for the call
        callback = kwds.pop("callback",None)
        token = kwds.pop("token",self.token)
        verifier = kwds.pop("verifier",None)
        if kwds:
            raise TypeError("unexpected kwds: " + kwds)
        #  Do the requisite signing using whatever info we have.
        oa = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,
            token = token,
            verifier = verifier,
            callback = callback,
            http_method = method,
            http_url = url,
        )
        oa.sign_request(self.sigmethod, self.consumer, self.token)
        headers.update(oa.to_header())
        #  Flattr doesn't like full URLs in request line, only paths.
        u = urlparse.urlsplit(url)
        reqpath = u.path
        if u.query:
            reqpath += "?" + u.query
        #  Actually send the request.
        self.connection.request(method, reqpath, body=body, headers=headers)
        return self.connection.getresponse()

    def request_access_token(self, callback, access_scope="read"):
        response = self.request("GET",self.REQUEST_TOKEN_URL,callback=callback)
        token = oauth.OAuthToken.from_string(response.read())
        request = oauth.OAuthRequest.from_token_and_callback(token=token, http_url=self.AUTHORIZATION_URL)
        request.parameters["access_scope"] = access_scope
        return request.to_url()

    def claim_access_token(self, token, verifier):
        kwds = dict(token=token,verifier=verifier) 
        response = self.request("GET",self.ACCESS_TOKEN_URL,**kwds)
        self.token = oauth.OAuthToken.from_string(response.read())
        return self.token

