import requests
from flask import Flask, request, redirect
import adal
from dotenv import load_dotenv
import os

load_dotenv()

# Load Azure AD credentials from environment variables
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPES = ['User.Read']
RESOURCE = 'https://management.azure.com/'
graph_api_endpoint = 'https://graph.microsoft.com/v1.0/me'
authority_url = f'https://login.microsoftonline.com/{TENANT_ID}'
redirect_uri = 'http://localhost:5000/'

app = Flask(__name__)

@app.route('/')
def login():
    # Construct authorization URL
    auth_context = adal.AuthenticationContext(authority_url)
    auth_url = auth_context.get_authorization_request_url(
        RESOURCE,
        client_id=CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=SCOPES
    )
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    # Handle authorization code response
    code = request.args.get('code')
    auth_context = adal.AuthenticationContext(authority_url)
    token_response = auth_context.acquire_token_with_authorization_code(
        code,
        redirect_uri,
        RESOURCE,
        CLIENT_ID,
        CLIENT_SECRET
    )
    access_token = token_response.get('accessToken')
    # Use access token to call Microsoft Graph API
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(graph_api_endpoint, headers=headers)
    user_data = response.json()
    return f"User data: {user_data}"

if __name__ == '__main__':
    app.run(debug=True, port=8002)
