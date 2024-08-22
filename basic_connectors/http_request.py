import requests
import logging
import base64
import json



def http_request(method,url,authorization_params,query_params,headers_params,body_params,optional):
    try:
        headers={}
        query={}
        params={}
        body={}

        # Auth type 
        if 'type' in  authorization_params:
            if authorization_params['type'] == 'API Key':           #if API Key
                key = authorization_params['key']
                value = authorization_params['value']
                addTo = authorization_params['addTo']
                if addTo == 'Header':     #Add to header
                    headers[key] = value
                elif addTo == 'Query Params':   #Add to Query
                    params[key] = value
            elif authorization_params['type'] == 'Bearer Token':     #if Bearer Token 
                token = authorization_params['token']
                headers['Authorization']= f'Bearer {token}'
            elif authorization_params['type'] == 'Basic Auth':      #if BAsic Auth
                username = authorization_params['username']
                password = authorization_params['password']
                credentials = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
                headers['Authorization'] = f'Basic {credentials}'

        # Header Params 
        for item in headers_params:
                headers[item['name']] = item['value']

        # Query Params
        for item in query_params:
            query[item['key']] = item['value']



        # Body
        if 'type' in body_params:
            if body_params['type'] == 'JSON':       #Body type json
                headers['Content-Type'] = 'application/json'
                body = body_params['json']
            elif body_params['type'] == 'Form Data':   #Body type Form Data
                body={}
                for item in body_params['formData']: 
                        if item['type'] == 'binary':
                            body[item['key']] = item['value'].encode('utf-8')
                        elif  item['type'] == 'text':
                            body[item['key']] = item['value']
                        elif item['type'] == 'url':
                            file = requests.get(item['value'])
                            body[item['key']] = file.content
            elif body_params['type'] == 'Binary':   #Body type Binary
                headers['Content-Type'] = 'application/octet-stream'
                body = body_params['binary-data'].encode('utf-8')
        # elif body_params['type'] == 'XML':


        #Enable SSL certificate verification
        SSL = optional['ssl']   #Default True
        timeout = optional['timeout']  #Default 30
        


        if method == 'POST':
            response = requests.post(url, params=query, headers=headers, json=body, verify=SSL, timeout=timeout)
        elif method == 'GET':
            response = requests.get(url, params=query, headers=headers, verify=SSL, timeout=timeout)
        elif method == 'PUT':
            response = requests.put(url, params=query, headers=headers, json=body, verify=SSL, timeout=timeout)
        elif method == 'DELETE':
            response = requests.delete(url, params=query, headers=headers, json=body, verify=SSL, timeout=timeout)
        elif method == 'PATCH':
            response = requests.patch(url, params=query, headers=headers, json=body, verify=SSL, timeout=timeout)
        response.raise_for_status()  # Raises an exception for HTTP errors
        try:
            json_data = json.loads(response.text)
            return json_data  # If it's valid JSON, return the parsed JSON data.
        except json.JSONDecodeError:
            return response.text 
    

    except requests.exceptions.HTTPError as e:
        error_response = e.response.text
        raise requests.exceptions.HTTPError(f"HTTP error: {str(e)}\nResponse content: {error_response}")
    except requests.exceptions.Timeout:
        raise Exception("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed with an error: {str(e)}")
    except Exception as error:
        raise Exception(error)