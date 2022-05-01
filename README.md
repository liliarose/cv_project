# Shark & Human Tracking 

## Setting Up for VIA2Coco
-  Python libraries like coco, opencv, matplotlib should be installed (make sure u can run coco's demo code) 
-  FFmpeg is also needed
-  VIA annotations should have the same name as their video counterparts; some of via's meta data isn't considered. 
    -  Having the via annotations & videos together will make your life easier if you want to use the commandline version 
- Separate each video into frames; frames from the same video should be in the same folder and not mixed up with another other images or frames from other videos
    -  Sample command to split frames & then if u know enough bash/python, u can move the files into individual folders: `for i in *.mp4; do ffmpeg -i "$i" "${i%.*}.mp4"; done`
