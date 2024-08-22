import requests
import json

def trello_get_list(cred,params):
    """Get details of a Trello list.

        Retrieves details of a Trello list using the provided credentials and parameters.

        
        :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
        :param dict params: Dictionary containing parameters for the request.
         -'list_id' : (str,required) The ID of the list to retrieve.

        Returns:
            dict: A dictionary containing the details of the Trello list.
    """
    try:
        creds = json.loads(cred)
        if "list_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey'] 
            token = creds['token']  
            url = f"https://api.trello.com/1/lists/{params['list_id']}"
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'list_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.get(url, params=request_params)
            if response.status_code == 200:
                trello_list = response.json() 
                return trello_list
            else:
                raise Exception(f"Failed to retrieve the list: {response.text}")
        else:
            raise Exception("missing params")
    except Exception as e:
        raise Exception(e) 
    

def trello_get_many_lists(cred, params):
    """Get details of multiple Trello lists.

    Retrieves details of multiple Trello lists from a specified board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board containing the lists.

    Returns:
        list: A list of dictionaries, each containing the details of a Trello list.

    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey'] 
            token = creds['token'] 
            url = f"https://api.trello.com/1/boards/{params['board_id']}/lists"
            query_params = {
                'key': apiKey,
                'token': token
            }
            response = requests.get(url, params=query_params)           
            if response.status_code == 200:
                lists = response.json() 
                return lists
            else:
                raise Exception(f"Failed to get many lists: {response.text}")
        else:
            raise Exception("missing params")
    except Exception as e:
        raise Exception(e)
    
def trello_get_many_checklists(cred,params):
    """Get details of multiple Trello checklists.

    Retrieves details of multiple Trello checklists associated with a specified card 
    using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board containing the checklists.

    Returns:
        list: A list of dictionaries, each containing the details of a Trello checklist.
    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey'] 
            token = creds['token']             
            url = f"https://api.trello.com/1/boards/{params['board_id']}/checklists"
            params = {
                'key': apiKey,
                'token': token
            }
            response = requests.get(url, params=params)        
            if response.status_code == 200:
                checklists = response.json() 
                return checklists
            else:
                raise Exception(f"Failed to get many checklist: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)


def trello_update_list(cred,params):
    """Update a Trello list.

    Updates a Trello list using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'list_id' : (str, required) The ID of the list to update.

    Returns:
        dict: A dictionary containing the updated details of the Trello list.

    """
    try:
        creds = json.loads(cred)
        if "list_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/lists/{params['list_id']}"
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'list_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.put(url, params=request_params)
            if response.status_code == 200:
                trello_list = response.json() 
                return trello_list
            else:
                raise Exception(f"Failed to retrieve the list: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e) 
    
def trello_create_list(cred,params):
    """Create a new Trello list.

    Creates a new Trello list on a specified board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board on which to create the list.
                        - 'list_name' : (str, required) The name of the new list.

                        Additional Parameters (optional):
                        - 'pos' : (str) The position of the new list ('top', 'bottom', or a positive float).
                        - 'idListSource' : (str) The ID of the list to copy cards from into the new list.

    Returns:
        dict: A dictionary containing the details of the newly created Trello list.
    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "list_name" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = "https://api.trello.com/1/lists"
            query_params = {
                'name': params['list_name'],
                'idBoard': params['board_id'],
                'key': apiKey,
                'token': token
            }
            data= {}
            ignore = ["board_id","list_name"]
            for key, value in params.items():
                if key in ignore:
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.post(url, params=query_params)
            if response.status_code == 200:
                created_list = response.json() 
                return created_list
            else:
                raise Exception(f"Failed to create the list: {response.text}")
        else:
            raise Exception("Missing parameters")
    except Exception as e:
        raise Exception(e)
   
def trello_getCard_list(cred,params):
    """Get cards from a Trello list.

    Retrieves cards from a Trello list using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'list_id' : (str, required) The ID of the list from which to retrieve cards.

    Returns:
        list: A list of dictionaries, each containing the details of a Trello card.
    """
    try:
        creds = json.loads(cred)
        if "list_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/lists/{params['list_id']}/cards"
            query_params = {
                'key': apiKey,
                'token': token
            }
            headers = {
                'Accept': 'application/json'
            }
            response = requests.get(url, params=query_params, headers=headers)
            if response.status_code == 200:
                card_list = response.json() 
                return card_list
            else:
                raise Exception(f"Failed to get the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_archive_list(cred,params):
    """Archive a Trello list.

    Archives a Trello list using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'list_id' : (str, required) The ID of the list to archive.

    Returns:
        dict: A dictionary containing the details of the archived Trello list.
    """
    try:
        creds = json.loads(cred)
        if "list_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/lists/{params['list_id']}/closed"
            query_params = {
                'key': apiKey,  
                'token': token,  
                'value': "true",  
            }
            response = requests.put(url, params=query_params)
            if response.status_code == 200:
                archived = response.json() 
                return archived
            else:
                raise Exception(f"Failed to archive the list: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_unarchive_list(cred,params):
    """Unarchive a Trello list.

    Unarchives a Trello list using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'list_id' : (str, required) The ID of the list to archive.

    Returns:
        dict: A dictionary containing the details of the archived Trello list.
    """
    try:
        creds = json.loads(cred)
        if "list_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/lists/{params['list_id']}/closed"
            query_params = {
                'key': apiKey,  
                'token': token,  
                'value': "false"  
            }
            response = requests.put(url, params=query_params)
            if response.status_code == 200:
                archived = response.json() 
                return archived
            else:
                raise Exception(f"Failed to unarchive the list: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_get_checklist(cred,params):
    """Get details of a Trello checklist.

    Retrieves details of a Trello checklist using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'checklist_id' : (str, required) The ID of the checklist to retrieve.

    Returns:
        dict: A dictionary containing the details of the Trello checklist.
    """
    try:
        creds = json.loads(cred)
        if "checklist_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/checklists/{params['checklist_id']}"
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'checklist_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.get(url, params=request_params)
            if response.status_code == 200:
                trello_checklist = response.json() 
                return trello_checklist
            else:
                raise Exception(f"Failed to retrieve the checklist: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_get_checkitem_states(cred,params):
    """Get the completed checklists of a Trello card.

    Retrieves the the completed checklists of a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card to retrieve the completed checklists from.

    Returns:
        list: A list of dictionaries, each containing the state of a check item on the card.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/checkItemStates"
            query_params = {
                'key': apiKey,
                'token': token
            }
            response = requests.get(url, params=query_params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get checkitem: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_create_checklist(cred,params):
    """Create a new checklist on a Trello card.

    Creates a new checklist on a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card on which to create the checklist.

                        Additional Parameters (optional):
                        - 'name' : (str) The name of the new checklist.
                        - 'pos' : (str) The pos of the new checklist.
                        - 'idChecklistSource' : (str) The id of the Checklist Source of the new checklist.

    Returns:
        dict: A dictionary containing the details of the newly created checklist.
    """
    try:
        creds= json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = "https://api.trello.com/1/checklists"
            query_params = {
                'idCard': params['card_id'],
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'card_id':
                    continue
                if value:
                    data[key] = value

            query_params.update(data)
            response = requests.post(url, params=query_params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get create checklis: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_create_item_checklist(cred,params):
    """Create a checkitem item in a Trello checklist.

    Creates a new checkitem item in a Trello checklist using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'checklist_id' : (str, required) The ID of the checklist to which the item belongs.
                        - 'name' : (str, required) The name of the new checklist item.

                        Additional Parameters (optional):
                        - 'checked' : (bool) Whether the new checklist item is checked or not.

    Returns:
        dict: A dictionary containing the details of the newly created checklist item.
    """
    try:
        creds = json.loads(cred)
        if "checklist_id" in params and "name" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/checklists/{params['checklist_id']}/checkItems"
            query_params = {
                'name': params['name'],
                'key': apiKey,
                'token': token
            }
            data = {}
            ignore = ["checklist_id","name"]
            for key, value in params.items():
                if key in ignore:
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.post(url, params=query_params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get item checklist: {response.text}")
        else:
            raise Exception("missing required params")  
    except Exception as e:
        raise Exception(e)

def trello_get_checkitems_checklist(cred,params):
    """
    Get checklist items from a Trello checklist.

    Retrieves checklist items from a Trello checklist using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'checklist_id' : (str, required) The ID of the checklist from which to retrieve items.

    Returns:
        list: A list of dictionaries, each containing the details of a checklist item.
    """
    try:
        creds = json.loads(cred)
        if "checklist_id" in params and "apiKey" in creds and "token" in creds:
            apiKey = creds['apiKey']
            token = creds['token']
            url = f"https://api.trello.com/1/checklists/{params['checklist_id']}/checkItems"
            query_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'checklist_id':
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.get(url, params=query_params)
            if response.status_code == 200:
                trello_list = response.json() 
                return trello_list
            else:
                raise Exception(f"Failed to retrieve the checklist items {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_delete_checklist(cred,params):
    """Delete a Trello checklist.

    Deletes a Trello checklist using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'checklist_id' : (str, required) The ID of the checklist to delete.

    Returns:
        dict: A dictionary containing the result of the deletion.
    """
    try:
        creds = json.loads(cred)
        if "checklist_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey= creds['apiKey']
            url = f"https://api.trello.com/1/checklists/{params['checklist_id']}"
            query_params = {
                'key': apiKey,  
                'token': token  
            }
            response = requests.delete(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to delete the checklist: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_update_checklist(cred,params):
    """Update a Trello checklist.

    Updates a Trello checklist using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'checklist_id' : (str, required) The ID of the checklist to update.
                        - 'field' : (str, required) The field to update in the checklist.
                        - 'value' : (str, required) The new value for the specified field.

    Returns:
        dict: A dictionary containing the updated details of the Trello checklist.
    """
    try:
        creds = json.loads(cred)
        if "checklist_id" in params and "value" in params and "field" in params:
            token= creds['token']
            apiKey= creds['apiKey']
            url = f"https://api.trello.com/1/checklists/{params['checklist_id']}/{params['field']}"
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'checklist_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.put(url, params=request_params)
            if response.status_code == 200:
                trello_list = response.json() 
                return trello_list
            else:
                raise Exception(f"Failed to retrieve the list: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_delete_item_checklist(cred,params):
    """Delete a Trello checklist item.

    Deletes a Trello checklist item using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'checklist_id' : (str, required) The ID of the checklist to which the item belongs.
                        - 'checkitem_id' : (str, required) The ID of the checklist item to delete.

    Returns:
        dict: A dictionary containing the result of the deletion.
    """
    try:
        creds = json.loads(cred)
        if "checklist_id" in params and "checkitem_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey= creds['apiKey']
            url = f"https://api.trello.com/1/checklists/{params['checklist_id']}/checkItems/{params['checkitem_id']}"
            
            query_params = {
                'key': apiKey,  
                'token': token,  
            }
            response = requests.delete(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to delete the checklist item: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_create_card(cred,params):
    """Create a new Trello card.

    Creates a new Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'list_id' : (str, required) The ID of the list where the card will be created.

                        Additional Parameters (optional):
                        - 'name' : (str) The name of the new card.
                        - 'desc' : (str) The description of the new card.
                        - 'due' : (str) The due date of the new card (in ISO 8601 format).
                        - 'labels' : (str) Comma-separated list of label IDs to be attached to the new card.
                        - 'pos' : (str) The position of the new card ('top', 'bottom', or a positive float).
                        - 'idMembers' : (str) Comma-separated list of member IDs to be assigned to the new card.

    Returns:
        dict: A dictionary containing the details of the newly created card.
    """
    try:
        creds= json.loads(cred)
        if "list_id" in params and "apiKey" in creds and "token" in creds:
            list_id =params['list_id']
            token= creds['token']
            apiKey= creds['apiKey']
            url = "https://api.trello.com/1/cards"
            headers = {
            "Accept": "application/json"
            }
            query_params = {
            'idList': list_id,
            'key': apiKey,
            'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'list_id':
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.post(url,headers=headers, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to create the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_delete_card(cred,params):
    """Delete a Trello card.

    Deletes a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card to delete.

    Returns:
        dict: A dictionary containing the result of the deletion.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey= creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}"
            query_params = {
                'key': apiKey,  
                'token':token,  
            }
            response = requests.delete(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to delete the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_update_card(cred,params):
    """Update a Trello card.

    Updates a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card to update.

                        Additional Parameters (optional):
                        - 'name' : (str) The new name for the card.
                        - 'desc' : (str) The new description for the card.
                        - 'due' : (str) The new due date for the card (in ISO 8601 format).
                        - 'closed' : (bool) Whether the card should be archived (closed: true)
                        - 'subscribed' : (bool) Whether the member is should be subscribed to the card

    Returns:
        dict: A dictionary containing the updated details of the Trello card.
    """

    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}"
            headers = {
            "Accept": "application/json"
            }     
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'card_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.put(url,headers=headers, params=request_params)
            if response.status_code == 200:
                updated_card = response.json() 
                return updated_card
            else:
                raise Exception(f"Failed to update the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_get_card(cred,params):
    """Get details of a Trello card.

    Retrieves details of a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card to retrieve.

    Returns:
        dict: A dictionary containing the details of the Trello card.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}"
            headers = {
                "Accept": "application/json"
            }
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'card_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.get(url, headers=headers, params=request_params)
            if response.status_code == 200:
                trello_card = response.json()
                return trello_card
            else:
                raise Exception(f"Failed to retrieve the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    

def trello_create_card_comment(cred,params):
    """Create a comment on a Trello card.

    Creates a comment on a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card to add the comment to.
                        - 'comment' : (str, required) The text of the comment to create.

    Returns:
        dict: A dictionary containing the details of the created comment.

    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "comment" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/actions/comments"
            headers = {
            "Accept": "application/json"
            }
            query_params = {
            'text': params['comment'],
            'key': apiKey,
            'token': token
            }
            response = requests.post(url,headers=headers, params=query_params)
            if response.status_code == 200:
                trello_card = response.json()
                return trello_card
            else:
                raise Exception(f"Failed to create the comment on card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_update_card_comment(cred,params):
    """Update a comment on a Trello card.

    Updates a comment on a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card containing the comment.
                        - 'comment_id' : (str, required) The ID of the comment to update.
                        - 'comment_text' : (str, required) The new text for the comment.

    Returns:
        dict: A dictionary containing the updated comment details.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "comment_id" in params and "comment_text" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/actions/{params['comment_id']}/comments"
            request_params = {
                'text':params['comment_text'],
                'key': apiKey,
                'token': token
            }
            response = requests.put(url, params=request_params)
            if response.status_code == 200:
                updated_comment = response.json() 
                return updated_comment
            else:
                raise Exception(f"Failed to update comment: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_delete_card_comment(cred,params):
    """Delete a comment from a Trello card.

    Deletes a comment from a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'comment_id' : (str, required) The ID of the comment to delete.
                        - 'card_id' : (str, required) The ID of the card containing the comment.

    Returns:
        dict: A dictionary containing information about the deleted comment.

    """
    try:
        creds = json.loads(cred)
        if "idAction" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/actions/{params['idAction']}/comments"
            request_params = {
                'key': apiKey,
                'token': token
            }
            response = requests.delete(url, params=request_params)
            if response.status_code == 200:
                trello_comment_del = response.json() 
                return trello_comment_del
            else:
                raise Exception(f"Failed to delete comment: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_add_member_to_card(cred,params):
    """Add a member to a Trello card.

    Adds a member to a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id' : (str, required) The ID of the card to add the member to.
                        - 'value' : (str, required) The ID of the member to add.

    Returns:
        dict: A dictionary containing information about the added member.

    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "value" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/idMembers"
            query_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'card_id':
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.post(url, params=query_params)
            if response.status_code == 200:
                added_member = response.json() 
                return added_member
            else:
                raise Exception(f"Failed to add member: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e) 
    
def trello_get_board(cred,params):
    """Get details of a Trello board.

    Retrieves details of a Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board to retrieve.

    Returns:
        dict: A dictionary containing the details of the Trello board.

    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/boards/{params['board_id']}"
            headers = {
            "Accept": "application/json"
            }
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'board_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.get(url,headers=headers, params=request_params)
            if response.status_code == 200:
                trello_board = response.json() 
                return trello_board
            else:
                raise Exception(f"Failed to retrieve the board: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_get_many_boards(cred,params):
    """Get details of multiple boards associated with a member.

    Retrieves details of multiple Trello boards associated with a member using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'idMember' : (str, required) The ID of the member whose boards are to be retrieved.

    Returns:
        dict: A dictionary containing details of multiple Trello boards associated with the member.

    """
    try:
        creds = json.loads(cred)
        if "idMember" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/members/{params['idMember']}/boards"
            params = {
                'key': apiKey,
                'token': token
            }

            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                boards = response.json() 
                return boards
            else:
                raise Exception(f"Failed to get many board: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_update_board(cred,params):
    """Update a Trello board.

    Updates a Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board to update.
                        - Additional parameters: Parameters to update the board. These can include:
                            - 'name' : (str) The new name for the board.
                            - 'desc' : (str) The new description for the board.
                            - 'closed' : (bool) Whether the board should be closed or open.
                            - 'idOrganization' : (str) The id of the Workspace the board should be moved to
                            - 'subscribed' : (bool) Whether the current user should be subscribed to the board.

    Returns:
        dict: A dictionary containing the updated details of the Trello board.

    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/boards/{params['board_id']}"
            
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'board_id':
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.put(url, params=request_params)
            if response.status_code == 200:
                updated_board = response.json() 
                return updated_board
            else:
                raise Exception(f"Failed to update the board: {response.text}")
        else:
            raise Exception("missing required params")
            
    except Exception as e:
        raise Exception(e)

def trello_delete_board(cred,params):
    """Delete a Trello board.

    Deletes a Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board to delete.

    Returns:
        dict: A dictionary containing information about the deleted board.

    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/boards/{params['board_id']}"            
            query_params = {
                'key': apiKey,  
                'token': token
            }
            response = requests.delete(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to delete the board: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_create_board(cred,params):
    """Create a Trello board.

    Creates a new Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'name' : (str, required) The name of the new board.
                        - Additional parameters: Additional options for creating the board.
                                                 These can include:
                            - 'desc' : (str) The description of the new board.
                            - 'prefs_permissionLevel' : (str) The permission level for the board.
                            
    Returns:
        dict: A dictionary containing information about the created board.

    """
    try:
        creds = json.loads(cred)
        if "name" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = "https://api.trello.com/1/boards/"
            query_params = {
                'name': params['name'],
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'name':
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.post(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to create the board: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_board_member(cred,params):
    """Get members of a Trello board.

    Retrieves the members of a Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id' : (str, required) The ID of the board whose members to retrieve.

    Returns:
        dict: A dictionary containing information about the members of the board.
    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/boards/{params['board_id']}/members"
            query_params = {
                'key': apiKey,
                'token': token
            }
            response = requests.get(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to retrieve members the board: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_board_Addmember(cred,params):
    """Add a member to a Trello board.

    Adds a member to a Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id': (str, required) The ID of the board to which the member will be added.
                        - 'member_id': (str, required) The ID of the member to be added.
                        - 'type': (str, required) The type of the membership. Possible values: 'normal', 'admin', 'observer'.

    Returns:
        dict: A dictionary containing information about the added member.
    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "member_id" in params and "type" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/boards/{params['board_id']}/members/{params['member_id']}"
            query_params = {
                'type':params['type'],
                'key': apiKey,
                'token': token
            }
            data = {}
            ignore= ['board_id','member_id','type']
            for key, value in params.items():
                if key in ignore:
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            response = requests.put(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to add member to the board: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_close_board(cred,params):
    """Close a Trello board.

    Closes a Trello board using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'board_id': (str, required) The ID of the board to be closed.

    Returns:
        dict: A dictionary containing information about the updated board after closure.

    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/boards/{params['board_id']}?closed=true"
            request_params = {
                'key': apiKey,
                'token': token
            }
            response = requests.put(url, params=request_params)
            if response.status_code == 200:
                updated_board = response.json() 
                return updated_board
            else:
                raise Exception(f"Failed to close the board: {response.text}")
    except Exception as e:
        raise Exception(e)

def trello_get_attachment(cred,params):
    """Retrieve information about a Trello card attachment.

    Retrieves information about a Trello card attachment using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id': (str, required) The ID of the card containing the attachment.
                        - 'attachment_id': (str, required) The ID of the attachment to retrieve.

    Returns:
        dict: A dictionary containing information about the attachment.

    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "attachment_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/attachments/{params['attachment_id']}"
            headers = {
            "Accept": "application/json"
            }
            request_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            ignore = ["card_id","attachment_id"]
            for key, value in params.items():
                if key in ignore:
                    continue
                if value:
                    data[key] = value
            request_params.update(data)
            response = requests.get(url,headers=headers, params=request_params)
            if response.status_code == 200:
                trello_attach = response.json() 
                return trello_attach
            else:
                raise Exception(f"Failed to retrieve the attachment: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_getmany_attachment(cred,params):
    """Retrieve information about multiple attachments on a Trello card.

    Retrieves information about multiple attachments on a Trello card using the provided credentials and parameters.

    :param str cred: JSON string containing Trello API credentials, including 'apiKey' and 'token'.
    :param dict params: Dictionary containing parameters for the request.
                        - 'card_id': (str, required) The ID of the card containing the attachments.

    Returns:
        list: A list of dictionaries, each containing information about an attachment.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/attachments"
            headers = {
            "Accept": "application/json"
            }
            query_params = {
                'key': apiKey,
                'token': token
            }
            data = {}
            for key, value in params.items():
                if key == 'card_id':
                    continue
                if value:
                    data[key] = value

            query_params.update(data)
            response = requests.get(url,headers=headers, params=query_params)
            if response.status_code == 200:
                trello_attach = response.json() 
                return trello_attach
            else:
                raise Exception(f"Failed to retrieve the attachment: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def trello_delete_attachment(cred,params):
    """Delete an attachment from a Trello card.

    Deletes an attachment from a Trello card using the provided credentials and parameters.

    Args:
        cred (str): JSON string containing Trello API credentials, including 'apiKey' and 'token'.
        params (dict): Dictionary containing parameters for the request.
            - 'card_id' (str, required): The ID of the card containing the attachment.
            - 'attachment_id' (str, required): The ID of the attachment to be deleted.

    Returns:
        dict: A dictionary containing information about the deleted attachment.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "attachment_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/attachments/{params['attachment_id']}"   
            query_params = {
                'key': apiKey,  
                'token': token  
            }
            response = requests.delete(url, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to delete the attachment: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_create_attachment(cred,params):
    """Create an attachment for a Trello card.

    Creates an attachment for a Trello card using the provided credentials and parameters.

    Args:
        cred (str): JSON string containing Trello API credentials, including 'apiKey' and 'token'.
        params (dict): Dictionary containing parameters for the request.
            - 'card_id' (str, required): The ID of the card to attach the file or URL.
            - 'name' (str, required): The name of the attachment to be added.
            - 'type' (str, required): The type of attachment. Possible values: 'url' or 'file'.
            - 'value' (str, required): The URL or file path of the attachment to be added.

    Returns:
        dict: A dictionary containing information about the created attachment.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "type" in params and "value" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}/attachments"
            query_params = {
                'key': apiKey,
                'token': token
            }
            headers = {
            "Accept": "application/json"
            }
            data = {}
            ignore = ["card_id","type","value"]
            if params['type'] == "url":
                data['url']= params['value']
            if params['type'] == "file":
                data['file']= params['value']
            
            for key, value in params.items():
                if key in ignore:
                    continue
                if value:
                    data[key] = value
            query_params.update(data)
            
            response = requests.post(url,headers=headers, params=query_params)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Failed to create the attachment: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)


def trello_archive_card(cred,params):
    """Archive a Trello card.

    Archives a Trello card using the provided credentials and parameters.

    Args:
        cred (str): JSON string containing Trello API credentials, including 'apiKey' and 'token'.
        params (dict): Dictionary containing parameters for the request.
            - 'card_id' (str, required): The ID of the card to be archived.

    Returns:
        dict: A dictionary containing information about the archived card.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}"
            headers = {
                "Accept": "application/json"
            }
            request_params = {
                'key': apiKey,
                'token': token,
                'closed' :"true"
            }            
            response = requests.put(url, headers=headers, params=request_params) 
            if response.status_code == 200:
                updated_card = response.json() 
                return updated_card
            else:
                raise Exception(f"Failed to archive the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_unarchive_card(cred,params):
    """Unarchive a Trello card.

    Unarchives a previously archived Trello card using the provided credentials and parameters.

    Args:
        cred (str): JSON string containing Trello API credentials, including 'apiKey' and 'token'.
        params (dict): Dictionary containing parameters for the request.
            - 'card_id' (str, required): The ID of the card to be unarchived.

    Returns:
        dict: A dictionary containing information about the unarchived card.
    """
    try:
        creds = json.loads(cred)
        if "card_id" in params and "apiKey" in creds and "token" in creds:
            token= creds['token']
            apiKey = creds['apiKey']
            url = f"https://api.trello.com/1/cards/{params['card_id']}"
            headers = {
                "Accept": "application/json"
            }
            request_params = {
                'key': apiKey,
                'token': token,
                'closed' :"false"
            }            
            response = requests.put(url, headers=headers, params=request_params) 
            if response.status_code == 200:
                updated_card = response.json() 
                return updated_card
            else:
                raise Exception(f"Failed to archive the card: {response.text}")
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def trello_board_invite_member(cred,params):
    """Invite a member to a Trello board.

    Invites a member to a Trello board using the provided credentials and parameters.

    Args:
        params (dict): Dictionary containing parameters for the request.
            - 'board_id' (str, required): The ID of the board.
            - 'email' (str, required): The email address of the member to be invited.
            - 'fullName' (str, optional): The full name of the member to be invited.
        cred (str): JSON string containing Trello API credentials, including 'apiKey' and 'token'.

    Returns:
        dict: A dictionary containing information about the invited member.
    """
    try:
        creds = json.loads(cred)
        if "board_id" in params and "email" in params and "apiKey" in creds and "token" in creds:
            url = f"https://api.trello.com/1/boards/{params['board_id']}/members"
            token = creds['token']
            apiKey = creds['apiKey']
            email = params['email']
            data = {}
            if 'fullName' in params:
                data = {
                    'fullName':params['fullName']
                }
            query_params = {
                'email': email,
                'key': apiKey,
                'token': token
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.put(url, headers=headers, params=query_params, json=data)
            if response.status_code == 200:
                board_member = response.json()
                return board_member
            else:
                return {"error": f"Failed to invite member: {response.text}"}
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)