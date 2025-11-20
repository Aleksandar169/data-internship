
import os
import json
import unittest
from unittest.mock import patch

os.environ["DYNAMODB_TABLE_NAME"] = "dummy-table"
os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"


from lamdass.lambda_insert_db import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch("lamdass.lambda_insert_db.table")  # mock-ujemo table objekat
    def test_lambda_inserts_item_for_allowed_prefix(self, mock_table):
        # 2. Pripremimo fake SQS event sa S3 rekordom
        event = {
            "Records": [
                {
                    "body": json.dumps({
                        "Records": [
                            {
                                "eventTime": "2025-11-20T10:00:00.000Z",
                                "s3": {
                                    "bucket": {"name": "my-bucket"},
                                    "object": {"key": "pollution/city/file1.json"}
                                }
                            }
                        ]
                    })
                }
            ]
        }

        # 3. Pozovemo lambda_handler
        response = lambda_handler(event, None)

        # 4. Proverimo response
        self.assertEqual(response["statusCode"], 200)

        # 5. Proverimo da je put_item pozvan jednom
        mock_table.put_item.assert_called_once()

        # 6. Proverimo konkretne podatke upisane u Item
        _, kwargs = mock_table.put_item.call_args
        item = kwargs["Item"]
        self.assertEqual(item["file_name"], "pollution/city/file1.json")
        self.assertEqual(item["timestamp"], "2025-11-20T10:00:00.000Z")
        self.assertEqual(item["status"], 0)

    @patch("lamdass.lambda_insert_db.table")
    def test_lambda_ignores_disallowed_prefix(self, mock_table):
        event = {
            "Records": [
                {
                    "body": json.dumps({
                        "Records": [
                            {
                                "eventTime": "2025-11-20T10:00:00.000Z",
                                "s3": {
                                    "bucket": {"name": "my-bucket"},
                                    "object": {"key": "other/something.txt"}
                                }
                            }
                        ]
                    })
                }
            ]
        }

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        # Za zabranjeni prefiks ne sme da pozove put_item
        mock_table.put_item.assert_not_called()


if __name__ == "__main__":
    unittest.main()

