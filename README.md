# Vid-IO
- Twitter Video Scraper using the Twitter API and Python

# General Information
- This scraper will download videos from the advanced search query you provide.
- It was developed to help document misinformation and create a timeline during the War between Russia and Ukraine.
- The videos will be named after their unique tweet id. More information about each video can be found in the text file of the same name, saved in the tweettext folder.
- Downloading of duplicates is cut down on by computing the md5 hash of each video and adding it to the actuallydownloaded.csv file in the outfiles folder.
- Any file that has already been downloaded will be deleted, eliminating exact duplicate videos.

# Prerequisites:
- You need a Twitter Developer Account.
- You can sign up for one here: https://developer.twitter.com/en
- Once you have your Developer Account, you will need to fill in your Accounts Consumer Key and Consumer Secret key into their respective fields in the download_videos.toml file.
- Afterwards, register a new App Here: https://developer.twitter.com/en/portal/apps/new
- Put the API Key and API Secret Key into the access_token_key and access_token_secret fields in the download_videos.toml.
- Now set up an Environment here: https://developer.twitter.com/en/account/environments
- Select 30 Days, select your lable and set that label in the download_videos.toml file.
(If you have access to a paid subscription, you can also register your environment as fullarchive)

-- Optional:
- You can gain elevated API access by applying in your developer dashboard: https://developer.twitter.com/en/portal/dashboard
- This will get you a range of privileges, listed here: https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api


# Installation/Usage:
0. Do the steps laid out in the Prerequisites Section.

Linux: 
1. Install python3 using your Distro's Package Manager
2. Navigate into this folder using the Terminal
3. Enter the following Command to install the dependencies of this project: "pip3 install -r requirements.txt"
4. (Optional) Change video_download_location and tweettext_download_location fields in the download_videos.toml file to the folder you want your videos and tweet texts to end up in.
5. Change your search_query in download_videos.toml to the query you'd like to scrape. For non academic/paid twitter API access, you are limited to queries of 256 characters.
6. Start the script, using the command "python3 actuallydownload.py"

Windows:
1. Install python3: https://www.python.org/downloads/
2. Open powershell and navigate to this folder using "cd pathtofthisfolder"
3. Enter the following command to install the dependencies of this project: "pip install -r requirements.txt"
4. Change the video_download_location and tweettext_download_location fields in the download_videos.toml file to ".\out\videos\" and ".\out\tweettext\" (or another path, whereever you want to save these). 
5. Change your search_query in download_videos.toml to the query you'd like to scrape. For non academic/paid twitter API access, you are limited to queries of 256 characters.
6. Start the script, using the command "python actuallydownload.py"

Mac:
I do not have a mac, so if issues arise, please ask a mac user. 
Steps will be similar to the Linux steps.
Get python3 here: https://www.python.org/downloads/macos/
Then try following the Linux steps.
