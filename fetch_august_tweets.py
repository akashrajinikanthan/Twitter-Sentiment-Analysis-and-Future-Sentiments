import tweepy
import csv
import os
from datetime import datetime, timedelta

# 🔑 Set your Bearer Token here
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEiq3wEAAAAAWyLcgHL6gRl4d8PZJ654sKIUx70%3DtI2xjUOcNYwo5igQnHKnxgr2Xe5r1U2zNppmRfhCnONmmHRBrm"

# Authenticate
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

def fetch_50_tweets(query, filename="fifty_tweets.csv"):
    """
    Fetch exactly 50 tweets for a given query and save to CSV.
    """
    print(f"Fetching 50 tweets for query: {query}")

    response = client.search_recent_tweets(
        query=query,
        tweet_fields=["id", "text", "created_at"],
        max_results=50
    )

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "tweet"])  # header

        if response.data:
            for tweet in response.data:
                writer.writerow([tweet.id, tweet.text])

    print(f"✅ 50 tweets saved to {filename}")


if __name__ == "__main__":
    fetch_50_tweets("AI langchain", filename="fifty_tweets.csv")

