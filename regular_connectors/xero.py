import requests,json

SCOPES = [
    "offline_access",
    "openid",
    "profile",
    "accounting.settings",
    "accounting.contacts.read",
    "accounting.transactions.read",
    "accounting.transactions",
    "accounting.contacts",
    "email",
    "accounting.settings.read",
]

def xero_refresh_access_token(cred):
    try:
        credentials = json.loads(cred)
        refresh_token = credentials['refreshToken']
        client_id = credentials['clientID']
        client_secret = credentials['clientSecret']
        url = "https://identity.xero.com/connect/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            accessToken = token_info["access_token"]
            refreshToken = token_info["refresh_token"]
            return accessToken
        else:
            err_msg = [response.text, response.status_code]
            raise  Exception(err_msg)
    except requests.exceptions.RequestException as e:
        raise (e)
    except Exception as e:
        raise (e)


# ##############################################
# Contact Methods


def xero_get_contact(access_token,params):

    '''
    Retrieves informations about a specific Xero contact.
    
    :param str access_token: The Xero access token for authentication
    :param dict params: Dictionary contains parameters.
            
     - :tenant_id: (str,required) The ID of the organization that encompasses the specified contact.
     - :ContactID: (str,required) The ID of the Xero contact to be retrieved.
        
    Returns:
        dict: A dictionary contains informations about the specified Xero contact
    
    '''
    
    try:
        if "ContactID" and "tenant_id" in params:
            url = f"https://api.xero.com/api.xro/2.0/Contacts/{params['ContactID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Xero-tenant-id": params["tenant_id"],
            }
            api_response = requests.get(url=url, headers=headers)
            return api_response.json()
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def xero_get_many_contact(access_token, params):

    '''
        Retrieves a list of Xero contacts based on the provided parameters.
        
        :param str access_token: The xero access token for authentication.
        :param dict params: Dictionary contains parameters.
            
         - :tenant_id: (str,required) The ID of the organization that encompasses the contacts.
         - :includeArchived: (boolean, optional) Contacts with the status: 'ARCHIVED' will be included in the response.
         - :where: (str,optional) Filter contacts with a specified condition.
         - :order: (str,optional) Specify the order in which the retrieved contacts should be sorted based on a particular field. Example: "Name Asc".
        
        Returns
            dict: A dictionary contains informations about the list of Xero contacts that match the condition.
    
    '''
    
    try:
        if "tenant_id" in params:
            url = "https://api.xero.com/api.xro/2.0/Contacts"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Xero-tenant-id": params["tenant_id"],
            }
            query_params = {}
            keys_to_skip = ["tenant_id","orderBy",'sortOrder'] 
            #Check if the field to sort on is provided
            if "orderBy" in params: 
                order_value = params['orderBy'] #Get field name
                #check if the sorting order is provided
                if "sortOrder" in params: 
                    order_value += f" {params['sortOrder']}" #Concatenate the name of the field with the sorting order provided
                query_params['order'] = order_value #Set the final string as the value of the 'order' key
            for key, value in params.items():
                if key not in keys_to_skip:
                    query_params[key] = value
            api_response = requests.get(url=url, headers=headers, params=query_params)
            result = api_response.json()
            if "ErrorNumber" in result:
                err_msg = result['Message']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def xero_create_contact(access_token, params):

    '''
        Creates a contact with the specified properties passed in parameters.
        
        :param str access_token: The Xero access token for authentication
        :param dict params: Dictionary contains parameters 
            
         - :tenant_id: (str,required) The ID of the organization where the contact should be created.
         - :Name: (str,required) Full name of the contact to be created.
         - :AccountNumber: (str,optional) A user defined account number.
         - :BankAccountDetails: (str,optional) Bank account number of the contact.
         - :ContactNumber: (str,optional) Unique identifier number for the contact to be created.
         - :ContactStatus: (str,optional) Current status of the contact.
         - :DefaultCurrency: (str,optional) Default currency for raising invoices against contact.
         - :FirstName: (str,optional) First name of the contact person.
         - :LastName: (str,optional) Last name of the contact person.
         - :EmailAddress: (str,optional) Email address of the contact person.
         - :PurchasesDefaultAccountCode: (str, optional) 
         - :SalesDefaultAccountCode: (str,optional) 
         - :TaxNumber: (str,optional) The unique identification number associated with a contact for tax-related purposes.
         - :Addresses: (dict,optional) Dictionary contains address informations.
         
          - :AddressType: (str,required) Type of address.(STREET,PO BOX...).
          - :AddressLine1: (str,optional) The main part of the address.(building_nb ,st_name).
          - :AddressLine2: (str,optional) Additional details about the address.
          - :City: (str,optional) Address city.
          - :Region: (str,optional) Address region.
          - :PostalCode: (str,optional) Address Postal Code.
          - :Country: (str,optional) Address country.
            
         - :Phones: (dict,optional) Dictionary contains phone informations.
         
          - :PhoneType: (str,required) The type of the phone.(Mobile,Fax...).
          - :PhoneNumber: (str,optional) The  Number.
          - :PhoneAreaCode: (str,optional) The  area code.
          - :PhoneCountryCode: (str,optional) The  country code.

        Returns:
          dict: A dictionary contains informations about the created contact.
    
    '''
    
    try:
        if "tenant_id" and "Name" in params:
            url = "https://api.xero.com/api.xro/2.0/Contacts"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Xero-tenant-id": params["tenant_id"],
                "Content-type": "application/json",
            }
            data = {}
            key_to_skip = ["tenant_id"]
            for key, value in params.items():
                if key in key_to_skip:
                    continue
                if value:
                    data[key] = value
            data = {"Contacts": [data]} #Wrap the data with the "Contacts" key as the Xero API expects to receive
            api_response = requests.post(url, headers=headers, json=data)
            result = api_response.json()
            if "ErrorNumber" in result:
                err_msg = result['Elements']
                for msg in err_msg:
                    error = msg['ValidationErrors']
                raise Exception(error)
            return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def xero_update_contact(access_token, params):
    
    
    '''
        Updates a contact with properties passed in parameters.
        
        :param str access_token: the Xero access token for authentication.
        :param dict params: Dictionary contains parameters.
        
         - :tenant_id: (str,required) The ID of the organization that contains the contact to be updated.
         - :ContactID: (ste,required) The ID of the contact to be updated.
         - :AccountNumber: (str,optional) A user defined account number.
         - :BankAccountDetails: (str,optional) Bank account number of the contact.
         - :ContactNumber: (str,optional) Unique identifier number for the contact to be updated.
         - :ContactStatus: (str,optional) Current status of the contact.
         - :DefaultCurrency: (str,optional) Default currency for raising invoices against contact.
         - :FirstName: (str,optional) New first name of the contact person.
         - :LastName: (str,optional) New last name of the contact person.
         - :EmailAddress: (str,optional) New email address of the contact person.
         - :PurchasesDefaultAccountCode: (str, optional) 
         - :SalesDefaultAccountCode: (str,optional) 
         - :TaxNumber: (str,optional) The unique identification number associated with a contact for tax-related purposes.
         - :Addresses: (dict,optional) Dictionary contains address informations.
         
          - :AddressType: (str,required) Type of address.(STREET,PO BOX...).
          - :AddressLine1: (str,optional) The main part of the address.(building_nb ,st_name).
          - :AddressLine2: (str,optional) Additional details about the address.
          - :City: (str,optional) Address city.
          - :Region: (str,optional) Address region.
          - :PostalCode: (str,optional) Address Postal Code.
          - :Country: (str,optional) Address country.
         - :Phones: (dict,optional) Dictionary contains phone informations.
         
          - :PhoneType: (str,required) The type of the phone.(Mobile,Fax...).
          - :PhoneNumber: (str,optional) The Number.
          - :PhoneAreaCode: (str,optional) The area code.
          - :PhoneCountryCode: (str,optional) The country code.

        Returns:
           dict: A dictionary contains new informations about the updated contact.
    
    '''

    try:
        if "ContactID" in params and "tenant_id" in params:
            url = f"https://api.xero.com/api.xro/2.0/Contacts/{params['ContactID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Xero-tenant-id": params["tenant_id"],
            }
            data = {}
            key_to_skip = ["tenant_id", "contactId"]
            for key, value in params.items():
                if key in key_to_skip:
                    continue
                if value:
                    data[key] = value

            data = {"Contacts": [data]} #Wrap the data with the "Contacts" key as the Xero API expects to receive
            api_response = requests.post(url, headers=headers, json=data)
            result = api_response.json()
            if "ErrorNumber" in result:
                err_msg = result['Message']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


# ##########################################################
# Invoice Operations


def xero_get_invoice(access_token, params):
    
    
    '''
        Retrieves informations about a specific invoice.
        
        :param str access_token: The Xero access token for authentication.
        :param dict params: Dictionary contains parameters.
        
         - :tenant_id: (str,required) The ID of the organization that contains the invoice to be retrieved.
         - :InvoiceID: (str,required) The ID of the invoice to be retrieved.
         
        Returns:
           dict: A dictionary contains information about the retrieved invoice.
    '''

    try:
        if "InvoiceID" in params:
            url = f"https://api.xero.com/api.xro/2.0/Invoices/{params['InvoiceID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Xero-Tenant-id": params["tenant_id"],
            }
            api_response = requests.get(url=url, headers=headers)
            return api_response.json()
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def xero_get_many_invoice(access_token, params):
    
    '''
        Retrieves a list of invoices based on the provided paramerters.
        
        :param str access_token: The Xero access token for authentication.
        :param dict params: Dictionary contains parameters.
        
         - :tenant_id: (str,required) The ID of the organization that contains the invoices to be retrieved.
         - :createdByMyApp: (boolean, optional) When set to true you'll only retrieve Invoices created by your app.
         - :where: (str,optional) Filter Invoices with a specified condition.
         - :order: (str,optional) Specify the order in which the retrieved invoices should be sorted based on a particular field. Example: "Date Desc".
         - :statuses: (str, optional) A comma-separated string to specify multiple statuses.
        
        Returns:
            dict: dict: A dictionary contains informations about the list of Xero Invoices that match the condition.
    '''

    try:
        if "tenant_id" in params:
            url = "https://api.xero.com/api.xro/2.0/Invoices"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Xero-tenant-id": params["tenant_id"],
            }
            query_params = {}
            keys_to_skip = ["tenant_id","orderBy",'sortOrder'] 
            #Check if the field to sort on is provided
            if "orderBy" in params: 
                order_value = params['orderBy'] #Get field name
                #check if the sorting order is provided
                if "sortOrder" in params: 
                    order_value += f" {params['sortOrder']}" #Concatenate the name of the field with the sorting order provided
                query_params['order'] = order_value #Set the final string as the value of the 'order' key
            for key, value in params.items():
                if key not in keys_to_skip:
                    query_params[key] = value

            api_response = requests.get(url=url, headers=headers, params=query_params)
            result = api_response.json()
            if "ErrorNumber" in result:
                err_msg = result['Message']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def xero_create_invoice(access_token, params):


    '''
        Creates an invoice with the specified properties passed in parameters.
        
        :param str access_token: The Xero access token for authentication
        :param dict params: Dictionary contains parameters.
        
         - :tenant_id: (str,required) The ID of the organization where the invoice should be created.
         - :Type: (str,required) Invoice type.
         - :ContactID: (str,required) The unique identifier of the contact associated with the invoice.
         - :BrandingThemeID: (str,optional) The branding Theme of the invoice.
         - :CurrencyCode: (str,optional) The currency that invoice has been raised in.
         - :CurrencyRate: (str,optional) The currency rate for a multicurrency invoice.
         - :Date: (str,optional) Date invoice was issued – YYYY-MM-DD.
         - :DueDate: (str,optional) Date invoice is due – YYYY-MM-DD.
         - :ExpectedPaymentDate: (str,optional) Shown on sales invoices when this has been set.
         - :PlannedPaymentDate: (str,optional) Shown on bills when this has been set.
         - :InvoiceNumber: (str,optional) An alpha numeric code identifying invoice.
         - :LineAmountType: (str,optional) Specifies how the line item amounts are treated.
         - :Reference: (str,optional) Additional reference number.
         - :SentToContact: (boolean,optiona) To indicate whether the invoice in the Xero app displays as "sent".
         - :Status: (str,optional) Invoice status.
         - :Url: (str,optional) URL link to a source document - shown as "Go to [appName]" in the Xero app.
         - :LineItems: (dict,optional) Dictionary contains items informations.
         
          - :Description: (str,optional) The description of the line item.
          - :Quantity: (number,optional) Line item Quantity.
          - :UnitAmount: (number,optional) Line item unit price.
          - :ItemCode: (str,required) User defined item code.
          - :AccountID: (str,required) Customer defined alpha numeric account code.
          - :TaxType: (str,required) Type of the tax.
          - :TaxAmount: (number,optional) The tax amount is auto calculated as a percentage of the line amount based on the tax rate.
          - :LineAmount: (number,optional)  LineAmount = Quantity * Unit Amount * ((100 – DiscountRate)/100).
          - :DiscountRate: (number,optional) Percentage discount being applied to a line item.
         
        Returns:
          dict: A dictionary contains informations about the created invoice.
    '''

    try:
        if "tenant_id" in params and "ContactID" in params['Contact'] and "Type" in params:
            url = "https://api.xero.com/api.xro/2.0/Invoices"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Xero-tenant-id": params["tenant_id"],
                "Content-type": "application/json",
            }
            data = {}
            key_to_skip = ["tenant_id"]
            # Check if the parameter Type is set to "Sales Invoice"
            if params["Type"] == "Sales Invoice":
            # If so, change it to the Xero API equivalent "ACCREC" (Accounts Receivable)
                params["Type"] = "ACCREC"

            # Check if the parameter Type is set to "Bill"
            if params["Type"] == "Bill":
            # If so, change it to the Xero API equivalent "ACCPAY" (Accounts Payable)
                params["Type"] = "ACCPAY"

            for key, value in params.items():
                if key in key_to_skip:
                    continue
                if value:
                    data[key] = value

            data = {"Invoices": [data]} #Wrap the data with the "Invoices" key as the Xero API expects to receive
            api_response = requests.post(url=url, headers=headers, json=data)
            result= api_response.json()
            if "ErrorNumber" and not "Message" in result:
                err_msg = result['Elements']
                error = ""
                for msg in err_msg:
                    error = msg['ValidationErrors']
                raise Exception(error)
            elif "ErrorNumber" and "Message" in result: #invalid contact id
                err_msg = result['Message']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def xero_update_invoice(access_token, params):
    
    ''' 
        Updates an invoice with the specified properties passed in parameters.
        
        :param str access_token: The Xero access token for authentication.
        :param dict params: Dictionary contains parameters.
        
         - :tenant_id: (str,required) The ID of the organization contains the invoice to be updated.
         - :InvoiceID: (str,required) The unique identifier of the invoice to be updated.
         - :ContactID: (str,optional) The unique identifier of the contact associated with the invoice.
         - :BrandingThemeID: (str,optional) The branding Theme of the invoice.
         - :CurrencyCode: (str,optional) The currency that invoice has been raised in.
         - :CurrencyRate: (str,optional) The currency rate for a multicurrency invoice.
         - :Date: (str,optional) Date invoice was issued – YYYY-MM-DD.
         - :DueDate: (str,optional) Date invoice is due – YYYY-MM-DD.
         - :ExpectedPaymentDate: (str,optional) Shown on sales invoices when this has been set.
         - :PlannedPaymentDate: (str,optional) Shown on bills when this has been set.
         - :InvoiceNumber: (str,optional) An alpha numeric code identifying invoice.
         - :LineAmountType: (str,optional) Specifies how the line item amounts are treated.
         - :Reference: (str,optional) Additional reference number.
         - :SentToContact: (boolean,optiona) To indicate whether the invoice in the Xero app displays as "sent".
         - :Status: (str,optional) Invoice status.
         - :Url: (str,optional) URL link to a source document - shown as "Go to [appName]" in the Xero app.
         - :LineItems: (dict,optional) Dictionary contains items informations.
           
          - :Description: (str,optional) The description of the line item.
          - :Quantity: (number,optional) Line item Quantity.
          - :UnitAmount: (number,optional) Line item unit price.
          - :ItemCode: (str,required) User defined item code.
          - :AccountID: (str,required) Customer defined alpha numeric account code.
          - :TaxType: (str,required) Type of the tax.
          - :TaxAmount: (number,optional) The tax amount is auto calculated as a percentage of the line amount based on the tax rate.
          - :LineAmount: (number,optional)  LineAmount = Quantity * Unit Amount * ((100 – DiscountRate)/100).
          - :DiscountRate: (number,optional) Percentage discount being applied to a line item.
            
        Returns:
          dict: A dictionary contains the new informations about the updated invoice.
    '''   

    try:
        if "InvoiceID" in params and "tenant_id" in params:
            url = f"https://api.xero.com/api.xro/2.0/Invoices/{params['InvoiceID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Xero-tenant-id": params["tenant_id"],
            }
            data = {}
            keys_to_skip = ["tenant_id", "InvoiceID"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    data[key] = value

            data = {"Invoices": [data]} #Wrap the data with the "Invoices" key as the Xero API expects to receive
            api_response = requests.post(url=url, headers=headers, json=data)
            result= api_response.json()
            if "ErrorNumber" and not "Message" in result: #an invalid value passed in param
                err_msg = result['Elements']
                for msg in err_msg:
                    error = msg['ValidationErrors']
                raise Exception(error)
            elif "ErrorNumber" and "Message" in result: #invalid invoice id
                err_msg = result['Message']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)

