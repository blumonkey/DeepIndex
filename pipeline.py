import subprocess
import tempfile
import os
from glob import glob
import re
import argparse


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('-([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def DeepIndex(filename):
    file_code = os.path.basename(filename)
    base = file_code.split('.', 1)[0]
    temp_dir = tempfile.mkdtemp(base + '_files')

    subprocess.call(['pdftoppm', '-jpeg', '-r', '72', filename, temp_dir +'/' + base])

    jpg_images = glob(temp_dir+'/'+base+'-*.jpg')
    jpg_images = natural_sort(jpg_images)

    # Call the model and retrieve BBxs and Sections

    # convert blah-1.jpg -crop widthxheight+x+y out.jpg
    # tesseract out.jpg stdout --oem 1  -l eng
    AllBbox = []

    for bbox, ctype, pageNum in AllBbox:
        subprocess.call(['convert', temp_dir+'/'+base+'-'+pageNum+'.jpg', '-crop',
                         '{}x{}+{}+{}'.format(bbox.width, bbox.height, bbox.xmin, bbox.xmax), 'out.jpg'])
        subprocess.call(['tesseract', 'out.jpg', 'out',
                         '--oem', '1', '-l', 'eng'])
        with open('out.txt', 'r') as myfile:
            ocr_text = myfile.read().replace('\n', ' ').strip()
        print(ctype+': ' + ocr_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DeepIndex Application')
    parser.add_argument('filename', help='PDF file to be processed')

    args = parser.parse_args()
    print(args)

    DeepIndex(args.filename)