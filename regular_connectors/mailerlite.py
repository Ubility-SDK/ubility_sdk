import requests,json

# Subscribers Operations

def mailerlite_get_subscriber(cred, params):
    
    '''
    Retrieves a subscriber based on the subscriber email passed in params.
    
    :param str api_key: Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the subscriber email.
    
     - :email: (str,required) The email address of the subscriber to retrieve.
     
    Returns:
        dict: A dictionary containing information about the retrieved subscriber.
    ''' 
    
    try:
        if "email" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            url = f"https://connect.mailerlite.com/api/subscribers/{params['email']}"
            headers = {
                "Content-Type":"application/json",
                "Accept":"application/json",
                "Authorization":f"Bearer {api_key}"
            }
            response = requests.get(url=url,headers=headers)
            if response.status_code == 200:
                result= response.json()
                if 'message' in result and result['message'] == 'Resource not found.': #invalid email
                    err_msg = result['message']+ " Please check your input."
                    raise Exception(err_msg)
                else:
                    return result
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    

# Get  subscriber id and status to use them in other functions.  
def mailerlite_get_subscriberId(cred, params):
    try:
        if "email" in params:
            credenials = json.loads(cred)
            api_key = credenials['apiKey']
            url = f"https://connect.mailerlite.com/api/subscribers/{params['email']}"
            headers = {
                "Content-Type":"application/json",
                "Accept":"application/json",
                "Authorization":f"Bearer {api_key}"
            }
            response = requests.get(url=url,headers=headers)
            if response.status_code == 200:
                result= response.json()
                if 'message' in result and result['message'] == 'Resource not found.': #invalid email
                    err_msg = result['message']+ " Please check your input."
                    raise Exception(err_msg)
                else:
                    return result['data']['id'],result['data']['status'] #Return only subscriber id and status 
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
   

   
def mailerlite_get_many_subscriber(cred, params):
    
    '''
    Retrieves a list of subscribers from Mailerlite based on specified criterias passed in params.
    
    :param str api_token:  Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the criterias to filter result based on it.
    
     - :limit: (integer,optional) The number of subscribers to retrieves. Default is 25.
     - :filter[status]: (str, optional) Subscribers status. Must be one of the possible statuses: active, unsubscribed or unconfirmed.
     
     
    Returns:
        dict: A dictionary containing the subscribers list that matches the criteria passed in params.
    '''
    
    try:
        credentials = json.loads(cred)
        api_key = credentials['apiKey']
        url=  "https://connect.mailerlite.com/api/subscribers"
        headers = {
            "Authorization":f"Bearer {api_key}",
            "Content-Type":"application/json",
            "Accept":"application/json",
        }
        body_data ={}
        for key,value in params.items():
            body_data[key] = value
        response = requests.get(url=url,headers=headers,params=body_data)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            raise Exception(response.json())
    except Exception as e:
        raise Exception(e)     
    
    
    
def mailerlite_create_subscriber(cred, params):
    
    '''
    Creates a new subscriber based on the properties passed in params.
    
    :param str api_token: Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the necessary properties to create the subscriber.
    
     - :email: (str,required) The email address of the new subscriber.
     - :fields: (obj, optional) Additional fields or properties for the new subscriber.
     
      - :name: (str, optional) Subscriber's first name.
      - :last_name: (str, optional) Subscriber's last name.
      - :city: (str, optional) Subscriber's city.
      - :country: (str, optional) Subscriber's country.
      - :company: (str, optional) Subscriber's company.
      - :phone: (str, optional) Subscriber's phone.
      - :z_i_p: (str, optional) Subscriber's ZIP code (Postal code).
    
     - :status: (str,optional) Subscriber status. Can be one of the following: active, unsubscribed or unconfirmed.
     - :ip_address: (str,optional) Subscriber IP.Must be a valid ip address.
     
    Returns:
        dict: A dictionary containing information about the created subscriber.
    '''
    
    try:
        if "email" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            url = "https://connect.mailerlite.com/api/subscribers"
            headers = {
                "Authorization":f"Bearer {api_key}",
                "Content-Type":"application/json",
                "Accept":"application/json"
            }
            body_data ={}
            for key,value in params.items():
                body_data[key] = value
            response = requests.post(url=url,headers=headers,json=body_data)
            result = response.json()
            if response.status_code == 201:
                return result
            elif response.status_code == 200: #User Email Already Exists
                raise Exception("User Email Already Exists! Please check your input") 
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    

def mailerlite_update_subscriber(cred, params):
    
    '''
    Updates an existing subscriber with the specified properties passed in params.
    
    :param str api_token: Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the new information for the subscriber to update.
    
     - :email: (str,required) The email of the subscriber to update.
     - :fields: (obj, optional) Contains the new properties for the subscriber to update.
     
      - :name: (str, optional) Subscriber's first name.
      - :last_name: (str, optional) Subscriber's last name.
      - :city: (str, optional) Subscriber's city.
      - :country: (str, optional) Subscriber's country.
      - :company: (str, optional) Subscriber's company.
      - :phone: (str, optional) Subscriber's phone.
      - :z_i_p: (str, optional) Subscriber's ZIP code (Postal code).
    
     - :status: (str,optional) Subscriber status. Can be one of the following: active, unsubscribed or unconfirmed.
     - :ip_address: (str,optional) Subscriber IP.Must be a valid ip address.
     
    Returns:
        dict: A dictionary containing the updated subscriber information.
    '''
    
    
    try:
        if "email" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            # Get the subscriber id based on the email provided by calling this method to pass it in the url.
            sub_id,_ = mailerlite_get_subscriberId(cred,params)
            url = f"https://connect.mailerlite.com/api/subscribers/{sub_id}"
            headers  ={
                "Authorization":f"Bearer {api_key}",
                "Content-Type":"application/json",
                "Accept":"application/json",
            }
            body_data = {}
            for key,value in params.items():
                if key != 'email':
                    body_data[key] = value
            response = requests.put(url=url,headers=headers,json=body_data)
            result = response.json()
            if response.status_code == 200:
                return result
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    

def mailerlite_upsert_subscriber(cred, params):
    
    '''
    Inserts a new subscriber or updates an existing one (based on the email provided) with the specified properties passed in params.
    
    :param str api_token: Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the information for the subscriber to insert or update.
    
     - :email: (str, required) The email of the subscriber to insert or update.
     - :fields: (obj, optional) Contains the properties for the subscriber to insert or update.
     
      - :name: (str, optional) Subscriber's first name.
      - :last_name: (str, optional) Subscriber's last name.
      - :city: (str, optional) Subscriber's city.
      - :country: (str, optional) Subscriber's country.
      - :company: (str, optional) Subscriber's company.
      - :phone: (str, optional) Subscriber's phone.
      - :z_i_p: (str, optional) Subscriber's ZIP code (Postal code).
    
     - :status: (str, optional) Subscriber's status. Can be one of the following: 'active', 'unsubscribed', or 'unconfirmed'.
     - :ip_address: (str, optional) Subscriber's IP. Must be a valid IP address.
     
    
    Returns:
        dict: A dictionary containing the response from the operation, which includes information about the subscriber that was either inserted or updated.
    
    '''
    
    try:
        if "email" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            url = "https://connect.mailerlite.com/api/subscribers"
            headers = {
                "Authorization":f"Bearer {api_key}",
                "Content-Type":"application/json",
                "Accept":"application/json"
            }
            body_data ={}
            for key,value in params.items():
                body_data[key] = value
            response = requests.post(url=url,headers=headers,json=body_data)
            result = response.json()
            if "errors" in result: #An error in the parameters
                err_msg = result['errors']['email']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    
    
    
def mailerlite_unsubscribe_subscriber(cred, params):
    
    '''
    Unsubscribes an existing subscriber from receiving future communications.
    
    :param str api_key: Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the information for the subscriber to unsubscribe.
    
     - :email: (str, required) The email of the subscriber to unsubscribe.
     
    Returns:
        dict: A dictionary containing the response from the Mailerlite API, usually includes the unsubscribed subscriber's information.
    '''
    
    try:
        if "email" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            # Get the subscriber id and status by calling this function
            # and check if the status is unsubscribed to raise exception
            sub_id,status = mailerlite_get_subscriberId(cred,params)
            if status == "unsubscribed":  
                raise Exception("This Subscriber is already unsubscribed")
            url = f"https://connect.mailerlite.com/api/subscribers/{sub_id}"
            headers  ={
                "Authorization":f"Bearer {api_key}",
                "Content-Type":"application/json",
                "Accept":"application/json",
            }
            body_data = {"status":"unsubscribed"}
            response = requests.put(url=url,headers=headers,json=body_data)
            result = response.json()
            if response.status_code == 200:
                return result
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    
    
##################################################################
# Group Operations

def mailerlite_add_subscriber_to_group(cred, params):
    
    '''
    Adds an existing subscriber to a given group.
    
    :param str api_key: Mailerlite ApiKey for authentication.
    :param dict params: A dictionary containing the subscriber email and the group_id.
    
     - :email: (str,required) Email of the subscriber to be added to the group.
     - :group_id: (str, required) The ID of the group to which the subscriber will be added.
    
    Returns: 
        dict: A dictionary containing the response from the MailerLite API, typically includes the subscriber's details and group assignment information.
     
    '''
    
    try:
        if "email" in params and "group_id" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            email = params['email']
            group_id = params['group_id']
            url = f"https://connect.mailerlite.com/api/subscribers/{email}/groups/{group_id}"
            headers = {
                "Authorization":f"Bearer {api_key}",
                "Content-Type":"application/json",
                "Accept":"application/json",
            }
            response = requests.post(url=url,headers=headers)
            result = response.json()
            if response.status_code == 200:
                return result
            elif response.status_code == 404: #Subscriber or group not found.
                if 'message' in result and result['message'] == "Resource not found.":
                    err_msg = result['message'] + " please check your inputs"
                    raise Exception(err_msg)
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    
    

def mailerlite_remove_subscriber_from_group(cred, params):
    
    '''
    Removes an existing subscriber from a specified group in MailerLite.
    
    :param str api_key: MailerLite ApiKey used for authentication.
    :param dict params: A dictionary containing the necessary information to remove the subscriber from the group.
    
     - :email: (str, required) The email address of the subscriber to be removed from the group.
        - :group_id: (str, required) The ID of the group from which the subscriber will be removed.
     
    Returns:
        response: The response from the MailerLite API upon successful removal.
    '''
    
    try:
        if "email" in params and "group_id" in params:
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            email = params['email']
            group_id = params['group_id']
            url = f"https://connect.mailerlite.com/api/subscribers/{email}/groups/{group_id}"
            headers = {
                "Authorization":f"Bearer {api_key}",
                "Content-Type":"application/json",
                "Accept":"application/json",
            }
            response = requests.delete(url=url,headers=headers)
            if response.status_code == 204:
                return {"message":"The Subscriber successfully removed from the group"}        
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    


##############################################################
# Campaign Operations


def mailerlite_create_draft_campaign(cred, params):
    
    '''
    Creates a draft campaign in MailerLite with the specified parameters.

    :param str api_key: MailerLite ApiKey for authentication.
    :param dict params: A dictionary containing the campaign details.
    
     - :name: (str,required) Campaign Name.
     - :type: (str,required) Campaign Type. Must be one of the following: regular, ab, resend.
     - :emails: (array,required) Must contain 1 email object item
     
      - :subject: (str,required) The email subject.
      - :from_name: (str, required) The sender's name.
      - :from: (str, required) The sender's email address, already verified on MailerLite.
      - :content: (str, optional) Content of the email.
      
     - :ab_settings: (obj,required if type is 'ab') All items of the array are required.
      - :test_type: (str,required if type is 'ab') Must be one of the following: subject, sender, sending_time.
      - :select_winner_by: (str,required if type is ab and test type is not sending_time) Has only two values: 'o' or 'c'
      - :after_time_unit: (str, required if type is ab and test type is not sending_time) Use 'h' for hours and 'd' for days.
      - :test_split: (int,required if type is 'ab') Must be between 5 and 25 for test types subject and sender and 100 for sending_time test type.
      - :b_value: (obj,required if type is ab and test type is not sending_time) Must contain the items for the b version of the campaign.
       
       - :subject: (str,required if test_type is 'subject') 
       - :from_name: (str,required if ab test type is 'sender')  
       - :from: (str,required if ab test type is sender) Must be a valid email that has been already verified.
       
       
    Returns:
        dict: A dictionary containing information about the created campaign. 

    '''
    
    try:
        if "name" and "type" and "emails" and "subject" and "from_name" and "from":
            url = "https://connect.mailerlite.com/api/campaigns"
            credentials = json.loads(cred)
            api_key = credentials['apiKey']
            headers ={
                        "Authorization":f"Bearer {api_key}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
            body_data = {}
            for key,value in params.items():
                body_data[key] = value
            response = requests.post(url=url,headers=headers,json=body_data)
            result = response.json()
            if response.status_code == 201:
                return result
            elif response.status_code == 422:
                if "errors" in result:
                    err_msg = result['errors']
                    raise Exception(err_msg)
            else:
                raise Exception(response.json()) 
        else:
            raise Exception("Missing Input Data")
        
    except Exception as e:
        raise Exception(e)

