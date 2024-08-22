from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import Error
import json


def create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION):
    """
       Create a service that will be used for authorization purposes.
    
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'calendar'
    :param str API_VERSION: (str,required) the version used is v3  
    :return: details about the created service
    :rtype: dict  
    """
    try:
        creds_data = json.loads(ACCESS_TOKEN)
        creds = Credentials.from_authorized_user_info(creds_data)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build(API_SERVICE_NAME,API_VERSION,
                        credentials=creds, static_discovery=False)
        return service
    except Exception as e:
        raise Exception(f'Failed to create service instance {e}')
    

def create_token(cred):
    try:
        result={}
        result['token']=cred['accessToken']
        result['refresh_token']=cred['refreshToken']
        result['token_uri']="https://oauth2.googleapis.com/token"
        result['client_id']=cred['clientID']
        result['client_secret']=cred['clientSecret']
        result['scopes']=["https://www.googleapis.com/auth/calendar"]
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e)

#################################################################################################


def Google_Calendar_get_all_events(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Returns a list of events with custom properties.

    :param str ACCESS_TOKEN: (str, required) Used for authentication.
    :param str API_SERVICE_NAME: (str, required) The service name, for the calendar, it's 'calendar'.
    :param str API_VERSION: (str, required) The version used is v3.
    :param dict params: Filters the properties to be returned for each event.
    
        - :calendarId: (str, Required) The id of the calendar (calendar identifier).
        -  :orderBy: (str) The order of the events returned in the result.
                  Acceptable values are startTime, updated.
        - :timeMax: (datetime) Upper bound (exclusive) for an event's start time to filter by.
        - :timeMin: (datetime) Lower bound (exclusive) for an event's end time to filter by.
        - :iCalUID: (str) Specifies an event ID in the iCalendar format to be
                  provided in the response.
        - :maxAttendees: (str) The maximum number of attendees to include in the response.
        - :q: (str) Free text search terms to find events that match one of these
            summary, description, location, etc.
        - :showHiddenInvitations: (bool)  - Whether to include hidden invitations 
                                      in result. Optional. The default is False.
        - :timeZone: (str) Time zone used in the response.
        - :updatedMin: (datetime) Lower bound for an event's last modification time to filter by.

    :return: The list of events with the filtered properties.
    :rtype: dict
    """
    try:
      cred=json.loads(creds)
      ACCESS_TOKEN=create_token(cred)
      if "calendarId" in params:
         events = {}
         for key, value in params.items():
            if value:
                events[key] = value
         service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
         response = service.events().list(**events).execute()
         return response
      else:
            raise Exception("email required")
    except Exception as error:
        raise Exception(error)
      
def Google_Calendar_create_event(creds,API_SERVICE_NAME,API_VERSION,params):
 """
        Creates an event of a specific id.
    
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'calendar'
    :param str API_VERSION: (str,required) the version used is v3  
    :param dict params: contains the properties  to be added to the event
      
     - :colorId: (str) The color of the event. This is an ID referring to an entry in the event section of the colors definition 
      - :calendarId: (str,required) the id of the calendar (calendar identifier)
      - :start: (dict,required) 'dateTime':The time, as a combined date-time value (formatted according to RFC3339)
      - :end: (dict,required) 'dateTime' : The time, as a combined date-time value (formatted according to RFC3339)
      - :visibility: (str) possible values are default,public,private,confidential
      - :description: (str) Description of the event
      - :location: (str) Geographic location of the event as free-form text.
      - :maxAttendees: (str) The maximum number of attendees to include in the response
      - :attendees: (arr of str) The attendees of the event
      - :guestsCanInviteOthers: (bool) Whether attendees other than 
      
            the organizer can invite others to the event.
      - :guestsCanModify: (bool) 	Whether attendees other than the organizer can modify the event
      - :guestsCanSeeOtherGuests: (bool)  Whether attendees other than
       
             the organizer can see who the event's 
             
              attendees are
      - :sendUpdates: (bool) Whether to send notifications about the creation of the new event.
    :return: details about the created event(id,properties,..)
    :rtype: dict  
 """
 try:
    cred=json.loads(creds)
    ACCESS_TOKEN=create_token(cred)
    if 'start' in params and 'end' in params and 'calendarId' in params:
      to_create = {}
      keys_to_skip = ["calendarId"]
      for key, value in params.items():
        if key in keys_to_skip:
                continue
        if value:
            to_create[key] = value
      service=create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION)
      response = service.events().insert(calendarId=params['calendarId'],body=to_create).execute()
      return response
    else:
        raise Exception("missing input data")
 except Exception as error:
        raise Exception(error)

def Google_Calendar_get_event(creds,API_SERVICE_NAME,API_VERSION,params):
 """
        Returns an event of a specific id.
    
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'calendar'
    :param str API_VERSION: (str,required) the version used is v3  
    :param dict params:
      - :eventId: (str,required) The id of the event to be retrieved
      - :calendarId: (str,required) the id of the calendar (calendar identifier)
    :return: details about the retrieved event(id,properties,..)
    :rtype: dict  
 """
 try:
    cred=json.loads(creds)
    ACCESS_TOKEN=create_token(cred)
    if 'calendarId' in params and 'eventId' in params:
      service=create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION)
      response = service.events().get(calendarId=params['calendarId'], eventId=params['eventId']).execute()
      return response
    else:
        raise Exception("missing input data")
 except Exception as error:
        raise Exception(error)

def Google_Calendar_delete_event(creds,API_SERVICE_NAME,API_VERSION,params):
 """
         Deletes a event of a specific id
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'calendar'
    :param str API_VERSION: (str,required) the version used is v3  
    :param dict params: contains the id of the event to be deleted 
      - :eventId: (str,required) The id of the event to be deleted
      - :calendarId: (str,required) the id of the calendar (calendar identifier)

    :return: a statement about the successful/failed deletion of the event
    :rtype: json  
 """
 try:
    cred=json.loads(creds)
    ACCESS_TOKEN=create_token(cred)
    if 'calendarId' in params and 'eventId' in params:
      service=create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION)
      response = service.events().delete(calendarId=params['calendarId'], eventId=params['eventId']).execute()
      return f"Event with ID : {params['eventId']} deleted successfully "
    else:
        raise Exception("missing input data")
 except Exception as error:
        raise Exception(error)

def Google_Calendar_update_event(creds,API_SERVICE_NAME,API_VERSION,params):
  """
        Updates an event of a specific id.
    
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'calendar'
    :param str API_VERSION: (str,required) the version used is v3  
    :param dict params: contains the properties of the event , that need to be modified
      
      - :colorId: (str) The color of the event. This is an ID referring to an entry in the event section of the colors definition 
      - :eventId: (str,required) The id of the event to be modified
      - :calendarId: (str,required) the id of the calendar (calendar identifier)
      - :start: (dict,required) 'dateTime':The time, as a combined date-time value (formatted according to RFC3339)
      - :end: (dict,required) 'dateTime' : The time, as a combined date-time value (formatted according to RFC3339)
      - :visibility: (str) possible values are default,public,private,confidential
      - :description: (str) Description of the event
      - :location: (str) Geographic location of the event as free-form text.
      - :maxAttendees: (str) The maximum number of attendees to include in the response
      - :attendees: (arr of str) The attendees of the event
      - :guestsCanInviteOthers: (bool) Whether attendees other than 
      
            the organizer can invite others to the event.
      - :guestsCanModify: (bool) 	Whether attendees other than the organizer can modify the event
      - :guestsCanSeeOtherGuests: (bool) - Whether attendees other than
       
             the organizer can see who the event's 
             
              attendees are
      - :sendUpdates: (bool) Whether to send notifications about the creation of the new event.
    :return: details about the updated event(id,properties,..)
    :rtype: dict  
  """
  try:
    cred=json.loads(creds)
    ACCESS_TOKEN=create_token(cred)
    if 'calendarId' in params and 'eventId' in params and 'start' in params and 'end' in params:
      to_update = {}
      keys_to_skip = ["calendarId","eventId"]
      for key, value in params.items():
       if key in keys_to_skip:
              continue
       if value:
          to_update[key] = value
      service=create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION)
      response = service.events().update(calendarId=params['calendarId'], eventId=params['eventId'], body=to_update).execute()
      return response 
    else:
        raise Exception("Missing input data")
  
  except Exception as error:
        raise Exception(error)

def Google_Calendar_get_calendar(creds,API_SERVICE_NAME,API_VERSION,params):
 """
        Returns an calendar of a specific id.
    
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'calendar'
    :param str API_VERSION: (str,required) the version used is v3  
    :param dict params:
  
      - :calendarId: (str,required) the id of the calendar (calendar identifier)
    :return: details about the retrieved calendar(id,properties,..)
    :rtype: dict  
 """
 try:
    cred=json.loads(creds)
    ACCESS_TOKEN=create_token(cred)
    if 'calendarId' in params:
      service=create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION)
      response = service.calendars().get(calendarId=params['calendarId']).execute()
      return response
    else:
        raise Exception("missing calendar email")
 except Exception as error:
        raise Exception(error)
