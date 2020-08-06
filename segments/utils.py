import os
from io import BytesIO
import requests
import json
from tqdm import tqdm

from PIL import Image

import numpy as np


def load_image(url):
    image = Image.open(BytesIO(requests.get(url).content))
    return image

def load_segmentation_bitmap(url):
    def extract_segmentation_bitmap(segmentation_bitmap):
        segmentation_bitmap = np.array(segmentation_bitmap)
        segmentation_bitmap[:,:,3] = 0
        segmentation_bitmap = segmentation_bitmap.view(np.uint32).squeeze(2)
        segmentation_bitmap = Image.fromarray(segmentation_bitmap)
        return segmentation_bitmap

    segmentation_bitmap = Image.open(BytesIO(requests.get(url).content))
    segmentation_bitmap = extract_segmentation_bitmap(segmentation_bitmap)
    return segmentation_bitmap

def bitmap2file(bitmap, is_segmentation_bitmap=False):
    if is_segmentation_bitmap:
        bitmap2 = np.copy(bitmap)
        bitmap2 = bitmap2[:, :, None].view(np.uint8)
        bitmap2[:, :, 3] = 255
    else:
        bitmap2 = bitmap
        
    file = BytesIO()
    Image.fromarray(bitmap2).save(file, 'PNG')
    return file

def export_dataset(dataset, export_format='coco'):
    from pycocotools import mask
    from skimage.measure import regionprops

    def get_bbox(binary_mask):
        regions = regionprops(np.uint8(binary_mask))
        if len(regions) == 1:
            bbox = regions[0].bbox
            return bbox
        else:
    #         assert False
            return False

    # https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch/#coco-dataset-format

    if export_format != 'coco':
        print('Supported export formats: coco')
        return

    info = {
        'description': dataset.release['dataset']['name'],
        # 'url': 'https://segments.ai/test/test',
        'version':  dataset.release['name'],
        # 'year': 2020,
        # 'contributor': 'Segments.ai',
        # 'date_created': '2020/09/01'
    }

    # licenses = [{
    #     'url': 'http://creativecommons.org/licenses/by-nc-sa/2.0/',
    #     'id': 1,
    #     'name': 'Attribution-NonCommercial-ShareAlike License'
    # }]

    categories = dataset.categories
    # for i, category in enumerate(dataset.project_info['label_taxonomy']):
    #     categories.append({
    #         'id': i+1,
    #         'supercategory': 'object',
    #         'name': category
    #     })

    images = []
    annotations = []

    annotation_id = 1
    for i in tqdm(range(len(dataset))):        
        sample = dataset[i]
    #     print(sample)
        
        image_id = i+1
        images.append({        
            'id': image_id,
            # 'license': 1,
            'file_name': sample['file_name'],
            'height': sample['image'].size[1],
            'width': sample['image'].size[0],
    #         'date_captured': "2013-11-14 17:02:52",
    #         'coco_url': "http://images.cocodataset.org/val2017/000000397133.jpg",
    #         'flickr_url': "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",        
        })
        
        for instance in sample['annotations']:
            category_id = instance['category_id']
                
            instance_mask = np.array(sample['segmentation_bitmap'], np.uint32) == instance['id']
            bbox = get_bbox(instance_mask)
            if not bbox:
                continue
                
            y0, x0, y1, x1 = bbox
            # rle = mask.encode(np.asfortranarray(instance_mask))
            rle = mask.encode(np.array(instance_mask[:,:,None], dtype=np.uint8, order='F'))[0] # https://github.com/matterport/Mask_RCNN/issues/387#issuecomment-522671380
    #         instance_mask_crop = instance_mask[y0:y1, x0:x1]
    #         rle = mask.encode(np.asfortranarray(instance_mask_crop))
    #         plt.imshow(instance_mask_crop)
    #         plt.show()
            
            area = int(mask.area(rle))
            rle['counts'] = rle['counts'].decode('ascii')
            
            annotations.append({
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
                'bbox': [x0, y0, x1-x0, y1-y0],
    #             'bbox_mode': BoxMode.XYWH_ABS,
                'segmentation': rle,
                'area': area,
                'iscrowd': 0,
            })
            annotation_id += 1
            
    json_data = {
        'info': info,
        # 'licenses': licenses,
        'categories': categories,
        'images': images,
        'annotations': annotations    
    #     'segment_info': [] # Only in Panoptic annotations
    }

    file_name = '{}_coco.json'.format(os.path.splitext(os.path.basename(dataset.release_file))[0])
    with open(file_name, 'w') as f:
        json.dump(json_data, f)

    print('Exported to {}.'.format(file_name))
    return file_name, dataset.image_dir
