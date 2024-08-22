import json
from openai import OpenAI
def openai_chat_completion(creds,params):
    """
    Generate a chat-based completion using the OpenAI GPT-3.5-turbo model.

    :param dict cred:
        A dictionary containing API key and optional organization details.
        - apiKey (str): OpenAI API key for authentication. (required)
        - org (str): Optional organization name associated with the API key. (optional)

    :param dict params:
        - prompt (str): The user's message prompt. (required)
        - simplify (bool): Whether to return only the content of the completed message or the full completion details.
        - optional(dict):
            - frequency_penalty (float): Controls the likelihood of using less common completions.
            - max_tokens (int): Maximum number of tokens to generate in the completion.
            - n (int): Number of completions to generate.
            - presence_penalty (float): Controls the likelihood of the model generating completions related to the input context.
            - temperature (float): Controls the randomness of the model's output.
            - top_p (float): Limits the diversity of the model's output to a subset of the most likely tokens.

    :return: A completed message or detailed information about the completion based on the 'simplify' parameter.
    :rtype: str or dict
    """
    try:
        cred=json.loads(creds)
        if "prompt" in params and 'apiKey' in cred:
            if 'organization' in cred:
                openai_client = OpenAI(api_key=cred['apiKey'], organization=cred["organization"])
            else:
                openai_client = OpenAI(api_key=cred['apiKey'])
            if 'optional' in params:
                data={}
                for key, value in params["optional"].items():
                    if value:
                        data[key] = value
                completion = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content":params["prompt"]}
                ],
                **data
            )
            else:
                completion = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content":params["prompt"]}
                    ]
                )
            if params["simplify"]:
                return completion.choices[0].message.content
            else:
                completion_dict={
                "id": completion.id,
                "choices": [
                    {
                        "finish_reason": choice.finish_reason,
                        "index": choice.index,
                        "logprobs": choice.logprobs,
                        "message_content": choice.message.content if choice.message else None
                    }
                    for choice in completion.choices
                ],
                "created":completion.created,
                "model":completion.model,
                "object":completion.object,
                "system_fingerprint":completion.system_fingerprint,
                "usage": {
                    "completion_tokens":completion.usage.completion_tokens,
                    "prompt_tokens":completion.usage.prompt_tokens,
                    "total_tokens":completion.usage.total_tokens
                }
            }
                return completion_dict
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

