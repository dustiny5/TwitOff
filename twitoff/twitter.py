# Retrieve tweets, embeddings, and persist in the database
import tweepy
import basilica
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))

# Connect to API
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

# Class

def add_or_update_user(username):
    """Add or update user and their tweets, else error if not a Twitter user"""
    try:
        twitter_user = TWITTER.get_user(username)
        # Get existing user or make a new user.
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        # Add to the database
        DB.session.add(db_user)
        # Want as many recent non-retweet/reply statuses
        tweets = twitter_user.timeline(
            count=250, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id
        )
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # Grab our embedding from basilica
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], 
                             embedding=embedding)
            # Append db_tweet to db_user.tweets(empty list NOT in database)
            db_user.tweets.append(db_tweet)
            # Add the db_tweet to database
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        # Error message will show on the site
        raise e
    else:
        DB.session.commit()



















