import unittest

from src.chat.main import _normalize_messages


class ChatMainTests(unittest.TestCase):
    def test_normalize_messages_keeps_history_order(self):
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]

        result = _normalize_messages(history)

        self.assertEqual(result, [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ])

    def test_normalize_messages_accepts_single_prompt(self):
        result = _normalize_messages("What is AI?")

        self.assertEqual(result, [{"role": "user", "content": "What is AI?"}])


if __name__ == "__main__":
    unittest.main()
