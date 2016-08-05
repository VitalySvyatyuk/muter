import os, sys
from pydub import AudioSegment
from pydub.silence import detect_silence
from pydub.utils import mediainfo
from mutagen.mp3 import MP3



print("Muter 1.2")

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
    print("Threshold is " + threshold)
    threshold = int(threshold)
except:
    threshold = -30
    print("Wrong value. Threshold is " + str(threshold))

TAG_ABBRS = [
    'TIT2', 'CHAP', 'CTOC', 'TIT1', 'TCON', 'COMM', 'TORY', 'TRCK',
    'TYER', 'TDRC', 'TDAT', 'TIME', 'IPLS', 'TPE1', 'TIT3', 'POPM',
    'APIC', 'TALB', 'TPE2', 'TSOT', 'TDEN', 'TIPL', 'RVAD'
]
TAG_WORDS = [
    'Title', 'Chapter', 'Table of contents', 'Content group description',
    'Content type (Genre)', 'User Comment', 'Original Release Year',
    'Track Number', 'Year of recording', 'Recording Time',
    'Date of recording (DDMM)', 'Time of recording (HHMM)',
    'Involved People List', 'Artist',
    'Subtitle/Description refinement', 'Popularimeter', 'Attached Picture',
    'Album', 'Band/Orchestra/Accompaniment', 'Title Sort Order key',
    'Encoding Time', 'Involved People List', 'Relative volume adjustment'
]
TAGS = {}

log = open('log.txt', 'w')
for wave in os.listdir("Audio"):
    if wave.endswith(".mp3"):
        sound = AudioSegment.from_file("Audio/" + wave)
        first = AudioSegment.silent(duration=0)
        last = first
        center = sound
        sil = detect_silence(sound, min_silence_len=10, silence_thresh=threshold)
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
       # last = AudioSegment.silent(duration=len(last))
       # last = AudioSegment(duration=len(last))
        output = first + center + last
        
        filetags = MP3("Audio/" +filename+ ".mp3")
        
        for tag in TAG_ABBRS:
            if tag in filetags.keys():
                TAGS[TAG_WORDS[TAG_ABBRS.index(tag)]] = filetags[tag].text[0]
                
        output.export("Result/" +filename+ ".mp3", format="mp3",
                      bitrate=str(filetags.info.bitrate),
                      tags=TAGS)
    # print(filename + " " + str(len(first)) + " " + str(len(last)) +" " + str(TAGS) + " is ready.")
        print(filename + " " + str(len(first)) + " " + str(len(last)) + " is ready.")
        log.write(filename)
        log.write(" first=" +str(len(first)))
        log.write(" last=" +str(len(last))+ "\n")
log.close()

