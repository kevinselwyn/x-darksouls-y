#!/usr/bin/env python
# coding=utf-8
# pylint: disable=C0103,C0301,R0201,R0902,R0913,W0110
"""
X is the Dark Souls of Y

Usage: python x-darksouls-y.py --consumer-key "<consumer_key>"
                               --consumer-secret "<consumer_secret>"
                               --access-token-key "<access_token_key>"
                               --access-token-secret "<access_token_secret>"
                               [--pattern "<pattern>"]
                               [--search "<search_term>"]
"""

import argparse
import math
import os
import random
import re
import string
import urllib
import twitter

class DarkSouls(object):
    """DarkSouls"""

    # TWITTER VARS

    api = None
    consumer_key = None
    consumer_secret = None
    access_token_key = None
    access_token_secret = None

    # PATTERN

    pattern = 'is the Dark Souls of'

    # SEARCH VARS

    search_term = 'is harder than'
    search_count = 100
    search_query = ''

    # BAD FILTERS

    bad_hashtags = [
        'repost'
    ]

    bad_followups = [
        'I ',
        'ever',
        'it looks',
        'it sounds',
        'it seems',
        'it should be',
        'usual',
        'anticipated',
        'you might',
        'you think',
        'you thought',
        'you\'d'
    ]

    # CONSTRUCTOR

    def __init__(self, consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None, pattern=None, search_term=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

        if pattern:
            self.pattern = pattern

        if search_term:
            self.search_term = search_term

        self.search_query = 'q=%%22%s%%22&count=%d' % (urllib.parse.quote_plus(self.search_term), self.search_count)

    # UTILS

    def dedupe(self, seq):
        """Dedupe lists"""

        seen = set()
        seen_add = seen.add

        return [x for x in seq if not (x in seen or seen_add(x))]

    # TWEET CLEANING

    def remove_chars(self, tweet=''):
        """Remove chars"""

        printable = set(string.printable)
        tweet = ''.join(list(filter(lambda x: x in printable, tweet)))
        tweet = tweet.replace('&amp;', '&')

        return tweet

    def remove_urls(self, tweet=''):
        """Remove urls"""

        return re.sub(r'http\S+', '', tweet)

    def remove_handles(self, tweet=''):
        """Remove handles"""

        return ' '.join(re.sub(r'(@[A-Za-z0-9_]+)', ' ', tweet).split())

    def remove_rt(self, tweet=''):
        """Remove RT"""

        return tweet.replace('RT', '')

    def remove_hashtags(self, tweet=''):
        """Remove hashtags"""

        for hashtag in self.bad_hashtags:
            tweet = re.sub('#%s' % (hashtag), '', tweet, flags=re.IGNORECASE)

        return tweet

    def remove_at(self, text=''):
        """Remove at"""

        return re.sub(r'^@\s+', '', text)

    def clean_tweet(self, tweet=''):
        """Clean tweet"""

        tweet = self.remove_chars(tweet)
        tweet = self.remove_urls(tweet)
        tweet = self.remove_handles(tweet)
        tweet = self.remove_rt(tweet)
        tweet = self.remove_hashtags(tweet)

        return tweet.strip()

    # CONNECT

    def get_api(self):
        """Get API"""

        api_opts = {
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'access_token_key': self.access_token_key,
            'access_token_secret': self.access_token_secret
        }

        if not self.api:
            self.api = twitter.Api(**api_opts)

        return self.api

    # SEARCH

    def get_search(self):
        """Search"""

        results = []

        try:
            api = self.get_api()
            results = api.GetSearch(raw_query=self.search_query)
        except twitter.error.TwitterError:
            print('Could not reach Twitter at this time. Please try again later.')
            results = []

        return results

    # PARSER

    def parse_followups(self, y=''):
        """Parse followups"""

        for followup in self.bad_followups:
            if re.match(followup, y, re.IGNORECASE):
                return False

        parts = y.split(' ')

        if len(parts) >= 1:
            if parts[0].lower() == 'you':
                return False

        if len(parts) >= 2:
            if parts[1].lower() == 'think':
                return False

        return True

    def parse_tweet(self, tweet=''):
        """Parse tweet"""

        tweet = self.clean_tweet(tweet)
        empty = ['', '']

        parts = tweet.split(self.search_term)

        if len(parts) != 2:
            return empty

        split_on = r'[:;\.,]'

        before_parts = re.split(split_on, parts[0])
        after_parts = re.split(split_on, parts[1])

        if not before_parts or not after_parts:
            return empty

        x = (before_parts[-1:][0]).strip()
        y = (after_parts[:1][0]).strip()

        x = self.remove_at(x)

        if not self.parse_followups(y):
            return empty

        return [x, y]

    # TWEETS

    def post_tweet(self, message=''):
        """Post tweet"""

        api = self.get_api()

        return api.PostUpdate(message)

    def get_tweets(self):
        """Get tweets"""

        total = 3000
        api = self.get_api()
        max_id = 0
        tweets = []

        for _i in range(0, int(math.ceil(total / 200))):
            results = api.GetUserTimeline(count=200, max_id=max_id, include_rts=True)

            if not results:
                break

            for result in results:
                tweets.append(result.text)
                max_id = result.id

        tweets = self.dedupe(tweets)

        return tweets

    def generate_tweets(self):
        """Generate tweets"""

        tweets = []
        results = self.get_search()

        if not results:
            return tweets

        for result in results:
            x, y = self.parse_tweet(result.text)

            if not x or not y:
                continue

            x = x.capitalize()

            tweets.append('%s %s %s' % (x, self.pattern, y))

        tweets = self.dedupe(tweets)

        return tweets

def run(args):
    """Run"""

    opts = {
        'consumer_key': os.getenv('CONSUMER_KEY', args.consumer_key),
        'consumer_secret': os.getenv('CONSUMER_SECRET', args.consumer_secret),
        'access_token_key': os.getenv('ACCESS_TOKEN_KEY', args.access_token_key),
        'access_token_secret': os.getenv('ACCESS_TOKEN_SECRET', args.access_token_secret),
        'pattern': args.pattern,
        'search_term': args.search_term
    }

    dark_souls = DarkSouls(**opts)
    new_tweets = dark_souls.generate_tweets()
    old_tweets = dark_souls.get_tweets()

    new_tweet = None

    rand_order = [x for x in range(0, len(new_tweets))]
    random.shuffle(rand_order)

    for rand in rand_order:
        new_tweet = new_tweets[rand]

        if new_tweet not in old_tweets:
            break

    if not new_tweet:
        print('No new unique Tweet could be generated')
        return

    print('Tweeting: %s' % (new_tweet))
    print(dark_souls.post_tweet(new_tweet))

def main():
    """Main function"""

    parser = argparse.ArgumentParser()

    parser.add_argument('--consumer-key', type=str, dest='consumer_key', default=None, required=(False if os.getenv('CONSUMER_KEY', None) else True))
    parser.add_argument('--consumer-secret', type=str, dest='consumer_secret', default=None, required=(False if os.getenv('CONSUMER_SECRET', None) else True))
    parser.add_argument('--access-token-key', type=str, dest='access_token_key', default=None, required=(False if os.getenv('ACCESS_TOKEN_KEY', None) else True))
    parser.add_argument('--access-token-secret', type=str, dest='access_token_secret', default=None, required=(False if os.getenv('ACCESS_TOKEN_SECRET', None) else True))
    parser.add_argument('--pattern', type=str, dest='pattern', default=None, required=False)
    parser.add_argument('--search', type=str, dest='search_term', default=None, required=False)

    args = parser.parse_args()

    run(args)

if __name__ == '__main__':
    main()
