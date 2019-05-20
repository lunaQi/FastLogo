import json
import os

import cv2

dataset = {
    'licenses': [],
    'info': [],
    'categories': [],
    'images': [],
    'annotations': []
}

classes = ['adidas', 'aldi', 'apple', 'becks', 'bmw',
    'carlsberg', 'chimay', 'cocacola', 'corona', 'dhl',
    'erdinger', 'esso', 'fedex', 'ferrari', 'ford',
    'fosters', 'google', 'guiness', 'heineken', 'HP',
    'milka', 'nvidia', 'paulaner', 'pepsi', 'rittersport',
    'shell', 'singha', 'starbucks', 'stellaartois', 'texaco',
    'tsingtao', 'ups']

for i, cls in enumerate(classes, 1):  #指定索引的起始值从1开始
    dataset['categories'].append({
        'id': i,
        'name': cls,
        'supercategory': 'logo'
    })

def get_category_id(cls):
    for category in dataset['categories']:
        if category['name'] == cls:
            return category['id']

j = 1
with open('files/flickr_logo_32_vali_set_annotation.txt', 'r') as f:
    img_number = 0
    file_name_dict = {}
    lines = [line for line in f.readlines() if line.strip()]
    for i, line in enumerate(lines):
        parts = line.strip().split()
        fn = parts[0]
        cls = parts[1]
        x1 = int(parts[2])
        y1 = int(parts[3])
        width = int(parts[4])
        height = int(parts[5])
        if cls == 'no-logo':
            continue
        img_dir = os.path.join('files/jpg', cls)
        im = cv2.imread(os.path.join(img_dir, fn))
        img_height, img_width, _ = im.shape
        if fn in file_name_dict:
            img_id = file_name_dict[fn]
        else:
            img_number = img_number + 1
            file_name_dict[fn] = img_number
            img_id = file_name_dict[fn]
        dataset['images'].append({
            'coco_url': '',
            'date_captured': '',
            'file_name': fn,
            'flickr_url': '',
            'id': img_id,
            'license': 0,
            'width': img_width,
            'height': img_height
        })

        dataset['annotations'].append({
            'area': width * height,
            'bbox': [x1, y1, width, height],
            'category_id': get_category_id(cls),
            'id': j,
            'image_id': img_id,
            'iscrowd': 0,
            'segmentation': []
        })
        j += 1

folder = os.path.join('files/', 'annotations')
if not os.path.exists(folder):
    os.makedirs(folder)
json_name = os.path.join('files', 'annotations/val.json')
with open(json_name, 'w') as f:
    json.dump(dataset, f)
