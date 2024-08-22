import requests
import json


def discord_get_channel(creds,params):
    """
        Returns a discord channel with its properties
    :param str bot_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the channel to be returned
    
       - :channel_id: (str, Required) The Id of the channel to be retrieved
    
    :return: Details about the retrieved channel(name,type,..).
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        if 'channel_id' in params:
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
            }
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}"
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                channel_info = response.json()
                return channel_info
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing channel id")
    except Exception as e:
        raise Exception(e)  

def discord_create_channel(creds,params):
    """
     Creates a discord channel with custom properties if added.

    :param str bot_token: Used for authentication purposes. 
    :param dict params: contains properties to be added to the created channel
    
        - :name: (str, Required) the name of the channel.
        - :guild_id: (str,Required) the id of the guild (may be missing for some channel objects received over gateway guild dispatches)
        - :type: (int) Possible values are 0, 2, 4, GUILD_TEXT , GUILD_VOICE , GUILD_CATEGORY
        - :topic: (str) the channel topic.
        - :position: (int) sorting position of the channel.
        - :parent_id: (str) id of the parent category for a channel.
        - :rate_limit_per_user: (int) amount of seconds a user has to wait before sending another message (0-21600)
        
    :return: Details about the created channel
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        required_params=['name','guild_id']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            channel = {}
            key_to_skip=['guild_id']
            for key, value in params.items():
                if key in key_to_skip:
                    continue
                channel[key] = value
            api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/channels"
            response = requests.post(api_url, headers=headers, json=channel)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e)  

def discord_update_channel(creds,params):
    """
     Updates a discord channel with custom properties if added.

    :param str bot_token: Used for authentication purposes. 
    :param dict params: contains properties to be added(or modified) to the channel
    
        - :channel_id: (str, Required) The Id of the channel to be modified.
        - :guild_id: (str,Required) the id of the guild (may be missing for some channel objects received over gateway guild dispatches)
        - :type: (int) Possible values are 0, 2, 4, GUILD_TEXT , GUILD_VOICE , GUILD_CATEGORY
        - :topic: (str) the channel topic.
        - :position: (int) sorting position of the channel.
        - :parent_id: (str) id of the parent category for a channel.
        - :rate_limit_per_user: (int) amount of seconds a user has to wait before sending another message (0-21600)
        - :name: (str) the new name for the channel.

    :return: Details about the updated channel
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        if 'channel_id' in params:
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            channel = {}
            key_to_skip=['channel_id']
            for key, value in params.items():
                if key in key_to_skip:
                    continue
                channel[key] = value
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}"
            response = requests.patch(api_url, headers=headers, json=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing channel id")
    except Exception as e:
         raise Exception(e)  

def discord_delete_channel(creds,params):
    """
        Deletes a discord channel
    :param str bot_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the channel to be deleted
    
       - :channel_id: (str, Required) The Id of the channel to be deleted.
    
    :return: Details about the deleted channel(name,type,id,..).
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        if 'channel_id' in params:
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
            }
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}"
            response = requests.delete(api_url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing channel Id")
    except Exception as e:
        raise Exception(e)  

def discord_get_many_channels(creds,params):
    """
       Returns a list of guild channel objects. 
    :param str bot_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the guild of the channels
    
       - :guild_id: (str, Required) The Id of the guild to which the channels belong.
    
    :return: Returns a list of channels,each with its properties.
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        if 'guild_id' in params:
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            api_url = f"https://discord.com/api/v7/guilds/{params['guild_id']}/channels"
            response = requests.get(api_url, headers=headers)
            if response.status_code==200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing guild Id")
    except Exception as e:
        raise Exception(e)  

def discord_get_many_members(creds,params):
    """
       Returns a list of guild member objects with properties. 
    :param str bot_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the guild of the channels
    
       - :guild_id: (str, Required) The Id of the guild to which the members belong.
       - :limit: (str) max number of members to return (1-1000).
       - :after: (str) the highest user id in the previous page.
    
    :return: Returns a list of members,each with its properties.
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        if 'guild_id' in params:
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/members"
            if 'limit' in params and 'after' in params:
                api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/members?limit={params['limit']}&after={params['after']}"
            elif 'limit' in params:
                api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/members?limit={params['limit']}"
            elif 'after' in params:
                api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/members?after={params['after']}"
            response = requests.get(api_url, headers=headers)
            if response.status_code==200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing guild Id")
    except Exception as e:
        raise Exception(e)  

def discord_add_member_role(creds,params):  
    """
     Adds a role to a guild member. Requires the MANAGE_ROLES permission.

    :param str bot_token: Used for authentication purposes. 
    :param dict params: contains parameters needed for the addition  of the role
    
        - :name: (str, Required) the name of the channel.
        - :guild_id: (str,Required) the id of the guild (may be missing for some channel objects received over gateway guild dispatches)
        - :role_id: (int) The Id of the role to be added
        - :user_id: (str) The Id of the member.
    :return: A statement declaring success/failure of the function
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        required_params=['guild_id','role_id','user_id']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/members/{params['user_id']}/roles/{params['role_id']}"
            response = requests.put(api_url, headers=headers)
            if response.status_code == 204:
                return f'Role added successfully'
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required parameters")
    except Exception as e:
        raise Exception(e)  
    
def discord_remove_member_role(creds,params):
    """
     Removes a role from a guild member. Requires the MANAGE_ROLES permission.

    :param str bot_token: Used for authentication purposes. 
    :param dict params: contains parameters needed for the removal of the role
    
        - :name: (str, Required) the name of the channel.
        - :guild_id: (str,Required) the id of the guild (may be missing for some channel objects received over gateway guild dispatches)
        - :role_id: (int) The Id of the role to be removed
        - :user_id: (str) The Id of the member.
    :return: A statement declaring success/failure of the function
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        required_params=['guild_id','role_id','user_id']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            api_url = api_url = f"https://discord.com/api/v10/guilds/{params['guild_id']}/members/{params['user_id']}/roles/{params['role_id']}"
            response = requests.delete(api_url, headers=headers)
            if response.status_code == 204:
                return f' Role removed successfully'
            else:
               raise Exception(response.json())
        else:
            raise Exception("missing required data")
    except Exception as e:
        raise Exception(e)  
    
def discord_create_message(creds,params):
    """
     Creates a discord message with custom properties if added.

    :param str bot_token: Used for authentication purposes. 
    :param dict params: contains properties to be added to the created message
    
        - :content: (str, Required) the content of the message.
        - :channel_id: (str,Required) the id of the channel (may be missing for some message objects received over gateway guild dispatches)
        - :tts: (bool) Text To Speech
        - :flags: (int) message flags combined as a bitfield
        - :embeds: (arr) array of embed objects :Up to 10 rich embeds.
        
        
    :return: Details about the created message
    :rtype: dict
    :Examples:
    >>> params = {
    "channel_id":"",
    "content":"",
    "tts":True,  
    "flags":"",
    "embeds":[ "title":"",
                "color":"",
                    "author": 
                    {
                    "name": 
                    "Lil Sm"
                    },
                    "image": 
                    {
                    "url": 
                    "",  
                    },
                "url":"",
                "description":""
              ],
     }
    """
    try:
        credentials=json.loads(creds)
        required_params=['channel_id','content']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            message = {}
            key_to_skip=['channel_id']
            for key, value in params.items():
                if key in key_to_skip:
                    continue
                message[key] = value
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}/messages"
            response = requests.post(api_url, headers=headers, json=message)
            if response.status_code==200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required parameters")
    except Exception as e:
        raise Exception(e)  
        
def discord_delete_message(creds,params):
    """
        Deletes a discord message
    :param str bot_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the message to be deleted
    
       - :message_id: (str, Required) The Id of the message to be deleted.
       - :channel_id: (str, Required) The channel where the message is
    :return: Details about the deleted message(name,type,id,..).
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        required_params=['channel_id','message_id']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}/messages/{params['message_id']}"
            response = requests.delete(api_url, headers=headers)
            if response.status_code==204:
                return f"message of id : {params['message_id']} deleted successfully"
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required parameters")
    except Exception as e:
        raise Exception(e)  
        
def discord_edit_message(creds,params):
    """
     Edits a discord message with custom properties if added.

    :param str bot_token: Used for authentication purposes. 
    :param dict params: contains properties to be added to the created message
    
        - :content: (str, Required) the content of the message.
        - :channel_id: (str,Required) the id of the channel (may be missing for some message objects received over gateway guild dispatches)
        - :message_id: (str,Required) the id of the message to be edited
        
        
    :return: Details about the edited message
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        required_params=['channel_id','message_id']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            message={}
            keys_to_skip=['channel_id','message_id']
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                message[key] = value
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}/messages/{params['message_id']}"
            response = requests.patch(api_url, headers=headers,json=message)
            if response.status_code==200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required parameters") 
    except Exception as e:
        raise Exception(e)  

def discord_get_many_messages(creds,params):
    """
       Returns a list of guild message objects with properties. 
    :param str bot_token: Used for authentication purposes. 
    :param dict params: Contains the Id of the guild of the messages

       - :channel_id: (str, Required) The Id of the channel to which the messages belong.
       - :limit: (str) max number of messages to return (1-1000).

    :return: Returns a list of messages,each with its properties.
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        if 'channel_id' in params:
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            if 'limit' in params:
                api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}/messages?limit={params['limit']}"
            else:
                api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}/messages"
            response = requests.get(api_url, headers=headers)
            if response.status_code==200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing channel Id")
    except Exception as e:
        raise Exception(e)  
        
def discord_get_message(creds,params):
    """
        Returns a discord message with its properties
    :param str bot_token:
        Used for authentication purposes. 
    :param dict params: Contains the Id of the message to be returned
    
       - :channel_id: (str, Required) The Id of the channel where the message was sent
       - :message_id: (str, Required) The Id of the message to be retrieved
    
    :return: Details about the retrieved message(content,type,..).
    :rtype: dict
    """
    try:
        credentials=json.loads(creds)
        required_params=['channel_id','message_id']
        if all(param in params for param in required_params):
            headers = {
                'Authorization': f'Bot {credentials["botToken"]}',
                'Content-Type': 'application/json',
            }
            api_url = f"https://discord.com/api/v10/channels/{params['channel_id']}/messages/{params['message_id']}"
            response = requests.get(api_url, headers=headers)
            if response.status_code==200:
                return response.json()
            else:
                raise Exception(response.json())
        else:
            raise Exception("missing required Data")
    except Exception as e:
        raise Exception(e)  
        