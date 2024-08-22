import requests,json




#############################################################
# Records Operations

def quickbase_delete_record(cred,params):
    
    '''
    Deletes record(s) in a table based on a query. Alternatively, all records in the table can be deleted.
    
    :param str token: QuickBase user token for authentication.
    :param str realm_hostname: The realm hostname for the QuickBase application.
    :param dict params: A dictionary containig parameters for the delete operation.
    
     - :from: (str,required) The ID of the table from which records should be deleted.
     - :where: (str,required) The filter to delete records. To delete all records specify a filter that will include all records, for example {3.GT.0} where 3 is the ID of the Record ID field, GT is the operator and 0 is the value to compare on.
                                For more information visit "QuickBase query language".
    
    Returns:
        dict: A dictionary containing the result of the delete operation.The result includes information about the number of records deleted. 
    
    
    '''
    
    try:
        if "from" in params and "value" in params and "operator" in params and "field_id" in params:
            credentials = json.loads(cred)
            url = "https://api.quickbase.com/v1/records"
            realm_hostname = credentials['realmHostname']
            token = credentials['accessToken']
            headers ={
                "Authorization": f"QB-USER-TOKEN {token}",
                "QB-Realm-Hostname":realm_hostname,
                "Content-Type":"application/json; charset=utf-8",
            }
            body_data = {}
            fieldId = params['field_id'] #ID of the field to apply the filter
            operator = params['operator'] #Operator for comparison 
            values=  params["value"] #Value to compare against
            where = f"{{{fieldId}.{operator}.'{values}'}}" #Format as per API requirements ex:{6.EX.'hello'}
            body_data['where'] = where #assign the value to the where key as quickbase API expects
            keys_to_skip =['field_id','operator','value']
            for key,value in params.items():
                if key not in keys_to_skip:
                    body_data[key] = value
            response = requests.delete(url=url,headers=headers,json=body_data)
            result= response.json()
            if result['numberDeleted'] == 0: #no records match the query provided
                raise Exception("No records deleted. Please check your inputs")
            elif 'message' in result and result['message'] == 'Access denied': #invalid appId
                raise Exception("Error! User token or application id is invalid")
            else:
                return result
        else :
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)



def quickbase_create_record(cred,params):
    
    '''
    Creates a record in a table with the specified properties passed in params.
    
    :param str token: QuickBase user token for authentication.
    :param str realm_hostname: The realm hostname for the QuickBase application.
    :param dict params: A dictionary containig the record properties (e.g fields,values...).
    
     - :to: (str,required) The table identifier (where the record will be created).
     - :data: (list of dict,required) A list where each item represents a single record to be added. 
                                      Each record should contains at least one field with its corresponding value to be successfully inserted.
                                      Each dictionary within the record corresponds to a field/value pair, with the structure as follows:

      - :field_id: (dict, required) Each key represents the unique identifier (ID) of a field within the Quick Base table.
       - :value: (varied types,required) The value of the field of the record to be inserted. (The value's type depends on the field's type within quickbase).
       
     - :fieldsoReturn: (array of integer, optional) This parameter allows users to specify which fields should be included in the response after a record is created.
                                                    Only the fields specified in this list will be included in the response.
      - :field_id: (int,optional) The id of the field to return.
      
    Example:
    data = [
        {
            "field_id_1": {"value": "value for field_id_1"},
            "field_id_2": {"value": "value for field_id_2"},
            ....
        }
    ],
    "fieldsToReturn": [
    field_id_1,
    field_id_2,
    field_id_3,
    ....
    ]
    
    
    Returns:
        dict: A dictionary containing the response data from Quick Base after the record creation operation.
    '''
    
    try:
        if "to" in params and "data" in params:
            credentials = json.loads(cred)
            realm_hostname = credentials['realmHostname']
            token = credentials['accessToken']
            url = "https://api.quickbase.com/v1/records"
            headers= {
                "Authorization":f"QB-USER-TOKEN {token}",
                "Content-Type":"application/json; charset=utf-8",
                "QB-Realm-Hostname":realm_hostname,
            }
            body_data = {}
            for key,value in params.items():
                body_data[key]=  value
            Restructured={}    
            for field in body_data['data']:
                for key ,value in field.items():
                   Restructured[key] = value
            body_data['data'] = [Restructured] #restructure the data from UI as quickbase API expects
            response = requests.post(url=url,headers=headers,json=body_data)
            result= response.json()
            if 'message' in result and result['message'] == 'Access denied': #invalid tableId or appId
                raise Exception("Error! User token or application id is invalid")
            elif 'metadata' in result and 'lineErrors' in result['metadata']: #an error in the parameters
                err_msg = result['metadata']['lineErrors']['1']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")       
    except Exception as e:
        raise Exception(e)


def quickbase_update_record(cred,params):
    
    '''
    Updates a record in a table with the specified properties passed in params.
    
    :param str token: QuickBase user token for authentication.
    :param str realm_hostname: The realm hostname for the QuickBase application.
    :param dict params: A dictionary containig the record properties (e.g fields,values...).
    
     - :to: (str,required) The table identifier (where the record will be updated).
     - :data: (list of dict,required) A list where each item represents a single record to be updated. 
                                      Each record should contains at least one field with its corresponding value to be successfully updated.
                                      For updating an existing record, add a mapping of the table key field ID (defaults to '3') to the record ID, in the data array.
                                      Each dictionary within the record corresponds to a field/value pair, with the structure as follows:
      - :field_id: (dict, required) Each key represents the unique identifier (ID) of a field within the Quick Base table.
       - :value: (varied types,required) The value of the field of the record to be inserted. (The value's type depends on the field's type within quickbase).
       
     - :fieldsoReturn: (array of integer, optional) This parameter allows users to specify which fields should be included in the response after a record is created.
                                                    Only the fields specified in this list will be included in the response.
      - :field_id: (int,optional) The id of the field to return.
    
    Example:
    data = [
        {
            "table_key_filed_id": {"value": "Id of the record to update"},
            "field_id_1": {"value": "value for field_id_1"},
            "field_id_2": {"value": "value for field_id_2"},
            ....
        }
    ],
    "fieldsToReturn": [
    field_id_1,
    field_id_2,
    field_id_3,
    ....
    ]
    
    
    Returns:
        dict: A dictionary containing the response data from Quick Base after the record update operation.
    '''
    
    try:
        if "to" in params and "data" in params:
            credentials = json.loads(cred)
            token = credentials['accessToken']
            realm_hostname = credentials['realmHostname']
            url = "https://api.quickbase.com/v1/records"
            headers = {
                "Authorization":f"QB-USER-TOKEN {token}",
                "Content-Type":"application/json; charset=utf-8",
                "QB-Realm-Hostname":realm_hostname
            }
            body_data ={}
            for key,value in params.items():
                body_data[key] = value
            Restructured={}    
            for field in body_data['data']:
                for key ,value in field.items():
                   Restructured[key] = value
            body_data['data'] = [Restructured] #restructure the data from UI as quickbase API expects
            response = requests.post(url=url,headers=headers,json=body_data)
            result = response.json()
            if 'message' in result and result['message'] == 'Access denied': #invalid appId
                raise Exception("Error! User token or application id is invalid")
            elif 'metadata' in result and 'lineErrors' in result['metadata']: #an error in the parameters
                err_msg = result['metadata']['lineErrors']['1']
                raise Exception(err_msg)
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    
    
    
def quickbase_get_many_records(cred,params):
    
    '''
    Retrieves a list of records from a given table based on specified criteria passed in params.
    
    :param str token: QuickBase user token for authentication.
    :param str realm_hostname: The realm hostname for the QuickBase application.
    :param dict params: A dictionary containig the criteria .
    
     - :from: (str.required) The table identifier from which records will be queried.
     - :select: (list of int, optional) An array of field ids for the fields that should be returned in the response. If empty, the default columns on the table will be returned.
      - :field_id: (int,optional) The fields id that should be returned in the response.
     - :sortBy: (list of dict,optional) An array of field IDs and sort directions. If this attribute is not set or set to false, queries will be unsorted to improve performance.
      - :field_id: (int,optional) The unique identifier of a field in a table.
      - :order: (str,optional) Sort based on ascending order (ASC), descending order (DESC) or equal values (equal-values).
     - :where: (str,optional) The filter, using the Quickbase query language, which determines the records to return. If this parameter is omitted, the query will return all records.
                                For more information visit "QuickBase query language". 
                                
    Returns:
        dict: A dictionary containing a list of retrieved records from the table passed in params.
    '''
    
    try:
        if "from" in params:
            credentials = json.loads(cred)
            token = credentials['accessToken']
            realm_hostname = credentials['realmHostname']
            url = "https://api.quickbase.com/v1/records/query"
            headers ={
                "Authorization":f"QB-USER-TOKEN {token}",
                "Content-Type":"application/json; charset=utf-8",
                "QB-Realm-Hostname": realm_hostname
            }
            body_data ={}
            if "field_id" in params and "operator" in params and "value" in params:
                fieldId = params['field_id'] #ID of the field to apply the filter
                operator = params['operator'] #Operator for comparison 
                values=  params["value"] #Value to compare against
                where = f"{{{fieldId}.{operator}.'{values}'}}" #Format as per API requirements ex:{6.EX.'hello'}
                body_data['where'] = where #assign the value to the where key as quickbase API expects
            keys_to_skip = ['field_id','operator','value']
            for key,value in params.items():
                if key not in keys_to_skip:
                    body_data[key]= value
            response = requests.post(url=url,headers=headers,json=body_data)
            result = response.json()
            if 'message' in result and result['message'] == 'Access denied': #invalid appId
                raise Exception("Error! User token or application id is invalid")
            else:
                return result
        else:
            raise Exception("Missing Input Data")
    except Exception as e:
        raise Exception(e)
    
    
    
def quickbase_upsert_record(cred,params):
    
    
    '''
    Performs an upsert operation on a QuickBase table. This operation will update records if they exist
    or insert them as new records based on the uniqueness of a specified merge field.
    
    :param str token: QuickBase user token for authentication.
    :param str realm_hostname: The realm hostname for the QuickBase application.
    :param dict params: A dictionary containing the parameters for the upsert operation.
    
     - :to: (str,required) The table identifier (where the record will be updated/inserted).
     - :data: (list of dict,required) A list where each item represents a single record's data for upsertion.
                                      Each record is a dictionary of field/value pairs.
                                      
      - :field_id: (dict, required) Each key represents the unique identifier (ID) of a field within the Quick Base table.
       - :value: (varied types,required) The value of the field of the record to be inserted. (The value's type depends on the field's type within quickbase).
       
     - :fieldsoReturn: (array of integer, optional) This parameter allows users to specify which fields should be included in the response after a record is created.
                                                    Only the fields specified in this list will be included in the response.
      - :field_id: (int,optional) The id of the field to return.
     
     - :mergeFieldId: (str,required)  The field ID used to determine uniqueness for the upsert operation.
                                      Records with matching values in this field will be updated; others will be inserted.
                                      It should be unique in the table.
                                      
                                      
    Returns: 
        dict: A dictionary containing the response data from QuickBase after the upsert operation.
           
    '''
    
    try:
        if "to" in params and "data" in params and "mergeFieldId" in params:
            credentials = json.loads(cred)
            token = credentials['accessToken']
            realm_hostname = credentials['realmHostname']
            url = "https://api.quickbase.com/v1/records"
            headers ={
                "Authorization":f"QB-USER-TOKEN {token}",
                "Content-Type":"application/json; charset=utf-8",
                "QB-Realm-Hostname": realm_hostname
            }
            body_data ={}
            for key,value in params.items():
                body_data[key] = value
            Restructured={}    
            for field in body_data['data']:
                for key ,value in field.items():
                   Restructured[key] = value
            body_data['data'] = [Restructured] #restructure the data from UI as quickbase API expects
            response = requests.post(url=url,headers=headers,json=body_data)
            result = response.json()
            if 'message' in result and result['message'] == 'Access denied': #invalid appId
                raise Exception("Error! User token or application id is invalid")
            elif 'metadata' in result and 'lineErrors' in result['metadata']: #an error in the parameters
                err_msg = result['metadata']['lineErrors']['1']
                raise Exception(err_msg)
            elif 'message' in result and result['message'] == 'Invalid input':
                err_message = "Invalid Input! "+result['description']
                raise Exception(err_message)
            else:
                return result                     
        else:
            raise Exception("Missing Input Data")      
        
    except Exception as e:
        raise Exception(e)



