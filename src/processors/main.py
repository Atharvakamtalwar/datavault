import json
import boto3
import os
import pandas as pd
from typing import Dict, List
from datetime import datetime

s3_client = boto3.client('s3')
kinesis_client = boto3.client('kinesis')

def validate_record(record: Dict) -> bool:
    """Validate if all required fields are present and have correct data types."""
    required_fields = ['id', 'timestamp', 'amount', 'customer_id']
    
    try:
        # Check if all required fields exist
        if not all(field in record for field in required_fields):
            return False
        
        # Validate data types
        if not isinstance(record['id'], str):
            return False
        if not isinstance(record['amount'], (int, float)):
            return False
        if not isinstance(record['customer_id'], str):
            return False
        
        # Validate timestamp format
        datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
        
        return True
    except (ValueError, AttributeError):
        return False

def enrich_record(record: Dict) -> Dict:
    """Enrich the record with additional metadata."""
    # Add processing timestamp
    record['processed_at'] = datetime.utcnow().isoformat()
    
    # Add data source identifier
    record['source'] = 'raw_data_bucket'
    
    # Add processing version
    record['version'] = '1.0'
    
    return record

def process_records(records: List[Dict]) -> List[Dict]:
    """Process a batch of records."""
    processed_records = []
    
    for record in records:
        if validate_record(record):
            enriched_record = enrich_record(record)
            processed_records.append(enriched_record)
    
    return processed_records

def save_to_s3(records: List[Dict], bucket: str, key: str):
    """Save processed records to S3."""
    df = pd.DataFrame(records)
    csv_buffer = df.to_csv(index=False).encode()
    
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=csv_buffer
    )

def handler(event, context):
    """Main Lambda handler function."""
    processed_bucket = os.environ['PROCESSED_BUCKET']
    
    try:
        # Process records from the event
        records = [json.loads(record['kinesis']['data']) for record in event['Records']]
        processed_records = process_records(records)
        
        if processed_records:
            # Generate a unique key for the processed file
            timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
            key = f'processed/data-{timestamp}.csv'
            
            # Save processed records to S3
            save_to_s3(processed_records, processed_bucket, key)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Successfully processed records',
                    'processed_count': len(processed_records),
                    'output_location': f's3://{processed_bucket}/{key}'
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No valid records to process',
                    'processed_count': 0
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing records',
                'error': str(e)
            })
        }
