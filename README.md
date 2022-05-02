# Shark & Human Tracking 

## Setting Up for VIA2Coco
-  Python libraries like opencv, and matplotlib should be installed 
-  Install [cocoapi](https://github.com/cocodataset/cocoapi) (make sure u can run [coco's demo code](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb)) 
-  FFmpeg is also needed for combining videos 
-  Separate each video into frames (with ffmpeg); frames from the same video need be in the same folder and not mixed up with another other images or frames from other videos & the names of the folders should be the same as the video. The frames themselves should also be stored as `<video_name>-<frame 3>.jpg`
    - I store all frames in the folder `shark_frames`, and in `shark_frames`, there is a folder for each video w/ the same name as video. (eg. frames from  `DJI_0386.mp4` are stored in `shark_frames/DJI_0386/DJI_0386-<frame #>.jpg`
  
-  VIA annotations should have the same name as their video counterparts; via's meta data isn't considered. 
    - The annotations should have object label or object present as well as an id. If another word is used, change the code around [here](https://github.com/liliarose/cv_project/blob/f0bcfab45936952079a50356e40089ed1cd309a8/via2coco.py#L34)


## Functionalities 
-   __VIA to Coco__: Here's a [sample notebook](https://github.com/liliarose/cv_project/blob/main/via2coco_example.ipynb) for converting a single video's VIA to Coco.   
    -  Alternatively, you can use the [commandline version](https://github.com/liliarose/cv_project/blob/main/via2coco.py) to convert a whole folder of annotations; type `python via2coco.py --help` for more info. 
- [__Coco to py-MDNet input__](https://github.com/liliarose/cv_project/blob/main/coco2mdnetI.ipynb): This converts coco annotations to py-MDNet's input json format; it will generate a file for each object
- [`create_bash.py`](https://github.com/liliarose/cv_project/blob/main/create_bash.py) was used to generate bash scripts to submit using `sbatch`
- [This notebook](https://github.com/liliarose/cv_project/blob/main/draw%20frames%20%26%20combine.ipynb) draws the bounding boxes using the input and output files from py-MDNet.  
