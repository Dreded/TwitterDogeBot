import tweepy
import re
from credentials import keys


class Bot:
    def __init__(self):
        self._consumer_key = keys[0]
        self._consumer_secret = keys[1]
        self._access_token = keys[2]
        self._access_secret = keys[3]
        self.last_match = 0
        self.match_list = []

        try:
            auth = tweepy.OAuthHandler(self._consumer_key,
                                       self._consumer_secret)
            auth.set_access_token(self._access_token, self._access_secret)
            self.client = tweepy.API(auth)
            if not self.client.verify_credentials():
                raise tweepy.TweepError
        except tweepy.TweepError as e:
            print('ERROR : connection failed. Check your OAuth keys.')
        else:
            print('Connected as @{}, you can start to tweet !'.format(self.client.me().screen_name))
            self.client_id = self.client.me().id

    def is_word_in_text(self, word, text):
        """
        Check if a word is in a text. Ignores case but word must be standalone so "buy doge" would work but "buy dogecoin" would not.
        """
        pattern = r'(^|[^\w]){}([^\w]|$)'.format(word)
        pattern = re.compile(pattern, re.IGNORECASE)
        matches = re.search(pattern, text)
        return bool(matches)

    def is_sequence_in_text(self, sequence, text):
        """
        Check if a sequence is in text. Ignores case.
        """
        pattern = r'{}'.format(sequence)
        pattern = re.compile(pattern, re.IGNORECASE)
        matches = re.search(pattern, text)
        return bool(matches)
    
    def add_to_matches(self,id):
        #requires a reverse list to work properly
        self.match_list.append(id)
        if len(self.match_list) > 5:
            self.match_list.popleft()

    def get_botuser_last_tweet(self):
        tweet = self.client.user_timeline(id = self.client_id, count = 1)[0]
        print(tweet.text)

    def get_user_tweets(self, userID):
        tweets = self.client.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           exclude_replies=True,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )

    def get_user_last_tweet(self, userID):
        tweet = self.client.user_timeline(screen_name=userID, 
                           count=1,
                           include_rts = False,
                           exclude_replies=True,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
        try:
            if self.last_match == 0:
                self.last_match = tweet[0].id
                return "First Run so not matching... {}".format(tweet[0].full_text)
            elif self.last_match >= tweet[0].id:
                #used greater than so if tweets are deleted they dont get matched
                return "Tweet has not changed."
            else:
                self.last_match = tweet[0].id
                return tweet[0]
        except:
            return False