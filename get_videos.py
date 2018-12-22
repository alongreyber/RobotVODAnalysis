from pytube import YouTube
import requests

base_url = 'http://www.thebluealliance.com/api/v3/'

headers = {'X-TBA-Auth-Key' : 'HmLM0gRxFg9TSNcMRNoDUZBVp105U5TrYExLLckCuivxQarsvj3UBOqXBSNQ3vbX'}

# Events with a camera feed that doesn't move (kinda)
events = ['2018qcmo', '2018isde1', '2018mawor', '2018onbar', '2018inmis']

# Number of matches to process
num_matches = 1

# Number of videos per match to process
num_videos = 1

for e in events:
    r = requests.get(base_url + 'event/' + e + '/matches', headers=headers)
    data = r.json()
    i = 0
    for match in data:
        if i >= num_matches:
            break
        if match == 'Errors':
            print("Error in event: " + e)
            continue
        j = 0
        for video in match['videos']:
            if j >= num_videos:
                break
            if len(video['key']) != 11:
                print("Skipping video with weird format: " + video['key'])
                continue
            video_url = "http://youtu.be/" + video['key']
            print("Downloading: " + video_url)
            YouTube(video_url).streams.first().download(filename=video['key'])
            j += 1
        i += 1
