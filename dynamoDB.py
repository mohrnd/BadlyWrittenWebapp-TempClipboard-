import boto3
import time
import config  # Import the config module

# Load configurations from config.py
region = config.REGION
dynamodb_name = config.DYNAMODB_NAME

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table(dynamodb_name)

def write_to_dynamodb(code, userid, content, ttl_seconds=7200):
    """
    Writes an item to the DynamoDB table.

    Parameters:
        code (str): The unique code for the content.
        userid (int): The ID of the user sharing the content.
        content (str): The content to be shared.
        ttl_seconds (int): The time-to-live in seconds (default is 2 hours).
    """
    ttl = int(time.time()) + ttl_seconds  # Calculate TTL as current time + ttl_seconds

    # Write the item to the DynamoDB table
    table.put_item(
        Item={
            'Code': code,        # Use capitalized 'Code' as the primary key
            'userid': userid,
            'content': content,
            'ttl': ttl
        }
    )
    print(f"Successfully wrote item with code '{code}' to the table.")

def read_from_dynamodb(code):
    """
    Reads an item from the DynamoDB table using the code.

    Parameters:
        code (str): The unique code to search for.

    Returns:
        dict: The retrieved item, or None if not found or expired.
    """
    response = table.get_item(Key={'Code': code})

    # Check if the item exists in the response
    if 'Item' in response:
        item = response['Item']

        # Check if the TTL has expired
        current_time = int(time.time())
        if item['ttl'] < current_time:
            print(f"The content with code '{code}' has expired.")
            return None

        print(f"Successfully retrieved item: {item}")
        return item
    else:
        print(f"No item found with code '{code}'.")
        return None
