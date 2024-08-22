# from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.string import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from typing import List, Dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessageChunk
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage, AIMessage
from ubility_langchain.model import Model
from ubility_langchain.callbacks_handler import LogsCallbackHandler, TokenCounter
from ubility_langchain.functions import post_langchain_to_elasticsearch, calculate_total_cost
import json, threading
import io
import os
import logging
import socketio
import uuid

store = {}


class InMemoryHistory(BaseModel):
    """In memory implementation of chat message history."""
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

def serialize_human_message(obj: HumanMessage) -> Dict[str, str]:
    return {'HumanMessage': obj.content}

def serialize_ai_message_chunk(obj: AIMessageChunk) -> Dict[str, str]:
    return {'AIMessageChunk': obj.content}

def serialize_message(message: BaseMessage) -> Dict[str, str]:
    if isinstance(message, HumanMessage):
        return serialize_human_message(message)
    elif isinstance(message, AIMessageChunk):
        return serialize_ai_message_chunk(message)
    else:
        raise TypeError(f"Unknown type: {type(message)}")

def serialize_in_memory_history(obj: InMemoryHistory) -> List[Dict[str, str]]:
    return [serialize_message(msg) for msg in obj.messages]


def get_session_history(
    session_id: str
) -> BaseChatMessageHistory:
    if (session_id) not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


def langchain_invoke_conversation(inputs, model, cred,chainMemory, flowName, userId, params):
    try:
        global store

        cred = json.loads(cred)

        handler = LogsCallbackHandler()
        if model:
            if "provider" in model and "params" in model and "optionals" in model["params"]:
                llm_model = Model(provider=model["provider"], model=model["model"] if "model" in model else "", credentials= cred, params=model["params"]).chat()
            else:
                raise Exception("Missing Model Data")
                
            if 'type' in chainMemory :
                memory = ConversationBufferMemory(memory_key="history", return_messages= True)
                msgs = []
                if 'context' in chainMemory :
                    for context in chainMemory['context']:
                        input_history = HumanMessage(content=str(context['input']))
                        msgs.append(input_history)
                        output_history = AIMessageChunk(content=str(context['output']))
                        msgs.append(output_history)
                        memory.save_context({'input': str(context['input'])},{"output": str(context['output'])})
                if 'historyId' in chainMemory :
                    historyId = chainMemory['historyId']
                    filePath = f'langchain_connectors/langchain_history/{historyId}.json'
                    if os.path.exists(filePath):
                        f = open(filePath)
                        logging.warning('awal')
                        try:
                            data = json.load(f)
                        except Exception:
                            data = {historyId: []}
                        f.close()
                        # msgs = []
                        for context in data[historyId]:
                            for msg in context:
                                if "HumanMessage" in msg:
                                    input_context = msg["HumanMessage"]
                                    input_history = HumanMessage(content=input_context)
                                    msgs.append(input_history)
                                if "AIMessageChunk" in msg:
                                    output_context = msg["AIMessageChunk"]
                                    output_history = AIMessageChunk(content=output_context)
                                    msgs.append(output_history)
                            if input_context and output_context:
                                # local_store = InMemoryHistory()
                                # local_store.add_messages(messages=msgs)
                                # store[historyId] = local_store
                                memory.save_context({'input': input_context},{"output": output_context})
                            else:
                                raise Exception("input or output not found") 
                    else:
                        with io.open(filePath, 'w', encoding='utf-8') as file:
                            data = {historyId: []}
                            str_ = json.dumps(data,
                                            indent=4, sort_keys=True,
                                            separators=(',', ': '), ensure_ascii=False)
                            file.write(str_)

                local_store = InMemoryHistory()
                local_store.add_messages(messages=msgs)
                store[historyId] = local_store

            else:
                raise Exception('Missing Memory type')
            
            if "prompt" in inputs and "promptType" in inputs["prompt"]:
                if inputs["prompt"]["promptType"] == "chatPrompt":
                    if "query" in inputs and "template" in inputs["prompt"]:
                        messages = []
                        if "messages" in inputs["prompt"]:
                            for human_ai_messages in inputs["prompt"]["messages"]:
                                if "humanMessage" in human_ai_messages and "aiMessage" in human_ai_messages:
                                    messages.append(HumanMessage(content=human_ai_messages["humanMessage"]))
                                    messages.append(AIMessage(content=human_ai_messages["aiMessage"]))

                        outputParser = StrOutputParser()
                        template = inputs["prompt"]["template"] + "{question}"
                        partialVariables = {}
                        inputVariables = ["question"]
                        

                        messages.append(MessagesPlaceholder(variable_name="history"))
                        messages.append(HumanMessagePromptTemplate.from_template(template))

                        prompt = ChatPromptTemplate(
                            messages=messages, 
                            input_variables=inputVariables,
                            partial_variables=partialVariables,
                            output_parser=outputParser,
                            )

                        chain = prompt | llm_model
                        chain_with_history = RunnableWithMessageHistory(
                            chain,
                            get_session_history,
                            memory=memory,
                            input_messages_key="question",
                            history_messages_key="history",
                        )
                        token_counter = TokenCounter(llm_model)
                        
                        result = ""
                        if "streaming" in params and "conversation_id" in params["streaming"]:
                            conv_id = params["streaming"]["conversation_id"]
                            sio = socketio.Client()
                            custom_client_id = str(uuid.uuid4())
                            sio.connect('', headers={'client_id': custom_client_id,'conversation_id':conv_id})
                            for chunk in chain_with_history.stream({"question": inputs['query']}, config={"callbacks": [handler, token_counter], "configurable": {"session_id": historyId}}):
                                sio.send({'message':chunk.content, 'conversation_id': conv_id})
                                result += chunk.content
                        else:
                            for chunk in chain_with_history.stream({"question": inputs['query']}, config={"callbacks": [handler, token_counter], "configurable": {"session_id": historyId}}):
                                result += chunk.content
                           
            else: 
                default_prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", 'The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its history {history}. If the AI does not know the answer to a question, it truthfully says it does not know.'),
                        MessagesPlaceholder(variable_name="history"),
                        ("human", "{question}"),
                    ]
                )
                chain = default_prompt | llm_model
                chain_with_history = RunnableWithMessageHistory(
                    chain,
                    get_session_history,
                    memory=memory,
                    input_messages_key="question",
                    history_messages_key="history",
                )
                token_counter = TokenCounter(llm_model)

                result = ""
                if "streaming" in params and "conversation_id" in params["streaming"]:
                    conv_id = params["streaming"]["conversation_id"]
                    sio = socketio.Client()
                    custom_client_id = str(uuid.uuid4())
                    sio.connect('', headers={'client_id': custom_client_id,'conversation_id':conv_id})
                    for chunk in chain_with_history.stream({"question": inputs['query']}, config={"callbacks": [token_counter, handler], "configurable": {"session_id": historyId}}):
                        sio.send({'message':chunk.content, 'conversation_id': conv_id})
                        result += chunk.content
                else:
                    for chunk in chain_with_history.stream({"question": inputs['query']}, config={"callbacks": [token_counter, handler], "configurable": {"session_id": historyId}}):
                        result += chunk.content

            if 'historyId' in chainMemory:
                json_data = {key: serialize_in_memory_history(value) for key, value in store.items()}
                last_messages = json_data[historyId][-2:]
                f = open(filePath)
                try:
                    data = json.load(f)
                except Exception:
                    data = {historyId: []}
                f.close()
                if historyId in data:
                    data[historyId].append(last_messages)
                else:
                    data[historyId] = []
                    data[historyId].append(last_messages)

                with io.open(filePath, 'w', encoding='utf-8') as file:
                    str_ = json.dumps(data,
                                    indent=4, sort_keys=True,
                                    separators=(',', ': '), ensure_ascii=False)
                    file.write(str_)

            answer = {"answer":result}

            # calculate the total cost based on the number of tokens and the model
            cost = calculate_total_cost(token_counter, model["model"])

            # prepare chatModel json: {provider, model, cost}
            chatModelJson = {
                "provider": model["provider"],
                "model": model["model"],
                "cost": str(cost)
            }

            # post chain to elasticsearch
            logs = handler.log + "\n" + str(answer)
            thread = threading.Thread(target=post_langchain_to_elasticsearch, args=(flowName, userId, chatModelJson, "Conversational Chain", inputs["query"], answer, token_counter.total_tokens, logs))
            thread.start()

            return answer
        else:
            raise Exception("Missing required input data")
    except Exception as exc:
        raise Exception(exc)