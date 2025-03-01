import time
from functools import cache
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.query_engine import CitationQueryEngine

from pydantic import BaseModel

from rag_setup import RagSetup
from setup_logger import logger
import config as config


async def lifespan(app: FastAPI):
    on_startup()
    yield
    on_shutdown()


app = FastAPI(lifespan=lifespan)


# this is the heaviest operation to initialize the LLM and vector index.
# so we cache it.
@cache
def get_chat_engine() -> BaseChatEngine:
    rag = RagSetup()
    index = rag.index
    chat_engine = index.as_chat_engine(
        chat_mode=config.CHAT_MODE,
        context_prompt=(config.CONTEXT_PROMPT_TEMPLATE or None),
        verbose=True,
    )
    return chat_engine

# calculate the time spent on the request and log it.
@app.middleware("http")
async def add_process_time_logging(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("request complete in {%.2f}s" % (process_time))
    return response


def conversation_search(query):
    resp = get_chat_engine().chat(query)
    print(resp)
    links = []
    for nodes in resp.source_nodes:
        links.append(nodes.node.metadata["link"])
    return resp.response, links


class QueryResponse(BaseModel):
    answer: str
    document_links: List[str]


@app.get("/query", response_model=QueryResponse)
async def query_endpoint(query: str):
    try:
        answer, document_links = conversation_search(query)
        return QueryResponse(answer=answer, document_links=document_links)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# I had grand plans! 
# @app.post("/new_conversation")
# async def new_conversation():
#     try:
#         chat_store.persist(persist_path="chat_store.json")
#         chat_engine.reset()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# I had grand plans! 
@app.post("/reset")
async def reset_conversation():
    try:
        get_chat_engine().reset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def on_startup():
    # this is to initialize the vector index befor the first request arrives.
    logger.info("Application starting up. Initializing the RAG stack")
    get_chat_engine()
    logger.info(
        "Application startup complete. Rag stack initialization complete.")


def on_shutdown():
    pass


if __name__ == "__main__":

    # timeout is high as ollama and local chroma db take a while to do
    # anything.
    uvicorn.run(app, host="0.0.0.0", port=8080, timeout_keep_alive=30)
