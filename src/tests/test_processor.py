import pytest
import json
from datetime import datetime
from src.processors.main import validate_record, enrich_record, process_records

def test_validate_record_valid():
    record = {
        'id': '123',
        'timestamp': '2023-01-01T12:00:00Z',
        'amount': 100.50,
        'customer_id': 'CUST123'
    }
    assert validate_record(record) == True

def test_validate_record_invalid():
    record = {
        'id': '123',
        'timestamp': 'invalid_date',
        'amount': 100.50,
        'customer_id': 'CUST123'
    }
    assert validate_record(record) == False

def test_enrich_record():
    record = {
        'id': '123',
        'timestamp': '2023-01-01T12:00:00Z',
        'amount': 100.50,
        'customer_id': 'CUST123'
    }
    enriched = enrich_record(record)
    
    assert 'processed_at' in enriched
    assert 'source' in enriched
    assert 'version' in enriched
    assert enriched['source'] == 'raw_data_bucket'
    assert enriched['version'] == '1.0'

def test_process_records():
    records = [
        {
            'id': '123',
            'timestamp': '2023-01-01T12:00:00Z',
            'amount': 100.50,
            'customer_id': 'CUST123'
        },
        {
            'id': '456',
            'timestamp': 'invalid_date',
            'amount': 200.75,
            'customer_id': 'CUST456'
        }
    ]
    
    processed = process_records(records)
    assert len(processed) == 1  # Only one valid record should be processed
    assert processed[0]['id'] == '123'
