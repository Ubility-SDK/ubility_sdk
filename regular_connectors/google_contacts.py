from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import json
import requests
import base64


def create_service(ACCESS_TOKEN,API_SERVICE_NAME,API_VERSION):
    """
    Create a service that will be used for authorization purposes.
    
    :param str ACCESS_TOKEN: (str,required) used for authentication
    :param str API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :param str API_VERSION: (str,required) the version used is v1  
    
    :return: the created service object
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
        result['scopes']=["https://www.googleapis.com/auth/contacts"]
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e)

#################################################################################################

def Google_Contacts_get_all_contacts(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Provides a list of the authenticated user's contacts.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :personFields: (str, Required) - A field mask to restrict which fields on each person are returned. Multiple fields can be specified by separating them with commas. Valid values are: *, addresses, ageRanges, biographies, birthdays, calendarUrls, clientData, coverPhotos, emailAddresses, events, externalIds, genders, imClients, interests, locales, locations, memberships, metadata, miscKeywords, names, nicknames, occupations, organizations, phoneNumbers, photos, relations, sipAddresses, skills, urls, userDefined
    - :pageSize: (int) - The number of connections to include in the response. Valid values are between 1 and 1000, inclusive. Defaults to 100 if not set or set to 0.
    - :sortOrder: (str) - string, Optional. The order in which the connections should be sorted. Defaults to `LAST_MODIFIED_ASCENDING`.
    
        :Allowed values:
        
        LAST_MODIFIED_ASCENDING - Sort people by when they were changed; older entries first.
        
        LAST_MODIFIED_DESCENDING - Sort people by when they were changed; newer entries first.
        
        FIRST_NAME_ASCENDING - Sort people by first name.
        
        LAST_NAME_ASCENDING - Sort people by last name.

    :return: dictionary object containing a list of Person objects with each person object representing a contact
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "personFields" in params:
            data = {
                key: value
                for (key, value) in params.items()
                if value
            }
            data["resourceName"] = "people/me"
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().connections().list(**data).execute()
            if response:
                return response
            else:
                return {"message": "No Contacts Found"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Contacts_get_contact(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Provides information about a person by specifying a Contact's resourceName.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :resourceName: (str, Required) - The resource name of the person to provide information about. To get information about a contact, specify the resource name that identifies the contact as returned by `people.connections.list`.
    - :personFields: (str, Required) - A field mask to restrict which fields on each person are returned. Multiple fields can be specified by separating them with commas. Valid values are: *, addresses, ageRanges, biographies, birthdays, calendarUrls, clientData, coverPhotos, emailAddresses, events, externalIds, genders, imClients, interests, locales, locations, memberships, metadata, miscKeywords, names, nicknames, occupations, organizations, phoneNumbers, photos, relations, sipAddresses, skills, urls, userDefined

    :return: Person resource object representing the retrieved contact. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/people
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "personFields" in params and "resourceName" in params:
            resourceName = params["resourceName"]
            personFields = params["personFields"]
            data = {"resourceName": resourceName, "personFields": personFields}
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().get(**data).execute()
            return response
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Contacts_search_contacts(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Provides a list of the authenticated user's contacts matching the search query.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :query: (str, Required) - The plain-text query for the request. The query is used to match prefix phrases of the fields on a person. For example, a person with name "foo name" matches queries such as "f", "fo", "foo", "foo n", "nam", etc., but not "oo n".
    - :readMask: (str, Required) - A field mask to restrict which fields on each person are returned. Multiple fields can be specified by separating them with commas. Valid values are: *, addresses, ageRanges, biographies, birthdays, calendarUrls, clientData, coverPhotos, emailAddresses, events, externalIds, genders, imClients, interests, locales, locations, memberships, metadata, miscKeywords, names, nicknames, occupations, organizations, phoneNumbers, photos, relations, sipAddresses, skills, urls, userDefined
    - :pageSize: (int) - The number of results to return. Defaults to 10 if field is not set, or set to 0. Values greater than 30 will be capped to 30.

    :return: dictionary object containing a list of Person objects with each person object representing a contact
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "readMask" in params and "query" in params:
            data = {
                key: value
                for (key, value) in params.items()
                if value
            }
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().searchContacts(**data).execute()
            if response:
                return response
            else:
                return {"message": "No Contacts Found"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)




def Google_Contacts_create_contact(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Create a new contact and return the person resource for that contact.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :body: (dict, Required) - an instance of the Person object which contains Information about a person merged from various data sources such as the authenticated user's contacts and profile data. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/people

    :return: Person resource object of the newly created Contact. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/people
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "body" in params:
            body =  params.get("body")
            personFields = "addresses,ageRanges,biographies,birthdays,calendarUrls,clientData,coverPhotos,emailAddresses,events,externalIds,genders,imClients,interests,locales,locations,memberships,metadata,miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,skills,urls,userDefined"
            data = {"personFields": personFields, "body": body}
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().createContact(**data).execute()
            return response
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Contacts_update_contact(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Retrieve contact etag then Update contact data for an existing contact person. 
    
    Any non-contact data will not be modified. Any non-contact data in the person to update will be ignored. All fields specified in the `updatePersonFields` will be replaced.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :resourceName: (str, Required) - The resource name for the person, assigned by the server. An ASCII string in the form of `people/{person_id}`.
    - :updatePersonFields: (str, Required) - A field mask to restrict which fields on the person are updated. Multiple fields can be specified by separating them with commas. All updated fields will be replaced. Valid values are: addresses, biographies, birthdays, calendarUrls, clientData, emailAddresses, events, externalIds, genders, imClients, interests, locales, locations, memberships, miscKeywords, names, nicknames, occupations, organizations, phoneNumbers, relations, sipAddresses, urls, userDefined
    - :body: (dict, Required) - an instance of the Person object which contains Information about a person merged from various data sources such as the authenticated user's contacts and profile data. you must include the 'etag' field in the person for the contact to be updated to make sure the contact has not changed since your last read. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/people
    
        -:etag: (str, Required) - The `HTTP entity tag <https://en.wikipedia.org/wiki/HTTP_ETag>`_ of the resource. Used for web cache validation. can be retrieved from the person resource object from the contact to be updated.

    :return: Person resource object of the newly Updated Contact. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/people
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        etag = params.get("body", {}).get("etag", "")
        if "body" in params and "resourceName" in params and "updatePersonFields" in params and etag:
            personFields = "addresses,ageRanges,biographies,birthdays,calendarUrls,clientData,coverPhotos,emailAddresses,events,externalIds,genders,imClients,interests,locales,locations,memberships,metadata,miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,skills,urls,userDefined"
            data = {
                key: value
                for (key, value) in params.items()
                if value
            }
            data["personFields"] = personFields
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().updateContact(**data).execute()
            return response
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Contacts_delete_contact(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Delete a contact person. Any non-contact data will not be deleted. Mutate requests for the same user should be sent sequentially to avoid increased latency and failures.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :resourceName: (str, Required) - The resource name of the contact to delete.

    :return: Dictionary confirming the successfull deletion of the contact
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "resourceName" in params:
            resourceName = params["resourceName"]
            data = {"resourceName": resourceName}
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().deleteContact(**data).execute()
            if response:
                return response
            else:
                return {"message": "Contact Deleted successfully"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)




def Google_Contacts_upload_contact_photo(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Update a contact's photo.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :resourceName: (str, Required) - The resource name of the contact whose photo is to be updated. To get information about a contact, specify the resource name that identifies the contact as returned by `people.connections.list`.
    - :photoSource: (str, Required) - Choice for whether the to retrieve the photo in base64 format or from a url. Possible values: (url, base64)
    - :photoUrl: (str, Required if photoSource = url) - Url of photo to upload. must have a valid photo format: JPEG or PNG.
    - :photoBytes: (str, Required if photoSource = base64) - Raw photo bytes. A base64-encoded string. must have a valid photo format: JPEG or PNG.
    - :personFields: (str, optional) - A field mask to restrict which fields on each person are returned. Multiple fields can be specified by separating them with commas. Defaults to empty if not set, which will skip the post mutate get. Valid values are: *, addresses, ageRanges, biographies, birthdays, calendarUrls, clientData, coverPhotos, emailAddresses, events, externalIds, genders, imClients, interests, locales, locations, memberships, metadata, miscKeywords, names, nicknames, occupations, organizations, phoneNumbers, photos, relations, sipAddresses, skills, urls, userDefined

    :return: Person resource object representing the contact the photo was uploaded to. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/people
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "photoSource" in params and "resourceName" in params and ("photoBytes" in params or "photoUrl" in params):
            resourceName = params["resourceName"]
            photoSource = params["photoSource"]
            personFields = params.get("personFields", "")
            photoBytes = ""
            
            if photoSource == "url" and "photoUrl" in params:
                photoUrl = params.get("photoUrl", "")
                try:
                    url_response = requests.get(photoUrl)
                    url_response.raise_for_status()  
                    body = url_response.content
                except requests.RequestException as e:
                    raise Exception(f"Error downloading file from URL: {e}")
                except Exception as e:
                    raise Exception(f"error: {e}")
                finally:
                    if body:
                        photoBytes = base64.b64encode(body).decode()
                    else:
                        raise Exception("File content is empty.")
            elif photoSource == "base64" and "photoBytes" in params:
                photoBytes = params.get("photoBytes", "")
            else:
                raise Exception("Missing Input Data")
            data = {"resourceName": resourceName, "body": {"photoBytes": photoBytes}}
            if personFields:
                data["body"]["personFields"] = personFields
            
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.people().updateContactPhoto(**data).execute()
            return response
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Contacts_get_all_groups(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    List all contact groups owned by the authenticated user. Members of the contact groups are not populated.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :groupFields: (str, Optional) - A field mask to restrict which fields on the group are returned. Defaults to `metadata`, `groupType`, `memberCount`, and `name` if not set or set to empty. Valid fields are: (clientData, groupType, memberCount, metadata, name)
    - :pageSize: (int, Optional) - The maximum number of resources to return. Valid values are between 1 and 1000, inclusive. Defaults to 30 if not set or set to 0.
    

    :return: dictionary object containing a list of `ContactGroup resource objects <https://developers.google.com/people/api/rest/v1/contactGroups
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        data = {
            key: value
            for (key, value) in params.items()
            if value
        }
        service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
        response = service.contactGroups().list(**data).execute()
        if response:
            return response
        else:
            return {"message": "No Contact Groups Found"}
        
    except Exception as error:
        raise Exception(error)




def Google_Contacts_create_group(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Create a new contact group owned by the authenticated user.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :name: (str, Required) - Name of the group to be created

    :return: ContactGroup resource object of the newly created Contact Group. for more information see this `LINK <https://developers.google.com/people/api/rest/v1/contactGroups
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        if "name" in params:
            name = params["name"]
            data = {
                "readGroupFields": "clientData,groupType,memberCount,metadata,name",
                "contactGroup": {
                    "name": name
                }
            }
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.contactGroups().create(body=data).execute()
            return response
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)





def Google_Contacts_update_contacts_in_group(creds,API_SERVICE_NAME,API_VERSION,params):
    """
    Modify the members of a contact group owned by the authenticated user. 
    
    The only system contact groups that can have members added are `contactGroups/myContacts` and `contactGroups/starred`. Other system contact groups are deprecated and can only have contacts removed.

    :ACCESS_TOKEN: (str, required) Used for authentication.
    :API_SERVICE_NAME: (str,required) for Contacts, it's 'people'
    :API_VERSION: (str,required) the version used is v1  
    :params: Dictionary containing parameters.
    
    - :resourceName: (str, Required) - The resource name of the contact group to modify. in the format: contactGroups/{contact_group_id}
    - :body: (dict, Required) - The request body of a request to modify an existing contact group's members. Contacts can be removed from any group but they can only be added to a user group or "myContacts" or "starred" system groups.
    
        - :resourceNamesToAdd: (list, Optional) - The resource names of the contact 
        
            people to add in the form of `people/{person_id}`.
        
        - :resourceNamesToRemove: (list, Optional) - The resource names of the contact 
        
            people to remove in the form of `people/{person_id}`.
        
        The total number of resource names in `resource_names_to_add` and `resource_names_to_remove` must be less than or equal to 1000.

    :return: if successfull this operation returns a dictionary containing a success message. In case of of failure this operation returns a dictionary containing one of two lists or both. The first list has the key `notFoundResourceNames` and contains The contact people resource names that were not found. The second list has the key `canNotRemoveLastContactGroupResourceNames` and contains The contact people resource names that cannot be removed from their last contact group.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        ACCESS_TOKEN=create_token(cred)
        resourceName = params.get("resourceName", "")
        body =  params.get("body", {})
        if body and resourceName and (body.get("resourceNamesToAdd", []) or body.get("resourceNamesToRemove", [])):
            data = {"resourceName": resourceName, "body": body}
            service = create_service(ACCESS_TOKEN, API_SERVICE_NAME, API_VERSION)
            response = service.contactGroups().members().modify(**data).execute()
            if response:
                return response
            else:
                return {"message": "Contact Group Updated successfully"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

