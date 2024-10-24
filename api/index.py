from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery
from azure.core.credentials import AzureKeyCredential
import openai

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.post("/api/py/chatComplete")
async def chatComplete(req: Request):
    body = await req.json()
    messages = list(body["messages"])
    print(messages)
    load_dotenv()

    search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"])
    #index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    index_name = "vector-1728792603465"

    azure_search_admin_key = os.environ["AZURE_SEARCH_ADMIN_KEY"]
    openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    #azure_api_key = os.environ["AZURE_API_KEY"]
    chat_deployment_id = os.environ["AZURE_OPENAI_DEPLOYMENT_ID"]
    # messages = [
    #     {"role": "system", "content": "You are a medical professional. Response should be for a specific disease."}, 
    #     #{"role": "user", "content": "What are Cobb syndrome symptoms? Provide result in a list."}]
    #     #{"role": "user", "content": "What is Serpinginous tubular signal void structure?"}]
    #     #{"role": "user", "content": "What legions can you find on someone with Cobb Syndrome?"}]
    #     #{"role": "user", "content": "What is Hereditary multiple exostoses?"}]
    #     {"role": "user", "content": question}]


    azure_openai_key = os.environ["AZURE_OPENAI_KEY"]

    client = openai.AzureOpenAI(azure_endpoint=openai_endpoint, api_version='2024-02-01', api_key=azure_openai_key)

    events = client.chat.completions.create(
        messages=messages,
        model = chat_deployment_id,
        max_tokens=2000,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": index_name,
                        "authentication": {
                            "type": "api_key",
                            "key": azure_search_admin_key
                        }
                    }
                }
            ]
        }

    )
    answer = events.choices[0].message.content
    context = events.choices[0].message.context
    for index, citation in enumerate(context["citations"]):
        print(f"url {index}: {citation["url"]}")
        print(f"filepath {index}: {citation["filepath"]}")
        print(f"title {index}: {citation["title"]}")
        #append title to answer
        answer += '<br/>' + citation['title']
    #print(events)
    # for choice in events.choices:
    #     print(choice)
    #     print("\n\n")
    #print(choice.message.content)
    #{ role: "assistant", content: assistantMessage }
    resp = { "role": "assistant", "content": answer }

    return JSONResponse(content=resp)