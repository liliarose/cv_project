import cv2
import os 
import json 
import argparse

def sec2frame(seconds, fps):
    return round(seconds*fps)

def get_vid_meta(filename):
    video = cv2.VideoCapture(filename)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps

    return fps, duration, frame_count


def process_single(annot_fn, fps, fout, img_folder):
    with open(annot_fn) as f:
        contents = json.load(f)

    annot = contents['metadata']
    attr = contents['attribute']

    # not doing anything with the temporal
    # section.......
    obj_seg = []
    for d in annot.values():
        if len(d['z']) == 1:
            obj_seg.append(d)
    # just using object present & object id for this....
    name2i_attr = {d['aname']: i for i, d in attr.items()}
    object_present = name2i_attr['object_present']
    object_id = name2i_attr['object_id']
    object_label = name2i_attr['object_label']

    # coco starting out
    coco_dict = { 'annotations': [ ]}

    # just gonna use object present & object id
    cat2id = {}
    id_count = 0
    dropped_items = []
    for i, obj in enumerate(obj_seg):
        av = obj['av']
        # ==2 checks for rectangle
        if (object_label not in av  and object_present not in av ) or obj['xy'][0] != 2:
            if len(dropped_items) == 0:
                dropped_items.append(name2i_attr)
            dropped_items.append(obj)
            continue
        if av.get(object_label, None):
            cat = av[object_label].strip()
        else:
            cat = av[object_present].strip()

        c_id = av.get(object_id, '0').strip()
        # adding to categories.....if needed
        if (cat, c_id) not in cat2id:
                cat2id[(cat, c_id)] = id_count
                id_count +=1

        coco_dict['annotations'].append({
                'id': i,
                # we need keypoint or segmentation for some reason....
                'keypoints': None,
                'category_id': cat2id[(cat, c_id)],
                "image_id": sec2frame(obj['z'][0], fps),
                'bbox': obj['xy'][1:],
                'area': obj['xy'][-1]*obj['xy'][-2]

        })

    imgs = sorted(os.listdir(img_folder))
    paths = [f'{img_folder}/{f}' for f in imgs]
    assert(int(paths[-1].split('.jpg')[0].split('-')[-1]) == len(paths))
    coco_dict['images'] = [{'id':i, 'file_name':fn} for i, fn in enumerate(paths)]
    coco_dict['categories'] = [{'id': i, 'name': f'{cat}_{im}', 'supercategory':cat}
                               for (cat, im), i in cat2id.items()]
    with open(fout, 'w') as f:
        json.dump(coco_dict, f)

    return dropped_items


def main(args):

    prefixes = [f for f in os.listdir(frames) if os.path.isdir(f'{args.frames}/{f}')]
    dropped_things = {}
    annot_folder = 'coco_files'
    new_prefixes = []
    for p in prefixes:
        new_p = f'{args.folder}/{p}'
        if os.path.isfile(new_p + '.json') and os.path.isfile(new_p + '.mp4'):
            print('Processing', new_p)
            fps, _, _ = get_vid_meta(new_p + '.mp4')
            fout = f'{annot_folder}/{p}_coco.json'
            dropped_items = process_single(new_p+'.json', fps, fout, f'{frames}/{p}')
            if len(dropped_items) > 0:
                dropped_things[p] = dropped_items
            else:
                new_prefixes.append(p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', help='folder with the annotations and videos; annotations & videos should have the same names')
    parser.add_argument('frames', help='folder with folders of video frames')
    parser.add_argument('--output_folder', '-o', help='folder to output the coco annotations', default='.')
    args = parser.parse_args()
    main(args)




