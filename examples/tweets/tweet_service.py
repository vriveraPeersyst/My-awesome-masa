import json
import logging
import os
import time
from datetime import datetime

def setup_logging(log_level, log_format):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(level=numeric_level, format=log_format)

def ensure_data_directory(directory):
    os.makedirs(directory, exist_ok=True)

def save_tweet_response(response_data, current_date, data_directory):
    filename = f'{data_directory}/tweet_response_{current_date.strftime("%Y-%m-%d")}_{int(time.time())}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(response_data, file, ensure_ascii=False, indent=2)
    logging.info(f"Tweet response saved to {filename}")

def create_tweet_query(hashtag, start_date, end_date):
    return f"({hashtag} until:{end_date.strftime('%Y-%m-%d')} since:{start_date.strftime('%Y-%m-%d')})"