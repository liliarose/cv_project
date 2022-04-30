# this file assumes that a single video/file
# does not check the 'project' or 'file' 
import cv2
import os 
import json 

def default_img_fldr(video_path):
    return video_path.split('/')[-1].split('.')[0]

# may not be used 
def gen_all_frames_from_video(video_path, output_folder=None):
    if not output_folder:
        output_folder = default_img_fldr(video_path)

    os.system(f'ffmpeg -i {video_path} {output_folder}/%d.jpeg')


def frame_num(output_folder=None, ext='.jpeg'):
    if not output_folder:
        output_folder = default_img_fldr(video_path)
    os.listdir('imgs')

def nullable_string(val):
    if not val:
        return None
    return val

def single_frame_by_time(video_path, seconds, output_name):
    # ffmpeg -i input_file.mp4 -ss 01:23:45.. -vframes 1 output.jpg
    os.system(f'ffmpeg -i {video_path} {output_name}')

def main(args):
    
    # get the json file w/ annot
    json_f = args.json_annot
    if json_f =='':
        video_s = args.video.split('.')[:-1]
        args.json_annot = '.'.join(video_s) + '.json'

    # read the annot 
    with open(json_f) as f:
        annot = json.load(f)

    # figure out metadata
    '''
    "1": {                          # attribute-id (unique)
      "aname":"Activity",           # attribute name (shown to the user)
      "anchor_id":"FILE1_Z2_XY0",   # FILE1_Z2_XY0 denotes that this attribute define a temporal segment of a video file. See https://gitlab.com/vgg/via/-/blob/master/via-3.x.y/src/js/_via_attribute.js
      "type":4,                     # attributes's user input type ('TEXT':1, 'CHECKBOX':2, 'RADIO':3, 'SELECT':4, 'IMAGE':5 )
      "desc":"Activity",            # (NOT USED YET)
      "options":{"1":"Break Egg", "2":"Pour Liquid", "3":"Cut Garlic", "4":"Mix"}, # defines KEY:VALUE pairs and VALUE is shown as options of dropdown menu or radio button list
      "default_option_id":""
    },
    '''
    # could include 'object_present', 'object_id', 'object_label'
    attr = annot['attributes'] 
    '''
    "ui": {
      "file_content_align": "center",
      "file_metadata_editor_visible": true,
      "spatial_metadata_editor_visible": true,
      "spatial_region_label_attribute_id": ""
    }
    '''
    ui = annot['config']['ui']
    data = annot['metadata']

    # separate dataset into temporal seg vs object seg
    # currently not doing anything with segments but can later 
    segs, obj_segs = [], []

    for k, d in data.values():
        if len(d['z']) > 1:
            segs.append(d)
        else:
            obj_segs.append(d)
    
    # transform 
    coco_format = { 'info': {}, 'licenses': [], 
            'images': [], 'annotations': [], 'categories': []} 
    '''  
    image{
    "id": int, "width": int, "height": int, 
    "file_name": str, "license": int, 
    "flickr_url": str, "coco_url": str, "date_captured": datetime,
    } 
    '''





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=str, help='video path')
    parser.add_argument('--json_annot', '-ja', help='path to the json file annotations', default=None, type=str)
    parser.add_argument('--output_folder', '-of', help='folder where frames are stored', default=None, type=str)
    args = parser.parse_args()

    json_f = args.json_annot
    if json_f =='':
        video_s = args.video.split('.')[:-1]
        args.json_annot = '.'.join(args.video.split('.')[:-1]) + '.json'

    gen_all_frames_from_video(args.video_path, args.output_folder) 
