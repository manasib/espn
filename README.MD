# ESPN Feed search

# This repository has 3 independent components
1. Feed_ETL - Feed_etl reads the RSS feed URLs from configuration file and creats embeddings from them and saves those embeddings to local chroma_db. 
Each RSS URL is read and a text embedding is created and associated with metadata related to the feed like author, date, the url etc.

Why did I choose chroma_db? 
1. Easy local setup.
2. chroma db allows time based filtering based on metadata. 
3. works great with llama_index chat_engine. 

2. Backend
This is a fastAPI based rest api setup. This service provides the backend for the streamlit app. 


3. Streamlit app
UI for sending search queries to the backend apis. 
reset button resets the conversation and removes the conversation history context.


# External dependencies
I was asked to create a project which could be run completely locally. 
I have used ollama to serve the LLMs. You just need to install ollama.
you can download ollama from here https://ollama.com/download
once you download, you will need to pull llama3.2:1b model with the following command
`ollama pull llama3.2:1b`

llama3.2:1b is the smallest model from meta and works great locally. It;s just 1.3GB.


# How to run this project? 
run   `make all` 
this should run the etl, to create the local chromadb, run the backend server and open the streamlit ui.


# how to run unit tests 
run   `make all-unittest` 

# what could be done better?
UI
1. Better UI
2. Save and reload conversation
3. Reset conversation

GenAI
1. Saving conversations
2. Multi-modal embeddings and response, currently it's text only
3. Giving a personality to the bot
4. So much could be done with the data itself, Ideally, I could parse the articles and ingest those in the embeddings, ingest text as well as image data. 
5. Streaming output
6. When feeding the embeddings to the DB, I am calculating the embeddings and then upserting them and kind of relying on the database to tell me if there is a need for any update or now. While that would work amazing for a dataset that is changing a lot, it kind of feels lazy for a dataset that does not change as much like this ESPN rss feed. For this sort of data source, may be it's better if I get the exisiting indexes and cross compare that with the feed data ids and only upsert the newer data by article published date. 

DevOps
1. Separate configs for DEV, TEST, STG and PROD
2. Better support for docker containers e.g. with docker compose

MLOPs
MLFlow would be super helpful to tune the prompt and embeddings. 









