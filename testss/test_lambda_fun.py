import lambda_fun
from lambda_fun import lambda_handler
import unittest


class TestLambdaHandler(unittest.TestCase):
    def test_returns_hello_with_name(self):
        event = {"name": "Aleksandar"}
        result = lambda_handler(event, None)
        self.assertEqual(result, "Hello Aleksandar")

    def test_uses_default_when_name_missing(self):
        event = {}
        result = lambda_handler(event, None)
        self.assertEqual(result, "Hello Unknown")


if __name__ == "__main__":
    unittest.main()
