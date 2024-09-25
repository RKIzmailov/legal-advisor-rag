import weaviate
from weaviate.auth import AuthApiKey

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from utils.yaml_util import load_config
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("Weaviate_API_KEY_READ")
weaviate_url = os.getenv("Weaviate_URL")

config = load_config()
Org =  config['Weaviate']['ORG']

# Initialize the Weaviate client globally
weaviate_client = None

def initialize_weaviate_client():
    global weaviate_client
    if weaviate_client is None:
        weaviate_client =  weaviate.connect_to_wcs(
            cluster_url=weaviate_url,
            auth_credentials=AuthApiKey(api_key=API_KEY)
            )
        print("Weaviate client connected:", weaviate_client.is_ready())
        download_embed_model()
    return weaviate_client


def download_embed_model():
    embed_model_name = config.get('Embedding_model', 'sentence-transformers/distiluse-base-multilingual-cased-v2')

    if "sentence-transformers" not in embed_model_name:
        print(f"Warning: The model {embed_model_name} is not a sentence-transformer model. Switching to a default.")
        embed_model_name = 'sentence-transformers/distiluse-base-multilingual-cased-v2'

    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)

    Settings.embed_model = embed_model

    print(f"Using embedding model: {embed_model_name}")


def close_weaviate_client():
    global weaviate_client
    if weaviate_client:
        weaviate_client.close()
        weaviate_client = None
        print("Weaviate client connection closed.")
