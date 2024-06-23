from app.config import SQS_QUEUE_URL  
from botocore.exceptions import ClientError  
import boto3  
import os  

sqs = boto3.client("sqs", endpoint_url=SQS_QUEUE_URL, region_name="localhost")

def read_messages_from_sqs(max_messages: int = 10) -> list:
    
    messages = []  
    try:
        # Call the receive_message method of the SQS client to retrieve messages
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,  
            MaxNumberOfMessages=max_messages  
        )

        if "Messages" in response:
            messages = response["Messages"]  

    except ClientError as e:
        print(f"Error reading messages from SQS: {e}")

    return messages  # Return the list of messages