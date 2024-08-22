import json
import requests

status = [200, 201, 202, 204, 206, 207, 208]

def grafana_create_dashboard(params,cred):
    """
    Create an empty dashboard in Grafana.

    :param dict params:
        - dashboard (dict):
            - id (int): none to create a new dashboard. (required)
            - title (str): Title of the new Dashboard. (required)
        - folderUid (str): The UID of the folder to save the dashboard in. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the created dashboard.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "title" in params["dashboard"] and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/dashboards/db"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.post(GRAFANA_API_URL, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_get_dashboard(params,cred):
    """
    Get a dashboard by the UID in Grafana.

    :param dict params:
        - uid (str): The UID of the dashboard. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about a specified dashboard.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "uid" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/dashboards/uid/{data['uid']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.get(GRAFANA_API_URL, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_delete_dashboard(params,cred):
    """
    Delete a dashboard by the UID in Grafana.

    :param dict params:
        - uid (str): The UID of the dashboard. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about deleted dashboard.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "uid" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/dashboards/uid/{data['uid']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.delete(GRAFANA_API_URL, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_get_many_dashboard(params,cred):
    """
    Retrieve information about one or multiple dashboards in Grafana.

    :param dict params:
        - type (str): Type to search for, in this case dash-db for dashboards. (required)
        - limit (int): Limit the number of returned results. (optional)
        - query (str): Search query. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the requested dashboards.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'type' in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/search/"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.get(GRAFANA_API_URL, headers=headers, params=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_update_dashboard(params,cred):
    """
    Update information for a specific dashboard in Grafana.

    :param dict params:
        - dashboard (dict):
            - uid: dashboard uid. (required)
            - title (str): Dashboard title to update. (optional)
        - overwrite (boolean): Set to true if you want to overwrite an existing dashboard with a newer version. (required)
        - folderUid (str): The UID of the folder to save the dashboard in. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the updated dashboard.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "uid" in params["dashboard"] and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/dashboards/db"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.post(GRAFANA_API_URL, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_create_team(params,cred):
    """
    Create a team in Grafana.

    :param dict params:
        - name (str): Name of the team. (required)
        - email (str): Email address associated with the team. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the created team.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "name" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.post(GRAFANA_API_URL, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_delete_team(params,cred):
    """
    Delete a team in Grafana.

    :param dict params:
        - teams_id (str): ID of the team to delete. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the deleted team.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "teams_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams/{data['teams_id']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.delete(GRAFANA_API_URL, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_get_team(params,cred):
    """
    Retrieve information about a team in Grafana.

    :param dict params:
        - teams_id (str): ID of the team to retrieve information. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the specified team.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "teams_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams/{data['teams_id']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.get(GRAFANA_API_URL, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_get_many_team(params,cred):
    """
    Retrieve information about multiple teams in Grafana.

    :param dict params:
        - perpage (int): Number of teams per page. (optional)
        - name (str): Filter teams by name. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the requested teams.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams/search"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.get(GRAFANA_API_URL, headers=headers, params=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_update_team(params,cred):
    """
    Update information for a team in Grafana.

    :param dict params:
        - team_id (str): ID of the team to update. (required)
        - name (str): New name for the team. (optional)
        - email (str): New email address for the team. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the updated team.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "team_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams/{data['team_id']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.put(GRAFANA_API_URL, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_get_many_users(params,cred):
    """
    Retrieve information about multiple users in Grafana.

    :param dict params:
        - limit (int): Limit the number of users returned. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the requested users.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/org/users"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.get(GRAFANA_API_URL, headers=headers, params=data)
            if response.status_code in status:
                print(response.json())
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_update_user(params,cred):
    """
    Update information for a user in Grafana.

    :param dict params:
        - user_id (int): ID of the user to update. (required)
        - role (str): New role for the user. (optional)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the updated user.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "user_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if key == "user_id":
                    continue
                else:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/org/users/{params['user_id']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.patch(GRAFANA_API_URL, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_delete_user(params,cred):
    """
    Delete a user in Grafana.

    :param dict params:
        - user_id (int): ID of the user to delete. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the deleted user.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "user_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/org/users/{data['user_id']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.delete(GRAFANA_API_URL, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def grafana_get_team_members(params,cred):
    """
    Retrieve information about members of a team in Grafana.

    :param dict params:
        - team_id (str): ID of the team to retrieve members. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the team members.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "team_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams/{data['team_id']}/members"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.get(GRAFANA_API_URL, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
def grafana_delete_team_members(params,cred):
    """
    Remove a user from a team in Grafana.

    :param dict params:
        - team_id (str): ID of the team from which to remove the user. (required)
        - user_id (str): ID of the user to be removed from the team. (required)
    :param str token: Token for authenticating with Grafana API. (required)
    :param str domain: Base URL of your Grafana instance. (required)

    :return: Information about the removed team member.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if "team_id" in params and "user_id" in params and 'accessToken' in creds and 'domain' in creds:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            GRAFANA_API_URL = f"https://{creds['domain']}/api/teams/{data['team_id']}/members/{data['user_id']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds['accessToken']}",
            }
            response = requests.delete(GRAFANA_API_URL, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
