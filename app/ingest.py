import weaviate
from weaviate.auth import AuthApiKey
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from openai import OpenAI
from anthropic import Anthropic

import os
from dotenv import load_dotenv

from utils.yaml_util import load_config

load_dotenv()
API_KEY = os.getenv("Weaviate_API_KEY_READ")
weaviate_url = os.getenv("Weaviate_URL")

config = load_config()
Org =  config['Weaviate']['ORG']


def connect_index(weaviate_client):
    vector_store = WeaviateVectorStore(
        weaviate_client=weaviate_client,
        index_name=Org
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)
    return index


def load_weaviate():
    weaviate_client = weaviate.connect_to_wcs(
        cluster_url=weaviate_url,
        auth_credentials=AuthApiKey(api_key=API_KEY)
        )
    print("Weaviate client connected:", weaviate_client.is_ready(), end = ' | ')
    # try:
    index = connect_index(weaviate_client=weaviate_client)
    return index
    # finally:
    #     weaviate_client.close()
    #     print("Weaviate client connection closed.")


def initialize_llm_client(model_name = "gpt-4o-mini"):
    """
    Initialize the appropriate LLM client based on the model name.
    The function pulls the API key from environment variables based on the model.
    
    Args:
        model_name (str): Name of the LLM model ("gpt-4o-mini" or "claude-3-sonnet-20240229").
    
    Returns:
        llm_client: The initialized client for the specified model.

    Raises:
        ValueError: If the API key is missing or the model name is not recognized.
    """

    if model_name == "gpt-4o-mini":
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("Missing OpenAI API key.")
        llm_client = OpenAI(api_key=openai_api_key)

    elif model_name == "claude-3-sonnet-20240229":
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not anthropic_api_key:
            raise ValueError("Missing Anthropic API key.")
        llm_client = Anthropic(api_key=anthropic_api_key)

    else:
        raise ValueError(f"LLM client error: '{model_name}' is not recognized.")

    return llm_client