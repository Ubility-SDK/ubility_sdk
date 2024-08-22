import requests
import base64
import json 


def zendesk_create_ticket(params,cred):
    """
        Creates a ticket with properties passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    description: str (required)
          a brief description of the ticket , passed in the 'ticket' dictionary.
    ticket : dictionary  (optional)
        assignee_email,external_id,group_id,status,subject,priority,type,custom_fields,tags

    Returns
    -------
    json 
       details about the created ticket,including its id
    """
    try:
            creds=json.loads(cred)
            if 'description' in params['ticket']:
                ticket = {}
                for key, value in params.items():
                    ticket[key] = value
                email=creds['email']
                api_token=creds['apiToken']
                base_url=creds['baseUrl']
                auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
                url =f"https://{base_url}.zendesk.com/api/v2/tickets" 
                headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
                response = requests.post(url,headers=headers,data=json.dumps(ticket))
                if response.status_code == 201:
                    return response.json()
                else:
                    raise Exception(response.text)
            else:
                raise Exception("Missing input data")   
    except Exception as error:
        raise Exception(error)

def zendesk_get_ticket(params,cred):
    """
        Retrieves a ticket of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the ticket to be retrieved

    Returns
    -------
    json 
       details about the retrieved ticket
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
         email=creds['email']
         api_token=creds['apiToken']
         base_url=creds['baseUrl']
         auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
         url = f"https://{base_url}.zendesk.com/api/v2/tickets/{params['id']}" 
         headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json"
            }
         response = requests.get(url, headers=headers)
         if response.status_code == 200:
            return response.json()
         else:
             raise Exception(response.json())
        else:
         raise Exception("missing ticket id")
    except Exception as e:
        raise Exception(e)


def zendesk_get_all_tickets(params,cred):
    """
        Returns a specific number of contacts (if specified) with custom properties.
    Parameters
    ----------
    access_token : str (required)
        Retrieved from the hubspot app.
    properties : array of str
        filters the properties to be returned for each contact.
        firstname,company,website,phone

    Returns
    -------
    list
        The list of contacts with the filtered properties and limit.
    """
    try:
       creds=json.loads(cred)
       email=creds['email']
       api_token=creds['apiToken']
       base_url=creds['baseUrl']
       url = f'https://{base_url}.zendesk.com/api/v2/search?query=type:ticket'
       if params['status']:
            url += f'+status:{params["status"]}'
       if params['sort_by']:
            url += f'&sort_by:{params["sort_by"]}'
       if params['sort_order']:
            url += f'&sort_order:{params["sort_order"]}'
       
       auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
       
       headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            } 
       response = requests.get(url,headers=headers,params=params)
       if response.status_code == 200:
           return response.json()
       else:
           raise Exception(response.json())
    except Exception as e:
        raise Exception(e)

def zendesk_update_ticket(params,cred):
    """
        Updates a contact with properties passed in the parameters 
    Parameters
    ----------
    access_token : str (required)
        Retrieved from the hubspot app.
    id : str (required)
        passed in the parameters properties.
    properties : array of str (optional)
        email,phone,website,company,firstname,lifecyclestage,lastname,industry,country,fax

    Returns
    -------
    json 
       details about the updated contact,including his id
    """
    try:
        creds=json.loads(cred)
        if "ticket_id" in params:
            ticket_id=params['ticket_id']
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/tickets/{ticket_id}" 
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            ticket = {}
            keys_to_skip = ["ticket_id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                  ticket[key] = value
            response = requests.put(url,headers=headers,data=json.dumps(ticket))
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def zendesk_delete_ticket(params,cred):
    """
        Deletes a ticket of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the ticket to be deleted

    Returns
    -------
    json 
       details about the deleted ticket
    """
    
    try:
          creds=json.loads(cred)
          if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/tickets/{params['id']}" 
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            response=requests.delete(url,headers=headers)
            if response.status_code == 204:
                return f"ticket with Id {params['id']} deleted successfully"
            else:
                raise Exception(response.json())
          else:
            raise Exception("missing ticket id")
    except Exception as e:
        raise Exception(e)

def zendesk_recover_ticket(params,cred):
    
    """
        Recovers  a zendesk ticket of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the ticket to be recovered

    Returns
    -------
    json 
       details about the recovered ticket
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url=f"https://{base_url}.zendesk.com/api/v2/deleted_tickets/{params['id']}/restore"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            response=requests.put(url,headers=headers)
            if response.status_code == 200:
                return f"successfully recovered ticket"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing ticket id")
    except Exception as e:
        raise Exception(e)

def zendesk_create_user(params,cred):
    try:
        creds=json.loads(cred)
        if "name" in params["user"] and len(params["user"]["name"]) >= 1:
            new_user = {}
            for key, value in params.items():
                if value:
                  new_user[key] = value
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/users" 
            headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json"
             }
            response = requests.post(url, headers=headers, json=new_user)
            if response.status_code == 201:
             return response.json()
            else:
             raise Exception(response.json())
        else:
            raise Exception("Name must be at least one character long.")
    except Exception as e:
        raise Exception(e)

def zendesk_get_user(params,cred):
    """
        Retrieves a user of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the user to be retrieved

    Returns
    -------
    json 
       details about the retrieved user
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/users/{params['id']}" 
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.json())
        else:
            raise Exception("missing user id")
    except Exception as e:
        raise Exception(e)

def zendesk_get_all_users(params,cred):
    try:
        creds=json.loads(cred)
        email=creds['email']
        api_token=creds['apiToken']
        base_url=creds['baseUrl']
        url = f"https://{base_url}.zendesk.com/api/v2/users" 
        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        full_url = f"{url}?{query_string}"
        
        auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
        headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            } 
        response = requests.get(full_url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(e)

def zendesk_delete_user(params,cred):
    """
        Deletes a user of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the user to be deleted

    Returns
    -------
    json 
       details about the deleted user
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/users/{params['id']}" 
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                } 
            response=requests.delete(url,headers=headers)
            if response.status_code == 200 :
                return f"user with Id {params['id']} deleted successfully"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing user id ")
    except Exception as e:
        raise Exception(e)

def zendesk_update_user(params,cred):
  try:
        creds=json.loads(cred)
        if "id" in params:
            user_id=params['id']
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/users/{user_id}" 
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            updated= {}
            keys_to_skip = ["id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                  updated[key] = value  
            response = requests.put(url,headers=headers,data=json.dumps(updated))
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Error : Missing input data")
  except Exception as e:
        raise Exception(e)
  
def zendesk_get_user_org(params,cred):
    
    """
        Returns organization of  a user of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the user to whose organization will be returned

    Returns
    -------
    json 
       details about the deleted user
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            url = f"https://{base_url}.zendesk.com/api/v2/users/{params['id']}/organizations" 
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else: 
            raise Exception(" Error : missing user id")
    except Exception as e:
        raise Exception(e)

def zendesk_get_data_related_to_user(params,cred):
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            url = f"https://{base_url}.zendesk.com/api/v2/users/{params['id']}/related" 
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.json())
        else:
            raise Exception(" Error : missing user Id")
    except Exception as e:
        raise Exception(e)

def zendesk_search_users(params,cred):
    try:
        creds=json.loads(cred)
        email=creds['email']
        api_token=creds['apiToken']
        base_url=creds['baseUrl']
        auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
        headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
        url = f"https://{base_url}.zendesk.com/api/v2/users/search" 
        if "external_id" in params:
            external_id = params["external_id"]
            url += f"?external_id={external_id}"
        if "query" in params:
           query = params["query"]
           if "external_id" in params:
                 url += f"&query={query}"
           else:
                  url += f"?query={query}"
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(e)

def zendesk_get_organization(params,cred):
    """
        Retrieves a organization of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the organization to be retrieved

    Returns
    -------
    json 
       details about the retrieved organization
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            url = f"https://{base_url}.zendesk.com/api/v2/organizations/{params['id']}" 
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.json())
        else:
            raise Exception("Error : missing organization ID")
    except Exception as e:
        raise Exception(e)

def zendesk_get_all_organizations(cred):
    try:
        creds=json.loads(cred)
        email=creds['email']
        api_token=creds['apiToken']
        base_url=creds['baseUrl']
        auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
        headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
        url = f"https://{base_url}.zendesk.com/api/v2/organizations/" 
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(e)
    
def zendesk_create_org(params,cred):
    try:
            creds=json.loads(cred)
            if "name" in params['organization']:
             org = {}
             for key, value in params.items():
                 org[key] = value
             email=creds['email']
             api_token=creds['apiToken']
             base_url=creds['baseUrl']
             auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
             url = f"https://{base_url}.zendesk.com/api/v2/organizations/"  
             headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
             }
             response = requests.post(url,headers=headers,data=json.dumps(org))
             if response.status_code == 201:
                 return response.json()
             else:
                 raise Exception(response.json())
            else:
              raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def zendesk_update_org(params,cred):
  try:
        creds=json.loads(cred) 
        if "id" in params:
            org_id=params['id']
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            url = f"https://{base_url}.zendesk.com/api/v2/organizations/{org_id}" 
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            updated= {}
            keys_to_skip = ["id"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                  updated[key] = value     
            response = requests.put(url,headers=headers,data=json.dumps(updated))
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing input data")
  except Exception as e:
        raise Exception(e)
    
def zendesk_delete_org(params,cred):
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            url = f"https://{base_url}.zendesk.com/api/v2/organizations/{params['id']}" 
            response=requests.delete(url,headers=headers)
            if response.status_code == 204 :
                return f"organization with Id {params['id']} deleted successfully"
            else:
                raise Exception(response.json())
        else :
            raise Exception("Error : missing organization ID")
    except Exception as e:
        raise Exception(e)

def zendesk_get_data_related_to_org(params,cred):
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                    }
            url = f"https://{base_url}.zendesk.com/api/v2/organizations/{params['id']}/related" 
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Error : missing organization ID")
    except Exception as e:
        raise Exception(e)

def zendesk_count_organizations(cred):
    try:
        creds=json.loads(cred)
        email=creds['email']
        api_token=creds['apiToken']
        base_url=creds['baseUrl']
        auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
        headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }

        url = f"https://{base_url}.zendesk.com/api/v2/organizations/count" 
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(e)
    
def zendesk_get_ticket_field(params,cred):
    """
        Retrieves a ticket field of id passed in the parameters (dictionary)
    Parameters
    ----------
    api_token : str (required)
        auto-generated passwords in the Zendesk Admin Center.
    base_url : str (required)
        containing the subdomain of the user,(the address of your help center is a Zendesk subdomain),to be passed in the request url.
    email : str (required)
        the user's email.
    id : str  (required)
        the id of the ticket field to be retrieved

    Returns
    -------
    json 
       details about the retrieved ticket field
    """
    try:
        creds=json.loads(cred)
        if 'id' in params:
            email=creds['email']
            api_token=creds['apiToken']
            base_url=creds['baseUrl']
            auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
            headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            url = f"https://{base_url}.zendesk.com/api/v2/ticket_fields/{params['id']}" 
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Error : missing Ticket ID")
    except Exception as e:
        raise Exception(e)

def zendesk_get_all_ticket_fields(cred):
    try:
        creds=json.loads(cred)
        email=creds['email']
        api_token=creds['apiToken']
        base_url=creds['baseUrl']
        auth_header = f"Basic {base64.b64encode(f'{email}/token:{api_token}'.encode()).decode()}"
        headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
        url = f"https://{base_url}.zendesk.com/api/v2/ticket_fields/" 
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
         return response.json()
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    