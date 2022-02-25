import cv2
import glob

filepath = "Saved videos\Img_SS.avi"
out = cv2.VideoWriter(filepath,cv2.VideoWriter_fourcc(*'MJPG'), 0.3333333, (600,1024))
for filename in glob.glob(R"Images\*.jpg"):
    img = cv2.imread(filename)
    img = cv2.resize(img,(600,1024))
    out.write(img)
out.release()



