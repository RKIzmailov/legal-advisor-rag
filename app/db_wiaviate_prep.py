import weaviate
from weaviate.auth import AuthApiKey
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from transformers import BertTokenizer
import os
from dotenv import load_dotenv
import re

from utils.yaml_util import load_config
from utils.weaviate_client import download_embed_model, close_weaviate_client

load_dotenv()
API_KEY = os.getenv("Weaviate_API_KEY")
weaviate_url = os.getenv("Weaviate_URL")

config = load_config()
Org =  config['Weaviate']['ORG']
documents_file_path = config['Documents_path']
# documents_file_path = r'D:\Rustem\2_Education\7_Data_science\4_DS_Projects_for_GH\7-legal-advisor-rag\data\laws'


def clear_weaviate():
    def get_weaviate_client(api_key, url):
        return weaviate.Client(
                url=url,
                auth_client_secret=weaviate.AuthApiKey(api_key=api_key)
            )


    weaviate_client = get_weaviate_client(API_KEY, weaviate_url)
    print(f"Client exists: {weaviate_client.is_ready()}")

    # DELETING all info from DB
    weaviate_client.schema.delete_class(Org)


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
    print("*** Weaviate client is ready:", client.is_ready())

    documents = load_documents(documents_file_path)
    print('*** The following documents uploaded:')
    for doc in documents:
        print('\t\t-', doc.metadata['file_name'].replace('.txt', ''))

    print('*** Creating nodes...')
    nodes = create_nodes(documents)
    print('*** Creating nodes compleated.')

    print('*** Inserting indexes to Weaviate...')
    index = connect_index(weaviate_client=client)
    insert_nodes_index(index, nodes=nodes)
    print('*** Inserting indexes to Weaviate compleated.')

    client.close()
    print("***Weaviate client connection closed.")
    

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
    print(f"Weaviate initialization and docs uploading completed successfully. Weaviate DB name: {Org}")