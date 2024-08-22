import base64
import requests
import json

def outlook_refresh_access_token(creds):
    try:
        cred=json.loads(creds)
        token_endpoint="https://login.microsoftonline.com/common/oauth2/v2.0/token"
        request_body = {
            'client_id': cred['clientId'],
            'client_secret': cred['clientSecret'],
            'scope': ' '.join(['https://graph.microsoft.com/.default'] +['offline_access']),
            'refresh_token': cred['refreshToken'],
            "grant_type": "refresh_token",
        }
        response = requests.post(token_endpoint, data=request_body)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}
    except Exception as error:
        raise Exception(error)
    
##########################################################################################################################

########################################## CONTACT ##########################################


def outlook_get_many_contact(accessToken, params):
    """
    Retrieve multiple contacts from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - Maximum number of contacts to retrieve.
        - :filter: (str,optional) - Filter criteria for contacts (e.g., "name eq 'Work'").

    Returns:
        list: List of contacts retrieved from Outlook.
    """
    try:
        graph_api_url = "https://graph.microsoft.com/v1.0/me/contacts"
        limit_param = params.get("limit", "")
        filter_param = params.get("filter", "")
        query_params = []
        if limit_param:
            query_params.append(f"$top={limit_param}")
        if filter_param:
            query_params.append(f"$filter={filter_param}")
        if query_params:
            graph_api_url += "?" + "&".join(query_params)
        headers = {
            "Authorization": "Bearer " + accessToken,
        }
        response = requests.get(url=graph_api_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['value']
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def outlook_get_contact(accessToken, params):
    """
    Retrieve a contact from Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (str,required) - ID of the contact to be retrieved.

    Returns:
        dict: Details of the retrieved contact.
    """
    try:
        if "contact_id" in params:
            contact_id = params["contact_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-type": "application/json"
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_create_contact(accessToken, params):
    """
    Create a contact in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :givenName: (Str,required) - The contact's given name.
        - :surname:	(Str,optional) - The contact's surname.
        - :birthday: (DateTime,optional) - The contact's birthday.
        - :businessAddress:	(dict,optional) - The contact's business address.

         :city: (Str,optional) - City of the business address.
         :countryOrRegion: (Str,optional) - Country or region of the business address.
         :postalCode: (Str,optional) - Postal code of the business address.
         :state: (Str,optional) - State of the business address.
         :street: (Str,optional) - Street address of the business.

        - :homeAddress: (dict,optional) - The contact's home address.

         :city: (Str,optional) - City of the home address.
         :countryOrRegion: (Str,optional) - Country or region of the home address.
         :postalCode: (Str,optional) - Postal code of the home address.
         :state: (Str,optional) - State of the home address.
         :street: (Str,optional) - Street address of the home.

        - :otherAddress: (dict,optional) - Other addresses for the contact.

         :city: (Str,optional) - City of the Other addresses.
         :countryOrRegion: (Str,optional) - Country or region of the Other addresses.
         :postalCode: (Str,optional) - Postal code of the Other addresses.
         :state: (Str,optional) - State of the Other addresses.
         :street: (Str,optional) - Street of the Other addresses.

        - :businessHomePage: (Str,optional) - The business home page of the contact.
        - :businessPhones: (list of strings, optional) - The contact's business phone numbers.
        - :homePhones: (list of strings , optional) - The contact's home phone numbers.
        - :mobilePhone: (list of strings , optional) - The contact's mobile phone number.
        - :emailAddresses: (list of dictionaries , optional) - The contact's email addresses.
            
            - :address: (Str,optional) - The email address.
        - :jobTitle: (Str,optional) - The contact’s job title.
        - :companyName: (Str,optional) - The name of the contact's company.
        - :department: (Str,optional) - The contact's department.
        - :personalNotes: (Str,optional) - The user's notes about the contact.
        - :fileAs: (Str,optional) - The name the contact is filed under.

    Returns:
        dict: Details of the created contact.
    """
    try:
        if "givenName" in params:
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/contacts"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_update_contact(accessToken, params):
    """
    Update a contact in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (str,required) - ID of the contact to be updated.
        - :givenName: (Str,optional) - The contact's given name.
        - :surname:	(Str,optional) - The contact's surname.
        - :birthday: (DateTime,optional) - The contact's birthday.
        - :businessAddress:	(dict,optional) - The contact's business address.

         :city: (Str,optional) - City of the business address.
         :countryOrRegion: (Str,optional) - Country or region of the business address.
         :postalCode: (Str,optional) - Postal code of the business address.
         :state: (Str,optional) - State of the business address.
         :street: (Str,optional) - Street address of the business.

        - :homeAddress: (dict,optional) - The contact's home address.

         :city: (Str,optional) - City of the home address.
         :countryOrRegion: (Str,optional) - Country or region of the home address.
         :postalCode: (Str,optional) - Postal code of the home address.
         :state: (Str,optional) - State of the home address.
         :street: (Str,optional) - Street address of the home.

        - :otherAddress: (dict,optional) - Other addresses for the contact.

         :city: (Str,optional) - City of the Other addresses.
         :countryOrRegion: (Str,optional) - Country or region of the Other addresses.
         :postalCode: (Str,optional) - Postal code of the Other addresses.
         :state: (Str,optional) - State of the Other addresses.
         :street: (Str,optional) - Street of the Other addresses.

        - :businessHomePage: (Str,optional) - The business home page of the contact.
        - :businessPhones: (list of strings, optional) - The contact's business phone numbers.
        - :homePhones: (list of strings , optional) - The contact's home phone numbers.
        - :mobilePhone: (list of strings , optional) - The contact's mobile phone number.
        - :emailAddresses: (list of dictionaries , optional) - The contact's email addresses.
            
            - :address: (Str,optional) - The email address.
        - :jobTitle: (Str,optional) - The contact’s job title.
        - :companyName: (Str,optional) - The name of the contact's company.
        - :department: (Str,optional) - The contact's department.
        - :personalNotes: (Str,optional) - The user's notes about the contact.

    Returns:
        dict: Details of the updated contact.
    """
    try:
        if "contact_id" in params:
            contact_id = params["contact_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["contact_id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            if data:
                response = requests.patch(
                    url=graph_api_url, headers=headers, json=data)
                if response:
                    return response.json()
                else:
                    raise Exception(
                        f"Status code: {response.status_code}. Response: {response.text}")
            else:
                raise Exception("At least update one")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_delete_contact(accessToken, params):
    """
    Delete a contact in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (str,required) - ID of the contact to be deleted.

    Returns:
        dict: Confirmation message after successful deletion.
    """
    try:
        if "contact_id" in params:
            contact_id = params["contact_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}"
            headers = {
                "Authorization": "Bearer " + accessToken
            }
            response = requests.delete(url=graph_api_url, headers=headers)
            if response:
                return {"message": "Contact deleted successfully!"}
            else:
                raise Exception(
                    f"The resource you are requesting could not be found")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

########################################## calendar ##########################################


def outlook_get_many_calendar(accessToken, params):
    """
    Retrieve multiple calendars from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :limit: (str,optional) - Maximum number of calendars to retrieve.
        - :filter: (str,optional) - Filter criteria for calendars (e.g., "name eq 'Work'").

    Returns:
        list: List of calendars retrieved from Outlook.
    """
    try:
        graph_api_url = "https://graph.microsoft.com/v1.0/me/calendars"
        limit_param = params.get("limit", "")
        filter_param = params.get("filter", "")
        query_params = []
        if limit_param:
            query_params.append(f"$top={limit_param}")
        if filter_param:
            query_params.append(f"$filter={filter_param}")
        if query_params:
            graph_api_url += "?" + "&".join(query_params)
        headers = {
            "Authorization": "Bearer " + accessToken,
        }
        response = requests.get(url=graph_api_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['value']
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def outlook_get_calendar(accessToken, params):
    """
    Retrieve a calendar from Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - ID of the calendar to be retrieved.

    Returns:
        dict: Details of the retrieved calendar.
    """
    try:
        if "calendar_id" in params:
            calendar_id = params["calendar_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_create_calendar(accessToken, params):
    """
    Create a calendar in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :name: (Str,required) - The calendar name.
        - :calendarGroup_id: (Str,optional) - Id of calendar group.
        - :color: (str,optional) - Specifies the color theme to distinguish the calendar from other calendars in a UI. 

            The property values are: lightBlue, lightGreen, lightOrange, lightGray, lightYellow, lightTeal, lightPink, lightBrown, lightRed.

    Returns:
        dict: Details of the created calendar.
    """
    try:
        if "name" in params:
            calendarGroup_id = params.get("calendarGroup_id")
            base_url = f"https://graph.microsoft.com/v1.0/me"
            if calendarGroup_id:
                graph_api_url = f"{base_url}/calendarGroups/{calendarGroup_id}/calendars"
            else:
                graph_api_url = f"{base_url}/calendars"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["calendarGroup_id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_update_calendar(accessToken, params):
    """
    Update a calendar in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - ID of the calendar to be updated.
        - :color: (str,optional) - Specifies the color theme to distinguish the calendar from other calendars in a UI. 

                The property values are: lightBlue, lightGreen, lightOrange, lightGray, lightYellow, lightTeal, lightPink, lightBrown, lightRed
        - :isDefaultCalendar: (Boolean,optional) - True if this calendar is the user's default calendar, false otherwise.
        - :name: (str,optional) - The calendar name.

    Returns:
        dict: Details of the updated calendar.
    """
    try:
        if "calendar_id" in params:
            calendar_id = params["calendar_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["calendar_id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            if data:
                response = requests.patch(
                    url=graph_api_url, headers=headers, json=data)
                if response:
                    return response.json()
                else:
                    raise Exception(
                        f"Status code: {response.status_code}. Response: {response.text}")
            else:
                raise Exception("At least update one")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_delete_calendar(accessToken, params):
    """
    Delete a calendar in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - ID of the calendar to be deleted.

    Returns:
        dict: Confirmation message after successful deletion.
    """
    try:
        if "calendar_id" in params:
            calendar_id = params["calendar_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}"
            headers = {
                "Authorization": "Bearer " + accessToken
            }
            response = requests.delete(url=graph_api_url, headers=headers)
            if response:
                return {"message": "Calendar deleted successfully!"}
            else:
                raise Exception(
                    f"The resource you are requesting could not be found")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

########################################## folder ##########################################


def outlook_get_many_folder(accessToken, params):
    """
    Retrieve multiple folders from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :limit: (str,optional) - Maximum number of folders to retrieve.
        - :filter: (str,optional) - Filter criteria for folders.

    Returns:
        list: List of folders retrieved from Outlook.
    """
    try:
        graph_api_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
        limit_param = params.get("limit", "")
        filter_param = params.get("filter", "")
        query_params = []
        if limit_param:
            query_params.append(f"$top={limit_param}")
        if filter_param:
            query_params.append(f"$filter={filter_param}")
        if query_params:
            graph_api_url += "?" + "&".join(query_params)
        headers = {
            "Authorization": "Bearer " + accessToken,
        }
        response = requests.get(url=graph_api_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['value']
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def outlook_get_folder(accessToken, params):
    """
    Retrieve a folder from Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - ID of the folder to be retrieved.

    Returns:
        dict: Details of the retrieved folder.
    """
    try:
        if "folder_id" in params:
            folder_id = params["folder_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_create_folder(accessToken, params):
    """
    Create a folder in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :displayName: (Str,required) - The mailFolder's display name.

    Returns:
        dict: Details of the created folder.
    """
    try:
        if "displayName" in params:
            graph_api_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_update_folder(accessToken, params):
    """
    Update a folder in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - ID of the folder to be updated.
        - :displayName: (str,optional) - The mailFolder's display name.

    Returns:
        dict: Details of the updated folder.
    """
    try:
        if "folder_id" in params:
            folder_id = params["folder_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["folder_id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            if data:
                response = requests.patch(
                    url=graph_api_url, headers=headers, json=data)
                if response:
                    return response.json()
                else:
                    raise Exception(
                        f"Status code: {response.status_code}. Response: {response.text}")
            else:
                raise Exception("At least update one")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_delete_folder(accessToken, params):
    """
    Delete an folder by ID using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - ID of the folder to be deleted.

    Returns:
        dict: A message indicating the success of the deletion.
    """
    try:
        if "folder_id" in params:
            folder_id = params["folder_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }

            response = requests.delete(url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "Folder deleted successfully."}
            elif response.status_code == 404:
                raise Exception("Folder Not Found.")
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

########################################## folder message ##########################################


def outlook_get_many_folder_message(accessToken,params):
    """
    Retrieves the messages in a folder from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :folder_id: (str,required) - The ID of the Outlook folder from which to retrieve messages.
        - :limit: (str,optional) - Maximum number of messages in a folder to retrieve.
        - :filter: (str,optional) - Filter criteria for messages in a folder . Note that 'filter' cannot be used with 'search'.
        - :search: (str,optional) - A search string to filter . Note that 'search' cannot be used with 'filter'.

    Returns:
        list: List of messages in a folder retrieved from Outlook.
    """
    try:
        if "folder_id" in params:
            folder_id = params["folder_id"]
            base_url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages"
            limit_param = params.get("limit", "")
            filter_param = params.get("filter", "")
            search_param = params.get("search", "")
            query_params = []
            if limit_param:
                query_params.append(f"$top={limit_param}")
            if search_param:
                query_params.append(f"$search={search_param}")
            if filter_param:
                query_params.append(f"$filter={filter_param}")
            if query_params:
                base_url += "?" + "&".join(query_params)
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=base_url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['value']
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

##########################################  message ##########################################


def outlook_get_many_message(accessToken, params):
    """
    Retrieve multiple messages from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :limit: (str,optional) - Maximum number of messages to retrieve.
        - :filter: (str,optional) - Filter criteria for messages . Note that 'filter' cannot be used with 'search'.
        - :search: (str,optional) - A search string to filter . Note that 'search' cannot be used with 'filter'.      

    Returns:
        list: List of messages retrieved from Outlook.
    """
    try:
        base_url = f"https://graph.microsoft.com/v1.0/me/messages"
        limit_param = params.get("limit", "")
        filter_param = params.get("filter", "")
        search_param = params.get("search", "")
        query_params = []
        if limit_param:
            query_params.append(f"$top={limit_param}")
        if search_param:
            query_params.append(f"$search={search_param}")
        if filter_param:
            query_params.append(f"$filter={filter_param}")
        if query_params:
            base_url += "?" + "&".join(query_params)
        headers = {
            "Authorization": "Bearer " + accessToken,
        }
        response = requests.get(url=base_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['value']
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def outlook_get_message(accessToken, params):
    """
    Retrieve a message from Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :message_id: (str,required) - ID of the message to be retrieved.

    Returns:
        dict: Details of the retrieved message.
    """
    try:
        if "message_id" in params:
            message_id = params["message_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-type": "application/json"
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_delete_message(accessToken, params):
    """
    Delete an message by ID using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :message_id: (str,required) - ID of the message to be deleted.

    Returns:
        dict: A message indicating the success of the deletion.
    """
    try:
        if "message_id" in params:
            message_id = params["message_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "Message deleted successfully."}
            elif response.status_code == 404:
                raise Exception("Message Not Found.")
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_move_message(accessToken, params):
    """
    Move a message to a specific folder in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

       - :message_id: (str,required) - ID of the message to be moved.
       - :destinationId: (str,required) - ID of the destination folder where the message will be moved.

    Returns:
        dict: The updated message details.
    """
    try:
        if "message_id" in params and "destinationId" in params:
            message_id = params["message_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/move"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["message_id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_reply_message(accessToken, params):
    """
    Create a reply to a message in Outlook.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :message_id: (str,required) - The ID of the Outlook message to which a reply will be created.
        - :reply_content_body: (str,required) - The body of the reply message.
        - :reply_contentType_body: (str,required) - The content Type of the reply message.

    Returns:
        dict: A dictionary containing information about the created reply.

    """
    try:
        if "message_id" in params and "reply_content_body" in params and "reply_contentType_body" in params:
            message_id = params["message_id"]
            reply_content_body = params.get("reply_content_body")
            reply_contentType_body = params.get("reply_contentType_body")
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/reply"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json"
            }
            data = {
                "message": {
                    "body": {
                        "content": reply_content_body,
                        "contentType": reply_contentType_body
                    }
                }
            }
            for key, value in params.items():
                skip_keys = ["message_id", "reply_body"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(
                url=graph_api_url, json=data, headers=headers)

            if response:
                return {"message": "Reply creation request accepted."}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_send_message(accessToken, params):
    """
    Send a message in Outlook.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :to_emails: (list,required) - List of email addresses for primary recipients.
        - :subject: (str,required) - The subject of the email.
        - :bodyFormat: (str,required) - The format of the email body ("text" or "html").
        - :body: (str,required) - The content of the email body.
        - :cc_emails: (list,optional) - List of email addresses for CC (Carbon Copy).
        - :bcc_emails: (list,optional) - List of email addresses for BCC (Blind Carbon Copy).
        - :attachments: (list, optional) - List of dictionaries representing attachments. 
            
         :type: (str, required) - Type of attachment ("ByteString" or "url").
         :fileName: (str, required) - Name of the attachment file.
         :contentBytes: (str,required if type is "ByteString") - Base64 encoded content of the attachment.
         :url_attachment: (str,required if type is "url") - URL of the attachment.

    Returns:
        dict: A dictionary indicating the success of the operation.

    """
    try:
        if "subject" in params and "body" in params and "bodyFormat" in params and "to_emails" in params:
            subject = params["subject"]
            body = params["body"]
            bodyFormat = params["bodyFormat"]
            to_emails = params["to_emails"]
            cc_emails = params.get("cc_emails", "")
            bcc_emails = params.get("bcc_emails", "")
            attachments = params.get("attachments", "")
            graph_api_url = "https://graph.microsoft.com/v1.0/me/sendMail"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            email_data = {
                "message": {
                    "subject": subject,
                    "body": {
                        "content": body,
                        "contentType": bodyFormat
                    },
                    "toRecipients": [{"emailAddress": {"address": email}} for email in to_emails],
                    "ccRecipients": [{"emailAddress": {"address": email}} for email in cc_emails],
                    "bccRecipients": [{"emailAddress": {"address": email}} for email in bcc_emails],
                }
            }
            if attachments:
                email_data["message"]["attachments"] = []
                for attachment in attachments:
                    if attachment["type"] == "ByteString":
                        email_data["message"]["attachments"].append({
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": attachment["fileName"],
                            "contentBytes": attachment["contentBytes"]
                        })
                    elif attachment["type"] == "url":
                        response = requests.get(attachment["url_attachment"])
                        if response.status_code == 200:
                            file_content = response.content
                            if file_content:
                                encoded_content = base64.b64encode(
                                    file_content).decode('utf-8')
                                email_data["message"]["attachments"].append(
                                    {
                                        "@odata.type": "#microsoft.graph.fileAttachment",
                                        "name": attachment["fileName"],
                                        "contentBytes": encoded_content
                                    })
                            else:
                                raise Exception("File content is empty.")
                        else:
                            raise Exception(
                                f"Failed to download file from URL. Status code: {response.status_code}")
                    else:
                        raise Exception(
                            f"Invalid attachment type: {attachment['type']}")
            send_response = requests.post(
                url=graph_api_url, json=email_data, headers=headers)
            if send_response.status_code == 202:
                return {"message": "Email sent successfully!"}
            else:
                raise Exception(
                    f"Failed to send email. Status code: {send_response.status_code}. Response: {send_response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


##########################################  event ##########################################
    
def outlook_get_event(accessToken, params):
    """
    Retrieve a specific event from a calendar using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - The ID of the calendar containing the event.
        - :event_id: (str,required) - The ID of the event to retrieve.

    Returns:
        dict: Details of the retrieved event.
    """
    try:
        if "calendar_id" in params and "event_id" in params:
            calendar_id = params["calendar_id"]
            event_id = params["event_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events/{event_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_delete_event(accessToken, params):
    """
    Delete an event by ID using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - The ID of the calendar containing the event.
        - :event_id: (str,required) - ID of the event to be deleted.

    Returns:
        dict: A message indicating the success of the deletion.
    """
    try:
        if "calendar_id" in params and "event_id" in params:
            calendar_id = params["calendar_id"]
            event_id = params["event_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events/{event_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=graph_api_url, headers=headers)
            if response.status_code == 204:
                return {"message": "Event deleted successfully."}
            elif response.status_code == 404:
                raise Exception("Not Found.")
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_get_many_event(accessToken, params):
    """
    Retrieve multiple events from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - The ID of the calendar containing the event.
        - :limit: (str,optional) - Maximum number of events to retrieve.
        - :filter: (str,optional) - Filter criteria for events.

    Returns:
        list: List of events retrieved from Outlook.
    """
    try:
        if "calendar_id" in params:
            calendar_id = params["calendar_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events"
            limit_param = params.get("limit", "")
            filter_param = params.get("filter", "")
            query_params = []
            if limit_param:
                query_params.append(f"$top={limit_param}")
            if filter_param:
                query_params.append(f"$filter={filter_param}")
            if query_params:
                graph_api_url += "?" + "&".join(query_params)
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['value']
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_create_event(accessToken, params):
    """
    Create an event in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - ID of the calendar where the event will be created.
        - :subject: (str,required) - The subject or title of the event.
        - :start_time: (dateTime,required) - The start time of the event (e.g., "2024-01-17T14:00:00").
        - :end_time: (dateTime,required) - The end time of the event (e.g., "2024-01-17T15:00:00").
        - :body_content: (str, optional) - The description or body content of the event.
        - :show_as: (str, optional) - Availability status of the event (e.g., "free", "busy").
        - :is_all_day: (bool, optional) - Indicates whether the event is an all-day event.

    Returns:
        dict: The created event details.
    """
    try:
        if "calendar_id" in params and "subject" in params and "start_time" in params and "end_time" in params:
            calendar_id = params["calendar_id"]
            body_content = params.get("body_content")
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {
                "start": {"dateTime": params["start_time"], "timeZone": "UTC"},
                "end": {"dateTime": params["end_time"], "timeZone": "UTC"}
            }
            if body_content:
                data["body"] = {
                    "content": body_content,
                    "contentType": "HTML"
                }
            for key, value in params.items():
                skip_keys = ["calendar_id", "body_content",
                             "start_time", "end_time"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(
                url=graph_api_url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_update_event(accessToken, params):
    """
    Update a event in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - ID of the calendar where the event will be created.
        - :event_id: (str,required) - ID of the event to be updated.
        - :subject: (str,optional) - The subject or title of the event.
        - :start_time: (dateTime,optional) - The start time of the event (e.g., "2024-01-17T14:00:00").
        - :end_time: (dateTime,optional) - The end time of the event (e.g., "2024-01-17T15:00:00").
        - :body_content: (str, optional) - The description or body content of the event.
        - :show_as: (str, optional) - Availability status of the event (e.g., "free", "busy").
        - :is_all_day: (bool, optional) - Indicates whether the event is an all-day event.
        - :isOnlineMeeting: (bool, optional) - Indicates whether the event is an online meeting.
        - :hideAttendees: (bool, optional) - Indicates whether attendees should be hidden.
        - :importance: (str, optional) - The importance of the event. The possible values are: low, normal, high.
        - :categories: (list of strings , optional) - The categories associated with the event.


    Returns:
        dict: Details of the updated event.
    """
    try:
        if "event_id" in params and "calendar_id" in params:
            calendar_id = params["calendar_id"]
            event_id = params["event_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events/{event_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["calendar_id", "event_id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            if data:
                response = requests.patch(
                    url=graph_api_url, headers=headers, json=data)
                if response:
                    return response.json()
                else:
                    raise Exception(
                        f"Status code: {response.status_code}. Response: {response.text}")
            else:
                raise Exception("At least update one")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

##########################################  message attachment ##########################################


def outlook_get_many_message_attachment(accessToken, params):
    """
    Retrieves many attachments from an Outlook message using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :message_id: (str,required) -The ID of the Outlook message from which to retrieve attachments.
        - :limit: (str,optional) - Maximum number of messages to retrieve.      

    Returns:
        list: A list of dictionaries representing the attachments.
    """
    try:
        if "message_id" in params:
            message_id = params["message_id"]
            base_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments?$select=contentType,isInline,lastModifiedDateTime,name,size"
            limit_param = params.get("limit", "")
            query_params = []
            if limit_param:
                query_params.append(f"$top={limit_param}")
            if query_params:
                base_url += "?" + "&".join(query_params)
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=base_url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['value']
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def outlook_get_message_attachment(accessToken, params):
    """
    Retrieve information about an attachment of a message in Outlook.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :message_id: (str,required) - The ID of the Outlook message containing the attachment.
        - :attachment_id: (str,required) - The ID of the attachment to retrieve information.

    Returns:
        dict: A dictionary containing information about the attachment.

    """
    try:
        if "message_id" in params and "attachment_id" in params:
            message_id = params["message_id"]
            attachment_id = params["attachment_id"]
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments/{attachment_id}?$select=contentType,isInline,lastModifiedDateTime,name,size"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=graph_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)
