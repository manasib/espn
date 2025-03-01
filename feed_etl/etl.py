import sys
from datetime import datetime, timezone
from time import mktime

import chromadb
import feedparser
from llama_index.core import (Document,
                              Settings,
                              StorageContext)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma.base import ChromaVectorStore

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma.base import ChromaVectorStore

import config as config
from setup_logger import logger


class ETLProcessor:

    def __init__(self,
                 rss_urls,
                 db_path="./../chroma_db",
                 collection_name="espn"):
        self.rss_urls = rss_urls
        self.db_path = db_path
        self.collection_name = collection_name
        self.documents = {}

        self.db = None
        self.chroma_collection = None
        self.vector_store = None
        self.storage_context = None
        self.llm = Ollama(
            model=config.LLM_MODEL,
            host=config.LLM_HOST,
            port=config.LLM_PORT,
            timeout=config.LLM_TIMEOUT,
            temperature=0,
        )
        Settings.llm = self.llm
        self.embeddings_model = HuggingFaceEmbedding(
            model_name=config.EMBEDDING_MODEL)
        Settings.embed_model = self.embeddings_model

    def feed_metadata_data_about_feed(self, count):
        document = Document(
                    text=config.METADATA_DOC["text"].format(number_of_feeds=str(count)), 
                    doc_id=config.METADATA_DOC["id"], 
                    metadata={
                    "title": config.METADATA_DOC["title"],
                    "published": int(datetime.now().now().timestamp()),
                    "author": config.METADATA_DOC["author"],
                    "entry_id": config.METADATA_DOC["id"],
                    "link": config.METADATA_DOC["link"],
                    })
        return document
    def setup_db(self):
        logger.info("Setting up Chroma-db")
        self.db = chromadb.PersistentClient(path=self.db_path)
        self.chroma_collection = self.db.get_or_create_collection(
            self.collection_name)
        initial_count = self.chroma_collection.count()
        logger.info(
            f"START: Initial Chroma collection has {initial_count} vectors. Each vector represents one page of a rss feed.")

        self.vector_store = ChromaVectorStore(
            chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        logger.info("Chroma-db setup complete")

    def read_feed(self):

        if not self.rss_urls:
            logger.error("No RSS URLs provided. Existing application. Sad!")
            raise ValueError("No RSS URLs provided. Sad!")

        logger.info(f"Reading {len(self.rss_urls)} feeds")
        for url in self.rss_urls:
            feed = feedparser.parse(url)
            if feed.bozo == 1:
                logger.error("Error parsing feed: ", feed.bozo_exception)
                sys.exit(1)

            logger.info(
                f"Reading feed Title: {feed.feed.title}, feed has {len(feed.entries)} entries"
            )
            for entry in feed.entries:
                text = entry.description + " link: " + entry.link
                doc_id = entry.id
                author = getattr(
                    entry, "author", "NO-AUTHOR"
                )  # author is an optional attribute - weird but true
                published = datetime.fromtimestamp(
                    mktime(entry.published_parsed), timezone.utc
                )
                metadata = {
                    "title": entry.title,
                    "published": int(published.timestamp()),
                    "author": author,
                    "entry_id": entry.id,
                    "link": entry.link,
                }
                document = Document(
                    text=text, doc_id=doc_id, metadata=metadata)
                # storing the document with doc_id as key, as there are same documents included in multiple feeds.
                self.documents[doc_id] = document
                logger.info(f"Added document with ID: {doc_id}")
        
    def document_upsert(self):
        original_count = self.chroma_collection.count()
        logger.info(f"{original_count} embeddings exist")
        logger.info("Creating Index")
        self.chroma_collection.upsert(
            ids=[doc.doc_id for doc in self.documents.values()],
            documents=[doc.text for doc in self.documents.values()],
            metadatas=[doc.metadata for doc in self.documents.values()],
        )
        logger.info("Done creating Index")
        new_count = self.chroma_collection.count()
        document = self.feed_metadata_data_about_feed(new_count)
        self.chroma_collection.upsert(
            ids=[document.doc_id],
            documents=[document.text],
            metadatas=[document.metadata],
        )
        logger.info(f"{new_count-original_count} embedding(s) upserted")


if __name__ == "__main__":
    embed_model = HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL)
    Settings.embed_model = embed_model
    try:
        etl_processor = ETLProcessor(
            rss_urls=config.ESPN_FEEDS,
            db_path=config.CHROMA_DB_DIR,
            collection_name=config.COLLECTION_NAME,
        )
        etl_processor.setup_db()
        etl_processor.read_feed()
        etl_processor.document_upsert()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
