import requests,logging,json,datetime

################## AUTHENTICATION ######################################################################################

    
def hubspot_refresh_access_token(credentials):
    try:
        url = "https://api.hubapi.com/oauth/v1/token"
        cred = json.loads(credentials)
        client_id = cred['clientID']
        client_secret = cred['clientSecret']
        refresh_token = cred['refreshToken']
        redirect_uri = cred['redirectUri']
        headers= {
            "Content-Type":"application/x-www-form-urlencoded",
            "Accept":"application/json",
        }
        token_data = {
            "grant_type":"refresh_token",
            "client_id":client_id,
            "client_secret":client_secret,
            "refresh_token":refresh_token,
            "redirect_uri":redirect_uri
        }
        response = requests.post(url=url,headers=headers,data=token_data)
        if response.status_code == 200:
            token_info = response.json()
            accessToken = token_info['access_token']
            return accessToken
        else:
            raise Exception(response.json())
    except requests.exceptions.RequestException as error:
        raise Exception(f"RequestException: {error}")
    except Exception as e:
        raise Exception(f"Unexpected error:{e}")
        
############# CONTACTS ####################################################################################
def hubspot_get_all_contacts(access_token,params):
    """
        Returns a specific number of contacts (if specified) with custom properties.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: filters the properties to be returned for each contact.
    
      :properties: (array of str) firstname,company,website,phone.
    :return: The list of contacts with the filtered properties and limit.
    :rtype: dict
    """
    try:
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        query_params = {}
        for key , value in params.items():
            query_params[key]= value
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        print(url)
        response = requests.get(url=url,headers=headers,params=query_params)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(result)
    except Exception as e:
        raise Exception(e)
def hubspot_get_contact(access_token,params):
    """
        Returns a contact of a specific id with custom properties (if specified).
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: filters the properties to be returned for the retrieved contact.
    
      :properties: (array of str) firstname,company,website,phone.
      :id: (str,required) The id of the contact to be retrieved
    :return: details about the retrieved contact,including the filtered properties
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/contacts/{params['id']}"
          query_params ={}
          for key ,value in params.items():
              if key != "id":
                  query_params[key] = value
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          contact = requests.get(url=url,headers=headers,params=query_params)
          if contact.status_code == 404:
                raise Exception("invalid input data")
          else:
                return contact.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
            
def hubspot_create_contact(access_token,params):
    """
        Creates a contact with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the contact.
    
      :properties: (dict) email(required),phone,website,company,firstname,lifecyclestage,
        lastname,industry,country,fax
    :return: details about the created contact
    :rtype: dict  
    """
    try:
        if 'email'in params['properties']:
            contact = {}
            for key, value in params.items():
                contact[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            url = "https://api.hubapi.com/crm/v3/objects/contacts"
            response = requests.post(url=url,json=contact,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("missing contact email")
    except Exception as e:
        raise Exception(e)   
    
def hubspot_update_contact(access_token,params):
    """
         Updates a contact with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains properties to be modified(or added) of the contact.
    
      :id: (str,required) the id of the contact to be modified.
      :properties: (dict) email,phone,website,company,firstname,lifecyclestage,
        lastname,industry,country,fax
    :return: details about the updated contact,including his id
    :rtype: dict  
    """
    try:
        if 'id' in params:
            contact = {}
            for key, value in params.items():
                if key != "id":
                    contact[key] = value
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                    }
            url = f"https://api.hubapi.com/crm/v3/objects/contacts/{params['id']}"
            response = requests.patch(url=url,json=contact,headers=headers)
            result=response.json()
            if response.status_code==200:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("Missing contact Id ")
    except Exception as e:
        raise Exception(e)  
    
def hubspot_delete_contact(access_token,params):
    """
         Deletes a contact of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the contact to be deleted.
    
      :id:  (str,required) the id of the contact.
    :return: a statement about the successful deletion of the contact
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/contacts/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"contact of id {params['id']} successfully deleted"  
    except Exception as e:
        raise Exception(e)
####################################### COMPANIES ######################################
def hubspot_create_company(access_token,params):
    """
        Creates a company with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the company.
    
      :properties: (dict)  domain (required),name,phone,lifecyclestage,
            annualrevenue,website,country,about_us,
    
    :return: details about the created company
    :rtype: dict  
    """
    try:
        if 'domain' in params['properties']:
            company = {}
            for key,value in params.items():
                company[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            url = "https://api.hubapi.com/crm/v3/objects/companies"
            response = requests.post(url=url,json=company,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(result)
        else:
            raise Exception("missing company domain")
    except Exception as e:
        raise Exception(e)   

def hubspot_update_company(access_token,params):
    """
         Updates a company with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains properties to be modified(or added) of the company.
    
      :id: (str,required) the id of the company to be modified.
      :properties: (dict) name,phone,lifecyclestage,annualrevenue,website,
                  country,about_us
    :return: details about the updated company,including its id
    :rtype: dict  
    """
    try:
        if 'id' in params:
            company = {}
            for key, value in params.items():
                if key != "id":     
                    if value:
                        company[key] = value
            headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {access_token}'
                    }
            url = f"https://api.hubapi.com/crm/v3/objects/companies/{params['id']}"
            response = requests.patch(url=url,json=company,headers=headers)
            result=response.json()
            if response.status_code==200:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("Missing company Id ")
    except Exception as e:
        raise Exception(e)  

def hubspot_get_company(access_token,params):
    """
        Returns a company of a specific id
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the id of the company to be returned.
    
      :properties: The id of the company to be retrieved.
      :id: (str,required) The id of the company to be retrieved.
    :return: details about the retrieved company
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/companies/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          response = requests.get(url, headers=headers)
          if response.status_code == 404:
                raise Exception("invalid input data")
          else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
    
def hubspot_get_all_companies(access_token,params):
  """
        Returns a specific number of companies (if specified) with custom properties.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: filters the properties to be returned for each company.
    
      :properties: (array of str) name,phone,lifecyclestage,annualrevenue,
                   website,country,about_us
      
    :return: The list of companies with the filtered properties and limit.
    :rtype: dict
  """
  try: 
        url = 'https://api.hubapi.com/crm/v3/objects/companies'
        query_params ={}
        for key ,value in params.items():
            query_params[key] = value 
        headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url, headers=headers,params=query_params)
        result=response.json()
        if response.status_code==200:
            return result
        else:
            raise Exception(result)
  except Exception as e:
        raise Exception(e)

def hubspot_delete_company(access_token,params):
    """
         Deletes a company of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the company to be deleted.
    
      :id:  (str,required) the id of the company.
    :return: a statement about the successful deletion of the company
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/companies/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"company of id {params['id']} successfully deleted"
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
##################### TICKETS ##############################################
def  hubspot_create_ticket(access_token,params):
    """
        Creates a ticket with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the ticket.
    
      :properties: (dict) hs_pipeline_stage (required),subject,hs_ticket_priority,
                hs_ticket_category,closed_date,createdate
         
    :return: details about the created ticket
    :rtype: dict  
    """
    try:   
          if 'hs_pipeline_stage' in params['properties']:
            ticket = {}
            keys_to_skip = ['ticketCreateTime','ticketCreateDate','ticketCloseTime','ticketCloseDate']
            for key, value in params.items():
                if key not in keys_to_skip:
                    ticket[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            if "ticketCreateTime" in params and  params['ticketCreateTime']:
                ticket_time = params['ticketCreateTime']
                # Split the time to two parts: min and sec
                time_parts = ticket_time.split(":") 
                date_obj=''
                # check existing of the meetingstartDate property
                if 'ticketCreateDate' in params and params['ticketCreateDate']:
                    ticket_date = params['ticketCreateDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(ticket_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    ticket_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(ticket_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_create = int(combined_date.timestamp() * 1000)
                ticket['properties']['createdate'] = unix_date_create
            url = "https://api.hubapi.com/crm/v3/objects/tickets"
            response = requests.post(url=url,json=ticket,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
          else:
              raise Exception("missing pipeline stage")
    
    except Exception as e:
        raise Exception(e)
        
def  hubspot_update_ticket(access_token,params):
    """
         Updates a ticket with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains properties to be modified(or added) of the ticket.
    
      :id: (str,required) the id of the ticket to be modified.
      :properties: (dict) subject,hs_ticket_priority,hs_ticket_category,
                   closed_date,createdate
    :return: details about the updated ticket,including its id
    :rtype: dict  
    """
    try:
          if 'id' in params:
            ticket = {}
            keys_to_skip = ['ticketCreateTime','ticketCreateDate','ticketCloseTime','ticketCloseDate',"id"]
            for key, value in params.items():
                if key not in keys_to_skip:
                    ticket[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            if "ticketCreateTime" in params and  params['ticketCreateTime']:
                ticket_time = params['ticketCreateTime']
                # Split the time to two parts: min and sec
                time_parts = ticket_time.split(":") 
                date_obj=''
                # check existing of the meetingstartDate property
                if 'ticketCreateDate' in params and params['ticketCreateDate']:
                    ticket_date = params['ticketCreateDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(ticket_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    ticket_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(ticket_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_create = int(combined_date.timestamp() * 1000)
                ticket['properties']['createdate'] = unix_date_create
            url = f"https://api.hubapi.com/crm/v3/objects/tickets/{params['id']}"
            response = requests.patch(url=url,json=ticket,headers=headers)
            result=response.json()
            if response.status_code==200:
               return result  
            else:
                raise Exception(result)
          else:
              raise Exception("missing ticket id")
    
    except Exception as e:
        raise Exception(e) 
     
def hubspot_get_ticket(access_token,params):
    """
        Returns a ticket of a specific id with custom properties (if specified).
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: filters the properties to be returned for the retrieved ticket.
    
      :properties: (array of str) subject,hs_ticket_priority,hs_ticket_category,
         closed_date,createdate.
      :id: (str,required) The id of the ticket to be retrieved
    :return: details about the retrieved ticket,including the filtered properties
    :rtype: dict  
    """
    try:
        if 'id' in params:
            url = f"https://api.hubapi.com/crm/v3/objects/tickets/{params['id']}"
            query_params = {}
            for key,value in params.items():
                if key != "id":
                    query_params[key]= value
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url=url, headers=headers,params=query_params)
            if response.status_code == 404:
                raise Exception("invalid input data")
            else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
    
def hubspot_get_all_tickets(access_token,params):
    """
            Returns a specific number of tickets (if specified) with custom properties.
        
        :param str access_token: retrieved from the hubspot app.   
        :param dict params: filters the properties to be returned for each ticket.
        
        :properties: (array of str) hs_pipeline_stage,hs_ticket_priority,subject
                    
        
        :return: The list of tickets with the filtered properties and limit.
        :rtype: dict
    """
    try: 
        url = "https://api.hubapi.com/crm/v3/objects/tickets"
        query_params = {}
        for key,value in params.items():
            query_params[key] = value
        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url=url, headers=headers,params=query_params)
        result=response.json()
        if response.status_code==200:
            return result  
        else:
            raise Exception(result)
    except Exception as e:
        raise Exception(e)
        
def hubspot_delete_ticket(access_token,params):
    """
         Deletes a ticket of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the ticket to be deleted.
    
      :id:  (str,required) the id of the ticket.
    :return: a statement about the successful deletion of the ticket
    :rtype: json  
    """
    try:
        if 'id' in params:
            url = f"https://api.hubapi.com/crm/v3/objects/tickets/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            requests.delete(url,headers=headers)
            return f"ticket of id {params['id']} successfully deleted"
        else:
            raise Exception("Missing ticket ID")
    except Exception as e:
        raise Exception(e)
 ############################### Deals ##################################################################################
def hubspot_create_deal(access_token,params):
    """
        Creates a deal with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the deal.
    
      :properties: (dict) dealname(required),closedate,createdate,amount,dealstage,
                dealtype
         
    :return: details about the created deal
    :rtype: dict  
    """
    try:
        if 'dealname' in params['properties']:
            keys_to_skip =['dealCreateTime','dealCreateDate','dealCloseTime','dealCloseDate']
            deal = {}
            for key, value in params.items():
                if key not in keys_to_skip:
                    deal[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            if "dealCreateTime" in params and  params['dealCreateTime']:
                deal_time = params['dealCreateTime']
                # Split the time to two parts: min and sec
                time_parts = deal_time.split(":") 
                date_obj=''
                # check existing of the meetingstartDate property
                if 'dealCreateDate' in params and params['dealCreateDate']:
                    deal_date = params['dealCreateDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    deal_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_create = int(combined_date.timestamp() * 1000)
                deal['properties']['createdate'] = unix_date_create
            if "dealCloseTime" in params and  params['dealCloseTime']:
                deal_time = params['dealCloseTime']
                # Split the time to two parts: min and sec
                time_parts = deal_time.split(":")
                date_obj=''
                # Check existing of the meetingEndtDate property
                if 'dealCloseDate' in params and params['dealCloseDate']:
                    deal_date = params['dealCloseDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    deal_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_end = int(combined_date.timestamp() * 1000)
                deal['properties']['closedate'] = unix_date_end
            url = "https://api.hubapi.com/crm/v3/objects/deals"
            response = requests.post(url=url,json=deal,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("missing deal name")
    except Exception as e:
        raise Exception(e)  

def hubspot_update_deal(access_token,params):
    """
         Updates a deal with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains properties to be modified(or added) of the deal.
    
      :id: (str,required) the id of the deal to be modified.
      :properties: (dict)  closedate,createdate,amount,dealstage,dealtype
    :return: details about the updated deal,including its id
    :rtype: dict  
    """
    try:
        if 'id' in params:
            deal = {}
            keys_to_skip=['id','dealCreateTime','dealCreateDate','dealCloseTime','dealCloseDate']
            for key, value in params.items():
                if key in keys_to_skip:
                        continue
                if value:
                    deal[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            if "dealCreateTime" in params and  params['dealCreateTime']:
                deal_time = params['dealCreateTime']
                # Split the time to two parts: min and sec
                time_parts = deal_time.split(":") 
                date_obj=''
                # check existing of the meetingstartDate property
                if 'dealCreateDate' in params and params['dealCreateDate']:
                    deal_date = params['dealCreateDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    deal_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_create = int(combined_date.timestamp() * 1000)
                deal['properties']['createdate'] = unix_date_create
            if "dealCloseTime" in params and  params['dealCloseTime']:
                deal_time = params['dealCloseTime']
                # Split the time to two parts: min and sec
                time_parts = deal_time.split(":")
                date_obj=''
                # Check existing of the meetingEndtDate property
                if 'dealCloseDate' in params and params['dealCloseDate']:
                    deal_date = params['dealCloseDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    deal_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(deal_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_end = int(combined_date.timestamp() * 1000)
                deal['properties']['closedate'] = unix_date_end
            url = f"https://api.hubapi.com/crm/v3/objects/deals/{params['id']}"
            response = requests.patch(url=url,json=deal,headers=headers)
            result=response.json()
            if response.status_code==200:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("Missing deal Id ")
    except Exception as e:
        raise Exception(e) 

def hubspot_get_deal(access_token,params):
    """
        Returns a deal of a specific id with custom properties (if specified).
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: filters the properties to be returned for the retrieved deal.
    
      :properties: (array of str) dealname,amount,createdate,closedate.
         
      :id: (str,required) The id of the deal to be retrieved
    :return: details about the retrieved deal,including the filtered properties
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/deals/{params['id']}"
          query_params = {}
          for key ,value in params.items():
              if key != "id":
                  query_params[key] = value
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          response = requests.get(url=url,headers=headers,params=query_params)
          if response.status_code == 404:
                raise Exception("invalid input data")
          else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)    

def hubspot_get_many_deals(access_token,params):
  """
        Returns a specific number of deals (if specified) with custom properties.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: filters the properties to be returned for each deal.
    
      :properties: (array of str) closedate,createdate,amount,dealstage,dealtype
                   
    :return: The list of deals with the filtered properties and limit.
    :rtype: dict
  """
  try: 
         url = "https://api.hubapi.com/crm/v3/objects/deals"
         query_params = {}
         for key, value in params.items():
             query_params[key] = value
         headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
         response = requests.get(url=url,headers=headers,params=query_params)
         result=response.json()
         if response.status_code==200:
               return result  
         else:
                raise Exception(result)
  except Exception as e:
        raise Exception(e)
            
def hubspot_delete_deal(access_token,params):
    """
         Deletes a deal of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the deal to be deleted.
    
      :id:  (str,required) the id of the deal.
    :return: a statement about the successful deletion of the deal
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/deals/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"deal of id {params['id']} successfully deleted"
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
##################### ENGAGEMENTS ########################################################################################
########## CALLS ################################
def hubspot_create_call(access_token,params):
    """
        Creates a call with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the call.
    
      :properties: (dict) hs_timestamp(required) hs_call_to_number,hs_call_duration,
      hs_call_status,hs_call_from_number,hs_call_title
         
    :return: details about the created deal
    :rtype: dict
      
    """
    try:
        if 'hs_timestamp' in params['properties']:
            call = {}
            for key, value in params.items():
                call[key] = value
            headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {access_token}'
                    }
            url = "https://api.hubapi.com/crm/v3/objects/calls"
            response = requests.post(url=url,json=call,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("missing call timestamp")
    except Exception as e:
        raise Exception(e)
      
def hubspot_get_call(access_token,params):
    """
        Returns a call of a specific id
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the id of the call to be returned.
    
      :properties: The id of the call to be retrieved.
      :id: (str,required) The id of the call to be retrieved.
    :return: details about the retrieved call
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/calls/{params['id']}"
          query_params = {}
          for key,value in params.items():
              if key != "id":
                  query_params[key] = value
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          response = requests.get(url=url,headers=headers,params=query_params)
          if response.status_code == 404:
                raise Exception("invalid input data")
          else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
    
def hubspot_get_many_calls(access_token,params):
  """
        Returns a specific number of calls.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the number of calls to be retrieved
    
      :limit: (str) the number of calls to be returned
                   
    :return: The list of calls with a limit.
    :rtype: dict
  """
  try:   
         url = "https://api.hubapi.com/crm/v3/objects/calls"
         query_params = {}
         for key, value in params.items():
             query_params[key] = value
        
         headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
         response = requests.get(url=url,headers=headers,params=query_params)
         result=response.json()
         if response.status_code==200:
               return result  
         else:
                raise Exception(result)
  except Exception as e:
        raise Exception(e)
        
def hubspot_delete_call(access_token,params):
    """
         Deletes a call of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the call to be deleted.
    
      :id:  (str,required) the id of the call.
    :return: a statement about the successful deletion of the call
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/calls/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"call of id {params['id']} successfully deleted"
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
########## Email  ####################################################################################
def hubspot_create_email(access_token,params):
    """
        Creates a email with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the email.
    
      :properties: (dict) hs_timestamp (required), hs_email_status,
             hs_email_subject,hs_email_text
         
    :return: details about the created deal
    :rtype: dict
      
    """
    try:
        if 'hs_timestamp' and "hs_email_direction" in params['properties']:
            email = {}
            for key, value in params.items():
                email[key] = value
                
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            url = "https://api.hubapi.com/crm/v3/objects/emails"
            response = requests.post(url=url,json=email,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("missing email timestamp")
    except Exception as e:
        raise Exception(e) 

    
def hubspot_get_email(access_token,params):
    """
        Returns a email of a specific id
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the id of the email to be returned.
    
      :properties: The id of the email to be retrieved.
      :id: (str,required) The id of the email to be retrieved.
    :return: details about the retrieved email
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/emails/{params['id']}"
          query_params ={}
          for key, value in params.items():
              if key != "id":
                  query_params[key] = value
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          response = requests.get(url=url,headers=headers,params=query_params)
          if response.status_code == 404:
                raise Exception("invalid input data")
          else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e) 
    
def hubspot_get_many_emails(access_token,params):
  """
        Returns a specific number of emails.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the number of emails to be retrieved
    
      :limit: (str) the number of emails to be returned
                   
    :return: The list of emails with a limit.
    :rtype: dict
  """
  try:   
         url = "https://api.hubapi.com/crm/v3/objects/emails"
         query_params = {}
         for key,value in params.items():
             query_params[key] = value
         headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
         response = requests.get(url=url, headers=headers,params=query_params)
         result=response.json()
         if response.status_code==200:
               return result  
         else:
                raise Exception(result)
  except Exception as e:
        raise Exception(e)
        
def hubspot_delete_email(access_token,params):
    """
         Deletes a email of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the email to be deleted.
    
      :id:  (str,required) the id of the email.
    :return: a statement about the successful deletion of the email
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/emails/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"email of id {params['id']} successfully deleted"
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)

################### TASKS #########################################################
def hubspot_create_task(access_token,params):
    """
        Creates a task with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the task.
    
      :properties: (dict) hs_timestamp (required), hs_task_subject,
                  hs_task_priority,hs_task_status,hs_task_type
         
    :return: details about the created deal
    :rtype: dict
      
    """
    try:
        if 'hs_timestamp' in params['properties']:
            task = {}
            for key, value in params.items():
                task[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            url = "https://api.hubapi.com/crm/v3/objects/tasks"
            response = requests.post(url=url,json=task,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("missing task timestamp")
    except Exception as e:
        raise Exception(e)
 
    
def hubspot_get_task(access_token,params):
    """
        Returns a task of a specific id
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the id of the task to be returned.
    
      :properties: The id of the task to be retrieved.
      :id: (str,required) The id of the task to be retrieved.
    :return: details about the retrieved task
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/tasks/{params['id']}"
          query_params = {}
          for key,value in params.items():
              if key !="id":
                  query_params[key] = value
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          response = requests.get(url=url,headers=headers,params=query_params)
          if response.status_code == 404:
                raise Exception("invalid input data")
          else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e) 
    
def hubspot_get_many_tasks(access_token,params):
  """
        Returns a specific number of tasks.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the number of tasks to be retrieved
    
      :limit: (str) the number of tasks to be returned
                   
    :return: The list of tasks with a limit.
    :rtype: dict
  """
  try:   
         url = "https://api.hubapi.com/crm/v3/objects/tasks"
         query_params = {}
         for key,value in params.items():
             query_params[key] = value
         headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
         response = requests.get(url=url, headers=headers,params=query_params)
         result=response.json()
         if response.status_code==200:
               return result  
         else:
                raise Exception(result)
  except Exception as e:
        raise Exception(e)
        
def hubspot_delete_task(access_token,params):
    """
         Deletes a task of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the task to be deleted.
    
      :id:  (str,required) the id of the task.
    :return: a statement about the successful deletion of the task
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/tasks/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"task of id {params['id']} successfully deleted"
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
    
################### MEETINGS #########################################################
def hubspot_create_meeting(access_token,params):
    """
        Creates a task with properties passed in the parameters
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains specific properties to be added for the task.
    
      :properties: (dict) hs_timestamp (required),  hs_meeting_external_URL,hs_meeting_start_time,
      hs_meeting_end_time,hs_meeting_location,hs_meeting_title
         
    :return: details about the created deal
    :rtype: dict
      
    """
    try:
        if 'hs_timestamp' in params['properties']:
            meeting = {}
            keys_to_skip= ['meetingStartTime','meetingStartDate','meetingEndTime','meetingEndDate']
            for key, value in params.items():
                if key not in keys_to_skip:
                    meeting[key] = value
            headers = {
                        'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}'
                        }
            if "meetingStartTime" in params and  params['meetingStartTime']:
                meeting_time = params['meetingStartTime']
                # Split the time to two parts: min and sec
                time_parts = meeting_time.split(":") 
                date_obj=''
                # check existing of the meetingstartDate property
                if 'meetingStartDate' in params and params['meetingStartDate']:
                    meeting_date = params['meetingStartDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(meeting_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    meeting_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(meeting_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_start = int(combined_date.timestamp() * 1000)
                meeting['properties']['hs_meeting_start_time'] = unix_date_start
            if "meetingEndTime" in params and  params['meetingEndTime']:
                meeting_time = params['meetingEndTime']
                # Split the time to two parts: min and sec
                time_parts = meeting_time.split(":")
                date_obj=''
                # Check existing of the meetingEndtDate property
                if 'meetingEndDate' in params and params['meetingEndDate']:
                    meeting_date = params['meetingEndDate']
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(meeting_date, "%Y-%m-%d").date()
                else: # Put the date as today's date if not specified
                    meeting_date = datetime.date.today()
                    # Convert string to date object
                    date_obj = datetime.datetime.strptime(meeting_date, "%Y-%m-%d").date()
                # Combine date and time into a datetime object
                combined_date = datetime.datetime(date_obj.year,date_obj.month,date_obj.day,int(time_parts[0]),int(time_parts[1]),tzinfo=datetime.timezone.utc)
                # Convert to Unix timestamp in milliseconds as Hubspot API expects
                unix_date_end = int(combined_date.timestamp() * 1000)
                meeting['properties']['hs_meeting_end_time'] = unix_date_end

            url = "https://api.hubapi.com/crm/v3/objects/meetings"
            response = requests.post(url=url,json=meeting,headers=headers)
            result=response.json()
            if response.status_code==201:
               return result  
            else:
                raise Exception(result)
        else:
            raise Exception("missing meeting timestamp")
    except Exception as e:
        raise Exception(e) 
    
def hubspot_get_meeting(access_token,params):
    """
        Returns a meeting of a specific id
    
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the id of the meeting to be returned.
    
      :properties: The id of the meeting to be retrieved.
      :id: (str,required) The id of the meeting to be retrieved.
    :return: details about the retrieved meeting
    :rtype: dict  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/meetings/{params['id']}"
          query_params = {}
          for key , value in params.items():
              if key != "id":
                  query_params[key] = value
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          response = requests.get(url=url,headers=headers,params=query_params)
          if response.status_code == 404:
                raise Exception("invalid input data")
          else:
                return response.json() 
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)   
    
def hubspot_get_many_meetings(access_token,params):
  """
        Returns a specific number of meetings.
     
    :param str access_token: retrieved from the hubspot app.   
    :param dict params: contains the number of meetings to be retrieved
    
      :limit: (str) the number of meetings to be returned
                   
    :return: The list of meetings with a limit.
    :rtype: dict
  """
  try:   
         url ="https://api.hubapi.com/crm/v3/objects/meetings"
         query_params = {}
         for key,value in params.items():
             query_params[key] = value
         headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
         response = requests.get(url=url, headers=headers,params=query_params)
         result=response.json()
         if response.status_code==200:
               return result  
         else:
                raise Exception(result)
  except Exception as e:
        raise Exception(e)
        
def hubspot_delete_meeting(access_token,params):
    """
         Deletes a meeting of a specific id
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the id of the meeting to be deleted.
    
      :id:  (str,required) the id of the meeting.
    :return: a statement about the successful deletion of the meeting
    :rtype: json  
    """
    try:
        if 'id' in params:
          url = f"https://api.hubapi.com/crm/v3/objects/meetings/{params['id']}"
          headers = {
           'Content-Type': 'application/json',
           'Authorization': f'Bearer {access_token}'
          }
          requests.delete(url,headers=headers)
          return f"meeting of id {params['id']} successfully deleted"
        else:
            raise Exception("missing input data")
    except Exception as e:
        raise Exception(e)
################# CONTACT LIST ######################################################################################## 
def hubspot_add_to_list(access_token,params):
    """
         Adds an array of contacts to a specific list
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the ids of the contacts and list to which they will be added.
    
      :record:  (arr of str,required) The ids of the contacts to be added.
      :list:  (arr of str,required) The id of the list to be added to.
    :return: the ids of the contacts that were added to the list
    :rtype: arr  
    """
    try:
        if 'record' in params:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            url = f"https://api.hubapi.com/crm/v3/lists/{params['list_id']}/memberships/add"
            response = requests.put(url=url,json=params['record'],headers=headers)
            result=response.json()
            if response.status_code==200:
             return result  
            else:
             raise Exception(result)
        else:
            raise Exception("missing record id")
    except Exception as e:
        raise Exception(e)
    
def hubspot_remove_from_list(access_token,params):
    """
         Removes an array of contacts from a specific list
     
    :param str access_token: retrieved from the hubspot app.
    :param dict params: contains the ids of the contacts and list from which they will be removed.
    
      :record:  (arr of str,required) The ids of the contacts to be removed.
      :list:  (arr of str,required) The id of the list to be removed from.
    :return: the ids of the contacts that were removed
    :rtype: arr  
    """
    try:
        if 'record' in params:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            url = f"https://api.hubapi.com/crm/v3/lists/{params['list_id']}/memberships/remove"
            logging.warning(params['record'])
            response = requests.put(url=url,json=params['record'],headers=headers)
            result=response.json()
            if response.status_code==200:
             return result  
            else:
             raise Exception(result)
        else:
            raise Exception("missing record id")
    except Exception as e:
        raise Exception(e)

