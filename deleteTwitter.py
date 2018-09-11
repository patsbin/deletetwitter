import tweepy
import csv
import twitterconfig as tc


def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)


auth = tweepy.OAuthHandler(tc.CONFIG['consumer_key'], tc.CONFIG['consumer_secret'])
auth.set_access_token(tc.CONFIG['access_key'], tc.CONFIG['access_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)
print("Authenticated as: %s" % api.me().screen_name)


def read_csv(file):
    """
    reads a CSV file into a list of lists
    """
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rows = []
        for line in reader:
            row_data = []
            for element in line:
                row_data.append(element)
            if row_data != []:
                rows.append(row_data)
    rows.pop(0)
    return(rows)


tweets = read_csv('./tweets.csv')
tweets_marked = []

"""
HASHTAGS

hashtag = '#hashtag'
for tweet in tweets:
    if hashtag in tweet[5]:
        tweets_marked.append(tweet)
"""

"""
RETWEETS

for tweet in tweets:
    if tweet[5][0:3] == 'RT ':
        tweets_marked.append(tweet)
"""

"""
TIMING for year

year_list = ['2009','2010']
for tweet in tweets:
    if tweet[3][0:4] in year_list:
    tweets_marked.append(tweet)
"""


# year_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
year_list = ['2018']
month_list = ['2018-01', '2018-02', '2018-03', '2018-04']

for tweet in tweets:
    if tweet[3][0:4] in year_list:
        # if tweet[5][0:3] == 'RT ':
            tweets_marked.append(tweet)
    elif tweet[3][0:7] in month_list:
        tweets_marked.append(tweet)

print(len(tweets_marked), ' tweets marked for deletion.')


# Save some tweets
to_delete_ids = []
delete_count = 0
for tweet in tweets_marked:
    to_delete_ids.append(tweet[0])

    # Don't save retweets
    if tweet[6] != '':
        print('This is a retweet - Delete!')
        continue

    # Save my own pictures that are not retweets (tweet[6])
    urls = ['twitpic', 'photo']
    for url in urls:
        if (tweet[9].find(url) >= 0) and (tweet[6] == ''):
            to_delete_ids.pop()
            print('string found: ', tweet[9])
        continue

    # Some to save and not delete
    # single_one = api.get_status('1019514746347900928')
    try:
        single_one = api.get_status(tweet[0])
        # has a retweet or fav or media, save
        if single_one.retweet_count > 0:
            print(single_one.text, ' more retweets: ', single_one.retweet_count)
            to_delete_ids.pop()
#        elif single_one.favorite_count > 0:
#            print(single_one.text, ' more favs: ', single_one.favorite_count)
#            to_delete_ids.pop()
        elif 'media' in single_one.entities:
            print(single_one.text, ' has media:', single_one.entities)
            to_delete_ids.pop()
        else:
            try:
                api.destroy_status(tweet[0])
                print(tweet[0], ' deleted!')
                delete_count +=1
            except:
                print(tweet[0], ' could not be deleted.')
    except:
        print('id not found. Already deleted?')

# Delete remaining retweets etc
for status_id in to_delete_ids:
    try:
        api.destroy_status(status_id)
        print(status_id, 'deleted!')
        delete_count +=1
    except:
        print(status_id, 'could not be deleted.')

print(delete_count, 'tweets deleted.')
