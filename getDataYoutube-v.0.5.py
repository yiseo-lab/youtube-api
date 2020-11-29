# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import csv
import googleapiclient.discovery

DEVELOPER_KEY = "AIzaSyBIUVW5T4snLgw0A87q-XOlRqHdPfWReHA"                       # My api key 
FILENAME = "csv_data.csv"                                                     # define file location

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"


    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
    
    channel_id = request_channel_id(youtube, channel_youtube)
    upload_playlist_id = request_upload_id_playlist(youtube, channel_id)
    
    video_id = request_video_id(youtube, upload_playlist_id)
    # print(video_id)
    for videoId in video_id:
        request_video_data(youtube, videoId)

#----------------------------------------------------------------|
# Function get id of video upload playlist by use channel ID     |
#----------------------------------------------------------------|
def request_upload_id_playlist(youtube, channel_id):
    """ Get id of upload playlist of Channel """
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id,
        maxResults=50
    )
    response = request.execute()
    print(type(response))
    items_tag = response.get('items')
    print(type(items_tag))               # Type list

    for data_dic in items_tag:
        print('... Extract dict in list ')              # Type dict
     
    for key, value in data_dic.items():
        if key == 'contentDetails':
            print(f"{key} and {value}")
            
            for key_contentDetails, value_contentDetails in value.items():
               if key_contentDetails== 'relatedPlaylists':
                    print(f"{key_contentDetails} and {value_contentDetails}")

                    for key_relatedPlaylists, value_relatedPlaylists in value_contentDetails.items():
                        if key_relatedPlaylists == 'uploads':
                            print(f'{key_relatedPlaylists} and {value_relatedPlaylists}')
                            result_upload_playlist_id = value_relatedPlaylists
                            print(result_upload_playlist_id)

    return result_upload_playlist_id

#----------------------------------------------------------------|
# Function get videos form uploadplaylist                        |
#----------------------------------------------------------------|
def request_video_id(youtube, playlist_id):  
    result_video_id = []
    request = youtube.playlistItems().list(
        part="contentDetails,status",
        maxResults=50,
        #playlistId="UUtqzfvy3SMX-kHJC85HB7jA"
        playlistId = playlist_id
    )
    response = request.execute()
    print(type(response))

    items_tag = response.get('items')

    print(type(items_tag))               # Type list

    for data_dic in items_tag:
        print('---> Extract dict in list.')              # Type dict

        for key, value in data_dic.items():
            if key == 'contentDetails':
                print(f"{key} and {value}")
                for key_contentDetails, value_contentDetails in value.items():
                    if key_contentDetails == 'videoId':
                        print(f"{key_contentDetails} and {value_contentDetails}")
                        result_video_id.append(value_contentDetails)

    return result_video_id

#----------------------------------------------------------------|
# Function for get video data                                    |
#----------------------------------------------------------------|
def request_video_data(youtube, video_id):
    """Get data of video from youtube by use video id """
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id = video_id
    )
    response = request.execute()        # response type is dic
    create_csv(response)

#----------------------------------------------------------------|
# Function for create file .CSV                                  |
#----------------------------------------------------------------|
def create_csv(response_value):
    """ Create CSV File with youtube video data """
    items_tag = response_value.get('items')

    print(f"--- Extract list from dict")               # Type list

    for data_dic in items_tag:
        print('... Extract dict in list ')              # Type dict
        
 
    for key, value in data_dic.items():
        if key == 'id':
            print(f"https://www.youtube.com/watch?v={value}")
            video_url = f"https://www.youtube.com/watch?v={value}"

        if key == 'snippet':
            for sn_key, sn_value in value.items():
                if sn_key == 'title':
                    print(f"{sn_value}")                # Video name
                    video_name = f"{sn_value}"
                if sn_key == 'publishedAt':
                    print(f"{sn_value}")                # Time release
                    time_release = f"{sn_value}"   
                if sn_key == 'channelId':
                    print(f"{sn_value}")                # Channel ID
                    channel_id = f"{sn_value}"
                if sn_key == 'description':
                    print(f"{sn_value}")                # Discripton
                    #discription = f"{sn_value}"
                if sn_key == 'channelTitle':
                    print(f"{sn_value}")                # Channel name
                    channel_name = f"{sn_value}"
        
        if key == 'contentDetails':
            for sn_key, sn_value in value.items():
                if sn_key == 'duration':    
                    print(f"{sn_value}")                # Duration Video
                    duration_time = f"{sn_value}"

        if key == 'statistics':
            for sn_key, sn_value in value.items():
                if sn_key == 'viewCount':    
                    print(f"{sn_value}")                # View count
                    view_count = f"{sn_value}"
                if sn_key == 'likeCount':    
                    print(f"{sn_value}")                # Like count
                    like_count = f"{sn_value}"
                if sn_key == 'dislikeCount':
                    print(f"{sn_value}")                # Dislike count
                    dislike_count = f"{sn_value}"
                if sn_key == 'commentCount':
                    print(f"{sn_value}")                # Comment count
                    comment_count = f"{sn_value}"
                else:
                    comment_count = '0'

    ### Write csv ###
    # field names
    fields = ['Channel name', 'Channel ID', 'URL', 'Video name', 'Time release', 'Duration Video', 'View', 'Like', 'Disklisk', 'Comment count']
    # data rows of csv file
    rows = [channel_name, channel_id, video_url, video_name, time_release, duration_time, view_count, like_count, dislike_count, comment_count ]
    # writing to csv file
    with open(FILENAME, 'a+', encoding='utf-8', newline='') as csvfile:
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        
        # writing the fields if file size == 0 
        if os.stat(FILENAME).st_size == 0:
            csvwriter.writerow(fields) 
            csvwriter.writerow(rows)  
        else:
        # writing the data rows  
            csvwriter.writerow(rows) 


#----------------------------------------------------------------|
# Function get Channel_id from username                             |
#----------------------------------------------------------------|
def request_channel_id(youtube,youtube_username):
    result_channelId = ''
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=youtube_username
    )
    response = request.execute()
    
    #print(type(response))
    items_tag = response.get('items')
    #print(type(items_tag))               # Type list

    for data_dic in items_tag:
        #print('... Extract dict in list ')              # Type dict
        for key, value in data_dic.items():
            if key == 'id':
                #print(f"{key} and {value}")
                for key_id, value_id in value.items():
                    if key_id == 'channelId':
                        #print(f"{key_id} and {value_id}")
                        result_channelId = value_id

    if result_channelId == '':
        print("\nInvalid Youtube Username (T-T)\n")
        exit()
    else:
        return result_channelId


#----------------------------------------------------------------|
# Call main()                              |
#----------------------------------------------------------------|  
if __name__ == "__main__":
    prompt = "\nInput Channel USERNAME or Channel-ID "
    prompt += "or Enter 'quit' to end the script. \n ง(-_*)ง =: "

    active = True
    
    while active:
        message = input(prompt)
        
        if message == 'quit':
            active = False
        else:
            channel_youtube = message
            main()