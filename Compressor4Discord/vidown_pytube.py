import pytube
import ctypes
import os
from pytube.cli import on_progress
import spotdl


#CTYPES_MessageBox_icons
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

#windowsmessagebox
MessageBox = ctypes.windll.user32.MessageBoxW

def mbox_error(message):
    return ctypes.windll.user32.MessageBoxW(0,message, 'Compress for Discord', MB_OK | ICON_INFO)

def mbox(message):
    return ctypes.windll.user32.MessageBoxW(0,message, 'Compress for Discord', MB_YESNO | ICON_EXLAIM)

def ytdownload(link):
    # where to save 
    userprofile_path = os.environ['USERPROFILE']
    save_path = userprofile_path + '\AppData\Local\Temp\Compressor4Discord' 

    if not os.path.exists(save_path):
        os.makedirs(save_path)

  
    # link of the video to be downloaded 
  
    try: 
        # object creation using YouTube
        # which was imported in the beginning 
        yt = pytube.YouTube(link, on_progress_callback=on_progress) 
    except: 
        print("Connection Error") #to handle exception 
        mbox_error('''Connection Error!
    Please reconnect your PC to the internet and try again later''')
  
    # filters out all the files with "mp4" extension 
    mp4files = yt.streams.filter('mp4') 
  
# get the video with the extension and
# resolution passed in the get() function 

#tag 22 means youtube 720p
    streams = yt.streams.get_by_itag(22) 
    try: 
    # downloading the video 
        streams.download(save_path)
        print('YouTube Video Downloaded Successfully!') 
    except: 
        print("An error ocorrued while downloading the YouTube Video!") 

 