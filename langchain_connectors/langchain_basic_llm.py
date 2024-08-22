
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.output_parsers.list import CommaSeparatedListOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import json


from ubility_langchain.callbacks_handler import LogsCallbackHandler, TokenCounter
from ubility_langchain.model import Model
from ubility_langchain.functions import post_langchain_to_elasticsearch, calculate_total_cost
import threading
import socketio
import uuid

def langchain_basic_llm_set_outputParser(params):
    try:
        if params["outputParser"]["type"] == "StructuredOutputParser":
            if "responseSchemas" in params["outputParser"]:
                response_schemas = []
                for resp_schema in params["outputParser"]["responseSchemas"]:
                    response_schemas.append(ResponseSchema(name=resp_schema["name"], description=resp_schema["description"], type= resp_schema["type"]))

                output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

            else:
                raise Exception("Missing Required Inputs")
        
        if params["outputParser"]["type"] == "CommaSeparatedListOutputParser":
            output_parser = CommaSeparatedListOutputParser()
            
        return output_parser
           
    except Exception as exc:
        raise Exception(exc)        

def langchain_basic_llm_create_chain(cred, model, inputs, params, flowName, userId):
    try:
        cred = json.loads(cred)

        # create a callback handler instance to return logs
        handler = LogsCallbackHandler()

        if "provider" in model and "params" in model and "optionals" in model["params"]:
            llm_model = Model(provider=model["provider"], model=model["model"] if "model" in model else "", credentials= cred, params=model["params"]).chat()

        else:
            raise Exception("Missing Model Data")
        
        if "prompt" in inputs and "promptType" in inputs["prompt"]:
            if inputs["prompt"]["promptType"] == "chatPrompt":
                if "query" in inputs and "template" in inputs["prompt"]:
                    messages = []
                    if "messages" in inputs["prompt"]:
                        for human_ai_messages in inputs["prompt"]["messages"]:
                            if "humanMessage" in human_ai_messages and "aiMessage" in human_ai_messages:
                                messages.append(HumanMessage(content=human_ai_messages["humanMessage"]))
                                messages.append(AIMessage(content=human_ai_messages["aiMessage"]))

                    if "outputParser" in params and "type" in params["outputParser"]:
                        if params["outputParser"]["type"] == "StructuredOutputParser":
                            outputParser = langchain_basic_llm_set_outputParser(params)
                            template = inputs["prompt"]["template"] + "{input} {format_instructions}"
                            partialVariables = {"format_instructions": outputParser.get_format_instructions()}
                            inputVariables = ["input", "format_instructions"]

                        if params["outputParser"]["type"] == "CommaSeparatedListOutputParser":
                            nb_of_items = params["outputParser"]["nbOfItems"]
                            outputParser = langchain_basic_llm_set_outputParser(params)
                            template = inputs["prompt"]["template"] + "{input} , Your response should only be an unnumbered list of " + str(nb_of_items) + " items, and you should return the results as a comma separeted list."
                            partialVariables = {}
                            inputVariables = ["input"]
                            
                    else:
                        outputParser = StrOutputParser()
                        template = inputs["prompt"]["template"] + "{input}"
                        partialVariables = {}
                        inputVariables = ["input"]
                        
                    messages.append(HumanMessagePromptTemplate.from_template(template))
                    prompt = ChatPromptTemplate(
                        messages=messages, 
                        input_variables=inputVariables,
                        partial_variables=partialVariables,
                        output_parser=outputParser,
                        )

                    chain = prompt | llm_model 
                    token_counter = TokenCounter(llm_model)

                    result = ""
                    if "streaming" in params and "conversation_id" in params["streaming"]:
                        conv_id = params["streaming"]["conversation_id"]
                        sio = socketio.Client()
                        custom_client_id = str(uuid.uuid4())
                        sio.connect('', headers={'client_id': custom_client_id,'conversation_id':conv_id})
                        for chunk in chain.stream(input=inputs["query"], config={"callbacks": [handler, token_counter]}):
                            sio.send({'message':chunk.content, 'conversation_id': conv_id})
                            result += chunk.content

                    else:
                        for chunk in chain.stream(input=inputs["query"], config={"callbacks": [handler, token_counter]}):
                            result += chunk.content
                    
                    input_to_post = inputs["query"]
                    
                else:
                    raise Exception("Missing Query")
    
            if inputs["prompt"]["promptType"] == "Prompt":
                if "promptInputs" in inputs:
                    if "template" in inputs["prompt"]:
                        if "outputParser" in params and "type" in params["outputParser"]:
                            if params["outputParser"]["type"] == "StructuredOutputParser":
                                template = inputs["prompt"]["template"] + " {format_instructions} "
                                outputParser = langchain_basic_llm_set_outputParser(params)
                                partialVariables = {"format_instructions": outputParser.get_format_instructions()}
                            
                            if params["outputParser"]["type"] == "CommaSeparatedListOutputParser":
                                nb_of_items = params["outputParser"]["nbOfItems"]
                                template = inputs["prompt"]["template"] + ", Your response should only be an unnumbered list of " + str(nb_of_items) + " items, and you should return the results as a comma separeted list."
                                outputParser = langchain_basic_llm_set_outputParser(params)
                                partialVariables = {}

                        else:
                            template = inputs["prompt"]["template"]
                            outputParser = StrOutputParser()
                            partialVariables = {}

                        prompt = PromptTemplate(
                        template=template,
                        input_variables=inputs["prompt"]["inputVariables"] if "inputVariables" in inputs["prompt"] else [],
                        partial_variables=partialVariables,
                        output_parser=outputParser,
                        )      

                        chain = prompt | llm_model 
                        token_counter = TokenCounter(llm_model)

                        result = ""
                        if "streaming" in params and "conversation_id" in params["streaming"]:
                            conv_id = params["streaming"]["conversation_id"]
                            sio = socketio.Client()
                            custom_client_id = str(uuid.uuid4())
                            sio.connect('', headers={'client_id': custom_client_id,'conversation_id':conv_id})
                            for chunk in chain.stream(input=inputs["promptInputs"], config={"callbacks": [handler, token_counter]}):
                                sio.send({'message':chunk.content, 'conversation_id': conv_id})
                                result += chunk.content
                        else:
                            for chunk in chain.stream(input=inputs["promptInputs"], config={"callbacks": [handler, token_counter]}):
                                result += chunk.content

                        input_to_post = inputs["prompt"]["template"]

                    else:
                        raise Exception("Missing template")
                
                else:
                    raise Exception("Missing Prompt Inputs")
                    
        else:
            raise Exception("Missing Prompt")
        
        if "outputParser" in params:
            answer = result
            parsedAnswer = outputParser.parse(answer)
            if type(parsedAnswer) == dict:
                resp_to_return = parsedAnswer
                # reformulate the type of values to string
                resp_to_post = {}
                for key, value in parsedAnswer.items():
                    resp_to_post[key] = str(parsedAnswer[key])

            if type(parsedAnswer) == list:
                resp_to_return = {"answer" : parsedAnswer}
                resp_to_post = {"answer" : str(parsedAnswer)}
            
        else:
            resp_to_return = result
            resp_to_post = {}
            if type(result) == dict:
                for key, value in result.items():
                    resp_to_post[key] = str(result[key])
            else:
                resp_to_post = {"answer" : result}

        # calculate the total cost based on the number of tokens and the model
        cost = calculate_total_cost(token_counter, model["model"])

        # prepare chatModel json: {provider, model, cost}
        chatModelJson = {
            "provider": model["provider"],
            "model": model["model"],
            "cost": str(cost)
        }

        # post chain to elasticsearch
        logs = handler.log + "\n" + str(resp_to_post)
        thread = threading.Thread(target=post_langchain_to_elasticsearch, args=(flowName, userId, chatModelJson, "Basic LLM Chain", input_to_post, resp_to_post, token_counter.total_tokens, logs))
        thread.start()

        return resp_to_return

    except Exception as exc:
        raise Exception(exc)