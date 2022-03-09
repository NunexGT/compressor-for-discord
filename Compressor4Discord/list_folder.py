import os
from statistics import median

def list_folder(mediadir):
  extensions_file = open("file_extensions.list", "r")

  extensions_list = []
  for line in extensions_file:
    stripped_line = line.strip()
    line_list = stripped_line.split()
    extensions_list.append(line_list)

  extensions_file.close()
  loop_int = -1

  def check_files_with_extension(extensions_list,loop_int):
    for x in extensions_list:
        loop_int = loop_int + 1
        extension__list_value = extensions_list[loop_int]
        extension_str = str(extension__list_value)[1:-1]
        extension = extension_str.replace("'",'',2)
        get_files(extension)

  def get_files(extension):
    for file in os.listdir(mediadir):
      if file.endswith(extension):
        print(os.path.join(mediadir, file))

  check_files_with_extension(extensions_list,loop_int)