# author : noracnr@bu.edu
import queue
import multiprocessing
import time
import threading
from summarizer import Summarizer
from apiKey import consumer_key, consumer_secret, access_token, access_token_secret

num_worker_threads = 10

def source():
  keyName = [
    ["Trump","trump"],
    ["COVID-19","covid"],
    ["Wuhan","wuhan"],
    ["2020","2020"],
    ["Japan","japan"],
    ["Diamond Pricess","cruise"],
    ["Breaking","news"],
    ["Valentine","valentine"],
    ["UEFA","uefa"],
    ["Boston","boston"],
    ["China","china"]
  ]
  source = []
  for key, name in keyName:
    a = [key, name, consumer_key, consumer_secret, access_token, access_token_secret]
    print(a)
    source.append(a)
  return source

def worker():
  i = 0
  while True:
    item = q.get()
    if item is None:
      print("Break ! cuz item is None")
      break
    api = Summarizer(item[0], item[1], item[2], item[3], item[4], item[5])
    api.keyToVideo()
    i += 1
    print("-----Task{0}----".format(i))
    q.task_done()

q = queue.Queue()
threads = []
for i in range(num_worker_threads):
  t = threading.Thread(target=worker)
  t.start()
  threads.append(t)

for item in source():
  q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
  q.put(None)
for t in threads:
  t.join()

