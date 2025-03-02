import unittest
import uuid
import xml.sax
from datetime import datetime
from time import mktime
from unittest.mock import MagicMock, patch

from llama_index.core import Settings

from etl import ETLProcessor


class TestETLProcessor(unittest.TestCase):

    def setUp(self):
        self.rss_urls = ["http://example.com/feed"]
        self.etl_processor = ETLProcessor(self.rss_urls)

    def test_initialization(self):
        self.assertEqual(self.etl_processor.rss_urls, self.rss_urls)
        self.assertEqual(self.etl_processor.db_path, "./../chroma_db")
        self.assertEqual(self.etl_processor.collection_name, "espn")
        self.assertEqual(self.etl_processor.documents, {})
        self.assertIsNone(self.etl_processor.db)
        self.assertIsNone(self.etl_processor.chroma_collection)
        self.assertIsNone(self.etl_processor.vector_store)
        self.assertIsNone(self.etl_processor.storage_context)

    @patch("etl.logger")
    @patch("etl.chromadb.PersistentClient")
    def test_setup_db_initial_count(self, mock_persistent_client, mock_logger):
        mock_db = MagicMock()
        mock_persistent_client.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.get_or_create_collection.return_value = mock_collection
        mock_collection.count.return_value = 5

        self.etl_processor.setup_db()

        mock_logger.info.assert_any_call("Setting up Chroma-db")
        mock_logger.info.assert_any_call("Chroma-db setup complete")
        mock_logger.info.assert_any_call(
            "START: Initial Chroma collection has 5 vectors. Each vector represents one page of a rss feed."
        )
        self.assertEqual(self.etl_processor.db, mock_db)
        self.assertEqual(self.etl_processor.chroma_collection, mock_collection)

    @patch("etl.logger")
    def test_read_feed_no_rss_urls(self, mock_logger):
        self.etl_processor.rss_urls = []

        with self.assertRaises(ValueError):
            self.etl_processor.read_feed()

        mock_logger.error.assert_called_with(
            "No RSS URLs provided. Existing application. Sad!"
        )

    @patch("etl.logger")
    @patch("etl.feedparser.parse")
    def test_read_feed_bozo_exception(self, mock_feedparser, mock_logger):
        mock_feed = MagicMock()
        mock_feed.bozo = 1
        mock_feed.bozo_exception = Exception("Test Exception")
        mock_feedparser.return_value = mock_feed

        self.etl_processor.read_feed()

        mock_logger.error.assert_called_with(
            f"Error parsing feed: {self.rss_urls[0]} {mock_feed.bozo_exception}"
        )

    @patch("etl.logger")
    @patch("etl.feedparser.parse")
    def test_read_feed_success(self, mock_feedparser, mock_logger):
        mock_feed = MagicMock()
        mock_feed.bozo = 0
        mock_feed.feed.title = "Test Feed"
        mock_feed.entries = [
            MagicMock(
                description="Test Description",
                link="http://example.com/entry1",
                title="Test Entry 1",
                published_parsed=datetime.now().timetuple(),
                id="entry1",
            )
        ]
        mock_feedparser.return_value = mock_feed

        self.etl_processor.read_feed()

        self.assertEqual(len(self.etl_processor.documents), 1)
        document = self.etl_processor.documents["entry1"]
        self.assertEqual(document.doc_id, "entry1")
        self.assertEqual(document.metadata["title"], "Test Entry 1")
        mock_logger.info.assert_any_call(
            f"Reading feed Title: {mock_feed.feed.title}, feed has {len(mock_feed.entries)} entries"
        )
        mock_logger.info.assert_any_call(f"Added document with ID: entry1")

    @patch("etl.logger")
    @patch("etl.chromadb.PersistentClient")
    def test_document_upsert_success(self, mock_persistent_client, mock_logger):
        mock_db = MagicMock()
        mock_persistent_client.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.get_or_create_collection.return_value = mock_collection
        mock_collection.count.side_effect = [0, 1]

        doc_uid = str(uuid.uuid4())
        self.etl_processor.documents = {
            doc_uid: MagicMock(
                doc_id=doc_uid, metadata={"link": "link"}, text="Test Text"
            )
        }
        self.etl_processor.storage_context = MagicMock()
        self.etl_processor.chroma_collection = mock_collection

        self.etl_processor.document_upsert()

        mock_logger.info.assert_any_call("0 embeddings exist")
        mock_logger.info.assert_any_call("Creating Index")
        mock_logger.info.assert_any_call("Done creating Index")
        mock_logger.info.assert_any_call("1 embedding(s) upserted")
        self.assertEqual(mock_collection.count.call_count, 2)
