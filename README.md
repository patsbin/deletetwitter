# deletetwitter
python script to delete selected tweets based on your twitter archive
Script based on this work: https://pushpullfork.com/i-deleted-tweets/

You need your tweet archive and a registered twitter app (https://apps.twitter.com/)
The script uses tweepy to access your twitter feed and cvs to read your archive file. Install both plugins using pip:
pip install tweepy cvs

The cronjob-script uses GetOldTweets-python (https://github.com/Jefferson-Henrique/GetOldTweets-python).

Full requirements:
pip install tweepy cvs python-dateutil pyquery

Rename twitterconfig.sample.py to twitterconfig.py and add your twitter app account
Place your tweets.cvs in the same folder as the deletetwitter.py script and twitterconfig.py file
