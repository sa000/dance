
#Download video from tiktok with urllib
import urllib.request
import requests 
import json
import moviepy.editor as mp


import time 
#remove html tags from response text
import re
INPUTDIR = 'input'
#Decorator to see how long it takes to run a function
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r  %2.2f sec' % \
              (method.__name__, te-ts))
        return result

    return timed
@timeit
def get_tiktok_mp4_url(url:str) -> str: 
    '''
    Exctract the video mp4 url from the tiktok url by looking at the response data and parising through to find the url in "preLoadList"

    '''
    time.sleep(5)
    response = requests.get(url).text+''
    mp4_json = response.split('preloadList":[')[1].split(',"id"')[0]+'}'
    mp4_url = json.loads(mp4_json)['url']
    print(mp4_url)
    return mp4_url

def download_file(url: str, filename:str ):
    '''
    Download a url thats just an mp4 locally
    '''
    urllib.request.urlretrieve(url, f'{INPUTDIR}/{filename}.mp4')
    print("Download file complete", filename)

#Convert mp4 to gif
@timeit

def convert_mp4_to_gif(filename:str):
    '''
    Convert an mp4 to a gif
    '''
    clip = mp.VideoFileClip(f"{filename}.mp4")
    clip.write_gif(f"{INPUTDIR}/{filename}_y.gif")
    print("Convert mp4 to gif complete", filename)


filename = 'v1'
url = 'https://www.tiktok.com/t/ZTRuVvjsg/'

mp4_url = get_tiktok_mp4_url(url)
download_file(mp4_url, filename)
convert_mp4_to_gif(filename)

