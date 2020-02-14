import time
import re
import os
import subprocess
# Import the twython library for Twitter APIs
from twython import Twython
from twython import TwythonError


COUNT = 100

class Summarizor():
  def __init__(self, keyword="", videoName="", consumer_key="", consumer_secret="", access_token="", access_token_secret=""):
    self.keyword = keyword
    self.Name = videoName
    self.twitter_list = []
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.access_token = access_token
    self.access_token_secret = access_token_secret

  def filter(self, text):
    """filter the tweet text to spam and pass ffmpeg compile"""
    #text = re.sub('RT \@+\w+\:','',text) #delete head of retweet
    # text = re.sub('\#+\w+\s','',text)     #delete hashtag
    text = re.sub('https://t.co/+\w+.','',text)  #delete url
    #text = re.sub('\@+\w+(\\n|\s)','',text)    #delete @people  
    text = re.sub('\n','',text)                #delete \n
    text = re.sub('…','',text)
    text = re.sub("'",'',text)
    text = re.sub('"','\\"',text)
    text = re.sub("‘",'\'',text)
    text = re.sub("’",'\'',text)
    text = re.sub("#",r'\#',text)
    text = re.sub(",",r'\,',text)
    text = re.sub(":",r'\:',text)
    text = re.sub(r'https\://t','',text)  #delete url
    text = re.sub("%",r'\%',text)
    text = re.sub("-",r'\-',text)
    text = re.sub(";",r'\;',text)
    text = re.sub("@",r'\@',text)
    # text = re.sub("?",'\?',text)
    return text


  def search_keyword(self):
    """return a list of tweets"""
    hash_list = []
    # Fill in your keys and tokens
    APP_KEY= self.consumer_key
    APP_SECRET = self.consumer_secret
    OAUTH_TOKEN = self.access_token
    OAUTH_TOKEN_SECRET = self.access_token_secret
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    SUPPORTED_LANGUAGE = ['zh', 'zh-Hant', 'en']
    if len(self.keyword) == 0:
      self.keyword = "coronavirus"
    
    
    try:
      results = twitter.cursor(twitter.search, q=self.keyword, result_type = 'recent'
                  , count = COUNT, include_entities = True)
      MAX_TWEETS = 30
      for idx, status in enumerate(results):  # 'results' is a generator. It yields tweet objects
        if idx < MAX_TWEETS:
          #print(idx)
          gap = '\n'
          content = {}
          content['lang'] = status['lang']
          hashValue = hash(status["text"])  #if texts are identical, hash value is same
          if content['lang'] in SUPPORTED_LANGUAGE:
            if (hashValue not in hash_list) : #or (content["hash"] in twitter_list and content['text'] not in twitter_list)
              hash_list.append(hashValue)
              # content["entities"] = status['entities']
              # content["retweet_count"] = status['retweet_count'] # return int
              # content["favorite_count"] = status['favorite_count'] #return integer or Nullable
              tweet_list = list(self.filter(status['text']))
              for i in range(len(tweet_list)):
                if (i % 50) == 0:
                  tweet_list.insert(i,gap)
              tweetText = ''.join(tweet_list)
              self.twitter_list.append(tweetText)
        else:
          break
    except TwythonError as e:
      if e.error_code == 429:
        print("Too many requests!")
      else:
        print(e.error_code)
    except StopIteration:
      pass

    return self.twitter_list

  def textToImage(self):
    """Convert text into an image in a frame"""
    for idx,text in enumerate(self.twitter_list):
      # print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
      # print(text)
      subprocess.run("ffmpeg -i frame1.jpeg -vf \"drawtext=text=\'{0}\':fontfile=./Lato/Lato-Regular.ttf:fontcolor=white:fontsize=40:x=200:y=250:\" /Users/noracnr/Documents/EC500/video/img/{2}_{1}.jpg".format(text,idx,self.Name),shell=True,check=True)

  def imageToVideo(self):
    """Convert image to video in chronological order, and play each frame for 3s"""
    returnCompletedProcess = subprocess.run(r"ffmpeg -r 0.3 -f image2 -s 1200x630 -i /Users/noracnr/Documents/EC500/video/img/{0}_\%d.jpg -vcodec libx264 -crf 25 -pix_fmt yuv420p {0}.mp4".format(self.Name), shell=True, check=True)
    return returnCompletedProcess.returncode

  def keyToVideo(self):
    """Integrate search_keyword textToImage imageToVideo """
    self.search_keyword()
    self.textToImage()
    return self.imageToVideo()



if __name__ == '__main__':
  api = Summarizor("","virus","Q99zzkOXcr4rJMLX6apAe9xV1","2tjQeRoJ1KuhWp100khCjcs8yCDOUWcSHJSLkVFEinmYjiPWsz","1172962292217999360-yIBAO1UIPNgSmKlkp0cV9801DsoegI","MKtFv7sgeCsfGch8XYDFPevk46FYiNEYaaGRnH8fdEdWq")
  api.keyToVideo()