import cv2
import matplotlib.pyplot as plt
import numpy as np
import json
import os


def mdnet2list(video_fin, video_results, frames, offset=-1):
    '''
    video_fin: mdnet input folder for a single video

    results: list of filenames w/ video results

    frames: list of all the frames

    output: list of dictionaries w/ keys 'img' and 'bbox'
    '''
    # getting all the name of the images
    output = [{'img': frame, 'bbox': []} for frame in sorted(os.listdir(frames)) if frame.endswith('.jpg')]
    frame_num = int(output[-1]['img'].split('.jpg')[0].split('-')[-1])
    assert(frame_num == len(output)) # to confirm that all frames are generated


    for result in video_results:

        # gets the input file to figure out where we started out
        fn = result.split('/')[-1]
        input_fn = f'{video_fin}/{fn}'
        if not (os.path.isfile(result) and os.path.isfile(input_fn)):
            print('\tdropping', result)
            continue

        with open(result) as f:
            res_contts = json.load(f)
        with open(input_fn) as f:
            i_contts = json.load(f)

        # figures out where we started
        tmp = i_contts['img_list'][0].split('/')[-1]
        img_i = int(tmp.split('.jpg')[0].split('-')[-1]) + offset

        # append bboxes :)
        for bbox in res_contts['res']:
            if img_i < frame_num:
                output[img_i]['bbox'].append(bbox)
                img_i +=1
            else:
                print('dropped', img_i, bbox)

    return output

def mdnet2dict_all(fin_folder = 'mdnet_input', results_fldr='results', frame_fldr='shark_frames'):
    '''
    fin_folder: folder containing all mdnet input (for figuring out where it starts out)

    results: results folder containing all the results

    '''

    # get all video folders
    fin_fldrs = [fldr for fldr in os.listdir(fin_folder) if os.path.isdir(fin_folder)]
    fldr2bbox = {}
    # get list of corresponding video results in results folder
    # expecting it to have it be the same
    for fldr in fin_fldrs:
        video_fin = f'{fin_folder}/{fldr}'
        video_results = [f'{results_fldr}/{f}' for f in os.listdir(results_fldr) if f.startswith(fldr) and f.endswith('.json')]
        frames = f'{frame_fldr}/{fldr}'
        # only adds if there are video_results
        if len(video_results) >0:
            fldr2bbox[fldr] = mdnet2list(video_fin, video_results, frames)
    return fldr2bbox

def generate_results_boxes(frames_fldr, bboxes_l, output_folder='test', draw_text=True,  show_img=None,
                            box_thickness=10, fontScale = 4, color = (36,255,12), # neon green
                            font = cv2.FONT_HERSHEY_SIMPLEX, text_thickness = 10, ):
    '''
    frames_fldr: folder containing all the frames for a video
    bboxes_l: the bounding boxes output from mdnet2list function
    output_folder: folder to output the images
    draw_text: whether to draw the file names (for combining multiple videos together)
    show_img: whether or not to show every n-th image (n= show_img)
    '''
    for i, frame in enumerate(bboxes_l):
        fn = f"{frames_fldr}/{frame['img']}"
        bboxes = frame['bbox']
        image = cv2.cvtColor(cv2.imread(fn), cv2.COLOR_BGR2RGB)

        # adding annotations
        for box in bboxes:
            rects = np.array(box).astype(int)
            s = rects[:2]
            e = rects[:2] + rects[2:]
            image = cv2.rectangle(image, s, e, color, box_thickness)

        if draw_text:
            org = (50,150)
            image = cv2.putText(image, frames_fldr, org, font,
                   fontScale, color, text_thickness, cv2.LINE_AA)

        out_fn = f"{output_folder}/{frame['img']}"

        # prints out images that were not saved & had bounding boxes
        if len(bboxes) > 0 and not cv2.imwrite(out_fn, image):
            print(out_fn)

        # shows image if needed
        if show_img and i%show_img ==0:
            print(fn)
            plt.imshow(image)
            plt.show()

