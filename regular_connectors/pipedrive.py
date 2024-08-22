import json
import requests
status = [200, 201, 202, 204, 206, 207, 208]

def pipedrive_refresh_token(cred):
    try:
        creds=json.loads(cred)
        token_endpoint = "https://oauth.pipedrive.com/oauth/token"
        data = {
            'grant_type': 'refresh_token',
            'client_id': creds['clientID'],
            'client_secret': creds['clientSecret'],
            'refresh_token': creds['refreshToken'],
        }
        response = requests.post(token_endpoint, data=data)
        if response.status_code in status:
            token_data = response.json()['access_token']
            return token_data
        else:
            raise Exception(f"Failed to refresh Pipedrive token. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(e)

def pipedrive_create_activity(access_token,params):
    """
    Create a new activity in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - subject (str): Subject of the activity. (required)
        - note (str): Note or description for the activity. (optional)
        - due_date (str): Due date for the activity. (optional)
        - person_id (int): ID of the person associated with the activity. (optional)
        - type (str): Type of the activity. (optional)
        - done (int): Flag indicating whether the activity is done (1) or not done (0). (optional)
        - deal_id (int): ID of the deal associated with the activity. (optional)
        - org_id (int): ID of the organization associated with the activity. (optional)
        - user_id (int): ID of the user responsible for the activity. (optional)

    :return: Information about the created activity obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'subject' in params:
            endpoint = "https://api.pipedrive.com/v1/activities"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                activity_data = response.json()
                return activity_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)
    
def pipedrive_delete_activity(access_token,params):
    """
    Delete a Pipedrive activity.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the activity to be deleted. (required)

    :return: A success message if the activity is deleted successfully.
    :rtype: str
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/activities/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.delete(endpoint, headers=headers)
            if response.status_code in status:
                return "Activity deleted successfully"
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_get_activity(access_token,params):
    """
    Retrieve information about a Pipedrive activity.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the activity to be retrieved. (required)

    :return: Information about the specified Pipedrive activity obtained from the API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/activities/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code in status:
                data=response.json()
                return data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_get_many_activity(access_token,params):
    """
    Retrieve multiple Pipedrive activities based on specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - filter_id (int): ID of the filter to be applied. (optional)
        - type (str): Type of activities to retrieve, e.g., 'call'. (optional)
        - limit (int): Maximum number of activities to retrieve. (optional)
        - start_date (str): Start date for filtering activities. (optional)
        - end_date (str): End date for filtering activities. (optional)
        - done (int): Indicator for completed activities, e.g., '0' for not done. (optional)

    :return: Information about Pipedrive activities based on the specified parameters obtained from the API.
    :rtype: dict
    """
    try:
            endpoint = f"https://api.pipedrive.com/v1/activities"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers,params=params)
            if response.status_code in status:
                data=response.json()
                return data
            else:
                raise Exception(f"Failed. Response: {response.text}")
    except Exception as e:
        raise Exception(e)
    
def pipedrive_update_activity(access_token,params):
    """
    Update a Pipedrive activity with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the activity to be updated. (required)
        - subject (str): Subject of the activity. (optional)
        - note (str): Additional notes for the activity. (optional)
        - due_date (int): Due date for the activity. (optional)
        - person_id (int): ID of the person associated with the activity. (optional)
        - type (str): Type of the activity, e.g., 'meet'. (optional)
        - done (int): Indicator for the completion status of the activity, e.g., 0 for not done. (optional)
        - org_id (int): ID of the organization associated with the activity. (optional)
        - user_id (int): ID of the user associated with the activity. (optional)

    :return: Information about the updated Pipedrive activity obtained from the API.
    :rtype: dict
    """
    try:
        if 'id' in params: 
            endpoint = f"https://api.pipedrive.com/v1/activities/{params['id']}"    
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.put(endpoint, headers=headers, json=params)
            if response.status_code in status:
                activity_data = response.json()
                return activity_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_create_product(access_token,params):
    """
    Create a product in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - name (str): Name of the product. (required)
        - code (str): Product code or identifier. (optional)
        - unit (str): Unit of the product. (optional)
        - tax (float): Tax information for the product. (optional)
        - active_flag (bool): Indicator for the product's active status. (optional)
        - owner_id (int): ID of the owner associated with the product. (optional)
        - prices (list): List containing dictionaries with pricing details:
            - currency (str): Currency of the price.
            - price (float): Price of the product.
            - cost (float): Cost price of the product.
            - overhead_cost (float): Overhead cost of the product.

    :return: Information about the created product obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'name' in params:
            endpoint = "https://api.pipedrive.com/v1/products"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                product_data = response.json()
                return product_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_get_many_products(access_token,params):
    """
    Retrieve information about multiple products from Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - limit (int): Number of items to retrieve per page. (optional)

    :return: Information about multiple products obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        endpoint = "https://api.pipedrive.com/v1/products"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code in status:
            products_data = response.json()
            return products_data
        else:
            raise Exception(f"Failed. Response: {response.text}")
    except Exception as e:
        raise Exception(e)

def pipedrive_get_product(access_token,params):
    """
    Retrieve information about a specific product from Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the product to retrieve. (required)

    :return: Information about the specified product obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/products/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code in status:
                product_data = response.json()
                return product_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

   
def pipedrive_delete_product(access_token,params):
    """
    Delete a product in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the product to delete. (required)

    :return: Message indicating the success of the deletion.
    :rtype: str
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/products/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.delete(endpoint, headers=headers)
            if response.status_code in status:
                return "Product deleted successfully."
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception("Missing required parameters")
    except Exception as e:
        raise Exception(e)

def pipedrive_create_person(access_token,params):
    """
    Create a person in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - name (str): Name of the person. (required)
        - email (list): Email address of the person. (optional)
        - label (int): The ID of the label. (optional)
        - marketing_status (str): Marketing status of the person. (optional)
        - org_id (int): Organization ID associated with the person. (optional)
        - phone (list): Phone number of the person. (optional)

    :return: Information about the created person obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'name' in params:
            endpoint = "https://api.pipedrive.com/v1/persons"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                person_data = response.json()
                return person_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_delete_person(access_token,params):
    """
    Delete a person in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the person to be deleted. (required)

    :return: Success message if the person is deleted successfully.
    :rtype: str
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/persons/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.delete(endpoint, headers=headers)
            if response.status_code in status:
                return "Person deleted successfully."
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception("Missing required parameters")
    except Exception as e:
        raise Exception(e)

def pipedrive_get_person(access_token,params):
    """
    Retrieve information about a person in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the person to retrieve information. (required)

    :return: Information about the specified person obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/persons/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code in status:
                person_data = response.json()
                return person_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception("Missing required parameters")
    except Exception as e:
        raise Exception(e)

def pipedrive_get_many_persons(access_token,params):
    """
    Retrieve information about multiple persons in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - filter_id (int): ID of the filter to apply. (optional)
        - first_char (str): First character to filter persons by. (optional)
        - limit (int): Limit the number of persons returned. (optional)

    :return: Information about multiple persons obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        endpoint = "https://api.pipedrive.com/v1/persons"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code in status:
            persons_data = response.json()
            return persons_data
        else:
            raise Exception(f"Failed. Response: {response.text}")
    except Exception as e:
        raise Exception(e)

def pipedrive_search_persons(access_token,params):
    """
    Search for persons in Pipedrive based on specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - term (str): Search term. (required)
        - include_fields (str): Comma-separated list of fields to include in the response. (optional)
        - fields (str): Search query for fields. (optional)
        - organization_id (int): ID of the organization to filter by. (optional)
        - exact_match (bool): When enabled, only full exact matches against the given term are returned. (optional)
        - limit (int): Limit the number of persons returned. (optional)

    :return: Information about persons matching the search criteria obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'term' in params:
            endpoint = "https://api.pipedrive.com/v1/persons/search"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers, params=params)
            if response.status_code in status:
                persons_data = response.json()
                return persons_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)
    
def pipedrive_update_person(access_token,params):
    """
    Update a person in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the person to update. (required)
        - name (str): Name of the person. (optional)
        - email (list): List of email addresses associated with the person. (optional)
        - phone (list): List of phone numbers associated with the person. (optional)
        - org_id (int): ID of the organization associated with the person. (optional)
        - label (int): ID of the label associated with the person. (optional)
        - marketing_status (str): Marketing status of the person. (optional)

    :return: Information about the updated person obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            person_id = params.pop('id')
            endpoint = f"https://api.pipedrive.com/v1/persons/{person_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.put(endpoint, headers=headers, json=params)
            if response.status_code in status:
                updated_person_data = response.json()
                return updated_person_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_create_organization(access_token,params):
    """
    Create an organization in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - name (str): Name of the organization. (required)
        - label (int): ID of the label associated with the organization. (optional)

    :return: Information about the created organization obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'name' in params:
            endpoint = "https://api.pipedrive.com/v1/organizations"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                organization_data = response.json()
                return organization_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_delete_organization(access_token,params):
    """
    Delete an organization in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the organization to be deleted. (required)

    :return: Message indicating the success of the deletion.
    :rtype: str
    """
    try:
        if 'id' in params:
            organization_id = params['id']
            endpoint = f"https://api.pipedrive.com/v1/organizations/{organization_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.delete(endpoint, headers=headers)
            if response.status_code in status:
                return "Organization deleted successfully."
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_get_organization(access_token,params):
    """
    Get information about an organization in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the organization to retrieve information. (required)

    :return: Information about the organization obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            organization_id = params['id']
            endpoint = f"https://api.pipedrive.com/v1/organizations/{organization_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code in status:
                organization_data = response.json()
                return organization_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_get_many_organizations(access_token,params):
    """
    Get information about multiple organizations in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - filter_id (int): ID of the filter to apply. (optional)
        - first_char (str): First character to filter organizations. (optional)
        - limit (int): Limit the number of organizations to retrieve. (optional)

    :return: Information about multiple organizations obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        endpoint = "https://api.pipedrive.com/v1/organizations"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code in status:
            organizations_data = response.json()
            return organizations_data
        else:
            raise Exception(f"Failed. Response: {response.text}")
    except Exception as e:
        raise Exception(e)

def pipedrive_search_organizations(access_token,params):
    """
    Search for organizations in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - term (str): Search term for organizations. (required)
        - limit (int): Limit the number of organizations to retrieve. (optional)
        - exact_match (bool): Set to True for an exact match search. (optional)

    :return: Information about organizations obtained from the Pipedrive API based on the search.
    :rtype: dict
    """
    try:
        if 'term' in params:
            endpoint = "https://api.pipedrive.com/v1/organizations/search"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers, params=params)
            if response.status_code in status:
                organizations_data = response.json()
                return organizations_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_update_organization(access_token,params):
    """
    Update an organization in Pipedrive based on the provided parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the organization to update. (required)
        - name (str): Updated name of the organization. (optional)
        - label (int): Updated label of the organization. (optional)
        - owner_id (int): Updated owner ID of the organization. (optional)

    :return: Information about the updated organization obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            organization_id = params.pop('id')
            endpoint = f"https://api.pipedrive.com/v1/organizations/{organization_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.put(endpoint, headers=headers, json=params)
            if response.status_code in status:
                organization_data = response.json()
                return organization_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)
 
def pipedrive_create_note(access_token,params):
    """
    Create a note in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - content (str): Content of the note. (required)
        - lead_id (int): ID of the lead associated with the note. (optional)
        - deal_id (int): ID of the deal associated with the note. (optional)
        - person_id (int): ID of the person associated with the note. (optional)
        - org_id (int): ID of the organization associated with the note. (optional)

    :return: Information about the created note obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'content' in params:
            endpoint = "https://api.pipedrive.com/v1/notes"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                note_data = response.json()
                return note_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_delete_note(access_token,params):
    """
    Delete a note in Pipedrive with the specified ID.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the note to be deleted. (required)

    :return: Message indicating the success of the deletion.
    :rtype: str
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/notes/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.delete(endpoint, headers=headers)
            if response.status_code in status:
                return "Note deleted successfully."
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)


def pipedrive_get_note(access_token,params):
    """
    Retrieve information about a note in Pipedrive with the specified ID.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the note to retrieve. (required)

    :return: Information about the specified note obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/notes/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code in status:
                note_data = response.json()
                return note_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_get_many_notes(access_token,params):
    """
    Retrieve information about multiple notes in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - deal_id (int): ID of the deal associated with the notes. (optional)
        - lead_id (int): ID of the lead associated with the notes. (optional)
        - org_id (int): ID of the organization associated with the notes. (optional)
        - person_id (int): ID of the person associated with the notes. (optional)
        - limit (int): Maximum number of notes to retrieve. (optional)

    :return: Information about the specified notes obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        endpoint = "https://api.pipedrive.com/v1/notes"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code in status:
            notes_data = response.json()
            return notes_data
        else:
            raise Exception(f"Failed. Response: {response.text}")
    except Exception as e:
        raise Exception(e)

def pipedrive_update_note(access_token,params):
    """
    Update a note in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - id (int): ID of the note to be updated. (required)
        - content (str): Content of the note. (optional)
        - deal_id (int): ID of the deal associated with the note. (optional)
        - lead_id (int): ID of the lead associated with the note. (optional)
        - org_id (int): ID of the organization associated with the note. (optional)
        - person_id (int): ID of the person associated with the note. (optional)

    :return: Information about the updated note obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'id' in params:
            endpoint = f"https://api.pipedrive.com/v1/notes/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.put(endpoint, headers=headers, json=params)
            if response.status_code in status:
                note_data = response.json()
                return note_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)


def pipedrive_create_lead(access_token,params):
    """
    Create a lead in Pipedrive with the specified parameters.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - title (str): Title of the lead. (required)
        - expected_close_date (str): Expected close date of the lead. (optional)
        - owner_id (int): ID of the owner associated with the lead. (optional)
        - person_id (int): ID of the person associated with the lead. (optional)
        - organization_id (int): ID of the organization associated with the lead. (optional)

    :return: Information about the created lead obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'title' in params:
            endpoint = "https://api.pipedrive.com/v1/leads"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                lead_data = response.json()
                return lead_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

def pipedrive_create_deal(access_token,params):
    """
    Create a deal in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - title (str): Title of the deal. (required)
        - value (str): Value of the deal. (optional)
        - currency (str): Currency of the deal value, e.g., 'USD'. (optional)
        - org_id (int): ID of the organization associated with the deal. (optional)
        - person_id (int): ID of the person associated with the deal. (optional)
        - user_id (int): ID of the user responsible for the deal. (optional)
        - stage_id (int): ID of the deal stage. (optional)
        - status (str): Status of the deal, e.g., 'open', 'won', 'lost'. (optional)
        - lost_reason (str): Reason for losing the deal. (optional)
        - probability (float): Probability of winning the deal. (optional)

    :return: Information about the created deal obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'title' in params:
            endpoint = "https://api.pipedrive.com/v1/deals"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                deal_data = response.json()
                return deal_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)


def pipedrive_add_product_to_deal(access_token,params):
    """
    Add a product to a deal in Pipedrive.

    :param str access_token: Pipedrive API access token. (required)
    :param dict params:
        - deal_id (int): ID of the deal to which the product will be added. (required)
        - product_id (int): ID of the product to be added to the deal. (required)
        - item_price (float): Price of the product item. (required)
        - quantity (int): How many items of this product will be added to the deal (required)
        - comments (str): Comments or notes about the product. (optional)
        - discount_type (str): The type of the discount's value.
        - discount (float): The value of the discount. (optional)
        - product_variation_id (int): ID of the product variation. (optional)

    :return: Information about the added product obtained from the Pipedrive API.
    :rtype: dict
    """
    try:
        if 'deal_id' in params and 'product_id' in params and 'item_price' in params and 'quantity' in params:
            endpoint = f"https://api.pipedrive.com/v1/deals/{params['deal_id']}/products"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            params.pop('deal_id')
            response = requests.post(endpoint, headers=headers, json=params)
            if response.status_code in status:
                product_data = response.json()
                print(product_data)
                return product_data
            else:
                raise Exception(f"Failed. Response: {response.text}")
        else:
            raise Exception('Missing required parameters')
    except Exception as e:
        raise Exception(e)

