import json
import requests
import base64
status=[200, 201, 202, 204, 206, 207, 208]

def generate_token(username,password):
    try:
        auth_str = username+':'+password
        token = base64.b64encode(auth_str.encode()).decode()
        return token
    except Exception as e:
        raise Exception(e)
#####################################################################################


def wordpress_create_post(params,cred):
    """
    Create a new WordPress post.

    :param dict params:
        - title (str): Title of the post. (required)
        - author (int): ID of the author for the post. (optional)
        - content (str): Content of the post. (optional)
        - slug (str): Slug for the post. (optional)
        - password (str): Password for password-protected post. (optional)
        - status (str): Status of the post. (optional)
        - comment_status (str): Comment status for the post. (optional)
        - ping_status (str): Ping status for the post. (optional)
        - format (str): Format for the post. (optional)
        - categories (int): Category ID for the post. (optional)
        - tags (int): Tag ID for the post. (optional)
        - sticky (bool): Whether the post should be sticky. (optional)

    :param str base_url: Base URL of the WordPress site. (required)

    :param str token: Authentication token for accessing the WordPress API. (required)

    :return: Information about the created WordPress post.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'title' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/posts"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to create a new post.")
        else:
            raise Exception('Missing parameters.')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")
    
def wordpress_get_post(params,cred):
    """
    Retrieve information about a WordPress post.

    :param dict params:
        - post_id (int): ID of the post to retrieve. (required)
        - context (str): Optional parameter to specify the context. (optional)
        - password (str): Optional parameter for password-protected posts. (optional)

    :param str base_url: Base URL of the WordPress site. (required)

    :param str token: Authentication token for accessing the WordPress API. (required)

    :return: Information about the retrieved WordPress post.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'post_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            
            api_url = f"{base_url}/wp-json/wp/v2/posts/{params2['post_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to retrieve the post.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")
    

def wordpress_get_posts(params,cred):
    """
    Retrieve WordPress posts based on specified parameters.

    :param dict params:
        - context (str): Context for the posts. (optional)
        - search (str): Search term for posts. (optional)
        - author (int): ID of the author for the posts. (optional)
        - order (str): Order of the posts. (optional)
        - orderby (str): Field to order the posts by. (optional)
        - status (str): Status of the posts. (optional)
        - sticky (bool): Whether the posts should be sticky. (optional)
        - categories (int): Category ID for the posts. (optional)
        - tags (int): Tag ID for the posts. (optional)

    :param str base_url: Base URL of the WordPress site. (required)

    :param str token: Authentication token for accessing the WordPress API. (required)

    :return: Information about the retrieved WordPress posts.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/posts"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in status:
                posts_data = response.json()
                return posts_data
            else:
                raise Exception(f"Failed to retrieve posts.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_update_post(params,cred):
    """
    Update a WordPress post based on specified parameters.

    :param dict params:
        - post_id (int): ID of the post to be updated. (required)
        - author (int): ID of the author for the post. (optional)
        - title (str): Title of the post. (optional)
        - content (str): Content of the post. (optional)
        - slug (str): Slug of the post. (optional)
        - password (str): Password for the post. (optional)
        - status (str): Status of the post. (optional)
        - comment_status (str): Comment status for the post. (optional)
        - ping_status (str): Ping status for the post. (optional)
        - format (str): Format for the post. (optional)
        - categories (int): Category ID for the post. (optional)
        - tags (int): Tag ID for the post. (optional)
        - sticky (bool): Whether the post should be sticky. (optional)

    :param str base_url: Base URL of the WordPress site. (required)

    :param str token: Authentication token for accessing the WordPress API. (required)

    :return: Information about the updated WordPress post.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'post_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/posts/{params2['post_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to update the post.")
        else:
            raise Exception('Missing parameters')   
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_delete_post(params,cred):
    """
    Delete a WordPress post based on specified parameters.

    :param dict params:
        - post_id (int): ID of the post to be deleted. (required)
        - force (bool): Whether to force delete the post.(optional)

    :param str base_url: Base URL of the WordPress site. (required)

    :param str token: Authentication token for accessing the WordPress API. (required)

    :return: Success message if post is deleted successfully.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'post_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/posts/{params2['post_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(api_url, headers=headers)
            if response.status_code in status:
                return 'Post deleted successfully.'
            else:
                raise Exception(f"Failed to delete the post.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordress_get_users(params,cred):
    """
Retrieve WordPress users based on specified parameters.

:param dict params:
    - context (str): Scope under which the request is made. (optional)
    - search (str): Search term(s) to retrieve users. (optional)
    - order (str): Order of the users. (optional)
    - orderby (str): Field to order users by. (optional)

:param str base_url: Base URL of the WordPress site. (required)

:param str token: Authentication token for accessing the WordPress API. (required)

:return: User data based on the specified parameters.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/users"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to retrieve users.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_get_user(params,cred):
    """
    Retrieve information about a WordPress user based on specified parameters.

    :param dict params:
        - user_id (int): ID of the user to be retrieved. (required)
        - context (str): Optional parameter to specify the context. (optional)

    :param str base_url: Base URL of the WordPress site. (required)

    :param str token: Authentication token for accessing the WordPress API. (required)

    :return: User information.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'user_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/posts/{params2['user_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to retrieve user.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_update_user(params,cred):
    """
Update a WordPress user based on specified parameters.

:param dict params:
    - user_id (int): ID of the user to be updated. (required)
    - name (str): Display name of the user. (optional)
    - first_name (str): First name of the user. (optional)
    - last_name (str): Last name of the user. (optional)
    - description (str): Description of the user. (optional)
    - url (str): URL of the user. (optional)
    - email (str): Email address of the user. (optional)
    - password (str): Password for the user. (optional)

:param str base_url: Base URL of the WordPress site. (required)

:param str token: Authentication token for accessing the WordPress API. (required)

:return: User data after the update.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'user_id'in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/users/{params2['user_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.put(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to update user.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_create_user(params,cred):
    """
Create a new WordPress user based on specified parameters.

:param dict params:
    - username (str): Username for the new user. (required)
    - email (str): Email address for the new user. (required)
    - password (str): Password for the new user. (required)
    - name (str): Display name of the new user. (optional)
    - first_name (str): First name of the new user. (optional)
    - last_name (str): Last name of the new user. (optional)
    - description (str): Description of the new user. (optional)
    - url (str): URL of the new user. (optional)
    - nickname (str): Nickname of the new user. (optional)
    - slug (str): Slug for the new user. (optional)

:param str base_url: Base URL of the WordPress site. (required)

:param str token: Authentication token for accessing the WordPress API. (required)

:return: User data after creation.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'username' in params and 'email' in params and 'password' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds :
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/users"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(api_url, json=params2 , headers=headers)

            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to create user.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_delete_user(params,cred):
    """
Delete a WordPress user based on specified parameters.

:param dict params:
    - user_id (int): ID of the user to be deleted. (required)
    - reassign (int): ID of the user to reassign posts to. (required)

:param str base_url: Base URL of the WordPress site. (required)

:param str token: Authentication token for accessing the WordPress API.(required)

:return: Success message if user is deleted successfully.
:rtype: str
    """

    try:
        creds=json.loads(cred)
        if 'user_id' in params and 'reassign' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:    
            params2 = {'force':True,}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/users/{params2['user_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.delete(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return 'User deleted successfully'
            elif response.status_code == 404:
                raise Exception('User not found')
            else:
                raise Exception(f"Failed to delete user.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_create_categorie(params,cred):
    """
Create a new WordPress category based on specified parameters.

:param dict params:
    - name (str): Name of the category. (required)
    - description (str): Description of the category.(optional)
    - slug (str): Slug for the category.(optional)

:param str base_url: Base URL of the WordPress site. (required)

:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the created category.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'name' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/categories"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to create category.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_get_categories(params,cred):
    """
Retrieve WordPress categories based on specified parameters.

:param dict params:
    - context (str): Optional parameter to specify the context. (optional)
    - search (str): Search term(s) to retrieve specific categories. (optional)
    - order (str): Order sort attribute ascending or descending. (optional)
    - orderby (str): Sort categories by a specific field. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the retrieved categories.
:rtype: dict
    """
    try:
        creds=json.loads(cred)    
        if 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/categories"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to fetch categories.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_get_categorie(params,cred):
    """
Retrieve information about a specific WordPress category based on the category ID.

:param dict params:
    - categorie_id (int): ID of the category to retrieve information. (required)
    - context (str): Optional parameter to specify the context. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the specified category.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'categorie_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/categories/{params2['categorie_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to fetch categorie.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_update_categorie(params,cred):
    """
Update information about a specific WordPress category based on the category ID.

:param dict params:
    - categorie_id (int): ID of the category to be updated. (required)
    - name (str): New name for the category. (optional)
    - description (str): New description for the category. (optional)
    - slug (str): New slug for the category. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the updated category.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'categorie_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/categories/{params2['categorie_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.put(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to update categorie.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_delete_categorie(params,cred):
    """
Delete a WordPress category based on specified parameters.

:param dict params:
    - categorie_id (int): ID of the category to be deleted. (required)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Success message if the category is deleted successfully.
:rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'categorie_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
                params2 = {'force':True,}
                token=generate_token(creds['username'],creds['applicationPassword'])
                base_url=creds['baseUrl']
                for key, value in params.items():
                    if value:
                        params2[key] = value
                api_url = f"{base_url}/wp-json/wp/v2/categories/{params2['categorie_id']}"
                headers = {
                    'Authorization': f'Bearer {token}',
                }
                response = requests.delete(api_url,params=params2, headers=headers)
                if response.status_code in status:
                    return 'Deleted Successfully'
                else:
                    raise Exception(f"Failed to delete categorie.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_get_tags(params,cred):
    """
Retrieve WordPress tags based on specified parameters.

:param dict params:
    - context (str): Optional parameter to specify the context. (optional)
    - search (str): Search term(s) to retrieve specific tags. (optional)
    - order (str): Order the tags by a specific parameter. (optional)
    - orderby (str): Sort tags by a specific parameter. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: List of tags matching the specified parameters.
:rtype: dict
"""
    try:
        creds=json.loads(cred)
        if 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/tags"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to fetch tags.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_create_tag(params,cred):
    """
Create a new WordPress tag based on specified parameters.

:param dict params:
    - name (str): Name of the new tag. (required)
    - description (str): Description of the new tag. (optional)
    - slug (str): Slug for the new tag. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the created tag.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'name'in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/tags"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to create tag.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_get_tag(params,cred):
    """
Retrieve information about a WordPress tag based on specified parameters.

:param dict params:
    - tag_id (int): ID of the tag to be retrieved. (required)
    - context (str): Optional parameter to specify the context. (optional)


:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the specified tag.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'tag_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/tags/{params2['tag_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to fetch tag.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_update_tag(params,cred):
    """
Update information about a WordPress tag based on specified parameters.

:param dict params:
    - tag_id (int): ID of the tag to be updated. (required)
    - name (str): New name for the tag. (optional)
    - description (str): New description for the tag. (optional)
    - slug (str): New slug for the tag. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Information about the updated tag.
:rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'tag_id'in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/tags/{params2['tag_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.put(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to update tag.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_delete_tag(params,cred):
    """
Delete a WordPress tag based on specified parameters.

:param dict params:
    - tag_id (int): ID of the tag to be deleted. (required)
    - force (bool): If set to True, force the deletion of the tag.(optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Success message if the tag is deleted successfully.
:rtype: str
    """

    try:
        creds=json.loads(cred)
        if 'tag_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
                params2 = {'force':True,}
                token=generate_token(creds['username'],creds['applicationPassword'])
                base_url=creds['baseUrl']
                for key, value in params.items():
                    if value:
                        params2[key] = value
                api_url = f"{base_url}/wp-json/wp/v2/tags/{params2['tag_id']}"
                headers = {
                    'Authorization': f'Bearer {token}',
                }
                response = requests.delete(api_url,params=params2, headers=headers)
                if response.status_code in status:
                    return 'Deleted Successfully'
                else:
                    raise Exception(f"Failed to delete tag.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_create_page(params,cred):
    """
Create a new WordPress page based on specified parameters.

:param dict params:
    - title (str): Title of the new page. (required)
    - author (int): ID of the author for the new page.(optional)
    - content (str): Content of the new page.(optional)
    - slug (str): Slug for the new page.(optional)
    - password (str): Password for the new page.(optional)
    - status (str): Status of the new page.(optional)
    - comment_status (str): Comment status of the new page.(optional)
    - ping_status (str): Ping status of the new page.(optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Data representing the newly created page.
:rtype: dict
"""

    try:
        creds=json.loads(cred)
        if 'title' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/pages"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to create page.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_get_page(params,cred):
    """
Retrieve a WordPress page based on specified parameters.

:param dict params:
    - page_id (int): ID of the page to be retrieved. (required)
    - context (str): Optional parameter to specify the context. (optional)
    - password (str): Password for the page retrieval.(optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Data representing the retrieved page.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'page_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:

            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/pages/{params2['page_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception (f"Failed to retrieve the page.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_get_pages(params,cred):
    """
Retrieve WordPress pages based on specified parameters.

:param dict params:
    - context (str): Context for the page retrieval.(optional)
    - search (str): Search term for filtering pages.(optional)
    - author (int): ID of the author for filtering pages.(optional)
    - order (str): Order of the pages.(optional)
    - orderby (str): Field to order pages by.(optional)
    - status (str): Status of the pages to retrieve.(optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Data representing the retrieved pages.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/pages"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to retrieve pages.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_update_page(params,cred):
    """
Update a WordPress page based on specified parameters.

:param dict params:
    - page_id (int): ID of the page to be updated. (required)
    - author (int): ID of the author for the updated page.(optional)
    - title (str): New title for the page.(optional)
    - content (str): New content for the page.(optional)
    - password (str): New password for the page.(optional)
    - status (str): New status for the page.(optional)
    - comment_status (str): New comment status for the page.(optional)
    - ping_status (str): New ping status for the page.(optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Data representing the updated page.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'page_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/pages/{params2['page_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to update the page.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_delete_page(params,cred):
    """
Delete a WordPress page based on specified parameters.

:param dict params:
    - page_id (int): ID of the page to be deleted. (required)
    - force (bool): If set to True, force the deletion of the page.(optional)


:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: Success message if the page is deleted successfully.
:rtype: str
    """

    try:
        creds=json.loads(cred)
        if 'page_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/pages/{params2['page_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return 'Page deleted successfully.'
            else:
                raise Exception(f"Failed to delete the page.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    

def wordpress_create_comment(params,cred):
    """
Create a new comment on a WordPress post based on specified parameters.

:param dict params:
    - post (int): ID of the post for which the comment is created. (required)
    - content (str): Content of the comment. (required)
    - author (int): ID of the comment author. (optional)
    - author_email (str): Email address of the comment author. (optional)
    - author_name (str): Name of the comment author. (optional)
    - status (str): Status of the comment. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: The created comment.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'post' in params and 'content' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/comments"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            response = requests.post(api_url, json=params2, headers=headers)

            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to create comment.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")


def wordpress_get_comments(params,cred):
    """
Retrieve comments from a WordPress site based on specified parameters.

:param dict params:
    - context (str): Context in which the comments are retrieved. (optional)
    - search (str): Search term to filter comments. (optional)
    - order (str): Order of the comments. (optional)
    - orderby (str): Field to order comments by. (optional)
    - post (int): ID of the post for which comments are retrieved. (optional)
    - password (str): Password for password-protected comments. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: The retrieved comments.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/comments"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to retrieve comments.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_get_comment(params,cred):
    """
Retrieve a specific comment from a WordPress site based on the comment ID.

:param dict params:
    - comment_id (int): ID of the comment to be retrieved. (required)
    - context (str): Context in which the comment is retrieved. (optional)
    - password (str): Password for password-protected comment. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: The retrieved comment.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'comment_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/comments/{params2['comment_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to retrieve comment.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_update_comment(params,cred):
    """
Update a specific comment on a WordPress site based on the comment ID.

:param dict params:
    - comment_id (int): ID of the comment to be updated. (required)
    - content (str): New content for the comment. (required)
    - author (int): ID of the comment author. (optional)
    - author_name (str): Name of the comment author. (optional)
    - author_email (str): Email address of the comment author. (optional)
    - status (str): Status of the comment. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: The updated comment.
:rtype: dict
    """

    try:
        creds=json.loads(cred)
        if 'comment_id' in params and 'content' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/comments/{params2['comment_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(api_url, json=params2, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(f"Failed to update the cmnt.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    
def wordpress_delete_comment(params,cred):
    """
Delete a specific comment on a WordPress site based on the comment ID.

:param dict params:
    - comment_id (int): ID of the comment to be deleted. (required)
    - password (str): Password for the comment (if required). (optional)
    - force (bool): If set to True, forces deletion of the comment. (optional)

:param str base_url: Base URL of the WordPress site. (required)
:param str token: Authentication token for accessing the WordPress API. (required)

:return: A message indicating the success of the operation.
:rtype: str
    """

    try:
        creds=json.loads(cred)
        if 'comment_id' in params and 'username' in creds and 'applicationPassword' in creds and 'baseUrl' in creds:
            params2 = {}
            token=generate_token(creds['username'],creds['applicationPassword'])
            base_url=creds['baseUrl']
            for key, value in params.items():
                if value:
                    params2[key] = value
            api_url = f"{base_url}/wp-json/wp/v2/comments/{params2['comment_id']}"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(api_url,params=params2, headers=headers)
            if response.status_code in status:
                return 'Comment deleted successfully.'
            else:
                raise Exception(f"Failed to delete comment.")
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(f"{str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")

    