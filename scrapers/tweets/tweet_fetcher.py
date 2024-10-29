import requests
import os
import yaml
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import logging
import json
from tweet_service import setup_logging, ensure_data_directory, save_all_tweets, create_tweet_query

def load_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'tweet_fetcher_config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_state(state, api_calls_count, records_fetched, all_tweets):
    state_data = {
        'last_known_state': state,
        'api_calls_count': api_calls_count,
        'records_fetched': records_fetched,
        'all_tweets_sample': all_tweets[:7]  # Guarda una muestra de los primeros 10 tweets para visibilidad
    }
    with open('last_known_state_detailed.json', 'w') as f:
        json.dump(state_data, f, indent=4)

def load_state():
    try:
        with open('last_known_state_detailed.json', 'r') as f:
            return json.load(f).get('last_known_state', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def exponential_backoff(attempt, base=60):
    return base * (2 ** attempt)  # Backoff exponencial: retraso base * 2^intento

def fetch_tweets(config):
    start_date = datetime.strptime(config['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(config['end_date'], '%Y-%m-%d').date()
    days_per_iteration = config['days_per_iteration']

    # Lista de cuentas de Twitter de los equipos de La Liga 2024-2025
    accounts = [
        'Alaves',
        'Atleti',
        'Osasuna',
        'FCBarcelona',
        'GironaFC',
        'Osasuna',
        'RCCelta',
        'RCD_Mallorca',
        'realmadrid',
        'realvalladolid',
        'UDLP_Oficial',
        'VillarrealCF',
        'AthleticClub',
        'Cadiz_CF',
        'CDLeganes',
        'GetafeCF',
        'GranadaCF',
        'RayoVallecano',
        'RCDEspanyol',
        'RealBetis',
        'RealSociedad',
        'SevillaFC',
        'valenciacf'
    ]

    for account in accounts:
        logging.info(f"Fetching tweets for account: {account}")
        current_date = end_date

        # Crear un directorio de datos para cada cuenta
        account_data_directory = os.path.join(config['data_directory'], account)
        ensure_data_directory(account_data_directory)

        api_calls_count = 0
        records_fetched = 0
        all_tweets = []

        while current_date >= start_date:
            success = False
            attempts = 0

            while not success and attempts < config['max_retries']:
                iteration_start_date = current_date - timedelta(days=days_per_iteration)
                day_before = max(iteration_start_date, start_date - timedelta(days=1))

                # Crear el query para la cuenta actual
                query = create_tweet_query(account, day_before, current_date)
                print(query)
                request_body = {"query": query, "count": config['tweets_per_request']}

                try:
                    response = requests.post(
                        config['api_endpoint'],
                        json=request_body,
                        headers=config['headers'],
                        timeout=config['request_timeout']
                    )
                    api_calls_count += 1

                    if response.status_code == 200:
                        response_data = response.json()
                        if response_data and 'data' in response_data and response_data['data'] is not None:
                            tweets = response_data['data']
                            all_tweets.extend(tweets)
                            num_tweets = len(tweets)
                            records_fetched += num_tweets
                            logging.info(f"Fetched {num_tweets} tweets for {account} from {day_before} to {current_date}.")
                            success = True
                        else:
                            logging.warning(f"No tweets fetched for {account} from {day_before} to {current_date}. Retrying after delay...")
                            time.sleep(config['request_delay'])
                            attempts += 1
                    elif response.status_code == 429 or response.status_code == 500:
                        if response.status_code == 429:
                            logging.warning("Rate-limited. Retrying after delay...")
                            time.sleep(exponential_backoff(attempts, base=config['retry_delay']))
                            attempts += 1
                        elif response.status_code == 500:
                            logging.warning("500 Error. Retrying after delay...")
                            time.sleep(exponential_backoff(attempts, base=config['request_delay']))
                            attempts += 1
                    else:
                        logging.error(f"Failed to fetch tweets: {response.status_code}")
                        break

                except requests.exceptions.RequestException as e:
                    logging.error(f"Request failed: {e}")
                    time.sleep(exponential_backoff(attempts, base=config['retry_delay']))
                    attempts += 1

            if not success:
                logging.error(f"Failed after {attempts} attempts for {account} from {day_before} to {current_date}")

            # Guardar el estado si es necesario
            save_state({'current_date': current_date.strftime('%Y-%m-%d'), 'account': account}, api_calls_count, records_fetched, all_tweets)
            current_date -= timedelta(days=days_per_iteration)
            time.sleep(config['request_delay'])

        # Guardar todos los tweets de la cuenta actual
        save_all_tweets(all_tweets, account_data_directory, f"from:{account}")

        logging.info(f"Finished fetching tweets for account: {account}. Total API calls: {api_calls_count}. Total records fetched: {records_fetched}")

if __name__ == "__main__":
    load_dotenv()
    config = load_config()
    setup_logging(config['log_level'], config['log_format'])
    fetch_tweets(config)