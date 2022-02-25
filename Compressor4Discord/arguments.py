import argparse
import webbrowser
from vidown_pytube import *
from list_folder import *

video_compression_target = 0

parser = argparse.ArgumentParser(description='Compressor 4 Discord:')
args, unknown = parser.parse_known_args()
#set target video compression size
parser.add_argument('-s', action='store_const', const='video_compression_target', default='')
unknown = video_compression_target

#add a folder of various media to compress as a queue
parser.add_argument('-q','--queue', help="Add folder with media files to compress as a queue")

#download video from youtube and compress it
parser.add_argument('-yt','--youtube', help="Download a YouTube Video and then compress it")

#download youtube audio and compress it
parser.add_argument('-ytA','--YouTubeAudio')

#download songs with spotify links through spotdl
parser.add_argument('-spdl','--spotdl', help="Download a spotify song and if it is a large file, the compress it")

#Give a Rickroll
parser.add_argument('-rck','--rick', help="You just got Rickrolled",action="store_true")

arg = parser.parse_args()
print(arg)

def spotdl_download(spotify_link):
    os.system("spotdl" + spotify_link)

if arg.queue:
    list_media_folder(arg.queue)

#if arg.spotdl():
 #   spotdl_download(arg.spotdl)


if arg.youtube:
    print(arg.youtube)
    ytdownload(arg.youtube)

if arg.rick:
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print("Why did you do this to yourself? WHY?")





