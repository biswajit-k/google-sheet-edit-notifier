import pprint

from flask import Flask, redirect, request
import google_auth_oauthlib


app = Flask('app')
app.secret_key = 'thisisnotsecret'

@app.route('/')
def home():
    return "<h1>Hello world</h1>"


# variables
############################################
SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CLIENT_SECRET_FILE = 'client_secret.json'
REDIRECT_URI = 'http://localhost:5000/oauth2callback'


# helper functions
############################################
def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def generate_flow():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPE)
    flow.redirect_uri = REDIRECT_URI

    return flow

def save_variable_in_env(key, value):
    import dotenv
    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_file, key, value)


# Routes
############################################
@app.route('/fetch_code')
def fetch_code():
    flow = generate_flow()

    authorization_url = flow.authorization_url(access_type='offline', include_granted_scopes='true')[0]

    return redirect(authorization_url)


# route to which google sends the code(use https domain). For local just copy code from browser
@app.route('/oauth2callback')
def fetch_token_in_redirect():

    flow = generate_flow()
    code = request.args.get('code', type=str)

    flow.fetch_token(code=code)

    credentials = credentials_to_dict(flow.credentials)

    # save refresh token in env
    save_variable_in_env('REFRESH_TOKEN', credentials['refresh_token'])
    save_variable_in_env('CLIENT_ID', credentials['client_id'])
    save_variable_in_env('CLIENT_SECRET', credentials['client_secret'])

    # print credentials in colsole
    print(f"credentials-\n\n")
    pprint.pprint(credentials)
    print("\n\n")

    return "<h3>Credentials added in env file 👀"
