import subprocess
import tempfile
import os
from glob import glob
import re
import argparse


import numpy as np
import utils
from PIL import Image
import math

from google.cloud import vision
from google.cloud.vision import types
import shutil

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('-([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def DeepIndex(filename):
    file_code = os.path.basename(filename)
    base = file_code.split('.', 1)[0]
    temp_dir = tempfile.mkdtemp(base + '_files')

    subprocess.call(['pdftoppm', '-jpeg', '-r', '72', filename, os.path.join(temp_dir, base) ])

    jpg_images = glob(temp_dir+'/'+base+'-*.jpg')
    jpg_images = natural_sort(jpg_images)

    # Call the model and retrieve BBxs and Sections
    client = vision.ImageAnnotatorClient()
    AllBbox = []

    for img_path in jpg_images:
        image = Image.open(img_path)
        image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)

        sess, tensor_dict,image_tensor = utils.initialize()
        indices = utils.findIndex(image_np_expanded, 0.5, sess, tensor_dict,image_tensor)
        AllBbox.append(indices)

    tot_pages = len(jpg_images)
    pageNum = 1
    imgNum = 1
    if tot_pages >= 10:
    	placeholder = '%02d'
    else:
    	placeholder = '%d'
    for ctype, bboxes in AllBbox:
        for o_class, bbox in zip(ctype, bboxes):
            subprocess.call(['convert', temp_dir+'/'+ base + ('-' + placeholder % pageNum)+'.jpg', '-crop',
                             '{:d}x{:d}+{:d}+{:d}'.format(int(math.ceil(bbox[3])), int(math.ceil(bbox[2])),
                                                          int(math.floor(bbox[1])), int(math.floor(bbox[0]))), os.path.join(temp_dir, 'out-%d.jpg' % imgNum)])

            with open(os.path.join(temp_dir, 'out-%d.jpg' % imgNum), 'rb') as image:
                content = image.read()

            img = types.Image(content=content)
            res = client.text_detection(image=img)
            try:
                text = res.text_annotations[0].description
                if o_class == 1:
                    o_class = 'TITLE'
                else:
                    o_class = 'SECTION'
                print 'Pg: ' + str(pageNum)
                print('Class: {}, Text: {}'.format(o_class, text))
            except:
                pass
            imgNum += 1
        pageNum += 1

    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DeepIndex Application')
    parser.add_argument('filename', help='PDF file to be processed')

    args = parser.parse_args()
    print(args)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/blumonkey/Acads/Winter 2018/617/DeepIndex-0de2be869214.json"
    DeepIndex(args.filename)