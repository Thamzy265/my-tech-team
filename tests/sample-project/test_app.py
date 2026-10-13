import json
import threading
import unittest
import urllib.request

import app


class NotesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = app.make_server(port=0)
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_notes_starts_empty(self):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/notes", timeout=5) as r:
            self.assertEqual(json.load(r), [])


if __name__ == "__main__":
    unittest.main()
