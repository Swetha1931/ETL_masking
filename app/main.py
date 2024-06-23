
import json  
from dataclasses import dataclass
from app.config import POSTGRES_CONNECTION  
from app.postgres import insert_to_postgres  
from app.sqs import read_messages_from_sqs  
from app.mask_pii import mask_pii_data  

@dataclass
class Record:
    """
    A data class to represent a record with masked PII data.
    """
    user_id: str
    device_type: str
    masked_ip: str
    masked_device_id: str
    locale: str
    app_version: int
    create_date: str


# function to process messages from SQS
def process_messages(messages):
    return [Record(**mask_pii_data(json.loads(message["Body"]))) for message in messages]


def main():
    messages = read_messages_from_sqs()
    # Process the messages by masking PII data
    records = process_messages(messages)
    # Insert the records into PostgreSQL
    insert_to_postgres(POSTGRES_CONNECTION, records)

if __name__ == "__main__":
    main()