import json
import webbrowser
import msal
import requests
from dotenv import load_dotenv
import os


load_dotenv()

APPLICATION_ID = os.getenv("APPLICATION_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
SCOPES = ['User.Read']

authority_url = f'https://login.microsoftonline.com/{TENANT_ID}/'
client_instance = msal.ConfidentialClientApplication(
    client_id=APPLICATION_ID,
    client_credential=CLIENT_SECRET,
    authority=authority_url
)


authorization_request_url = client_instance.get_authorization_request_url(
    scopes=SCOPES,
    redirect_uri='http://localhost:5000'
)

print(f'Please visit the following URL to authorize: {authorization_request_url}')

# Open the authorization URL in the default web browser
webbrowser.open(authorization_request_url, new=True)

# Retrieve authorization code from user input (manually enter after authorization)
authorization_code = input('Enter the authorization code from the URL: ')

# Exchange authorization code for access token
token_response = client_instance.acquire_token_by_authorization_code(
    authorization_code,
    scopes=SCOPES,
    redirect_uri='http://localhost:5000',
)


if 'access_token' in token_response:
    access_token = token_response['access_token']
    with open('access_token.json', 'w') as token_file:
        json.dump({'access_token': access_token}, token_file)

    print('Access token saved to access_token.json')
else:
    print('Failed to acquire access token')

