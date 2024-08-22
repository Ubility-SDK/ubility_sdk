from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
import random
import string
def create_token(cred):
    try:
        result={}
        result['token']=cred['accessToken']
        result['refresh_token']=cred['refreshToken']
        result['token_uri']="https://oauth2.googleapis.com/token"
        result['client_id']=cred['clientID']
        result['client_secret']=cred['clientSecret']
        result['scopes']=['https://www.googleapis.com/auth/calendar']
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e)
    

def create_service(access_token, API_SERVICE_NAME, API_VERSION):
    try:
        creds_data = json.loads(access_token)
        creds = Credentials.from_authorized_user_info(creds_data)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build(API_SERVICE_NAME, API_VERSION,
                        credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        raise Exception(
            f'Failed to create service instance for {API_SERVICE_NAME}')
    

def generate_request_id(length=40):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_google_meet_event(creds,params):
    try:
        if "calendar_id" and "start" and "end" in params:
            cred=json.loads(creds)
            access_token=create_token(cred)
            service = create_service(access_token,'calendar', 'v3')
            calendar_id = params.pop("calendar_id")
            params['conferenceData'] = {
                'createRequest': {
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    },
                    'requestId': generate_request_id()
                }
            }
            event = service.events().insert(calendarId=calendar_id, body=params,conferenceDataVersion=1).execute()
            if event:
                return event
            else:
                raise Exception('Failed to Create Event')
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise(e)