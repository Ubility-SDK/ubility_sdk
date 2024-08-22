import requests
################## CONTACTS ###########################
def keap_get_all_contacts(access_token,params):
    """
          Returns a specific number of contacts (if specified) with custom properties.
       :param str access_token: Used for authentication purposes. 
       :param dict params:  filters the properties to be returned for the contacts ( email,order,given_name..).

       :return: The list of contacts with the filtered properties and limit.
       :rtype: dict
    """
    try:
        url = 'https://api.infusionsoft.com/crm/rest/v1/contacts?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url,headers=headers)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(response.json())
    except Exception as e:
        raise Exception(e)

def keap_get_contact(access_token,params):
    """
          Returns a specific contact with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params:  filters the id and properties to be returned for the contact 

           - :id: (str,REQUIRED) the id of the contact to be retrieved
           - :optional_properties: (arr of str) filtered properties to be returned for the contact ( email,order,given_name..).

       :return: Details about the retrieved contact.
       :rtype: dict
    """
    try:
        if 'id' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/contacts/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url=url,headers=headers)
            result=response.json()
     
            if response.status_code==200:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing contact Id")
    except Exception as e:
        raise Exception(e)
    

def keap_delete_contact(access_token,params):
    """
          Deletes a specific contact
       :param str access_token (REQUIRED): Used for authentication purposes. 
       :param dict params: contains the Id of the contact to be deleted

           - :id: (str,REQUIRED) the id of the contact to be deleted

       :return: Success / Failure of the deletion process
       :rtype: dict
    """
    try:
        if 'id' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/contacts/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.delete(url=url,headers=headers)
            if response.status_code==204:
                return {"message": f"Deleted contact with ID  : {params['id']}"}
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing contact Id")
    except Exception as e:
        raise Exception(e)
    

def keap_create_contact(access_token,params):
    """
          Creates a keap contact with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the contact

           
           - :email_addresses: (arr of obj,REQUIRED) contains  objects of emails of the created  contact (email and field("EMAIL1","EMAIL2","EMAIL3"))

           - :phone_numbers: (arr of obj,REQUIRED) contains  objects of phone numbers of the created  contact (number and field("PHONE1" "PHONE2" "PHONE3" "PHONE4" "PHONE5")
           - :addresses:   (arr of obj,REQUIRED) contains objects of addresses of the created contact
           - :website: (str) website of the created contact
           - :region: (str) region of the contact 
           - :job_title: (str) the contact's job title
           - :given_name: (str) the name of the contact 
           - :time_zone : (str) the timezone of the contact
       :return: Details about the created contact.
       :rtype: dict
    """
    try:
        required_params=['email_addresses','phone_numbers']
        if all(param in params for param in required_params):
            url = f"https://api.infusionsoft.com/crm/rest/v1/contacts"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            contact={}
            for key,value in params.items():
                    contact[key]=value

            response = requests.post(json=contact,url=url,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def keap_update_contact(access_token,params):
    """
          Updates a keap contact with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added (or modified ) to the contact
           
           - :contactId: (int) id of the contact to be updated
           - :email_addresses: (arr of obj) contains  objects of emails of the updated  contact (email and field("EMAIL1","EMAIL2","EMAIL3"))

           - :phone_numbers: (arr of obj) contains  objects of phone numbers of the updated  contact (number and field("PHONE1" "PHONE2" "PHONE3" "PHONE4" "PHONE5")
           - :addresses:   (arr of obj) contains objects of addresses of the updated contact
           - :website: (str) website of the updated contact
           - :region: (str) region of the contact 
           - :job_title: (str) the contact's job title
           - :given_name: (str) the name of the contact 
           - :time_zone: (str) the timezone of the contact
       :return: Details about the updated contact.
       :rtype: dict
    """
    try:
        if 'contactId' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/contacts/{params['contactId']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            contact={}
            for key,value in params.items():
                    if 'contactId' in key:
                         continue
                    contact[key]=value

            response = requests.patch(json=contact,url=url,headers=headers)
            result=response.json()
            if response.status_code==200:
                return result  
            else:
                raise Exception(response['message'])
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
############################ EMAILS ####################################################

def keap_get_all_emails(access_token,params):
    """
          Returns a specific number of emails (if specified) with custom properties.
       :param str access_token: Used for authentication purposes. 
       :param dict params:  filters the properties to be returned for the emails ( email,offset,contact_id..).

       :return: The list of emails with the filtered properties and limit.
       :rtype: dict
    """
    try:
        url = f"https://api.infusionsoft.com/crm/rest/v1/emails?" + '&'.join([f'{key}={value}' for key, value in params.items()])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url,headers=headers)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(response.json())
    except Exception as e:
        raise Exception(e)

def keap_create_email_record(access_token,params):
    """
          Creates a keap email record with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the email

           
           - :sent from address: (str,REQUIRED) source address of the email
           - :sent to address: (str,REQUIRED)  destination address of the email 
           - :sent_date: (string <date-time>,REQUIRED)  the date on which the email was sent
           - :received_date:   (string <date-time>,REQUIRED)  the date on which the email was received
           - :plain_content: (str) Base64 encoded text
           - :subject: (str) the email subject
           - :contact_id: (int) the id of the contact who sent the email
           - :html_content: (str) Base64 encoded HTML
           - :headers : (str) 
           - :opened_date : (string <date-time>) 
       :return: Details about the created email.
       :rtype: dict
    """
    try:
        required_params=['sent_from_address','sent_to_address']
        if all(param in params for param in required_params):
            url = f"https://api.infusionsoft.com/crm/rest/v1/emails"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            email={}
            for key,value in params.items():
                    email[key]=value

            response = requests.post(json=email,url=url,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def keap_send_email(access_token,params):
    """
         Send an Email to a list of Contacts
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the email

           
           - :subject: (str,REQUIRED) The subject line of the email
           - :user_id: (str,REQUIRED)  The infusionsoft user to send the email on behalf of
           - :contacts: (arr of int) An array of Contact Ids to receive the email
           - :address_field:   (str) Email field of each Contact record to address the email to, such as 'Email', 'EmailAddress2', 'EmailAddress3' 
                                                      or '_CustomFieldName', defaulting to the contact's primary email
           - :plain_content: (str) Base64 encoded text
           - :html_content: (str) The HTML-formatted content of the email, encoded in Base64
           - :attachments: (arr of Obj) Attachments to be sent with each copy of the email, maximum of 10 with size of 1MB each
       :return: Details about the sent email.
       :rtype: dict
    """
    try:
        required_params=['subject','user_id','contacts']
        if all(param in params for param in required_params):
            url = f"https://api.infusionsoft.com/crm/rest/v1/emails/queue"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            email={}
            for key,value in params.items():
                    email[key]=value
            response = requests.post(json=email,url=url,headers=headers)
            if response.status_code==202:
                return {"success": f"Email Sent to contacts of Ids : {params['contacts']}"}
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)

def keap_get_all_companies(access_token,params):
    """
          Retrieves a list of all companies
       :param str access_token: Used for authentication purposes. 
       :param dict params:  filters the properties to be returned for the emails ( email,offset,contact_id..).

           - :limit: (str) Sets a total of items to return
           - :optional_parameters: (str) Comma-delimited list of Company properties to include in the response. (Fields such as notes, fax_number and custom_fields aren't included, by default.)
           - :order: (str) 	Attribute to order items by, possible values : "id" "date_created" "name" "email"
           - :order_direction: (str) How to order the data,  possible values : "ASCENDING" , "DESCENDING"
           - :company_name: (str) Optional company name to query on
       :return: The list of emails with the filtered properties and limit.
       :rtype: dict
    """
    try:
        url = f"https://api.infusionsoft.com/crm/rest/v1/companies?" + '&'.join([f'{key}={value}' for key, value in params.items()])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url,headers=headers)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(response.json())
    except Exception as e:
        raise Exception(e)   

def keap_create_company(access_token,params):
    """
          Creates a new company as the authenticated user. NB: Company must contain at least the company name.
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the company
           
           - :company_name: (str,REQUIRED) the company's name
           - :email_address: (str)  the official email of the company
           - :fax_number: (dict)  the fax number of the company (contains fields : number and type)
           - :phone_number:   (str)  the phone number of the company
           - :website: (str) the company's website
           - :address: (dict) the company's address

       :return: Details about the created company.
       :rtype: dict
    """
    try:
        if 'company_name' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/companies"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            company={}
            for key,value in params.items():
                    company[key]=value

            response = requests.post(json=company,url=url,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
###########################  E-COMMERCE ORDERS ########################
def keap_get_all_orders(access_token,params):
    """
          Retrieves a list of all orders using the specified search criteria. Each order may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params:  filters the properties to be returned for the orders ( order,paid,contact_id..).

       :return: The list of orders with the filtered properties and limit.
       :rtype: dict
    """
    try:
        url = f"https://api.infusionsoft.com/crm/rest/v1/orders?" + '&'.join([f'{key}={value}' for key, value in params.items()])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url,headers=headers)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(response.json())
    except Exception as e:
        raise Exception(e)
    
def keap_get_order(access_token,params):
    """
         Retrieves a single order. The order may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params: contains the id of the order to be retrieved

       :return: details about the retrieved order
       :rtype: dict
    """
    try:
        if 'id' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/orders/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url=url,headers=headers)
            result=response.json()
            if response.status_code==200:
                return result  
            else:
                    raise Exception(response.json())
        else:
             raise Exception("missing order Id")
    except Exception as e:
        raise Exception(e)

def keap_delete_order(access_token,params):
    """
         Deletes a single order. The order may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params: contains the id of the order to be deleted

       :return: details about the deleted order
       :rtype: dict
    """
    try:
        if 'id' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/orders/{params['id']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.delete(url=url,headers=headers)
            # logging.warning(response.status_code)
            if response.status_code==204:
                return {"message": f"Deleted order with ID  : {params['id']}"}
            else:
                    raise Exception(response.json())
        else:
             raise Exception("missing order Id")
    except Exception as e:
        raise Exception(e)
    
def keap_create_order(access_token,params):
    """
          Creates a keap order record with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the order

           - :contact_id: (int,REQUIRED) 	integer <int64>
           - :order_date: (str <date-time>,REQUIRED)  	string <date-time>
           - :order_items: (arr of objects,REQUIRED) Array of objects (CreateOrderItem)
           - :order_title:   (str,REQUIRED)  the title of the order
           - :order_type: (str,REQUIRED) <date-time>
           - :promo_codes: (arr of str) Uses multiple strings as promo codes. The corresponding discount will be applied to the order.
           - :shipping_address: (dict) the address of the order 

       :return: Details about the created order.
       :rtype: dict
    """
    try:
        required_params=['contact_id','order_date','order_items','order_title','order_type']
        if all(param in params for param in required_params):
            url = f"https://api.infusionsoft.com/crm/rest/v1/orders"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            order={}
            for key,value in params.items():
                    order[key]=value

            response = requests.post(json=order,url=url,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
############# E-COMMERCE PRODUCT ###########################################################
def keap_get_all_products(access_token,params):
    """
         Retrieves a list of all products

       :param str access_token: Used for authentication purposes. 
       :param dict params:  filters the properties to be returned for the products ( active..).

       :return: The list of products with the filtered properties and limit.
       :rtype: dict
    """
    try:
        url = f"https://api.infusionsoft.com/crm/rest/v1/products?" + '&'.join([f'{key}={value}' for key, value in params.items()])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url,headers=headers)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(response.json())
    except Exception as e:
        raise Exception(e)

def keap_get_product(access_token,params):
    """
         Retrieves a single product. The product may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params: contains the id of the product to be retrieved

       :return: details about the retrieved product
       :rtype: dict
    """
    try:
        if 'productId' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/products/{params['productId']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url=url,headers=headers)
            result=response.json()
            if response.status_code==200:
                return result  
            else:
                    raise Exception(response.json())
        else:
             raise Exception("missing product Id")
    except Exception as e:
        raise Exception(e)
    
def keap_delete_product(access_token,params):
    """
         Retrieves a single product. The product may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params: contains the id of the product to be retrieved

       :return: details about the retrieved product
       :rtype: dict
    """
    try:
        if 'productId' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/products/{params['productId']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.delete(url=url,headers=headers)
            if response.status_code==204:
                return {"message": f"Deleted product with ID  : {params['productId']}"}
            else:
                    raise Exception(response.json())
        else:
             raise Exception("missing product Id")
    except Exception as e:
        raise Exception(e)
    
def keap_create_product(access_token,params):
    """
          Creates a keap product  with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the product

           - :product_name: (str,REQUIRED)  the name of the product
           - :active: (bool) possible values: True , False
           - :product_desc: (str) description of the product
           - :product_price:  (number <double>)  the price of the product
           - :sku: (str) stock keeping unit of the product
           - :subscription_only: (bool)  possible values: True , False
       :return: Details about the created product.
       :rtype: dict
    """
    try:
        required_params=['product_name']
        if all(param in params for param in required_params):
            url = f"https://api.infusionsoft.com/crm/rest/v1/products"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            product={}
            for key,value in params.items():
                    product[key]=value

            response = requests.post(json=product,url=url,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
############ CONTACT_NOTE #############################
def keap_create_note(access_token,params):
    """
          Creates a keap note  with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added to the note

           - :contact_id: (int,REQUIRED) integer <int64> , the contact to whom the note belongs
           - :body: (str) the body of the note 
           - :title: (str) description of the note
           - :type:  (str) possibe values : "Appointment" "Call" "Email" "Fax" "Letter" "Other"
           - :user_id: (int) integer <int64>
       :return: Details about the created note.
       :rtype: dict
    """
    try:
        required_params=['contact_id']
        if all(param in params for param in required_params):
            url = f"https://api.infusionsoft.com/crm/rest/v1/notes"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            note={}
            for key,value in params.items():
                    note[key]=value

            response = requests.post(json=note,url=url,headers=headers)
            result=response.json()
            if response.status_code==201:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def keap_update_note(access_token,params):
    """
          Updates a keap note  with custom properties (if specified)
       :param str access_token (required): Used for authentication purposes. 
       :param dict params: includes the properties to be added(or modified) to the note
          
           - :noteId:(str,REQUIRED) : the Id of the note to be modified
           - :contact_id: (int) integer <int64> , the contact to whom the note belongs
           - :body: (str) the body of the note 
           - :title: (str) description of the note
           - :type:  (str) possibe values : "Appointment" "Call" "Email" "Fax" "Letter" "Other"
           - :user_id: (int) integer <int64>
       :return: Details about the updated note.
       :rtype: dict
    """
    try:
        if 'noteId' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/notes/{params['noteId']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            note={}
            for key,value in params.items():
                    if 'noteId' in key:
                         continue
                    note[key]=value

            response = requests.patch(json=note,url=url,headers=headers)
            result=response.json()
            if response.status_code==200:
                return result  
            else:
                    raise Exception(response.json())
        else:
            raise Exception("missing required params")
    except Exception as e:
        raise Exception(e)
    
def keap_get_note(access_token,params):
    """
         Retrieves a single note. The note may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params: contains the id of the note to be retrieved

       :return: details about the retrieved note
       :rtype: dict
    """
    try:
        if 'noteId' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/notes/{params['noteId']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(url=url,headers=headers)
            result=response.json()
            if response.status_code==200:
                return result  
            else:
                    raise Exception(response.json())
        else:
             raise Exception("missing note Id")
    except Exception as e:
        raise Exception(e)
    
def keap_delete_note(access_token,params):
    """
         Retrieves a single note. The note may or may not have items.
       :param str access_token: Used for authentication purposes. 
       :param dict params: contains the id of the note to be retrieved

       :return: details about the retrieved note
       :rtype: dict
    """
    try:
        if 'noteId' in params:
            url = f"https://api.infusionsoft.com/crm/rest/v1/notes/{params['noteId']}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.delete(url=url,headers=headers)
            if response.status_code==204:
                return {"message": f"Deleted note with ID  : {params['noteId']}"}
            else:
                    raise Exception(response.json())
        else:
             raise Exception("missing note Id")
    except Exception as e:
        raise Exception(e)

def keap_get_all_notes(access_token,params):
    """
          Retrieves a list of all notes
       :param str access_token: Used for authentication purposes. 
       :param dict params:  filters the properties to be returned for the notes ( limit,user_id,contact_id..).

         - :contact_id: (int) integer <int64> Filter based on the contact id assigned to the note.
         - :user_id: (int) Filter based on the user id assigned to the note.
         - :limit: (int) Filter based on the user id assigned to the note.

       :return: The list of notes with the filtered properties and limit.
       :rtype: dict
    """
    try:
        url = f"https://api.infusionsoft.com/crm/rest/v1/notes?" + '&'.join([f'{key}={value}' for key, value in params.items()])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url=url,headers=headers)
        result=response.json()
        if response.status_code==200:
              return result  
        else:
                raise Exception(response.json())
    except Exception as e:
        raise Exception(e)