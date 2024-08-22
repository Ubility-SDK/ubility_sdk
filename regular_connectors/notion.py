import json
import requests
def notion_get_many_users(creds,params):
    """
        Returns a specific number of users
     
    :param str integration_token: (str,required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params: (optional) contains the number of users to be returned
    
      :page_size: (int) The number of items from the full list to include in the response.
    :return: The list of  'page_size' number of users 
    :rtype: dict
    """
    cred=json.loads(creds)
    if 'page_size' in params:
      limit= params['page_size']
      url = f"https://api.notion.com/v1/users?page_size={limit}"
    else:
      url = f"https://api.notion.com/v1/users"
    headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2022-06-28",  
         "Content-Type": "application/json"  
    }
    try:
        response = requests.get(url, headers=headers)  
        if response.status_code==200:
         data = response.json()
         return data["results"]
        else:
           raise Exception(response.json())    
    except Exception as error:
        raise Exception(error)

def notion_get_user(creds,params):
    """
        Returns a user of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :user_id: (str,required) The id of the user to be retrieved
    :return: details about the retrieved user(id,properties,..)
    :rtype: dict  
    """
    try:
     cred=json.loads(creds)
     if 'user_id' in params:
       url = f"https://api.notion.com/v1/users/{params['user_id']}"
       headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2022-06-28",  
         "Content-Type": "application/json"  
       }
       response = requests.get(url, headers=headers)
       if response.status_code==200:
         data = response.json()
         return data
       else:
           raise Exception(response.json())
     else:
          raise Exception("missing user id")
    except Exception as error:
        raise Exception(error)

def notion_get_database(creds,params):
    """
        Returns a database of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :id: (str,required) The id of the database to be retrieved
    :return: details about the retrieved database(id,properties,..)
    :rtype: dict  
    """
    try: 
     cred=json.loads(creds)
     if 'database_id' in params:
       url = f"https://api.notion.com/v1/databases/{params['database_id']}"
       headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2022-06-28",  
         "Content-Type": "application/json"  
       }
       response = requests.get(url, headers=headers)
       if response.status_code==200:
         data = response.json()
         return data
       else:
           raise Exception(response.json())
     else:
          raise Exception("missing database id")
    except Exception as error:
        raise Exception(error)

def notion_get_many_databases(creds,params):
    """
        Returns a specific number of databases
     
    :param str integration_token: (str,required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params: (optional) contains the number of databases to be returned
    
      :page_size: (int) The number of items from the full list to include in the response.
    :return: The list of  'page_size' number of databases 
    :rtype: dict
    """
    cred=json.loads(creds)
    if 'page_size' in params:
      limit= params['page_size']
      url = f"https://api.notion.com/v1/databases?page_size={limit}"
    else:
      url = f"https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2021-05-13",  
         "Content-Type": "application/json"  
    }
    try:
        response = requests.get(url, headers=headers)  
        if response.status_code==200:
         data = response.json()
         return data
        else:
           raise Exception(response.json())    
    except Exception as error:
        raise Exception(error)

def notion_search_database(creds,params):
    """
        Returns a database of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :id: (str,required) The id of the database to be retrieved
    :return: details about the retrieved database(id,properties,..)
    :rtype: dict  
    """
    try:
     cred=json.loads(creds)
     if 'database_id' in params:
       url = f"https://api.notion.com/v1/databases/{params['database_id']}/query"
       headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2022-06-28",  
         "Content-Type": "application/json"  
       }
       response = requests.post(url, headers=headers)
       if response.status_code==200:
         data = response.json()
         return data
       else:
           raise Exception(response.json())
     else:
          raise Exception("missing database id")
    except Exception as error:
        raise Exception(error)
      
def notion_create_page(creds,params): 
    """
        Creates a page with properties passed in the parameters
     
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params: contains specific properties to be added to the user.
    
      :parent: (dict,required) type(value should be page_id),page_id (str) id of the parent page
      :properties: title(arr): contains 'text'(dict),and annotations like (color,code,italic..)
    :return: details about the created page
    :rtype: dict  
    :Examples:
    >>> params = {
        "parent": {
        "type": "page_id",
        "page_id": ""},
      "properties": {
        "title": [ 
            {
                "type": "text",
                "text": {
                    "content": "",
                    "link": "},
                  "annotations":{
                  "bold":True,
                  "italic":True,
                  "strikethrough":True,
                  "underline":True,
                  "code":False,
                  "color":"green"},
               "plain_text":"My New Page",
               "href":"" 
           }, ],},
     }
    """
    try: 
      cred=json.loads(creds)
      if 'parent' in params and 'properties' in params:
        notion_api_url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {cred['accessToken']}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13", 
            }
        response = requests.post(notion_api_url, headers=headers, json=params)
        if response.status_code == 200:
          return response.json()
        else:
          raise Exception(response.json())
      else:
        raise Exception("missing required parameters")
    except Exception as error:
         raise Exception(error)

def notion_get_page(creds,params):
    """
        Returns a page of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :page_id: (str,required) The id of the page to be retrieved
    :return: details about the retrieved page(id,properties,..)
    :rtype: dict  
    """
    try:
     cred=json.loads(creds)
     if 'page_id' in params:
       url = f"https://api.notion.com/v1/pages/{params['page_id']}"
       headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2022-06-28",  
         "Content-Type": "application/json"  
       }
       response = requests.get(url, headers=headers)
       if response.status_code==200:
         data = response.json()
         return data
       else:
           raise Exception(response.json())
     else:
          raise Exception("missing page id")
    except Exception as error:
        raise Exception(error)

def notion_archive_page(creds,params):
 """
        Used to archive a page of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :page_id: (str,required) The id of the page to be retrieved
      :archived: (bool,required) value can be True or False
    :return: details about the archived page(id,properties,..)
    :rtype: dict  
 """
 try:
    cred=json.loads(creds)
    if 'page_id' in params and 'archived' in params:
            notion_api_url = f"https://api.notion.com/v1/pages/{params['page_id']}"
            headers = {
                "Authorization": f"Bearer {cred['accessToken']}",
                "Content-Type": "application/json",
                "Notion-Version": "2021-05-13", 
                }
            to_archive={}
            to_archive['archived']=params['archived']
            response = requests.patch(notion_api_url, headers=headers, json=to_archive)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.json())
    else:
       raise Exception("missing page id")
 except Exception as error:
         raise Exception(error)
       
def notion_get_block(creds,params):
    """
        Returns a block of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :block_id: (str,required) The id of the block to be retrieved
    :return: details about the retrieved block(id,properties,..)
    :rtype: dict  
    """
    try:
     cred=json.loads(creds)
     if 'block_id' in params:        
       url = f"https://api.notion.com/v1/blocks/{params['block_id']}"
       headers = {
        "Authorization": f"Bearer {cred['accessToken']}",
        "Notion-Version": "2022-06-28",  
         "Content-Type": "application/json"  
       }
       response = requests.get(url, headers=headers)
       if response.status_code==200:
         data = response.json()
         return data
       else:
           raise Exception(response.json())
     else:
          raise Exception("missing block id")
    except Exception as error:
        raise Exception(error)
      
def notion_get_many_child_blocks(creds,params):
    """
        Returns children of a block of a specific id.
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :block_id: (str,required) The id of the block whose children are to be retrieved
      :page_size: (str,optional) The number of children to be retrieved
    :return: details about the retrieved block children(id,properties,..)
    :rtype: dict  
    """
    try:
        cred=json.loads(creds)
        if 'block_id' in params:
            if 'page_size' in params:
                 notion_api_url = f"https://api.notion.com/v1/blocks/{params['block_id']}/children?page_size={params['page_size']}"
            else:
                notion_api_url = f"https://api.notion.com/v1/blocks/{params['block_id']}/children"
            headers = {
             "Authorization": f"Bearer {cred['accessToken']}",
             "Notion-Version": "2021-05-13",  
             }
            response = requests.get(notion_api_url, headers=headers)
            if response.status_code == 200:
             return response.json()
            else:
             raise Exception(response.json())
        else:
            raise Exception("missing block Id")
    
    except Exception as error:
        raise Exception(error)

def notion_append_child_blocks(creds,params):
    """
        Creates and appends new children blocks to the parent specified
    
    :param str integration_token: (required) Once the integration is created, you can update its settings as needed under the Capabilities tab and retrieve the integration token under Secrets.
    :param dict params:
    
      :block_id: (str,required) The id of the block whose children are to be retrieved
      :children: (arr,required) Details about children to be added to the parent block (see more in examples)
    :return: details about the created block children(id,properties,..)
    :rtype: dict  
    :Examples:
    >>> params = {
      "block_id":"",
        "children": [{
    "object":"block",
    "type": "file",
    "file":
      {
		"caption": [],
    "type": "external",
    "external": {
 	  	"url": "https://example-files.online-convert.com/document/txt/example.txt"
    }}},
    {
    "object":"block",
    "type": "image",
    "image": {
    "type": "external",
    "external": {
 	  	"url": "https://hips.hearstapps.com/clv.h-cdn.co/assets/17/29/2048x1152/hd-aspect-1500566326-gettyimages-512366437-1.jpg"
     }
    }
    },
      {
      "object":"block",
      "type": "image",
      "image":
          {
        "type": "external",
        "external": {
          "url": "https://hips.hearstapps.com/clv.h-cdn.co/assets/17/29/2048x1152/hd-aspect-1500566326-gettyimages-512366437-1.jpg"
        }
      }
      },
       {
        "object":"block",
        "type": "pdf",
        "pdf": {
        "type": "external",
        "external": {
          "url": "https://website.domain/files/doc.pdf"
        }}
        },], }
    """
    try:
        cred=json.loads(creds)
        if 'block_id' in params and 'children' in params:
            notion_api_url = f"https://api.notion.com/v1/blocks/{params['block_id']}/children"
            headers = {
                "Authorization": f"Bearer {cred['accessToken']}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",  # Specify content type as JSON
            }
            to_append={}
            to_append['children']=params['children']
            response = requests.patch(notion_api_url, headers=headers, json=to_append)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required input")
    except Exception as error:
            raise Exception(error)
