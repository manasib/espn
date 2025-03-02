ESPN_FEEDS = [
    "https://www.espn.com/espn/rss/news",
    "https://www.espn.com/espn/rss/nfl/news",
    "https://www.espn.com/espn/rss/nba/news",
    "https://www.espn.com/espn/rss/wnba/news",
    "https://www.espn.com/espn/rss/nhl/news",
    "https://www.espn.com/espn/rss/mlb/news",
    "https://www.espn.com/espn/rss/soccer/news",
    "https://www.espn.com/espn/rss/golf/news",
    "https://www.espn.com/espn/rss/poker/news",
    "https://www.espn.com/espn/rss/rpm/news",
    "https://www.espn.com/espn/rss/tennis/news",
    "https://www.espn.com/espn/rss/boxing/news",
    "https://www.espn.com/espn/rss/espnu/news",
    "https://www.espn.com/espn/rss/ncb/news",
    "https://www.espn.com/espn/rss/ncf/news",
    "https://www.espn.com/espn/rss/ncaa/news",
    "https://www.espn.com/espn/rss/oly/news",
    "https://www.espn.com/espn/rss/horse/news",
    "https://www.espn.com/blog/feed?blog=sec",
    "https://www.espn.com/blog/feed?blog=acc",
    "https://www.espn.com/blog/feed?blog=big12",
    "https://www.espn.com/blog/feed?blog=bigeast",
    "https://www.espn.com/blog/feed?blog=bigten",
    "https://www.espn.com/blog/feed?blog=pac12",
    "https://www.espn.com/blog/feed?blog=ncfnation",
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
    "link": "https://www.espn.com/espn/rss/news",
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

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"
