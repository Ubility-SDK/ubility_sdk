import json
import requests

def convertkit_create_tag(params,cred):
    """
    Create a tag.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - tag (dict): Tag information.
            - name (str): Name of the tag to be created. (required)

    :return: Information about the created tag.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'tag' in params and 'name' in params['tag']:
            base_url = "https://api.convertkit.com/v3/tags"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(base_url, json=params, headers=headers)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Failed to create a tag:{response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    
def convertkit_get_tags(params,cred):
    """
    Retrieve all tags from ConvertKit.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)

    :return: Information about all tags.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds:
            base_url = "https://api.convertkit.com/v3/tags"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }   
            response = requests.get(base_url, params=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get tags: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_add_tag_to_subscriber(params,cred):
    """
    Add a tag to a subscriber.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - tag_id (str): ID of the tag to add to the subscriber. (required)
        - email (str): Email address of the subscriber. (required)
        - first_name (str): First name of the subscriber. (optional)

    :return: Information about the tag added to the subscriber.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'tag_id' in params and 'email' in params:
            tag_id = params.pop('tag_id')
            base_url = f"https://api.convertkit.com/v3/tags/{tag_id}/subscribe"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(base_url, json=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to add tag to subscriber: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_list_subscriptions_to_tag(params,cred):
    """
    List subscriptions to a tag.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - tag_id (str): ID of the tag to list subscriptions for. (required)
        - subscriber_state (str): State of the subscribers to filter (active or cancelled). (optional)
        - page (int): Page number of the results being requested. (optional)

    :return: Information about subscriptions to the tag.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'tag_id' in params:
            tag_id = params.pop('tag_id')
            base_url = f"https://api.convertkit.com/v3/tags/{tag_id}/subscriptions"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(base_url, params=params, headers=headers)
            print(response.text)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list subscriptions to tag: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    

def convertkit_remove_tag_from_subscriber_by_email(params,cred):
    """
    Remove a tag from a subscriber by email.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - tag_id (str): ID of the tag to remove from the subscriber. (required)
        - email (str): Email address of the subscriber. (required)

    :return: Information about the removed tag from the subscriber.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'tag_id' in params and 'email' in params:
            tag_id = params.pop('tag_id')
            base_url = f"https://api.convertkit.com/v3/tags/{tag_id}/unsubscribe"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(base_url, json=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to remove tag from subscriber: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    
def convertkit_add_subscriber_to_sequence(params,cred):
    """
    Add a subscriber to a sequence.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - sequence_id (str): ID of the sequence to add the subscriber to. (required)
        - email (str): Email address of the subscriber. (required)
        - first_name (str): First name of the subscriber. (optional)

    :return: Information about the subscriber added to the sequence.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'sequence_id' in params and 'email' in params:
            sequence_id = params.pop('sequence_id')
            base_url = f"https://api.convertkit.com/v3/sequences/{sequence_id}/subscribe"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(base_url, json=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to add subscriber to sequence: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_list_sequences(params,cred):
    """
    List all sequences.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)

    :return: Information about all sequences.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds:
            base_url = "https://api.convertkit.com/v3/sequences"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(base_url, params=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list sequences: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def convertkit_list_subscriptions_to_sequence(params,cred):
    """
    List subscriptions to a sequence.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - sequence_id (str): ID of the sequence to list subscriptions for. (required)
        - subscriber_state (str): State of the subscribers to filter (active or cancelled). (optional)
        - page (int): Page number of the results being requested. (optional)

    :return: Information about subscriptions to the sequence.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'sequence_id' in params:
            sequence_id = params.pop('sequence_id')
            base_url = f"https://api.convertkit.com/v3/sequences/{sequence_id}/subscriptions"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(base_url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list subscriptions to sequence: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_add_subscriber_to_form(params,cred):
    """
    Add a subscriber to a form.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - form_id (str): ID of the form to add the subscriber to. (required)
        - email (str): Email address of the subscriber. (required)
        - first_name (str): First name of the subscriber. (optional)

    :return: Information about the subscriber added to the form.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'form_id' in params and 'email' in params:
            form_id = params.pop('form_id')
            base_url = f"https://api.convertkit.com/v3/forms/{form_id}/subscribe"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(base_url, json=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to add subscriber to form: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_list_forms(params,cred):
    """
    List all forms.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)

    :return: Information about all forms.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds:
            base_url = "https://api.convertkit.com/v3/forms"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(base_url, params=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list forms: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_list_subscriptions_to_form(params,cred):
    """
    List subscriptions to a form.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - form_id (str): ID of the form to list subscriptions for. (required)
        - subscriber_state (str): State of the subscribers to filter (active or cancelled). (optional)
        - page (int): Page number of the results being requested. (optional)

    :return: Information about subscriptions to the form.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'form_id' in params:
            form_id = params.pop('form_id')
            base_url = f"https://api.convertkit.com/v3/forms/{form_id}/subscriptions"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(base_url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list subscriptions to form: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_create_custom_fields(params,cred):
    """
    Create custom fields.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - label (str): The label(s) of the custom field. (required)

    :return: Information about the created custom fields.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'label' in params:
            base_url = "https://api.convertkit.com/v3/custom_fields"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(base_url, json=params, headers=headers)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Failed to create custom fields: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def convertkit_list_custom_fields(params,cred):
    """
    List all custom fields.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)

    :return: Information about all custom fields.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds:
            base_url = "https://api.convertkit.com/v3/custom_fields"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(base_url, params=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to list custom fields: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def convertkit_delete_custom_field(params,cred):
    """
    Delete a custom field.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - id (int): The ID of the custom field to delete. (required)

    :return: Confirmation message about the deletion of the custom field.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'id' in params:
            field_id=params.pop("id")
            base_url = f"https://api.convertkit.com/v3/custom_fields/{field_id}"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.delete(base_url, json=params, headers=headers)
            if response.status_code == 204:
                return "Custom field successfully Deleted."
            else:
                raise Exception(f"Failed to destroy custom field: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def convertkit_update_custom_field(params,cred):
    """
    Update a custom field.

    :param dict params:
        - api_secret (str): Your ConvertKit API secret key. (required)
        - id (int): The ID of the custom field to update. (required)
        - label (str): The label of the custom field. (required)

    :return: Confirmation message about the update of the custom field.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'apiSecret' in creds and 'id' in params and 'label' in params:
            field_id=params.pop("id")
            base_url = f"https://api.convertkit.com/v3/custom_fields/{field_id}"
            params['api_secret'] = creds['apiSecret']
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.put(base_url, json=params, headers=headers)
            if response.status_code == 204:
                return "Custom field successfully updated."
            else:
                raise Exception(f"Failed to update custom field: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)