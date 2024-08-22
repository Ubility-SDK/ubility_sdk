import requests
import json

def woocommerce_get_many_product(creds,params):
    """
    Retrieve multiple products from WooCommerce API.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :per_page: (integer,optional) - Maximum number of items to be returned in result set. Default is 10.
    - :after: (str,optional) - Limit response to resources published after a given ISO8601 compliant date.
    - :before: (str,optional) - Limit response to resources published before a given ISO8601 compliant date.
    - :category: (str,optional) - Limit result set to products assigned a specific category ID.
    - :context: (str,optional) - Scope under which the request is made; determines fields present in response. Options: view and edit. Default is "view".
    - :featured: (bool,optional) - Limit result set to featured products. Default is False.
    - :min_price: (str,optional) - Limit result set to products based on a minimum price.
    - :max_price: (str,optional) - Limit result set to products based on a maximum price.
    - :order: (str,optional) - Order sort attribute ascending or descending. Options: asc and desc. Default is "desc".
    - :orderby: (str,optional) - Sort collection by object attribute. Options: date, id, include, title, and slug. Default is "date".
    - :search: (str,optional) - Limit results to those matching a string.
    - :sku: (str,optional) - Limit result set to products with a specific SKU.
    - :slug: (str,optional) - Limit result set to products with a specific slug.
    - :status: (str,optional) - Limit result set to products assigned a specific status. Options: any, draft, pending, private, and publish. Default is "any".
    - :stock_status: (str,optional) - Limit result set to products with specified stock status. Options: instock, outofstock, and onbackorder.
    - :tag: (str,optional) - Limit result set to products assigned a specific tag ID.
    - :tax_class: (str,optional) - Limit result set to products with a specific tax class. Default options: standard, reduced-rate, and zero-rate.
    - :type: (str,optional) - Limit result set to products assigned a specific type. Options: simple, grouped, external, and variable.

    Returns:
        list: A list containing products retrieved .
    """
    try:
        creds=json.loads(creds)
        if "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/products"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth, json=data)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_get_product(creds,params):
    """
    Retrieve a product from WooCommerce API by ID.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :product_id: (int,required) - The ID of the product to retrieve.

    Returns:
        dict: A dictionary containing the retrieved product information.
    """
    try:
        creds=json.loads(creds)
        if "product_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            product_id = params["product_id"]
            url = f"{baseUrl}/wp-json/wc/v3/products/{product_id}"
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_create_product(creds,params):
    """
    Create a product on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :name: (str,required) -  Product name.
    - :backorders: (str,optional) -  If managing stock, this controls if backorders are allowed. Options: no, notify, and yes. Default is no.
    - :button_text: (str,optional) -  Product external button text. Only for external products.
    - :catalog_visibility: (str,optional) -  Catalog visibility. Options: visible, catalog, search, and hidden. Default is visible.
    - :categories: (list,optional) - List of categories.
    - :cross_sell_ids: (list,optional) - List of cross-sell products IDs.
    - :date_on_sale_from: (str,optional) -  Start date of sale price, in the site's timezone.
    - :date_on_sale_to: (str,optional) -  End date of sale price, in the site's timezone.
    - :description: (str,optional) -  Product description.
    - :downloadable: (bool,optional) -  If the product is downloadable. Default is false.
    - :external_url: (str,optional) -  Product external URL. Only for external products.
    - :featured: (bool,optional) -  Featured product. Default is false.
    - :manage_stock: (bool,optional) -  Stock management at product level. Default is false.
    - :menu_order: (int,optional) -  Menu order, used to custom sort products.
    - :parent_id: (int,optional) -  Product parent ID.
    - :purchase_note: (str,optional) -  Purchase Note - Optional note to send the customer after purchase.
    - :regular_price: (str,optional) -  Product regular price.
    - :reviews_allowed: (bool,optional) -  Allow reviews. Default is true.
    - :sale_price: (str,optional) -  Product sale price.
    - :shipping_class: (str,optional) -  Shipping class slug.
    - :short_description: (str,optional) -  Product short description.
    - :sku: (str,optional) -  Unique identifier.
    - :slug: (str,optional) -  Product slug.
    - :sold_individually: (bool,optional) -  Allow one item to be bought in a single order. Default is false.
    - :status: (str,optional) -  Product status (post status). Options: draft, pending, private, and publish. Default is publish.
    - :stock_quantity: (int,optional) -  Stock quantity.
    - :stock_status: (str,optional) -  Controls the stock status of the product. Options: instock, outofstock, onbackorder. Default is instock.
    - :tags: (list,optional) - List of tags.
    - :tax_class: (str,optional) -  Tax class.
    - :tax_status: (str,optional) -  Tax status. Options: taxable, shipping, and none. Default is taxable.
    - :type: (str,optional) -  Product type. Options: simple, grouped, external, and variable. Default is simple.
    - :upsell_ids: (list,optional) - List of up-sell products IDs.
    - :virtual: (bool,optional) -  If the product is virtual. Default is false.
    - :weight: (str,optional) -  Product weight.
    - :dimensions: (dict,optional) - Product dimensions: length, width, height.
    - :images: (list,optional) - List of images .

        - :src: (str,optional) -  Image URL.
        - :name: (str,optional) -  Image name.
        - :alt: (str,optional) -  Image alternative text.

    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "name" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/products"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_update_product(creds,params):
    """
    Update a product on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :product_id: (int,required) - The ID of the product to update.
    - :name: (str,optional) -  Product name.
    - :backorders: (str,optional) -  If managing stock, this controls if backorders are allowed. Options: no, notify, and yes. Default is no.
    - :button_text: (str,optional) -  Product external button text. Only for external products.
    - :catalog_visibility: (str,optional) -  Catalog visibility. Options: visible, catalog, search, and hidden. Default is visible.
    - :categories: (list,optional) - List of categories.
    - :cross_sell_ids: (list,optional) - List of cross-sell products IDs.
    - :date_on_sale_from: (str,optional) -  Start date of sale price, in the site's timezone.
    - :date_on_sale_to: (str,optional) -  End date of sale price, in the site's timezone.
    - :description: (str,optional) -  Product description.
    - :downloadable: (bool,optional) -  If the product is downloadable. Default is false.
    - :external_url: (str,optional) -  Product external URL. Only for external products.
    - :featured: (bool,optional) -  Featured product. Default is false.
    - :manage_stock: (bool,optional) -  Stock management at product level. Default is false.
    - :menu_order: (int,optional) -  Menu order, used to custom sort products.
    - :parent_id: (int,optional) -  Product parent ID.
    - :purchase_note: (str,optional) -  Purchase Note - Optional note to send the customer after purchase.
    - :regular_price: (str,optional) -  Product regular price.
    - :reviews_allowed: (bool,optional) -  Allow reviews. Default is true.
    - :sale_price: (str,optional) -  Product sale price.
    - :shipping_class: (str,optional) -  Shipping class slug.
    - :short_description: (str,optional) -  Product short description.
    - :sku: (str,optional) -  Unique identifier.
    - :slug: (str,optional) -  Product slug.
    - :sold_individually: (bool,optional) -  Allow one item to be bought in a single order. Default is false.
    - :status: (str,optional) -  Product status (post status). Options: draft, pending, private, and publish. Default is publish.
    - :stock_quantity: (int,optional) -  Stock quantity.
    - :stock_status: (str,optional) -  Controls the stock status of the product. Options: instock, outofstock, onbackorder. Default is instock.
    - :tags: (list,optional) - List of tags.
    - :tax_class: (str,optional) -  Tax class.
    - :tax_status: (str,optional) -  Tax status. Options: taxable, shipping, and none. Default is taxable.
    - :type: (str,optional) -  Product type. Options: simple, grouped, external, and variable. Default is simple.
    - :upsell_ids: (list,optional) - List of up-sell products IDs.
    - :virtual: (bool,optional) -  If the product is virtual. Default is false.
    - :weight: (str,optional) -  Product weight.
    - :dimensions: (dict,optional) - Product dimensions: length, width, height.
    - :images: (list,optional) - List of images .

        - :src: (str,optional) -  Image URL.
        - :name: (str,optional) -  Image name.
        - :alt: (str,optional) -  Image alternative text.

    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "product_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            product_id = params["product_id"]
            url = f"{baseUrl}/wp-json/wc/v3/products/{product_id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.put(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_delete_product(creds,params):
    """
    Delete a product on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :product_id: (int,required) - The ID of the product to delete.

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "product_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            product_id = params["product_id"]
            url = f"{baseUrl}/wp-json/wc/v3/products/{product_id}?force=true"
            auth = (consumerKey, consumerSecret)
            response = requests.delete(url, auth=auth)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_get_many_customer(creds,params):
    """
    Retrieve multiple customers from WooCommerce API.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :per_page: (integer,optional) - Maximum number of items to be returned in result set. Default is 10.
    - :email: (str,optional) - The email address for the customer.
    - :order: (str,optional) - Order sort attribute ascending or descending. Options: asc and desc. Default is asc.
    - :orderby: (str,optional) - Sort collection by object attribute. Options: id, include, name and registered_date. Default is name.

    Returns:
        list: A list containing customers retrieved from the API according to specified parameters.
    """
    try:
        creds=json.loads(creds)
        if "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/customers"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth, json=data)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_get_customer(creds,params):
    """
    Retrieve a customer from WooCommerce API by ID.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :customer_id: (int,required) - The ID of the customer to retrieve.

    Returns:
        dict: A dictionary containing the retrieved customer information.
    """
    try:
        creds=json.loads(creds)
        if "customer_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            customer_id = params["customer_id"]
            url = f"{baseUrl}/wp-json/wc/v3/customers/{customer_id}"
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


# def woocommerce_create_customer(creds,params):
#     """
#     Create a customer on WooCommerce.

#     :param str baseUrl: The base URL of the WooCommerce store.
#     :param str consumerKey: The consumer key for WooCommerce API authentication.
#     :param str consumerSecret: The consumer secret for WooCommerce API authentication.
#     :param dict params: Dictionary containing parameters.

#     - :email: (str,required) -  The email address for the customer.
#     - :first_name: (str,optional) - Customer first name.
#     - :last_name: (str,optional) - Customer last name.
#     - :username: (str,optional) - Customer login name.
#     - :password: (str,optional) - Customer password.
#     - :billing: (dict,optional) - Dict of billing address data

#         - :first_name: (str,optional) - First name.
#         - :last_name: (str,optional) - Last name.
#         - :company: (str,optional) - Company name.
#         - :address_1: (str,optional) - Address line 1
#         - :address_2: (str,optional) - Address line 2
#         - :city: (str,optional) - City name.
#         - :state: (str,optional) - ISO code or name of the state, province or district.
#         - :postcode: (str,optional) - Postal code.
#         - :country: (str,optional) - ISO code of the country.
#         - :email: (str,optional) - Email address.
#         - :phone: (str,optional) - Phone number.

#     - :shipping: (dict,optional) - Dict of shipping address data

#         - :first_name: (str,optional) - First name.
#         - :last_name: (str,optional) - Last name.
#         - :company: (str,optional) - Company name.
#         - :address_1: (str,optional) - Address line 1
#         - :address_2: (str,optional) - Address line 2
#         - :city: (str,optional) - City name.
#         - :state: (str,optional) - ISO code or name of the state, province or district.
#         - :postcode: (str,optional) - Postal code.
#         - :country: (str,optional) - ISO code of the country.
#         - :email: (str,optional) - Email address.
#         - :phone: (str,optional) - Phone number.

#     - :meta_data: (list,optional) - List of metadata (key, value).

#     Returns:
#         dict: A dictionary containing the response data from the WooCommerce API.
#     """
#     try:
#         creds=json.loads(creds)
#         if "email" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
#             baseUrl = creds["baseUrl"]
#             consumerKey = creds["consumerKey"]
#             consumerSecret = creds["consumerSecret"]
#             url = f"{baseUrl}/wp-json/wc/v3/customers"
#             data = {}
#             for key, value in params.items():
#                 if value:
#                     data[key] = value
#             auth = (consumerKey, consumerSecret)
#             headers = {"Content-Type": "application/json"}
#             response = requests.post(url, auth=auth, json=data, headers=headers)
#             if response:
#                 return response.json()
#             else:
#                 raise Exception(response.json())
#         else:
#             raise Exception("Missing Input Data")
#     except Exception as error:
#         raise Exception(error)

def woocommerce_update_customer(creds,params):
    """
    Update a customer on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :customer_id: (int,required) - The ID of the customer to update.
    - :first_name: (str,optional) - Customer first name.
    - :last_name: (str,optional) - Customer last name.
    - :billing: (dict,optional) - Dict of billing address data

        - :first_name: (str,optional) - First name.
        - :last_name: (str,optional) - Last name.
        - :company: (str,optional) - Company name.
        - :address_1: (str,optional) - Address line 1
        - :address_2: (str,optional) - Address line 2
        - :city: (str,optional) - City name.
        - :state: (str,optional) - ISO code or name of the state, province or district.
        - :postcode: (str,optional) - Postal code.
        - :country: (str,optional) - ISO code of the country.
        - :email: (str,optional) - Email address.
        - :phone: (str,optional) - Phone number.

    - :shipping: (dict,optional) - Dict of shipping address data

        - :first_name: (str,optional) - First name.
        - :last_name: (str,optional) - Last name.
        - :company: (str,optional) - Company name.
        - :address_1: (str,optional) - Address line 1
        - :address_2: (str,optional) - Address line 2
        - :city: (str,optional) - City name.
        - :state: (str,optional) - ISO code or name of the state, province or district.
        - :postcode: (str,optional) - Postal code.
        - :country: (str,optional) - ISO code of the country.
        - :email: (str,optional) - Email address.
        - :phone: (str,optional) - Phone number.

    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "customer_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            customer_id = params["customer_id"]
            url = f"{baseUrl}/wp-json/wc/v3/customers/{customer_id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.put(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_delete_customer(creds,params):
    """
    Delete a customer on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :customer_id: (int,required) - The ID of the customer to delete.

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "customer_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            customer_id = params["customer_id"]
            url = f"{baseUrl}/wp-json/wc/v3/customers/{customer_id}?force=true"
            auth = (consumerKey, consumerSecret)
            response = requests.delete(url, auth=auth)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_get_many_order(creds,params):
    """
    Retrieve multiple orders from WooCommerce API.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :per_page: (integer,optional) - Maximum number of items to be returned in result set. Default is 10.
    - :search: (str,optional) - Limit results to those matching a string.
    - :after: (str,optional) - Limit response to resources published after a given ISO8601 compliant date.
    - :before: (str,optional) - Limit response to resources published before a given ISO8601 compliant date.
    - :customer: (integer,optional) - Limit result set to orders assigned a specific customer.
    - :product: (integer,optional) - Limit result set to orders assigned a specific product.
    - :dp: (integer,optional) - Number of decimal points to use in each resource. Default is 2.
    - :order: (str,optional) - Order sort attribute ascending or descending. Options: asc and desc. Default is desc.
    - :orderby: (str,optional) - Sort collection by object attribute. Options: date, id, include, title and slug. Default is date.
    - :status: (str,optional) - Limit result set to orders assigned a specific status. Options: any, pending, processing, on-hold, completed, cancelled, refunded, failed and trash. Default is any.

    Returns:
        list: A list containing orders retrieved from the API according to specified parameters.
    """
    try:
        creds=json.loads(creds)
        if "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/orders"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth, json=data)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data") 
    except Exception as error:
        raise Exception(error)

def woocommerce_get_order(creds,params):
    """
    Retrieve a order from WooCommerce API by ID.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :order_id: (int,required) - The ID of the order to retrieve.

    Returns:
        dict: A dictionary containing the retrieved order information.
    """
    try:
        creds=json.loads(creds)
        if "order_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            order_id = params["order_id"]
            url = f"{baseUrl}/wp-json/wc/v3/orders/{order_id}"
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_create_order(creds,params):
    """
    Create a order on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :status: (str,optional) - Order status. Options: pending, processing, on-hold, completed, cancelled, refunded, failed and trash. Default is pending.
    - :currency: (str,optional) - Currency the order was created with, in ISO format. Options: AED, AFN, ALL,... Default is USD.
    - :parent_id: (integer,optional) - Parent order ID.
    - :payment_method: (string,optional) - Payment method ID.
    - :payment_method_title: (string,optional) - Payment method title.
    - :set_paid: (boolean,optional) - Define if the order is paid. It will set the status to processing and reduce stock items. Default is false.
    - :customer_id: (integer,optional) - User ID who owns the order. 0 for guests. Default is 0.
    - :customer_note: (string,optional) - Note left by customer during checkout.
    - :transaction_id: (string,optional) - Unique transaction ID.
    - :line_items: (array,optional) - Line items data.

        - :name: (str,optional) - Product name.
        - :product_id: (integer,optional) - Product ID.
        - :variation_id: (integer,optional) - Variation ID, if applicable.
        - :quantity: (integer,optional) - Quantity ordered.
        - :tax_class: (str,optional) - Slug of the tax class of product.
        - :subtotal: (str,optional) - Line subtotal (before discounts).
        - :total: (str,optional) - Line total (after discounts).

    - :shipping_lines: (array,optional) - Shipping lines data.

        - :method_title: (str,optional) - Shipping method name.
        - :method_id: (str,optional) - Shipping method ID.
        - :total: (str,optional) - Line total (after discounts).
        - :meta_data: (list,optional) - List of metadata (key, value).

    - :fee_lines: (array,optional) - Fee lines data.

        - :name: (str,optional) - Fee name.
        - :tax_class: (str,optional) - Tax class of fee.
        - :tax_status: (str,optional) - Tax status of fee. Options: taxable and none.
        - :total: (str,optional) - Line total (after discounts).
        - :meta_data: (list,optional) - List of metadata (key, value).    

    - :coupon_lines: (array,optional) - Coupons line data.

        - :code: (str,optional) - Coupon code.
        - :meta_data: (list,optional) - List of metadata (key, value).   

    - :billing: (dict,optional) - Dict of billing address data

        - :first_name: (str,optional) - First name.
        - :last_name: (str,optional) - Last name.
        - :company: (str,optional) - Company name.
        - :address_1: (str,optional) - Address line 1
        - :address_2: (str,optional) - Address line 2
        - :city: (str,optional) - City name.
        - :state: (str,optional) - ISO code or name of the state, province or district.
        - :postcode: (str,optional) - Postal code.
        - :country: (str,optional) - ISO code of the country.
        - :email: (str,optional) - Email address.
        - :phone: (str,optional) - Phone number.

    - :shipping: (dict,optional) - Dict of shipping address data

        - :first_name: (str,optional) - First name.
        - :last_name: (str,optional) - Last name.
        - :company: (str,optional) - Company name.
        - :address_1: (str,optional) - Address line 1
        - :address_2: (str,optional) - Address line 2
        - :city: (str,optional) - City name.
        - :state: (str,optional) - ISO code or name of the state, province or district.
        - :postcode: (str,optional) - Postal code.
        - :country: (str,optional) - ISO code of the country.
        - :email: (str,optional) - Email address.
        - :phone: (str,optional) - Phone number.

    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/orders"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_update_order(creds,params):
    """
    Update a order on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :order_id: (int,required) - The ID of the order to update.
    - :status: (str,optional) - Order status. Options: pending, processing, on-hold, completed, cancelled, refunded, failed and trash. Default is pending.
    - :currency: (str,optional) - Currency the order was created with, in ISO format. Options: AED, AFN, ALL,... Default is USD.
    - :parent_id: (integer,optional) - Parent order ID.
    - :payment_method: (string,optional) - Payment method ID.
    - :payment_method_title: (string,optional) - Payment method title.
    - :customer_id: (integer,optional) - User ID who owns the order. 0 for guests. Default is 0.
    - :customer_note: (string,optional) - Note left by customer during checkout.
    - :transaction_id: (string,optional) - Unique transaction ID.
    - :line_items: (array,optional) - Line items data.

        - :name: (str,optional) - Product name.
        - :product_id: (integer,optional) - Product ID.
        - :variation_id: (integer,optional) - Variation ID, if applicable.
        - :quantity: (integer,optional) - Quantity ordered.
        - :tax_class: (str,optional) - Slug of the tax class of product.
        - :subtotal: (str,optional) - Line subtotal (before discounts).
        - :total: (str,optional) - Line total (after discounts).
        - :meta_data: (list,optional) - List of metadata (key, value).

    - :shipping_lines: (array,optional) - Shipping lines data.

        - :method_title: (str,optional) - Shipping method name.
        - :method_id: (str,optional) - Shipping method ID.
        - :total: (str,optional) - Line total (after discounts).
        - :meta_data: (list,optional) - List of metadata (key, value).

    - :fee_lines: (array,optional) - Fee lines data.

        - :name: (str,optional) - Fee name.
        - :tax_class: (str,optional) - Tax class of fee.
        - :tax_status: (str,optional) - Tax status of fee. Options: taxable and none.
        - :total: (str,optional) - Line total (after discounts).
        - :meta_data: (list,optional) - List of metadata (key, value).    

    - :coupon_lines: (array,optional) - Coupons line data.

        - :code: (str,optional) - Coupon code.
        - :meta_data: (list,optional) - List of metadata (key, value).   

    - :billing: (dict,optional) - Dict of billing address data

        - :first_name: (str,optional) - First name.
        - :last_name: (str,optional) - Last name.
        - :company: (str,optional) - Company name.
        - :address_1: (str,optional) - Address line 1
        - :address_2: (str,optional) - Address line 2
        - :city: (str,optional) - City name.
        - :state: (str,optional) - ISO code or name of the state, province or district.
        - :postcode: (str,optional) - Postal code.
        - :country: (str,optional) - ISO code of the country.
        - :email: (str,optional) - Email address.
        - :phone: (str,optional) - Phone number.

    - :shipping: (dict,optional) - Dict of shipping address data

        - :first_name: (str,optional) - First name.
        - :last_name: (str,optional) - Last name.
        - :company: (str,optional) - Company name.
        - :address_1: (str,optional) - Address line 1
        - :address_2: (str,optional) - Address line 2
        - :city: (str,optional) - City name.
        - :state: (str,optional) - ISO code or name of the state, province or district.
        - :postcode: (str,optional) - Postal code.
        - :country: (str,optional) - ISO code of the country.
        - :email: (str,optional) - Email address.
        - :phone: (str,optional) - Phone number.

    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "order_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            order_id = params["order_id"]
            url = f"{baseUrl}/wp-json/wc/v3/orders/{order_id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.put(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)

def woocommerce_delete_order(creds,params):
    """
    Delete a order on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :order_id: (int,required) - The ID of the order to delete.

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "order_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            order_id = params["order_id"]
            url = f"{baseUrl}/wp-json/wc/v3/orders/{order_id}?force=true"
            auth = (consumerKey, consumerSecret)
            response = requests.delete(url, auth=auth)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_create_order_note(creds,params):
    """
    Create a note for a specific order in WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :order_id: (int,required) - The ID of the order.
    - :note: (str,optional) - Order note content.
    - :customer_note: (boolean,optional) - If true, the note will be shown to customers and they will be notified. If false, the note will be for admin reference only. Default is false.
    - :added_by_user: (boolean,optional) - If true, this note will be attributed to the current user. If false, the note will be attributed to the system. Default is false

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "order_id" in params and "note" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            order_id = params["order_id"]
            url = f"{baseUrl}/wp-json/wc/v3/orders/{order_id}/notes"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_get_many_order_note(creds,params):
    """
    Retrieves multiple order notes from WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :order_id: (integer,optional) - The ID of the order.
    - :context: (str,optional) - Scope under which the request is made; determines fields present in response. Options: view and edit. Default is view.
    - :type: (str,optional) - Limit result to customers or internal notes. Options: any, customer and internal. Default is any.

    Returns:
        list: A list of order notes.
    """
    try:
        creds=json.loads(creds)
        if "order_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            order_id = params["order_id"]
            url = f"{baseUrl}/wp-json/wc/v3/orders/{order_id}/notes"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth, json=data)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_get_many_coupon(creds,params):
    """
    Retrieves multiple coupons from WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :per_page: (integer,optional) - Maximum number of items to be returned in result set. Default is 10.

    Returns:
        list: A list of coupons.
    """
    try:
        creds=json.loads(creds)
        if "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/coupons"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            response = requests.get(url, auth=auth, json=data)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_create_coupon(creds,params):
    """
    Create a coupon in WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :code: (str,required) - Coupon code.
    - :amount: (str,required) - The amount of discount. Should always be numeric, even if setting a percentage.
    - :discount_type: (str,required) - Determines the type of discount that will be applied. Options: percent, fixed_cart and fixed_product. Default is fixed_cart.
    - :date_expires: (str,optional) - The date the coupon expires, in the site's timezone.
    - :description: (str,optional) - Coupon description.
    - :individual_use: (boolean,optional) - If true, the coupon can only be used individually. Other applied coupons will be removed from the cart. Default is false.
    - :usage_limit: (integer,optional) - How many times the coupon can be used in total.
    - :usage_limit_per_user: (integer,optional) - How many times the coupon can be used per customer.
    - :limit_usage_to_x_items: (integer,optional) - Max number of items in the cart the coupon can be applied to.
    - :free_shipping: (boolean,optional) - If true and if the free shipping method requires a coupon, this coupon will enable free shipping. Default is false.
    - :exclude_sale_items: (boolean,optional) - If true, this coupon will not be applied to items that have sale prices. Default is false.
    - :minimum_amount: (str,optional) - Minimum order amount that needs to be in the cart before coupon applies.
    - :maximum_amount: (str,optional) - Maximum order amount allowed when using the coupon.
    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            url = f"{baseUrl}/wp-json/wc/v3/coupons"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def woocommerce_update_coupon(creds,params):
    """
    Update a coupon on WooCommerce.

    :param str baseUrl: The base URL of the WooCommerce store.
    :param str consumerKey: The consumer key for WooCommerce API authentication.
    :param str consumerSecret: The consumer secret for WooCommerce API authentication.
    :param dict params: Dictionary containing parameters.

    - :coupon_id: (int,required) - The ID of the coupon to update.
    - :code: (str,optional) - Coupon code.
    - :amount: (str,optional) - The amount of discount. Should always be numeric, even if setting a percentage.
    - :discount_type: (str,optional) - Determines the type of discount that will be applied. Options: percent, fixed_cart and fixed_product. Default is fixed_cart.
    - :date_expires: (str,optional) - The date the coupon expires, in the site's timezone.
    - :description: (str,optional) - Coupon description.
    - :individual_use: (boolean,optional) - If true, the coupon can only be used individually. Other applied coupons will be removed from the cart. Default is false.
    - :usage_limit: (integer,optional) - How many times the coupon can be used in total.
    - :usage_limit_per_user: (integer,optional) - How many times the coupon can be used per customer.
    - :limit_usage_to_x_items: (integer,optional) - Max number of items in the cart the coupon can be applied to.
    - :free_shipping: (boolean,optional) - If true and if the free shipping method requires a coupon, this coupon will enable free shipping. Default is false.
    - :exclude_sale_items: (boolean,optional) - If true, this coupon will not be applied to items that have sale prices. Default is false.
    - :minimum_amount: (str,optional) - Minimum order amount that needs to be in the cart before coupon applies.
    - :maximum_amount: (str,optional) - Maximum order amount allowed when using the coupon.
    - :meta_data: (list,optional) - List of metadata (key, value).

    Returns:
        dict: A dictionary containing the response data from the WooCommerce API.
    """
    try:
        creds=json.loads(creds)
        if "coupon_id" in params and "baseUrl" in creds and "consumerKey" in creds and "consumerSecret" in creds:
            baseUrl = creds["baseUrl"]
            consumerKey = creds["consumerKey"]
            consumerSecret = creds["consumerSecret"]
            coupon_id = params["coupon_id"]
            url = f"{baseUrl}/wp-json/wc/v3/coupons/{coupon_id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            auth = (consumerKey, consumerSecret)
            headers = {"Content-Type": "application/json"}
            response = requests.put(
                url, auth=auth, json=data, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)
