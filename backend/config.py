
CHROMA_DB_DIR = "./../chroma_db"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "espn"

LLM_MODEL = "llama3.2:1b"
LLM_HOST = "localhost"
LLM_PORT = 11434
CHAT_MODE = "condense_plus_context"
LLM_TIMEOUT = 120
CONTEXT_PROMPT_TEMPLATE = """You are a Americal sports league expert,
you are able to have normal interactions and you can discuss
about American sports leagues news in details.
Here are the relevant documents for the context:\n {context_str}
\nInstruction: Use the previous chat history, or the context above,
to interact and help the user."""
