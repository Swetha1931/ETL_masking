import pytest
import json
from app.sqs import read_messages_from_sqs
from app.postgres import insert_to_postgres
from app.mask_pii import mask_pii
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_sqs_response():
    # Mock SQS response with a single message
    return {
        "Messages": [
            {
                "Body": json.dumps({"key": "value"}),
                "ReceiptHandle": "test_receipt_handle"
            }
        ]
    }


# Test reading messages from SQS
def test_read_messages_from_sqs(mock_sqs_response):
    with patch("app.sqs.sqs") as mock_sqs:
        mock_sqs.receive_message.return_value = mock_sqs_response
        mock_sqs.delete_message.return_value = None

        messages = read_messages_from_sqs()
        # Assert that the function returns a list with one message
        assert len(messages) == 1
        # Assert that the message body is a JSON object with the expected key-value pair
        assert json.loads(messages[0]["Body"]) == {"key": "value"}


# Test inserting records into Postgres
def test_insert_to_postgres():
    records = [
        ("user_id_1", "device_type_1", "masked_ip_1",
         "masked_device_id_1", "locale_1", 1, "2022-01-01"),
        ("user_id_2", "device_type_2", "masked_ip_2",
         "masked_device_id_2", "locale_2", 2, "2022-01-02")
    ]

    with patch("app.postgres.psycopg2") as mock_psycopg2:
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        # Set up the mock connection and cursor
        mock_psycopg2.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        insert_to_postgres(records)

        # Assert that the connection and cursor were created correctly
        mock_psycopg2.connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cur.executemany.assert_called_once_with("""
                INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, records)
        # Assert that the connection was committed
        mock_conn.commit.assert_called_once()


# Test masking PII data using SHA-256
def test_mask_pii_sha256():
    input_data = "example_data"
    expected_output = "ae1d31f8c0bc324ebf384c447d5c1b89be9b9a9e5d507a17e50f2a1e779ca24d"

    # Check that the mask_pii function returns the expected output
    assert mask_pii(input_data) == expected_output


# Test masking PII data with an invalid method
def test_mask_pii_invalid_method():
    # Assert that the mask_pii function raises a ValueError when given an unsupported method
    with pytest.raises(ValueError):
        mask_pii("example_data", method="unsupported_method")