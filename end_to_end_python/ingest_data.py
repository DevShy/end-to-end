import snscrape.modules.twitter as sntwitter
import pandas as pd
from sqlalchemy import create_engine
import argparse
import re


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    query = params.query

    def clean_tweet(tweets_text):
        clean_text = re.sub(r"RT+", "", tweets_text)
        clean_text = re.sub(r"@\S+", "", clean_text)
        clean_text = re.sub(r"https?\S+", "", clean_text)
        clean_text = clean_text.replace("\n", " ")

        return clean_text

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    limit = 5000
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        tweet.content = clean_tweet(tweet.content)
        if len(tweets) == limit:
            break
        if (
            tweet.user.username == "vemsercadmus"
            or tweet.user.username == "GoVulpi"
            or tweet.user.username == "FabrciaDiniz"
        ):
            continue
        else:
            tweets.append(
                [
                    tweet.date,
                    tweet.user.username,
                    tweet.content,
                    tweet.url,
                ]
            )

    df = pd.DataFrame(tweets, columns=["date", "user", "content", "url"])
    df.to_csv("tweets.csv", index=False)
    df.to_sql(table_name, con=engine, if_exists="append")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest data from Twitter")
    parser.add_argument("--user", type=str, help="User name for postgres")
    parser.add_argument("--password", type=str, help="Password for postgres")
    parser.add_argument("--host", type=str, help="Host for postgres")
    parser.add_argument("--port", type=str, help="Port for postgres")
    parser.add_argument("--db", type=str, help="Database name for postgres")
    parser.add_argument("--table_name", type=str, help="Table name for postgres")
    parser.add_argument("--query", type=str, help="Query for twitter")

    args = parser.parse_args()

    main(args)
