import os

extensions = open("file_extensions.list").read().splitlines()
print(extensions)

def list_media_folder(mediadir):
    for file in os.listdir(mediadir):
        if file.endswith(extensions):
         print(os.path.join(mediadir, file))
