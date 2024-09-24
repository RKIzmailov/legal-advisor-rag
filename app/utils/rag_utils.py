from yandexfreetranslate import YandexFreeTranslate

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from utils.yaml_util import load_config

config = load_config()
Org =  config['Weaviate']['ORG']
documents_file_path = config['Documents_path']

yt = YandexFreeTranslate(api='ios')

def ru(txt):
  return yt.translate("en", "ru", txt)

def en(txt):
  return yt.translate("ru", "en", txt)


def download_embed_model():
    embed_model_name = config.get('Embedding_model', 'sentence-transformers/distiluse-base-multilingual-cased-v2')

    if "sentence-transformers" not in embed_model_name:
        print(f"Warning: The model {embed_model_name} is not a sentence-transformer model. Switching to a default.")
        embed_model_name = 'sentence-transformers/distiluse-base-multilingual-cased-v2'

    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)

    Settings.embed_model = embed_model

    print(f"Using embedding model: {embed_model_name}")