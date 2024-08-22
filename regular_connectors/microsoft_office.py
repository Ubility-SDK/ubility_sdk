import base64
import requests
import json

def office_365_refresh_access_token(creds):
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


def office_365_get_many_contact(accessToken, params):
    """
    Retrieve multiple contacts from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :contact_folder_id: (str,optional) - If empty, will search for contacts in the default Contacts folder.
        - :limit: (int,optional) - Maximum number of contacts to retrieve.
        - :first_name: (str,optional) - first name to filter by
        - :last_name: (str,optional) - last name to filter by
        - :email: (str,optional) - email to filter by

    Returns:
        list: List of contacts retrieved from Outlook.
    """
    try:
        contact_folder_id = params.get("contact_folder_id", "")
        limit_param = params.get("limit", "")
        first_name = params.get("first_name", "")
        last_name = params.get("last_name", "")
        email = params.get("email", "")
        filter_param = []
        query_params = {}
        if first_name:
            filter_param.append(f"contains(givenName,'{first_name}')")
        if last_name:
            filter_param.append(f"contains(surname,'{last_name}')")
        if email:
            filter_param.append(f"emailAddresses/any(i:i/address eq '{email}')")
        if limit_param:
            query_params["$top"]= limit_param
        if filter_param:
            query_params["$filter"] = " and ".join(filter_param)
        graph_api_url = ""
        if contact_folder_id:
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/contactFolders/{contact_folder_id}/contacts"
        else:
            graph_api_url = "https://graph.microsoft.com/v1.0/me/contacts"
        headers = {
            "Authorization": "Bearer " + accessToken,
        }
        if query_params:
            response = requests.get(url=graph_api_url, headers=headers, params=query_params)
        else:
            response = requests.get(url=graph_api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def office_365_create_contact(accessToken, params):
    """
    Create a contact in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :contact_folder_id: (str,optional) - If empty, will create contact in the default Contacts folder.
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
            
        - :jobTitle: (Str,optional) - The contact's job title.
        - :companyName: (Str,optional) - The name of the contact's company.
        - :department: (Str,optional) - The contact's department.
        - :personalNotes: (Str,optional) - The user's notes about the contact.
        - :fileAs: (Str,optional) - The name the contact is filed under.

    Returns:
        dict: Details of the created contact.
    """
    try:
        if "givenName" in params:
            contact_folder_id = params.get("contact_folder_id", "")
            graph_api_url = ""
            if contact_folder_id:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/contactFolders/{contact_folder_id}/contacts"
            else:
                graph_api_url = "https://graph.microsoft.com/v1.0/me/contacts"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            ignore_keys = ["contact_folder_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }
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


def office_365_update_contact(accessToken, params):
    """
    Update a contact in Outlook using the Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (str,required) - ID of the contact to be updated.
        - :contact_folder_id: (str,optional) - If empty, will Update contact in the default Contacts folder.
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
            contact_folder_id = params.get("contact_folder_id", "")
            graph_api_url = ""
            if contact_folder_id:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/contactFolders/{contact_folder_id}/contacts/{contact_id}"
            else:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            ignore_keys = ["contact_folder_id", "contact_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }
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


##########################################  message ##########################################


def office_365_send_message(accessToken, params):
    """
    Send a message in Outlook.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :sender: (str,optional) - The account that is actually used to generate the message. You can set this property to a different value when sending a message from a shared mailbox, for a shared calendar, or as a delegate.
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
            sender = params.get("sender", "")
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
            if sender:
                email_data["message"]["sender"] = sender
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


def office_365_create_message_draft(accessToken, params):
    """
    Create a message draft in Outlook.

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
            graph_api_url = "https://graph.microsoft.com/v1.0/me/messages"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            email_data = {
                "subject": subject,
                "body": {
                    "content": body,
                    "contentType": bodyFormat
                },
                "toRecipients": [{"emailAddress": {"address": email}} for email in to_emails],
                "ccRecipients": [{"emailAddress": {"address": email}} for email in cc_emails],
                "bccRecipients": [{"emailAddress": {"address": email}} for email in bcc_emails],
            }
            if attachments:
                email_data["attachments"] = []
                for attachment in attachments:
                    if attachment["type"] == "ByteString":
                        email_data["attachments"].append({
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
                                email_data["attachments"].append(
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
            create_response = requests.post(
                url=graph_api_url, json=email_data, headers=headers)
            if create_response.status_code == 201:
                return create_response.json()
            else:
                raise Exception(
                    f"Failed to create email. Status code: {create_response.status_code}. Response: {create_response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


##########################################  event ##########################################


def office_365_delete_event(accessToken, params):
    """
    Delete an event by ID using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,optional) - The ID of the calendar containing the event. If empty, will accept an event from any calendar. .
        - :event_id: (str,required) - ID of the event to be deleted.

    Returns:
        dict: A message indicating the success of the deletion.
    """
    try:
        if "event_id" in params:
            calendar_id = params.get("calendar_id", "")
            event_id = params["event_id"]
            graph_api_url = ""
            if calendar_id:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events/{event_id}"
            else:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
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


def office_365_get_many_event(accessToken, params):
    """
    Retrieve multiple events from Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,optional) - The ID of the calendar containing the event. If empty, will default to your default calendar.
        - :limit: (str,optional) - Maximum number of events to retrieve.
        - :search: (str,optional) - search criteria for events.
        - :start_date: (str,optional) - Date and time of when this event starts.
        - :end_date: (str,optional) - Date and time of when this event ends.

    Returns:
        list: List of events retrieved from Outlook.
    """
    try:
        calendar_id = params.get("calendar_id", "")
        limit_param = params.get("limit", "")
        search_param = params.get("search", "")
        start_date_param = params.get("start_date", "")
        end_date_param = params.get("end_date", "")
        query_params = {}
        filter_param = []
        graph_api_url = ""
        if start_date_param:
            filter_param.append(f"start/dateTime ge '{start_date_param}'")
        if end_date_param:
            filter_param.append(f"end/dateTime le '{end_date_param}'")
        if search_param:
            filter_param.append(search_param)
        if limit_param:
            query_params["$top"]= limit_param
        if filter_param:
            query_params["$filter"] = " and ".join(filter_param)
        if calendar_id:
            graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events"
        else:
            graph_api_url = "https://graph.microsoft.com/v1.0/me/calendar/events"
        headers = {
            "Authorization": "Bearer " + accessToken,
        }
        if query_params:
            response = requests.get(url=graph_api_url, headers=headers, params=query_params)
        else:
            response = requests.get(url=graph_api_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['value']
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def office_365_create_event(accessToken, params):
    """
    Create an event in Outlook using Microsoft Graph API.

    :param str accessToken: Access token for authentication with Microsoft Graph API.
    :param dict params: Dictionary containing parameters.

        - :calendar_id: (str,required) - ID of the calendar where the event will be created. If empty, will default to your default calendar.
        - :subject: (str,required) - The subject or title of the event.
        - :start_time: (dateTime,required) - The start time of the event (e.g., "2024-01-17T14:00:00").
        - :end_time: (dateTime,required) - The end time of the event (e.g., "2024-01-17T15:00:00").
        - :showAs: (str, optional) - Availability status of the event (e.g., "free", "busy").
        - :isAllDay: (bool, optional) - Indicates whether the event is an all-day event.
        - :categories: (list of string, optional) - The categories associated with the event. Each category corresponds to the displayName property of an `outlookCategory <https://learn.microsoft.com/en-us/graph/api/resources/outlookcategory?view=graph-rest-1.0>`_ defined for the user.
        - :attendees: (list of str, optional) - list containing attendee email addresses
        - :location: (str, optional) - The location of the event.
        - :body: (dict, optional) - dictionary containing The description or body content of the event in html or text format.
        
            - :contentType: (str, optional) - Possible values: (text, html)
            - :content: (str, optional) - The content of the event in html or text format depending on contentType value.
        

    Returns:
        dict: The created event details.
    """
    try:
        if "subject" in params and "start_time" in params and "end_time" in params:
            calendar_id = params.get("calendar_id", "")
            attendees = params.get("attendees", [])
            location = params.get("location", "")
            if calendar_id:
                graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events"
            else:
                graph_api_url = "https://graph.microsoft.com/v1.0/me/calendar/events"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {
                "start": {"dateTime": params["start_time"], "timeZone": "UTC"},
                "end": {"dateTime": params["end_time"], "timeZone": "UTC"}
            }
            if attendees:
                data["attendees"] = [{"emailAddress": {"address": email}} for email in attendees]
            if location:
                data["location"] = {"displayName": location}
            for key, value in params.items():
                skip_keys = ["calendar_id", "start_time", "end_time", "attendees", "location"]
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

