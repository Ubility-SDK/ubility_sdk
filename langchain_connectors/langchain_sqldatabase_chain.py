from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from sqlalchemy import create_engine
import sys
import json
import os

from ubility_langchain.model import Model
from ubility_langchain.callbacks_handler import LogsCallbackHandler, TokenCounter
from ubility_langchain.functions import post_langchain_to_elasticsearch, calculate_total_cost
import threading


def langchain_sqlDatabase_chain(cred, model, inputs, flowName, userId):
    try:
        cred = json.loads(cred)

        handler = LogsCallbackHandler()
        if "provider" in model and "params" in model and "optionals" in model["params"]:
            llm_model = Model(provider=model["provider"], model=model["model"] if "model" in model else "", credentials=cred, params=model["params"]).chat()

        else:
            raise Exception("Missing Model Data")

        if "dbType" in inputs:
            if inputs['dbType'] == 'postgres':
                if 'Postgres' in cred:
                    url = 'postgresql://' \
                                        +cred['Postgres']['username']+':'+cred['Postgres']['password']+'@' \
                                        +cred['Postgres']['host']+':'+cred['Postgres']['port']+'/' \
                                        +cred['Postgres']['database']
                    if "sslMode" in cred['Postgres']:
                        url += '?sslmode='+cred['Postgres']['sslMode']
                else:
                    raise Exception("Missing Postgres Credentials")
                    
            elif inputs['dbType'] == 'mySQL':           
                if 'MySQL' in cred:
                    url = 'mysql+pymysql://' \
                                            +cred['MySQL']['user']+':'+cred['MySQL']['password']+'@' \
                                            +cred['MySQL']['host']+':'+cred['MySQL']['port']+'/' \
                                            +cred['MySQL']['database'] 
                    # if "sslMode" in cred['MySQL']:
                    #     url += '?sslmode='+cred['MySQL']['sslMode']
                else:
                    raise Exception("Missing MySQL Credentials")
                
            else:
                raise Exception(f"Invalid DB Type '{inputs['dbType']}'. Valid types are: 'postgres' and 'mySQL'")
                
            engine = create_engine(url)

        else:
            raise Exception("Missing DB Type")
        
        if "query" in inputs:
            db = SQLDatabase(
                engine=engine, 
                include_tables=inputs["includeTables"] if "includeTables" in inputs else [],
                ignore_tables=inputs["ignoreTables"] if "ignoreTables" in inputs else [],
                sample_rows_in_table_info=inputs["sampleRowsInTableInfo"] if "sampleRowsInTableInfo" in inputs else 3
            )
            agent_executor = create_sql_agent(
                agent_type="tool-calling",
                llm=llm_model,
                db=db,
                top_k=inputs["topK"] if "topK" in inputs else 10,
                verbose=True,
                prompt=PromptTemplate(
                        template=inputs["customPrompt"],
                        input_variables=["agent_scratchpad"],
                    ) if "customPrompt" in inputs else None, # check if "{agent_scratchpad}" in customPrompt
            )

            agent_executor.callbacks = [handler]
            token_counter = TokenCounter(llm_model)
            result = agent_executor.invoke(inputs["query"], config={"callbacks": [token_counter]})

        else:
            raise Exception("Missing Input Data")

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
        thread = threading.Thread(target=post_langchain_to_elasticsearch, args=(flowName, userId, chatModelJson, "SQL Database Chain", final_result["input"], final_result, token_counter.total_tokens, logs))
        thread.start()

        return final_result

    except Exception as exec:
        raise Exception(exec)