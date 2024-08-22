#####################################################################
# The core element of any language model application is...the model.#
#####################################################################


# pip install -qU langchain-anthropic
# pip install --upgrade --quiet  langchain-aws
# pip install langchain-openai
# pip install --upgrade --quiet  langchain-google-vertexai
# pip install -U langchain-mistralai
# pip install --upgrade langchain-together
# pip install -U langchain-cohere

import logging
from typing import (Any,Callable,Dict,Generator,Iterable,List,Optional,Tuple,Type)
import os
import types


from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models.ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_aws import ChatBedrock
from langchain_community.chat_models.google_palm import ChatGooglePalm
from langchain_openai import AzureChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_cohere import ChatCohere
from langchain_together import ChatTogether
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_google_vertexai import ChatVertexAI




class Model:
    
    _VALID_PROVIDERS=["openAi","ollama","anthropic","awsBedrock","googlePaLMGemini","azureOpenAi","mistralAi","cohere","togetherAi","huggingFace","vertexAi"]
    
    def __init__(
        self,
        provider: str,
        model: str,
        credentials: dict,
        params: dict = {}
        ):
        """
            Create object for your model
            
            Example:
                .. code-block:: python

                    from uintegrate_langchain.model import Model

                    my_model_object = Model(
                        provider = "openAi",
                        credentials = {"apiKey":"fdfd7fds8fsd"},
                        model = "text-embedding-3-large"
                    )
        """
        logging.info("--------------Start--------------")
        logging.info("Setting up model object")
        
        if provider in self._VALID_PROVIDERS:
            self.provider = provider
        else:
            raise ValueError(f"Invalid provider '{provider}'. Valid providers are: {', '.join(self._VALID_PROVIDERS)}")
        
        self.model= model
        self.credentials=credentials
        self.params=params
        
        # Call the model functions based on the provider
        if self.provider == "openAi":
            logging.info("It is a openAi provider")
            self._setup_openAi(self.credentials)
        elif self.provider == "ollama":
            logging.info("It is a ollama provider")
            self._setup_ollama(self.credentials)
        elif self.provider == "anthropic":
            logging.info("It is an anthropic provider")
            self._setup_anthropic(self.credentials)
        elif self.provider == "awsBedrock":
            logging.info("It is an awsBedrock provider")
            self._setup_awsBedrock(self.credentials)
        elif self.provider == "googlePaLMGemini":
            logging.info("It is an googlePaLMGemini provider")
            self._setup_googlePaLMGemini(self.credentials)
        elif self.provider == "azureOpenAi":
            logging.info("It is an azureOpenAi provider")
            self._setup_azureOpenAi(self.credentials)
        elif self.provider == "mistralAi":
            logging.info("It is an mistralAi provider")
            self._setup_mistralAi(self.credentials)
        elif self.provider == "cohere":
            logging.info("It is an cohere provider")
            self._setup_cohere(self.credentials)
        elif self.provider == "togetherAi":
            logging.info("It is an togetherAi provider")
            self._setup_togetherAi(self.credentials)
        elif self.provider == "huggingFace":
            logging.info("It is an huggingFace provider")
            self._setup_huggingFace(self.credentials)
        elif self.provider == "vertexAi":
            logging.info("It is an vertexAi provider")
            self._setup_vertexAi(self.credentials)
            

    #set up openAi object 
    def _setup_openAi(self,cred):
        try:
            if "OpenAI" in cred:
                self.api_key=cred["OpenAI"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing OpenAI credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up ollama object 
    def _setup_ollama(self,cred):
        try:
            if "Ollama" in cred:
                self.base_url=cred["Ollama"]["ollamaBaseUrl"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Ollama credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up anthropic object 
    def _setup_anthropic(self,cred):
        try:
            if "Anthropic" in cred:
                self.api_key=cred["Anthropic"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Anthropic credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up awsBedrock object 
    def _setup_awsBedrock(self,cred):
        try:
            if "AWSBedrock" in cred:
                self.region_name=cred["AWSBedrock"]["regionName"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing AWS Bedrock credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up googlePaLMGemini object 
    def _setup_googlePaLMGemini(self,cred):
        try:
            if "GooglePaLMGemini" in cred:
                self.api_key=cred["GooglePaLMGemini"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Google PaLM (Gemini) credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up azureOpenAi object 
    def _setup_azureOpenAi(self,cred):
        try:
            if "AzureOpenAi" in cred:
                self.api_key=cred["AzureOpenAi"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Azure OpenAI credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up mistralAi object 
    def _setup_mistralAi(self,cred):
        try:
            if "MistralAi" in cred:
                self.api_key=cred["MistralAi"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing MistralAI credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up cohere object 
    def _setup_cohere(self,cred):
        try:
            if "Cohere" in cred:
                self.api_key=cred["Cohere"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing Cohere credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up togetherAi object 
    def _setup_togetherAi(self,cred):
        try:
            if "TogetherAi" in cred:
                self.api_key=cred["TogetherAi"]["apiKey"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing TogetherAi credentials")
        except Exception as error:
            raise Exception(error)
        
    #set up huggingFace object 
    def _setup_huggingFace(self,cred):
        try:
            if "HuggingFace" in cred and "endpoint" in self.params:
                self.api_token=cred["HuggingFace"]["apiToken"]
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing HuggingFace credentials or params")
        except Exception as error:
            raise Exception(error)

    #set up vertexAi object 
    def _setup_vertexAi(self,cred):
        try:
            if "VertexAi" in cred:
                optionals = self.params
                self.kwargs = {
                        "project_id": cred["VertexAi"]["projectId"],
                        "credentials": cred["VertexAi"]["credentials"],
                        **optionals
                    }
                logging.info("--------------Done--------------")
            else:
                raise Exception("missing VertexAI credentials")
        except Exception as error:
            raise Exception(error)
        
        
        
    def embedding(self):
        """
            Embedding model are used to transform words into numerical arrays or vectors.
        """
        _VALID_EMBEDDING_PROVIDERS=["openAi","ollama"]
        logging.info("Create embedding model")
        try:
            if self.provider in _VALID_EMBEDDING_PROVIDERS:
                optionals = self.params
                if self.provider == "openAi":
                    response = OpenAIEmbeddings(openai_api_key= self.api_key,model=self.model,**optionals)
                elif self.provider == "ollama":
                    response = OllamaEmbeddings(base_url=self.base_url,model=self.model,**optionals)
                return response
            else:
                raise ValueError(f"Invalid method for provider '{self.provider}'. Valid providers for embedding method are: {', '.join(_VALID_EMBEDDING_PROVIDERS)}")
        except ValueError as error:
            raise ValueError(error)
        except Exception as error:
            raise Exception(error)
        
    def chat(self):
        """
            A chat model is a language model that uses chat messages as inputs and returns chat messages as outputs (as opposed to using plain text)
        """
        _VALID_CHAT_PROVIDERS=["openAi","ollama","anthropic","awsBedrock","googlePaLMGemini","azureOpenAi","mistralAi","cohere","togetherAi","huggingFace","vertexAi"]
        logging.info("Create chat model")
        try:
            if self.provider in _VALID_CHAT_PROVIDERS:
                optionals = self.params["optionals"]
                if self.provider == "openAi":
                    llm = ChatOpenAI(model=self.model, api_key=self.api_key,**optionals)
                elif self.provider == "ollama":
                    llm = ChatOllama(model=self.model, base_url=self.base_url,**optionals)
                elif self.provider == "anthropic":
                    llm = ChatAnthropic(model=self.model, anthropic_api_key=self.api_key,**optionals)
                elif self.provider == "awsBedrock":
                    llm = ChatBedrock(region_name=self.region_name, model_id=self.model, model_kwargs=optionals)
                elif self.provider == "googlePaLMGemini":
                    llm = ChatGooglePalm(google_api_key=self.api_key, model_name=self.model, **optionals)
                elif self.provider == "azureOpenAi":
                    llm = AzureChatOpenAI(api_key=self.api_key, model=self.model, **optionals)
                elif self.provider == "mistralAi":
                    llm = ChatMistralAI(api_key=self.api_key, model_name=self.model, **optionals)
                elif self.provider == "cohere":
                    llm = ChatCohere(cohere_api_key=self.api_key, model=self.model, **optionals)
                elif self.provider == "togetherAi":
                    llm = ChatTogether(api_key=self.api_key, model=self.model, **optionals)
                elif self.provider == "huggingFace":
                    llm_model = HuggingFaceEndpoint(huggingfacehub_api_token=self.api_token, endpoint_url=self.params["endpoint"], model=self.model, **optionals)
                    llm = ChatHuggingFace(llm=llm_model)
                elif self.provider == "vertexAi":
                    kwargs=self.kwargs
                    llm = ChatVertexAI(model_name=self.model, **kwargs)
                return llm
            else:
                raise ValueError(f"Invalid method for provider '{self.provider}'. Valid providers for chat method are: {', '.join(_VALID_CHAT_PROVIDERS)}")
        except ValueError as error:
            raise ValueError(error)
        except Exception as error:
            raise Exception(error)