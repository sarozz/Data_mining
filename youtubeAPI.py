import warnings
import csv
import pandas as pd
from pprint import pprint
from apiclient.discovery import build
warnings.filterwarnings('ignore')
api_key = "AIzaSyDuyO7-bZvAdsjQiWv8yw7350O8UX1mgzs"
youtube = build('youtube', 'v3', developerKey = api_key)
waste,video_id = video_url.split("=")
#req = youtube.commentThreads().list(videoId = "UCqC-b4Hkp_Dv9VNVJxfc4VA", part = "snippet", textFormat = "plainText").execute()
results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText",
    maxResults = 50
  ).execute()
print(type(results))
#pprint(results)

#print(len(results))
for items in results["items"]:
    comment = items["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    channelIds = comment["snippet"]["authorChannelId"]["value"]
    raw_data = {'Author':[author], 'Comment': [text], 'ChannelId': [channelIds]}
    # df = pd.DataFrame(raw_data, columns= ['Author', 'Comment','ChannelId'])
    # df.to_csv('comments.csv')
    #print(df)
    print("\n {} comments \n {} \n\n ".format(author,text))
    #To save all the comments along with author in CSV file
    #pprint("{}'s channel id is {}".format(author,channelIds))
