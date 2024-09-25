from llama_index.core.retrievers import VectorIndexRetriever
import ingest

from utils.yaml_util import load_config
from utils.rag_utils import ru
from utils.weaviate_client import initialize_weaviate_client 

config = load_config()
Org = config['Weaviate']['ORG']
language = config['Language']

model_name = config['RAG_model']['model_name']
llm_client = ingest.initialize_llm_client(model_name)
print(f"Successfully initialized {model_name} LLM client.")

weaviate_client = initialize_weaviate_client()
index = ingest.connect_index(weaviate_client = weaviate_client)
print(f"Successfully weaviate index loaded.")

retriever = VectorIndexRetriever(
    index,
    vector_store_query_mode="hybrid",
    similarity_top_k = config['Retriever']['similarity_top_k'],
    alpha = config['Retriever']['alpha'],
    similarity_threshold = config['Retriever']['similarity_threshold'],
    )


def search_nodes(query, retriever):
    return retriever.retrieve(query)


def build_prompt(query, search_results):
    nodes_with_scores = [(node, node.score) for node in search_results]
    sorted_nodes = sorted(nodes_with_scores, key=lambda x: x[1], reverse=True)
    sorted_nodes_only = [node for node, score in sorted_nodes]

    context = ""
    
    for nod in sorted_nodes_only:
        context = context + nod.metadata['file_name'].replace('txt', '') + '\n' + nod.text + "\n\n"

    prompt_template = config['RAG_model']['prompt_template']
    prompt = prompt_template.format(language = language, question=query, context=context).strip()
    return prompt

def llm_response(prompt):
    response = llm_client.chat.completions.create(
        model=config['RAG_model']['model_name'],
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query):
    query = ru(query)
    search_results = search_nodes(query, retriever)
    prompt = build_prompt(query, search_results)
    answer = llm_response(prompt)

    answer_data = {
        "answer": answer,
    }
    return answer_data

# print(rag('What evidence is required for a person to be formally charged as an accused?'))