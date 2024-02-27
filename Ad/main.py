from flask import Flask, request, session, redirect, url_for
import msal

app = Flask(__name__)
app.secret_key = b'5555'

from dotenv import load_dotenv
import os


load_dotenv()

APPLICATION_ID = os.getenv("APPLICATION_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = 'https://login.microsoftonline.com/your_tenant_id'
SCOPES = ['User.Read']
REDIRECT_PATH = 'http://localhost:5000'

@app.route('/')
def index():
    auth_url = _build_auth_url(scopes=SCOPES, redirect_uri=request.base_url + REDIRECT_PATH)
    return redirect(auth_url)

@app.route('/auth_callback')
def auth_callback():
    auth_code = request.args.get('code')
    if auth_code:
        session['auth_code'] = auth_code
        return redirect(url_for('get_token'))
    else:
        return 'Authorization code not found.'


@app.route('/get_token')
def get_token():
    auth_code = session.get('auth_code')
    if auth_code:
        token_response = _get_token(auth_code)
        if 'access_token' in token_response:
            access_token = token_response['access_token']
            session['access_token'] = access_token
            return 'Access token obtained and stored in session storage.'
        else:
            return 'Failed to obtain access token.'
    else:
        return 'Authorization code not found.'


def _build_auth_url(scopes, redirect_uri):
    client = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    return client.get_authorization_request_url(scopes=scopes, redirect_uri=redirect_uri)

def _get_token(auth_code):
    client = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    return client.acquire_token_by_authorization_code(auth_code, scopes=SCOPES, redirect_uri=request.base_url + REDIRECT_PATH)

if __name__ == '__main__':
    app.run(debug=True, port=8000, host="localhost")
