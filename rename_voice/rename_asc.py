import os
import re

# directory/folder path
dir_path = r"C:/Users/omarb/OneDrive/Documents/Sound Recordings"


# Iterate directory
for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)) and file_path.find("Recording") != -1:
        s = file_path
        i = re.findall(r"\(\s*\+?(-?\d+)\s*\)", file_path)
        # add filename to list
        os.renames(os.path.join(dir_path, file_path),
                   os.path.join(dir_path, "Recording ("+str(int(i[0])+99)+")"))
