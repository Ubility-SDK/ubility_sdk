
from langchain_community.document_loaders import WebBaseLoader, CSVLoader, JSONLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate


import os
import logging


from ubility_langchain.callbacks_handler import LogsCallbackHandler, TokenCounter
from ubility_langchain.model import Model
from ubility_langchain.functions import post_langchain_to_elasticsearch, calculate_total_cost
import threading
import random
import string
import base64
import json
import socketio
import uuid

# pip install jq

file_name=""

def langchain_summarization_chain(cred, model, inputs, flowName, userId, params):
    try:
        global file_name

        cred = json.loads(cred)

        handler = LogsCallbackHandler()

        if "provider" in model and "params" in model and "optionals" in model["params"]:
            llm_model = Model(provider=model["provider"], model=model["model"] if "model" in model else "", credentials= cred, params=model["params"]).chat()
        else:
            raise Exception("Missing Model Data")
        
        ##############################  chain_type = stuff || map_reduce #############################
        if inputs["chain_type"] == "stuff" or inputs["chain_type"]  == "map_reduce":
            # print("====== STUFF or MAP REDUCE ======")
            if "prompt" in inputs:
                prompt_template = inputs["prompt"]
            else:
                prompt_template = """Write a concise summary of the following:
                "{docs}"
                CONCISE SUMMARY:"""
            prompt = PromptTemplate.from_template(prompt_template)
            chain = (
                {"docs": RunnablePassthrough()}
                | prompt 
                | llm_model
                )
        
        #############################  chain_type = refine  #############################
        if inputs["chain_type"] == "refine":
            # print("====== REFINE ======")
            if "initial_prompt" in inputs and "refine_prompt" in inputs:
                initial_template = inputs["initial_prompt"]
                refine_template = inputs["refine_prompt"]
            else:
                initial_template = """Write a concise summary of the following:
                {docs}
                CONCISE SUMMARY:"""
                refine_template = (
                    "Your job is to produce a final summary\n"
                    "We have provided an existing summary up to a certain point\n"
                    "We have the opportunity to refine the existing summary"
                    "(only if needed) with some more context below.\n"
                    "------------\n"
                    "{docs}\n"
                    "------------\n"
                    "If the context isn't useful, return the original summary."
                )
            
            initial_prompt = PromptTemplate.from_template(initial_template)
            refine_prompt = PromptTemplate.from_template(refine_template)
            chain = (
                {"docs": RunnablePassthrough()}
                | initial_prompt
                | llm_model
                | refine_prompt
                | llm_model
                )
        
        loader = load_input_data(inputs)
        try:
            documents = loader.load()
        except Exception as exec:
            logging.warning("error while loading the document: " + str(exec))
            if file_name != "":
                remove_file(file_name)
                logging.warning("document was removed: " + file_name)
            raise Exception("error while loading the document")
        
        split_docs = create_text_splitter(inputs, documents)
        token_counter = TokenCounter(llm_model)
        
        summary = ""
        if "streaming" in params and "conversation_id" in params["streaming"]:
            conv_id = params["streaming"]["conversation_id"]
            sio = socketio.Client()
            custom_client_id = str(uuid.uuid4())
            sio.connect('', headers={'client_id': custom_client_id,'conversation_id':conv_id})
            for chunk in chain.stream(split_docs, config={"callbacks": [token_counter, handler]}):
                sio.send({'message':chunk.content, 'conversation_id': conv_id})
                summary += chunk.content
        else:
            for chunk in chain.stream(split_docs, config={"callbacks": [token_counter, handler]}):
                summary += chunk.content

        if file_name != "":
            remove_file(file_name)
            logging.warning("document was removed: " + file_name)

        # calculate the total cost based on the number of tokens and the model
        cost = calculate_total_cost(token_counter, model["model"])

        # prepare chatModel json: {provider, model, cost}
        chatModelJson = {
            "provider": model["provider"],
            "model": model["model"],
            "cost": str(cost)
        }

        final_summary = {"Summary": summary}

        # post chain to elasticsearch
        logs = handler.log + "\n" + str(final_summary)
        thread = threading.Thread(target=post_langchain_to_elasticsearch, args=(flowName, userId, chatModelJson, "Summarization Chain", f"{split_docs}", final_summary, token_counter.total_tokens, logs))
        thread.start()

        return final_summary

    except Exception as exec:
        if file_name != "":
            remove_file(file_name)
            logging.warning("document was removed: " + file_name)
        raise Exception(exec)
    
def load_input_data(inputs):
    try:
        global file_name

        if "data_form" in inputs and "data" in inputs:
            if inputs["data_form"] == "URL":
                loader = WebBaseLoader(inputs["data"])

            elif inputs["data_form"] == "Binary":
                if "data_type" in inputs:
                    file_name = generate_random_filename(inputs["data_type"])
                    file_path = "temp/" + file_name
                    add_data_to_file(inputs["data"], file_path)

                    if inputs["data_type"] == "txt":
                        loader = TextLoader(file_path=file_path)
                    elif inputs["data_type"] == "json":
                        loader = JSONLoader(file_path=file_path, jq_schema=".", text_content=False)
                    elif inputs["data_type"] == "pdf":
                        loader = PyPDFLoader(file_path=file_path)
                    elif inputs["data_type"] == "csv":
                        loader = CSVLoader(file_path=file_path)

                else:
                    raise Exception("Missing data_type")
                
        else:    
            raise Exception("Missing data_form or data")
        
        return loader  
    except Exception as exec:
        if file_name != "":
            remove_file(file_name)
            logging.warning("document was removed: " + file_name)
        raise Exception(exec)

def add_data_to_file(data, file_path):
    try:
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(data))

    except Exception as error:
        raise Exception(error)

def generate_random_filename(extension):
    try:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Generate a random string of letters and digits
        filename = random_string + '.' + extension   # Concatenate the random string with the extension
        return filename
    
    except Exception as error:
        raise Exception(error)
    
def create_text_splitter(inputs, documents):
    try:
        if "splitter_type" in inputs and "chunk_size" in inputs and "chunk_overlap" in inputs:
            if inputs["splitter_type"] == "CharacterTextSplitter":
                text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=inputs["chunk_size"], chunk_overlap=inputs["chunk_overlap"]) 
            if inputs["splitter_type"] == "RecursiveCharacterTextSplitter":
                text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=inputs["chunk_size"], chunk_overlap=inputs["chunk_overlap"]) 
            if inputs["splitter_type"] == "TokenTextSplitter":
                text_splitter = TokenTextSplitter(chunk_size=inputs["chunk_size"], chunk_overlap=inputs["chunk_overlap"]) 
        else:
            raise Exception("Missing splitter data")

        split_docs = text_splitter.split_documents(documents)
        return split_docs
    
    except Exception as error:
        raise Exception(error)

def remove_file(file_name):
    os.remove("temp/"+file_name)