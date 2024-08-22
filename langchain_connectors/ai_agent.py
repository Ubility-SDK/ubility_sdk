
from langchain_community.chat_models.openai import ChatOpenAI
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain.chains.llm import LLMChain
from langchain.chains.llm_math.base import LLMMathChain
from ubility_langchain.model import Model
from langchain.tools import BaseTool
import requests
import json
import os, io
import logging


class GetTrigger(BaseTool):
    name = "trigger-flow"
    description = ""
    url = ""

    def _run(self):
        def get():
            url = self.url
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)

            return "triggered successfully"

        trigger = get()
        return trigger

    def _arun(self):
        raise NotImplementedError("This tool does not support async")


class PostTrigger(BaseTool):
    name = "trigger-flow"
    description = ""
    url = ""
    body = {}
    query = ""

    def _run(self, **kwargs):
        def post():
            multi_input_template = """
            Given the following JSON object, where each key's description is provided as its value, and a user query, 
            replace each description with the appropriate value based on the query. Your response should be the final JSON object.

            JSON to fill:
            {jsonTofill}

            User question or query:
            {query}

            Instructions:
            1. Identify the relevant information from the user query.
            2. Replace each key's description in the JSON object with the appropriate value based on the user query.
            3. Ensure the final JSON object is correctly formatted and complete.

            Respond with the final JSON object only.
            """
            multi_input_prompt = PromptTemplate(
                input_variables=["jsonTofill", "query"], template=multi_input_template
            )
            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0,
                openai_api_key="",
            )
            llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm, verbose=True)
            finalBody = llm_chain.run({"jsonTofill": self.body, "query": self.query})
            input_dict = eval(finalBody)
            json_output = json.dumps(input_dict)
            url = self.url
            payload = json_output
            headers = {"Content-Type": "application/json"}
            logging.warning(payload)
            response1 = requests.request("POST", url, headers=headers, data=payload)
            logging.warning(response1.text)
            response = requests.request("GET", response1.text, headers=headers)
            logging.warning(response.text)
            while "ocessing..." in response.text:
                response = requests.request("GET", response1.text, headers=headers)
                logging.warning(response.text)
            return response.text

        trigger = post()
        return trigger

    def _arun(self):
        raise NotImplementedError("This tool does not support async")


class PythonCustomTool(BaseTool):
    name = ""
    description = ""
    code = ""
    query = ""

    def _run(self):
        multi_input_template = """
        {pythonCode}
        The above is a python code that you will use it and run it to get answer.
        You are responsable to get the {query} and run the above function only.
        Dont develop a new python script and use it.
        And get variables from query if the function has arguments. 
        """
        print(multi_input_template)
        multi_input_prompt = PromptTemplate(
            input_variables=["pythonCode", "query"], template=multi_input_template
        )
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key="",
        )
        llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
        finalAnswer = llm_chain.run({"pythonCode": self.code, "query": self.query})
        print(finalAnswer)
        return finalAnswer

    def _arun(self):
        raise NotImplementedError("This tool does not support async")


def create_custom_tools(tools, params, cred, inputs):
    try:
        for tool in params["tools"]:
            if tool["type"] == "getTrigger":
                tools.append(
                    GetTrigger(
                        name=tool["name"],
                        description=tool["description"],
                        url=tool["params"]["url"],
                    )
                )
            if tool["type"] == "postTrigger":
                tools.append(
                    PostTrigger(
                        name=tool["name"],
                        description=tool["description"],
                        url=tool["params"]["url"],
                        body=tool["params"]["body"],
                        query=inputs["query"],
                    )
                )
            if tool["type"] == "pythonCode":
                tools.append(
                    PythonCustomTool(
                        name=tool["name"],
                        description=tool["description"],
                        code=tool["params"]["customPythonCode"],
                        query=inputs["query"],
                    )
                )
            if tool["type"] == "serpApi":
                serpApi = SerpAPIWrapper(serpapi_api_key=cred["SerpApi"]["apiKey"])
                tools.append(
                    Tool(
                        name="serpApiWrapper",
                        func=serpApi.run,
                        description="Useful when you need to search to get answer",
                    )
                )
            if tool["type"] == "wikipidia":
                wikipedia = WikipediaAPIWrapper()
                tools.append(
                    Tool(
                        name="wikipedia",
                        func=wikipedia.run,
                        description="Useful for when you need to look up a topic, country or person on wikipedia",
                    )
                )
            if tool["type"] == "calculator":
                llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0,
                    openai_api_key="",
                )
                llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
                tools.append(
                    Tool.from_function(
                        func=llm_math_chain.run,
                        name="Calculator",
                        description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions.",
                    )
                )

        return tools

    except Exception as exc:
        raise Exception(exc)


def create_default_tools(tools):
    try:
        search = GoogleSearchAPIWrapper(
            google_api_key="",
            google_cse_id="",
        )
        default_search_ubility_tool = Tool(
            name="current-search",
            func=search.run,
            description="Useful when you need to answer questions about nouns, current events or the current state of the world.",
        )
        tools.append(default_search_ubility_tool)

        return tools

    except Exception as exc:
        raise Exception(exc)
  
    
def invoke(inputs, model, params, cred):
    """
    inputs:{
        prompt: {
            text: string
            inputs: string
        }
        agentType: string
        query: string
    }
    params :{
        tools:[
            {
                type: string[getTrigger, postTrigger, pythonCode, serpApi]
                name: string
                description: string
                params:{
                    url: string
                    body: {
                        key: string(description)
                    }
                    customPythonCode: string
                    customJavaScriptCode: string
                }
            }
        ]
        memory:{
            "type": "ConversationBufferMemory",
            "historyId":"164e70e4ced"
        }
    }
    """
    try:
        cred = json.loads(cred)
        tools = []
        if "tools" in params:
            tools = create_custom_tools(tools, params, cred, inputs)

        if tools == []:
            tools = create_default_tools(tools)

        if "provider" in model and "params" in model and "optionals" in model["params"]:
            llm_model = Model(provider=model["provider"], model=model["model"] if "model" in model else "", credentials= cred, params=model["params"]).chat()

        else:
            raise Exception("Missing Model Data")
        
        logging.warning("test1")
        if "memory" in params and "type" in params["memory"]:
            memory = ConversationBufferMemory(memory_key="history", return_messages=True)

            if 'context' in params["memory"] :
                for context in params["memory"]['context']:
                    memory.save_context({'input': str(context['input'])},{"output": str(context['output'])})

            if "historyId" in params["memory"]:
                historyId = params["memory"]["historyId"]
                filePath = f"/langchain_connectors/langchain_history/{historyId}.json"
                if os.path.exists(filePath):
                    f = open(filePath)
                    
                    try:
                        data = json.load(f)
                    except Exception:
                        data = {"context": []}
                    f.close()
                    for context in data["context"]:
                        memory.save_context({"input": str(context["input"])}, {"output": str(context["output"])})
                else:
                    with io.open(filePath, "w", encoding="utf-8") as file:
                        data = {"context": []}
                        str_ = json.dumps(
                            data,
                            indent=4,
                            sort_keys=True,
                            separators=(",", ": "),
                            ensure_ascii=False,
                        )
                        file.write(str_)
            else:
                raise Exception("missing history id")

        if inputs["agentType"] == "openai-functions-agent":
            agent_executor = initialize_agent(
                tools=tools,
                llm=llm_model,
                agent=AgentType.OPENAI_MULTI_FUNCTIONS,
                max_iterations=5,
                verbose=True,
            )
            
            if "memory" in params:
                agent_executor.agent.prompt.input_variables.append("history")
                agent_executor.agent.prompt.messages.insert(1, MessagesPlaceholder(variable_name="history"))
                agent_executor.memory = memory

            
        if inputs["agentType"] == "react":
            agent_executor = initialize_agent(
                tools=tools,
                llm=llm_model,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                max_iterations=10,
                verbose=True,
            )
            
        if inputs["agentType"] == "conversational-agent":
            agent_executor = initialize_agent(
                tools=tools,
                llm=llm_model,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                max_iterations=5,
                verbose=True,
            )

            if "memory" in params:
                agent_executor.agent.llm_chain.prompt.input_variables.append("history")
                agent_executor.agent.llm_chain.prompt.messages.insert(1, MessagesPlaceholder(variable_name="history"))
                agent_executor.memory = memory
        
        answer = agent_executor.invoke(input=inputs["query"])
        if type(answer) == dict:
                                for key, value in answer.items():
                                    answer[key] = str(answer[key])
                                    
        if "memory" in params and "type" in params["memory"] and "historyId" in params["memory"]:
            f = open(filePath)
            logging.warning("teni")
            try:
                data = json.load(f)
            except Exception:
                data = {"context": []}
            f.close()

            data["context"].append({"input": inputs["query"], "output": answer["output"]})
            with io.open(filePath, "w", encoding="utf-8") as file:
                str_ = json.dumps(
                    data,
                    indent=4,
                    sort_keys=True,
                    separators=(",", ": "),
                    ensure_ascii=False,
                )
                file.write(str_)

        return answer
    
    except Exception as exc:
        raise Exception(exc)

