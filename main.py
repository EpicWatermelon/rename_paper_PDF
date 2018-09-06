#-*- coding: utf-8 -*-
import os
import re
import shutil

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def GetPDFName(root):
    path = root
    fp = open(path,'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)
    doc.set_parser(parser)

    doc.initialize('')

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    page = doc.get_pages()
    interpreter.process_page(next(page))
    layout = device.get_result()
    text = []
    for out in layout:
        if isinstance(out, LTTextBoxHorizontal):
            results = out.get_text()
            if re.match(r'\w\w', results) or re.match(r'\w\s\w\w', results):
                text.append(results)
    return text[0]

def RenamePDF():
    list = os.listdir(root)
    if not list:
        raise print('There Is No PDF In This File')

    dest_path = './pdf_renamed'
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        print('dir created')

    for pdf in list:
        path = root + pdf
        title = GetPDFName(path)
        title = title.replace("\n", " ")
        print('proccessing the pdf')
        for i in i_dont_want_these_chars:
            title = title.replace(i,"")
        if title[-1] == ' ':
            title = title[:-1]

        shutil.move(path,'./pdf_renamed/'+title+'.pdf')
    print('all finished!')

i_dont_want_these_chars = ['/','\\',':','*','?','<','>','|']
root = './pdf/'

if __name__ == '__main__':
    RenamePDF()