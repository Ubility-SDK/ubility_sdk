import requests, base64,json

SCOPES = [
    "com.intuit.quickbooks.accounting",
    "com.intuit.quickbooks.payment",
    "openid",
    "profile",
    "email",
    "phone",
    "address",
]


def quickbooks_refresh_access_token(cred):
    try:
        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        credentials = json.loads(cred)
        client_id = credentials['clientID']
        client_secret = credentials['clientSecret']
        refresh_token = credentials['refreshToken']
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": "Basic "
            + base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode(
                "utf-8"
            ),
        }
        token_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = requests.post(url=url, headers=token_headers, data=token_data)
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info["access_token"]
            return access_token
        else:
            err_msg = [response.text,response.status_code]
            raise Exception(err_msg)
    except requests.exceptions.RequestException as error:
        raise Exception(f"RequestException: {error}")
    except Exception as e:
        raise Exception(f"Unexpected error:{e}")


#######################################################################
# Create Operations


def quickbooks_create_bill(cred,access_token,params):
    
    """
    Creates a bill in QuickBooks online with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the bill details.
    
     - :VendorRef: (dict,required) Dictionary containing vendor information.
      - :name: (str,optional) Vendor Name.
      - :value: (str,required) Vendor ID.
        
     - :Line: (dict,required) Dictionary containing line item information.
      - :Description: (str,optional) Description of the line item.
      - :Amount: (Decimal,required) Amount of the line item.
      - :DetailType: (str,required) Specify the type of detail for the bill.Use "ItemBasedExpenseLineDetail" if providing line items, and "AccountBasedExpenseLineDetail" if providing account-based details.
      - :ItemBasedExpenseLineDetail: (dict,required) 
       - :ItemRef: (dict,required)
        - :name: (str,optional)  Item name.
        - :value: (str,required) Item ID.
      - :AccountBasedExpenseLineDetail: (dict,required)
      
        - :AccountRef: (dict,required) 
         - :name: (str,optional) Account Name.
         - :value: (str,required) Account ID.
            
      - :LineNum: (Decimal,optional) Position of the line in the collection of transaction lines.
            
     - :APAccountRef: (dict,optional) Account payable reference
      - :name: (str,optional) Account Name.
      - :value: (str,required) Account ID.
     - :Balance: (str,optional) The balance reflecting any payments made against the transaction.
     - :DueDate: (date,optional) Date when the payment of the transaction is due.
     - :SalesTermRef: (dict,optional) 
       - :name: (str,optional) Sales term name.
       - :value: (str,required) Sales term ID.
     - :TotalAmt: (Decimal,optional) Total amount of the transaction.
     - :TxnDate: (date,optional) Date when the transaction occurred.
        
    Returns:
        dict: A dictionary containing information about the created bill.
        
        
    """ 
    
    try:
        if "VendorRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox": #check the choosed environment to put the correct url
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/bill"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/bill"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response= api_response.json()
            if "Fault" in response: #an error occured
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else: 
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_creditMemo(cred,access_token,params):
    
    '''
    Create a credit memo with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contans the credit memo details.
    
     - :CustomerRef: (dict,required) Dictionary containing customer information.
      - :name: (str,optional) Customer name.
      - :value: (str,required) Customer ID.
        
     - :Line: (dict,required) Dictionary containing line item information.
      - :Description: (str,optional) Description of the line item.
      - :Amount: (Decimal,required) Amount of the line item.
      - :DetailType: (str,required) Type of the detail of the credit memo.
          Use SalesItemLineDetail.
      - :SalesItemLineDetail: (dict,required)
        - :ItemRef: (dict,required)
          - :name: (str,optional) Item name.
          - :value: (str,required) Item ID.
      - :LineNum: (Decimal,optional) Position of the line in the collection of transaction lines.
     - :Balance: (Decimal,optional) The balance reflecting any payments made against the transaction.
     - :SalesTermRef: (dict,optional) 
        - :name: (str,optional) Sales term name.
        - :value: (str,required) Sales term ID.
     - :TotalAmt: (Decimal,optional) Total amount of the transaction.
     - :TxnDate: (date,optional) Date when the transaction occurred.
     - :BillEmail: (dict,optional) Identifies the e-mail address where the credit-memo is sent. If EmailStatus=NeedToSend, BillEmailis a required input.
      - :Address: (str,required) An email address.
      
    Returns: 
        dict: A dictionary containing information about the created credit memo.
    '''
    
    try:
        if "CustomerRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/creditmemo"
            if env == "Production":
                url = (
                    f"https://quickbooks.api.intuit.com/v3/company/{realmId}/creditmemo"
                )
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_customer(cred,access_token,params):
    
    '''
    Create a customer with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the customer  details.
    
     - :DisplayName: (str,required) The name of the person as displayed.(Unique)
     - :Active: (boolean,optional) If true, this entity is currently enabled for use by QuickBooks.
     - :Balance: (Decimal,optional) Specifies the open balance amount or the amount unpaid by the customer.
     - :BalanceWithJob: (Decimal,optional) Cumulative open balance amount for the Customer (or Job) and all its sub-jobs.
     - :BillWithParent: (boolean,optional) If true, this Customer object is billed with its parent. 
     - :CompanyName: (str,optional) Customer company name.
     - :GivenName: (str,optional) Customer first name.
     - :FamilyName: (str,optional) Customer last name.
     - :FullyQualifiedName: (str,optional) Fully qualified name of the object.
     - :PreferredDeliveryMethod: (str,optional) Values are Print,Email or None.
     - :PrimaryEmailAddress: (str,optional) Primary email address.
     - :PrimaryPhone: (str,optional) Primary phone number.
     - :PrintOnCheckName: (str,optional) Name of the customer as printed on a check.
     - :Taxable: (boolean,optional) If true, transactions for this customer are taxable.
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
    Returns: 
        dict: A dictionary containing information about the created customer.
     
    '''
    
    try:
        if "DisplayName" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/customer"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/customer"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response: 
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_estimate(cred,access_token,params):
    
    '''
    Creates an estimate with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the estimate  details.
     
     - :CustomerRef: (dict,required) A dictionary containing customer information.
      - :name: (str,optional) Customer name.
      - :value: (str,required) Customer ID.
    
     - :Line: (dict,required) A dictionary containing line item information.
      - :Description: (str,optional) Line item description.
      - :Amount: (str,required) Line Item Amount.
      - :DetailType: (str, required) Type of the detail of the estimate. Use SalesItemLineDetail.
      - :SalesItemLineDetail: (dict,required)
       - :ItemRef: (dict,required) Reference to the line item.
        - :name: (str,optional) Item name.
        - :value: (str,required) Item ID.
       - :TaxCodeRef: (dict,required) Reference to the TaxCode for this item.
        - :name: (str,optional) TaxCode name.
        - :value: (str,required) TaxCode ID.
      - :LineNum: (Decimal,optional) Specifies the position of the line in the collection of transaction lines.
     - :ApplyTaxAfterDiscount: (boolean,optional) If false or null, calculate the sales tax first, and then apply the discount.
     - :BillEmail: (str,optional) Identifies the e-mail address where the estimate is sent.
     - :CustomerMemo: (dict,optional) A dictionary containing user-entered message to the customer.
      - :value: (str,required)  This message is visible to the end user on their transactions.
     - :DocNumber: (str,optinal) Reference number for the transaction.
     - :EmailStatus: (str,optional) Valid values: NotSet, NeedToSend, EmailSent.
     - :PrintStatus: (str,optional) Valid values: NotSet, NeedToPrint, PrintComplete.
     - :TotalAmt: (BigDecimal,optional) Indicates the total amount of the transaction.
     - :TxnDate: (Date,optinal) Date when the transaction occurred.
     - :TxnTaxCodeRef: (dict,optional) This data type provides information for taxes charged on the transaction as a whole.
      - :TotalTax: (Decimal,optional) Total tax calculated for the transaction.
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
     - :ShipAddr: (dict,optional) A dictionary containing shipping address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
    Returns:
       dict: A dictionary containing information about the created estimate.
    '''
    
    try:
        if "CustomerRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/estimate"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/estimate"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_expense(cred,access_token,params):
    
    '''
    Creates an expense with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the expense  details.
    
     - :PaymentType: (str,required) Type can be Cash, Check, or CreditCard.
     - :AccountRef: (dict,required) A dictionary containing the account reference.
      - :name: (str,optional) Account Name.
      - :value: (str,required) Account ID.
     - :Line: (dict,required) A dictionary containing line item information.
      - :Description: (str,optional) Line item description.
      - :Amount: (Decimal,required) Line item amount.
      - :LineNum: (Decimal,optional) Specifies the position of the line in the collection of transaction lines.
      - :DetailType: (str,required) Specify the type of detail for the expense. Use "ItemBasedExpenseLineDetail" if providing line items, and "AccountBasedExpenseLineDetail" if providing account-based details.
      - :ItemBasedExpenseLineDetail: (dict,required)
       - :ItemRef: (dict,required) A dictionary containing item reference.
        - :name: (str,optional) Item name.
        - :value: (str,required) Item ID.
       - :TaxCodeRef: (dict, optional) Reference to the TaxCode for this item.
        - :name: (str,optional) TaxCode name.
        - :value: (str,required) TaxCode ID.
      - :AccountBasedExpenseLineDetail: (dict,required) 
       - :AccountRef: (dict,required) A dictionary containing account reference.
        - :name: (str,optional) Account name.
        - :value: (str,required) Account ID.
       - :TaxCodeRef: (dict, optional) The TaxCode associated with the sales tax for the expense
        - :name: (str,optional) TaxCode name.
        - :value: (str,required) TaxCode ID.
     - :TxnDate: (Date,optional) The date entered by the user when this transaction occurred.
     - :TotalAmt: (BigDecimal,optional) The total amount of the transaction.
     - :DocNumber: (str,optional) Reference number for the transaction.
     
    Returns:
        dict: A dictionary containing information about the created expense.
       
    '''
    
    try:
        if "PaymentType" in params and "AccountRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/purchase"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/purchase"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_invoice(cred,access_token,params):
    
    '''
    Creates an invoice with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the invoice details.
    
     - :CustomerRef: (dict,required) A dictionary containing customer reference.
      - :name: (str,optional) Customer name.
      - :value: (str,required) Customer ID.
     
     - :Line: (dict,required) A dictionary containing line item information.
      - :Description: (str,optional) Line item description.
      - :Amount: (Decimal,required) Line item amount.
      - :DetailType: (str,required) Specify the type of detail for the invoice. Use SalesItemLineDetail.
      - :SalesItemLineDetail: (dict,required) 
       - :ItemRef: (dict,required) A dictionary containing item information.
        - :name: (str,optional) Item name.
        - :value: (str,required) Item ID.
       - :TaxCodeRef: (dict,optional) Reference to the TaxCode for the specified item.
        - :name: (str,optional) TaxCode name.
        - :value: (str,required) TaxCode value.
     - :Balance: (str,optional) The balance reflecting any payments made against the transaction.
     - :BillEmail: (str,optional) E-mail address to which the invoice will be sent.
     - :CustomerMemo: (dict,optional) A dictionary containing user-entered message to the customer.
      - :value: (str,required)  This message is visible to the end user on their transactions.
     - :DocNumber: (str,optinal) Reference number for the transaction.
     - :DueDate: (date,optional) Date when the payment of the transaction is due.
     - :EmailStatus: (str,optional) Valid values: NotSet, NeedToSend, EmailSent.
     - :PrintStatus: (str,optional) Valid values: NotSet, NeedToPrint, PrintComplete.
     
     - :TotalAmt: (Decimal,optional) Total amount of the transaction.
     - :TxnDate: (date,optional) Date when the transaction occurred.
     
     - :ShipAddr: (dict,optional) A dictionary containing shipping address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
      
    Returns:
        dict: A dictionary containing information about the created invoice.
     
    '''
    
    try:
        if "CustomerRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/invoice"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/invoice"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_journal_entry(cred,access_token,params):
    
    '''
    Creates a journal entry with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the journal entry details.
    
     - :Line: (dict,required) Individual line items of a transaction. There must be at least one pair of Journal Entry Line elements, representing a debit and a credit, called distribution lines.
      - :Description: (str,optional) Description of the line item.
      - :Amount: (Decimal,required) Line item amount.
      - :DetailType: (str,required)  Specify the type of detail for the journl entry. Use JournalEntryLineDetail.
      - :JournalEntryLineDetail: (dict,required) 
       - :PostingType: (str,required) Indicates whether this JournalEntry line is a debit or credit. Valid values: Credit, Debit.
       - :AccountRef: (dict,required) A dictionary containing account reference.
        - :name: (str,optional) Account name.
        - :value: (str,required) Account ID.
       - :Entity: (dict,conditionally required) When you use Accounts Receivable, you must choose a customer in the Name field. When you use Accounts Payable, you must choose a supplier/vendor in the Name field.
        - :Type: (str,optional) Valid values are Vendor, Employee, or Customer.
        - :EntityRef: (dict,required) A dictionary containing the entity reference.
         - :name: (str,optional) Entity name.
         - :value: (str,required) Entity ID.
    
     - :TxnDate: (Date,optional) The date entered by the user when this transaction occurred.
     - :DocNumber: (str, optional) Reference number for the transaction.
    
    Returns:
       dict: A dictionary containing information about the journal entry created.
    '''
    
    try:
        if "Line" in params and len(params["Line"]) > 1: 
            # it must have at least one set of two Line elements: one for debit and one for credit
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/journalentry"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/journalentry"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_payment(cred,access_token,params):
    
    '''
    Creates a payment with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the payment details.
    
     - :TotalAmt: (Decimal,required) Indicates the total amount of the transaction.
     - :CustomerRef: (dict,required) A dictionary containing customer reference.
      - :name: (str,optional) Customer name.
      - :value: (str,required) Customer ID.
     - :TxnDate: (Date,optional) The date entered by the user when this transaction occurred.
     
    Returns:
        dict: A dictionary containing information about the created payment.
        
    
    '''
    
    try:
        if "TotalAmt" in params and "CustomerRef":
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/payment"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/payment"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_productOrder(cred,access_token, params):
    
    '''
    Creates a product order with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the product order details.
    
     - :APAccountRef: (dict,required) Specifies to which AP account the bill is credited.
      - :name: (str,optional) Account name.
      - :value: (str,required) Account ID.
     - :VendorRef: (dict,required) Reference to the vendor for this transaction.
      - :name: (str,optional) Vendor Name.
      - :value: (str,required) Vendor ID.
     
     - :Line: (dict,required) Individual line items of a transaction. Valid Line types include: ItemBasedExpenseLine and AccountBasedExpenseLine.
      - :Description: (str,optional) Line item Description.
      - :DetailType: (str,required) Specify the type of the detait. Use "ItemBasedExpenseLineDetail" if providing line items, and "AccountBasedExpenseLineDetail" if providing account-based details.
      - :ItemBasedExpenseLineDetail: (dict,required) 
       - :ItemRef: (dict,required) A dictionary containing item reference.
        - :name: (str,optional) Item name.
        - :value: (str,required) Item ID.
      - :AccountBasedExpenseLineDetail: (str,required)
       - :AccountRef: (dict,required) A dictionary containing account reference.
        - :name: (str,optional) Account name.
        - :value: (str,required) Account ID.
      - :LineNum: (Decimal,optional) Position of the line in the collection of transaction lines.
     
     - :POStatus: (String,optional) Valid values are: Open and Closed.
     - :TxnDate: (Date,optional) Date when the transaction occurred.
     - :ShipAddr: (dict,optional) A dictionary containing shipping address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
     - :VendorAddr: (dict,optional) Address to which the payment should be sent.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
    Returns:
        dict: A dictionary containing the information about the product order created.
    '''
    
    try:
        if "APAccountRef" in params and "VendorRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/purchaseorder"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/purchaseorder"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_productOrService(cred,access_token, params):
    
    '''
    Creates an item with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the item details.
    
     - :Name: (str,required) Name of the item. This value must be unique.
     - :IncomeAccountRef: (dict,required) Reference to the posting account, Must be an account with account type of Sales of Product Income.
      - :name: (str,optional) Account name.
      - :value: (str,required) Account ID.
     
     - :ExpenseAccountRef: (dict,required) Reference to the expense account used to pay the vendor for this item. Must be an account with account type of Cost of Goods Sold.
      - :name: (str,optional) Account name.
      - :value: (str,required) Account ID.
     
     - :QtyOnHand: (Decimal,conditionally required) Current quantity of the Inventory items available for sale. Not used for Service or NonInventory type items.Required for Inventory type items.
     - :InvStartDate: (Date,optional) Date of opening balance for the inventory transaction. Required when creating an Item.Type=Inventory.
     
    Returns:
       dict: A dictionary containing information about the created item.
      
      
      
      
    '''
    
    try:
        if (
            "Name" in params
            and "IncomeAccountRef" in params
            and "ExpenseAccountRef" in params
        ):
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/item"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/item"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")

    except Exception as e:
        raise Exception(e)


def quickbooks_create_refundReceipt(cred,access_token,params):
    
    '''
    Creates a refund Receipt with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the refund receipt details.
    
    
     - :DepositToAccountRef: (dict,required): Accounts receivable asset account from which payment money is refunded. 
      - :name: (str,optional) Account Name.
      - :value: (str,required) Account ID.
     
     - :Line: (dict,required) A dictionary containing line item details.
      - :Description: (str,optional) Line item description.
      - :Amount: (Decimal, required) Line item amount.
      - :LineNum: (Decimal, optional) Position of the line in the collection of transaction lines.
      - :DetailType: (str,required)  Specify the type of detail for the refundReceipt. Use SalesItemLineDetail.
      - :SalesItemLineDetail: (dict,required)
       - :ItemRef: (dict,required) A dictionary containing line item information.
        - :name: (str,optional) Item name.
        - :value: (str,required) Item ID.
       - :TaxCodeRef: (dict,optional) A dictionary containing tax code reference.
        - :name: (str,optional) TaxCode name.
        - :value: (str,required) TaxCode ID.
     
     - :TxnDate: (Date,optional) The date entered by the user when this transaction occurred.
     - :CustomerMemo: (dict,optional) User-entered message to the customer.
      - :value: (str,required) this message is visible to end user on their transaction.
     - :CustomerRef: (dict,optional) A dictionary containing the customer Reference.
      - :name: (str,optional) Customer name.
      - :value: (str,required) Customer ID.
     - :DocNumber: (str,optional) Reference number for the transaction.
     
     
    Returns: 
        dict: A dictionary containing information about the created refund Receipt.
     
     
    '''
    
    try:
        if "DepositToAccountRef" in params and "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/refundreceipt"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/refundreceipt"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_salesReceipt(cred,access_token,params):
    
    '''
    Creates a Sales Receipt with the specified properites passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the Sales Receipt details.
    
     - :Line: (str,required) A dictionary containing line item information.
      - :Description: (str,optional) Description of the line item.
      - :DetailType: (str,required) Specify the type of the detail for the SalesReceipt. Use  SalesItemLineDetail.
      - :LineNum: (Decimal,optional) Position of the line in the collection of transaction lines.
      - :SalesItemLineDetail: (dict,required) 
       - :ItemRef: (dict,required) A dictionary containing item reference.
        - :name: (str,optional) Item Name.
        - :value: (str,required) Item value.
       - :TaxCodeRef: (dict,optional) Reference to the TaxCodefor this item.
        - :name: (str,required) TaxCode name.
        - :value: (str,required) TaxCode ID.
     - :PrintStatus: (str,optional) Valid values: NotSet, NeedToPrint, PrintComplete .
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
     - :ShipAddr: (dict,optional) A dictionary containing shipping address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
     - :TxnDate: (Date,optional) The date entered by the user when this transaction occurred.
     - :CustomerRef: (dict,required) A dictionary containing the customer reference.
      - :name: (str,optional) Customer name.
      - :value: (str,required) Customer ID.
     - :DepositToAccountRef: (dict,optional) Account to which payment money is deposited.
      - :name: (str,optional) Account name.
      - :value: (str,required) Account ID.
     - :CustomerMemo: (dict,optional)  User-entered message to the customer.
      - :value: (str,required) this message is visible to the end user on their transactions.
     - :PaymentMethodRef: (dict,optional) Reference to a PaymentMethod associated with this transaction.
      - :name: (str,optional) Method name.
      - :value: (str,required) Method ID.
      
    Returns: 
        dict: A dictionary containing information about the created Sales Receipt.
      
    
    ''' 
    
    try:
        if "Line" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/salesreceipt"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/salesreceipt"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_timeActivity(cred,access_token,params):
    
    
    '''
    Creates a time activity with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the time activity details.
    
     - :NameOf: (str,required) Enumeration of time activity types. Valid values: Vendor or Employee.
     - :Hours: (integer,Condtionally required) Hours and minutes worked. Required if StartTime and EndTime not specified.
     - :StartTime: (DateTime,Condtionally required) Time that work starts. Required if Hours and Minutes not specified.
     - :EndTime: (str,Condtionally required) Time that work ends. Required if Hours and Minutes not specified.
     - :VendorRef: (dict,Condtionally required) Specifies the employee whose time is being recorded. 
      - :name: (str,optional) Employee name.
      - :value: (str,required) Employee ID.
     - :VendorRef: (dict,Condtionally required) Specifies the vendor whose time is being recorded. 
      - :name: (str,optional) Vendor Name.
      - :value: (str,required) Vendor ID.
     - :BillableStatus: (str,Conditionally required) Valid values: Billable, NotBillable, HasBeenBilled.
     - :CustomerRef: (dict,Conditionally required)  Reference to a customer or job. Required if BillableStatus is set to Billable.
      - :name: (str,optional) Customer  Name.
      - :value: (str,required) Customer ID.
      
    Returns:
       dict: A dictionary containing information about the time activity created.
     
    '''
    
    try:
        if "NameOf" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/timeactivity"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/timeactivity"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_create_vendor(cred,access_token,params):
    
    '''
    Creates a vendor with the specified properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary contains the vendor details.
    
     - :DisplayName: (str,required) The display name of the vendor to create.
     - :GivenName: (str,optional) Given name or first name of a person. 
     - :FamilyName: (str,optional) Family name or the last name of the person.
     - :CompanyName: (str,optional) The name of the company associated with the person or organization.
     - :Vendor1099: (str,optional) A 1099 vendor is paid with regular checks, and taxes are not withheld on their behalf.
     - :PrintOnCheckName: (str,optional) Name of the vendor as printed on a check.
     - :PrimaryPhone: (dict,optional) Primary phone number.
      - :FreeFormNumber: (str,optional) Specifies the telephone number in free form.
     - :PrimaryEmailAddr: (dict,optional) 
      - :Address: (str,optional) An email address. The address format must follow the RFC 822 standard.
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
     - :AcctNum: (str,optional) Name or number of the account associated with this vendor.
     - :Active: (boolean,optional) If true, this object is currently enabled for use by QuickBooks.
     - :Balance: (str,optional) The balance reflecting any payments made against the transaction.
     
     
    Returns:
        dict: A dictionary containing information about the created vendor.
        
    '''
    
    try:
        if "DisplayName" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/vendor"

            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/vendor"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value

            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


############################################################
# Send Operations


def quickbooks_send_invoice(cred,access_token,params):
    
    '''
    Sends an invoice via email using QuickBooks API.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the invoice id and the email of the recipient.
     
        - :Email: (str,required) The email of the recipient of the invoice.
        - :InvoiceID: (str,required) The id of the invoice to be sent.
        
    Returns:
        dict: A dictionary containing information about the sent invoice.
    '''
    
    try:
        if "Email" in params and "InvoiceID" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/invoice/{params['InvoiceID']}/send?sendTo={params['Email']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/invoice/{params['InvoiceID']}/send?sendTo={params['Email']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/octet-stream",
            }
            api_response = requests.post(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_send_salesReceipt(cred,access_token,params):
    
    '''
    Sends a Sales Receipt via email using QuickBooks API.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the sales receipt id and the email of the recipient.
     
        - :Email: (str,required) The email of the recipient of the Sales Receipt.
        - :SalesReceiptID: (str,required) The id of the Sales Receipt to be sent.
        
    Returns:
        dict: A dictionary containing information about the sent SalesReceipt.
    '''
    
    try:
        if "salesReceiptID" in params and "Email" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/salesreceipt/{params['salesReceiptID']}/send?sendTo={params['Email']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/salesreceipt/{params['salesReceiptID']}/send?sendTo={params['Email']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/octet-stream",
            }
            api_response = requests.post(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


###########################################################
# Update Operations
# To update a customer using the QuickBooks API, it is necessary to retrieve the current SyncToken for that customer.
# The SyncToken ensures that updates are applied to the correct version of the object.
# This mechanism prevents conflicts by verifying that the update is being made to the latest version.
def quickbooks_get_customer_syncToken(cred,access_token,params):
    try:
        if "Id" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/customer/{params['Id']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/customer/{params['Id']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            api_response = requests.get(url=url, headers=headers)
            response = api_response.json()
            return response["Customer"]["SyncToken"] #Retrieve only customer synctoken
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_update_customer(cred,access_token,params):
    
    '''
    Updates the customer properties with the new properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the customer new properties to update it.
    
     - :Id: (str,required) ID of the customer to be updated.
     - :Active: (boolean,optional) If true, this entity is currently enabled for use by QuickBooks.
     - :Balance: (Decimal,optional) Specifies the open balance amount or the amount unpaid by the customer.
     - :BalanceWithJob: (Decimal,optional) Cumulative open balance amount for the Customer (or Job) and all its sub-jobs.
     - :BillWithParent: (boolean,optional) If true, this Customer object is billed with its parent. 
     - :CompanyName: (str,optional) Customer company name.
     - :GivenName: (str,optional) Customer first name.
     - :FamilyName: (str,optional) Customer last name.
     - :FullyQualifiedName: (str,optional) Fully qualified name of the object.
     - :PreferredDeliveryMethod: (str,optional) Values are Print,Email or None.
     - :PrimaryEmailAddress: (str,optional) Primary email address.
     - :PrimaryPhone: (str,optional) Primary phone number.
     - :PrintOnCheckName: (str,optional) Name of the customer as printed on a check.
     - :Taxable: (boolean,optional) If true, transactions for this customer are taxable.
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
    Returns: 
        dict: A dictionary containing new information about the updated customer.
     
    '''
    
    try:
        if "Id" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/customer"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/customer"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            body_data["SyncToken"] = quickbooks_get_customer_syncToken(
                cred, access_token,params
            )
            #get the customer syncToken and put it in the request payload
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)

def quickbooks_get_invoice_info(cred,access_token,params):
    # get synctoken line items and customer reference for the invoice to update
    try:
        if "Id" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/invoice/{params['Id']}"
            elif env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/invoice/{params['Id']}"

            headers = {
                "Authorization":f"Bearer {access_token}",
                "Accept":"application/json",
            }
            
            api_response = requests.get(url=url,headers=headers)
            response = api_response.json()
            #return only SyncToken ,LIne items and customerRef
            return response['Invoice']['SyncToken'],response['Invoice']['Line'],response['Invoice']['CustomerRef']
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    
def quickbooks_update_invoice(cred,access_token, params):
    
    '''
    Updates the invoice properties with the new properties passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the new invoice information to update it.
    
     - :Id: (str,required) Id of the invoice to update.
     - :Balance: (str,optional) The balance reflecting any payments made against the transaction.
     - :BillEmail: (str,optional) E-mail address to which the invoice will be sent.
     - :CustomerMemo: (dict,optional) A dictionary containing user-entered message to the customer.
      - :value: (str,required)  This message is visible to the end user on their transactions.
     - :DocNumber: (str,optinal) Reference number for the transaction.
     - :DueDate: (date,optional) Date when the payment of the transaction is due.
     - :EmailStatus: (str,optional) Valid values: NotSet, NeedToSend, EmailSent.
     - :PrintStatus: (str,optional) Valid values: NotSet, NeedToPrint, PrintComplete.
     
     - :TotalAmt: (Decimal,optional) Total amount of the transaction.
     - :TxnDate: (date,optional) Date when the transaction occurred.
     
     - :ShipAddr: (dict,optional) A dictionary containing shipping address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
     
     - :BillAddr: (dict,optional) A dictionary containing billing address information.
     
      - :City: (str,optional) Address city.
      - :Line1: (str,optional) Address first line.
      - :PostalCode: (str,optional) Address postal code.
      - :Lat: (str,optional) Latitude coordinate of Geocode.
      - :Long: (str,optioal) Longitude coordinate of Geocode.
      - :CountrySubDivisionCode: (str,optional) Region within a country.
      
    Returns:
       dict: A dictionary containing information about the updated invoice.
      
    '''
    
    try:
        if "Id" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/invoice"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/invoice"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            body_data = {}
            for key, value in params.items():
                body_data[key] = value
            SyncToken,Line,CusotmerRef = quickbooks_get_invoice_info(cred,access_token,params)
            body_data['SyncToken'] = SyncToken
            body_data['Line'] = Line
            body_data['CustomerRef'] = CusotmerRef
            api_response = requests.post(url=url, headers=headers, json=body_data)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


####################################################################
# Get Operations


def quickbooks_get_account(cred,access_token, params):
    
    '''
    Retrieves the account with the specified id passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the account details.
    
      - :AccountID: (str,required) The Id of the account to be retrieved.
      
    Returns:
       dict: A dictionary containing information about the retrieved account.
    '''
    
    try:
        if "AccountID" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/account/{params['AccountID']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/account/{params['AccountID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            api_response = requests.get(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_get_customer(cred,access_token,params):
    
    '''
    Retrieves the customer with the specified id passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the customer id to retrieve it.
    
      - :CustomerID: (str,required) The Id of the customer to be retrieved.
      
    Returns:
       dict: A dictionary containing information about the retrieved customer.
    '''
    
    try:
        if "CustomerID" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/customer/{params['CustomerID']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/customer/{params['CustomerID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            api_response = requests.get(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_get_invoice(cred,access_token,params):
    
    
    '''
    Retrieves the invoice with the specified id passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the invoice id to retrieve it.
    
      - :InvoiceID: (str,required) The Id of the invoice to be retrieved.
      
    Returns:
       dict: A dictionary containing information about the retrieved invoice.
    '''
    
    try:
        if "InvoiceID" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/invoice/{params['InvoiceID']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/invoice/{params['InvoiceID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            api_response = requests.get(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")

    except Exception as e:
        raise Exception(e)


def quickbooks_get_product(cred,access_token,params):
    
    '''
    Retrieves the product with the specified id passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the product id to retrieve it.
    
      - :ProductID: (str,required) The Id of the product to be retrieved.
      
    Returns:
       dict: A dictionary containing information about the retrieved product.
    '''
    
    try:
        if "ProductID" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/item/{params['ProductID']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/item/{params['ProductID']}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            api_response = requests.get(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)


def quickbooks_get_vendor(cred,access_token,params):
    
    '''
    Retrieves the vendor with the specified id passed in params.
    
    :param str access_token: The OAuth2 access token for authentication.
    :param str realmId: The QuickBooks realm/Company ID.
    :param str env: The environment, either "SandBox" or "Production".
    :param dict params: A dictionary containing the vendor id to retrieve it.
    
      - :VendorID: (str,required) The Id of the vendor to be retrieved.
      
    Returns:
       dict: A dictionary containing information about the retrieved vendor.
    '''
    
    try:
        if "VendorID" in params:
            credentials = json.loads(cred)
            env = credentials['environment']
            realmId = credentials['realmId']
            if env == "Sandbox":
                url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}/vendor/{params['VendorID']}"
            if env == "Production":
                url = f"https://quickbooks.api.intuit.com/v3/company/{realmId}/vendor/{params['VendorID']}"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            api_response = requests.get(url=url, headers=headers)
            response = api_response.json()
            if "Fault" in response:
                err_msg = response['Fault']['Error']
                raise Exception(err_msg)
            else:
                return response

        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)



