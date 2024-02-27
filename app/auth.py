import requests
from flask import Blueprint, redirect, url_for, session, render_template, request
import msal
import os
from dotenv import load_dotenv

load_dotenv()

auth_blueprint = Blueprint("auth", __name__)

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


@auth_blueprint.route('/')
def index():
    authorization_request_url = client_instance.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri='http://localhost:5000'
    )
    return redirect(authorization_request_url)


@auth_blueprint.route('/auth_callback')
def auth_callback():
    token_response = client_instance.acquire_token_by_authorization_code(
        request.args['code'],
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/'
    )

    if 'access_token' in token_response:
        session['access_token'] = token_response['access_token']
        print("user_info",session)
        # Retrieve user information from Microsoft Graph API
        user_info = get_user_info(session['access_token'])
        if user_info:
            user_name = user_info.get('displayName', 'User')
            session['user'] = user_name

            print("user_info",user_info)
            print(f"Access Token: {session['access_token']}")
            print(f"User Name: {session['user']}")

    return redirect(url_for('.success'))



@auth_blueprint.route('/success')
def success():
    user_name = session.get('user', 'User')
    return render_template('index.html', user_name=user_name)



def get_user_info(access_token):
    graph_endpoint = 'https://graph.microsoft.com/v1.0/me'
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(graph_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


