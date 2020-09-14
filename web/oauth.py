import os
import urllib
import urllib.parse

from flask import redirect, request
from oauthlib.oauth1 import SIGNATURE_HMAC, SIGNATURE_TYPE_AUTH_HEADER, Client
from requests_oauthlib import OAuth1Session

from .config import Config

'''
OAuth for Warwick ITS helper methods
Heavily inspired by: https://github.com/UniversityofWarwick/python-warwick-sso-oauth-example
'''

CONSUMER_SECRET = Config.CONSUMER_SECRET
CONSUMER_KEY = Config.CONSUMER_KEY

ACCESS_TOKEN_URL = 'https://websignon.warwick.ac.uk/oauth/accessToken'
AUTHORISE_URL = 'https://websignon.warwick.ac.uk/oauth/authorise?'
REQUEST_TOKEN_URL = 'https://websignon.warwick.ac.uk/oauth/requestToken?'
SCOPES = 'urn:websignon.warwick.ac.uk:sso:service'

class WarwickClient(Client):
    def _render(self, request, formencode=False, realm=None):
        request.headers['User-Agent'] = os.getenv('OAUTH_USER_AGENT')
        return super()._render(request, formencode, realm)

def get_request_token_with_callback(verify_id, callback):
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET,
                          signature_method=SIGNATURE_HMAC,
                          signature_type=SIGNATURE_TYPE_AUTH_HEADER, client_class=WarwickClient,
                          callback_uri=callback)
    
    resp = oauth.fetch_request_token(
        url=REQUEST_TOKEN_URL + urllib.parse.urlencode({ 'scope': SCOPES, 'expiry': '10m' })
    )

    return {
        'token': resp['oauth_token'],
        'secret': resp['oauth_token_secret']
    }

def get_user_access_token(oauth_token_secret):
    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, resource_owner_secret=oauth_token_secret, client_class=WarwickClient)

    oauth.parse_authorization_response(request.url)
    access = oauth.fetch_access_token(ACCESS_TOKEN_URL)

    return {
        'token': access['oauth_token'],
        'secret': access['oauth_token_secret']
    }

def get_user_oauth_session(oauth_token, oauth_token_secret):
    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, resource_owner_key=oauth_token,
                          resource_owner_secret=oauth_token_secret, client_class=WarwickClient)
    
    return oauth

def get_redirect_to_authorise_url(oauth_token):
    authorise_qs = urllib.parse.urlencode({'oauth_token': oauth_token})

    return redirect(AUTHORISE_URL + authorise_qs, code=302)

def get_sso_attributes(oauth):
    resp = oauth.request('POST', 'https://websignon.warwick.ac.uk/oauth/authenticate/attributes')
    content = str(resp.content, 'UTF-8').strip()

    end_data = {}

    for item in content.split('\n'):
        if '=' not in item:
            continue

        name = item[0:item.find('=')]
        value = item[item.find('=') + 1:]
        end_data[name] = value
    
    return end_data