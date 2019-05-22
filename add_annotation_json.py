import json
import os

root_path = 'files/annotations'
target_path = 'files/finalanno'

if not os.path.exists(target_path):
    os.makedirs(target_path)

dataset = json.load(open(os.path.join(root_path, 'train.json')))
data = json.load(open(os.path.join(root_path, 'val.json')))

image_id = dataset['images'][-1]['id']
anno_id = dataset['annotations'][-1]['id']
#print(len(dataset['images']))
#print(len(dataset['annotations']))
#print(len(data['images']))
#print(len(data['annotations']))
def get_annos(image_id):
    annos = []
    for anno in data['annotations']:
        if anno['image_id'] == image_id:
            annos.append(anno)
            #data['annotations'].remove(anno)
    return annos

for img in data['images']:
    orig_image_id = img['id']

    dataset['images'].append({
        'coco_url': '',
        'date_captured': '',
        'file_name': img['file_name'],
        'flickr_url': '',
        'id': image_id + 1,
        'license': 0,
        'width': img['width'],
        'height': img['height']
    })
    '''从字典列表中取出特定键值的所有元素'''
    for anno in get_annos(orig_image_id):
        dataset['annotations'].append({
            'area': anno['area'],
            'bbox': anno['bbox'],
            'category_id': anno['category_id'],
            'id': anno_id + 1,
            'image_id': image_id + 1,
            'iscrowd': 0,
            'segmentation': []
        })
        anno_id = anno_id + 1
    image_id = image_id + 1

json_name = os.path.join(target_path, 'train.json')
with open(json_name, 'w') as f:
    json.dump(dataset, f)
print(len(dataset['images']))
print(len(dataset['annotations']))