import os
n = 0

with open("number.txt", "r+", encoding="utf-8") as number:
    n = int(number.read())
    number.seek(0)
    number.truncate()
    try:
        while (1):
            transcription = input("input transcription " + str(n)+" : \n")
            with open("csv.txt", "r+", encoding="utf-8") as csv:
                csv.seek(0, os.SEEK_END)
                csv.write("\nroot_dir/audio_wav_"+str(n)+".wav,"+transcription)
                n = n+1
                csv.close()

    except KeyboardInterrupt:
        number.write(str(n))
        number.close()
