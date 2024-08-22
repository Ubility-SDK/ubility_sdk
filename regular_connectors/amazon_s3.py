import boto3
import boto3.session
import json,datetime,base64
from botocore.exceptions import ClientError

def autheticate_to_amazon_s_three(cred):
    try:
        conn = boto3.session.Session()
        s3 = conn.client(
            service_name="s3",
            region_name = cred['region'],
            aws_access_key_id= cred['awsAccessKeyId'],
            aws_secret_access_key =cred['secretAccessKey']
        )
        return s3    
    except ClientError as error:
        raise Exception(f"Failed to authenticate. {error}")



def amazon_s_three_get_object_metadata(cred,params):
    try:
        if "bucketName" in params and "objectID" in params:
            credential = json.loads(cred)
            s3 = autheticate_to_amazon_s_three(credential)
            object_response = s3.head_object(Bucket = params['bucketName'], Key = params['objectID'])
            if object_response:
                for key, value in object_response.items():
                    if isinstance(value, datetime.datetime):
                        object_response[key]=  value.strftime("%Y-%m-%d %H:%M:%S %z")
                    else:
                        continue
            else:
                raise Exception(f"Object with the object id {params['objectID']} was not found")
            return object_response
        else:
            raise Exception("Missing required parameter(s)")
    except ClientError as error:
        raise Exception(f"An error occured: {error}")
    
    
def amazon_s_three_create_bucket(cred,params):
    try:
        if "bucketName" in params:
            credential = json.loads(cred)
            s3_client = autheticate_to_amazon_s_three(credential)
            bucket = s3_client.create_bucket(Bucket=params['bucketName'],CreateBucketConfiguration={'LocationConstraint':credential['region']})
            return bucket
        else:
            raise Exception("Missing Required Parameter(s)")
    except ClientError as error:
        raise Exception(f"An error occured: {error}")
    
def amazon_s_three_delete_bucket(cred,params):
    try:
        if "bucketName" in params:
            credential = json.loads(cred)
            s3_client = autheticate_to_amazon_s_three(credential)
            bucket = s3_client.delete_bucket(Bucket = params['bucketName'])
            return bucket
        else:
            raise Exception("Missing Required Parameter(s)")
    except ClientError as error:
        raise Exception(f"An error occured: {error}")
    
    
def amazon_s_three_create_text_object(cred,params):
    try:
        if "bucketName" in params and "key" in params and "fileContent" in params:
            credential = json.loads(cred)
            s3_client = autheticate_to_amazon_s_three(credential)
            file = s3_client.put_object(Body=params['fileContent'], Bucket=params['bucketName'], Key=params['key'])
            return file
        else:
            raise Exception("Missing required Parameter(s)")
    except ClientError as error:
        raise Exception(f"An error occured: {error}")


def amazon_s_three_upload_file(cred,params):
    try:
        if "bucketName" in params and "fileContent" in params and "key" in params:
            credential = json.loads(cred)
            s3_client = autheticate_to_amazon_s_three(credential)
            file_content = params['fileContent']
            encoded_file_content = base64.b64decode(file_content)
            file = s3_client.put_object(Body=encoded_file_content,Bucket=params['bucketName'],Key=params['key'])
            return file
        else:
            raise Exception("Missing Required Parameter(s)")
    except ClientError as error:
        raise Exception(f"An error occured: {error}")

