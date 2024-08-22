import json
import requests
status = [200, 201, 202, 204, 206, 207, 208]
def ref_token(creds):
    try:
        cred=json.loads(creds)
        token_endpoint="https://login.microsoftonline.com/common/oauth2/v2.0/token"
        request_body = {
            'client_id': cred['clientId'],
            'client_secret': cred['clientSecret'],
            'scope': ' '.join(['https://graph.microsoft.com/.default'] +['offline_access']),
            'refresh_token': cred['refreshToken'],
            'grant_type': 'refresh_token',
        }
        response = requests.post(token_endpoint, data=request_body)
        response_json = response.json()
        if "access_token" in response_json:
            print(response_json["access_token"])
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}
    except Exception as error:
        raise Exception(error)
    
def teams_get_many_teams(accessToken):  
    """
    Retrieve information about joined teams in Microsoft Teams.

    :param str accessToken: Microsoft Graph API access token. (required)

    :return: Information about the joined teams.
    :rtype: dict
    """
    try:
        graph_endpoint = "https://graph.microsoft.com/v1.0/me/joinedTeams"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accessToken}",
        }
        response = requests.get(graph_endpoint, headers=headers)
        if response.status_code in status:
            teams = response.json()
            return teams
        else:
            raise Exception(response.text)
    except Exception as e:
        raise Exception(f'error:{e}')
    
def create_team(accessToken,params):
    """
    Create a new team in Microsoft Teams.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - displayName (str): Display name of the new team. (required)
        - description (str): Description of the new team. (optional)
        - template@odata.bind (str): Template for the new team. (required)

    :return: Success message if the team is created successfully.
    :rtype: str
    """
    try:
        if 'displayName' and 'template@odata.bind' in params:
            graph_endpoint = "https://graph.microsoft.com/v1.0/teams"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.post(graph_endpoint, headers=headers, json=params)
            if response.status_code in status:
                return 'Created successfully.'
            else:
                raise Exception(response.text)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    
def get_channels_for_team(accessToken,params):
    """
    Retrieve channels for a team in Microsoft Teams.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - team_id (str): ID of the team to retrieve channels for. (required)

    :return: Information about the channels in the team.
    :rtype: dict
    """
    try:
        if "team_id" in params:
            team_id = params.pop("team_id")
            graph_endpoint = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels"
            headers = {
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.get(graph_endpoint, headers=headers, params=params)
            if response.status_code in status:
                channels = response.json()
                return channels
            else:
                raise Exception(response.text)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    
def get_channel(accessToken,params):
    """
    Retrieve information about a channel in a team in Microsoft Teams.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - team_id (str): ID of the team containing the channel. (required)
        - channel_id (str): ID of the channel to retrieve. (required)

    :return: Information about the specified channel.
    :rtype: dict
    """
    try:
        if "team_id" and "channel_id" in params:
            graph_endpoint = f"https://graph.microsoft.com/v1.0/teams/{params['team_id']}/channels/{params['channel_id']}"
            headers = {
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.get(graph_endpoint, headers=headers)
            if response.status_code in status:
                channel = response.json()
                return channel
            else:
                raise Exception(response.text)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    
def send_message(accessToken,params):
    """
    Send a message to a channel in a team in Microsoft Teams.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - team_id (str): ID of the team containing the channel. (required)
        - channel_id (str): ID of the channel to send the message to. (required)
        - body (dict): Message body containing the content. (required)
            - content (str): Content of the message. (required)
            - contentType (str): Type of content. (optional)

    :return: Information about the sent message.
    :rtype: dict
    """
    try:
        if "team_id" in params and "channel_id" in params:
            team_id = params.pop("team_id")
            channel_id = params.pop("channel_id")
            graph_endpoint = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json"
            }
            response = requests.post(graph_endpoint, headers=headers, json=params)
            if response.status_code in status:
                message_data = response.json()
                return message_data
            else:
                raise Exception(response.text)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)