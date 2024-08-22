import json
from pymongo import MongoClient,errors

def connect_to_mongodb(uri, databaseName, collectionName):
    # Connect to the MongoDB server
    client = MongoClient(uri)
    # Select the database
    db = client[databaseName]
    # Select the collection
    collection = db[collectionName]
    return collection

def mongodb_find_documents(cred,params):
    """
    Find documents in a MongoDB collection based on the provided credentials and query parameters.

    :param string cred: A JSON string containing MongoDB credentials, including:

        - :uri: (string,required) - The MongoDB connection string URI.
        - :databaseName: (string,required) - The name of the MongoDB database to connect to.

    :param dict params: A dictionary containing query parameters, including:

        - :collectionName: (string,required) - The name of the collection to query.
        - :limit: (int,optional) - The maximum number of documents to return (default is 100).
        - :query: (dict,optional) - The query filter to match documents (default is an empty dict to match all documents).
        - :sort: (dict,optional) - A dictionary representing the fields to sort by and the sorting order.
        
            The keys are the field names, and the values indicate the sorting order:
                
                - '1': for ascending order (smallest to largest).
                - '1': for descending order (largest to smallest).
                
            If not provided, documents will not be sorted.

    Returns:
        dict: A dictionary containing the found documents with `_id` converted to strings. 

    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            limit = params.get("limit", 100)
            query = params.get("query",{})
            sortData = params.get("sort")
            sort = []
            if sortData:
                for field, direction in sortData.items():
                    sort.append((field, direction))
            collection = connect_to_mongodb(uri, databaseName, collectionName)
            if sort:
                documents = list(collection.find(query).limit(limit).sort(sort))
            else:
                documents = list(collection.find(query).limit(limit))
            # Convert _id from ObjectId to string
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            if documents:
                return {"documents": documents}
            else:
                raise Exception("No document matches the provided query.")
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)

def mongodb_delete_many_document(cred,params):
    """
    Deletes multiple documents from a MongoDB collection based on a specified query.

    :param string cred: A JSON string containing MongoDB credentials, including:

        - :uri: (string,required) - The MongoDB connection string URI.
        - :databaseName: (string,required) - The name of the MongoDB database to connect to.
    :param dict params: A dictionary containing query parameters, including:

        - :collectionName: (string,required) - The name of the collection from which documents will be deleted
        - :query: (dict,optional) -  A dictionary representing the query filter to specify which documents to delete.If no query is provided, all documents in the collection will be deleted.

    Returns:
        dict: A dictionary containing the count of deleted documents with the format:
    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            query = params.get("query", {})
            collection = connect_to_mongodb(uri, databaseName, collectionName)
            result = collection.delete_many(query)
            return {"deletedCount": result.deleted_count}
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)
    
def mongodb_insert_one_document(cred,params):
    """
    Inserts a single document into a MongoDB collection and returns the _id of the inserted document.

    :param dict cred: The credentials dictionary containing MongoDB credentials
    :param dict params: A dictionary containing parameters for the request.

        - :collectionName: (string,required) - The name of the collection.
        - :document: (json,required) - The document to be inserted.
    
    Returns:
        dict: A dictionary containing the _id of the inserted document.
    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params and "document" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            document = params["document"]
            collection = connect_to_mongodb(uri, databaseName, collectionName)
            result = collection.insert_one(document)
            # Get the _id of the inserted document
            inserted_id = str(result.inserted_id)
            return {"inserted_id": inserted_id}
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)
    

def mongodb_insert_many_document(cred,params):
    """
    Inserts multiple documents into a MongoDB collection.

    :param dict cred: The credentials dictionary containing MongoDB credentials
    :param dict params: A dictionary containing parameters for the request.

        - :collectionName: (string,required) - The name of the collection.
        - :documents: (list of dicts, required): A list of dictionaries representing the documents to be inserted.
    
    Returns:
        dict: A dictionary with a success message indicating the number of inserted documents.
    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params and "documents" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            if isinstance(params["documents"], list):
                documents = params["documents"]
                collection = connect_to_mongodb(uri, databaseName, collectionName)
                result = collection.insert_many(documents)
                return {"message": f"Successfully inserted {len(result.inserted_ids)} items!"}
            raise Exception("Input data must be a list of dictionaries.")
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)

    
def mongodb_update_documents(cred,params):
    """
    Updates multiple documents in a MongoDB collection based on the specified query and update criteria.

    :param string cred: A JSON string containing MongoDB credentials, including:

        - :uri: (string,required) - The MongoDB connection string URI.
        - :databaseName: (string,required) - The name of the MongoDB database to connect to.
    :param dict params: A dictionary containing query parameters, including:

        - :collectionName: (string,required) - The name of the collection to update.
        - :query: (dict,required) - A dictionary representing the query filter to find the document to update.
        - :update: (dict,required) - A dictionary representing the update document specifying the modifications.
        - :upsert: (bool,optional) - If `True`, inserts a new document if no documents match the query criteria; if `False`, only updates existing documents.

    Returns:
        dict: A dictionary containing metadata about the update operation:

            :matched_count: The number of documents that matched the query.
            :modified_count: The number of documents that were modified.

    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params and "query" in params and "update" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            query = params.get("query", {})
            update = params.get("update", {})
            upsert = params.get("upsert", False)
            if update :
                collection = connect_to_mongodb(uri, databaseName, collectionName)
                result = collection.update_many(query, update, upsert)
                return {
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count
                }
            else:
                 raise Exception("The update document cannot be empty.")
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)

def mongodb_find_one_and_update_document(cred,params):
    """
    Finds a single document that matches the query, updates it, and returns the updated document.

    :param string cred: A JSON string containing MongoDB credentials, including:

        - :uri: (string,required) - The MongoDB connection string URI.
        - :databaseName: (string,required) - The name of the MongoDB database to connect to.
    :param dict params: A dictionary containing query parameters, including:

        - :collectionName: (string,required) - The name of the collection to update.
        - :query: (dict,required) - A dictionary representing the query filter to find the document to update.
        - :update: (dict,required) - A dictionary representing the update document specifying the modifications.
        - :upsert: (bool,optional) - If `True`, inserts a new document if no documents match the query criteria; if `False`, only updates existing documents.

    Returns:
        dict: A dictionary containing a message indicating the success of the update operation.

    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params and "query" in params and "update" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            query = params.get("query", {})
            updateData = params.get("update", {})
            update = {"$set": updateData}
            collection = connect_to_mongodb(uri, databaseName, collectionName)
            updated_document = collection.find_one_and_update(query,update)
            if updated_document:
                return {"message": "Successfully updated document"}
            else:
                raise Exception("No document matches the provided query.")
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)  

def mongodb_find_one_and_replace_document(cred,params):
    """
    Finds a single document in the specified collection, replaces it with a new document

    :param string cred: A JSON string containing MongoDB credentials, including:

        - :uri: (string,required) - The MongoDB connection string URI.
        - :databaseName: (string,required) - The name of the MongoDB database to connect to.
    :param dict params: A dictionary containing query parameters, including:

        - :collectionName: (string,required) - Name of the collection in which to perform the replacement.
        - :query: (dict,required) - A filter document used to find the document to replace. An empty query ({}) matches all documents.
        - :replacement: (dict,required) - The document that will replace the matched document. 

    Returns:
        dict: A dictionary containing a message indicating the success of the replacement operation.

    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params and "query" in params and "replacement" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            filter  = params.get("query", {})
            replacement = params.get("replacement", {})
            collection = connect_to_mongodb(uri, databaseName, collectionName)
            updated_document = collection.find_one_and_replace(filter,replacement)
            if updated_document:
                return {"message": "Successfully replaced document"}
            else:
                raise Exception("No document matches the provided query.")
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)
    
def mongodb_aggregate_documents(cred,params):
    """
    Aggregation operation based on provided criteria.

    :param string cred: A JSON string containing MongoDB credentials, including:

        - :uri: (string,required) - The MongoDB connection string URI.
        - :databaseName: (string,required) - The name of the MongoDB database to connect to.
    :param dict params: A dictionary containing query parameters, including:

        - :collectionName: (string,required) - The name of the collection.
        - :matchData: (dict,required) - The match criteria for the aggregation `$match` stage.
        - :groupData: (dict,required) - The grouping criteria for the aggregation `$group` stage.

    Returns:
        list: A list of documents resulting from the aggregation pipeline.

    """
    try:
        creds = json.loads(cred)
        if "uri" in creds and "databaseName" in creds and "collectionName" in params and "matchData" in params and "groupData" in params:
            uri = creds["uri"]
            databaseName = creds["databaseName"]
            collectionName = params["collectionName"]
            matchData = params["matchData"]
            groupData = params["groupData"]
            # Define the aggregation pipeline
            pipeline = [
                # Stage 1: Filter documents by matchData
                {
                    "$match": matchData
                },
                # Stage 2: Group remaining documents by groupData
                {
                    "$group": groupData
                }
            ]
            collection = connect_to_mongodb(uri, databaseName, collectionName)
            cursor = collection.aggregate(pipeline)
            results = list(cursor)
            return results
        else:
            raise Exception("missing input data")
    except errors.ConnectionFailure as conn_err:
        raise Exception(f"Failed to connect to MongoDB: {conn_err}")
    except Exception as error:
        raise Exception(error)