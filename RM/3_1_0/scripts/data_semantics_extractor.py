#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
data_semantics_extractor.py

Extracts S3Model 3.1.0 (and later) data and creates RDF triples in RDF/XML
This script must be executed after the dm_semantics_extractor.py script.

Copyright (C) 2016 - 2018 Data Insights, Inc., All Rights Reserved.
"""
import os
import sys
import re
from random import randint
from xml.sax.saxutils import escape

from lxml import etree

nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
        'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
        'dct':'http://purl.org/dc/terms/',
        'owl':'http://www.w3.org/2002/07/owl#',
        'vc':'http://www.w3.org/2007/XMLSchema-versioning',
        's3m':'https://www.s3model.com/ns/s3m/'}

dest = None
filename = None
tree = None

def parse_el(element):
    global dest
    global filename
    global tree


    for child in element.getchildren():
        if child.tag is not etree.Comment:
            if 'ms-' not in child.tag:
                c_name = child.tag.replace('{https://www.s3model.com/ns/s3m/}','s3m:')
                nodepath = tree.getelementpath(child).replace('{https://www.s3model.com/ns/s3m/}','s3m:')
                dest.write("<rdf:Description rdf:about='data/"+filename+nodepath+"'>\n")
                dest.write("  <rdfs:domain rdf:resource='data/"+filename+"'/>\n")
                nodepath = tree.getelementpath(child).replace('{https://www.s3model.com/ns/s3m/}','s3m:')
                dest.write("  <rdf:subPropertyOf rdf:resource='"+nodepath+"'/>\n")
                if child.text is not None:
                    dest.write("  <rdf:value>"+escape(child.text)+"</rdf:value>\n")
                dest.write("</rdf:Description>\n\n")
            else:
                c_name = child.tag.replace('{https://www.s3model.com/ns/s3m/}','s3m:')
                nodepath = tree.getelementpath(child).replace('{https://www.s3model.com/ns/s3m/}','s3m:')                
                dest.write("<rdf:Description rdf:about='data/"+filename+nodepath+"'>\n")
                dest.write("  <rdfs:domain rdf:resource='data/"+filename+"'/>\n")
                dest.write("  <rdf:type rdf:resource='"+c_name.replace('ms-','mc-')+"'/>\n")
                dest.write("</rdf:Description>\n\n")

            parse_el(child)


def main():
    global dest
    global filename
    global tree

    header = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
  xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'
  xmlns:owl="http://www.w3.org/2002/07/owl#"
  xmlns:dc='http://purl.org/dc/elements/1.1/'
  xmlns:ehr='http://www.S3Model.org/xmlns/ehr'
  xmlns:s3m='https://www.s3model.com/ns/s3m/'>
\n"""
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dct':'http://purl.org/dc/terms/',
            'owl':'http://www.w3.org/2002/07/owl#',
            'vc':'http://www.w3.org/2007/XMLSchema-versioning',
            's3m':'https://www.s3model.com/ns/s3m/'}

    parser = etree.XMLParser(ns_clean=True, recover=True)

    files = os.listdir('data')
    for filename in files:
        if filename[-4:] == '.xml':
            dest = open(os.path.join('rdf', filename.replace('.xml', '.rdf')), 'w')
            dest.write(header)

            print('\n\nProcessing: ', os.path.join('data', filename))
            src = open(os.path.join('data', filename), 'r')
            tree = etree.parse(src, parser)
            root = tree.getroot()

            dmid = root.tag.replace('{https://www.s3model.com/ns/s3m/}','')

            # create triple for the file link to the DM
            dest.write("\n<rdf:Description rdf:about='data/"+filename+"'> <!-- The document unique path/filename -->\n")
            dest.write("  <rdf:domain rdf:resource='https://dmgen.s3model.com/dmlib/"+dmid+".xsd'/>\n")
            dest.write("</rdf:Description>\n\n")

            parse_el(root)

            dest.write('\n</rdf:RDF>\n')
            dest.close()


if __name__ == '__main__':
    main()
    print("\n\nDone! \nCreated RDF/XML files in the rdf directory.\n\n")
    sys.exit(0)
