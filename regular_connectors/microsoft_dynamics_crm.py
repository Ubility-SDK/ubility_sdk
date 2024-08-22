import requests
import json

def microsoft_dynamics_crm_refresh_access_token(cred):
    try:
        creds = json.loads(cred)
        token_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        domain = creds["domain"]
        request_body = {
            "client_id": creds["clientId"],
            "client_secret": creds["clientSecret"],
            "scope": " ".join(
                [f"https://{domain}.crm4.dynamics.com/user_impersonation"]+ ["offline_access"]
            ),
            "refresh_token": creds["refreshToken"],
            "grant_type": "refresh_token",
        }
        response = requests.post(token_endpoint, data=request_body)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_many_account(accessToken, cred):
    """
    Fetches multiple account records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of account records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/accounts"
            headers = {"Authorization": "Bearer " + accessToken}
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_account(accessToken, cred, params):
    """
    Fetches a specific account record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :accountid: (string,required) - The unique identifier of the account to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific account record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "accountid" in params:
            domain = creds["domain"]
            accountid = params["accountid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/accounts({accountid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_account(accessToken, cred, params):
    """
    Creates a new account record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :name: (string,required) - Type the company or business name.
    - :accountnumber: (string,optional) - Type an ID number or code for the account to quickly search and identify the account in system views.
    - :accountratingcode: (Integer,optional) - 	Select a rating to indicate the value of the customer account.
    - :address1_addresstypecode: (Integer,optional) - Select the primary address type.

        **Default Options Values:**

        1. Bill To
        2. Ship To
        3. Primary
        4. Other

    - :address1_city: (string,optional) - Type the city for the primary address.
    - :address1_country: (string,optional) - Type the country or region for the primary address.
    - :address1_county: (string,optional) - Type the county for the primary address.
    - :address1_fax: (string,optional) - Type the fax number associated with the primary address.
    - :address1_freighttermscode:
    (Integer,optional) - Select the freight terms for the primary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. FOB
        2. No Charge

    - :address1_latitude: (Double,optional) - Type the latitude value for the primary address for use in mapping and other applications.
    - :address1_longitude: (Double,optional) - Type the longitude value for the primary address for use in mapping and other applications.
    - :address1_name: (string,optional) - Type a descriptive name for the primary address, such as Corporate Headquarters.
    - :address1_postofficebox: (string,optional) - Type the post office box number of the primary address.
    - :address1_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's primary address.

    - :address1_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Airborne
        2. DHL
        3. FedEx
        4. UPS
        5. Postal Mail
        6. Full Load
        7. Will Call

    - :address1_stateorprovince: (string,optional) - Type the state or province of the primary address.
    - :address1_line1: (string,optional) - Type the first line of the primary address.
    - :address1_line2: (string,optional) - Type the second line of the primary address.
    - :address1_line3: (string,optional) - Type the third line of the primary address.
    - :address1_telephone2: (string,optional) - Type a second phone number associated with the primary address.
    - :address1_telephone3: (string,optional) - Type a third phone number associated with the primary address.
    - :address1_upszone: (string,optional) - Type the UPS zone of the primary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address1_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.
    - :address2_addresstypecode: (Integer,optional) - Select the secondary address type.

        **Default Options Values:**

        1. Default Value

    - :address2_city: (string,optional) - Type the city for the secondary address.
    - :address2_country: (string,optional) - Type the country or region for the secondary address.
    - :address2_county: (string,optional) - Type the county for the secondary address.
    - :address2_fax: (string,optional) - Type the fax number associated with the secondary address.
    - :address2_freighttermscode:
    (Integer,optional) - Select the freight terms for the secondary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. Default Value

    - :address2_latitude: (Double,optional) - Type the latitude value for the secondary address for use in mapping and other applications.
    - :address2_longitude: (Double,optional) - Type the longitude value for the secondary address for use in mapping and other applications.
    - :address2_name: (string,optional) - Type a descriptive name for the secondary address, such as Corporate Headquarters.
    - :address2_postofficebox: (string,optional) - Type the post office box number of the secondary address.
    - :address2_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's secondary address.

    - :address2_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Default Value

    - :address2_stateorprovince:
    (string,optional) - Type the state or province of the secondary address.

    - :address2_line1: (string,optional) - Type the first line of the secondary address.
    - :address2_line2: (string,optional) - Type the second line of the secondary address.
    - :address2_line3: (string,optional) - Type the third line of the secondary address.
    - :address2_telephone1: (string,optional) - Type the main phone number associated with the secondary address.
    - :address2_telephone2: (string,optional) - Type a second phone number associated with the secondary address.
    - :address2_telephone3: (string,optional) - Type a third phone number associated with the secondary address.
    - :address2_upszone: (string,optional) - Type the UPS zone of the secondary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address2_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address2_postalcode: (string,optional) - Type the ZIP Code or postal code for the secondary address.
    - :address1_telephone1: (string,optional) - Type the main phone number associated with the primary address.
    - :revenue: (float,optional) - Type the annual revenue for the account, used as an indicator in financial performance analysis.
    - :businesstypecode: (Integer,optional) - Select the legal designation or other business type of the account for contracts or reporting purposes.

        **Default Options Values:**

        1. Default Value

    - :accountcategorycode: (Integer,optional) - Select a category to indicate whether the customer account is standard or preferred.

        **Default Options Values:**

        1. Preferred Customer
        2. Standard

    - :accountclassificationcode:
    (Integer,optional) - Select a classification code to indicate the potential value of the customer account based on the projected return on investment, cooperation level, sales cycle length or other criteria.

        **Default Options Values:**

        1. Default Value

    - :adx_createdbyipaddress: (string,optional) - Display Name: Created By (IP Address)
    - :adx_createdbyusername: (string,optional) - Display Name: Created By (User Name)
    - :creditonhold: (Boolean,optional) - Select whether the credit for the account is on hold. This is a useful reference while addressing the invoice and accounting issues with the customer. DefaultValue: false
    - :creditlimit: (float,optional) - Type the credit limit of the account. This is a useful reference when you address invoice and accounting issues with the customer.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :customersizecode: (Integer,optional) - Select the size category or range of the account for segmentation and reporting purposes.
    - :description: (string,optional) - Type additional information to describe the account, such as an excerpt from the company's website.
    - :donotbulkemail: (Boolean,optional) - Select whether the account allows bulk email sent through campaigns. If Do Not Allow is selected, the account can be added to marketing lists, but is excluded from email. DefaultValue: false
    - :donotbulkpostalmail: (Boolean,optional) - Select whether the account allows bulk postal mail sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the account can be added to marketing lists, but will be excluded from the postal mail.DefaultValue: false
    - :donotemail: (Boolean,optional) - Select whether the account allows direct email sent from Microsoft Dynamics 365. DefaultValue: false
    - :donotfax: (Boolean,optional) - Select whether the account allows faxes. If Do Not Allow is selected, the account will be excluded from fax activities distributed in marketing campaigns.DefaultValue: false
    - :donotpostalmail: (Boolean,optional) - Select whether the account allows direct mail. If Do Not Allow is selected, the account will be excluded from letter activities distributed in marketing campaigns.DefaultValue: false
    - :donotphone: (Boolean,optional) - Select whether the account allows phone calls. If Do Not Allow is selected, the account will be excluded from phone call activities distributed in marketing campaigns.DefaultValue: false
    - :emailaddress1: (string,optional) - Type the primary email address for the account.
    - :emailaddress2: (string,optional) - Type the secondary email address for the account.
    - :emailaddress3: (string,optional) - Type an alternate email address for the account.
    - :fax: (string,optional) - Type the fax number for the account.
    - :followemail: (Boolean,optional) - Information about whether to allow following email activity like opens, attachment views and link clicks for emails sent to the account.DefaultValue: true
    - :ftpsiteurl: (string,optional) - Type the URL for the account's FTP site to enable users to access data and share documents.
    - :importsequencenumber: (Integer,optional) - Unique identifier of the data import or data migration that created this record.
    - :industrycode: (Integer, optional) - Select the account’s primary industry for use in marketing segmentation and demographic analysis.

        **Default Options Values:**

        1. Accounting
        2. Agriculture and Non-petrol Natural Resource Extraction
        3. Broadcasting Printing and Publishing
        4. Brokers
        5. Building Supply Retail
        6. Business Services
        7. Consulting
        8. Consumer Services
        9. Design, Direction and Creative Management
        10. Distributors, Dispatchers and Processors
        11. Doctor’s Offices and Clinics
        12. Durable Manufacturing
        13. Eating and Drinking Places
        14. Entertainment Retail
        15. Equipment Rental and Leasing
        16. Financial
        17. Food and Tobacco Processing
        18. Inbound Capital Intensive Processing
        19. Inbound Repair and Services
        20. Insurance
        21. Legal Services
        22. Non-Durable Merchandise Retail
        23. Outbound Consumer Service
        24. Petrochemical Extraction and Distribution
        25. Service Retail
        26. SIG Affiliations
        27. Social Services
        28. Special Outbound Trade Contractors
        29. Specialty Realty
        30. Transportation
        31. Utility Creation and Distribution
        32. Vehicle Retail
        33. Wholesale

    - :lastonholdtime: (DateTime,optional) - Contains the date and time stamp of the last on hold time.
    - :telephone1: (String,optional) - Type the main phone number for this account.
    - :marketcap: (float,optional) - Type the market capitalization of the account to identify the company's equity, used as an indicator in financial performance analysis.
    - :marketingonly: (Boolean,optional) - Whether is only for marketing.DefaultValue: false
    - :adx_modifiedbyipaddress: (String,optional) - Modified By (IP Address)
    - :adx_modifiedbyusername: (String,optional) - Modified By (User Name)
    - :numberofemployees: (Integer,optional) - Type the number of employees that work at the account for use in marketing segmentation and demographic analysis.
    - :originatingleadid: (String,optional) - Shows the lead that the account was created from if the account was created by converting a lead in Microsoft Dynamics 365. This is used to relate the account to data on the originating lead for use in reporting and analytics.
    - :telephone2: (String,optional) - Type a second phone number for this account.
    - :ownershipcode: (Integer,optional) - Select the account's ownership structure, such as public or private.

        **Default Options Values:**

        1. Public
        2. Private
        3. Subsidiary
        4. Other

    - :parentaccountid: (String,optional) - Choose the parent account associated with this account to show parent and child businesses in reporting and analytics.
    - :participatesinworkflow: (Boolean,optional) - For system use only. Legacy Microsoft Dynamics CRM 3.0 workflow data.DefaultValue: false
    - :paymenttermscode: (Integer,optional) - Select the payment terms to indicate when the customer needs to pay the total amount.

        **Default Options Values:**

        1. Net 30
        2. 2% 10, Net 30
        3. Net 45
        4. Net 60

    - :preferredappointmentdaycode:
    (Integer,optional) - Select the preferred day of the week for service appointments.

        **Default Options Values:**

        0. Sunday
        1. Monday
        2. Tuesday
        3. Wednesday
        4. Thursday
        5. Friday
        6. Saturday

    - :preferredcontactmethodcode: (Integer,optional) - Select the preferred method of contact.

        **Default Options Values:**

        1. Any
        2. Email
        3. Phone
        4. Fax
        5. Mail

    - :preferredappointmenttimecode: (Integer,optional) - Select the preferred time of day for service appointments.

        **Default Options Values:**

        1. Morning
        2. Afternoon
        3. Evening

    - :defaultpricelevelid: (String,optional) - Choose the default price list associated with the account to make sure the correct product prices for this customer are applied in sales opportunities, quotes, and orders.
    - :primarycontactid: (String,optional) - Choose the primary contact for the account to provide quick access to contact details.
    - :primarysatoriid: (String,optional) - Primary Satori ID for Account
    - :primarytwitterid: (String,optional) - Primary Twitter ID for Account
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :customertypecode: (Integer,optional) - Select the category that best describes the relationship between the account and your organization.

        **Default Options Values:**

        1. Competitor
        2. Consultant
        3. Customer
        4. Investor
        5. Partner
        6. Influencer
        7. Press
        8. Prospect
        9. Reseller
        10. Supplier
        11. Vendor
        12. Other

    - :donotsendmm: (Boolean,optional) - Select whether the account accepts marketing materials, such as brochures or catalogs.DefaultValue: false
    - :sharesoutstanding: (Integer,optional) - Type the number of shares available to the public for the account. This number is used as an indicator in financial performance analysis.
    - :shippingmethodcode: (Integer,optional) - Select a shipping method for deliveries sent to the account's address to designate the preferred carrier or other delivery option.

        **Default Options Values:**

        1. Default Value

    - :sic: (String,optional) - Type the Standard Industrial Classification (SIC) code that indicates the account's primary industry of business, for use in marketing segmentation and demographic analysis.
    - :statuscode: (Integer,optional) - Select the account's status.

        **Default Options Values:**

        1. Active
        2. Inactive

    - :stockexchange: (String,optional) - Type the stock exchange at which the account is listed to track their stock and financial performance of the company.
    - :teamsfollowed: (Integer,optional) - Number of users or conversations followed the record
    - :telephone3: (String,optional) - Type a third phone number for this account.
    - :territorycode: (Integer,optional) - Select a region or territory for the account for use in segmentation and analysis.

        **Default Options Values:**

        1. Default Value

    - :tickersymbol: (String,optional) - Type the stock exchange symbol for the account to track financial performance of the company. You can click the code entered in this field to access the latest trading information from MSN Money.
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :websiteurl: (String,optional) - Type the account's website URL to get quick details about the company profile.
    - :yominame: (String,optional) - Type the phonetic spelling of the company name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.

    Returns:
        dict: A dictionary containing detailed information about the newly created account record.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "name" in params:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/accounts"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "primarycontactid" in params:
                data['primarycontactid@odata.bind'] = f"/contacts({params['primarycontactid']})"
            if "originatingleadid" in params:
                data['originatingleadid@odata.bind'] = f"/leads({params['originatingleadid']})"
            if "defaultpricelevelid" in params:
                data['defaultpricelevelid@odata.bind'] = f"/pricelevels({params['defaultpricelevelid']})"
            if "parentaccountid" in params:
                data['parentaccountid@odata.bind'] = f"/accounts({params['parentaccountid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid", "primarycontactid","originatingleadid", "defaultpricelevelid","parentaccountid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_account(accessToken, cred, params):
    """
    Updates a specific account record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :accountid: (string,required) - The unique identifier of the account to be updated.
    - :name: (string,optional) - Type the company or business name.
    - :accountnumber: (string,optional) - Type an ID number or code for the account to quickly search and identify the account in system views.
    - :accountratingcode: (Integer,optional) - 	Select a rating to indicate the value of the customer account.
    - :address1_addresstypecode: (Integer,optional) - Select the primary address type.

        **Default Options Values:**

        1. Bill To
        2. Ship To
        3. Primary
        4. Other

    - :address1_city: (string,optional) - Type the city for the primary address.
    - :address1_country: (string,optional) - Type the country or region for the primary address.
    - :address1_county: (string,optional) - Type the county for the primary address.
    - :address1_fax: (string,optional) - Type the fax number associated with the primary address.
    - :address1_freighttermscode:
    (Integer,optional) - Select the freight terms for the primary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. FOB
        2. No Charge

    - :address1_latitude: (Double,optional) - Type the latitude value for the primary address for use in mapping and other applications.
    - :address1_longitude: (Double,optional) - Type the longitude value for the primary address for use in mapping and other applications.
    - :address1_name: (string,optional) - Type a descriptive name for the primary address, such as Corporate Headquarters.
    - :address1_postofficebox: (string,optional) - Type the post office box number of the primary address.
    - :address1_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's primary address.

    - :address1_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Airborne
        2. DHL
        3. FedEx
        4. UPS
        5. Postal Mail
        6. Full Load
        7. Will Call

    - :address1_stateorprovince: (string,optional) - Type the state or province of the primary address.
    - :address1_line1: (string,optional) - Type the first line of the primary address.
    - :address1_line2: (string,optional) - Type the second line of the primary address.
    - :address1_line3: (string,optional) - Type the third line of the primary address.
    - :address1_telephone2: (string,optional) - Type a second phone number associated with the primary address.
    - :address1_telephone3: (string,optional) - Type a third phone number associated with the primary address.
    - :address1_upszone: (string,optional) - Type the UPS zone of the primary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address1_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.
    - :address2_addresstypecode: (Integer,optional) - Select the secondary address type.

        **Default Options Values:**

        1. Default Value

    - :address2_city: (string,optional) - Type the city for the secondary address.
    - :address2_country: (string,optional) - Type the country or region for the secondary address.
    - :address2_county: (string,optional) - Type the county for the secondary address.
    - :address2_fax: (string,optional) - Type the fax number associated with the secondary address.
    - :address2_freighttermscode:
    (Integer,optional) - Select the freight terms for the secondary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. Default Value

    - :address2_latitude: (Double,optional) - Type the latitude value for the secondary address for use in mapping and other applications.
    - :address2_longitude: (Double,optional) - Type the longitude value for the secondary address for use in mapping and other applications.
    - :address2_name: (string,optional) - Type a descriptive name for the secondary address, such as Corporate Headquarters.
    - :address2_postofficebox: (string,optional) - Type the post office box number of the secondary address.
    - :address2_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's secondary address.

    - :address2_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Default Value

    - :address2_stateorprovince:
    (string,optional) - Type the state or province of the secondary address.

    - :address2_line1: (string,optional) - Type the first line of the secondary address.
    - :address2_line2: (string,optional) - Type the second line of the secondary address.
    - :address2_line3: (string,optional) - Type the third line of the secondary address.
    - :address2_telephone1: (string,optional) - Type the main phone number associated with the secondary address.
    - :address2_telephone2: (string,optional) - Type a second phone number associated with the secondary address.
    - :address2_telephone3: (string,optional) - Type a third phone number associated with the secondary address.
    - :address2_upszone: (string,optional) - Type the UPS zone of the secondary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address2_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address2_postalcode: (string,optional) - Type the ZIP Code or postal code for the secondary address.
    - :address1_telephone1: (string,optional) - Type the main phone number associated with the primary address.
    - :revenue: (float,optional) - Type the annual revenue for the account, used as an indicator in financial performance analysis.
    - :businesstypecode: (Integer,optional) - Select the legal designation or other business type of the account for contracts or reporting purposes.

        **Default Options Values:**

        1. Default Value

    - :accountcategorycode: (Integer,optional) - Select a category to indicate whether the customer account is standard or preferred.

        **Default Options Values:**

        1. Preferred Customer
        2. Standard

    - :accountclassificationcode:
    (Integer,optional) - Select a classification code to indicate the potential value of the customer account based on the projected return on investment, cooperation level, sales cycle length or other criteria.

        **Default Options Values:**

        1. Default Value

    - :adx_createdbyipaddress: (string,optional) - Display Name: Created By (IP Address)
    - :adx_createdbyusername: (string,optional) - Display Name: Created By (User Name)
    - :creditonhold: (Boolean,optional) - Select whether the credit for the account is on hold. This is a useful reference while addressing the invoice and accounting issues with the customer. DefaultValue: false
    - :creditlimit: (float,optional) - Type the credit limit of the account. This is a useful reference when you address invoice and accounting issues with the customer.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :customersizecode: (Integer,optional) - Select the size category or range of the account for segmentation and reporting purposes.
    - :description: (string,optional) - Type additional information to describe the account, such as an excerpt from the company's website.
    - :donotbulkemail: (Boolean,optional) - Select whether the account allows bulk email sent through campaigns. If Do Not Allow is selected, the account can be added to marketing lists, but is excluded from email. DefaultValue: false
    - :donotbulkpostalmail: (Boolean,optional) - Select whether the account allows bulk postal mail sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the account can be added to marketing lists, but will be excluded from the postal mail.DefaultValue: false
    - :donotemail: (Boolean,optional) - Select whether the account allows direct email sent from Microsoft Dynamics 365. DefaultValue: false
    - :donotfax: (Boolean,optional) - Select whether the account allows faxes. If Do Not Allow is selected, the account will be excluded from fax activities distributed in marketing campaigns.DefaultValue: false
    - :donotpostalmail: (Boolean,optional) - Select whether the account allows direct mail. If Do Not Allow is selected, the account will be excluded from letter activities distributed in marketing campaigns.DefaultValue: false
    - :donotphone: (Boolean,optional) - Select whether the account allows phone calls. If Do Not Allow is selected, the account will be excluded from phone call activities distributed in marketing campaigns.DefaultValue: false
    - :emailaddress1: (string,optional) - Type the primary email address for the account.
    - :emailaddress2: (string,optional) - Type the secondary email address for the account.
    - :emailaddress3: (string,optional) - Type an alternate email address for the account.
    - :fax: (string,optional) - Type the fax number for the account.
    - :followemail: (Boolean,optional) - Information about whether to allow following email activity like opens, attachment views and link clicks for emails sent to the account.DefaultValue: true
    - :ftpsiteurl: (string,optional) - Type the URL for the account's FTP site to enable users to access data and share documents.
    - :importsequencenumber: (Integer,optional) - Unique identifier of the data import or data migration that created this record.
    - :industrycode: (Integer, optional) - Select the account’s primary industry for use in marketing segmentation and demographic analysis.

        **Default Options Values:**

        1. Accounting
        2. Agriculture and Non-petrol Natural Resource Extraction
        3. Broadcasting Printing and Publishing
        4. Brokers
        5. Building Supply Retail
        6. Business Services
        7. Consulting
        8. Consumer Services
        9. Design, Direction and Creative Management
        10. Distributors, Dispatchers and Processors
        11. Doctor’s Offices and Clinics
        12. Durable Manufacturing
        13. Eating and Drinking Places
        14. Entertainment Retail
        15. Equipment Rental and Leasing
        16. Financial
        17. Food and Tobacco Processing
        18. Inbound Capital Intensive Processing
        19. Inbound Repair and Services
        20. Insurance
        21. Legal Services
        22. Non-Durable Merchandise Retail
        23. Outbound Consumer Service
        24. Petrochemical Extraction and Distribution
        25. Service Retail
        26. SIG Affiliations
        27. Social Services
        28. Special Outbound Trade Contractors
        29. Specialty Realty
        30. Transportation
        31. Utility Creation and Distribution
        32. Vehicle Retail
        33. Wholesale

    - :lastonholdtime: (DateTime,optional) - Contains the date and time stamp of the last on hold time.
    - :telephone1: (String,optional) - Type the main phone number for this account.
    - :marketcap: (float,optional) - Type the market capitalization of the account to identify the company's equity, used as an indicator in financial performance analysis.
    - :marketingonly: (Boolean,optional) - Whether is only for marketing.DefaultValue: false
    - :adx_modifiedbyipaddress: (String,optional) - Modified By (IP Address)
    - :adx_modifiedbyusername: (String,optional) - Modified By (User Name)
    - :numberofemployees: (Integer,optional) - Type the number of employees that work at the account for use in marketing segmentation and demographic analysis.
    - :originatingleadid: (String,optional) - Shows the lead that the account was created from if the account was created by converting a lead in Microsoft Dynamics 365. This is used to relate the account to data on the originating lead for use in reporting and analytics.
    - :telephone2: (String,optional) - Type a second phone number for this account.
    - :ownershipcode: (Integer,optional) - Select the account's ownership structure, such as public or private.

        **Default Options Values:**

        1. Public
        2. Private
        3. Subsidiary
        4. Other

    - :parentaccountid: (String,optional) - Choose the parent account associated with this account to show parent and child businesses in reporting and analytics.
    - :participatesinworkflow: (Boolean,optional) - For system use only. Legacy Microsoft Dynamics CRM 3.0 workflow data.DefaultValue: false
    - :paymenttermscode: (Integer,optional) - Select the payment terms to indicate when the customer needs to pay the total amount.

        **Default Options Values:**

        1. Net 30
        2. 2% 10, Net 30
        3. Net 45
        4. Net 60

    - :preferredappointmentdaycode:
    (Integer,optional) - Select the preferred day of the week for service appointments.

        **Default Options Values:**

        0. Sunday
        1. Monday
        2. Tuesday
        3. Wednesday
        4. Thursday
        5. Friday
        6. Saturday

    - :preferredcontactmethodcode: (Integer,optional) - Select the preferred method of contact.

        **Default Options Values:**

        1. Any
        2. Email
        3. Phone
        4. Fax
        5. Mail

    - :preferredappointmenttimecode: (Integer,optional) - Select the preferred time of day for service appointments.

        **Default Options Values:**

        1. Morning
        2. Afternoon
        3. Evening

    - :defaultpricelevelid: (String,optional) - Choose the default price list associated with the account to make sure the correct product prices for this customer are applied in sales opportunities, quotes, and orders.
    - :primarycontactid: (String,optional) - Choose the primary contact for the account to provide quick access to contact details.
    - :primarysatoriid: (String,optional) - Primary Satori ID for Account
    - :primarytwitterid: (String,optional) - Primary Twitter ID for Account
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :customertypecode: (Integer,optional) - Select the category that best describes the relationship between the account and your organization.

        **Default Options Values:**

        1. Competitor
        2. Consultant
        3. Customer
        4. Investor
        5. Partner
        6. Influencer
        7. Press
        8. Prospect
        9. Reseller
        10. Supplier
        11. Vendor
        12. Other

    - :donotsendmm: (Boolean,optional) - Select whether the account accepts marketing materials, such as brochures or catalogs.DefaultValue: false
    - :sharesoutstanding: (Integer,optional) - Type the number of shares available to the public for the account. This number is used as an indicator in financial performance analysis.
    - :shippingmethodcode: (Integer,optional) - Select a shipping method for deliveries sent to the account's address to designate the preferred carrier or other delivery option.

        **Default Options Values:**

        1. Default Value

    - :sic: (String,optional) - Type the Standard Industrial Classification (SIC) code that indicates the account's primary industry of business, for use in marketing segmentation and demographic analysis.
    - :statuscode: (Integer,optional) - Select the account's status.

        **Default Options Values:**

        1. Active
        2. Inactive

    - :stockexchange: (String,optional) - Type the stock exchange at which the account is listed to track their stock and financial performance of the company.
    - :teamsfollowed: (Integer,optional) - Number of users or conversations followed the record
    - :telephone3: (String,optional) - Type a third phone number for this account.
    - :territorycode: (Integer,optional) - Select a region or territory for the account for use in segmentation and analysis.

        **Default Options Values:**

        1. Default Value

    - :tickersymbol: (String,optional) - Type the stock exchange symbol for the account to track financial performance of the company. You can click the code entered in this field to access the latest trading information from MSN Money.
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :websiteurl: (String,optional) - Type the account's website URL to get quick details about the company profile.
    - :yominame: (String,optional) - Type the phonetic spelling of the company name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.

    Returns:
        dict: A dictionary containing detailed information about the updated account record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "accountid" in params:
            domain = creds["domain"]
            accountid = params["accountid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/accounts({accountid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "primarycontactid" in params:
                data['primarycontactid@odata.bind'] = f"/contacts({params['primarycontactid']})"
            if "originatingleadid" in params:
                data['originatingleadid@odata.bind'] = f"/leads({params['originatingleadid']})"
            if "defaultpricelevelid" in params:
                data['defaultpricelevelid@odata.bind'] = f"/pricelevels({params['defaultpricelevelid']})"
            if "parentaccountid" in params:
                data['parentaccountid@odata.bind'] = f"/accounts({params['parentaccountid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid", "primarycontactid","originatingleadid", "defaultpricelevelid","parentaccountid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_account(accessToken, cred, params):
    """
    Deletes a specific account record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :accountid: (string,required) - The unique identifier of the account to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the account was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "accountid" in params:
            domain = creds["domain"]
            accountid = params["accountid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/accounts({accountid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Account deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Contacts ####################################################

def microsoft_dynamics_crm_get_many_contact(accessToken, cred):
    """
    Fetches multiple contact records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of contact records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/contacts"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_contact(accessToken, cred, params):
    """
    Fetches a specific contact record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :contactid: (string,required) - The unique identifier of the contact to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific contact record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "contactid" in params:
            contactid = params["contactid"]
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/contacts({contactid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_contact(accessToken, cred, params):
    """
    Creates a new contact record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :firstname: (string,required) - Type the contact's first name to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastname: (string,required) - Type the contact's last name to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :adx_identity_accessfailedcount:
    (Integer,optional) - Shows the current count of failed password attempts for the contact.

    - :address1_addresstypecode: (Integer,optional) - Select the primary address type.

        **Default Options Values:**

            1. Bill To
            2. Ship To
            3. Primary
            4. Other
    - :address1_city: (string,optional) - Type the city for the primary address.
    - :address1_country: (string,optional) - Type the country or region for the primary address.
    - :address1_county: (string,optional) - Type the county for the primary address.
    - :address1_fax: (string,optional) - Type the fax number associated with the primary address.
    - :address1_freighttermscode:
    (Integer,optional) - Select the freight terms for the primary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

            1. FOB
            2. No Charge
    - :address1_latitude: (Double,optional) - Type the latitude value for the primary address for use in mapping and other applications.
    - :address1_longitude: (Double,optional) - Type the longitude value for the primary address for use in mapping and other applications.
    - :address1_name: (string,optional) - Type a descriptive name for the primary address, such as Corporate Headquarters.
    - :address1_postofficebox: (string,optional) - Type the post office box number of the primary address.
    - :address1_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's primary address.

    - :address1_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

            1. Airborne
            2. DHL
            3. FedEx
            4. UPS
            5. Postal Mail
            6. Full Load
            7. Will Call

    - :address1_stateorprovince: (string,optional) - Type the state or province of the primary address.
    - :address1_line1: (string,optional) - Type the first line of the primary address.
    - :address1_line2: (string,optional) - Type the second line of the primary address.
    - :address1_line3: (string,optional) - Type the third line of the primary address.
    - :address1_telephone2: (string,optional) - Type a second phone number associated with the primary address.
    - :address1_telephone3: (string,optional) - Type a third phone number associated with the primary address.
    - :address1_upszone: (string,optional) - Type the UPS zone of the primary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address1_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.
    - :address2_addresstypecode: (Integer,optional) - Select the secondary address type.

        **Default Options Values:**

        1. Default Value
    - :address2_city: (string,optional) - Type the city for the secondary address.
    - :address2_country: (string,optional) - Type the country or region for the secondary address.
    - :address2_county: (string,optional) - Type the county for the secondary address.
    - :address2_fax: (string,optional) - Type the fax number associated with the secondary address.
    - :address2_freighttermscode:
    (Integer,optional) - Select the freight terms for the secondary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. Default Value
    - :address2_latitude: (Double,optional) - Type the latitude value for the secondary address for use in mapping and other applications.
    - :address2_longitude: (Double,optional) - Type the longitude value for the secondary address for use in mapping and other applications.
    - :address2_name: (string,optional) - Type a descriptive name for the secondary address, such as Corporate Headquarters.
    - :address2_postofficebox: (string,optional) - Type the post office box number of the secondary address.
    - :address2_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's secondary address.

    - :address2_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Default Value
    - :address2_stateorprovince:
    (string,optional) - Type the state or province of the secondary address.

    - :address2_line1: (string,optional) - Type the first line of the secondary address.
    - :address2_line2: (string,optional) - Type the second line of the secondary address.
    - :address2_line3: (string,optional) - Type the third line of the secondary address.
    - :address2_telephone1: (string,optional) - Type the main phone number associated with the secondary address.
    - :address2_telephone2: (string,optional) - Type a second phone number associated with the secondary address.
    - :address2_telephone3: (string,optional) - Type a third phone number associated with the secondary address.
    - :address2_upszone: (string,optional) - Type the UPS zone of the secondary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address2_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address2_postalcode: (string,optional) - Type the ZIP Code or postal code for the secondary address.
    - :address3_addresstypecode: (Integer,optional) - Select the third address type.

        **Default Options Values:**

        1. Default Value
    - :address3_city: (string,optional) - Type the city for the 3rd address.
    - :address3_country: (string,optional) - Type the country or region for the 3rd address.
    - :address3_county: (string,optional) - Type the county for the 3rd address.
    - :address3_fax: (string,optional) - Type the fax number associated with the 3rd address.
    - :address3_freighttermscode:
    (Integer,optional) - Select the freight terms for the 3rd address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. Default Value
    - :address3_latitude: (Double,optional) - Type the latitude value for the 3rd address for use in mapping and other applications.
    - :address3_longitude: (Double,optional) - Type the longitude value for the 3rd address for use in mapping and other applications.
    - :address3_name: (string,optional) - Type a descriptive name for the 3rd address, such as Corporate Headquarters.
    - :address3_postofficebox: (string,optional) - Type the post office box number of the 3rd address.
    - :address3_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's 3rd address.

    - :address3_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Default Value
    - :address3_stateorprovince: (string,optional) - Type the state or province of the 3rd address.
    - :address3_line1: (string,optional) - Type the first line of the 3rd address.
    - :address3_line2: (string,optional) - Type the second line of the 3rd address.
    - :address3_line3: (string,optional) - Type the third line of the 3rd address.
    - :address3_telephone1: (string,optional) - Type the main phone number associated with the 3rd address.
    - :address3_telephone2: (string,optional) - Type a second phone number associated with the 3rd address.
    - :address3_telephone3: (string,optional) - Type a third phone number associated with the 3rd address.
    - :address3_upszone: (string,optional) - Type the UPS zone of the 3rd address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address3_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address3_postalcode: (string,optional) - Type the ZIP Code or postal code for the 3rd address.
    - :anniversary: (Date,optional) - Enter the date of the contact's wedding or service anniversary for use in customer gift programs or other communications.
    - :annualincome: (Float,optional) - Type the contact's annual income for use in profiling and financial analysis.
    - :assistantname: (string,optional) - Type the name of the contact's assistant.
    - :assistantphone: (string,optional) - Type the phone number for the contact's assistant.
    - :isbackofficecustomer: (Boolean,optional) - Select whether the contact exists in a separate accounting or other system, such as Microsoft Dynamics GP or another ERP database, for use in integration processes.
    - :birthdate: (Date,optional) - Enter the contact's birthday for use in customer gift programs or other communications.
    - :telephone1: (string,optional) - Type the main phone number for this contact.
    - :business2: (string,optional) - Type a second business phone number for this contact.
    - :callback: (string,optional) - Type a callback phone number for this contact.
    - :childrensnames: (string,optional) - Type the names of the contact's children for reference in communications and client programs.
    - :company: (string,optional) - Type the company phone of the contact.
    - :adx_confirmremovepassword: (Boolean,optional) - Confirm Remove Password
    - :adx_createdbyipaddress: (string,optional) - Display Name: Created By (IP Address)
    - :adx_createdbyusername: (string,optional) - Display Name: Created By (User Name)
    - :creditonhold: (Boolean,optional) - Select whether the contact is on a credit hold, for reference when addressing invoice and accounting issues.DefaultValue: false
    - :creditlimit: (Float,optional) - Type the credit limit of the contact for reference when you address invoice and accounting issues with the customer.
    - :transactioncurrencyid:
    (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.

    - :customersizecode: (Integer,optional) - Select the size of the contact's company for segmentation and reporting purposes.

        **Default Options Values:**

        1. Default Value
    - :department: (string,optional) - Type the department or business unit where the contact works in the parent company or business.
    - :description: (string,optional) - Type additional information to describe the contact, such as an excerpt from the company's website.
    - :msdyn_disablewebtracking:
    (Boolean,optional) - Indicates that the contact has opted out of web tracking.

    - :donotbulkemail: (Boolean,optional) - Select whether the contact accepts bulk email sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the contact can be added to marketing lists, but will be excluded from the email.
    - :donotbulkpostalmail:
    (Boolean,optional) - Select whether the contact accepts bulk postal mail sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the contact can be added to marketing lists, but will be excluded from the letters.

    - :donotfax: (Boolean,optional) - Select whether the contact allows faxes. If Do Not Allow is selected, the contact will be excluded from any fax activities distributed in marketing campaigns.
    - :donotemail: (Boolean,optional) - Select whether the contact allows direct email sent from Microsoft Dynamics 365. If Do Not Allow is selected, Microsoft Dynamics 365 will not send the email.
    - :donotpostalmail: (Boolean,optional) - Select whether the contact allows direct mail. If Do Not Allow is selected, the contact will be excluded from letter activities distributed in marketing campaigns
    - :donotphone: (Boolean,optional) - Select whether the contact accepts phone calls. If Do Not Allow is selected, the contact will be excluded from any phone call activities distributed in marketing campaigns.
    - :educationcode: (Integer,optional) - Select the contact's highest level of education for use in segmentation and analysis.

        **Default Options Values:**

        1. Default Value
    - :emailaddress1: (string,optional) - Type the primary email address for the contact.
    - :emailaddress2: (string,optional) - Type the secondary email address for the contact.
    - :emailaddress3: (string,optional) - Type an alternate email address for the contact.
    - :adx_identity_emailaddress1confirmed:
    (Boolean,optional) - Determines if the email is confirmed by the contact.

    - :employeeid: (string,optional) - Type the employee ID or number for the contact for reference in orders, service cases, or other communications with the contact's organization.
    - :externaluseridentifier: (string,optional) - Identifier for an external user.
    - :fax: (string,optional) - Type the fax number for the contact.
    - :followemail: (Boolean,optional) - Information about whether to allow following email activity like opens, attachment views and link clicks for emails sent to the contact.
    - :ftpsiteurl: (string,optional) - Type the URL for the contact's FTP site to enable users to access data and share documents.
    - :gendercode: (Integer,optional) - Select the contact's gender to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.

        **Default Options Values:**

            1. Male
            2. Female
    - :governmentid: (string,optional) - Type the passport number or other government ID for the contact for use in documents or reports.
    - :haschildrencodeSelect:
    (Integer,optional) -  whether the contact has any children for reference in follow-up phone calls and other communications.

        **Default Options Values:**
        1. Default Value
    - :telephone2: (string,optional) - Type a second phone number for this contact.
    - :home2: (string,optional) - Type a second home phone number for this contact.
    - :importsequencenumber:
    (Integer,optional) -  Unique identifier of the data import or data migration that created this record.

    - :msdyn_isminor: (Boolean,optional) - Indicates that the contact is considered a minor in their jurisdiction.
    - :msdyn_isminorwithparentalconsent:
    (Boolean,optional) - Indicates that the contact is considered a minor in their jurisdiction and has parental consent.

    - :jobtitle: (String,optional) - Type the job title of the contact to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastonholdtime: (String,optional) - Contains the date and time stamp of the last on hold time.
    - :adx_identity_lastsuccessfullogin:
    (String,optional) - Indicates the last date and time the user successfully signed in to a portal.

    - :leadsourcecode: (Integer,optional) - Select the primary marketing source that directed the contact to your organization.

        **Default Options Values:**
        1. Default Value
    - :adx_identity_locallogindisabled:
    (Boolean,optional) - Indicates that the contact can no longer sign in to the portal using the local account.

    - :adx_identity_lockoutenabled:
    (Boolean,optional) - Determines if this contact will track failed access attempts and become locked after too many failed attempts. To prevent the contact from becoming locked, you can disable this setting.

    - :adx_identity_lockoutenddate:
    (DateTime,optional) - Shows the moment in time when the locked contact becomes unlocked again.

    - :adx_identity_logonenabled:
    (Boolean,optional) - Determines if web authentication is enabled for the contact.

    - :managername: (String,optional) - Type the name of the contact's manager for use in escalating issues or other follow-up communications with the contact.
    - :managerphone: (String,optional) - Type the phone number for the contact's manager.
    - :familystatuscode: (Integer,optional) - Select the marital status of the contact for reference in follow-up phone calls and other communications.

        **Default Options Values:**
            1. Single
            2. Married
            3. Divorced
            4. Widowed
    - :marketingonly: (Boolean,optional) - Whether is only for marketing
    - :middlename: (String,optional) - Type the contact's middle name or initial to make sure the contact is addressed correctly.
    - :mobilephone: (String,optional) - Type the mobile phone number for the contact.
    - :adx_identity_mobilephoneconfirmed:
    (Boolean,optional) - Determines if the phone number is confirmed by the contact.

    - :adx_modifiedbyipaddress:
    (String,optional) - Display Name: Modified By IP Address

    - :adx_modifiedbyusername: (String,optional) - Display Name: Modified By Username
    - :adx_identity_newpassword: (String,optional) - New Password Input
    - :nickname: (String,optional) - Type the contact's nickname.
    - :numberofchildren: (Integer,optional) - Type the number of children the contact has for reference in follow-up phone calls and other communications.
    - :adx_organizationname:
    (String,optional) - Display Name: Organization Name

    - :pager: (String,optional) - Type the pager number for the contact.
    - :participatesinworkflow: (Boolean,optional) - Shows whether the contact participates in workflow rules.
    - :adx_identity_passwordhash: (String,optional) - Password Hash
    - :paymenttermscode: (Integer,optional) - Select the payment terms to indicate when the customer needs to pay the total amount.

        **Default Options Values:**
            1. Net 30
            2. 2% 10, Net 30
            3. Net 45
            4. Net 60
    - :msdyn_portaltermsagreementdate:
    (DateTime,optional) - Indicates the date and time that the person agreed to the portal terms and conditions.

    - :preferredappointmentdaycode:
    (Integer,optional) - Select the preferred day of the week for service appointments.

        **Default Options Values:**
            0. Sunday
            1. Monday
            2. Tuesday
            3. Wednesday
            4. Thursday
            5. Friday
            6. Saturday
    - :mspp_userpreferredlcid: (Integer,optional) - User’s preferred portal language

        **Default Options Values:**
            - 1025: Arabic
            - 1069: Basque-Basque
            - 1026: Bulgarian - Bulgaria
            - 1027: Catalan - Catalan
            - 2052: Chinese - China
            - 3076: Chinese - Hong Kong SAR
            - 1028: Chinese - Traditional
            - 1050: Croatian - Croatia
            - 1029: Czech - Czech Republic
            - 1030: Danish - Denmark
            - 1043: Dutch - Netherlands
            - 1033: English
            - 1061: Estonian - Estonia
            - 1035: Finnish - Finland
            - 1036: French - France
            - 1110: Galician - Spain
            - 1031: German - Germany
            - 1032: Greek - Greece
            - 1037: Hebrew
            - 1081: Hindi - India
            - 1038: Hungarian - Hungary
            - 1057: Indonesian - Indonesia
            - 1040: Italian - Italy
            - 1041: Japanese - Japan
            - 1087: Kazakh - Kazakhstan
            - 1042: Korean - Korea
            - 1062: Latvian - Latvia
            - 1063: Lithuanian - Lithuania
            - 1086: Malay - Malaysia
            - 1044: Norwegian (Bokmål) - Norway
            - 1045: Polish - Poland
            - 1046: Portuguese - Brazil
            - 2070: Portuguese - Portugal
            - 1048: Romanian - Romania
            - 1049: Russian - Russia
            - 3098: Serbian (Cyrillic) - Serbia
            - 2074: Serbian (Latin) - Serbia
            - 1051: Slovak - Slovakia
            - 1060: Slovenian - Slovenia
            - 3082: Spanish (Traditional Sort) - Spain
            - 1053: Swedish - Sweden
            - 1054: Thai - Thailand
            - 1055: Turkish - Türkiye
            - 1058: Ukrainian - Ukraine
            - 1066: Vietnamese - Vietnam

    - :adx_preferredlcid: (Integer,optional) - User’s preferred portal LCID
    - :preferredcontactmethodcode:
    (Integer,optional) - Select the preferred method of contact.

        **Default Options Values:**
            1. Any
            2. Email
            3. Phone
            4. Fax
            5. Mail
    - :preferredappointmenttimecode:
    (Integer,optional) - Select the preferred time of day for service appointments.

        **Default Options Values:**
            1. Morning
            2. Afternoon
            3. Evening
    - :adx_profilealert: (Boolean,optional) - Profile Alert
    - :adx_profilealertdate: (DateTime,optional) - Profile Alert Date
    - :adx_profilealertinstructions: (String,optional) - Profile Alert Instructions
    - :adx_profileisanonymous: (Boolean,optional) - Profile Is Anonymous
    - :adx_profilelastactivity: (DateTime,optional) - Profile Last Activity
    - :adx_profilemodifiedon: (DateTime,optional) - Profile Modified On
    - :adx_publicprofilecopy: (String,optional) - Public Profile Copy
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :customertypecode: (Integer,optional) - Select the category that best describes the relationship between the contact and your organization.

        **Default Options Values:**
        1. Default Value
    - :accountrolecode: (Integer,optional) - Select the contact's role within the company or sales process, such as decision maker, employee, or influencer.

        **Default Options Values:**
            1. Decision Maker
            2. Employee
            3. Influencer
    - :salutation: (String,optional) - Type the salutation of the contact to make sure the contact is addressed correctly in sales calls, email messages, and marketing campaigns.
    - :adx_identity_securitystamp:
    (String,optional) - A token used to manage the web authentication session.

    - :donotsendmm: (Boolean,optional) - Select whether the contact accepts marketing materials, such as brochures or catalogs. Contacts that opt out can be excluded from marketing initiatives.
    - :shippingmethodcode: (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
        1. Default Value
    - :spousesname: (String,optional) - Type the name of the contact's spouse or partner for reference during calls, events, or other communications with the contact.
    - :statuscode: (Integer,optional) - Select the contact's status.

        **Default Options Values:**
            1. Active
            2. Inactive
    - :suffix: (String,optional) - Type the suffix used in the contact's name, such as Jr. or Sr. to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :telephone3: (String,optional) - Type a third phone number for this contact.
    - :territorycode: (Integer,optional) - Select a region or territory for the contact for use in segmentation and analysis.

        **Default Options Values:**
        1. Default Value
    - :adx_timezone: (Integer,optional) - Time Zone
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :adx_identity_twofactorenabled:
    (Boolean,optional) - Determines if two-factor authentication is enabled for the contact.

    - :adx_identity_username: (String,optional) - Shows the user identity for local web authentication.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :websiteurl: (String,optional) - Type the contact's professional or personal website or blog URL.
    - :yomifirstname: (String,optional) - Type the phonetic spelling of the contact's first name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the contact.
    - :yomilastname: (String,optional) - Type the phonetic spelling of the contact's last name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the contact.
    - :yomimiddlename: (String,optional) - Type the phonetic spelling of the contact's middle name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the contact.

    Returns:
        dict: A dictionary containing detailed information about the newly created contact record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "firstname" in params and "lastname" in params:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/contacts"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "originatingleadid" in params:
                data['originatingleadid@odata.bind'] = f"/leads({params['originatingleadid']})"
            if "defaultpricelevelid" in params:
                data['defaultpricelevelid@odata.bind'] = f"/pricelevels({params['defaultpricelevelid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid","originatingleadid", "defaultpricelevelid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_contact(accessToken, cred, params):
    """
    Updates a specific contact record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :contactid: (string,required) - The unique identifier of the contact to be updated.
    - :firstname: (string,optional) - Type the contact's first name to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastname: (string,optional) - Type the contact's last name to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :adx_identity_accessfailedcount:
    (Integer,optional) - Shows the current count of failed password attempts for the contact.

    - :address1_addresstypecode: (Integer,optional) - Select the primary address type.

        **Default Options Values:**

            1. Bill To
            2. Ship To
            3. Primary
            4. Other
    - :address1_city: (string,optional) - Type the city for the primary address.
    - :address1_country: (string,optional) - Type the country or region for the primary address.
    - :address1_county: (string,optional) - Type the county for the primary address.
    - :address1_fax: (string,optional) - Type the fax number associated with the primary address.
    - :address1_freighttermscode:
    (Integer,optional) - Select the freight terms for the primary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

            1. FOB
            2. No Charge
    - :address1_latitude: (Double,optional) - Type the latitude value for the primary address for use in mapping and other applications.
    - :address1_longitude: (Double,optional) - Type the longitude value for the primary address for use in mapping and other applications.
    - :address1_name: (string,optional) - Type a descriptive name for the primary address, such as Corporate Headquarters.
    - :address1_postofficebox: (string,optional) - Type the post office box number of the primary address.
    - :address1_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's primary address.

    - :address1_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

            1. Airborne
            2. DHL
            3. FedEx
            4. UPS
            5. Postal Mail
            6. Full Load
            7. Will Call

    - :address1_stateorprovince: (string,optional) - Type the state or province of the primary address.
    - :address1_line1: (string,optional) - Type the first line of the primary address.
    - :address1_line2: (string,optional) - Type the second line of the primary address.
    - :address1_line3: (string,optional) - Type the third line of the primary address.
    - :address1_telephone2: (string,optional) - Type a second phone number associated with the primary address.
    - :address1_telephone3: (string,optional) - Type a third phone number associated with the primary address.
    - :address1_upszone: (string,optional) - Type the UPS zone of the primary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address1_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.
    - :address2_addresstypecode: (Integer,optional) - Select the secondary address type.

        **Default Options Values:**

        1. Default Value
    - :address2_city: (string,optional) - Type the city for the secondary address.
    - :address2_country: (string,optional) - Type the country or region for the secondary address.
    - :address2_county: (string,optional) - Type the county for the secondary address.
    - :address2_fax: (string,optional) - Type the fax number associated with the secondary address.
    - :address2_freighttermscode:
    (Integer,optional) - Select the freight terms for the secondary address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. Default Value
    - :address2_latitude: (Double,optional) - Type the latitude value for the secondary address for use in mapping and other applications.
    - :address2_longitude: (Double,optional) - Type the longitude value for the secondary address for use in mapping and other applications.
    - :address2_name: (string,optional) - Type a descriptive name for the secondary address, such as Corporate Headquarters.
    - :address2_postofficebox: (string,optional) - Type the post office box number of the secondary address.
    - :address2_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's secondary address.

    - :address2_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Default Value
    - :address2_stateorprovince:
    (string,optional) - Type the state or province of the secondary address.

    - :address2_line1: (string,optional) - Type the first line of the secondary address.
    - :address2_line2: (string,optional) - Type the second line of the secondary address.
    - :address2_line3: (string,optional) - Type the third line of the secondary address.
    - :address2_telephone1: (string,optional) - Type the main phone number associated with the secondary address.
    - :address2_telephone2: (string,optional) - Type a second phone number associated with the secondary address.
    - :address2_telephone3: (string,optional) - Type a third phone number associated with the secondary address.
    - :address2_upszone: (string,optional) - Type the UPS zone of the secondary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address2_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address2_postalcode: (string,optional) - Type the ZIP Code or postal code for the secondary address.
    - :address3_addresstypecode: (Integer,optional) - Select the third address type.

        **Default Options Values:**

        1. Default Value
    - :address3_city: (string,optional) - Type the city for the 3rd address.
    - :address3_country: (string,optional) - Type the country or region for the 3rd address.
    - :address3_county: (string,optional) - Type the county for the 3rd address.
    - :address3_fax: (string,optional) - Type the fax number associated with the 3rd address.
    - :address3_freighttermscode:
    (Integer,optional) - Select the freight terms for the 3rd address to make sure shipping orders are processed correctly.

        **Default Options Values:**

        1. Default Value
    - :address3_latitude: (Double,optional) - Type the latitude value for the 3rd address for use in mapping and other applications.
    - :address3_longitude: (Double,optional) - Type the longitude value for the 3rd address for use in mapping and other applications.
    - :address3_name: (string,optional) - Type a descriptive name for the 3rd address, such as Corporate Headquarters.
    - :address3_postofficebox: (string,optional) - Type the post office box number of the 3rd address.
    - :address3_primarycontactname:
    (string,optional) - Type the name of the main contact at the account's 3rd address.

    - :address3_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**

        1. Default Value
    - :address3_stateorprovince: (string,optional) - Type the state or province of the 3rd address.
    - :address3_line1: (string,optional) - Type the first line of the 3rd address.
    - :address3_line2: (string,optional) - Type the second line of the 3rd address.
    - :address3_line3: (string,optional) - Type the third line of the 3rd address.
    - :address3_telephone1: (string,optional) - Type the main phone number associated with the 3rd address.
    - :address3_telephone2: (string,optional) - Type a second phone number associated with the 3rd address.
    - :address3_telephone3: (string,optional) - Type a third phone number associated with the 3rd address.
    - :address3_upszone: (string,optional) - Type the UPS zone of the 3rd address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address3_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address3_postalcode: (string,optional) - Type the ZIP Code or postal code for the 3rd address.
    - :anniversary: (Date,optional) - Enter the date of the contact's wedding or service anniversary for use in customer gift programs or other communications.
    - :annualincome: (Float,optional) - Type the contact's annual income for use in profiling and financial analysis.
    - :assistantname: (string,optional) - Type the name of the contact's assistant.
    - :assistantphone: (string,optional) - Type the phone number for the contact's assistant.
    - :isbackofficecustomer: (Boolean,optional) - Select whether the contact exists in a separate accounting or other system, such as Microsoft Dynamics GP or another ERP database, for use in integration processes.
    - :birthdate: (Date,optional) - Enter the contact's birthday for use in customer gift programs or other communications.
    - :telephone1: (string,optional) - Type the main phone number for this contact.
    - :business2: (string,optional) - Type a second business phone number for this contact.
    - :callback: (string,optional) - Type a callback phone number for this contact.
    - :childrensnames: (string,optional) - Type the names of the contact's children for reference in communications and client programs.
    - :company: (string,optional) - Type the company phone of the contact.
    - :adx_confirmremovepassword: (Boolean,optional) - Confirm Remove Password
    - :adx_createdbyipaddress: (string,optional) - Display Name: Created By (IP Address)
    - :adx_createdbyusername: (string,optional) - Display Name: Created By (User Name)
    - :creditonhold: (Boolean,optional) - Select whether the contact is on a credit hold, for reference when addressing invoice and accounting issues.DefaultValue: false
    - :creditlimit: (Float,optional) - Type the credit limit of the contact for reference when you address invoice and accounting issues with the customer.
    - :transactioncurrencyid:
    (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.

    - :customersizecode: (Integer,optional) - Select the size of the contact's company for segmentation and reporting purposes.

        **Default Options Values:**

        1. Default Value
    - :department: (string,optional) - Type the department or business unit where the contact works in the parent company or business.
    - :description: (string,optional) - Type additional information to describe the contact, such as an excerpt from the company's website.
    - :msdyn_disablewebtracking:
    (Boolean,optional) - Indicates that the contact has opted out of web tracking.

    - :donotbulkemail: (Boolean,optional) - Select whether the contact accepts bulk email sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the contact can be added to marketing lists, but will be excluded from the email.
    - :donotbulkpostalmail:
    (Boolean,optional) - Select whether the contact accepts bulk postal mail sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the contact can be added to marketing lists, but will be excluded from the letters.

    - :donotfax: (Boolean,optional) - Select whether the contact allows faxes. If Do Not Allow is selected, the contact will be excluded from any fax activities distributed in marketing campaigns.
    - :donotemail: (Boolean,optional) - Select whether the contact allows direct email sent from Microsoft Dynamics 365. If Do Not Allow is selected, Microsoft Dynamics 365 will not send the email.
    - :donotpostalmail: (Boolean,optional) - Select whether the contact allows direct mail. If Do Not Allow is selected, the contact will be excluded from letter activities distributed in marketing campaigns
    - :donotphone: (Boolean,optional) - Select whether the contact accepts phone calls. If Do Not Allow is selected, the contact will be excluded from any phone call activities distributed in marketing campaigns.
    - :educationcode: (Integer,optional) - Select the contact's highest level of education for use in segmentation and analysis.

        **Default Options Values:**

        1. Default Value
    - :emailaddress1: (string,optional) - Type the primary email address for the contact.
    - :emailaddress2: (string,optional) - Type the secondary email address for the contact.
    - :emailaddress3: (string,optional) - Type an alternate email address for the contact.
    - :adx_identity_emailaddress1confirmed:
    (Boolean,optional) - Determines if the email is confirmed by the contact.

    - :employeeid: (string,optional) - Type the employee ID or number for the contact for reference in orders, service cases, or other communications with the contact's organization.
    - :externaluseridentifier: (string,optional) - Identifier for an external user.
    - :fax: (string,optional) - Type the fax number for the contact.
    - :followemail: (Boolean,optional) - Information about whether to allow following email activity like opens, attachment views and link clicks for emails sent to the contact.
    - :ftpsiteurl: (string,optional) - Type the URL for the contact's FTP site to enable users to access data and share documents.
    - :gendercode: (Integer,optional) - Select the contact's gender to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.

        **Default Options Values:**

            1. Male
            2. Female
    - :governmentid: (string,optional) - Type the passport number or other government ID for the contact for use in documents or reports.
    - :haschildrencodeSelect:
    (Integer,optional) -  whether the contact has any children for reference in follow-up phone calls and other communications.

        **Default Options Values:**
        1. Default Value
    - :telephone2: (string,optional) - Type a second phone number for this contact.
    - :home2: (string,optional) - Type a second home phone number for this contact.
    - :importsequencenumber:
    (Integer,optional) -  Unique identifier of the data import or data migration that created this record.

    - :msdyn_isminor: (Boolean,optional) - Indicates that the contact is considered a minor in their jurisdiction.
    - :msdyn_isminorwithparentalconsent:
    (Boolean,optional) - Indicates that the contact is considered a minor in their jurisdiction and has parental consent.

    - :jobtitle: (String,optional) - Type the job title of the contact to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastonholdtime: (String,optional) - Contains the date and time stamp of the last on hold time.
    - :adx_identity_lastsuccessfullogin:
    (String,optional) - Indicates the last date and time the user successfully signed in to a portal.

    - :leadsourcecode: (Integer,optional) - Select the primary marketing source that directed the contact to your organization.

        **Default Options Values:**
        1. Default Value
    - :adx_identity_locallogindisabled:
    (Boolean,optional) - Indicates that the contact can no longer sign in to the portal using the local account.

    - :adx_identity_lockoutenabled:
    (Boolean,optional) - Determines if this contact will track failed access attempts and become locked after too many failed attempts. To prevent the contact from becoming locked, you can disable this setting.

    - :adx_identity_lockoutenddate:
    (DateTime,optional) - Shows the moment in time when the locked contact becomes unlocked again.

    - :adx_identity_logonenabled:
    (Boolean,optional) - Determines if web authentication is enabled for the contact.

    - :managername: (String,optional) - Type the name of the contact's manager for use in escalating issues or other follow-up communications with the contact.
    - :managerphone: (String,optional) - Type the phone number for the contact's manager.
    - :familystatuscode: (Integer,optional) - Select the marital status of the contact for reference in follow-up phone calls and other communications.

        **Default Options Values:**
            1. Single
            2. Married
            3. Divorced
            4. Widowed
    - :marketingonly: (Boolean,optional) - Whether is only for marketing
    - :middlename: (String,optional) - Type the contact's middle name or initial to make sure the contact is addressed correctly.
    - :mobilephone: (String,optional) - Type the mobile phone number for the contact.
    - :adx_identity_mobilephoneconfirmed:
    (Boolean,optional) - Determines if the phone number is confirmed by the contact.

    - :adx_modifiedbyipaddress:
    (String,optional) - Display Name: Modified By IP Address

    - :adx_modifiedbyusername: (String,optional) - Display Name: Modified By Username
    - :adx_identity_newpassword: (String,optional) - New Password Input
    - :nickname: (String,optional) - Type the contact's nickname.
    - :numberofchildren: (Integer,optional) - Type the number of children the contact has for reference in follow-up phone calls and other communications.
    - :adx_organizationname:
    (String,optional) - Display Name: Organization Name

    - :pager: (String,optional) - Type the pager number for the contact.
    - :participatesinworkflow: (Boolean,optional) - Shows whether the contact participates in workflow rules.
    - :adx_identity_passwordhash: (String,optional) - Password Hash
    - :paymenttermscode: (Integer,optional) - Select the payment terms to indicate when the customer needs to pay the total amount.

        **Default Options Values:**
            1. Net 30
            2. 2% 10, Net 30
            3. Net 45
            4. Net 60
    - :msdyn_portaltermsagreementdate:
    (DateTime,optional) - Indicates the date and time that the person agreed to the portal terms and conditions.

    - :preferredappointmentdaycode:
    (Integer,optional) - Select the preferred day of the week for service appointments.

        **Default Options Values:**
            0. Sunday
            1. Monday
            2. Tuesday
            3. Wednesday
            4. Thursday
            5. Friday
            6. Saturday
    - :mspp_userpreferredlcid: (Integer,optional) - User’s preferred portal language

        **Default Options Values:**
            - 1025: Arabic
            - 1069: Basque-Basque
            - 1026: Bulgarian - Bulgaria
            - 1027: Catalan - Catalan
            - 2052: Chinese - China
            - 3076: Chinese - Hong Kong SAR
            - 1028: Chinese - Traditional
            - 1050: Croatian - Croatia
            - 1029: Czech - Czech Republic
            - 1030: Danish - Denmark
            - 1043: Dutch - Netherlands
            - 1033: English
            - 1061: Estonian - Estonia
            - 1035: Finnish - Finland
            - 1036: French - France
            - 1110: Galician - Spain
            - 1031: German - Germany
            - 1032: Greek - Greece
            - 1037: Hebrew
            - 1081: Hindi - India
            - 1038: Hungarian - Hungary
            - 1057: Indonesian - Indonesia
            - 1040: Italian - Italy
            - 1041: Japanese - Japan
            - 1087: Kazakh - Kazakhstan
            - 1042: Korean - Korea
            - 1062: Latvian - Latvia
            - 1063: Lithuanian - Lithuania
            - 1086: Malay - Malaysia
            - 1044: Norwegian (Bokmål) - Norway
            - 1045: Polish - Poland
            - 1046: Portuguese - Brazil
            - 2070: Portuguese - Portugal
            - 1048: Romanian - Romania
            - 1049: Russian - Russia
            - 3098: Serbian (Cyrillic) - Serbia
            - 2074: Serbian (Latin) - Serbia
            - 1051: Slovak - Slovakia
            - 1060: Slovenian - Slovenia
            - 3082: Spanish (Traditional Sort) - Spain
            - 1053: Swedish - Sweden
            - 1054: Thai - Thailand
            - 1055: Turkish - Türkiye
            - 1058: Ukrainian - Ukraine
            - 1066: Vietnamese - Vietnam

    - :adx_preferredlcid: (Integer,optional) - User’s preferred portal LCID
    - :preferredcontactmethodcode:
    (Integer,optional) - Select the preferred method of contact.

        **Default Options Values:**
        1. Any
        2. Email
        3. Phone
        4. Fax
        5. Mail
    - :preferredappointmenttimecode:
    (Integer,optional) - Select the preferred time of day for service appointments.

        **Default Options Values:**
        1. Morning
        2. Afternoon
        3. Evening
    - :adx_profilealert: (Boolean,optional) - Profile Alert
    - :adx_profilealertdate: (DateTime,optional) - Profile Alert Date
    - :adx_profilealertinstructions: (String,optional) - Profile Alert Instructions
    - :adx_profileisanonymous: (Boolean,optional) - Profile Is Anonymous
    - :adx_profilelastactivity: (DateTime,optional) - Profile Last Activity
    - :adx_profilemodifiedon: (DateTime,optional) - Profile Modified On
    - :adx_publicprofilecopy: (String,optional) - Public Profile Copy
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :customertypecode: (Integer,optional) - Select the category that best describes the relationship between the contact and your organization.

        **Default Options Values:**
        1. Default Value
    - :accountrolecode: (Integer,optional) - Select the contact's role within the company or sales process, such as decision maker, employee, or influencer.

        **Default Options Values:**
        1. Decision Maker
        2. Employee
        3. Influencer
    - :salutation: (String,optional) - Type the salutation of the contact to make sure the contact is addressed correctly in sales calls, email messages, and marketing campaigns.
    - :adx_identity_securitystamp:
    (String,optional) - A token used to manage the web authentication session.

    - :donotsendmm: (Boolean,optional) - Select whether the contact accepts marketing materials, such as brochures or catalogs. Contacts that opt out can be excluded from marketing initiatives.
    - :shippingmethodcode: (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
        1. Default Value
    - :spousesname: (String,optional) - Type the name of the contact's spouse or partner for reference during calls, events, or other communications with the contact.
    - :statuscode: (Integer,optional) - Select the contact's status.

        **Default Options Values:**
        1. Active
        2. Inactive
    - :suffix: (String,optional) - Type the suffix used in the contact's name, such as Jr. or Sr. to make sure the contact is addressed correctly in sales calls, email, and marketing campaigns.
    - :telephone3: (String,optional) - Type a third phone number for this contact.
    - :territorycode: (Integer,optional) - Select a region or territory for the contact for use in segmentation and analysis.

        **Default Options Values:**
        1. Default Value
    - :adx_timezone: (Integer,optional) - Time Zone
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :adx_identity_twofactorenabled:
    (Boolean,optional) - Determines if two-factor authentication is enabled for the contact.

    - :adx_identity_username: (String,optional) - Shows the user identity for local web authentication.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :websiteurl: (String,optional) - Type the contact's professional or personal website or blog URL.
    - :yomifirstname: (String,optional) - Type the phonetic spelling of the contact's first name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the contact.
    - :yomilastname: (String,optional) - Type the phonetic spelling of the contact's last name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the contact.
    - :yomimiddlename: (String,optional) - Type the phonetic spelling of the contact's middle name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the contact.

    Returns:
        dict: A dictionary containing detailed information about the updated contact record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "contactid" in params:
            domain = creds["domain"]
            contactid = params["contactid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/contacts({contactid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "originatingleadid" in params:
                data['originatingleadid@odata.bind'] = f"/leads({params['originatingleadid']})"
            if "defaultpricelevelid" in params:
                data['defaultpricelevelid@odata.bind'] = f"/pricelevels({params['defaultpricelevelid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid","originatingleadid", "defaultpricelevelid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_contact(accessToken, cred, params):
    """
    Deletes a specific contact record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :contactid: (string,required) - The unique identifier of the contact to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the contact was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "contactid" in params:
            contactid = params["contactid"]
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/contacts({contactid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Contact deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Campaigns ####################################################

def microsoft_dynamics_crm_get_many_campaign(accessToken, cred):
    """
    Fetches multiple campaign records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of campaign records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaigns"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_campaign(accessToken, cred, params):
    """
    Fetches a specific campaign record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :campaignid: (string,required) - The unique identifier of the campaign to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific campaign record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "campaignid" in params:
            domain = creds["domain"]
            campaignid = params["campaignid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaigns({campaignid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_campaign(accessToken, cred, params):
    """
    Creates a new campaign record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :name: (string,required) - Type a name for the campaign so that it is identified correctly in lists.
    - :actualend: (DateTime,optional) - Enter the date when the campaign was closed or completed.
    - :actualstart: (DateTime,optional) - Enter the actual start date and time for the campaign.
    - :budgetedcost: (Integer,optional) - Type the amount budgeted for the campaign to define a limit for how much you can spend.
    - :codename: (string,optional) - Type a number or other tracking code to identify the campaign. If no value is entered, a code will be generated automatically.
    - :typecode: (Integer,optional) - Select the type of the campaign.

        **Default Options Values:**
            - 1: Advertisement
            - 2: Direct Marketing
            - 3: Event
            - 4: Co-branding
            - 5: Other
    - :description: (string,optional) - Type additional information to describe the campaign, such as the products or services offered or the targeted audience.
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :expectedrevenue: (Integer,optional) - Type the expected revenue for the campaign for return on investment projections and post-campaign reporting.
    - :expectedresponse: (Integer,optional) - Type the expected response rate for the campaign as a full number between 0 and 100.
    - :msdyn_gdproptout: (Boolean,optional) - Describes whether campaign is opted out or not.DefaultValue: false
    - :importsequencenumber:
    (Integer,optional) - Sequence number of the import that created this record.

    - :message: (string,optional) - Type the promotional message or marketing copy for the campaign.
    - :othercost: (Integer,optional) - Type the sum of any miscellaneous campaign costs not included in the campaign activities to make sure the actual cost of the campaign is calculated correctly.
    - :objective: (string,optional) - Type the objective of the campaign, including products, services, discounts, and pricing.
    - :pricelistid: (string,optional) - Choose the price list associated with this item to make sure the products associated with the campaign are offered at the correct prices.
    - :promotioncodename:
    (string,optional) - Type a promotional code to track sales related to the campaign or allow customers to redeem a discount offer.

    - :proposedend: (DateTime,optional) - Enter the date when the campaign is scheduled to end.
    - :proposedstart: (DateTime,optional) - Enter the date when the campaign is scheduled to start.
    - :overriddencreatedon:
    (DateTime,optional) - Date and time that the record was migrated.

    - :statuscode: (string,optional) - Select the campaign's status.

        **Default Options Values:**
            - 0: Proposed
            - 1: Ready To Launch
            - 2: Launched
            - 3: Completed
            - 4: Canceled
            - 5: Suspended
            - 6: Inactive
    - :istemplate: (Boolean,optional) - Select whether the campaign is a template that can be copied when you create future campaigns.DefaultValue: false
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :tmpregardingobjectid: (string,optional) - tmpregardingobjectid
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the newly created campaign record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "name" in params:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaigns"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "pricelistid" in params:
                data['pricelistid@odata.bind'] = f"/pricelevels({params['pricelistid']})"
            for key, value in params.items():
                skip_keys = ["pricelistid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_campaign(accessToken, cred, params):
    """
    Updates a specific campaign record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :campaignid: (string,required) - The unique identifier of the campaign to be updated.
    - :actualend: (DateTime,optional) - Enter the date when the campaign was closed or completed.
    - :actualstart: (DateTime,optional) - Enter the actual start date and time for the campaign.
    - :budgetedcost: (Integer,optional) - Type the amount budgeted for the campaign to define a limit for how much you can spend.
    - :codename: (string,optional) - Type a number or other tracking code to identify the campaign. If no value is entered, a code will be generated automatically.
    - :typecode: (Integer,optional) - Select the type of the campaign.

        **Default Options Values:**
            - 1: Advertisement
            - 2: Direct Marketing
            - 3: Event
            - 4: Co-branding
            - 5: Other
    - :description: (string,optional) - Type additional information to describe the campaign, such as the products or services offered or the targeted audience.
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :expectedrevenue: (Integer,optional) - Type the expected revenue for the campaign for return on investment projections and post-campaign reporting.
    - :expectedresponse: (Integer,optional) - Type the expected response rate for the campaign as a full number between 0 and 100.
    - :msdyn_gdproptout: (Boolean,optional) - Describes whether campaign is opted out or not.DefaultValue: false
    - :importsequencenumber:
    (Integer,optional) - Sequence number of the import that created this record.

    - :message: (string,optional) - Type the promotional message or marketing copy for the campaign.
    - :othercost: (Integer,optional) - Type the sum of any miscellaneous campaign costs not included in the campaign activities to make sure the actual cost of the campaign is calculated correctly.
    - :objective: (string,optional) - Type the objective of the campaign, including products, services, discounts, and pricing.
    - :pricelistid: (string,optional) - Choose the price list associated with this item to make sure the products associated with the campaign are offered at the correct prices.
    - :promotioncodename:
    (string,optional) - Type a promotional code to track sales related to the campaign or allow customers to redeem a discount offer.

    - :proposedend: (DateTime,optional) - Enter the date when the campaign is scheduled to end.
    - :proposedstart: (DateTime,optional) - Enter the date when the campaign is scheduled to start.
    - :overriddencreatedon:
    (DateTime,optional) - Date and time that the record was migrated.

    - :statuscode: (string,optional) - Select the campaign's status.

        **Default Options Values:**
            - 0: Proposed
            - 1: Ready To Launch
            - 2: Launched
            - 3: Completed
            - 4: Canceled
            - 5: Suspended
            - 6: Inactive
    - :istemplate: (Boolean,optional) - Select whether the campaign is a template that can be copied when you create future campaigns.DefaultValue: false
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :tmpregardingobjectid: (string,optional) - tmpregardingobjectid
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the updated campaign record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "campaignid" in params:
            domain = creds["domain"]
            campaignid = params["campaignid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaigns({campaignid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "pricelistid" in params:
                data['pricelistid@odata.bind'] = f"/pricelevels({params['pricelistid']})"
            for key, value in params.items():
                skip_keys = ["pricelistid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_campaign(accessToken, cred, params):
    """
    Deletes a specific campaign record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :campaignid: (string,required) - The unique identifier of the campaign to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the campaign was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "campaignid" in params:
            domain = creds["domain"]
            campaignid = params["campaignid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaigns({campaignid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Campaign deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Campaign Responses ####################################################

def microsoft_dynamics_crm_get_many_campaign_responses(accessToken, cred):
    """
    Fetches multiple campaign responses records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of campaign responses records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaignresponses"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_campaign_responses(accessToken, cred, params):
    """
    Fetches a specific campaign responses record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :activityid: (string,required) - The unique identifier of the campaign responses to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific campaign responses record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "activityid" in params:
            domain = creds["domain"]
            activityid = params["activityid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaignresponses({activityid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_campaign_responses(accessToken, cred, params):
    """
    Creates a new campaign responses record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :campaignid: (string,required) - Choose the parent campaign so that the campaign's response rate is tracked correctly.
    - :subject: (string,required) - Type a short description about the objective or primary topic of the campaign response.
    - :actualdurationminutes: (Integer,optional) - Type the number of minutes spent on this activity. The duration is used in reporting.
    - :actualend: (DateTime,optional) - Enter the date when the campaign response was actually completed.
    - :actualstart: (DateTime,optional) - Enter the actual start date and time for the campaign response.
    - :activityadditionalparams: (string,optional) - For internal use only.
    - :category: (string,optional) - Type a category to identify the campaign response type, such as new business development or customer retention, to tie the campaign response to a business group or function.
    - :channeltypecode: (Integer,optional) - Select how the response was received, such as phone, letter, fax, or email.

        **Default Options Values:**
            - 1: Email
            - 2: Phone
            - 3: Fax
            - 4: Letter
            - 5: Appointment
            - 6: Others
    - :scheduledend: (DateTime,optional) - Enter the expected due date and time for the activity to be completed to provide details about the timing of the campaign response.
    - :companyname: (string,optional) - Type the name of the company if the campaign response was received from a new prospect or customer.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :deliveryprioritycode: (Integer,optional) - Priority of delivery of the activity to the email server.

        **Default Options Values:**
            - 0: Low
            - 1: Normal
            - 2: High
    - :description: (string,optional) - Type additional information to describe the campaign response, such as key discussion points or objectives.
    - :emailaddress: (string,optional) - Type the responder's email address.
    - :exchangeitemid: (string,optional) - The message id of activity which is returned from Exchange Server.
    - :exchangeweblink: (string,optional) - Shows the web link of Activity of type email.
    - :fax: (string,optional) - Type the responder's fax number.
    - :firstname: (string,optional) - Type the responder's first name if the campaign response was received from a new prospect or customer.
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :isbilled: (Boolean,optional) - Specifies whether the campaign response was billed as part of resolving a case.DefaultValue: false
    - :ismapiprivate: (Boolean,optional) - For internal use only.DefaultValue: false
    - :isworkflowcreated: (Boolean,optional) - Specifies whether the campaign response is created by a workflow rule.DefaultValue: false
    - :lastname: (string,optional) - Type the responder's last name if the campaign response was received from a new prospect or customer.
    - :lastonholdtime: (DateTime,optional) - Contains the date and time stamp of the last on hold time.
    - :leftvoicemail: (Boolean,optional) - Left the voice mail.DefaultValue: false
    - :telephone: (string,optional) - Type the responder's primary phone number.
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
            - 0: Low
            - 1: Normal
            - 2: High
    - :promotioncodename: (string,optional) - Type a promotional code to track sales related to the campaign response or to allow the responder to redeem a discount offer.
    - :receivedon: (DateTime,optional) - Enter the date when the campaign response was received.
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :responsecode: (Integer,optional) - Select the type of response from the prospect or customer to indicate their interest in the campaign.

        **Default Options Values:**
            - 1: Interested
            - 2: Not Interested
            - 3: Do Not Send Marketing Materials
            - 4: Error
    - :scheduledstart: (DateTime,optional) - Enter the expected start date and time for the activity to provide details about the timing of the campaign response.
    - :community: (Integer,optional) - Shows how contact about the social activity originated, such as from Twitter or Facebook. This field is read-only.

        **Default Options Values:**
            - 0: Other
            - 1: Facebook
            - 2: Twitter
            - 3: Line
            - 4: Wechat
            - 5: Cortana
            - 6: Direct Line
            - 7: Microsoft Teams
            - 8: Direct Line Speech
            - 9: Email
            - 10: GroupMe
            - 11: Kik
            - 12: Telegram
            - 13: Skype
            - 14: Slack
            - 15: WhatsApp
            - 16: Apple Messages For Business
            - 17: Google’s Business Messages
    - :sortdate: (DateTime,optional) - Shows the date and time by which the activities are sorted.
    - :statuscode: (string,optional) - Select the campaign response's status.

        **Default Options Values:**
            - 1: Open
            - 2: Closed
            - 3: Canceled
    - :subcategory: (string,optional) - Type a subcategory to identify the campaign response type and relate the activity to a specific product, sales region, business group, or other function.
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :yomicompanyname: (string,optional) - Type the phonetic spelling of the company name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.
    - :yomifirstname: (string,optional) - Type the phonetic spelling of the campaign responder's first name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.
    - :yomilastname: (string,optional) - Type the phonetic spelling of the campaign responder's last name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.

    Returns:
        dict: A dictionary containing detailed information about the newly created campaign responses record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "campaignid" in params and "subject" in params:
            domain = creds["domain"]
            campaignid = params["campaignid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaignresponses"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {
                'regardingobjectid_campaign@odata.bind': f'/campaigns({campaignid})'
            }
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid", "campaignid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_campaign_responses(accessToken, cred, params):
    """
    Updates a specific campaign_responses record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :activityid: (string,required) - The unique identifier of the campaign responses to be updated.
    - :regardingobjectid: (string,optional) - Choose the parent campaign so that the campaign's response rate is tracked correctly.
    - :subject: (string,optional) - Type a short description about the objective or primary topic of the campaign response.
    - :actualdurationminutes: (Integer,optional) - Type the number of minutes spent on this activity. The duration is used in reporting.
    - :actualend: (DateTime,optional) - Enter the date when the campaign response was actually completed.
    - :actualstart: (DateTime,optional) - Enter the actual start date and time for the campaign response.
    - :activityadditionalparams: (string,optional) - For internal use only.
    - :category: (string,optional) - Type a category to identify the campaign response type, such as new business development or customer retention, to tie the campaign response to a business group or function.
    - :channeltypecode: (Integer,optional) - Select how the response was received, such as phone, letter, fax, or email.

        **Default Options Values:**
            - 1: Email
            - 2: Phone
            - 3: Fax
            - 4: Letter
            - 5: Appointment
            - 6: Others
    - :scheduledend: (DateTime,optional) - Enter the expected due date and time for the activity to be completed to provide details about the timing of the campaign response.
    - :companyname: (string,optional) - Type the name of the company if the campaign response was received from a new prospect or customer.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :deliveryprioritycode: (Integer,optional) - Priority of delivery of the activity to the email server.

        **Default Options Values:**
            - 0: Low
            - 1: Normal
            - 2: High
    - :description: (string,optional) - Type additional information to describe the campaign response, such as key discussion points or objectives.
    - :emailaddress: (string,optional) - Type the responder's email address.
    - :exchangeitemid: (string,optional) - The message id of activity which is returned from Exchange Server.
    - :exchangeweblink: (string,optional) - Shows the web link of Activity of type email.
    - :fax: (string,optional) - Type the responder's fax number.
    - :firstname: (string,optional) - Type the responder's first name if the campaign response was received from a new prospect or customer.
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :isbilled: (Boolean,optional) - Specifies whether the campaign response was billed as part of resolving a case.DefaultValue: false
    - :ismapiprivate: (Boolean,optional) - For internal use only.DefaultValue: false
    - :isworkflowcreated: (Boolean,optional) - Specifies whether the campaign response is created by a workflow rule.DefaultValue: false
    - :lastname: (string,optional) - Type the responder's last name if the campaign response was received from a new prospect or customer.
    - :lastonholdtime: (DateTime,optional) - Contains the date and time stamp of the last on hold time.
    - :leftvoicemail: (Boolean,optional) - Left the voice mail.DefaultValue: false
    - :telephone: (string,optional) - Type the responder's primary phone number.
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
            - 0: Low
            - 1: Normal
            - 2: High
    - :promotioncodename: (string,optional) - Type a promotional code to track sales related to the campaign response or to allow the responder to redeem a discount offer.
    - :receivedon: (DateTime,optional) - Enter the date when the campaign response was received.
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :responsecode: (Integer,optional) - Select the type of response from the prospect or customer to indicate their interest in the campaign.

        **Default Options Values:**
            - 1: Interested
            - 2: Not Interested
            - 3: Do Not Send Marketing Materials
            - 4: Error
    - :scheduledstart: (DateTime,optional) - Enter the expected start date and time for the activity to provide details about the timing of the campaign response.
    - :community: (Integer,optional) - Shows how contact about the social activity originated, such as from Twitter or Facebook. This field is read-only.

        **Default Options Values:**
            - 0: Other
            - 1: Facebook
            - 2: Twitter
            - 3: Line
            - 4: Wechat
            - 5: Cortana
            - 6: Direct Line
            - 7: Microsoft Teams
            - 8: Direct Line Speech
            - 9: Email
            - 10: GroupMe
            - 11: Kik
            - 12: Telegram
            - 13: Skype
            - 14: Slack
            - 15: WhatsApp
            - 16: Apple Messages For Business
            - 17: Google’s Business Messages
    - :sortdate: (DateTime,optional) - Shows the date and time by which the activities are sorted.
    - :statuscode: (string,optional) - Select the campaign response's status.

        **Default Options Values:**
            - 1: Open
            - 2: Closed
            - 3: Canceled
    - :subcategory: (string,optional) - Type a subcategory to identify the campaign response type and relate the activity to a specific product, sales region, business group, or other function.
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :yomicompanyname: (string,optional) - Type the phonetic spelling of the company name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.
    - :yomifirstname: (string,optional) - Type the phonetic spelling of the campaign responder's first name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.
    - :yomilastname: (string,optional) - Type the phonetic spelling of the campaign responder's last name, if specified in Japanese, to make sure the name is pronounced correctly in phone calls and other communications.

    Returns:
        dict: A dictionary containing detailed information about the updated campaign_responses record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "activityid" in params:
            domain = creds["domain"]
            activityid = params["activityid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaignresponses({activityid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_campaign_responses(accessToken, cred, params):
    """
    Deletes a specific campaign responses record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :activityid: (string,required) - The unique identifier of the campaign responses to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the campaign responses was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "activityid" in params:
            domain = creds["domain"]
            activityid = params["activityid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/campaignresponses({activityid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Campaign responses deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Invoices ####################################################

def microsoft_dynamics_crm_get_many_invoice(accessToken, cred):
    """
    Fetches multiple invoice records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of invoice records.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/invoices"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_invoice(accessToken, cred, params):
    """
    Fetches a specific invoice record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :invoiceid: (string,required) - The unique identifier of the invoice to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific invoice record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "invoiceid" in params:
            domain = creds["domain"]
            invoiceid = params["invoiceid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/invoices({invoiceid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_invoice(accessToken, cred, params):
    """
    Creates a new invoice record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :transactioncurrencyid: (string,required) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :name: (string,required) - Type a descriptive name for the invoice.
    - :pricelevelid: (string,required) - Choose the price list associated with this record to make sure the products associated with the campaign are offered at the correct prices.
    - :billto_city: (string,optional) - Type the city for the customer's billing address.
    - :billto_country: (string,optional) - Type the country or region for the customer's billing address.
    - :billto_fax: (string,optional) - Type the fax number for the customer's billing address.
    - :billto_name: (string,optional) - Type a name for the customer's billing address, such as "Headquarters" or "Field office", to identify the address.
    - :billto_telephone: (string,optional) - Type the phone number for the customer's billing address.
    - :billto_stateorprovince: (string,optional) - Type the state or province for the billing address.
    - :billto_line1: (string,optional) - Type the first line of the customer's billing address.
    - :billto_line2: (string,optional) - Type the second line of the customer's billing address.
    - :billto_line3: (string,optional) - Type the third line of the billing address.
    - :billto_postalcode: (string,optional) - Type the ZIP Code or postal code for the billing address.
    - :datedelivered: (DateTime,optional) - Enter the date when the products included in the invoice were delivered.
    - :description: (string,optional) - Type additional information to describe the invoice, such as shipping details or product substitutions.
    - :duedate: (DateTime,optional) - Enter the date by which the invoice should be paid by the customer.
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :freightamount: (Integer,optional) - Type the cost of freight or shipping for the products included in the invoice for use in calculating the total amount due.
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :discountpercentage: (Float,optional) - Type the discount rate that should be applied to the Detail Amount field, for use in calculating the Pre-Freight Amount and Total Amount values for the invoice.
    - :discountamount: (Integer,optional) - Type the discount amount for the invoice if the customer is eligible for special savings.
    - :invoicenumber: (string,optional) - Shows the identifying number or code of the invoice.
    - :lastonholdtime: (DateTime,optional) - Contains the date time stamp of the last on hold time.
    - :lastbackofficesubmit: (DateTime,optional) - Enter the date and time when the invoice was last submitted to an accounting or ERP system for processing.
    - :opportunityid: (string,optional) - Choose the opportunity that the invoice is related to for reporting and analytics.
    - :salesorderid: (string,optional) - Choose the order related to the invoice to make sure the order is fulfilled and invoiced correctly.
    - :paymenttermscode: (Integer,optional) - Select the payment terms to indicate when the customer needs to pay the total amount.

        **Default Options Values:**
            1. Net 30
            2. 2% 10, Net 30
            3. Net 45
            4. Net 60
    - :pricingerrorcode: (Integer,optional) - Type of pricing error for the invoice.

        **Default Options Values:**
            0. None
            1. Detail Error
            2. Missing Price Level
            3. Inactive Price Level
            4. Missing Quantity
            5. Missing Unit Price
            6. Missing Product
            7. Invalid Product
            8. Missing Pricing Code
            9. Invalid Pricing Code
            10. Missing UOM
            11. Product Not In Price Level
            12. Missing Price Level Amount
            13. Missing Price Level Percentage
            14. Missing Price
            15. Missing Current Cost
            16. Missing Standard Cost
            17. Invalid Price Level Amount
            18. Invalid Price Level Percentage
            19. Invalid Price
            20. Invalid Current Cost
            21. Invalid Standard Cost
            22. Invalid Rounding Policy
            23. Invalid Rounding Option
            24. Invalid Rounding Amount
            25. Price Calculation Error
            26. Invalid Discount Type
            27. Discount Type Invalid State
            28. Invalid Discount
            29. Invalid Quantity
            30. Invalid Pricing Precision
            31. Missing Product Default UOM
            32. Missing Product UOM Schedule
            33. Inactive Discount Type
            34. Invalid Price Level Currency
            35. Price Attribute Out Of Range
            36. Base Currency Attribute Overflow
            37. Base Currency Attribute Underflow
            38. Transaction currency is not set for the product price list item
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
            1. Default Value
    - :overriddencreatedon: (string,optional) - Date and time that the record was migrated.
    - :willcall: (Boolean,optional) - Select whether the products included in the invoice should be shipped to the specified address or held until the customer calls with further pick up or delivery instructions.DefaultValue: false
    - :shipto_city: (string,optional) - Type the city for the customer's shipping address.
    - :shipto_country: (string,optional) - Type the country or region for the customer's shipping address.
    - :shipto_fax: (string,optional) - Type the fax number for the customer's shipping address.
    - :shipto_freighttermscode: (Integer,optional) - Select the freight terms to make sure shipping orders are processed correctly.

        **Default Options Values:**
            1. Default Value
    - :shipto_name: (string,optional) - Type a name for the customer's shipping address, such as "Headquarters" or "Field office", to identify the address.
    - :shipto_telephone: (string,optional) - Type the phone number for the customer's shipping address.
    - :shipto_stateorprovince: (string,optional) - Type the state or province for the shipping address.
    - :shipto_line1: (string,optional) - Type the first line of the customer's shipping address.
    - :shipto_line2: (string,optional) - Type the second line of the customer's shipping address.
    - :shipto_line3: (string,optional) - Type the third line of the shipping address.
    - :shipto_postalcode: (string,optional) - Type the ZIP Code or postal code for the shipping address.
    - :shippingmethodcode: (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
            1. Airborne
            2. DHL
            3. FedEx
            4. UPS
            5. Postal Mail
            6. Full Load
            7. Will Call
    - :skippricecalculation: (Integer,optional) - Skip Price Calculation (For Internal Use)

        **Default Options Values:**
            0. DoPriceCalcAlways
            1. SkipPriceCalcOnRetrieve

    - :statuscode: (Integer,optional) - Select the invoice's status.

        **Default Options Values:**
            - 1: New
            - 2: Partially Shipped
            - 4: Billed
            - 5: Booked (applies to services)
            - 6: Installed (applies to services)

    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
      (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the newly created invoice record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "transactioncurrencyid" in params and "name" in params and "pricelevelid" in params:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/invoices"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "opportunityid" in params:
                data['opportunityid@odata.bind'] = f"/opportunities({params['opportunityid']})"
            if "salesorderid" in params:
                data['salesorderid@odata.bind'] = f"/salesorders({params['salesorderid']})"
            if "pricelevelid" in params:
                data['pricelevelid@odata.bind'] = f"/pricelevels({params['pricelevelid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid","pricelevelid", "opportunityid", "salesorderid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_invoice(accessToken, cred, params):
    """
    Updates a specific invoice record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :invoiceid: (string,required) - The unique identifier of the invoice to be updated.
    - :name: (string,optional) - Type a descriptive name for the invoice.
    - :pricelevelid: (string,optional) - Choose the price list associated with this record to make sure the products associated with the campaign are offered at the correct prices.
    - :billto_city: (string,optional) - Type the city for the customer's billing address.
    - :billto_country: (string,optional) - Type the country or region for the customer's billing address.
    - :billto_fax: (string,optional) - Type the fax number for the customer's billing address.
    - :billto_name: (string,optional) - Type a name for the customer's billing address, such as "Headquarters" or "Field office", to identify the address.
    - :billto_telephone: (string,optional) - Type the phone number for the customer's billing address.
    - :billto_stateorprovince: (string,optional) - Type the state or province for the billing address.
    - :billto_line1: (string,optional) - Type the first line of the customer's billing address.
    - :billto_line2: (string,optional) - Type the second line of the customer's billing address.
    - :billto_line3: (string,optional) - Type the third line of the billing address.
    - :billto_postalcode: (string,optional) - Type the ZIP Code or postal code for the billing address.
    - :datedelivered: (DateTime,optional) - Enter the date when the products included in the invoice were delivered.
    - :description: (string,optional) - Type additional information to describe the invoice, such as shipping details or product substitutions.
    - :duedate: (DateTime,optional) - Enter the date by which the invoice should be paid by the customer.
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :freightamount: (Integer,optional) - Type the cost of freight or shipping for the products included in the invoice for use in calculating the total amount due.
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :discountpercentage: (Float,optional) - Type the discount rate that should be applied to the Detail Amount field, for use in calculating the Pre-Freight Amount and Total Amount values for the invoice.
    - :discountamount: (Integer,optional) - Type the discount amount for the invoice if the customer is eligible for special savings.
    - :invoicenumber: (string,optional) - Shows the identifying number or code of the invoice.
    - :lastonholdtime: (DateTime,optional) - Contains the date time stamp of the last on hold time.
    - :lastbackofficesubmit: (DateTime,optional) - Enter the date and time when the invoice was last submitted to an accounting or ERP system for processing.
    - :opportunityid: (string,optional) - Choose the opportunity that the invoice is related to for reporting and analytics.
    - :salesorderid: (string,optional) - Choose the order related to the invoice to make sure the order is fulfilled and invoiced correctly.
    - :paymenttermscode: (Integer,optional) - Select the payment terms to indicate when the customer needs to pay the total amount.

        **Default Options Values:**
            1. Net 30
            2. 2% 10, Net 30
            3. Net 45
            4. Net 60
    - :pricingerrorcode: (Integer,optional) - Type of pricing error for the invoice.

        **Default Options Values:**
            0. None
            1. Detail Error
            2. Missing Price Level
            3. Inactive Price Level
            4. Missing Quantity
            5. Missing Unit Price
            6. Missing Product
            7. Invalid Product
            8. Missing Pricing Code
            9. Invalid Pricing Code
            10. Missing UOM
            11. Product Not In Price Level
            12. Missing Price Level Amount
            13. Missing Price Level Percentage
            14. Missing Price
            15. Missing Current Cost
            16. Missing Standard Cost
            17. Invalid Price Level Amount
            18. Invalid Price Level Percentage
            19. Invalid Price
            20. Invalid Current Cost
            21. Invalid Standard Cost
            22. Invalid Rounding Policy
            23. Invalid Rounding Option
            24. Invalid Rounding Amount
            25. Price Calculation Error
            26. Invalid Discount Type
            27. Discount Type Invalid State
            28. Invalid Discount
            29. Invalid Quantity
            30. Invalid Pricing Precision
            31. Missing Product Default UOM
            32. Missing Product UOM Schedule
            33. Inactive Discount Type
            34. Invalid Price Level Currency
            35. Price Attribute Out Of Range
            36. Base Currency Attribute Overflow
            37. Base Currency Attribute Underflow
            38. Transaction currency is not set for the product price list item
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
            1. Default Value
    - :overriddencreatedon: (string,optional) - Date and time that the record was migrated.
    - :willcall: (Boolean,optional) - Select whether the products included in the invoice should be shipped to the specified address or held until the customer calls with further pick up or delivery instructions.DefaultValue: false
    - :shipto_city: (string,optional) - Type the city for the customer's shipping address.
    - :shipto_country: (string,optional) - Type the country or region for the customer's shipping address.
    - :shipto_fax: (string,optional) - Type the fax number for the customer's shipping address.
    - :shipto_freighttermscode: (Integer,optional) - Select the freight terms to make sure shipping orders are processed correctly.

        **Default Options Values:**
            1. Default Value
    - :shipto_name: (string,optional) - Type a name for the customer's shipping address, such as "Headquarters" or "Field office", to identify the address.
    - :shipto_telephone: (string,optional) - Type the phone number for the customer's shipping address.
    - :shipto_stateorprovince: (string,optional) - Type the state or province for the shipping address.
    - :shipto_line1: (string,optional) - Type the first line of the customer's shipping address.
    - :shipto_line2: (string,optional) - Type the second line of the customer's shipping address.
    - :shipto_line3: (string,optional) - Type the third line of the shipping address.
    - :shipto_postalcode: (string,optional) - Type the ZIP Code or postal code for the shipping address.
    - :shippingmethodcode: (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
            1. Airborne
            2. DHL
            3. FedEx
            4. UPS
            5. Postal Mail
            6. Full Load
            7. Will Call
    - :skippricecalculation: (Integer,optional) - Skip Price Calculation (For Internal Use)

        **Default Options Values:**
            0. DoPriceCalcAlways
            1. SkipPriceCalcOnRetrieve
    - :statuscode: (Integer,optional) - Select the invoice's status.

        **Default Options Values:**
            - 1: New
            - 2: Partially Shipped
            - 4: Billed
            - 5: Booked (applies to services)
            - 6: Installed (applies to services)

    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
      (Integer,optional) - Time zone code that was in use when the record was created.
    Returns:
        dict: A dictionary containing detailed information about the updated invoice record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "invoiceid" in params:
            domain = creds["domain"]
            invoiceid = params["invoiceid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/invoices({invoiceid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "opportunityid" in params:
                data['opportunityid@odata.bind'] = f"/opportunities({params['opportunityid']})"
            if "salesorderid" in params:
                data['salesorderid@odata.bind'] = f"/salesorders({params['salesorderid']})"
            if "pricelevelid" in params:
                data['pricelevelid@odata.bind'] = f"/pricelevels({params['pricelevelid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid","pricelevelid", "opportunityid", "salesorderid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_invoice(accessToken, cred, params):
    """
    Deletes a specific invoice record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :invoiceid: (string,required) - The unique identifier of the invoice to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the invoice was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "invoiceid" in params:
            domain = creds["domain"]
            invoiceid = params["invoiceid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/invoices({invoiceid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Invoice deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Leads ####################################################

def microsoft_dynamics_crm_get_many_lead(accessToken, cred):
    """
    Fetches multiple lead records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of lead records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/leads"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_lead(accessToken, cred, params):
    """
    Fetches a specific lead record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :leadid: (string,required) - The unique identifier of the lead to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific lead record.
    """
    try:
        creds = json.loads(cred)
        if "leadid" in params and "domain" in creds:
            domain = creds["domain"]
            leadid = params["leadid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/leads({leadid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_lead(accessToken, cred, params):
    """
    Creates a new lead record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :firstname: (string,required) - Type the first name of the primary contact for the lead to make sure the prospect is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastname: (string,required) - Type the last name of the primary contact for the lead to make sure the prospect is addressed correctly in sales calls, email, and marketing campaigns.
    - :subject: (string,required) - Type a subject or descriptive name, such as the expected order, company name, or marketing source list, to identify the lead.
    - :address1_addresstypecode: (Integer,optional) - Select the primary address type.

        **Default Options Values:**
        1. Default Value
    - :address1_county: (string,optional) - Type the county for the primary address.
    - :address1_fax: (string,optional) - Type the fax number associated with the primary address.
    - :address1_latitude: (Double,optional) - Type the latitude value for the primary address for use in mapping and other applications.
    - :address1_longitude: (Double,optional) - Type the longitude value for the primary address for use in mapping and other applications.
    - :address1_name: (string,optional) - Type a descriptive name for the primary address, such as Corporate Headquarters.
    - :address1_postofficebox: (string,optional) - Type the post office box number of the primary address.
    - :address1_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
        1. Default Value
    - :address1_telephone1: (string,optional) - Type the main phone number associated with the primary address.
    - :address1_telephone2: (string,optional) - Type a second phone number associated with the primary address.
    - :address1_telephone3: (string,optional) - Type a third phone number associated with the primary address.
    - :address1_upszone: (string,optional) - Type the UPS zone of the primary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address1_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.
    - :address2_addresstypecode: (Integer,optional) - Select the secondary address type.

        **Default Options Values:**
        1. Default Value
    - :address2_city: (string,optional) - Type the city for the secondary address.
    - :address2_country: (string,optional) - Type the country or region for the secondary address.
    - :address2_county: (string,optional) - Type the county for the secondary address.
    - :address2_fax: (string,optional) - Type the fax number associated with the secondary address.
    - :address2_latitude: (Double,optional) - Type the latitude value for the secondary address for use in mapping and other applications.
    - :address2_longitude: (Double,optional) - Type the longitude value for the secondary address for use in mapping and other applications.
    - :address2_name: (string,optional) - Type a descriptive name for the secondary address, such as Corporate Headquarters.
    - :address2_postofficebox: (string,optional) - Type the post office box number of the secondary address.
    - :address2_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
        1. Default Value
    - :address2_stateorprovince:
    (string,optional) - Type the state or province of the secondary address.

    - :address2_line1: (string,optional) - Type the first line of the secondary address.
    - :address2_line2: (string,optional) - Type the second line of the secondary address.
    - :address2_line3: (string,optional) - Type the third line of the secondary address.
    - :address2_telephone1: (string,optional) - Type the main phone number associated with the secondary address.
    - :address2_telephone2: (string,optional) - Type a second phone number associated with the secondary address.
    - :address2_telephone3: (string,optional) - Type a third phone number associated with the secondary address.
    - :address2_upszone: (string,optional) - Type the UPS zone of the secondary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address2_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address2_postalcode: (string,optional) - Type the ZIP Code or postal code for the secondary address.
    - :revenue: (float,optional) - Type the annual revenue of the company associated with the lead to provide an understanding of the prospect's business.
    - :msdyn_salesassignmentresult: (Boolean,optional) - Result of the assignment rule process
    - :budgetstatus: (Integer,optional) - Information about the budget status of the lead's company or organization.

        **Default Options Values:**
            0. No Committed Budget
            1. May Buy
            2. Can Buy
            3. Will Buy
    - :budgetamount: (Integer,optional) - Information about the budget amount of the lead's company or organization.
    - :businesscard: (Integer,optional) - Stores Image of the Business Card
    - :telephone1: (string,optional) - Type the work phone number for the primary contact for the lead.
    - :businesscardattributes: (string,optional) - Stores Business Card Control Properties.
    - :address1_city: (string,optional) - Type the city for the primary address.
    - :companyname: (string,optional) - Type the name of the company associated with the lead. This becomes the account name when the lead is qualified and converted to a customer account.
    - :confirminterest: (Boolean,optional) - Select whether the lead confirmed interest in your offerings. This helps in determining the lead quality.DefaultValue: false
    - :address1_country: (string,optional) - Type the country or region for the primary address.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :decisionmaker: (Boolean,optional) - Select whether your notes include information about who makes the purchase decisions at the lead's company.DefaultValue: false
    - :description: (string,optional) - Type additional information to describe the lead, such as an excerpt from the company's website.
    - :donotbulkemail: (Boolean,optional) - Select whether the lead accepts bulk email sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the lead can be added to marketing lists, but will be excluded from the email.DefaultValue: false
    - :donotemail: (Boolean,optional) - Select whether the lead allows direct email sent from Microsoft Dynamics 365.DefaultValue: false
    - :donotfax: (Boolean,optional) - Select whether the lead allows faxes.DefaultValue: false
    - :donotpostalmail: (Boolean,optional) - Select whether the lead allows direct mail.DefaultValue: false
    - :donotphone: (Boolean,optional) - Select whether the lead allows phone calls.DefaultValue: false
    - :emailaddress1: (string,optional) - Type the primary email address for the lead.
    - :emailaddress2: (string,optional) - Type the secondary email address for the lead.
    - :emailaddress3: (string,optional) - Type an alternate email address for the lead.
    - :estimatedclosedate: (Date,optional) - Enter the expected close date for the lead, so that the sales team can schedule timely follow-up meetings to move the prospect to the next sales stage.
    - :estimatedamount: (Integer,optional) - Type the estimated revenue value that this lead will generate to assist in sales forecasting and planning.
    - :evaluatefit: (Boolean,optional) - Select whether the fit between the lead's requirements and your offerings was evaluated.DefaultValue: false
    - :fax: (string,optional) - Type the fax number for the primary contact for the lead.
    - :followemail: (Boolean,optional) - Information about whether to allow following email activity like opens, attachment views and link clicks for emails sent to the lead.DefaultValue: true
    - :msdyn_gdproptout: (Boolean,optional) - Describes whether lead is opted out or not.DefaultValue: false
    - :telephone2: (string,optional) - Type the home phone number for the primary contact for the lead.
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :industrycode: (Integer,optional) - Select the primary industry in which the lead's business is focused, for use in marketing segmentation and demographic analysis.

        **Default Options Values:**
            1. Accounting
            2. Agriculture and Non-petrol Natural Resource Extraction
            3. Broadcasting Printing and Publishing
            4. Brokers
            5. Building Supply Retail
            6. Business Services
            7. Consulting
            8. Consumer Services
            9. Design, Direction and Creative Management
            10. Distributors, Dispatchers and Processors
            11. Doctor's Offices and Clinics
            12. Durable Manufacturing
            13. Eating and Drinking Places
            14. Entertainment Retail
            15. Equipment Rental and Leasing
            16. Financial
            17. Food and Tobacco Processing
            18. Inbound Capital Intensive Processing
            19. Inbound Repair and Services
            20. Insurance
            21. Legal Services
            22. Non-Durable Merchandise Retail
            23. Outbound Consumer Service
            24. Petrochemical Extraction and Distribution
            25. Service Retail
            26. SIG Affiliations
            27. Social Services
            28. Special Outbound Trade Contractors
            29. Specialty Realty
            30. Transportation
            31. Utility Creation and Distribution
            32. Vehicle Retail
            33. Wholesale
    - :initialcommunication: (Boolean,optional) - Choose whether someone from the sales team contacted this lead earlier.
    - :jobtitle: (string,optional) - Type the job title of the primary contact for this lead to make sure the prospect is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastonholdtime: (DateAndTime,optional) - Contains the date and time stamp of the last on hold time.
    - :leadsourcecode: (Integer,optional) - Select the primary marketing source that prompted the lead to contact you.

        **Default Options Values:**
            1. Advertisement
            2. Employee Referral
            3. External Referral
            4. Partner
            5. Public Relations
            6. Seminar
            7. Trade Show
            8. Web
            9. Word of Mouth
            10. Other
    - :donotsendmm: (Boolean,optional) - Select whether the lead accepts marketing materials, such as brochures or catalogs. Leads that opt out can be excluded from marketing initiatives.DefaultValue: false
    - :middlename: (string,optional) - Type the middle name or initial of the primary contact for the lead to make sure the prospect is addressed correctly.
    - :mobilephone: (string,optional) - Type the mobile phone number for the primary contact for the lead.
    - :need: (Integer,optional) - Choose how high the level of need is for the lead's company.

        **Default Options Values:**
            0. Must have
            1. Should have
            2. Good to have
            3. No need
    - :numberofemployees: (Integer,optional) - Type the number of employees that work at the company associated with the lead, for use in marketing segmentation and demographic analysis.
    - :telephone3: (string,optional) - Type an alternate phone number for the primary contact for the lead.
    - :pager: (string,optional) - Type the pager number for the primary contact for the lead.
    - :parentaccountid: (string,optional) - Choose an account to connect this lead to, so that the relationship is visible in reports and analytics.
    - :parentcontactid: (string,optional) - Choose a contact to connect this lead to, so that the relationship is visible in reports and analytics.
    - :participatesinworkflow: (Boolean,optional) - Shows whether the lead participates in workflow rules.DefaultValue: false
    - :preferredcontactmethodcode: (Integer,optional) - Select the preferred method of contact.

        **Default Options Values:**
            1. Any
            2. Email
            3. Phone
            4. Fax
            5. Mail
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
        1. Default Value
    - :purchaseprocess: (Integer,optional) - Choose whether an individual or a committee will be involved in the purchase process for the lead.

        **Default Options Values:**
            0. Individual
            1. Committee
            2. Unknown
    - :purchasetimeframe: (Integer,optional) - Choose how long the lead will likely take to make the purchase, so the sales team will be aware.

        **Default Options Values:**
            0. Immediate
            1. This Quarter
            2. Next Quarter
            3. This Year
            4. Unknown
    - :qualificationcomments: (string,optional) - Type comments about the qualification or scoring of the lead.
    - :qualifyingopportunityids: (string,optional) - Choose the opportunity that the lead was qualified on and then converted to.
    - :leadqualitycode: (Integer,optional) - Select a rating value to indicate the lead's potential to become a customer.

        **Default Options Values:**
            1. Hot
            2. Warm
            3. Cold
    - :overriddencreatedon: (string,optional) - Date and time that the record was migrated.
    - :relatedobjectid: (string,optional) - Related Campaign Response.
    - :salesstage: (Integer,optional) - Select the sales stage of this lead to aid the sales team in their efforts to convert this lead to an opportunity.

        **Default Options Values:**
            1. Qualify
    - :salesstagecode: (Integer,optional) - Select the sales process stage for the lead to help determine the probability of the lead converting to an opportunity.

        **Default Options Values:**
            1. Default Value
    - :salutation: (string,optional) - Type the salutation of the primary contact for this lead to make sure the prospect is addressed correctly in sales calls, email messages, and marketing campaigns.
    - :schedulefollowup_prospect: (DateTime,optional) - Enter the date and time of the prospecting follow-up meeting with the lead.
    - :schedulefollowup_qualify:
    (DateTime,optional) - Enter the date and time of the qualifying follow-up meeting with the lead.

    - :sic: (string,optional) - Type the Standard Industrial Classification (SIC) code that indicates the lead's primary industry of business for use in marketing segmentation and demographic analysis.
    - :campaignid: (string,optional) - Choose the campaign that the lead was generated from to track the effectiveness of marketing campaigns and identify communications received by the lead.
    - :address1_stateorprovince: (string,optional) - Type the state or province of the primary address.
    - :statuscode: (Integer,optional) - Select the lead's status.

        **Default Options Values:**
            1. New
            2. Contacted
            3. Qualified
            4. Lost
            5. Cannot Contact
            6. No Longer Interested
            7. Canceled
    - :address1_line1: (string,optional) - Type the first line of the primary address.
    - :address1_line2: (string,optional) - Type the second line of the primary address.
    - :address1_line3: (string,optional) - Type the third line of the primary address.
    - :teamsfollowed: (Integer,optional) - Number of users or conversations followed the record
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :websiteurl: (string,optional) - Type the website URL for the company associated with this lead.
    - :yomicompanyname: (string,optional) - Type the phonetic spelling of the lead's company name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :yomifirstname: (string,optional) - Type the phonetic spelling of the lead's first name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :yomilastname: (string,optional) - Type the phonetic spelling of the lead's last name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :yomimiddlename: (string,optional) - Type the phonetic spelling of the lead's middle name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.

    Returns:
        dict: A dictionary containing detailed information about the newly created lead record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "firstname" in params and "lastname" in params and "subject" in params:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/leads"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "parentaccountid" in params:
                data['parentaccountid@odata.bind'] = f"/accounts({params['parentaccountid']})"
            if "parentcontactid" in params:
                data['parentcontactid@odata.bind'] = f"/contacts({params['parentcontactid']})"
            if "relatedobjectid" in params:
                data['relatedobjectid@odata.bind'] = f"/campaignresponses({params['relatedobjectid']})"
            if "campaignid" in params:
                data['campaignid@odata.bind'] = f"/campaigns({params['campaignid']})"
            if "qualifyingopportunityid" in params:
                data['qualifyingopportunityid@odata.bind'] = f"/opportunities({params['qualifyingopportunityid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid","parentaccountid","parentcontactid","relatedobjectid","campaignid","qualifyingopportunityid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_lead(accessToken, cred, params):
    """
    Updates a specific lead record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :leadid: (string,required) - The unique identifier of the lead to be updated.
    - :firstname: (string,optional) - Type the first name of the primary contact for the lead to make sure the prospect is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastname: (string,optional) - Type the last name of the primary contact for the lead to make sure the prospect is addressed correctly in sales calls, email, and marketing campaigns.
    - :subject: (string,optional) - Type a subject or descriptive name, such as the expected order, company name, or marketing source list, to identify the lead.
    - :address1_addresstypecode: (Integer,optional) - Select the primary address type.

        **Default Options Values:**
        1. Default Value
    - :address1_county: (string,optional) - Type the county for the primary address.
    - :address1_fax: (string,optional) - Type the fax number associated with the primary address.
    - :address1_latitude: (Double,optional) - Type the latitude value for the primary address for use in mapping and other applications.
    - :address1_longitude: (Double,optional) - Type the longitude value for the primary address for use in mapping and other applications.
    - :address1_name: (string,optional) - Type a descriptive name for the primary address, such as Corporate Headquarters.
    - :address1_postofficebox: (string,optional) - Type the post office box number of the primary address.
    - :address1_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
        1. Default Value
    - :address1_telephone1: (string,optional) - Type the main phone number associated with the primary address.
    - :address1_telephone2: (string,optional) - Type a second phone number associated with the primary address.
    - :address1_telephone3: (string,optional) - Type a third phone number associated with the primary address.
    - :address1_upszone: (string,optional) - Type the UPS zone of the primary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address1_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.
    - :address2_addresstypecode: (Integer,optional) - Select the secondary address type.

        **Default Options Values:**
        1. Default Value
    - :address2_city: (string,optional) - Type the city for the secondary address.
    - :address2_country: (string,optional) - Type the country or region for the secondary address.
    - :address2_county: (string,optional) - Type the county for the secondary address.
    - :address2_fax: (string,optional) - Type the fax number associated with the secondary address.
    - :address2_latitude: (Double,optional) - Type the latitude value for the secondary address for use in mapping and other applications.
    - :address2_longitude: (Double,optional) - Type the longitude value for the secondary address for use in mapping and other applications.
    - :address2_name: (string,optional) - Type a descriptive name for the secondary address, such as Corporate Headquarters.
    - :address2_postofficebox: (string,optional) - Type the post office box number of the secondary address.
    - :address2_shippingmethodcode:
    (Integer,optional) - Select a shipping method for deliveries sent to this address.

        **Default Options Values:**
        1. Default Value
    - :address2_stateorprovince:
    (string,optional) - Type the state or province of the secondary address.

    - :address2_line1: (string,optional) - Type the first line of the secondary address.
    - :address2_line2: (string,optional) - Type the second line of the secondary address.
    - :address2_line3: (string,optional) - Type the third line of the secondary address.
    - :address2_telephone1: (string,optional) - Type the main phone number associated with the secondary address.
    - :address2_telephone2: (string,optional) - Type a second phone number associated with the secondary address.
    - :address2_telephone3: (string,optional) - Type a third phone number associated with the secondary address.
    - :address2_upszone: (string,optional) - Type the UPS zone of the secondary address to make sure shipping charges are calculated correctly and deliveries are made promptly, if shipped by UPS.
    - :address2_utcoffset: (Integer,optional) - Select the time zone, or UTC offset, for this address so that other people can reference it when they contact someone at this address.
    - :address2_postalcode: (string,optional) - Type the ZIP Code or postal code for the secondary address.
    - :revenue: (float,optional) - Type the annual revenue of the company associated with the lead to provide an understanding of the prospect's business.
    - :msdyn_salesassignmentresult: (Boolean,optional) - Result of the assignment rule process
    - :budgetstatus: (Integer,optional) - Information about the budget status of the lead's company or organization.

        **Default Options Values:**
            0. No Committed Budget
            1. May Buy
            2. Can Buy
            3. Will Buy
    - :budgetamount: (Integer,optional) - Information about the budget amount of the lead's company or organization.
    - :businesscard: (Integer,optional) - Stores Image of the Business Card
    - :telephone1: (string,optional) - Type the work phone number for the primary contact for the lead.
    - :businesscardattributes: (string,optional) - Stores Business Card Control Properties.
    - :address1_city: (string,optional) - Type the city for the primary address.
    - :companyname: (string,optional) - Type the name of the company associated with the lead. This becomes the account name when the lead is qualified and converted to a customer account.
    - :confirminterest: (Boolean,optional) - Select whether the lead confirmed interest in your offerings. This helps in determining the lead quality.DefaultValue: false
    - :address1_country: (string,optional) - Type the country or region for the primary address.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :decisionmaker: (Boolean,optional) - Select whether your notes include information about who makes the purchase decisions at the lead's company.DefaultValue: false
    - :description: (string,optional) - Type additional information to describe the lead, such as an excerpt from the company's website.
    - :donotbulkemail: (Boolean,optional) - Select whether the lead accepts bulk email sent through marketing campaigns or quick campaigns. If Do Not Allow is selected, the lead can be added to marketing lists, but will be excluded from the email.DefaultValue: false
    - :donotemail: (Boolean,optional) - Select whether the lead allows direct email sent from Microsoft Dynamics 365.DefaultValue: false
    - :donotfax: (Boolean,optional) - Select whether the lead allows faxes.DefaultValue: false
    - :donotpostalmail: (Boolean,optional) - Select whether the lead allows direct mail.DefaultValue: false
    - :donotphone: (Boolean,optional) - Select whether the lead allows phone calls.DefaultValue: false
    - :emailaddress1: (string,optional) - Type the primary email address for the lead.
    - :emailaddress2: (string,optional) - Type the secondary email address for the lead.
    - :emailaddress3: (string,optional) - Type an alternate email address for the lead.
    - :estimatedclosedate: (Date,optional) - Enter the expected close date for the lead, so that the sales team can schedule timely follow-up meetings to move the prospect to the next sales stage.
    - :estimatedamount: (Integer,optional) - Type the estimated revenue value that this lead will generate to assist in sales forecasting and planning.
    - :evaluatefit: (Boolean,optional) - Select whether the fit between the lead's requirements and your offerings was evaluated.DefaultValue: false
    - :fax: (string,optional) - Type the fax number for the primary contact for the lead.
    - :followemail: (Boolean,optional) - Information about whether to allow following email activity like opens, attachment views and link clicks for emails sent to the lead.DefaultValue: true
    - :msdyn_gdproptout: (Boolean,optional) - Describes whether lead is opted out or not.DefaultValue: false
    - :telephone2: (string,optional) - Type the home phone number for the primary contact for the lead.
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :industrycode: (Integer,optional) - Select the primary industry in which the lead's business is focused, for use in marketing segmentation and demographic analysis.

        **Default Options Values:**
            1. Accounting
            2. Agriculture and Non-petrol Natural Resource Extraction
            3. Broadcasting Printing and Publishing
            4. Brokers
            5. Building Supply Retail
            6. Business Services
            7. Consulting
            8. Consumer Services
            9. Design, Direction and Creative Management
            10. Distributors, Dispatchers and Processors
            11. Doctor's Offices and Clinics
            12. Durable Manufacturing
            13. Eating and Drinking Places
            14. Entertainment Retail
            15. Equipment Rental and Leasing
            16. Financial
            17. Food and Tobacco Processing
            18. Inbound Capital Intensive Processing
            19. Inbound Repair and Services
            20. Insurance
            21. Legal Services
            22. Non-Durable Merchandise Retail
            23. Outbound Consumer Service
            24. Petrochemical Extraction and Distribution
            25. Service Retail
            26. SIG Affiliations
            27. Social Services
            28. Special Outbound Trade Contractors
            29. Specialty Realty
            30. Transportation
            31. Utility Creation and Distribution
            32. Vehicle Retail
            33. Wholesale
    - :initialcommunication: (Boolean,optional) - Choose whether someone from the sales team contacted this lead earlier.
    - :jobtitle: (string,optional) - Type the job title of the primary contact for this lead to make sure the prospect is addressed correctly in sales calls, email, and marketing campaigns.
    - :lastonholdtime: (DateAndTime,optional) - Contains the date and time stamp of the last on hold time.
    - :leadsourcecode: (Integer,optional) - Select the primary marketing source that prompted the lead to contact you.

        **Default Options Values:**
            1. Advertisement
            2. Employee Referral
            3. External Referral
            4. Partner
            5. Public Relations
            6. Seminar
            7. Trade Show
            8. Web
            9. Word of Mouth
            10. Other
    - :donotsendmm: (Boolean,optional) - Select whether the lead accepts marketing materials, such as brochures or catalogs. Leads that opt out can be excluded from marketing initiatives.DefaultValue: false
    - :middlename: (string,optional) - Type the middle name or initial of the primary contact for the lead to make sure the prospect is addressed correctly.
    - :mobilephone: (string,optional) - Type the mobile phone number for the primary contact for the lead.
    - :need: (Integer,optional) - Choose how high the level of need is for the lead's company.

        **Default Options Values:**
            0. Must have
            1. Should have
            2. Good to have
            3. No need
    - :numberofemployees: (Integer,optional) - Type the number of employees that work at the company associated with the lead, for use in marketing segmentation and demographic analysis.
    - :telephone3: (string,optional) - Type an alternate phone number for the primary contact for the lead.
    - :pager: (string,optional) - Type the pager number for the primary contact for the lead.
    - :parentaccountid: (string,optional) - Choose an account to connect this lead to, so that the relationship is visible in reports and analytics.
    - :parentcontactid: (string,optional) - Choose a contact to connect this lead to, so that the relationship is visible in reports and analytics.
    - :participatesinworkflow: (Boolean,optional) - Shows whether the lead participates in workflow rules.DefaultValue: false
    - :preferredcontactmethodcode: (Integer,optional) - Select the preferred method of contact.

        **Default Options Values:**
            1. Any
            2. Email
            3. Phone
            4. Fax
            5. Mail
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
        1. Default Value
    - :purchaseprocess: (Integer,optional) - Choose whether an individual or a committee will be involved in the purchase process for the lead.

        **Default Options Values:**
            0. Individual
            1. Committee
            2. Unknown
    - :purchasetimeframe: (Integer,optional) - Choose how long the lead will likely take to make the purchase, so the sales team will be aware.

        **Default Options Values:**
            0. Immediate
            1. This Quarter
            2. Next Quarter
            3. This Year
            4. Unknown
    - :qualificationcomments: (string,optional) - Type comments about the qualification or scoring of the lead.
    - :qualifyingopportunityids: (string,optional) - Choose the opportunity that the lead was qualified on and then converted to.
    - :leadqualitycode: (Integer,optional) - Select a rating value to indicate the lead's potential to become a customer.

        **Default Options Values:**
            1. Hot
            2. Warm
            3. Cold
    - :overriddencreatedon: (string,optional) - Date and time that the record was migrated.
    - :relatedobjectid: (string,optional) - Related Campaign Response.
    - :salesstage: (Integer,optional) - Select the sales stage of this lead to aid the sales team in their efforts to convert this lead to an opportunity.

        **Default Options Values:**
            1. Qualify
    - :salesstagecode: (Integer,optional) - Select the sales process stage for the lead to help determine the probability of the lead converting to an opportunity.

        **Default Options Values:**
            1. Default Value
    - :salutation: (string,optional) - Type the salutation of the primary contact for this lead to make sure the prospect is addressed correctly in sales calls, email messages, and marketing campaigns.
    - :schedulefollowup_prospect: (DateTime,optional) - Enter the date and time of the prospecting follow-up meeting with the lead.
    - :schedulefollowup_qualify:
    (DateTime,optional) - Enter the date and time of the qualifying follow-up meeting with the lead.

    - :sic: (string,optional) - Type the Standard Industrial Classification (SIC) code that indicates the lead's primary industry of business for use in marketing segmentation and demographic analysis.
    - :campaignid: (string,optional) - Choose the campaign that the lead was generated from to track the effectiveness of marketing campaigns and identify communications received by the lead.
    - :address1_stateorprovince: (string,optional) - Type the state or province of the primary address.
    - :statuscode: (Integer,optional) - Select the lead's status.

        **Default Options Values:**
            1. New
            2. Contacted
            3. Qualified
            4. Lost
            5. Cannot Contact
            6. No Longer Interested
            7. Canceled
    - :address1_line1: (string,optional) - Type the first line of the primary address.
    - :address1_line2: (string,optional) - Type the second line of the primary address.
    - :address1_line3: (string,optional) - Type the third line of the primary address.
    - :teamsfollowed: (Integer,optional) - Number of users or conversations followed the record
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    - :websiteurl: (string,optional) - Type the website URL for the company associated with this lead.
    - :yomicompanyname: (string,optional) - Type the phonetic spelling of the lead's company name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :yomifirstname: (string,optional) - Type the phonetic spelling of the lead's first name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :yomilastname: (string,optional) - Type the phonetic spelling of the lead's last name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :yomimiddlename: (string,optional) - Type the phonetic spelling of the lead's middle name, if the name is specified in Japanese, to make sure the name is pronounced correctly in phone calls with the prospect.
    - :address1_postalcode: (string,optional) - Type the ZIP Code or postal code for the primary address.

    Returns:
        dict: A dictionary containing detailed information about the updated lead record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "leadid" in params:
            domain = creds["domain"]
            leadid = params["leadid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/leads({leadid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "parentaccountid" in params:
                data['parentaccountid@odata.bind'] = f"/accounts({params['parentaccountid']})"
            if "parentcontactid" in params:
                data['parentcontactid@odata.bind'] = f"/contacts({params['parentcontactid']})"
            if "relatedobjectid" in params:
                data['relatedobjectid@odata.bind'] = f"/campaignresponses({params['relatedobjectid']})"
            if "campaignid" in params:
                data['campaignid@odata.bind'] = f"/campaigns({params['campaignid']})"
            if "qualifyingopportunityid" in params:
                data['qualifyingopportunityid@odata.bind'] = f"/opportunities({params['qualifyingopportunityid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid","parentaccountid","parentcontactid","relatedobjectid","campaignid","qualifyingopportunityid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_lead(accessToken, cred, params):
    """
    Deletes a specific lead record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :leadid: (string,required) - The unique identifier of the lead to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the lead was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "leadid" in params and "domain" in creds:
            domain = creds["domain"]
            leadid = params["leadid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/leads({leadid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Lead deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Case / Incident ####################################################

def microsoft_dynamics_crm_get_many_incident(accessToken, cred):
    """
    Fetches multiple incident records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of incident records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/incidents"
            headers = {"Authorization": "Bearer " + accessToken}
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_incident(accessToken, cred, params):
    """
    Fetches a specific incident record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :incidentid: (string,required) - The unique identifier of the incident to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific incident record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "incidentid" in params:
            domain = creds["domain"]
            incidentid = params["incidentid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/incidents({incidentid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_incident(accessToken, cred, params):
    """
    Creates a new incident record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :customeridtype: (string,required) - Customer Type ( account or contact )
    - :customerid: (string,required) - Select the customer account or contact to provide a quick link to additional customer details, such as account information, activities, and opportunities.
    - :title: (string,required) - Type a subject or descriptive name, such as the request, issue, or company name, to identify the case in Microsoft Dynamics 365 views.
    - :activitiescomplete: (Boolean,optional) - This attribute is used for Sample Service Business Processes.DefaultValue: false
    - :actualserviceunits: (Integer,optional) - Type the number of service units that were actually required to resolve the case.
    - :billedserviceunits: (Integer,optional) - Type the number of service units that were billed to the customer for the case.
    - :blockedprofile: (Boolean,optional) - Details whether the profile is blocked or not.DefaultValue: false
    - :ticketnumber: (string,optional) - Shows the case number for customer reference and searching capabilities. This cannot be modified.
    - :incidentstagecode: (Integer,optional) - Select the current stage of the service process for the case to assist service team members when they review or transfer a case.

        **Default Options Values:**
        1. Default Value
    - :casetypecode: (Integer,optional) - Select the type of case to identify the incident for use in case routing and analysis.

        **Default Options Values:**
            1. Question
            2. Problem
            3. Request
    - :checkemail: (Boolean,optional) - This attribute is used for Sample Service Business Processes.DefaultValue: false
    - :contractid: (string,optional) - Choose the service contract that the case should be logged under to make sure the customer is eligible for support services.
    - :customercontacted: (Boolean,optional) - Tells whether customer service representative has contacted the customer or not.DefaultValue: false
    - :decremententitlementterm: (Boolean,optional) - Shows whether terms of the associated entitlement should be decremented or not.DefaultValue: true
    - :isdecrementing: (Boolean,optional) - For system use only.DefaultValue: false
    - :description: (string,optional) - Type additional information to describe the case to assist the service team in reaching a resolution.
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :firstresponsesent: (Boolean,optional) - Indicates if the first response has been sent.DefaultValue: false
    - :firstresponseslastatus: (Integer,optional) - Shows the status of the initial response time for the case according to the terms of the SLA.

        **Default Options Values:**
            1. In Progress
            2. Nearing Noncompliance
            3. Succeeded
            4. Noncompliant
    - :followupby: (DateTime,optional) - Enter the date by which a customer service representative has to follow up with the customer on this case.
    - :followuptaskcreated: (Boolean,optional) - This attribute is used for Sample Service Business Processes.DefaultValue: false
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :influencescore: (Double,optional) - Will contain the Influencer score coming from NetBreeze.
    - :isescalated: (Boolean,optional) - Indicates if the case has been escalated.DefaultValue: false
    - :lastonholdtime: (DateTime,optional) - Contains the date time stamp of the last on hold time.
    - :masterid: (string,optional) - Choose the primary case the current case was merged into.
    - :caseorigincode: (Integer,optional) - Select how contact about the case was originated, such as email, phone, or web, for use in reporting and analysis.

        **Default Options Values:**
            - 1: Phone
            - 2: Email
            - 3: Web
            - 2483: Facebook
            - 3986: Twitter
    - :parentcaseid: (string,optional) - Choose the parent case for a case.
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
            1. High
            2. Normal
            3. Low
    - :productid: (string,optional) - Choose the product associated with the case to identify warranty, service, or other product issues and be able to report the number of incidents for each product.
    - :messagetypecode: (Integer,optional) - Shows whether the post originated as a public or private message.

        **Default Options Values:**
            0. Public Message
            1. Private Message
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :resolveby: (DateTime,optional) - Enter the date by when the case must be resolved.
    - :resolvebykpiid: (string,optional) - For internal use only.
    - :resolvebyslastatus: (Integer,optional) - Shows the status of the resolution time for the case according to the terms of the SLA.

        **Default Options Values:**
            1. In Progress
            2. Nearing Noncompliance
            3. Succeeded
            4. Noncompliant
    - :routecase: (Boolean,optional) - Tells whether the incident has been routed to queue or not.DefaultValue: true
    - :customersatisfactioncode:
    (Integer,optional) - Select the customer's level of satisfaction with the handling and resolution of the case.

        **Default Options Values:**
            1. Very Dissatisfied
            2. Dissatisfied
            3. Neutral
            4. Satisfied
            5. Very Satisfied
    - :sentimentvalue: (Double,optional) - Value derived after assessing words commonly associated with a negative, neutral, or positive sentiment that occurs in a social post. Sentiment information can also be reported as numeric values.
    - :productserialnumber: (string,optional) - Type the serial number of the product that is associated with this case, so that the number of cases per product can be reported.
    - :contractservicelevelcode: (Integer,optional) - Select the service level for the case to make sure the case is handled correctly.

        **Default Options Values:**
            1. Gold
            2. Silver
            3. Bronze
    - :servicestage: (Integer,optional) - Select the stage, in the case resolution process, that the case is in.

        **Default Options Values:**
            0. Identify
            1. Research
            2. Resolve
    - :severitycode: (Integer,optional) - Select the severity of this case to indicate the incident's impact on the customer's business.

        **Default Options Values:**
        1. Default Value
    - :socialprofileid: (string,optional) - Unique identifier of the social profile with which the case is associated.
    - :statuscode: (Integer,optional) - Select the case's status.

        **Default Options Values:**
            - 1: In Progress
            - 2: On Hold
            - 3: Waiting for Details
            - 4: Researching

    - :subjectid: (string,optional) - Choose the subject for the case, such as catalog request or product complaint, so customer service managers can identify frequent requests or problem areas. Administrators can configure subjects under Business Management in the Settings area.
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the newly created incident record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "customeridtype" in params and "customerid" in params and "title" in params :
            domain = creds["domain"]
            customerid = params["customerid"]
            customeridtype = params["customeridtype"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/incidents"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            if customeridtype == "contact":
                data = {
                    "customerid_contact@odata.bind": f"/contacts({customerid})"}
            elif customeridtype == "account":
                data = {
                    "customerid_account@odata.bind": f"/accounts({customerid})"}
            else:
                raise Exception(
                    "Invalid customeridtype. Expected 'contact' or 'account'."
                )
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "productid" in params:
                data['productid@odata.bind'] = f"/products({params['productid']})"
            if "resolvebykpiid" in params:
                data['resolvebykpiid@odata.bind'] = f"/slakpiinstances({params['resolvebykpiid']})"
            if "socialprofileid" in params:
                data['socialprofileid@odata.bind'] = f"/socialprofiles({params['socialprofileid']})"
            if "subjectid" in params:
                data['subjectid@odata.bind'] = f"/subjects({params['subjectid']})"
            if "parentcaseid" in params:
                data['parentcaseid@odata.bind'] = f"/incidents({params['parentcaseid']})"
            for key, value in params.items():
                skip_keys = ["customerid", "customeridtype", "transactioncurrencyid","productid", "resolvebykpiid", "socialprofileid", "subjectid","parentcaseid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_incident(accessToken, cred, params):
    """
    Updates a specific incident record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :incidentid: (string,required) - The unique identifier of the incident to be updated.
    - :title: (string,optional) - Type a subject or descriptive name, such as the request, issue, or company name, to identify the case in Microsoft Dynamics 365 views.
    - :activitiescomplete: (Boolean,optional) - This attribute is used for Sample Service Business Processes.DefaultValue: false
    - :actualserviceunits: (Integer,optional) - Type the number of service units that were actually required to resolve the case.
    - :billedserviceunits: (Integer,optional) - Type the number of service units that were billed to the customer for the case.
    - :blockedprofile: (Boolean,optional) - Details whether the profile is blocked or not.DefaultValue: false
    - :ticketnumber: (string,optional) - Shows the case number for customer reference and searching capabilities. This cannot be modified.
    - :incidentstagecode: (Integer,optional) - Select the current stage of the service process for the case to assist service team members when they review or transfer a case.

        **Default Options Values:**
        1. Default Value
    - :casetypecode: (Integer,optional) - Select the type of case to identify the incident for use in case routing and analysis.

        **Default Options Values:**
            1. Question
            2. Problem
            3. Request
    - :checkemail: (Boolean,optional) - This attribute is used for Sample Service Business Processes.DefaultValue: false
    - :contractid: (string,optional) - Choose the service contract that the case should be logged under to make sure the customer is eligible for support services.
    - :customercontacted: (Boolean,optional) - Tells whether customer service representative has contacted the customer or not.DefaultValue: false
    - :decremententitlementterm: (Boolean,optional) - Shows whether terms of the associated entitlement should be decremented or not.DefaultValue: true
    - :isdecrementing: (Boolean,optional) - For system use only.DefaultValue: false
    - :description: (string,optional) - Type additional information to describe the case to assist the service team in reaching a resolution.
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :firstresponsesent: (Boolean,optional) - Indicates if the first response has been sent.DefaultValue: false
    - :firstresponseslastatus: (Integer,optional) - Shows the status of the initial response time for the case according to the terms of the SLA.

        **Default Options Values:**
            1. In Progress
            2. Nearing Noncompliance
            3. Succeeded
            4. Noncompliant
    - :followupby: (DateTime,optional) - Enter the date by which a customer service representative has to follow up with the customer on this case.
    - :followuptaskcreated: (Boolean,optional) - This attribute is used for Sample Service Business Processes.DefaultValue: false
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :influencescore: (Double,optional) - Will contain the Influencer score coming from NetBreeze.
    - :isescalated: (Boolean,optional) - Indicates if the case has been escalated.DefaultValue: false
    - :lastonholdtime: (DateTime,optional) - Contains the date time stamp of the last on hold time.
    - :masterid: (string,optional) - Choose the primary case the current case was merged into.
    - :caseorigincode: (Integer,optional) - Select how contact about the case was originated, such as email, phone, or web, for use in reporting and analysis.

        **Default Options Values:**
            - 1: Phone
            - 2: Email
            - 3: Web
            - 2483: Facebook
            - 3986: Twitter
    - :parentcaseid: (string,optional) - Choose the parent case for a case.
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.

        **Default Options Values:**
            1. High
            2. Normal
            3. Low
    - :productid: (string,optional) - Choose the product associated with the case to identify warranty, service, or other product issues and be able to report the number of incidents for each product.
    - :messagetypecode: (Integer,optional) - Shows whether the post originated as a public or private message.

        **Default Options Values:**
            0. Public Message
            1. Private Message
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :resolveby: (DateTime,optional) - Enter the date by when the case must be resolved.
    - :resolvebykpiid: (string,optional) - For internal use only.
    - :resolvebyslastatus: (Integer,optional) - Shows the status of the resolution time for the case according to the terms of the SLA.

        **Default Options Values:**
            1. In Progress
            2. Nearing Noncompliance
            3. Succeeded
            4. Noncompliant
    - :routecase: (Boolean,optional) - Tells whether the incident has been routed to queue or not.DefaultValue: true
    - :customersatisfactioncode:
    (Integer,optional) - Select the customer's level of satisfaction with the handling and resolution of the case.

        **Default Options Values:**
            1. Very Dissatisfied
            2. Dissatisfied
            3. Neutral
            4. Satisfied
            5. Very Satisfied
    - :sentimentvalue: (Double,optional) - Value derived after assessing words commonly associated with a negative, neutral, or positive sentiment that occurs in a social post. Sentiment information can also be reported as numeric values.
    - :productserialnumber: (string,optional) - Type the serial number of the product that is associated with this case, so that the number of cases per product can be reported.
    - :contractservicelevelcode: (Integer,optional) - Select the service level for the case to make sure the case is handled correctly.

        **Default Options Values:**
            1. Gold
            2. Silver
            3. Bronze
    - :servicestage: (Integer,optional) - Select the stage, in the case resolution process, that the case is in.

        **Default Options Values:**
            0. Identify
            1. Research
            2. Resolve
    - :severitycode: (Integer,optional) - Select the severity of this case to indicate the incident's impact on the customer's business.

        **Default Options Values:**
        1. Default Value
    - :socialprofileid: (string,optional) - Unique identifier of the social profile with which the case is associated.
    - :statuscode: (Integer,optional) - Select the case's status.

        **Default Options Values:**
            - 1: In Progress
            - 2: On Hold
            - 3: Waiting for Details
            - 4: Researching

    - :subjectid: (string,optional) - Choose the subject for the case, such as catalog request or product complaint, so customer service managers can identify frequent requests or problem areas. Administrators can configure subjects under Business Management in the Settings area.
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the updated incident record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "incidentid" in params:
            domain = creds["domain"]
            incidentid = params["incidentid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/incidents({incidentid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "productid" in params:
                data['productid@odata.bind'] = f"/products({params['productid']})"
            if "resolvebykpiid" in params:
                data['resolvebykpiid@odata.bind'] = f"/slakpiinstances({params['resolvebykpiid']})"
            if "socialprofileid" in params:
                data['socialprofileid@odata.bind'] = f"/socialprofiles({params['socialprofileid']})"
            if "subjectid" in params:
                data['subjectid@odata.bind'] = f"/subjects({params['subjectid']})"
            if "parentcaseid" in params:
                data['parentcaseid@odata.bind'] = f"/incidents({params['parentcaseid']})"
            for key, value in params.items():
                skip_keys = ["customerid", "customeridtype", "transactioncurrencyid","productid", "resolvebykpiid", "socialprofileid", "subjectid","parentcaseid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_incident(accessToken, cred, params):
    """
    Deletes a specific incident record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :incidentid: (string,required) - The unique identifier of the incident to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the incident was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "incidentid" in params:
            domain = creds["domain"]
            incidentid = params["incidentid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/incidents({incidentid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Incident deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

#################################### Opportunity ####################################################

def microsoft_dynamics_crm_get_many_opportunity(accessToken, cred):
    """
    Fetches multiple opportunity records from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.

    Returns:
        dict: A dictionary containing the OData context and a list of opportunity records.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/opportunities"
            headers = {"Authorization": "Bearer " + accessToken}
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_get_opportunity(accessToken, cred, params):
    """
    Fetches a specific opportunity record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :opportunityid: (string,required) - The unique identifier of the opportunity to be retrieved.

    Returns:
        dict: A dictionary containing detailed information about the specific opportunity record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "opportunityid" in params:
            domain = creds["domain"]
            opportunityid = params["opportunityid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/opportunities({opportunityid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_create_opportunity(accessToken, cred, params):
    """
    Creates a new opportunity record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :transactioncurrencyid: (string,required) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :name: (string,required) - Type a subject or descriptive name, such as the expected order or company name, for the opportunity.
    - :parentaccountid: (string,optional) - Choose an account to connect this opportunity to, so that the relationship is visible in reports and analytics, and to provide a quick link to additional details, such as financial information and activities.
    - :actualclosedate: (DateTime,optional) - Shows the date and time when the opportunity was closed or canceled.
    - :actualvalue: (integer,optional) - Type the actual revenue amount for the opportunity for reporting and analysis of estimated versus actual sales. Field defaults to the Est. Revenue value when an opportunity is won.
    - :budgetstatus: (integer,optional) - Select the likely budget status for the lead's company. This may help determine the lead rating or your sales approach.

        **Default Options Values:**
            0.	No Committed Budget
            1.	May Buy
            2.	Can Buy
            3.	Will Buy
    - :budgetamount: (integer,optional) - Type a value between 0 and 1,000,000,000,000 to indicate the lead's potential available budget.
    - :completeinternalreview: (Boolean,optional) - Select whether an internal review has been completed for this opportunity.DefaultValue: false
    - :confirminterest: (Boolean,optional) - Select whether the lead confirmed interest in your offerings. This helps in determining the lead quality and the probability of it turning into an opportunity.DefaultValue: false
    - :parentcontactid: (string,optional) - Choose a contact to connect this opportunity to, so that the relationship is visible in reports and analytics.
    - :currentsituation: (string,optional) - Type notes about the company or organization associated with the opportunity.
    - :customerneed: (string,optional) - Type some notes about the customer's requirements, to help the sales team identify products and services that could meet their requirements.
    - :customerpainpoints: (string,optional) - Type notes about the customer's pain points to help the sales team identify products and services that could address these pain points.
    - :pursuitdecision: (Boolean,optional) - Select whether the decision about pursuing the opportunity has been made.DefaultValue: false
    - :decisionmaker: (Boolean,optional) - Select whether your notes include information about who makes the purchase decisions at the lead's company.DefaultValue: false
    - :description: (string,optional) - Type additional information to describe the opportunity, such as possible products to sell or past purchases from the customer.
    - :developproposal: (Boolean,optional) - Select whether a proposal has been developed for the opportunity.DefaultValue: false
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :estimatedclosedate: (DateTime,optional) - Enter the expected closing date of the opportunity to help make accurate revenue forecasts.
    - :estimatedvalue: (integer,optional) - Type the estimated revenue amount to indicate the potential sale or value of the opportunity for revenue forecasting. This field can be either system-populated or editable based on the selection in the Revenue field.
    - :evaluatefit: (Boolean,optional) - Select whether the fit between the lead's requirements and your offerings was evaluated.DefaultValue: false
    - :resolvefeedback: (Boolean,optional) - Choose whether the proposal feedback has been captured and resolved for the opportunity.DefaultValue: false
    - :filedebrief: (Boolean,optional) - Choose whether the sales team has recorded detailed notes on the proposals and the account's responses.DefaultValue: false
    - :finaldecisiondate: (DateTime,optional) - Enter the date and time when the final decision of the opportunity was made.
    - :completefinalproposal: (Boolean,optional) - Select whether a final proposal has been completed for the opportunity.DefaultValue: false
    - :freightamount: (integer,optional) - Type the cost of freight or shipping for the products included in the opportunity for use in calculating the Total Amount field.
    - :msdyn_gdproptout: (Boolean,optional) - Describes whether opportunity is opted out or not.DefaultValue: false
    - :identifycompetitors: (Boolean,optional) - Select whether information about competitors is included.DefaultValue: false
    - :identifycustomercontacts: (Boolean,optional) - Select whether the customer contacts for this opportunity have been identified.DefaultValue: false
    - :identifypursuitteam: (Boolean,optional) - Choose whether you have recorded who will pursue the opportunity.DefaultValue: false
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :initialcommunication: (Integer,optional) - Choose whether someone from the sales team contacted this lead earlier.

            **Default Options Values:**
                0.	Contacted
                1.	Not Contacted
    - :lastonholdtime: (DateTime,optional) - Contains the date and time stamp of the last on hold time.
    - :need: (Integer,optional) - Choose how high the level of need is for the lead's company.

            **Default Options Values:**
                0.  Must have
                1.  Should have
                2.  Good to have
                3.  No need
    - :discountpercentage: (Float,optional) - Type the discount rate that should be applied to the Product Totals field to include additional savings for the customer in the opportunity.
    - :discountamount: (Integer,optional) - Type the discount amount for the opportunity if the customer is eligible for special savings.
    - :originatingleadid: (string,optional) - Choose the lead that the opportunity was created from for reporting and analytics. The field is read-only after the opportunity is created and defaults to the correct lead when an opportunity is created from a converted lead.
    - :participatesinworkflow: (Boolean,optional) - Information about whether the opportunity participates in workflow rules.DefaultValue: false
    - :stepname: (string,optional) - Shows the current phase in the sales pipeline for the opportunity.
    - :presentfinalproposal: (Boolean,optional) - Select whether the final proposal has been presented to the account.DefaultValue: false
    - :presentproposal: (Boolean,optional) - Select whether a proposal for the opportunity has been presented to the account.DefaultValue: false
    - :pricelevelid: (string,optional) - Choose the price list associated with this record to make sure the products associated with the campaign are offered at the correct prices.
    - :pricingerrorcode: (Integer,optional) - Pricing error for the opportunity.

            **Default Options Values:**
                0.	None
                1.	Detail Error
                2.	Missing Price Level
                3.	Inactive Price Level
                4.	Missing Quantity
                5.	Missing Unit Price
                6.	Missing Product
                7.	Invalid Product
                8.	Missing Pricing Code
                9.	Invalid Pricing Code
                10.	Missing UOM
                11.	Product Not In Price Level
                12.	Missing Price Level Amount
                13.	Missing Price Level Percentage
                14.	Missing Price
                15.	Missing Current Cost
                16.	Missing Standard Cost
                17.	Invalid Price Level Amount
                18.	Invalid Price Level Percentage
                19.	Invalid Price
                20.	Invalid Current Cost
                21.	Invalid Standard Cost
                22.	Invalid Rounding Policy
                23.	Invalid Rounding Option
                24.	Invalid Rounding Amount
                25.	Price Calculation Error
                26.	Invalid Discount Type
                27.	Discount Type Invalid State
                28.	Invalid Discount
                29.	Invalid Quantity
                30.	Invalid Pricing Precision
                31.	Missing Product Default UOM
                32.	Missing Product UOM Schedule
                33.	Inactive Discount Type
                34.	Invalid Price Level Currency
                35.	Price Attribute Out Of Range
                36.	Base Currency Attribute Overflow
                37.	Base Currency Attribute Underflow
                38.	Transaction currency is not set for the product price list item
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.
            **Default Options Values:**
                1 - Default Value
    - :closeprobability: (integer,optional) - Type a number from 0 to 100 that represents the likelihood of closing the opportunity. This can aid the sales team in their efforts to convert the opportunity in a sale.
    - :salesstagecode: (Integer,optional) - Select the sales process stage for the opportunity to indicate the probability of closing the opportunity.
            **Default Options Values:**
                1 - Default Value
    - :captureproposalfeedback:
    (Boolean,optional) - Choose whether the proposal feedback has been captured for the opportunity.DefaultValue: false

    - :proposedsolution: (string,optional) - Type notes about the proposed solution for the opportunity.
    - :purchaseprocess: (Integer,optional) - Choose whether an individual or a committee will be involved in the purchase process for the lead.
            **Default Options Values:**
                0.	Individual
                1.	Committee
                2.	Unknown
    - :purchasetimeframe: (Integer,optional) - Choose how long the lead will likely take to make the purchase.
            **Default Options Values:**
                0.	Immediate
                1.	This Quarter
                2.	Next Quarter
                3.	This Year
                4.	Unknown
    - :qualificationcomments: (string,optional) - Type comments about the qualification or scoring of the lead.
    - :quotecomments: (string,optional) - Type comments about the quotes associated with the opportunity.
    - :opportunityratingcode: (Integer,optional) - Select the expected value or priority of the opportunity based on revenue, customer status, or closing probability.
            **Default Options Values:**
                1.	Hot
                2.	Warm
                3.	Cold
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :isrevenuesystemcalculated:
    (Boolean,optional) - Select whether the estimated revenue for the opportunity is calculated automatically based on the products entered or entered manually by a user.DefaultValue: false

    - :salesstage: (Integer,optional) - Select the sales stage of this opportunity to aid the sales team in their efforts to win this opportunity.
            **Default Options Values:**
                0.	Qualify
                1.	Develop
                2.	Propose
                3.	Close
    - :scheduleproposalmeeting:
    (DateTime,optional) - Enter the date and time of the proposal meeting for the opportunity.

    - :schedulefollowup_prospect: (DateTime,optional) - Enter the date and time of the prospecting follow-up meeting with the lead.
    - :schedulefollowup_qualify:
    (DateTime,optional) - Enter the date and time of the qualifying follow-up meeting with the lead.

    - :sendthankyounote: (Boolean,optional) - Select whether a thank you note has been sent to the account for considering the proposal.DefaultValue: false
    - :campaignid: (string,optional) - Shows the campaign that the opportunity was created from. The ID is used for tracking the success of the campaign.
    - :statuscode: (Integer,optional) - Select the opportunity's status.
            **Default Options Values:**
                1.	In Progress
                2.	On Hold
                3.	Won
                4.	Canceled
                5.	Out-Sold
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :timeline: (Integer,optional) - Select when the opportunity is likely to be closed.
            **Default Options Values:**
                0. Immediate
                1. This Quarter
                2. Next Quarter
                3. This Year
                4. Not known
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the newly created opportunity record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "transactioncurrencyid" in params and "name" in params:
            domain = creds["domain"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/opportunities"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "parentaccountid" in params:
                data['parentaccountid@odata.bind'] = f"/accounts({params['parentaccountid']})"
            if "parentcontactid" in params:
                data['parentcontactid@odata.bind'] = f"/contacts({params['parentcontactid']})"
            if "originatingleadid" in params:
                data['originatingleadid@odata.bind'] = f"/leads({params['originatingleadid']})"
            if "pricelevelid" in params:
                data['pricelevelid@odata.bind'] = f"/pricelevels({params['pricelevelid']})"
            if "campaignid" in params:
                data['campaignid@odata.bind'] = f"/campaigns({params['campaignid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid", "parentaccountid","parentcontactid", "originatingleadid", "pricelevelid", "campaignid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_update_opportunity(accessToken, cred, params):
    """
    Updates a specific opportunity record in Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

    - :opportunityid: (string,required) - The unique identifier of the opportunity to be updated.
    - :transactioncurrencyid: (string,optional) - Choose the local currency for the record to make sure budgets are reported in the correct currency.
    - :name: (string,optional) - Type a subject or descriptive name, such as the expected order or company name, for the opportunity.
    - :parentaccountid: (string,optional) - Choose an account to connect this opportunity to, so that the relationship is visible in reports and analytics, and to provide a quick link to additional details, such as financial information and activities.
    - :actualclosedate: (DateTime,optional) - Shows the date and time when the opportunity was closed or canceled.
    - :actualvalue: (integer,optional) - Type the actual revenue amount for the opportunity for reporting and analysis of estimated versus actual sales. Field defaults to the Est. Revenue value when an opportunity is won.
    - :budgetstatus: (integer,optional) - Select the likely budget status for the lead's company. This may help determine the lead rating or your sales approach.

        **Default Options Values:**
            0.	No Committed Budget
            1.	May Buy
            2.	Can Buy
            3.	Will Buy
    - :budgetamount: (integer,optional) - Type a value between 0 and 1,000,000,000,000 to indicate the lead's potential available budget.
    - :completeinternalreview: (Boolean,optional) - Select whether an internal review has been completed for this opportunity.DefaultValue: false
    - :confirminterest: (Boolean,optional) - Select whether the lead confirmed interest in your offerings. This helps in determining the lead quality and the probability of it turning into an opportunity.DefaultValue: false
    - :parentcontactid: (string,optional) - Choose a contact to connect this opportunity to, so that the relationship is visible in reports and analytics.
    - :currentsituation: (string,optional) - Type notes about the company or organization associated with the opportunity.
    - :customerneed: (string,optional) - Type some notes about the customer's requirements, to help the sales team identify products and services that could meet their requirements.
    - :customerpainpoints: (string,optional) - Type notes about the customer's pain points to help the sales team identify products and services that could address these pain points.
    - :pursuitdecision: (Boolean,optional) - Select whether the decision about pursuing the opportunity has been made.DefaultValue: false
    - :decisionmaker: (Boolean,optional) - Select whether your notes include information about who makes the purchase decisions at the lead's company.DefaultValue: false
    - :description: (string,optional) - Type additional information to describe the opportunity, such as possible products to sell or past purchases from the customer.
    - :developproposal: (Boolean,optional) - Select whether a proposal has been developed for the opportunity.DefaultValue: false
    - :emailaddress: (string,optional) - The primary email address for the entity.
    - :estimatedclosedate: (DateTime,optional) - Enter the expected closing date of the opportunity to help make accurate revenue forecasts.
    - :estimatedvalue: (integer,optional) - Type the estimated revenue amount to indicate the potential sale or value of the opportunity for revenue forecasting. This field can be either system-populated or editable based on the selection in the Revenue field.
    - :evaluatefit: (Boolean,optional) - Select whether the fit between the lead's requirements and your offerings was evaluated.DefaultValue: false
    - :resolvefeedback: (Boolean,optional) - Choose whether the proposal feedback has been captured and resolved for the opportunity.DefaultValue: false
    - :filedebrief: (Boolean,optional) - Choose whether the sales team has recorded detailed notes on the proposals and the account's responses.DefaultValue: false
    - :finaldecisiondate: (DateTime,optional) - Enter the date and time when the final decision of the opportunity was made.
    - :completefinalproposal: (Boolean,optional) - Select whether a final proposal has been completed for the opportunity.DefaultValue: false
    - :freightamount: (integer,optional) - Type the cost of freight or shipping for the products included in the opportunity for use in calculating the Total Amount field.
    - :msdyn_gdproptout: (Boolean,optional) - Describes whether opportunity is opted out or not.DefaultValue: false
    - :identifycompetitors: (Boolean,optional) - Select whether information about competitors is included.DefaultValue: false
    - :identifycustomercontacts: (Boolean,optional) - Select whether the customer contacts for this opportunity have been identified.DefaultValue: false
    - :identifypursuitteam: (Boolean,optional) - Choose whether you have recorded who will pursue the opportunity.DefaultValue: false
    - :importsequencenumber: (Integer,optional) - Sequence number of the import that created this record.
    - :initialcommunication: (Integer,optional) - Choose whether someone from the sales team contacted this lead earlier.

            **Default Options Values:**
                0.	Contacted
                1.	Not Contacted
    - :lastonholdtime: (DateTime,optional) - Contains the date and time stamp of the last on hold time.
    - :need: (Integer,optional) - Choose how high the level of need is for the lead's company.

            **Default Options Values:**
                0.  Must have
                1.  Should have
                2.  Good to have
                3.  No need
    - :discountpercentage: (Float,optional) - Type the discount rate that should be applied to the Product Totals field to include additional savings for the customer in the opportunity.
    - :discountamount: (Integer,optional) - Type the discount amount for the opportunity if the customer is eligible for special savings.
    - :originatingleadid: (string,optional) - Choose the lead that the opportunity was created from for reporting and analytics. The field is read-only after the opportunity is created and defaults to the correct lead when an opportunity is created from a converted lead.
    - :participatesinworkflow: (Boolean,optional) - Information about whether the opportunity participates in workflow rules.DefaultValue: false
    - :stepname: (string,optional) - Shows the current phase in the sales pipeline for the opportunity.
    - :presentfinalproposal: (Boolean,optional) - Select whether the final proposal has been presented to the account.DefaultValue: false
    - :presentproposal: (Boolean,optional) - Select whether a proposal for the opportunity has been presented to the account.DefaultValue: false
    - :pricelevelid: (string,optional) - Choose the price list associated with this record to make sure the products associated with the campaign are offered at the correct prices.
    - :pricingerrorcode: (Integer,optional) - Pricing error for the opportunity.

            **Default Options Values:**
                0.	None
                1.	Detail Error
                2.	Missing Price Level
                3.	Inactive Price Level
                4.	Missing Quantity
                5.	Missing Unit Price
                6.	Missing Product
                7.	Invalid Product
                8.	Missing Pricing Code
                9.	Invalid Pricing Code
                10.	Missing UOM
                11.	Product Not In Price Level
                12.	Missing Price Level Amount
                13.	Missing Price Level Percentage
                14.	Missing Price
                15.	Missing Current Cost
                16.	Missing Standard Cost
                17.	Invalid Price Level Amount
                18.	Invalid Price Level Percentage
                19.	Invalid Price
                20.	Invalid Current Cost
                21.	Invalid Standard Cost
                22.	Invalid Rounding Policy
                23.	Invalid Rounding Option
                24.	Invalid Rounding Amount
                25.	Price Calculation Error
                26.	Invalid Discount Type
                27.	Discount Type Invalid State
                28.	Invalid Discount
                29.	Invalid Quantity
                30.	Invalid Pricing Precision
                31.	Missing Product Default UOM
                32.	Missing Product UOM Schedule
                33.	Inactive Discount Type
                34.	Invalid Price Level Currency
                35.	Price Attribute Out Of Range
                36.	Base Currency Attribute Overflow
                37.	Base Currency Attribute Underflow
                38.	Transaction currency is not set for the product price list item
    - :prioritycode: (Integer,optional) - Select the priority so that preferred customers or critical issues are handled quickly.
            **Default Options Values:**
                1 - Default Value
    - :closeprobability: (integer,optional) - Type a number from 0 to 100 that represents the likelihood of closing the opportunity. This can aid the sales team in their efforts to convert the opportunity in a sale.
    - :salesstagecode: (Integer,optional) - Select the sales process stage for the opportunity to indicate the probability of closing the opportunity.
            **Default Options Values:**
                1 - Default Value
    - :captureproposalfeedback: (Boolean,optional) - Choose whether the proposal feedback has been captured for the opportunity.DefaultValue: false
    - :proposedsolution: (string,optional) - Type notes about the proposed solution for the opportunity.
    - :purchaseprocess: (Integer,optional) - Choose whether an individual or a committee will be involved in the purchase process for the lead.
            **Default Options Values:**
                0.	Individual
                1.	Committee
                2.	Unknown
    - :purchasetimeframe: (Integer,optional) - Choose how long the lead will likely take to make the purchase.
            **Default Options Values:**
                0.	Immediate
                1.	This Quarter
                2.	Next Quarter
                3.	This Year
                4.	Unknown
    - :qualificationcomments: (string,optional) - Type comments about the qualification or scoring of the lead.
    - :quotecomments: (string,optional) - Type comments about the quotes associated with the opportunity.
    - :opportunityratingcode: (Integer,optional) - Select the expected value or priority of the opportunity based on revenue, customer status, or closing probability.
            **Default Options Values:**
                1.	Hot
                2.	Warm
                3.	Cold
    - :overriddencreatedon: (DateTime,optional) - Date and time that the record was migrated.
    - :isrevenuesystemcalculated:
    (Boolean,optional) - Select whether the estimated revenue for the opportunity is calculated automatically based on the products entered or entered manually by a user.DefaultValue: false

    - :salesstage: (Integer,optional) - Select the sales stage of this opportunity to aid the sales team in their efforts to win this opportunity.
            **Default Options Values:**
                0.	Qualify
                1.	Develop
                2.	Propose
                3.	Close
    - :scheduleproposalmeeting:
    (DateTime,optional) - Enter the date and time of the proposal meeting for the opportunity.

    - :schedulefollowup_prospect: (DateTime,optional) - Enter the date and time of the prospecting follow-up meeting with the lead.
    - :schedulefollowup_qualify:
    (DateTime,optional) - Enter the date and time of the qualifying follow-up meeting with the lead.

    - :sendthankyounote: (Boolean,optional) - Select whether a thank you note has been sent to the account for considering the proposal.DefaultValue: false
    - :campaignid: (string,optional) - Shows the campaign that the opportunity was created from. The ID is used for tracking the success of the campaign.
    - :statuscode: (Integer,optional) - Select the opportunity's status.
            **Default Options Values:**
                1.	In Progress
                2.	On Hold
                3.	Won
                4.	Canceled
                5.	Out-Sold
    - :timezoneruleversionnumber: (Integer,optional) - For internal use only.
    - :timeline: (Integer,optional) - Select when the opportunity is likely to be closed.
            **Default Options Values:**
                0. Immediate
                1. This Quarter
                2. Next Quarter
                3. This Year
                4. Not known
    - :utcconversiontimezonecode:
    (Integer,optional) - Time zone code that was in use when the record was created.

    Returns:
        dict: A dictionary containing detailed information about the updated opportunity record.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "opportunityid" in params:
            domain = creds["domain"]
            opportunityid = params["opportunityid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/opportunities({opportunityid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            data = {}
            if "transactioncurrencyid" in params:
                data['transactioncurrencyid@odata.bind'] = f"/transactioncurrencies({params['transactioncurrencyid']})"
            if "parentaccountid" in params:
                data['parentaccountid@odata.bind'] = f"/accounts({params['parentaccountid']})"
            if "parentcontactid" in params:
                data['parentcontactid@odata.bind'] = f"/contacts({params['parentcontactid']})"
            if "originatingleadid" in params:
                data['originatingleadid@odata.bind'] = f"/leads({params['originatingleadid']})"
            if "pricelevelid" in params:
                data['pricelevelid@odata.bind'] = f"/pricelevels({params['pricelevelid']})"
            if "campaignid" in params:
                data['campaignid@odata.bind'] = f"/campaigns({params['campaignid']})"
            for key, value in params.items():
                skip_keys = ["transactioncurrencyid", "parentaccountid","parentcontactid", "originatingleadid", "pricelevelid", "campaignid"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.patch(url=url, headers=headers, json=data)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_dynamics_crm_delete_opportunity(accessToken, cred, params):
    """
    Deletes a specific opportunity record from Dynamics CRM.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict cred: The credentials dictionary containing necessary information like the CRM instance URL and other relevant details.
    :param dict params: A dictionary containing parameters for the request.

        - :opportunityid: (string,required) - The unique identifier of the opportunity to be deleted.

    Returns:
        dict: A dictionary containing a success message indicating that the opportunity was successfully deleted.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "opportunityid" in params:
            domain = creds["domain"]
            opportunityid = params["opportunityid"]
            url = f"https://{domain}.crm4.dynamics.com/api/data/v9.2/opportunities({opportunityid})"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return {"message": "Opportunity deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)