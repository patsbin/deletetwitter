from datetime import date
from dateutil.relativedelta import relativedelta
import logging
import tweepy
import twitterconfig as tc
import got

logging.basicConfig(filename='deleteTwitter.log', format='%(asctime)s %(message)s', level=logging.INFO)
logging.info('Started')

auth = tweepy.OAuthHandler(tc.CONFIG['consumer_key'], tc.CONFIG['consumer_secret'])
auth.set_access_token(tc.CONFIG['access_key'], tc.CONFIG['access_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)
logging.info('Authenticated as: %s', api.me().screen_name)

delete_count = 0
max_tweets = 500
until_date = date.today() - relativedelta(months=+6)

tweetCriteria = got.manager.TweetCriteria().setUsername("patsbin").setUntil(str(until_date)).setMaxTweets(max_tweets)
logging.info('Getting max. %s Tweets up until %s', max_tweets, str(until_date))

# whitelist
save_ids = []

for i in range(len(got.manager.TweetManager.getTweets(tweetCriteria))):
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)[i]

    # Whitelist
    if tweet.id in save_ids:
        # print('Tweet on whitelist')
        continue

    # Save my own pictures that are not retweets
    urls = ['twitpic', 'photo']
    if any(url in tweet.text for url in urls):
        # print('photo string found')
        continue

    try:
        single_one = api.get_status(tweet.id)
        # has a retweet or fav or media, save
        if single_one.retweet_count > 0:
            # print(tweet.id, ' more retweets: ', single_one.retweet_count)
            continue
        elif single_one.favorite_count > 5:
            # print(tweet.id, ' more favs: ', single_one.favorite_count)
            continue
        elif 'media' in single_one.entities:
            # print(tweet.id, ' has media:', single_one.entities)
            continue
        else:
            try:
                api.destroy_status(tweet.id)
                logging.info("Tweet ", tweet.id, " deleted:", tweet.text)
                delete_count +=1
            except:
                logging.info("Tweet ", tweet.id, " could not be deleted:", tweet.text)
    except:
        logging.info('id not found. Already deleted?')


logging.info('Finished')
