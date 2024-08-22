import requests, json


def extract_credential(credential):
    """
    Extract the Host address and Access token from the provided credentials.

    :credentials: A json dictionary containing credential parameters.
    
    - :host: (str, Required) - host web address of the magento 2 instance of the user
    - :accessToken: (str, Required) - Access Token acquired from Magento integration following the steps in this `page <https://docs.n8n.io/integrations/builtin/credentials/magento2/?utm_source=n8n_app&utm_medium=left_nav_menu&utm_campaign=create_new_credentials_modal#using-access-token>`_.
    
        - Note that if the magento instance version used is >= v2.4.0 then you should set the 'Stores > Configuration > Services > OAuth > Consumer Settings > Allow OAuth Access Tokens to be used as standalone Bearer tokens" option to 'Yes'.
    
    
    :return: tuple containing the host address in the first parameter and the access token in the second parameter
    :rtype: tuple of strings

    :raises Exception: If there's an issue with the input data or if an error occurs during connection setup.
    """
    try:
        credentials = json.loads(credential)
        if "host" in credentials and "accessToken" in credentials:
            host = credentials["host"]
            accessToken = credentials["accessToken"]
            return (host,accessToken)
        else:
            raise Exception("missing credentials")
    except Exception as e:
        raise Exception(f"Error creating client instance: {e}")



####################################### Customer ##########################################


def magento_2_get_many_customers(credential, params):
    """
    Retrieve many products from magento 2 instance depending on the parameters. for the specifics of the search parameters visit this `page <https://developer.adobe.com/commerce/webapi/rest/use-rest/performing-searches/>`_.

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :limit: (int,optional) - the number of retrieved products to display
    - :sort: (list of dict,optional) - list of dictionaries with each dictionary containing the following 2 keys:
    
        - :direction: (str,required) - sort direction. Optional values: (ASC, DESC)
        - :field: (str,required) - field name of the field to sort by
    
    - :filters_logical_operator: (str,optional) - the logical operator to group the filters by. Optional values: (and, or)
    - :filters: (list of dict,optional) - list of filter objects as dictionaries containing:

        - :field: (str,required) - field name of the field to filter by
        - :value: (str,optional) - value to filter by
        - :condition_type: (str,required) - condition type to filter by. 
        
            Optional values: (eq, finset, from, gt, gteq, in, like, lt, lteq, moreq, neq, nfinset, nin, nlike, notnull, null, to)

    :return: dictionary containing a list of customer objects
    :rtype: dict
    """
    try:
        limit = params.get("limit", None)
        sort = params.get("sort", [])
        filters_logical_operator = params.get("filters_logical_operator", "")
        filters = params.get("filters", [])
        host, access_token = extract_credential(credential)
        request_params = {"searchCriteria[currentPage]": "0"}
        api_url = f"{host}/rest/default/V1/customers/search"
        headers = {
            "Authorization": "Bearer " + access_token
        }
        if limit:
            request_params["searchCriteria[pageSize]"] = str(limit)
        
        if sort:
            if sort[0]:
                for i, sort_dict in enumerate(sort):
                    if "direction" in sort_dict and "field" in sort_dict:
                        request_params[f"searchCriteria[sortOrders][{i}][direction]"] = sort_dict.get("direction")
                        request_params[f"searchCriteria[sortOrders][{i}][field]"] = sort_dict.get("field")
                    else:
                        raise Exception("Missing input for sort")
            
        if filters:
            if (filters_logical_operator == "and" or filters_logical_operator == "or") and filters[0]:
                if filters_logical_operator == "and":
                    for i, filters_dict in enumerate(filters):
                        if "field" in filters_dict and "condition_type" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][field]"] = filters_dict.get("field")
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][condition_type]"] = filters_dict.get("condition_type")
                        else:
                            raise Exception("Missing Input for filter")
                        if "value" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][value]"] = filters_dict.get("value")
                elif filters_logical_operator == "or":
                    for i, filters_dict in enumerate(filters):
                        if "field" in filters_dict and "condition_type" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][field]"] = filters_dict.get("field")
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][condition_type]"] = filters_dict.get("condition_type")
                        else:
                            raise Exception("Missing Input for filter")
                        if "value" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][value]"] = filters_dict.get("value")
            
        response = requests.get(url=api_url, headers=headers, params=request_params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)




def magento_2_get_customer(credential, params):
    """
    Retrieve a Customer by it's customerID

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :customerID: (int,required) - ID of the Customer to be retrieved

    :return: The selected Customer object
    :rtype: dict
    """
    try:
        if "customerID" in params:
            customerID = params["customerID"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/customers/{customerID}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.get(url=api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def magento_2_create_customer(credential, params):
    """
    Create a Customer according to the provided Customer object

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :customer: (dict,required) - dictionary containing the values of the customer to be created as represented in a Customer object.

        - :email: (str,required) - 
        - :firstname: (str,required) - 
        - :lastname: (str,required) - 
        - :middlename: (str,optional) - 
        - :prefix: (str,optional) - 
        - :suffix: (str,optional) - 
        - :gender: (int,optional) - 
        - :store_id: (int,optional) - 
        - :group_id: (int,optional) - 
        - :confirmation: (str,optional) - 
        - :website_id: (int,optional) - 
        - :default_billing: (str,optional) - 
        - :default_shipping: (str,optional) - 
        - :dob: (str,optional) - Date of birth
        .
        .
        .
        .
        etc...
        
    - :password: (str,optional) - 
    
    :return: The Created Customer object
    :rtype: dict
    """
    try:
        customer = params.get("customer", {})
        if customer and "email" in customer and "firstname" in customer and "lastname" in customer:
            password = params.get("password", "")
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/customers"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {"customer": customer}
            if password:
                data["password"] = password
            
            response = requests.post(url=api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def magento_2_update_customer(credential, params):
    """
    Update a Customer by it's customerID according to the provided Customer object

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :customerID: (str,required) - customerID of the Customer to be Updated
    - :customer: (dict,required) - dictionary containing the values to be updated as represented in a Customer object. enter the parameter only if you want to update it

        - :email: (str,required) - 
        - :firstname: (str,required) - 
        - :lastname: (str,required) - 
        - :middlename: (str,optional) - 
        - :prefix: (str,optional) - 
        - :suffix: (str,optional) - 
        - :gender: (int,optional) - 
        - :store_id: (int,optional) - 
        - :group_id: (int,optional) - 
        - :confirmation: (str,optional) - 
        - :website_id: (int,optional) - 
        - :default_billing: (str,optional) - 
        - :default_shipping: (str,optional) - 
        - :dob: (str,optional) - Date of birth
        .
        .
        .
        .
        etc...
    
    - :passwordHash: (str,optional) - 
    
    :return: The Updated Customer object
    :rtype: dict
    """
    try:
        customer = params.get("customer", {})
        if "customerID" in params and customer and "email" in customer and "firstname" in customer and "lastname" in customer:
            passwordHash = params.get("passwordHash", "")
            customerID = params["customerID"]
            customer = params["customer"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/customers/{customerID}"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {"customer": customer}
            if passwordHash:
                data["passwordHash"] = passwordHash
            
            response = requests.put(url=api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)


def magento_2_delete_customer(credential, params):
    """
    Delete a Customer by it's customerID

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :customerID: (str,required) - customerID of the Customer to be deleted

    :return: returns dictionary containing Boolean true upon successfull deletion
    :rtype: dict
    """
    try:
        if "customerID" in params:
            customerID = params["customerID"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/customers/{customerID}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.delete(url=api_url, headers=headers)
            if response.status_code == 200 and response.json():
                return {"message": "Customer deleted Successfully", "response": response.json()}
            elif response.status_code == 200 and not response.json():
                return {"message": "Error Deleting Customer", "response": response.json()}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



####################################### Product ##########################################


def magento_2_get_many_products(credential, params):
    """
    Retrieve many products from magento 2 instance depending on the parameters. for the specifics of the search parameters visit this `page <https://developer.adobe.com/commerce/webapi/rest/use-rest/performing-searches/>`_.

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :limit: (int,optional) - the number of retrieved products to display
    - :sort: (list of dict,optional) - list of dictionaries with each dictionary containing the following 2 keys:
    
        - :direction: (str,required) - sort direction. Optional values: (ASC, DESC)
        - :field: (str,required) - field name of the field to sort by
    
    - :filters_logical_operator: (int,optional) - the logical operator to group the filters by. Optional values: (and, or)
    - :filters: (list of dict,optional) - list of filter objects as dictionaries containing:

        - :field: (str,required) - field name of the field to filter by
        - :value: (str,optional) - value to filter by
        - :condition_type: (str,required) - condition type to filter by. 
        
            Optional values: (eq, finset, from, gt, gteq, in, like, lt, lteq, moreq, neq, nfinset, nin, nlike, notnull, null, to)

    :return: dictionary containing a list of Product objects
    :rtype: dict
    """
    try:
        limit = params.get("limit", None)
        sort = params.get("sort", [])
        filters_logical_operator = params.get("filters_logical_operator", "")
        filters = params.get("filters", [])
        host, access_token = extract_credential(credential)
        request_params = {"searchCriteria[currentPage]": "0"}
        api_url = f"{host}/rest/default/V1/products"
        headers = {
            "Authorization": "Bearer " + access_token
        }
        if limit:
            request_params["searchCriteria[pageSize]"] = str(limit)
        
        if sort:
            if sort[0]:
                for i, sort_dict in enumerate(sort):
                    if "direction" in sort_dict and "field" in sort_dict:
                        request_params[f"searchCriteria[sortOrders][{i}][direction]"] = sort_dict.get("direction")
                        request_params[f"searchCriteria[sortOrders][{i}][field]"] = sort_dict.get("field")
                    else:
                        raise Exception("Missing input for sort")
            
        if filters:
            if (filters_logical_operator == "and" or filters_logical_operator == "or") and filters[0]:
                if filters_logical_operator == "and":
                    for i, filters_dict in enumerate(filters):
                        if "field" in filters_dict and "condition_type" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][field]"] = filters_dict.get("field")
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][condition_type]"] = filters_dict.get("condition_type")
                        else:
                            raise Exception("Missing Input for filter")
                        if "value" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][value]"] = filters_dict.get("value")
                elif filters_logical_operator == "or":
                    for i, filters_dict in enumerate(filters):
                        if "field" in filters_dict and "condition_type" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][field]"] = filters_dict.get("field")
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][condition_type]"] = filters_dict.get("condition_type")
                        else:
                            raise Exception("Missing Input for filter")
                        if "value" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][value]"] = filters_dict.get("value")
        
        response = requests.get(url=api_url, headers=headers, params=request_params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)


def magento_2_get_product(credential, params):
    """
    Retrieve a product by it's sku

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :sku: (str,required) - sku of the product to be retrieved

    :return: The selected Product object
    :rtype: dict
    """
    try:
        if "sku" in params:
            sku = params["sku"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/products/{sku}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.get(url=api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def magento_2_create_product(credential, params):
    """
    Create a product according to the provided product object

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :product: (dict,required) - dictionary containing the values of the product to be created as represented in a product object.

        - :sku: (str,required) - 
        - :name: (str,required) - 
        - :attribute_set_id: (int,required) - 
        - :price: (float,optional) - 
        - :status: (int,optional) - 
        - :visibility: (int,optional) - Optional Values: (1, 2, 3, 4) where 1 represents: 'Not Visible Individually', 2 represents: 'Catalog', 3 represents: 'Search', and 4 represents: 'Catalog, Search'
        - :type_id: (str,optional) - 
        - :weight: (int,optional) - 
        
    
    :return: The Created Product object
    :rtype: dict
    """
    try:
        product = params.get("product", {})
        if product and "sku" in product and "name" in product and "attribute_set_id" in product:
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/products"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {"product": product}
            response = requests.post(url=api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def magento_2_update_product(credential, params):
    """
    Update a product by it's sku according to the provided product object

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :sku: (str,required) - sku of the product to be Updated
    - :product: (dict,required) - dictionary containing the values to be updated as represented in a product object. enter the parameter only if you want to update it

        - :sku: (str,required) - sku of the product to be Updated
        - :name: (str,optional) - 
        - :attribute_set_id: (int,optional) - 
        - :price: (int,optional) - 
        - :status: (int,optional) - 
        - :visibility: (int,optional) - 
        - :type_id: (str,optional) - 
        - :weight: (int,optional) - 
        
    
    :return: The Updated Product object
    :rtype: dict
    """
    try:
        if "sku" in params and "product" in params:
            sku = params["sku"]
            product = params["product"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/products/{sku}"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {"product": product}
            response = requests.put(url=api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)



def magento_2_delete_product(credential, params):
    """
    Delete a product by it's sku

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :sku: (str,required) - sku of the product to be retrieved

    :return: returns dictionary containing Boolean true upon successfull deletion
    :rtype: dict
    """
    try:
        if "sku" in params:
            sku = params["sku"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/products/{sku}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.delete(url=api_url, headers=headers)
            if response.status_code == 200 and response.json():
                return {"message": "Product deleted Successfully", "response": response.json()}
            elif response.status_code == 200 and not response.json():
                return {"message": "Error Deleting Product", "response": response.json()}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)




####################################### Order ##########################################


def magento_2_get_many_orders(credential, params):
    """
    Retrieve many orders from magento 2 instance depending on the parameters. for the specifics of the search parameters visit this `page <https://developer.adobe.com/commerce/webapi/rest/use-rest/performing-searches/>`_.

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :limit: (int,optional) - the number of retrieved orders to display
    - :sort: (list of dict,optional) - list of dictionaries with each dictionary containing the following 2 keys:
    
        - :direction: (str,required) - sort direction. Optional values: (ASC, DESC)
        - :field: (str,required) - field name of the field to sort by
    
    - :filters_logical_operator: (int,optional) - the logical operator to group the filters by. Optional values: (and, or)
    - :filters: (list of dict,optional) - list of filter objects as dictionaries containing:

        - :field: (str,required) - field name of the field to filter by
        - :value: (str,optional) - value to filter by
        - :condition_type: (str,required) - condition type to filter by. 
        
            Optional values: (eq, finset, from, gt, gteq, in, like, lt, lteq, moreq, neq, nfinset, nin, nlike, notnull, null, to)

    :return: dictionary containing a list of Order objects
    :rtype: dict
    """
    try:
        limit = params.get("limit", None)
        sort = params.get("sort", [])
        filters_logical_operator = params.get("filters_logical_operator", "")
        filters = params.get("filters", [])
        host, access_token = extract_credential(credential)
        request_params = {"searchCriteria[currentPage]": "0"}
        api_url = f"{host}/rest/default/V1/orders"
        headers = {
            "Authorization": "Bearer " + access_token
        }
        if limit:
            request_params["searchCriteria[pageSize]"] = str(limit)
            
        if sort:
            if sort[0]:
                for i, sort_dict in enumerate(sort):
                    if "direction" in sort_dict and "field" in sort_dict:
                        request_params[f"searchCriteria[sortOrders][{i}][direction]"] = sort_dict.get("direction")
                        request_params[f"searchCriteria[sortOrders][{i}][field]"] = sort_dict.get("field")
                    else:
                        raise Exception("Missing input for sort")
        
        if filters:
            if (filters_logical_operator == "and" or filters_logical_operator == "or") and filters[0]:
                if filters_logical_operator == "and":
                    for i, filters_dict in enumerate(filters):
                        if "field" in filters_dict and "condition_type" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][field]"] = filters_dict.get("field")
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][condition_type]"] = filters_dict.get("condition_type")
                        else:
                            raise Exception("Missing Input for filter")
                        if "value" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][{i}][filters][0][value]"] = filters_dict.get("value")
                elif filters_logical_operator == "or":
                    for i, filters_dict in enumerate(filters):
                        if "field" in filters_dict and "condition_type" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][field]"] = filters_dict.get("field")
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][condition_type]"] = filters_dict.get("condition_type")
                        else:
                            raise Exception("Missing Input for filter")
                        if "value" in filters_dict:
                            request_params[f"searchCriteria[filter_groups][0][filters][{i}][value]"] = filters_dict.get("value")
        
        response = requests.get(url=api_url, headers=headers, params=request_params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)




def magento_2_get_order(credential, params):
    """
    Retrieve an Order by it's ID

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :id: (int,required) - ID of the Order to be retrieved also called order 'entity_id'

    :return: The selected Order object
    :rtype: dict
    """
    try:
        if "id" in params:
            id = params["id"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/orders/{id}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.get(url=api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)




def magento_2_create_order_comment(credential, params):
    """
    Create an order comment according to the provided status History object

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :id: (int,required) - ID of the Order to be commented on
    - :statusHistory: (dict,required) - dictionary containing the values neccessary to create an order comment.

        - :comment: (str,required) - 
        - :is_customer_notified: (int,required) - Is-customer-notified flag value.
        - :is_visible_on_front: (int,required) - Is-visible-on-storefront flag value.
        - :parent_id: (int,required) - 
        - :status: (str,optional) - 
        - :entity_id: (int,optional) - Order status history ID.
        - :entity_name: (str,optional) - 
        
    
    :return: returns dictionary containing Boolean true upon successfull creation
    :rtype: dict
    """
    try:
        statusHistory = params.get("statusHistory", {})
        if statusHistory and "comment" in statusHistory and "is_customer_notified" in statusHistory and "is_visible_on_front" in statusHistory and "id" in params:
            id = params["id"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/orders/{id}/comments"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            statusHistory["parent_id"] = id
            data = {"statusHistory": statusHistory}
            response = requests.post(url=api_url, headers=headers, json=data)
            if response.status_code == 200 and response.json():
                return {"message": "Order Comment Created Successfully", "response": response.json()}
            elif response.status_code == 200 and not response.json():
                return {"message": "Error Creating Order Comment", "response": response.json()}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)





def magento_2_ship_order(credential, params):
    """
    Ship an Order by it's ID

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :id: (int,required) - ID of the Order to be Shipped

    :return: dictionary containing the id of the created shipment
    :rtype: dict
    """
    try:
        if "id" in params:
            id = params["id"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/order/{id}/ship"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.post(url=api_url, headers=headers)
            if response.status_code == 200:
                return {"message": "Order Shipped Successfully", "Created Shipment ID": response.json()}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)





def magento_2_cancel_order(credential, params):
    """
    Cancel an Order by it's ID

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :id: (int,required) - id of the Order to be Cancelled

    :return: returns dictionary containing Boolean true upon successfull deletion
    :rtype: dict
    """
    try:
        if "id" in params:
            id = params["id"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/orders/{id}/cancel"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.post(url=api_url, headers=headers)
            if response.status_code == 200 and response.json():
                return {"message": "Order Cancelled Successfully", "response": response.json()}
            elif response.status_code == 200 and not response.json():
                return {"message": "Error Canceling Order", "response": response.json()}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)





####################################### Invoices ##########################################





def magento_2_create_invoice(credential, params):
    """
    create an invoice of the Order by it's order ID

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :id: (int,required) - ID of the Order to have an invoice created for

    :return: dictionary containing the id of the created invoice
    :rtype: dict
    """
    try:
        if "id" in params:
            id = params["id"]
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/order/{id}/invoice"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            response = requests.post(url=api_url, headers=headers)
            if response.status_code == 200:
                return {"message": "Invoice Created Successfully", "Created Invoice ID": response.json()}
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)




######################################## Categories #####################################




def magento_2_create_category(credential, params):
    """
    Create a Category according to the provided Category object

    :credentials: A json dictionary containing credential parameters.
    :params: Dictionary containing parameters.

    - :category: (dict,required) - dictionary containing the values of the Category to be created as represented in a Category object.

        - :name: (str,required) - Category name
        - :id: (int,optional) - Category id.
        - :available_sort_by: (list of str,optional) - Available sort by for category.
        - :children: (str,optional) - Children ids comma separated.
        - :include_in_menu: (bool,optional) - Category is included in menu.
        - :is_active: (bool,optional) - Whether category is active
        - :level: (int,optional) - Category level
        - :parent_id: (int,optional) - Parent category ID
        - :path: (str,optional) - Category full path.
        - :position: (int,optional) - Category position
        - :custom_attributes: (list of dict,optional) - list of dictionaries with each containing:
        
            - :attribute_code: (str,required) - Attribute code
            - :value: (str,required) - Attribute code
        
    
    :return: The Created Category object
    :rtype: dict
    """
    try:
        category = params.get("category", {})
        if category and "name" in category:
            host, access_token = extract_credential(credential)
            api_url = f"{host}/rest/default/V1/categories"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-type": "application/json"
            }
            data = {"category": category}
            response = requests.post(url=api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("missing input data")
    except Exception as error:
        raise Exception(error)

