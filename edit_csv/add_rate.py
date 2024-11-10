

import re
import os
import wave
import contextlib

# directory/folder path
dir_path = r"C:/Bradai/focus/AI_ASR_model/new/audio_asr/"


# Iterate directory
for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)):
        with contextlib.closing(wave.open(dir_path+file_path, 'r')) as f:

            rate = f.getframerate()

            with open("csv.txt", "r+", encoding="utf-8") as f:
                lines = f.read().splitlines()

            with open("csv.txt", "w", encoding="utf-8") as f:
                for line in lines:
                    if (line.find(file_path) > -1) and (line.find(str(rate)) == -1):
                        print(line + "," + str(rate), file=f)
                    elif (line.find(file_path) > -1) and (line.find(str(rate)) > -1):
                        print(line, file=f)
                    elif (line.find(file_path) == -1):
                        print(line, file=f)
