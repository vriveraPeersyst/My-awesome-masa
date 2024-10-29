# import json

# def load_and_process_tweets(file_path):
#     with open(file_path, 'r') as file:
#         tweet_data = json.load(file)
    
#     processed_tweets = []
#     for tweet_entry in tweet_data:
#         if tweet_entry['Error'] is None and 'Tweet' in tweet_entry:
#             tweet = tweet_entry['Tweet']
#             # Annotate tweet text with the username to indicate the author explicitly.
#             tweet_text = f"[Author: {tweet['Username']}] {tweet['Text']}"
#             processed_tweets.append(tweet_text)
    
#     return processed_tweets



import json
import logging

# src/agent/data/tweet_preprocessor.py

def load_and_process_tweets(file_path):
    with open(file_path, 'r') as file:
        tweet_data = json.load(file)
    
    processed_tweets = []
    for tweet_entry in tweet_data:
        if tweet_entry['Error'] is None and 'Tweet' in tweet_entry:
            tweet = tweet_entry['Tweet']
            # Annotate tweet text with the username to indicate the author explicitly.
            tweet_text = f"[Author: {tweet['Username']}] {tweet['Text']}"
            processed_tweets.append(tweet_text)
    
    return processed_tweets


def process_tweets(tweet_data):
    processed_tweets = []
    for tweet_entry in tweet_data:
        if tweet_entry['Error'] is None and 'Tweet' in tweet_entry:
            tweet = tweet_entry['Tweet']
            # Annotate tweet text with the username to indicate the author explicitly.
            tweet_text = f"[Author: {tweet['Username']}] {tweet['Text']}"
            processed_tweets.append(tweet_text)
    
    return processed_tweets

def process_matches(match_data):
    processed_matches = []
    
    # Loop through each matchday and match
    for matchday, matches in match_data.items():
        for match in matches:
            area = match['area']['name']
            competition = match['competition']['name']
            season_start = match['season']['startDate']
            season_end = match['season']['endDate']
            match_date = match['utcDate']
            status = match['status']
            matchday_number = match['matchday']
            stage = match['stage']
            last_updated = match['lastUpdated']
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']
            half_time_home = match['score']['halfTime']['home']
            half_time_away = match['score']['halfTime']['away']
            winner = match['score']['winner']
            duration = match['score']['duration']
            
            # Check for odds message if available
            odds_msg = match['odds']['msg'] if 'odds' in match else "No odds available"
            
            # Referee information
            referees = ', '.join([ref['name'] for ref in match['referees']]) if match['referees'] else "No referees"

            # Format the result
            match_info = (f"Matchday {matchday_number}, {stage}, {competition}, {area}\n"
                          f"Date: {match_date} | Status: {status} | Last updated: {last_updated}\n"
                          f"Season: {season_start} - {season_end}\n"
                          f"{home_team} {home_score} - {away_score} {away_team}\n"
                          f"Half-time score: {home_team} {half_time_home} - {half_time_away} {away_team}\n"
                          f"Winner: {winner} | Duration: {duration}\n"
                          f"Referees: {referees}\n"
                          f"Odds: {odds_msg}\n")
            
            processed_matches.append(match_info)
    
    return processed_matches

