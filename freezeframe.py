from moviepy.editor import *
from bs4 import BeautifulSoup

import os, urllib, urllib2, random

# DELETE OLD VIDEO

try:
    os.remove('input.mp4')
except OSError:
    pass

try:
    os.remove('input_2.mp4')
except OSError:
    pass

# EDIT VIDEO

clipArea = 0
#clipArea = int(VideoFileClip("input.mp4").duration/2) # pick from the middle of the video

# clip to 5 sec
command = "ffmpeg -i original.mp4 -strict -2 -ss "+ str(clipArea) +" -t 5 input.mp4"
print "FFMPEG: Clipping down to 5 sec \n"
os.system(command)

# convert to 360p (easier to manage)
# command2 = "ffmpeg -i input_2.mp4 -vf scale=-2:360 input.mp4"
# print "FFMPEG: Resizing to 360p \n"
# os.system(command2)

# pull it in for manipulation
clip = VideoFileClip("input.mp4")

# add in our audio clip
audioclip = AudioFileClip("recordscratch_vo.wav")
comp = concatenate_audioclips([clip.audio, audioclip])

# make that freeze frame
endtime = clip.duration - 0.1 # the videos ffmpeg exports aren't always exact in time, this ensures we get a freeze frame as close to the end as possible
freezeframe = clip.to_ImageClip(t=endtime)
screensize = VideoFileClip("input.mp4").size
freezeclip = (freezeframe
            .resize(height=screensize[1]*4)
            .resize(lambda t : 1+0.02*t)
            .set_position(('center', 'center'))
            .set_duration(8)
            )
freezeclip = CompositeVideoClip([freezeclip]).resize(width=screensize[0])
freezevid = CompositeVideoClip([freezeclip.set_position(('center', 'center'))],
                         size=screensize)

# combine and export video
final_clip = concatenate_videoclips([clip,freezevid]).set_duration(13).set_audio(comp)
final_clip.write_videofile("final.mp4",audio_codec='aac')
