from llama_index.core.retrievers import VectorIndexRetriever
from ingest import initialize_llm_client
from utils.yaml_util import load_config
from utils.rag_utils import ru

config = load_config()
Org = config['Weaviate']['ORG']
language = config['Language']

model_name = config['RAG_model']['model_name']
llm_client = initialize_llm_client(model_name)
print(f"Successfully initialized {model_name} LLM client.")


def search_nodes(query, retriever):
    return retriever.retrieve(query)


def build_prompt(query, search_results):
    nodes_with_scores = [(node, node.score) for node in search_results]
    sorted_nodes = sorted(nodes_with_scores, key=lambda x: x[1], reverse=True)
    sorted_nodes_only = [node for node, score in sorted_nodes]

    context = ""
    
    for node in sorted_nodes_only:
        context += node.metadata['file_name'].replace('txt', '') + '\n' + node.text + "\n\n"

    prompt_template = config['RAG_model']['prompt_template']
    prompt = prompt_template.format(language=language, question=query, context=context).strip()
    return prompt


def llm_response(prompt):
    response = llm_client.chat.completions.create(
        model=config['RAG_model']['model_name'],
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query, index):
    if language == "English":
        query = ru(query)

    retriever = VectorIndexRetriever(
        index,
        vector_store_query_mode="hybrid",
        similarity_top_k=config['Retriever']['similarity_top_k'],
        alpha=config['Retriever']['alpha'],
        similarity_threshold=config['Retriever']['similarity_threshold'],
    )
    
    search_results = search_nodes(query, retriever)
    prompt = build_prompt(query, search_results)
    answer = llm_response(prompt)

    answer_data = {
        "answer": answer,
    }
    return answer_data