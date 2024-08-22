import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging

def create_service(access_token, API_SERVICE_NAME, API_VERSION):
    try:
        creds_data = json.loads(access_token)
        creds = Credentials.from_authorized_user_info(creds_data)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build(API_SERVICE_NAME, API_VERSION,
                        credentials=creds, static_discovery=False)
        logging.warning(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        logging.warning(f'Failed to create service instance for {e}')
        raise Exception(f'Failed to create service instance {e}')
    
def create_token(cred):
    try:
        result={}
        result['token']=cred['accessToken']
        result['refresh_token']=cred['refreshToken']
        result['token_uri']="https://oauth2.googleapis.com/token"
        result['client_id']=cred['clientID']
        result['client_secret']=cred['clientSecret']
        result['scopes']=["https://www.googleapis.com/auth/documents"]
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e)  
 
def googledocs_create(creds,params):
    """
    Create a new Google Docs document.

    :param str access_token: Google API access token. (required)
    :param dict params:
        - title (str): Title of the Google Docs document. (required)

    :return: Information about the created Google Docs document.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if 'title' in params:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'docs','v1')
            doc = service.documents().create(body=data).execute()
            return doc
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise SyntaxError('error:'+ str(e))  

def googledocs_get(creds,params):
    """
    Retrieve information about a Google Docs document.

    :param str access_token: Google API access token. (required)
    :param dict params:
        - documentId (str): ID of the Google Docs document to retrieve information. (required)

    :return: Information about the Google Docs document.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if 'documentId' in params:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'docs','v1')
            document = service.documents().get(**data).execute()       
            return document
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise SyntaxError('error:'+ str(e)) 
    
def googledocs_update(creds,params):
    """
    Update information for a Google Docs document.

    :param access_token: str, Google API access token. (required)
    :param dict params:
        - documentId (str): ID of the Google Docs document to update. (required)
        - requests (list): List of update requests to apply to the document. (required)
        Example `requests` structure:
            [
            {
                "replaceAllText":{
                    "containsText":{
                        "text":"str",
                        "matchCase":"bool"
                    },
                    "replaceText":"str"
                }
            },
            {
                "insertText":{
                    "text":"str",
                    "endOfSegmentLocation":{
                        "segmentId":"str"
                    }
                }
            },
            {
                "insertText":{
                    "text":"str",
                    "location":{
                        "segmentId":"str",
                        "index":"str"
                    }
                }
            },
            {
                "createParagraphBullets":{
                    "range":{
                        "segmentId":"str",
                        "startIndex":"str",
                        "endIndex":"str"
                    },
                    "bulletPreset":"str"
                }
            },
            {
                "deleteParagraphBullets":{
                    "range":{
                        "segmentId":"str",
                        "startIndex":"str",
                        "endIndex":"str"
                    }
                }
            },
            {
                "createNamedRange":{
                    "name":"str",
                    "range":{
                        "segmentId":"str",
                        "startIndex":"str",
                        "endIndex":"str"
                    }
                }
            },
            {
                "deleteNamedRange":{
                    "name":"str"
                }
            },
            {
                "deleteNamedRange":{
                    "namedRangeId":"str"
                }
            },
            {
                "insertTable":{
                    "rows":"int",
                    "columns":"int",
                    "location":{
                        "segmentId":"str",
                        "index":"str"
                    }
                }
            },
            {
                "insertTable":{
                    "rows":"int",
                    "columns":"int",
                    "endOfSegmentLocation":{
                        "segmentId":"str"
                    }
                }
            },
            {
                "insertTableRow":{
                    "tableCellLocation":{
                        "tableStartLocation":{
                        "index":"str",
                        "segmentId":"str"
                        },
                        "rowIndex":"str",
                        "columnIndex":"str"
                    },
                    "insertBelow":"bool"
                }
            },
            {
                "insertTableColumn":{
                    "tableCellLocation":{
                        "tableStartLocation":{
                        "index":"str",
                        "segmentId":"str"
                        },
                        "rowIndex":"str",
                        "columnIndex":"str"
                    },
                    "insertRight":"bool"
                }
            },
            {
                "deleteTableRow":{
                    "tableCellLocation":{
                        "tableStartLocation":{
                        "index":"str",
                        "segmentId":"str"
                        },
                        "rowIndex":"str",
                        "columnIndex":"str"
                    }
                }
            },
            {
                "deleteTableColumn":{
                    "tableCellLocation":{
                        "tableStartLocation":{
                        "index":"str",
                        "segmentId":"str"
                        },
                        "rowIndex":"str",
                        "columnIndex":"str"
                    }
                }
            },
            {
                "insertPageBreak":{
                    "location":{
                        "segmentId":"str",
                        "index":"str"
                    }
                }
            },
            {
                "insertPageBreak":{
                    "endOfSegmentLocation":{
                        "segmentId":"str"
                    }
                }
            },
            {
                "deletePositionedObject":{
                    "objectId":"str"
                }
            },
            {
                "createHeader":{
                    "type":"str",
                    "sectionBreakLocation":{
                        "segmentId":"str",
                        "index":"str"
                    }
                }
            },
            {
                "createFooter":{
                    "type":"str",
                    "sectionBreakLocation":{
                        "segmentId":"str",
                        "index":"str"
                    }
                }
            },
            {
                "deleteHeader":{
                    "headerId":"str"
                }
            },
            {
                "deleteFooter":{
                    "footerId":"str"
                }
            }
            ]
    :return: Updated Google Docs document.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        if 'documentId' in params and 'requests' in params:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            service = create_service(access_token,'docs','v1')
            document = service.documents().batchUpdate(documentId=data['documentId'], body={'requests': data['requests']}).execute()       
            return document
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise SyntaxError('error:'+ str(e))  