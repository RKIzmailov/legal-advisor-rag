import os
from dotenv import load_dotenv
import re

import weaviate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from transformers import BertTokenizer

from utils.yaml_util import load_config

load_dotenv()
API_KEY = os.getenv("Weaviate_API_KEY")
weaviate_url = os.getenv("Weaviate_URL")

config = load_config()
Org =  config['Weaviate']['ORG']
documents_file_path = config['Documents_path']


def download_embed_model():
    embed_model_name = config.get('Embedding_model', 'sentence-transformers/distiluse-base-multilingual-cased-v2')

    if "sentence-transformers" not in embed_model_name:
        print(f"Warning: The model {embed_model_name} is not a sentence-transformer model. Switching to a default.")
        embed_model_name = 'sentence-transformers/distiluse-base-multilingual-cased-v2'

    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)

    Settings.embed_model = embed_model

    print(f"Using embedding model: {embed_model_name}")


def clear_weaviate():
    def get_weaviate_client(api_key, url):
        return weaviate.Client(
                url=url,
                auth_client_secret=weaviate.AuthApiKey(api_key=api_key)
            )

    # client
    client = get_weaviate_client(API_KEY, weaviate_url)

    print(f"Client exists: {client.is_ready()}")

    # DELETING all info from DB
    client.schema.delete_class(Org)


def upload_docs_to_weaviate():
    def load_documents(file_path):
        return SimpleDirectoryReader(file_path).load_data()

    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')


    def count_tokens(text):
        """Counting the number of tokens in a text"""
        tokens = tokenizer.tokenize(text)
        return len(tokens)


    def split_large_text(text, max_tokens=4000):
        """Split the text into fragments no larger than max_tokens"""
        words = text.split()
        split_texts = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if count_tokens(' '.join(current_chunk)) >= max_tokens:
                split_texts.append(' '.join(current_chunk))
                current_chunk = []

        if current_chunk:
            split_texts.append(' '.join(current_chunk))

        return split_texts


    def split_text_by_paragraphs(text, max_tokens=4000):
        """Splitting text into paragraphs of no more than max_tokens"""
        paragraphs = text.split('\n\n')
        new_nodes = []
        current_text = ""

        for para in paragraphs:
            if count_tokens(current_text + para) < max_tokens:
                current_text += para + "\n\n"
            else:
                if current_text:
                    new_nodes.append(current_text.strip())
                current_text = para + "\n\n"

        if current_text.strip():
            new_nodes.append(current_text.strip())

        final_nodes = []
        for node in new_nodes:
            if count_tokens(node) > max_tokens:
                split_nodes = split_large_text(node, max_tokens)
                final_nodes.extend(split_nodes)
            else:
                final_nodes.append(node)

        return final_nodes


    def create_nodes(documents, max_tokens=4000):
        all_nodes = []
        for doc in documents:
            law_name = doc.metadata['file_name'].replace('.txt', '')
            law_text = doc.text
            nodes_list = re.split(r'\n(?=Статья \d+\.)', law_text.strip())
            
            for node_text in nodes_list:
                if count_tokens(node_text) <= max_tokens:
                    all_nodes.append(Document(text=node_text, metadata={'file_name': law_name}))
                else:
                    split_nodes = split_text_by_paragraphs(node_text, max_tokens=4000)
                    for split_node in split_nodes:
                        all_nodes.append(Document(text=split_node, metadata={'file_name': law_name}))

        return all_nodes


    def connect_index(weaviate_client):
        vector_store = WeaviateVectorStore(
            weaviate_client=weaviate_client,
            index_name=Org
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex([], storage_context=storage_context)
        return index


    def insert_nodes_index(index, nodes):
        index.insert_nodes(nodes)


    client = weaviate.connect_to_wcs(
                cluster_url=weaviate_url,
                auth_credentials=weaviate.AuthApiKey(api_key=API_KEY)
    )
    print("Weaviate client is ready:", client.is_ready())

    documents = load_documents(documents_file_path)
    nodes = create_nodes(documents)

    index = connect_index(weaviate_client=client)
    insert_nodes_index(index, nodes=nodes)

    client.close()
    print("Weaviate client connection closed.")
    

if __name__ == "__main__":
    print("Initializing database...")

    print("Download embedding model...")
    download_embed_model()
    print("Embedding model downloaded.")

    print("Clearance of Weaviate DB...")
    clear_weaviate()
    print(f"All info from Weaviate DB: {Org} deleted.")

    print("Uploading docs to Weaviate DB...")
    upload_docs_to_weaviate()
    print("Weaviate initialization and docs uploading completed successfully!")
