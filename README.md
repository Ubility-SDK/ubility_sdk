# Ubility python SDK

The Ubility Python SDK is an open-source library for building AI Apps and automation workflows. The SDK combines the power of LLM orchestrators like Langchain with the App integration workflow like Zapier and make.

Why Ubility SDK?

Python is widely recognized as the go-to programming language for automation due to its simplicity and extensive ecosystem. However, building automation scripts often requires reading and understanding the documentation of each application involved in the automation process.

The Ubility SDK simplify and abstract away this complexity by providing a unified interface for interacting with various applications. With the Ubility SDK, you can focus on defining your automation logic without the need to delve into the complexity of each application’s API.

For example, let’s consider the scenario of opening a ticket in salesforce. Traditionally, you would need to study the salesforce API documentation, understand the authentication process, and write the necessary code to open a ticket: 

# Salesforce open ticket code:
```python
def salesforce_create_case(domain, token, params):
    try:
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Case"
        if "type" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)
```

However, with the Ubility SDK, you can achieve the same functionality with a much simpler approach:

# Salesforce open ticket function from Ubility SDK:

```python
SALESFORCE_CREDENTIAL_1 = 'salesForcecred2'
SALESFORCE_OPERATION_1 = 'Create Case'
SALESFORCE_JSON_1 = {'type': 'Problem'}
SALESFORCE_OUTPUT_1 = 'Salesforce0'

Salesforce0 = salesforce_create_case(parseDynamicVars(SALESFORCE_CREDENTIAL_1, globalList), parseDynamicVars(SALESFORCE_JSON_1, globalList))
Output['Salesforce0'] = Salesforce0
```
The Ubility SDK simplifies automation by providing pre-built functions and methods for each application. It takes care of the underlying technical complexities, saving you time and effort. You can concentrate on the core logic of your workflows without delving in the implementation details.

Choose the Ubility SDK to simplify your automation development process, increase productivity, and accelerate the implementation of your automation solutions.

# Installation

You can install the Ubility python SDK from our GitHub page: 

https://github.com/Ubility-SDK


# Docstring Link

You can check the Ubility Docstring by clicking on this link:

https://docstring.ubilityai.com/


# Stories And Templates Link
https://documentation.ubilityai.com/




# Ubility AI Orchestrator

Ubility AI Orchestrator is a powerful no-code orchestrator that is built on top of the Ubility SDK and Langchain. It empowers you to build and orchestrate LLM (Large Language Model) apps and workflow automations.

LLM apps are applications that leverage the capabilities of large language models, such as GPT-3.5, to perform various tasks. However, building LLM apps involves more than just the language models themselves. You also need to connect these apps to your enterprise applications, retrieve data from them, and perform actions through agents.

This is where Ubility Orchestrator comes into play. By combining the power of Langchain and the open-source Ubility SDK, Ubility Orchestrator simplifies the process of connecting LLM apps to your enterprise applications and orchestrating complex workflows.

At Ubility, we strongly believe in working together and empowering developers like you. Our goal is to encourage collaboration and provide you with the tools and resources needed to make the most out of Ubility Orchestrator. We want to support you in enhancing the capabilities of our orchestrator, helping you create amazing applications and workflows.


