from __future__ import unicode_literals
import youtube_dl
import re
import os
import threading
from argparse import ArgumentParser

# https://github.com/ytdl-org/youtube-dl/tree/3e4cedf9e8cd3157df2457df7274d0c842421945

import urllib.request
from bs4 import BeautifulSoup

def get_songs_from_file(fname):
    content = []
    try:
        print("Getting songnames from file {} ..".format(fname))
        with open(fname) as f:
            content = f.readlines()
        
        content = [x.strip() for x in content]
        print("Found {} songs to download ..\n".format(len(content)))
        return content
    except Exception as e:
        print(e)
        return []

def search_and_download_song(song):
    song_url = find_youtube_url_from_song_name(song)
    download_song(song_url,song)
    print("\n")
    return
    
def main():
    parser = ArgumentParser()
    parser.add_argument("-i","--input",help="input file where songnames are specified for the download",default="test.txt")
    args = parser.parse_args()
    
    song_list = get_songs_from_file(args.input)
    for song in song_list:
        t = threading.Thread(target=search_and_download_song,args=(song,))
        t.start()
        #t.join()
        
# https://stackoverflow.com/questions/29069444/returning-the-urls-as-a-list-from-a-youtube-search-query
def find_youtube_url_from_song_name(songname):
    
    query = urllib.parse.quote(songname)
    print("Finding URL for song {} ..".format(songname))
    
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if ( re.match('^\/watch\?v=.{11}$',vid['href']) ):
            yt_url = 'https://www.youtube.com' + vid['href']
            print("Found:\t{}".format(yt_url))
            return yt_url
    print("Not Found ..")
    return
    
# https://www.programcreek.com/python/example/98358/youtube_dl.YoutubeDL
def download_song(song_url="http://www.youtube.com/watch?v=BaW_jenozKc", song_title="youtube-dl", path='.'):
    """
    Download a song using youtube url and song title
    """
    if (song_url==None): return
    
    #outtmpl = os.path.join(path,'test',song_title + '.%(ext)s')
    outtmpl = os.path.join(path,'download',song_title+'.mp3')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'mp3',
              'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
        ],
    }
    
    try:
        print("Downloading {} ..".format(song_title))
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(song_url, download=True) 
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    main()