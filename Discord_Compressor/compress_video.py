import os
import shutil
import subprocess
import ffmpeg
import sys
from moviepy.editor import *
import numpy as np
from PIL import Image
import glob
import ctypes
import tempfile
from shutil import copyfile
import time

#CTYPES_MessageBox_icons
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10


input("Press ENTER to begin...")

video_extensions = ['.mp4','.avi']
image_extensions = ['.jpg','.jpeg','.png']
audio_extensions = ['.mp3','.wav']
gif_extensions = ['.gif']

#config.txt
script_path = os.path.dirname(os.path.realpath(__file__))
read_config = open(script_path + '\\config.txt','r')
config = read_config.read()
read_config.close()
content_config = config.splitlines()

for bwords in content_config[::3]:
    config_value = bwords

#Use discord nitro preset
#config value is a string (nitro_preset = false or true)
discord_nitro_preset = config_value




i = input()


sys.argv  #sys.argv[1] is the file to upload

file_path = sys.argv[1]
print(file_path)
filename, extension = os.path.splitext(sys.argv[1])
print(extension)

#windowsmessagebox
MessageBox = ctypes.windll.user32.MessageBoxW

def mbox(message):
    return ctypes.windll.user32.MessageBoxW(0,message, 'Compress for Discord', MB_YESNO | ICON_EXLAIM)


def compress_video(video_full_path, size_upper_bound, two_pass=True, filename_suffix='-compressed'):
    """
    Compress video file to max-supported size.
    :param video_full_path: the video you want to compress.
    :param size_upper_bound: Max video size in KB.
    :param two_pass: Set to True to enable two-pass calculation.
    :param filename_suffix: Add a suffix for new video.
    :return: out_put_name or error
    """
    filename, extension = os.path.splitext(video_full_path)
    
    output_file_name = filename + filename_suffix + extension

    total_bitrate_lower_bound = 110000
    min_audio_bitrate = 92000
    max_audio_bitrate = 256000
    min_video_bitrate = 3000000

    try:
        # Bitrate reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
        probe = ffmpeg.probe(video_full_path)
        # Video duration, in s.
        duration = float(probe['format']['duration'])
        # Audio bitrate, in bps.
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)["bit_rate"])
        # Target total bitrate, in bps.
        target_total_bitrate = (size_upper_bound * 1024 * 8) / (1.073741824 * duration)
        if target_total_bitrate < total_bitrate_lower_bound and size_upper_bound == 8000:
            print('Bitrate is extremely low!')
            winmessagebox=mbox('''This Video is really large to fit in 8MB
Do you want to try the 100MB Discord Nitro Limit?''')
            #yes button is equal to 6
            if  winmessagebox == 6:
                compress_video(sys.argv[1], 100 * 1000)
            return False

        if target_total_bitrate < total_bitrate_lower_bound and size_upper_bound == 100000:
            print('Bitrate is extremely low!')
            winmessagebox=mbox('''This video will not fit into Discord without making the video unwatchable
Do You Want to use nomral optimization to make it smaller?''')
            #yes button is equal to 6
            if  winmessagebox == 6:
                optimized_video()
            return False

        # Best min size, in kB.
        best_min_size = (min_audio_bitrate + min_video_bitrate) * (1.073741824 * duration) / (8 * 1024)
        if size_upper_bound < best_min_size:
            print('Quality not good! Recommended minimum size:', '{:,}'.format(int(best_min_size)), 'KB.')
            # return False

        # Target audio bitrate, in bps.
        audio_bitrate = audio_bitrate

        # target audio bitrate, in bps
        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate

        # Target video bitrate, in bps.
        video_bitrate = target_total_bitrate - audio_bitrate
        if video_bitrate < 1000:
            print('Bitrate {} is extremely low! Stop compress.'.format(video_bitrate))
            return False

        i = ffmpeg.input(video_full_path)
        if two_pass:
            ffmpeg.output(i, '/dev/null' if os.path.exists('/dev/null') else 'NUL',
                          **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                          ).overwrite_output().run()
            ffmpeg.output(i, output_file_name,
                          **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                          ).overwrite_output().run()
        else:
            ffmpeg.output(i, output_file_name,
                          **{'c:v': 'libx264', 'b:v': video_bitrate, 'c:a': 'aac', 'b:a': audio_bitrate}
                          ).overwrite_output().run()

        if os.path.getsize(output_file_name) <= size_upper_bound * 1024:
            return output_file_name
        elif os.path.getsize(output_file_name) < os.path.getsize(video_full_path):  # Do it again
            return save_compressed_video(output_file_name, size_upper_bound)
        else:
            return False
    except FileNotFoundError as e:
        print('You do not have ffmpeg installed!', e)
        print('You can install ffmpeg by reading https://github.com/kkroening/ffmpeg-python/issues/251')
        return False

def optimized_video():
    os.system('cmd /c "ffmpeg -i ' + '"' + file_path + '"' + ' -vcodec h264 -acodec mp2 -b:a 192k ' + '"' + filename + '.mp4"' + '"')


        #end Video COmpression

        #start image compression


def image_compression(im):
    picture = Image.open(im)
    print(picture.size)
    filename, extension = os.path.splitext(sys.argv[1])
    file_name = filename + "-compressed" + extension 
    picture.save(file_name,optimize=True,quality=25)

    #gif compression

min_fps = 10
min_colors = 40
min_dimension = 160

limit_size = 1000000

# FUNCTIONS DEFINATION
# Get the width of the clip.


def getClipWidth(clip):
    # Get the first frame of the clip.
    frame = clip.get_frame(0)
    return np.size(frame, 1)

# Get the height of the clip.


def getClipHeight(clip):
    # Get the first frame of the clip.
    frame = clip.get_frame(0)
    return np.size(frame, 0)

# Tell the side with the least pixels ("width"/"height").


def getClipSide(clip):
    # Return the dimension with the smallest value.
    if (getClipWidth(clip) < getClipHeight(clip)):
        return 'width'
    else:
        return 'height'

# Get the dimension of the smallest side.


def getClipDimension(clip):
    return min(getClipWidth(clip), getClipHeight(clip))

# Get the total frames count of the clip.


def getClipFramesCount(clip):
    return int(clip.fps * clip.duration)

# Get the size of a file.


def getFileSize(path):
    return os.path.getsize(path)

# Show the info of the original clip.


def showOrigInfo(width, height, framesCount, fps, duration, colors, size):
    print('  Dimension: %d * %d' % (width, height))
    print('  Frames Count: %(fr)d (%(fps)d fps *  %(du).2f s)' %
          {'fr': framesCount, 'fps': fps, 'du': duration})
    print('  File Size: %d KB\n' % (size / 1000))

# Show the changes after compression.


def showChangedInfo(width, height, framesCount, fps, duration, colors, size,
                    orig_width, orig_height, orig_framesCount,
                    orig_fps, orig_duration, orig_size):
    print('  Dimension: %(orig_wid)d * %(orig_hei)d -> %(curr_wid)d * %(curr_hei)d' %
          {'curr_wid': width, 'curr_hei': height, 'orig_wid': orig_width, 'orig_hei': orig_height})
    print('  Frames Count: %(orig_fr)d (%(orig_fps)d fps *  %(orig_du).2f s) -> %(curr_fr)d (%(curr_fps)d fps *  %(curr_du).2f s)' %
          {'orig_fr': orig_framesCount, 'orig_fps': orig_fps, 'orig_du': orig_duration,
           'curr_fr': framesCount, 'curr_fps': fps, 'curr_du': duration})
    print('  Colors Count: %d' % colors)
    print('  Size: %(orig)d KB -> %(curr)d KB\n' %
          {'orig': (orig_size / 1000), 'curr': (size / 1000)})


# Compress the clip.



def compressGif(clip_path):
    # Output file name and path setting.
    separatePaths = clip_path.split('\\')
    output_filename = separatePaths[-1].split('.')[0] + '-compressed.gif'
    userprofile_path = os.environ['USERPROFILE']
    gifs_path = userprofile_path + '\AppData\Local\Temp\DiscordCompressed\ ' 
    if not os.path.exists(gifs_path):
        os.makedirs(gifs_path)
    print(gifs_path)
    #tempdir = tempfile.mkdtemp(prefix="DiscordCompressed", dir='"%TEMP%"')
    #print(tempdir) # e.g. "/tmp/myapp-fevhzh93"
    temp_path = gifs_path + output_filename
    print(temp_path)

    clip = VideoFileClip(clip_path)

    # Store original clip information
    shortest_side = getClipSide(clip)
    original_dimension = getClipDimension(clip)
    original_width = getClipWidth(clip)
    original_height = getClipHeight(clip)
    original_fps = clip.fps
    original_duration = clip.duration
    original_framesCount = getClipFramesCount(clip)
    original_size = getFileSize(clip_path)

    print('\nOriginal Info:')
    showOrigInfo(original_width, original_height, original_framesCount,
                 original_fps, original_duration, 0, original_size)

    # PRE-COMPRESSION
    # Change color count.
    current_colorsCount = 64

    # Set a variable for changing dimension.
    if original_dimension > 300:
        current_dimension = 300
    else:
        current_dimension = original_dimension

    # Change dimension based on the shortest side.
    if shortest_side == 'width':
        temp_clip = clip.resize(width=current_dimension)
    else:
        temp_clip = clip.resize(height=current_dimension)

    # Change fps.
    if original_fps > 15:
        current_fps = 15
    else:
        current_fps = original_fps

    # Compress to a gif file.
    temp_clip.write_gif(temp_path, fps=current_fps, program='ffmpeg',
                        colors=current_colorsCount, tempfiles=True)

    temp_clip = VideoFileClip(temp_path)
    current_size = getFileSize(temp_path)
    current_framesCount = getClipFramesCount(temp_clip)
    current_duration = temp_clip.duration
    print('\n\n1-time compression finished.')
    showChangedInfo(getClipWidth(temp_clip), getClipHeight(temp_clip),
                    current_framesCount, temp_clip.fps, current_duration,
                    current_colorsCount, current_size, original_width,
                    original_height, original_framesCount, original_fps,
                    original_duration, original_size)

    # COMPRESSION
    compression_counter = 1
    real_counter = 1

    while True:
        if (current_size < limit_size) or (current_fps <= min_fps and current_dimension <= min_dimension and current_colorsCount <= min_colors):
            # os.rename(temp_path, output_path)
            print('Ouput file saved to %s\n' % temp_path)
            break

        # Compression settings
        if compression_counter == 0:
            if original_dimension > 300:
                current_dimension = 300
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 1:
            if original_dimension > 260:
                current_dimension = 260
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 2:
            if original_fps > 12:
                current_fps = 12
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 3:
            current_colorsCount = 56
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 4:
            if original_dimension > 220:
                current_dimension = 220
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 5:
            current_colorsCount = 48
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 6:
            if original_dimension > 200:
                current_dimension = 200
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 7:
            current_colorsCount = 40
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 8:
            if original_fps > 10:
                current_fps = 10
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 9:
            if original_dimension > 160:
                current_dimension = 160
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue

        # Execute the compression
        # Change dimension based on the shortest side.
        if shortest_side == 'width':
            temp_clip = clip.resize(width=current_dimension)
        else:
            temp_clip = clip.resize(height=current_dimension)

        # Compress to a gif file.
        temp_clip.write_gif(temp_path, fps=current_fps, program='ffmpeg',
                            colors=current_colorsCount, tempfiles=True)

        temp_clip = VideoFileClip(temp_path)
        current_size = getFileSize(temp_path)
        current_framesCount = getClipFramesCount(temp_clip)
        current_duration = temp_clip.duration
        print('\n\n%d-time compression finished.' % (real_counter))
        moveGif(gifs_path, temp_path)
        showChangedInfo(getClipWidth(temp_clip), getClipHeight(temp_clip),
                        current_framesCount, temp_clip.fps, current_duration,
                        current_colorsCount, current_size, original_width,
                        original_height, original_framesCount, original_fps,
                        original_duration, original_size)

        
        
        
        
                    
def moveGif (gifs_path, temp_path):
    gif_directory=os.path.dirname(file_path)
    print("Saving .gif to" + gif_directory)
    shutil.move(temp_path, gif_directory)
    shutil.rmtree(gifs_path)


def get_audio_length(file_path):
    lenght = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(lenght)
    lenght_float = float(lenght.stdout)
    print(lenght_float)
    compress_audio(file_path,filename,lenght_float)
    
    

    
def compress_audio(file_path,filename,lenght_float):
    if lenght_float <= 540:
        os.system('cmd /c "ffmpeg -i ' + '"' + file_path + '"' + ' -map a -ab 128000 -ar 44100 ' + '"' + filename + '-compressed.mp3"' + '"')
    if lenght_float >= 540 and lenght_float <= 660:
        winmessagebox=mbox('''Your Audio File is too big to fit in 8MB without severe Audio Quality Loss
Do You Want to try a more aggresive compression?''')
        if winmessagebox == 6:
            os.system('cmd /c "ffmpeg -i ' + '"' + file_path + '"' + ' -map a -ab 96000 -ar 44100 ' + '"' + filename + '-compressed.mp3"' + '"')
        if winmessagebox == 5:
            mbox('Do you want to try the Discord Nitro Preset instead? (100MB)')
    if lenght_float >= 660 and lenght_float <= 990:
        winmessagebox=mbox('''Your Audio File is too big to fit in 8MB without severe Audio Quality Loss
Do You Really Want to try a more aggresive compression?''')
        if winmessagebox == 6:
            os.system('cmd /c "ffmpeg -i ' + '"' + file_path + '"' + ' -map a -ab 64000 -ar 44100 ' + '"' + filename + '-compressed.mp3"' + '"')
        if winmessagebox == 5:
            mbox('Do you want to try the Discord Nitro Preset instead? (100MB)')
    if lenght_float >= 990 and lenght_float <= 1920:
        winmessagebox=mbox('''Your Audio File is too big to fit in 8MB without severe Audio Quality Loss
Do You Wish to proceed with Potato NOKIA Sound Mode?''')
        if winmessagebox == 6:
            os.system('cmd /c "ffmpeg -i ' + '"' + file_path + '"' + ' -map a -ab 32000 -ar 44100 ' + '"' + filename + '-compressed.mp3"' + '"')
        if winmessagebox == 7:
            mbox('Do you want to try the Discord Nitro Preset instead? (100MB)')
    if lenght_float >= 1920:
        winmessagebox=mbox('''Warning! Your audio file will not fit in the 8MB size
Do you want to try the Discord Nitro Preset Instead? (100MB)''')
        if winmessagebox == 6:
            compress_audio_nitro(file_path, filename)

def compress_audio_nitro(file_path, filename):
    os.system('cmd /c "ffmpeg -i ' + '"' + file_path + '"' + ' -map a -ab 128000 -ar 44100 ' + '"' + filename + '-compressed.mp3"' + '"')


def execute_photo():
    im = os.path.basename(sys.argv[1])
    print(im)
    image_compression(im)
    
def execute_audio():
    if (discord_nitro_preset == 'nitro_preset = false'):
        compress_audio(file_path)
    if (discord_nitro_preset == 'nitro_preset = true'):
        compress_audio_nitro

def execute_gif():
    files_count = len(sys.argv) - 1
    for i in range(files_count):
        clip_path = str(sys.argv[i + 1])
        gif_path = os.path.dirname(os.path.abspath(sys.argv[1]))
        

        print('\n----------------------------------------------\nCurrent job: %s' % clip_path)
        print('\nOverall progress: %(current)d/%(overall)d Started.' %
                {'current': (i + 1), 'overall': files_count})

        compressGif(clip_path)

        print('\nOverall progress: %(current)d/%(overall)d Finished.' %
                {'current': (i + 1), 'overall': files_count})


def execute_video():
    if (discord_nitro_preset == 'nitro_preset = false'): 
        compress_video(sys.argv[1], 8 * 1000)
    if (discord_nitro_preset == 'nitro_preset = true'):
        compress_video(sys.argv[1], 100 * 1000)

#start compression

video_file_extensions = ['.mp4','.avi','.mkv']
audio_file_extensions = ['.mp3','.wav']
photo_file_extension = ['.jpg','.jpeg','.png']

if extension in video_file_extensions:
    execute_video()
    
if extension in audio_file_extensions:
    get_audio_length(file_path)
    execute_audio()
    
if extension in photo_file_extension:
    execute_photo()
    
if (extension == '.gif'):
    execute_gif()
