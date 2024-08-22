##################################################################
# Use document loaders to load data from a source as Document's. #
##################################################################
import logging
from typing import (Any,Callable,Dict,Generator,Iterable,List,Optional,Tuple,Type)
import os
import types
import base64
import random
import string
import json


from langchain_community.document_loaders import TextLoader,PyPDFLoader,CSVLoader,JSONLoader,WebBaseLoader,WikipediaLoader,UnstructuredExcelLoader,UnstructuredPowerPointLoader,UnstructuredWordDocumentLoader




file_name=''


class DocumentLoader:
    
    _VALID_LOADERS=["basicDataLoader","webPageLoader","wikipediaLoader","MicrosoftLoader"]
    
    def __init__(
        self,
        type: str
        ):
        """
            Create object for your Document Loader
            
            Example:
                .. code-block:: python

                    from uintegrate_langchain.document_loader import DocumentLoader

                    my_dl_object = DocumentLoader(
                        type = "basicDataLoader"
                    )
        """
        logging.info("Setting up document loader object")
        
        if type in self._VALID_LOADERS:
            self.type = type
        else:
            raise ValueError(f"Invalid provider '{type}'. Valid providers are: {', '.join(self._VALID_LOADERS)}")
        

    def load(self,loader_data: dict):
        global file_name
        """
            Load data method
            
            Example:
                .. code-block:: python

                    from uintegrate_langchain.document_loader import DocumentLoader
                    
                    urls_list=["https://uintegrate.io"]
                    data={"urls":urls_list}
                    my_dl_object = DocumentLoader(type = "webPageLoader").load(data)
        """
        try:
            logging.info("Load data method")

            if self.type == "basicDataLoader":
                response = basicDataLoader(loader_data)
            elif self.type == "webPageLoader":
                response = webPageLoader(loader_data)
            elif self.type == "wikipediaLoader":
                response = wikipediaLoader(loader_data)
            elif self.type == "MicrosoftLoader":
                response = MicrosoftLoader(loader_data)
            documents = response.load()
            logging.info("////file_name////")
            logging.info(file_name)
            logging.info("////file_name////")
            if file_name != "":
                logging.info(f"deleting temp file: {file_name}")
                os.remove(file_name) #delete file    /app/robotfiles/UbilityLibraries/temp/
                file_name=''
                logging.info("file deleted succ")
            return documents
        except Exception as error:
            raise Exception(error)
 
 
def MicrosoftLoader(loader_data):
    logging.info("load data in MicrosoftLoader")
    global file_name
    try:
        temp_folder_path="/app/robotfiles/UbilityLibraries/temp/"
        binary_file=loader_data['data']
        fileType = loader_data['fileType']
        
        if fileType == "Excel":
            logging.info("data type excel")
            temp_file_name=generate_random_filename("xlsx")
            file_name=temp_folder_path+temp_file_name
            create_binary_temp_file(file_name,binary_file)
            logging.info(f"file created :  {file_name}")
            return UnstructuredExcelLoader(file_name, mode="elements")
        elif fileType == "Powerpoint":
            logging.info("data type powerpoint")
            temp_file_name=generate_random_filename("pptx")
            file_name=temp_folder_path+temp_file_name
            create_binary_temp_file(file_name,binary_file)
            logging.info(f"file created :  {file_name}")
            return UnstructuredPowerPointLoader(file_name, mode="elements")
        elif fileType == "Word":
            logging.info("data type word")
            temp_file_name=generate_random_filename("docx")
            file_name=temp_folder_path+temp_file_name
            create_binary_temp_file(file_name,binary_file)
            logging.info(f"file created :  {file_name}")
            return UnstructuredWordDocumentLoader(file_name, mode="elements")
    except Exception as error:
        raise Exception(error) 
        
def wikipediaLoader(loader_data):
    logging.info("load data in wikipediaLoader")
    try:
        docs=loader_data['loadMaxDocs']
        query=loader_data['query']
        return WikipediaLoader(query=query, load_max_docs=docs)
    except Exception as error:
        raise Exception(error)


def webPageLoader(loader_data):
    logging.info("load data in webPageLoader")
    try:
        urls = loader_data['urls']
        return WebBaseLoader(urls)
    except Exception as error:
        raise Exception(error)

def basicDataLoader(loader_data):
    logging.info("load data in basicDataLoader")
    global file_name
    try:
        temp_folder_path="/app/robotfiles/UbilityLibraries/temp/"
        dataType = loader_data['dataType']
        dataFormat = loader_data['dataFormat']
        data = loader_data['data']
        if dataType == "PDF":
            logging.info("data type PDF")
            if dataFormat == "URL":  # no (Data) format_type for pdf
                logging.info("data format URL")
                response = PyPDFLoader(data)
            elif dataFormat == "Binary":
                logging.info("data format Binary")
                temp_file_name=generate_random_filename("pdf")
                file_name=temp_folder_path+temp_file_name
                create_binary_temp_file(file_name,data)
                response = PyPDFLoader(file_name)
        elif dataType == "CSV":
            logging.info("data type CSV")
            if dataFormat == "Data": 
                logging.info("data format DATA")
                temp_file_name=generate_random_filename("csv")
                file_name=temp_folder_path+temp_file_name
                create_temp_file(file_name,data) #create file
                response = CSVLoader(file_name)
            elif dataFormat == "Binary":
                logging.info("data format Binary")
                temp_file_name=generate_random_filename("csv")
                file_name=temp_folder_path+temp_file_name
                create_binary_temp_file(file_name,data)
                response = CSVLoader(file_name)
        elif dataType == "JSON":
            logging.info("data type JSON")
            if dataFormat == "URL":
                logging.info("data format URL")
                response = WebBaseLoader(data)
            elif dataFormat == "Data":
                logging.info("data format DATA")
                temp_file_name=generate_random_filename("json")
                file_name=temp_folder_path+temp_file_name
                if isinstance(data,dict):
                    data=json.dumps(data)
                data=data.replace("'", '"')
                data=data.replace("True", 'true')
                data=data.replace("False", 'false')
                data=data.replace("null", 'None')
                create_temp_file(file_name,data) #create file
                response = JSONLoader(file_path=file_name,jq_schema='.',text_content=False)
            elif dataFormat == "Binary":
                logging.info("data format Binary")
                temp_file_name=generate_random_filename("json")
                file_name=temp_folder_path+temp_file_name
                create_binary_temp_file(file_name,data)
                response = JSONLoader(file_path=file_name,jq_schema='.',text_content=False)
        elif dataType == "TEXT":
            logging.info("data type TEXT")
            if dataFormat == "URL":
                logging.info("data format URL")
                response = WebBaseLoader(data)
            elif dataFormat == "Data":
                logging.info("data format DATA")
                temp_file_name=generate_random_filename("txt")
                file_name=temp_folder_path+temp_file_name
                create_temp_file(file_name,data) #create file
                response = TextLoader(file_name)
            elif dataFormat == "Binary":
                logging.info("data format Binary")
                temp_file_name=generate_random_filename("txt")
                file_name=temp_folder_path+temp_file_name
                create_binary_temp_file(file_name,data)
                response = TextLoader(file_name)
        return response
    except Exception as error:
        raise Exception(error)

def generate_random_filename(extension):
    logging.info("generate random filename")
    try:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Generate a random string of letters and digits
        filename = random_string + '.' + extension   # Concatenate the random string with the extension
        return filename
    except Exception as error:
        raise Exception (error)



def create_temp_file(temp_file_name,data):
    logging.info("creating file")
    try:
        with open(temp_file_name, 'w') as file:
            try:
                file.write(data)
            except (IOError, OSError):
                raise Exception("Error writing to file")
    except (FileNotFoundError, PermissionError, OSError):
        raise Exception("Error opening file")
    finally:
        file.close()

def create_binary_temp_file(temp_file_name,data):
    logging.info("creating binary file")
    try:
        file_data = base64.b64decode(data)
        with open(temp_file_name, 'wb') as file:
            try:
                file.write(file_data)
            except (IOError, OSError):
                raise Exception("Error writing to file")
    except (FileNotFoundError, PermissionError, OSError):
        raise Exception("Error opening file")
    finally:
        file.close()