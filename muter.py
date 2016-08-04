import os, sys
from pydub import AudioSegment
from pydub.silence import detect_silence
from pydub.utils import mediainfo
from subprocess import Popen, PIPE



print("Muter 1.0")

if not os.path.exists("Result"):
    os.makedirs("Result")
    
if not os.path.exists("Audio"):
    sys.exit("Can't find 'Audio' folder")
    
if os.name == "nt":
    FFMPEG_BIN = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.converter = FFMPEG_BIN
else:
    FFMPEG_BIN = "ffmpeg"

print("")
print("Please specify threshold of the silence. For example: -28")
print("..or just press Enter. Silence will be by default -35")
threshold = input("Threshold: ")

try:
    if not threshold[0] == "-":
        threshold = "-" + threshold
    threshold = int(threshold)
    print("Threshold is " + str(threshold))
except:
    threshold = -35
    print("Wrong value. Threshold is -35")

iter = 0
for wave in os.listdir("Audio"):
    iter += 1
    if wave.endswith(".mp3"):
        sound = AudioSegment.from_file("Audio/" + wave)
        first = AudioSegment.silent(duration=0)
        last = first
        center = sound
        sil = detect_silence(sound, min_silence_len=100, silence_thresh=threshold)
        if len(sil) == 0:
            pass
        elif len(sil) == 1:
            if sil[0][0] == 0:
                first = sound[0:sil[0][1]]
                center = sound[sil[0][1]:len(sound)]
            elif sil[0][1] == len(sound):
                last = sound[sil[0][0]:sil[0][1]]
                center = sound[0:sil[0][0]]
        elif len(sil) > 1:
            if sil[0][0] == 0:
                first = sound[0:sil[0][1]]
                if sil[-1][1] == len(sound):
                    last = sound[sil[-1][0]:sil[-1][1]]
                    center = sound[sil[0][1]:sil[-1][0]]
                else:
                    center = sound[sil[0][1]:len(sound)]
            else:
                if sil[-1][1] == len(sound):
                    last = sound[sil[-1][0]:sil[-1][1]]
                    center = sound[0:sil[-1][0]]
        filename = os.path.splitext(wave)[0]
        first = AudioSegment.silent(duration=len(first))
        last = AudioSegment.silent(duration=len(last))
        output = first + center + last
        output.export("Result/" +filename+ ".mp3", format="mp3",
                      )
        print(filename + " is ready.")
#        nam = "D:\\Mail\\David\\Audio\\sample_1.mp3"
        print(mediainfo("Audio/" +filename+ ".mp3").get('TAG', {}))

