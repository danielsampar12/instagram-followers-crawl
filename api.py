import os
import requests
import pandas as pd
import sys

target_username = sys.argv[1]
df = pd.read_csv(os.getcwd() + os.sep + "data" + os.sep + target_username + os.sep + "followers.csv", encoding='utf-8-sig')
numpyarr = df.to_numpy()

arr = numpyarr.tolist()
url = 'http://192.168.1.6:1337/follows'


for x in arr:
  p = {'follower': x[0], 'user': x[1]}
  x = requests.post(url, data = p)
 



