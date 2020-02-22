# Twitter to Video

### [Part1](https://github.com/BUEC500C1/video-noracnr/tree/master/part1)
Please see Part1 package with seperate README.md.

### Main Exercise(Summerizor.py)
Using the twitter feed, construct a daily video summarizing a twitter handle day
* Convert text into an image in a frame 
* Do a sequence of all texts and images in chronological order.
* Display each video frame for 3 seconds

### Guide
This application requires python3, Twython, FFmpeg. 
Make sure prepare your own twitter api keys, then put them a file named 'keys' without any extention in root program directory.Here is the format of api keys:
```
[auth]
consumer_key = ****
consumer_secret = ****
access_token = ****
access_secret = ****
```
To run this program, run summarizer.py for single thread, and run queue_system.py for Queue with multi-threading.
```bash
python3 summarizer.py
python3 queue_system.py
```
##### Customize
You can generate your own object in summarizer.py. For example, if you want to generate a video called "news.mp4" about Breaking News, you can use in this way:
```python3
# parameter1: search keyword of twitter 
# parameter2: expected video name
# parameter3: your keys file[ Default Name]

customizedObject = Summarizer("Breaking","news","keys")
```

##### Result
Check img and news.mp4.
Here is the result of queue_system.py
![video](img/screenshot_video.png)
![images](img/screenshot_imgs.png)

### Answers of tasks
* How many API calls you can handle simultaneously and why?

I only call Twitter API for this time. I have one worker with 10 threads using api simultaneously in queue_system.py.

* For example, run different API calls at the same time?

Yes.

* Split the processing of an API into multiple threads?

I can split a process into multiple threads using threading library, but in summarizer.py , I only use one thread for creating images and video after geting callback from twitter api. In queue_system.py, I use 10 threads for calling api synchronously.




