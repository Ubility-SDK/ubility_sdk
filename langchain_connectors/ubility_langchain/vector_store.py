###################################################################################
# A vector store takes care of storing embedded data and performing vector search.#
###################################################################################
import logging
from typing import (List)
import os
from datetime import datetime
import base64
from decouple import config


from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.vectorstores import Milvus
from langchain_pinecone import PineconeVectorStore
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.vectorstores.pinecone import Pinecone as langPinecone


from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from elasticsearch import Elasticsearch


class VectorStore:
    
    _VALID_TYPES=["postgres","milvus","pinecone","elasticSearch","ubilityVectorDatabase"]
    
    
    def __init__(
        self,
        type: str,
        credentials: dict,
        params: dict = {}
        ):
        """
            Create object for your vector store
            
            Example:
                .. code-block:: python

                    from uintegrate_langchain.vector_store import VectorStore

                    my_vectorstore_object = VectorStore(
                        type = "postgres",
                        credentials = {"host":"test.uintegrate.io","database":"db","username":"postgres","password":"****"},
                        params = {"collectionName":"my_collection"}
                    )
        """
        logging.info("--------------Start--------------")
        logging.info("Setting up vectore store object")
        
        if type in self._VALID_TYPES:
            self.type = type
        else:
            raise ValueError(f"Invalid type '{type}'. Valid types are: {', '.join(self._VALID_TYPES)}")
        
        self.credentials=credentials
        self.params=params

        # Call the vector store functions based on the type
        if self.type == "postgres":
            logging.info("It is a postgres vector store")
            self._setup_postgres(self.credentials, self.params)
        elif self.type == "milvus":
            logging.info("It is a milvus vector store")
            self._setup_milvus(self.credentials, self.params)
        elif self.type == "pinecone":
            logging.info("It is a pinecone vector store")
            self._setup_pinecone(self.credentials, self.params)
        elif self.type == "elasticSearch":
            logging.info("It is an elasticSearch vector store")
            self._setup_elastic_search(self.credentials, self.params)
            

    #set up postgres object 
    def _setup_postgres(self,cred,params):
        try:
            if "Postgres" in cred:
                host = cred["Postgres"]["host"]
                database = cred["Postgres"]["database"]
                username = cred["Postgres"]["username"]
                password = cred["Postgres"]["password"]
                c_name = params["collectionName"]
                self.connection_url = "postgresql+psycopg2://"+username+":"+password+"@"+host+":5432/"+database
                self.collection_name = c_name
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Postgres credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up milvus object 
    def _setup_milvus(self,cred,params):
        try:
            if "Milvus" in cred:
                host = cred["Milvus"]["host"]
                port = cred["Milvus"]["port"]
                self.connection_args={"host": host, "port": port}
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Milvus credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up pinecone object 
    def _setup_pinecone(self,cred,params):
        try:
            if "Pinecone" in cred:
                self.api_key = cred["Pinecone"]["pineconeApiKey"]
                self.index_name=params["indexName"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Pinecone credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up elastic search object 
    def _setup_elastic_search(self,cred,params):
        try:
            if "ElasticSearch" in cred:
                self.cloud_id = cred["ElasticSearch"]["cloudId"]
                self.user = cred["ElasticSearch"]["userName"]
                self.password = cred["ElasticSearch"]["password"]
                self.index_name = params["indexName"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing ElasticSearch credentials")
        except Exception as error:
            raise Exception(error)

        
    def insert_data(
        self,
        documents:List[Document],
        embedding:Embeddings,
        params: dict = {}
        ):
        """
            Insert data in your vectore store

            Args:
                documents: Splited data (from text splitter)
                embedding: numerical representations of texts in a multidimensional space (you can retrieve it from embedding models)
                params: parameters required while inserting data
                
            Return VectorStore initialized from documents and embeddings.

        """
        logging.info("Insert data in vector store")
        try:
            if self.type == "postgres":
                vectorestore = PGVector.from_documents(
                    embedding=embedding,
                    documents=documents,
                    collection_name=self.collection_name,
                    connection_string=self.connection_url
                    )
            elif self.type == "milvus":
                vectorestore = Milvus.from_documents(
                    documents=documents,
                    embedding=embedding,
                    connection_args=self.connection_args
                    )
            elif self.type == "pinecone":
                os.environ["PINECONE_API_KEY"] = self.api_key
                vectorestore = PineconeVectorStore.from_documents(
                    documents=documents,
                    embedding=embedding,
                    index_name=self.index_name
                    )
            elif self.type == "elasticSearch":
                vectorestore = ElasticsearchStore.from_documents(
                    documents=documents,
                    embedding=embedding,
                    es_cloud_id=self.cloud_id,
                    index_name = self.index_name,
                    es_user = self.user,
                    es_password = self.password
                    )

            return vectorestore
        except ValueError as error:
            raise ValueError(error)
        except Exception as error:
            raise Exception(error)
        
        
    def retrieve_data(
        self,
        embedding:Embeddings
        ):
        """
            Retrieve data from your vectore store

            Args:
                embedding: numerical representations of texts in a multidimensional space (you can retrieve it from embedding models)
                
            Return VectorStoreRetriever initialized from this VectorStore.

        """
        logging.info("Retrieve data from your vectore store")
        try:
            if self.type == "pinecone":
                vectorestore = langPinecone.from_existing_index(
                    embedding=embedding,
                    index_name=self.index_name,
                    api_key=self.api_key
                    )
                retriever = vectorestore.as_retriever()
            return retriever
        except ValueError as error:
            raise ValueError(error)
        except Exception as error:
            raise Exception(error)
        
