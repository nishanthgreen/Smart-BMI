from glob import glob
import os
import glob

for filename in glob.glob(R'Videos\*.mp4'):
    a = filename.split('\\')
    ind = a[1].split('.')
    rfp = a[0]+'\\'+ind[0]+'.avi'
    os.system(f'ffmpeg -i {filename} {rfp} -y')
    