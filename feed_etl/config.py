ESPN_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://www.espn.com/espn/rss/nfl/news",
    "https://www.espn.com/espn/rss/nba/news",
    "https://www.espn.com/espn/rss/wnba/news",
    "https://www.espn.com/espn/rss/nhl/news",
    "https://www.espn.com/espn/rss/soccer/news",
    "https://www.espn.com/espn/rss/golf/news",
    "https://www.espn.com/espn/rss/poker/news",
    "https://www.espn.com/espn/rss/rpm/news",
    "https://www.espn.com/espn/rss/tennis/news",
    "https://www.espn.com/espn/rss/boxing/news",
    "https://www.espn.com/blog/feed?blog=sec"
]

METADATA_DOC = {
    "id": "FIXED_ID_FOR_METADATA",
    # definitely an opportunity to extract this from ESPN_FEEDS
    "text": "I have read feeds about NFL, NBA, WNBA, NHL, Soccer, Golf, Poker, Autos, Tennis, Boxing, and SEC.\
    I have read {number_of_feeds} feeds.",
    "title": "Ingested feeds",
    "published": 1234567890,
    "author": "Manasi",
    "entry_id": "Test Entry ID",
    "link": "https://www.espn.com/espn/rss/news"
}



CHROMA_DB_DIR = "./../chroma_db"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "espn"

LLM_MODEL = "llama3.2:1b"
LLM_HOST = "localhost"
LLM_PORT = 11434
LLM_TIMEOUT = 120
# run every 4 hours
ETL_DATA_UPDATE_SCHEDULE = "0 */4 * * *"
