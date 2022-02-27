import pandas as pd
import time
import os
import pandas as pd
from TwitterAPI import TwitterAPI
import hashlib
import sys
import signal
import tomli
from requests_oauthlib import OAuth1
import urllib.request
import urllib.error
import youtube_dl
#can apphend date to metadata File
#maybe to filename too
#add 


#Global variables
filehashes = ['empty']
filenames = ['empty']
dir_path = os.path.dirname(os.path.abspath(__file__))




def downloadFromTwitterAPI():
    hasher = hashlib.md5()
    df = pd.DataFrame()
    if os.path.isfile(os.path.join(dir_path, "outfiles", "alreadydownloaded.csv")) == False:
        hash_list = []
        name_list = []

        checkpath = video_download_location
        for file in os.listdir(checkpath):
            hashVal = ""
            filename = os.path.join(video_download_location, file)
            with open(filename, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
                hashVal= (hasher.hexdigest())
                hash_list.append(hashVal)
                name_list.append(file)
        df = pd.DataFrame(hash_list, index=name_list, columns=["Hashes"])
        df.to_csv(os.path.join(dir_path, "outfiles", "alreadydownloaded.csv"))
    else:
        filehashes = pd.read_csv(os.path.join(dir_path, "outfiles", "alreadydownloaded.csv"))["Hashes"].tolist()
    
    while True:
        print("doin a query")
        
        SEARCH_TERM = search_query
        PRODUCT = product
        LABEL = label
        PRODUCT = '30day'
        LABEL = 'myLabel'
        api = TwitterAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret, auth_type='oAuth1')
        r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), {'query':SEARCH_TERM})
        for item in r:
            
            if 'text' in item:
                
                id_str = item['id_str']
                username = item['user']['name']
                screen_name = item['user']['screen_name']
                url = "https://twitter.com/" + screen_name + "/status/" + id_str
                textpath = tweettext_download_location
                if os.path.isfile(textpath) == False:
                    print(url)
                    print(username)
                    ydl_opts = {"outtmpl": os.path.join(video_download_location,id_str + ".mp4")}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ret = ydl.download([url])
                    
                    with open(os.path.join(video_download_location,id_str+ ".mp4"), 'rb') as afile:
                        buf = afile.read()
                        hasher.update(buf)
                    hashVal = (hasher.hexdigest())
                    if hashVal in filehashes:
                        os.remove(os.path.join(video_download_location,id_str + ".mp4"))
                    else:
                        filehashes.append(hashVal)
                        with(open(os.path.join(tweettext_download_location,id_str + ".txt"), 'w+')) as f:
                            f.write(url)
                            f.write(item['text'])
                            f.write(item['user']['name'])
                            f.write(item['user']['screen_name'])
                            filenames.append(id_str)
                        
            with(open(os.path.join(dir_path,"response.txt"), 'a+')) as f:
                f.write(str(r.json()))
            
def main():
    tomldict = {}
    with(open(os.path.join(dir_path,"download_videos.toml"), "rb") as f):
        tomldict = tomli.load(f)
    global consumer_key
    global consumer_secret
    global access_token_key
    global access_token_secret
    global video_download_location
    global tweettext_download_location
    global search_query
    global product
    global label
    consumer_key = str(tomldict["consumer_key"])
    consumer_secret = str(tomldict["consumer_secret"])
    access_token_key = str(tomldict["access_token_key"])
    access_token_secret = str(tomldict["access_token_secret"])
    video_download_location = str(tomldict["video_download_location"])
    tweettext_download_location = str(tomldict["tweettext_download_location"])
    search_query = str(tomldict["search_query"])
    product = str(tomldict["product"])
    label = str(tomldict["label"])
    downloadFromTwitterAPI()

def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    df = pd.DataFrame(filehashes, index=filenames, columns=["Hashes"])
    df.to_csv(os.path.join(dir_path,"outfiles","alreadydownloaded.csv"))
    sys.exit(0)

if __name__=="__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    main()