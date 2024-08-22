from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import sys
import os
UbilityLibraries = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(UbilityLibraries)
from langchain_connectors.ubility_langchain.document_loader import DocumentLoader
from langchain_connectors.ubility_langchain.model import Model
from langchain_connectors.ubility_langchain.vector_store import VectorStore


import logging


def Langchain_upsert(cred,document_loader_data,vector_store,embedding_model):
    try:

        creds=json.loads(cred)
        
        # Step 1: Load the data from input and split it
        chunkSize = document_loader_data['chunkSize']
        chunkOverlap = document_loader_data['chunkOverlap']  

        documents = DocumentLoader(type=document_loader_data['type']).load(document_loader_data)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunkSize, chunk_overlap=chunkOverlap)
        texts = text_splitter.split_documents(documents)  # Split data
        nbr_of_docs=len(texts)
        if nbr_of_docs !=0 :
            
            # Step 2: Create embedding using given model type
            provider = embedding_model["provider"]
            model = embedding_model["model"]
            embedding = Model(provider,model,creds).embedding()
            # Step3 : Insert splited data into vector store after embedding it using the created model
            vectoreStore_type = vector_store["type"]
            vectoreStore_details = vector_store
            insert_data= VectorStore(vectoreStore_type,creds,vectoreStore_details).insert_data(texts,embedding,vectoreStore_details)
            return {"Message":f"{nbr_of_docs} documents had been inserted to {vectoreStore_type}"}
        else:
            raise Exception("No data found to be retrieved")

    except Exception as error:
        raise Exception(error)

   