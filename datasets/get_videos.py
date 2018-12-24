from pytube import YouTube
import click
import requests

base_url = 'http://www.thebluealliance.com/api/v3/'

headers = {'X-TBA-Auth-Key' : 'HmLM0gRxFg9TSNcMRNoDUZBVp105U5TrYExLLckCuivxQarsvj3UBOqXBSNQ3vbX'}

# Events with a camera feed that doesn't move (kinda)
events = ['2018qcmo', '2018isde1', '2018mawor', '2018onbar', '2018inmis', '2018ncgre', '2018mokc2', '2018miesc', '2018wayak']

@click.command()
@click.option("--matches", type=int, default=1)
@click.option("--videos", type=int, default=1)
def download(matches, videos):
    # Number of matches to process
    matches = 1
    # Number of videos per match to process
    videos = 1
    for e in events:
        r = requests.get(base_url + 'event/' + e + '/matches', headers=headers)
        data = r.json()
        i = 0
        for match in data:
            if i >= matches:
                break
            if match == 'Errors':
                click.echo("Error in event: " + e)
                continue
            j = 0
            for video in match['videos']:
                if j >= videos:
                    break
                if len(video['key']) != 11:
                    click.echo("Skipping video with weird format: " + video['key'])
                    continue
                video_url = "http://youtu.be/" + video['key']
                click.echo("Downloading: " + video_url)
                YouTube(video_url).streams.first().download(output_path="data/", filename=video['key'])
                j += 1
            i += 1

if __name__ == '__main__':
    download()
