import json
import requests
status=[200, 201, 202, 204, 206, 207, 208] 
def refresh_access_token(cred):
    try:
        creds=json.loads(cred)
        token_params = {
        'grant_type': 'refresh_token',
        'refresh_token':creds['refreshToken'],
        'client_id': creds['clientID'],
        'client_secret': creds['clientSecret'],
    }
        response = requests.post('https://zoom.us/oauth/token', data=token_params)
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        raise(e)
    except Exception as e:
        raise Exception(e)

def zoom_create_meeting(params, access_token):
    """
    Create a Zoom meeting.

    :param dict params:
        - topic (str): Topic of the meeting. (required)
        - agenda (str): Agenda for the meeting. (optional)
        - duration (int): Duration of the meeting in minutes. (optional)
        - password (str): Password for the meeting. (optional)
        - schedule_for (str): Email address of the user to schedule the meeting for. (optional)
        - start_time (str): Start time of the meeting in the format "YYYY-MM-DDTHH:mm:ssZ". (optional)
        - timezone (str): Timezone for the meeting. (optional)
        - type (int): Type of meeting. (required)
        - settings (dict):
            - audio (str): Audio options for the meeting. (optional)
            - alternative_hosts (str): Email addresses of alternative hosts for the meeting. (optional)
            - auto_recording (str): Auto-recording setting for the meeting. (optional)
            - host_video (boolean): Start video when the host joins the meeting. (optional)
            - join_before_host (boolean): Allow participants to join the meeting before the host starts the meeting. (optional)
            - mute_upon_entry (boolean): Mute participants upon entry. (optional)
            - participant_video (boolean): Start video when participants join the meeting. (optional)
            - watermark (boolean): Whether to add a watermark when viewing a shared screen. (optional)
            - registration_type (int): Registration type for the meeting. (optional)

    :param str access_token: Zoom API access token. (required)

    :return: Information about the created Zoom meeting.
    :rtype: dict
    """
    try:
        if access_token:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            url = 'https://api.zoom.us/v2/users/me/meetings'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f'Meeting creation failed:{response.text}')
        else:
            raise Exception('Missing parameters')   
    except requests.exceptions.RequestException as e:
        raise(e)
    except Exception as e:
        raise Exception(e)

def zoom_get_meeting(params, access_token):
    """
    Retrieve information about a Zoom meeting.

    :param dict params:
        - meetingId (str): ID of the Zoom meeting to retrieve information. (required)
        - occurrences (list):
            - occurrence_id: Occurrence Id for the meeting. (optional)

    :param str access_token: Zoom API access token. (required)

    :return: Information about the Zoom meeting.
    :rtype: dict
    """
    try:
        if 'meetingId' in params and access_token:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            url = f'https://api.zoom.us/v2/meetings/{data["meetingId"]}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(url, headers=headers, params=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f'Meeting retrieval failed:{response.text}')
        else:
            raise Exception('Missing parameters')   
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def zoom_list_meetings(params, access_token):
    """
    List Zoom meetings for a specific user.

    :param dict params:
        - page_size (int): Number of meetings per page. (optional)
        - type (str): Type of meetings to list. (optional)

    :param str access_token: Zoom API access token. (required)

    :return: List of Zoom meetings.
    :rtype: dict
    """
    try:
        if access_token:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            url = 'https://api.zoom.us/v2/users/me/meetings'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(url, headers=headers, params=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f'Meeting listing failed:{response.text}')
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def zoom_update_meeting(params, access_token):
    """
    Update information for a Zoom meeting.

    :param dict params:
        - meeting_id (str): ID of the Zoom meeting to update. (required)
        - topic (str): Topic of the meeting. (optional)
        - agenda (str): Agenda for the meeting. (optional)
        - duration (int): Duration of the meeting in minutes. (optional)
        - password (str): Password for the meeting. (optional)
        - schedule_for (str): Email address of the user to schedule the meeting for. (optional)
        - start_time (str): Start time of the meeting in the format "YYYY-MM-DDTHH:mm:ssZ". (optional)
        - timezone (str): Timezone for the meeting. (optional)
        - type (int): Type of meeting. (optional)
        - settings (dict):
            - audio (str): Audio options for the meeting. (optional)
            - alternative_hosts (str): Email addresses of alternative hosts for the meeting. (optional)
            - auto_recording (str): Auto-recording setting for the meeting. (optional)
            - host_video (boolean): Start video when the host joins the meeting. (optional)
            - join_before_host (boolean): Allow participants to join the meeting before the host starts the meeting. (optional)
            - mute_upon_entry (boolean): Mute participants upon entry. (optional)
            - participant_video (boolean): Start video when participants join the meeting. (optional)
            - watermark (boolean): Whether to add a watermark when viewing a shared screen. (optional)
            - registration_type (int): Registration type for the meeting. (optional)

    :param str access_token: Zoom API access token. (required)

    :return: Success message indicating the meeting was updated.
    :rtype: str
    """
    try:
        if 'meeting_id' in params and access_token:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            url = f'https://api.zoom.us/v2/meetings/{data["meeting_id"]}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code in status:
                return "Meeting updated successfully"
            else:
                raise Exception(f'Meeting update failed:{response.text}')
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def zoom_delete_meeting(params, access_token):
    """
    Delete a Zoom meeting.

    :param dict params:
        - meeting_id (str): ID of the Zoom meeting to delete. (required)

    :param str access_token: Zoom API access token. (required)

    :return: Success message indicating the meeting was deleted.
    :rtype: str
    """
    try:
        if 'meeting_id' in params and access_token:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            url = f'https://api.zoom.us/v2/meetings/{data["meeting_id"]}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.delete(url, headers=headers, params=data)
            if response.status_code in status:
                return "Meeting deleted successfully"
            else:
                raise Exception(f'Meeting deletion failed:{response.text}')
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

    """
    Delete a Zoom meeting.

    Args:
    - params (dict): Dictionary containing parameters to delete a Zoom meeting.
        meeting_id (str): ID of the Zoom meeting to delete. (required)

    - access_token (str): Zoom API access token. (required)

    Returns:
    - str: Success message indicating the meeting was deleted.
    """
    try:
        if 'meeting_id' in params and access_token:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            url = f'https://api.zoom.us/v2/meetings/{data["meeting_id"]}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.delete(url, headers=headers,params=data)
            if response.status_code in status:
                return "Meeting deleted successfully"
            else:
                raise Exception(f'Meeting deletion failed:{response.text}')
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)