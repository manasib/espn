import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend import app, conversation_search, get_chat_engine

client = TestClient(app)


class TestBackend(unittest.TestCase):

    @patch("backend.get_chat_engine")
    def test_query_endpoint_success(self, mock_chat_engine):
        mock_response = MagicMock()
        mock_response.response = "This is a test response"
        mock_response.source_nodes = [
            MagicMock(node=MagicMock(metadata={"link": "http://example.com"}))
        ]
        mock_chat_engine.return_value.chat.return_value = mock_response

        response = client.get("/query", params={"query": "test query"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "answer": "This is a test response",
                "document_links": ["http://example.com"],
            },
        )

    @patch("backend.get_chat_engine")
    def test_query_endpoint_failure(self, mock_chat_engine):
        mock_chat_engine.return_value.chat.side_effect = Exception("Test exception")

        response = client.get("/query", params={"query": "test query"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Test exception"})

    @patch("backend.get_chat_engine")
    def test_reset_conversation_success(self, mock_chat_engine):
        response = client.post("/reset")
        self.assertEqual(response.status_code, 200)

    @patch("backend.get_chat_engine")
    def test_reset_conversation_failure(self, mock_chat_engine):
        mock_chat_engine.return_value.reset.side_effect = Exception("Test exception")

        response = client.post("/reset")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Test exception"})

    @patch("backend.get_chat_engine")
    def test_conversation_search_success(self, mock_chat_engine):
        mock_response = MagicMock()
        mock_response.response = "This is a test response"
        mock_response.source_nodes = [
            MagicMock(node=MagicMock(metadata={"link": "http://example.com"}))
        ]
        mock_chat_engine.return_value.chat.return_value = mock_response

        response, links = conversation_search("test query")
        self.assertEqual(response, "This is a test response")
        self.assertEqual(links, ["http://example.com"])

    @patch("backend.get_chat_engine")
    def test_conversation_search_failure(self, mock_chat_engine):
        mock_chat_engine.return_value.chat.side_effect = Exception("Test exception")

        with self.assertRaises(Exception) as context:
            conversation_search("test query")
        self.assertTrue("Test exception" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
