import glob
from moviepy.editor import *
import moviepy.editor
import os

clips = []
for filename in glob.glob(R'Videos\*.mp4'):
    clips.append(VideoFileClip(filename))
final = concatenate_videoclips(clips,method='compose')
moviepy.video.fx.all.resize(final, height=1024, width=600)
final.write_videofile(R"Saved videos\Video_SS.mp4")

os.system('ffmpeg -i "Saved videos\Video_SS.mp4" "Saved videos\Video_SS.avi" -y')

