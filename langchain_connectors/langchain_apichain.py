from langchain.chains.api.base import APIChain
from langchain_core.prompts import PromptTemplate
import json
import sys
import os

from ubility_langchain.model import Model
from ubility_langchain.callbacks_handler import LogsCallbackHandler, TokenCounter
from ubility_langchain.functions import post_langchain_to_elasticsearch, calculate_total_cost
import threading

def langchain_apichain(cred, model, inputs, flowName, userId):
    try:
        cred = json.loads(cred)

        handler = LogsCallbackHandler()

        if "provider" in model and "params" in model and "optionals" in model["params"]:
            llm_model = Model(provider=model["provider"], model=model["model"] if "model" in model else "", credentials=cred, params=model["params"]).chat()

        else:
            raise Exception("Missing Model Data")
        
        if "apiDocs" in inputs and "apiUrlPrompt" in inputs and "apiResponsePrompt" in inputs and "query" in inputs:
            apiChain = APIChain.from_llm_and_api_docs(
                llm=llm_model,
                api_docs=inputs["apiDocs"],
                limit_to_domains=None,
                headers=inputs["headers"] if "headers" in inputs else {},
                api_url_prompt=PromptTemplate(
                    template=inputs["apiUrlPrompt"],
                    input_variables=["question", "api_docs"],
                ),
                api_response_prompt=PromptTemplate(
                    template=inputs["apiResponsePrompt"],
                    input_variables=["question", "api_docs", "api_url", "api_response"],
                ),
                callbacks=[handler]
            )

            token_counter = TokenCounter(llm_model)
            result = apiChain.invoke(inputs["query"], config={"callbacks": [token_counter]})

            final_result = {}
            if type(result) == dict:
                for key, value in result.items():
                    final_result[key] = str(result[key])

            # calculate the total cost based on the number of tokens and the model
            cost = calculate_total_cost(token_counter, model["model"])

            # prepare chatModel json: {provider, model, cost}
            chatModelJson = {
                "provider": model["provider"],
                "model": model["model"],
                "cost": str(cost)
            }

            # post chain to elasticsearch
            logs = handler.log + "\n" + str(final_result)
            thread = threading.Thread(target=post_langchain_to_elasticsearch, args=(flowName, userId, chatModelJson, "API Chain", inputs["query"], final_result, token_counter.total_tokens, logs))
            thread.start()

        else:
            raise Exception("Missing Input Data")

        return final_result

    except Exception as exec:
        raise Exception(exec)