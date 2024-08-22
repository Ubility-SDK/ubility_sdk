import requests
import json
api_version = "2023-10"


def shopify_get_many_products(cred):
    """
    Retrieve multiple products from Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.

    Returns:
        list: List of products retrieved.
    """
    try:
        creds=json.loads(cred)
        if "subdomain" in creds and "apiKey" in creds and "apiPassword" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                products_data = response.json()
                return products_data
            else:
                raise Exception(
                    f"Failed to retrieve products. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_get_product(cred, params):
    """
    Retrieve product information from Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :product_id:  (str,required) - ID of the product.

    Returns:
        dict: Details of the retrieved product.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "product_id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            product_id = params["product_id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products/{product_id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                product_data = response.json()
                return product_data
            else:
                raise Exception(
                    f"Failed to retrieve product {product_id}. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_delete_product(cred, params):
    """
    Delete a product in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :product_id: (str,required) - ID of the product.

    Returns:
        dict: A message confirming the deletion of the product.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "product_id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            product_id = params["product_id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products/{product_id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.delete(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                return {"message": "Product deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete product {product_id}. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_create_product(cred, params):
    """
    Create a product in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :title: (str,required) - Title of the product.
        - :product_type: (str,optional) - Type of the product.
        - :vendor: (str,optional) - Vendor of the product.
        - :body_html: (str,optional) - Description of the product in HTML format.
        - :tags: (str,optional) - Tags associated with the product (comma-separated).
        - :published_at: (datetime,optional) - Date and time of product publication.
        - :images: (List,optional) - List of dictionaries containing image URLs for the product.
        - :sku: (str,optional) - Stock Keeping Unit (SKU) of the product.
        - :published_scope: (str,optional) - Published scope ('global' or 'web').

    Returns:
        dict: Details of the created product.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "title" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"product": {}}
            for key, value in params.items():
                if value:
                    data["product"][key] = value
            response = requests.post(
                base_url, auth=(apiKey, apiPassword), json=data, headers=headers
            )
            if response:
                product_data = response.json()
                return product_data
            else:
                raise Exception(
                    f"Failed to create the product. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_update_product(cred, params):
    """
    Update a product in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

            - :id: (str,required) - ID of the product.
            - :title: (str,optional) - Title of the product.
            - :product_type: (str,optional) - Type of the product.
            - :vendor: (str,optional) - Vendor of the product.
            - :body_html: (str,optional) - Description of the product in HTML format.
            - :tags: (str,optional) - Tags associated with the product (comma-separated).
            - :published_at: (datetime,optional) - Date and time of product publication.
            - :images: (List,optional) - List of dictionaries containing image URLs for the product.
            - :sku: (str,optional) - Stock Keeping Unit (SKU) of the product.
            - :published_scope: (str,optional) - Published scope ('global' or 'web').

    Returns:
        dict: Details of the updated product.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products/{id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"product": {}}
            for key, value in params.items():
                skip_keys = ["id"]
                if key in skip_keys:
                    continue
                if value:
                    data["product"][key] = value
            if data["product"]:
                response = requests.put(
                    base_url, auth=(apiKey, apiPassword), json=data, headers=headers
                )
                if response:
                    product_data = response.json()
                    return product_data
                else:
                    raise Exception(
                        f"Failed to update the product. Status code: {response.status_code}. Response: {response.text}"
                    )
            else:
                raise Exception("At least one field must be updated")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_update_variant_product(cred, params):
    """
    Update a variant of a product in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :product_id: (str,required) - ID of the product.
        - :variant_id: (str,required) - ID of the variant.
        - :title: (str,optional) - Title of the product.
        - :sku: (str,optional) - Stock Keeping Unit (SKU) of the product.
        - :compare_at_price: (str,optional) - The original price of the item before an adjustment or a sale.
        - :price: (str,optional) - The price of the product variant.

    Returns:
        dict: Details of the updated variant.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "product_id" in params
            and "variant_id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            product_id = params["product_id"]
            variant_id = params["variant_id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products/{product_id}/variants/{variant_id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"variant": {}}
            for key, value in params.items():
                skip_keys = ["product_id", "variant_id"]
                if key in skip_keys:
                    continue
                if value:
                    data["variant"][key] = value
            if data["variant"]:
                response = requests.put(
                    base_url, auth=(apiKey, apiPassword), json=data, headers=headers
                )
                if response:
                    variant_product_data = response.json()
                    return variant_product_data
                else:
                    raise Exception(
                        f"Failed to update the product variant. Status code: {response.status_code}. Response: {response.text}"
                    )
            else:
                raise Exception("At least one field must be updated")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_get_variant_products(cred, params):
    """
    Retrieve a list of product variants in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the product.

    Returns:
        list: List of product variants retrieved.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/products/{id}/variants.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                variant_product_data = response.json()
                return variant_product_data
            else:
                raise Exception(
                    f"Failed to retrieve variants for product {id}. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_create_variant_product(cred, params):
    """
    Create a variant for a product in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the product.
        - :inventory_policy: (str,optional) - Inventory policy ('continue' or 'deny').
        - :price: (str,optional) - Price of the variant.
        - :compare_at_price: (str,optional) - Compare at price of the variant.
        - :option1: (str,optional) - Name of the variant option.
        - :sku: (str,optional) - Stock Keeping Unit (SKU) of the variant.

    Returns:
        dict: Details of the created variant.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/2021-07/products/{id}/variants.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"variant": {}}
            for key, value in params.items():
                skip_keys = ["id"]
                if key in skip_keys:
                    continue
                if value:
                    data["variant"][key] = value
            response = requests.post(
                base_url, auth=(apiKey, apiPassword), json=data, headers=headers
            )
            if response:
                variant_product_data = response.json()
                return variant_product_data
            else:
                raise Exception(
                    f"Failed to create the product. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_get_many_customers(cred):
    """
    Retrieve a list of customers from Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.

    Returns:
        list: List of customers retrieved.
    """
    try:
        creds=json.loads(cred)
        if "subdomain" in creds and "apiKey" in creds and "apiPassword" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/customers.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                customers_data = response.json()
                return customers_data
            else:
                raise Exception(
                    f"Failed to retrieve customers. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_get_customer_by_id(cred, params):
    """
    Retrieve a single customer from Shopify.


    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the customer.

    Returns:
        dict: Details of the retrieved customer.
    """

    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/customers/{id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                customer_data = response.json()
                return customer_data
            else:
                raise Exception(
                    f"Failed to retrieve customer. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_create_customer(cred, params):
    """
    Creates a customer in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :first_name: (str,required) - First name of the customer.
        - :last_name: (str,required) - Last name of the customer.
        - :email: (str,required) - Email address of the customer.
        - :phone: (str,required) - Phone number of the customer.
        - :tags: (str,optional) - Tags associated with the customer.
        - :note: (str,optional) - Additional notes about the customer.
        - :accepts_marketing: (bool,optional) - Whether the customer accepts marketing.
        - :tax_exempt: (bool,optional) - Whether the customer is tax exempt.
        - :send_email_invite: (bool,optional) - Whether to send an email invitation to the customer).
        - :addresses: (list,optional) - List of customer addresses. Each address is a dictionary with the following fields:

            - :first_name: (str) - First name on the address.
            - :last_name: (str) - Last name on the address.
            - :company: (str) - Company name.
            - :address1: (str) - Address line 1.
            - :address2: (str) - Address line 2.
            - :city: (str) - City.
            - :zip: (str) - ZIP code.
            - :country: (str) - Country.
            - :province: (str) - Province or state.
            - :phone: (str) - Phone number for the address.

    Returns:
        dict: The created customer information.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "email" in params
            and "phone" in params
            and "first_name" in params
            and "last_name" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/customers.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"customer": {}}
            for key, value in params.items():
                if value:
                    data["customer"][key] = value
            response = requests.post(
                base_url, auth=(apiKey, apiPassword), json=data, headers=headers
            )
            if response:
                customer_data = response.json()
                return customer_data
            else:
                raise Exception(
                    f"Failed to create customer. Status code: {response.status_code}{response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_update_customer(cred, params):
    """
    Updates a customer in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the customer.
        - :first_name: (str,optional) - First name of the customer.
        - :last_name: (str,optional) - Last name of the customer.
        - :email: (str,optional) - Email address of the customer.
        - :phone: (str,optional) - Phone number of the customer.
        - :tags: (str,optional) - Tags associated with the customer.
        - :note: (str,optional) - Additional notes about the customer.
        - :accepts_marketing: (bool,optional) - Whether the customer accepts marketing.
        - :tax_exempt: (bool,optional) - Whether the customer is tax exempt.

    Returns:
        dict: The updated customer information.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/customers/{id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"customer": {}}
            for key, value in params.items():
                skip_keys = ["id"]
                if key in skip_keys:
                    continue
                if value:
                    data["customer"][key] = value
            if data["customer"]:
                response = requests.put(
                    base_url, auth=(apiKey, apiPassword), json=data, headers=headers
                )
                if response:
                    customer_data = response.json()
                    return customer_data
                else:
                    raise Exception(
                        f"Failed to update the customer. Status code: {response.status_code}. Response: {response.text}"
                    )
            else:
                raise Exception("At least one field must be updated")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_get_many_orders(cred):
    """
    Retrieve a list of orders from Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.

    Returns:
        list: List of orders retrieved.
    """
    try:
        creds=json.loads(cred)
        if "subdomain" in creds and "apiKey" in creds and "apiPassword" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/orders.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                orders_data = response.json()
                return orders_data
            else:
                raise Exception(
                    f"Failed to retrieve orders. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_get_order_by_id(cred, params):
    """
    Retrieve a single order from Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the order.

    Returns:
        dict: Details of the retrieved order.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/orders/{id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.get(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                order_data = response.json()
                return order_data
            else:
                raise Exception(
                    f"Failed to retrieve order {id}. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_delete_order(cred, params):
    """
    Delete a order in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the order.

    Returns:
        dict: A message confirming the deletion of the order.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/orders/{id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.delete(
                base_url, auth=(apiKey, apiPassword), headers=headers
            )
            if response:
                return {"message": "order deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete order {id}. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_create_order(cred, params):
    """
    Creates a order in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :line_items: (list): List of dictionaries representing line items in the order. Each dictionary should contain:

            - :title: (str) - The title of the product.
            - :variant_title: (str) - The title of the product variant.
            - :price: (str) - The price of the product.
            - :grams: (str) - The weight of the product in grams.
            - :quantity: (str) - The quantity of the product.
        - :email: (str,optional) - The email address associated with the order.
        - :note: (str,optional) - Additional notes about the order.
        - :tags: (str,optional) - Additional tags associated with the order.
        - :source_name: (str,optional) - The source of the order.
        - :send_receipt: (bool,optional) - Indicates whether to send a receipt to the customer.
        - :send_fulfillment_receipt: (bool,optional) - Indicates whether to send a fulfillment receipt to the customer.
        - :inventory_behaviour: (str,optional) - The behavior regarding inventory. ( 'bypass' or 'decrement_ignoring_policy'or 'decrement_obeying_policy' )
        - :fulfillment_status: (str,optional) - The fulfillment status of the order. ( 'fulfilled' or 'null'or 'partial' or 'restocked' )
        - :financial_status: (str,optional) - The financial status of the order. ( 'pending' or 'authorized' or 'partially_paid' or 'paid' or 'partially_refunded' or 'refunded' or 'voided' )
        - :shipping_address: (dict,optional) - Dictionary representing the shipping address.

            - :first_name: (str) - First name on the address.
            - :last_name: (str) - Last name on the address.
            - :address1: (str) - Address line 1.
            - :address2: (str) - Address line 2.
            - :city: (str) - City.
            - :zip: (str) - ZIP code.
            - :country: (str) - Country.
            - :province: (str) - Province or state.
            - :phone: (str) - Phone number for the address.
        - :billing_address: (dict,optional) - Dictionary representing the billing address.

            - :first_name: (str) - First name on the address.
            - :last_name: (str) - Last name on the address.
            - :address1: (str) - Address line 1.
            - :address2: (str) - Address line 2.
            - :city: (str) - City.
            - :zip: (str) - ZIP code.
            - :country: (str) - Country.
            - :province: (str) - Province or state.
            - :phone: (str) - Phone number for the address.
        - :location_id: (str,optional) - The location ID for the order.
        - :discount_codes: (list,optional) - List of dictionaries representing discount codes. Each dictionary should contain:

            - :code: (str): The discount code.
            - :amount: (str): The amount of the discount.
            - :type: (str): The type of the discount. ( 'fixed_amount' or 'percentage' or 'shipping' )

    Returns:
        dict: The created order information.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "line_items" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/orders.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"order": {}}
            for key, value in params.items():
                if value:
                    data["order"][key] = value
            response = requests.post(
                base_url, auth=(apiKey, apiPassword), json=data, headers=headers
            )
            if response:
                order_data = response.json()
                return order_data
            else:
                raise Exception(
                    f"Failed to create the order. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_update_order(cred, params):
    """
    Updates a order in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - ID of the order.
        - :email: (str,optional) - The email address associated with the order.
        - :note: (str,optional) - Additional notes about the order.
        - :tags: (str,optional) - Additional tags associated with the order.
        - :shipping_address: (dict,optional) - Dictionary representing the shipping address.

            - :first_name: (str) - First name on the address.
            - :last_name: (str) - Last name on the address.
            - :address1: (str) - Address line 1.
            - :address2: (str) - Address line 2.
            - :city: (str) - City.
            - :zip: (str) - ZIP code.
            - :country: (str) - Country.
            - :province: (str) - Province or state.
            - :phone: (str) - Phone number for the address.
        - :location_id: (str,optional) - The location ID for the order.
        - :source_name: (str,optional) - The source of the order.

    Returns:
        dict: The updated order information.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            id = params["id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/orders/{id}.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"order": {}}
            for key, value in params.items():
                skip_keys = ["id"]
                if key in skip_keys:
                    continue
                if value:
                    data["order"][key] = value
            if data["order"]:
                response = requests.put(
                    base_url, auth=(apiKey, apiPassword), json=data, headers=headers
                )
                if response:
                    order_data = response.json()
                    return order_data
                else:
                    raise Exception(
                        f"Failed to update the order. Status code: {response.status_code}. Response: {response.text}"
                    )
            else:
                raise Exception("At least one field must be updated")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_update_inventory_quantity(cred, params):
    """
    Updates the inventory quantity for a specific product variant in Shopify.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :available: (str,required) - Sets the available inventory quantity.
        - :inventory_item_id: (str,required) - The ID of the inventory item associated with the inventory level.
        - :location_id: (str,required) - The ID of the location that the inventory level belongs to.

    Returns:
        dict: The updated inventory quantity data.
    """
    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "inventory_item_id" in params
            and "available" in params
            and "location_id" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/inventory_levels/set.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if data:
                response = requests.post(
                    base_url, auth=(apiKey, apiPassword), json=data, headers=headers
                )
                if response:
                    inventory_quantity_data = response.json()
                    return inventory_quantity_data
                else:
                    raise Exception(
                        f"Failed to update inventory quantity. Status code: {response.status_code}. Response: {response.text}"
                    )
            else:
                raise Exception("At least one field must be updated")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def shopify_create_blog_articles(cred, params):
    """
    Creates an article for a blog.

    :param str subdomain: The subdomain of the Shopify store.
    :param str apiKey: The API key for authentication with the Shopify store.
    :param str apiPassword: The API password for authentication with the Shopify store.
    :param dict params: Dictionary containing parameters.

        - :blog_id: (str,required) - ID of the blog.
        - :title: (str,required) - The title of the article.
        - :author: (str,required) - The name of the author of the article.
        - :body_html: (str,required) - The text of the body of the article, complete with HTML markup.
        - :image: (dict,optional) - An image associated with the article.

            - :src: (str,optional) - A source URL that specifies the location of the image.
        - :summary_html: (str,optional) - The text of the summary of the article, complete with HTML markup.
        - :tags: (str,optional) - Tags are additional short descriptors formatted as a string of comma-separated values.

    Returns:
        dict: The created blog article information.
    """

    try:
        creds=json.loads(cred)
        if (
            "subdomain" in creds
            and "apiKey" in creds
            and "apiPassword" in creds
            and "blog_id" in params
            and "title" in params
            and "author" in params
            and "body_html" in params
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            apiPassword = creds["apiPassword"]
            blog_id = params["blog_id"]
            base_url = f"https://{subdomain}.myshopify.com/admin/api/{api_version}/blogs/{blog_id}/articles.json"
            headers = {
                "Content-Type": "application/json",
            }
            data = {"article": {}}
            for key, value in params.items():
                if value:
                    data["article"][key] = value
            response = requests.post(
                base_url, auth=(apiKey, apiPassword), json=data, headers=headers
            )
            if response:
                article = response.json()
                return article
            else:
                raise Exception(
                    f"Failed to create a new article. Status code: {response.status_code}. Response: {response.text}"
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)
