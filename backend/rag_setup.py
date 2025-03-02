import chromadb
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma.base import ChromaVectorStore

import config as config
from setup_logger import logging


# super simple setup for for chromadb with a local directory as the storage
class RagSetup:

    def __init__(self):
        llm = Ollama(
            model=config.LLM_MODEL,
            host=config.LLM_HOST,
            port=config.LLM_PORT,
            timeout=config.LLM_TIMEOUT,
            temperature=0,
        )
        Settings.llm = llm
        embedding_model = HuggingFaceEmbedding(
            model_name=config.EMBEDDING_MODEL)
        Settings.embed_model = embedding_model
        self.index = self.setupVectorIndex()

    def setupVectorIndex(self):
        db = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
        chroma_collection = db.get_collection(config.COLLECTION_NAME)
        embeddings_count = chroma_collection.count()
        logging.info(
            f"Total embeddings loaded in collection: {embeddings_count}")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        return VectorStoreIndex.from_vector_store(vector_store=vector_store)
