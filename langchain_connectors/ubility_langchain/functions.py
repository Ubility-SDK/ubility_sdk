import requests
from decouple import config
from tokencost.constants import TOKEN_COSTS
from tokencost import calculate_cost_by_tokens
import logging
# pip install tokencost

ELASTIC_URL = config("ELASTIC_URL")

def post_langchain_to_elasticsearch(flowName, user_id, chatModelJson, chain_type, inputs, outputs, total_tokens, logs, embeddingModelJson=None):
    try:
        url = f"{ELASTIC_URL}/elastic/langchain/post_result"
        document = {
            "userId": user_id,
            "flowName": flowName,
            "chatModel":chatModelJson,
            "AINode":chain_type,
            "inputs" : inputs,
            "outputs": outputs,
            "totalTokens": total_tokens,
            "logs": logs
        }

        models = []
        providers = []
        models.append(chatModelJson["model"])
        providers.append(chatModelJson["provider"])

        if embeddingModelJson != None:
            document["embeddingModel"] = embeddingModelJson
            if embeddingModelJson["model"] not in models:
                models.append(embeddingModelJson["model"])
            if embeddingModelJson["provider"] not in providers:
                providers.append(embeddingModelJson["provider"])
        
        document["models"] = models
        document["providers"] = providers

        response = requests.post(url=url, json=document, verify=False)
        logging.info("*************************************")
        logging.info(response.json())
        logging.info("*************************************")
        return response.json()

    except Exception as exc:
        raise Exception(exc)
    
def calculate_total_cost(token_counter, model):
    try:
        model = model.lower()
        if model not in TOKEN_COSTS:
            total_cost = None
        else:
            input_cost = calculate_cost_by_tokens(token_counter.input_tokens, model, "input")
            output_cost = calculate_cost_by_tokens(token_counter.output_tokens, model, "output")
            total_cost = input_cost + output_cost

        return total_cost
    
    except Exception as exc:
        raise Exception(exc)
