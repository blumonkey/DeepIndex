#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import subprocess

import errno

import shutil
from bs4 import BeautifulSoup
import Levenshtein
import difflib
from glob import glob
import tempfile
import argparse
import os
import re

Basic_Sections = ['ABSTRACT', 'CCS CONCEPTS', 'KEYWORDS', 'REFERENCES']


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('-([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


class BBGenerator(object):

    def __init__(self):
        self.foundTitle = False

    def check_write_MetaData(self, block, text, metadata, fp):
        # print('{%s}' % text)
        for sec in Basic_Sections:
            if text == sec:
                print('Here! ' + sec, file=fp)
                text_tag = block.find('TEXT')
                print('x: %s' % text_tag['x'], file=fp)
                print('y: %s' % text_tag['y'], file=fp)
                print('h: %s' % text_tag['height'], file=fp)
                print('w: %s' % text_tag['width'], file=fp)

        title = metadata['title']
        if not self.foundTitle and Levenshtein.distance(title, text) / float(len(text)) < 1.0:
            # print(title)
            # print(text)

            print('Here! ' + title, file=fp)
            x = float(block.find('TEXT')['x'])
            y = float(block.find('TEXT')['y'])
            h = float(block.find('TEXT')['height'])
            w = float(block.find('TEXT')['width'])
            text_tag = block.find('TEXT')
            # print(text_tag.text)
            # print(text_tag.next_sibling)
            while True:
                next_tag = text_tag.next_sibling
                if next_tag is None:
                    break
                # print(next_tag.text)
                # print('================================================================')
                s = difflib.SequenceMatcher(None, title, text)
                if sum(n for i,j,n in s.get_matching_blocks()) / float(len(text)) > 0.95:
                    text_tag = next_tag
                    h += float(text_tag['height'])
                    w = max(w, float(text_tag['width']))
                else:
                    break

            print('x: %f' % x, file=fp)
            print('y: %f' % y, file=fp)
            print('h: %f' % h, file=fp)
            print('w: %f' % w, file=fp)
            self.foundTitle = True

        sections = metadata['sections']
        for section in sections:
            # print(section)
            words = text.split()
            from2 = ' '.join(words[1:])
            # print(text)
            # print(from2)
            if text.startswith(section) or from2.startswith(section):
                print('Here! ' + section, file=fp)
                text_tag = block.find('TEXT')
                print('x: %s' % text_tag['x'], file=fp)
                print('y: %s' % text_tag['y'], file=fp)
                print('h: %s' % text_tag['height'], file=fp)
                print('w: %s' % text_tag['width'], file=fp)



    def __get_ground_truth(self, pdf, metadata, base):
        temp_dir = tempfile.mkdtemp(base + '_files')
        try:
            pdf_prefix = metadata['body']

            print(temp_dir)
            subprocess.call(['pdftk', pdf, 'burst', 'output', temp_dir +'/' + pdf_prefix +'-%d.pdf'])
            pdf_pages = glob(temp_dir+'/'+pdf_prefix+'-*.pdf')

            pdf_pages = natural_sort(pdf_pages)

            log_file  = open(os.path.dirname(pdf)+'/log-'+pdf_prefix+'.txt', 'w')

            for pdf_page in pdf_pages:
                print(pdf_page, file=log_file)
                subprocess.call(['pdf2xml', '-blocks', pdf_page])
                with open(pdf_page[:-3]+'xml', 'r') as fp:
                    xml_soup = BeautifulSoup(fp, features='xml')
                    pages = xml_soup.findAll('PAGE')
                    for page in pages:
                        blocks = page.findAll('BLOCK')
                        for block in blocks:
                            text = block.get_text(separator=' ')
                            # print(text)
                            self.check_write_MetaData(block, text, metadata, log_file)
                            # print('=============================')

            log_file.close()
        finally:
            try:
                shutil.rmtree(temp_dir)  # delete directory
            except OSError as exc:
                if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                    raise  # re-raise exception


    def get_bb_from_metadata(self, pdf, metadata, base):
        with open(metadata, 'r') as fp:
            metadata = json.load(fp)
        self.__get_ground_truth(pdf, metadata, base)
        self.foundTitle = False  # for the next file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Bounding Boxes for files created by LatexGenerator')
    parser.add_argument('batch', help='Directory of all files, main-*.pdf and meta-*.json')

    args = parser.parse_args()
    print(args)

    myObj = BBGenerator()
    files = glob(args.batch+'/main-*.pdf')
    pattern = re.compile('main-(.*).pdf')
    for file in files:
        file_code = os.path.basename(file)
        base = pattern.search(file_code).group(1)
        print(base)
        myObj.get_bb_from_metadata(args.batch+'/'+'main-%s.pdf' % base, args.batch+'/'+'meta-%s.json' % base, base)