from langchain_pinecone import Pinecone as langPinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_community.chat_models.ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
import logging
import json

from ubility_langchain.callbacks_handler import LogsCallbackHandler, TokenCounter
from ubility_langchain.functions import post_langchain_to_elasticsearch, calculate_total_cost
import threading
import socketio
import uuid

# pip install tiktoken
# pip install pinecone-client
# pip install langchain
# pip install langchain_community
# pip show langchain_community

def retrieve(inputs, model, vectorStore, embedding, cred, flowName, userId, params = {}):
    """_summary_
    Args:
    {
        "LANGCHAIN_MODEL_QUESTION_AND_ANSWER_CHAIN": {
            "model": "openAi",
            "openAiModel": "12048"
        },
        "LANGCHAIN_vectorStore_QUESTION_AND_ANSWER_CHAIN": {
            "vector": "pinecone",
            "index_name": "fromList"
        },
        "LANGCHAIN_EMBEDDING_QUESTION_AND_ANSWER_CHAIN": {
            "embedding": "openAi",
            "openAiModel": "12248"
        },
        "LANGCHAIN_PARAMS_QUESTION_AND_ANSWER_CHAIN": {},
        "LANGCHAIN_INPUTS_QUESTION_AND_ANSWER_CHAIN": {
            "query": "awdawd",
            "prompt": "adwdwa"
        },
        "LANGCHAINCRED": {
            openAi : {
                apiKey : string
            },
            pinecone : {
                pineconeApiKey : string
            },
            ollama : {
                ollamaBaseUrl : string
            }
        }
    }
    """
    try:
        cred = json.loads(cred)
        handler = LogsCallbackHandler()
        if embedding and vectorStore and model:
            if embedding['provider'] == 'openAi':
                if 'OpenAI' in cred and 'apiKey' in cred['OpenAI']:
                    embeddings = OpenAIEmbeddings(model=embedding['model'], openai_api_key=cred['OpenAI']['apiKey'])
                else:
                    raise Exception('Missing OpenAI API key')
            elif embedding['provider'] == 'ollama':
                embeddings = OllamaEmbeddings()
                if 'Ollama' in cred and 'ollamaBaseUrl' in cred['Ollama']:
                    if 'ollamaModel' in embedding:
                        embeddings = OllamaEmbeddings(model=embedding['model'], base_url=cred['Ollama']['ollamaBaseUrl'])
                else:
                    raise Exception('Missing Ollama base url')
 
            if 'type' in vectorStore :
                if  vectorStore['type'] == 'pinecone':
                    if 'Pinecone' in cred and 'pineconeApiKey' in cred['Pinecone']:
                        if 'indexName' in vectorStore:
                            vectordb = langPinecone(embedding=embeddings, index_name=vectorStore['indexName'], pinecone_api_key=cred['Pinecone']['pineconeApiKey'])
                            retriever = vectordb.as_retriever()
                        else:
                            raise Exception('Missing Pinecone Index')
                    else:
                        raise Exception('Missing Pinecone Api Key')
            else:
                raise Exception('Missing VectorStore type')

            if model['provider'] == 'openAi':
                if 'model' in model:
                    llm = ChatOpenAI(
                        model_name=model['model'],
                        temperature=0,
                        openai_api_key=cred['OpenAI']['apiKey'],
                    )
                else:
                    raise Exception('Missing openai model  model')
            if model['provider'] == 'ollama':
                if 'Ollama' in cred and 'ollamaBaseUrl' in cred['Ollama']:
                    if 'model' in model:
                        llm = ChatOllama(model=model['model'], base_url=cred['Ollama']['ollamaBaseUrl'])
                    else:
                        raise Exception('Missing Ollama model')
                else:
                    raise Exception('Missing Ollama base url')

            if "prompt" in inputs:
                template = inputs["prompt"]
            else:
                template = """
                As an AI assistant you provide answers to the question {question} based on the given context. 
                You must adhere to the following points:
                -Do not use any external data source
                -Do not use your data set
                -Do not use internet to get answer
                -Do not use any external data source if the context is empty
                -Say Idont know. if the context is empty
                -------------------
                context: {context}
                """
            prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            token_counter = TokenCounter(llm)

            answer = ""
            if "streaming" in params and "conversation_id" in params["streaming"]:
                conv_id = params["streaming"]["conversation_id"]
                sio = socketio.Client()
                custom_client_id = str(uuid.uuid4())
                sio.connect('', headers={'client_id': custom_client_id,'conversation_id':conv_id})
                for chunk in chain.stream(inputs["query"], config={"callbacks": [token_counter, handler]}):
                    sio.send({'message':chunk.content, 'conversation_id': conv_id})
                    answer += chunk
            else:
                for chunk in chain.stream(inputs["query"], config={"callbacks": [token_counter, handler]}):
                    answer += chunk

            final_answer = {"answer":answer}

            # calculate the total cost based on the number of tokens and the model
            chatModelCost = calculate_total_cost(token_counter, model["model"])
            embeddingModelCost = calculate_total_cost(token_counter, embedding["model"])

            # prepare chatModel json: {provider, model, cost}
            chatModelJson = {
                "provider": model["provider"],
                "model": model["model"],
                "cost": str(chatModelCost)
            }

            # prepare embeddingModel json: {provider, model, cost}
            embeddingModelJson = {
                "provider": embedding["provider"],
                "model": embedding["model"],
                "cost": str(embeddingModelCost)
            }

            # post chain to elasticsearch
            logs = handler.log + "\n" + str(final_answer)
            thread = threading.Thread(target=post_langchain_to_elasticsearch, args=(flowName, userId, chatModelJson, "Question & Answer Chain", inputs["query"], final_answer, token_counter.total_tokens, logs, embeddingModelJson))
            thread.start()

            return final_answer
        else:
            raise Exception("Missing required input data")
    except Exception as exc:
        raise Exception(exc)