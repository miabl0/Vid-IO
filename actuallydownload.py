import pandas as pd
import os
import pandas as pd
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterError
import hashlib
import sys
import signal
import tomli
import youtube_dl
import csv
import collections


#Global variables
filehashes = ['empty']
filenames = ['empty']
dir_path = os.path.dirname(os.path.abspath(__file__))

#Convert multi layer dict to single layer dict
#keys are joined for each value
def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)




def downloadFromTwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, video_download_location, tweettext_download_location, search_query, product, label):
    hasher = hashlib.md5()
    df = pd.DataFrame()
    #If the csv of existing videohashes somehow gets lost, create a new one from all downloaded videos
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
    
    #Continually do api requests
    while True:
        print("doin a query")
        
        SEARCH_TERM = search_query
        PRODUCT = product
        LABEL = label
        PRODUCT = '30day'
        LABEL = 'myLabel'
        api = TwitterAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret, auth_type='oAuth1')
        r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), {'query':SEARCH_TERM})
        #Do continual requests
        try:
            #Go through every item in the response of the twitter api
            for item in r:
                
                if 'text' in item:
                    #break up response
                    id_str = item['id_str']
                    username = item['user']['name']
                    screen_name = item['user']['screen_name']
                    url = "https://twitter.com/" + screen_name + "/status/" + id_str
                    textpath = tweettext_download_location
                    if os.path.isfile(textpath) == False:
                        print(url)
                        print(username)
                        #Download the video with youtube-dl and save it with the tweetid as its name
                        ydl_opts = {"outtmpl": os.path.join(video_download_location,id_str + ".mp4")}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                        
                        #Hash the video, if it was downloaded previously, append metadata and delete the duplicate video 
                        with open(os.path.join(video_download_location,id_str+ ".mp4"), 'rb') as afile:
                            buf = afile.read()
                            hasher.update(buf)
                        hashVal = (hasher.hexdigest())
                        if hashVal in filehashes:
                            os.remove(os.path.join(video_download_location,id_str + ".mp4"))
                            #Append existing metadata
                            if os.path.isfile(os.path.join(tweettext_download_location, id_str + ".csv")):
                                with open(os.path.join(tweettext_download_location, id_str + ".csv"), 'r+') as f:
                                    writeDict= flatten(item)
                                    reader = csv.DictReader(f)
                                    write_obj = [writeDict, write_obj]
                                    writer = csv.DictWriter(f, fieldnames=writeDict.keys())
                                    writer.writeheader()
                                    writer.writerows(write_obj)
                        else:
                            filehashes.append(hashVal)
                            #Create new metadata file
                            with(open(os.path.join(tweettext_download_location,id_str + ".csv"), 'w+')) as f:
                                writeDict= flatten(item)
                                writer = csv.DictWriter(f, fieldnames=writeDict.keys())
                                writer.writeheader()
                                writer.writerow(writeDict)
                        
                #save all responses you ever got from twitter, allowing you to go through them again at a later time
                with(open(os.path.join(dir_path,"response.txt"), 'a+')) as f:
                    f.write(str(r.json()))
        #Possible errors being caught here:
        #The given Query was formatted wrong
        #You are out of API Requests on your current token+endpoint
        except TwitterError.TwitterRequestError as e:
            print(e)
            print("stopping")
            break

            
def main():
    #Read variables from config file
    tomldict = {}
    with(open(os.path.join(dir_path,"download_videos.toml"), "rb") as f):
        tomldict = tomli.load(f)
    #Load variables from dict
    consumer_key = str(tomldict["consumer_key"])
    consumer_secret = str(tomldict["consumer_secret"])
    access_token_key = str(tomldict["access_token_key"])
    access_token_secret = str(tomldict["access_token_secret"])
    video_download_location = str(tomldict["video_download_location"])
    tweettext_download_location = str(tomldict["tweettext_download_location"])
    search_query = str(tomldict["search_query"])
    product = str(tomldict["product"])
    label = str(tomldict["label"])


    downloadFromTwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, video_download_location, tweettext_download_location, search_query, product, label)

#Allowing to stop the downloder via ctl+c, while still appending the video hashes to alreadydownloadedfiles.csv
def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    df = pd.DataFrame(filehashes, index=filenames, columns=["Hashes"])
    df.to_csv(os.path.join(dir_path,"outfiles","alreadydownloaded.csv"))
    sys.exit(0)

if __name__=="__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    main()