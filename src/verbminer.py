#!/usr/bin/env python
# coding: utf-8

from nltk import word_tokenize, Text, pos_tag
import sys
import csv

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
 
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'ascii'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def categorize(tags):
    ctags = {}
    for tag in tags:
        w = tag[0]
        t = tag[1]
        
        if t.startswith('VB') or t.startswith('JJ') or t.startswith('RB') or t.startswith('N'):
            if t not in ctags:
                ctags[t] = {}
            ctags[t][w] = 1
            
    for key in ctags.keys():
        ctags[key] = ctags[key].keys()
    return ctags

def map_to_csv(path, hashmap):
    output = open(path, 'wb')
    wr = csv.writer(output)
    
    line = []
    maxi = 0
    for key in sorted(hashmap.keys()):
        line.append(key)
        if len(hashmap[key]) > maxi: maxi = len(hashmap[key])
    wr.writerow(line)
    
    for i in range(maxi):
        line = []
        for key in sorted(hashmap.keys()):
            if len(hashmap[key]) > i: line.append(hashmap[key][i])
            else: line.append("")
        wr.writerow(line)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input = sys.argv[1]
    else:
        input = '../test/test.pdf'
        
    print 'input :', input
    print 'building index...'
    i = input.rindex('.')
    output = input[:i] + '_out' + '.csv'
    
    if input[-4:] == ".pdf":
        text = convert_pdf_to_txt(input)
    elif input[-4:] == ".txt":
        with open(input, 'r') as f:
            text = f.read()
    else:
        print 'file format', input[-4:], 'is not supported'
        sys.exit()
        
    tokens = word_tokenize(text)
    text = Text(tokens)
    tags = pos_tag(text)

    ctags = categorize(tags)
    
    print '---------'
    for key in sorted(ctags.keys()):
        print key, ':', len(ctags[key])
    print '---------'

    print 'output :', output
    map_to_csv(output, ctags)

    print 'done'
