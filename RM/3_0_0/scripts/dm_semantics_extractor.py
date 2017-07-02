#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
dm_semantics_extractor.py

Extracts the semantics from S3Model DMs and creates RDF triples in RDF/XML
This script must be executed before the data_semantics_extractor.py script.

    Copyright (C) 2016 Data Insights, Inc., All Rights Reserved.

"""
import os
import sys
import re
from lxml import etree

nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
        'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
        'dct':'http://purl.org/dc/terms/',
        'owl':'http://www.w3.org/2002/07/owl#',
        'vc':'http://www.w3.org/2007/XMLSchema-versioning',
        's3m':'http://www.s3model.com/ns/s3m/'}

def main():
    rootdir = '.'
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dct':'http://purl.org/dc/terms/',
            'owl':'http://www.w3.org/2002/07/owl#',
            'vc':'http://www.w3.org/2007/XMLSchema-versioning',
            's3m':'http://www.s3model.com/ns/s3m/'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    about = etree.XPath("//xs:annotation/xs:appinfo/rdf:Description", namespaces=nsDict)
    md = etree.XPath("//rdf:RDF/rdf:Description", namespaces=nsDict)
    dest = open('rdf/DM_semantics.rdf', 'w')

    dest.write("""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
\n""")

    for folder, subs, files in os.walk(rootdir):
        for filename in files:
            if filename[-4:] == '.xsd' and filename.startswith('dm-'):
                src = open(os.path.join(folder, filename), 'r')
                print('Processing: ', os.path.join(folder, filename))
                tree = etree.parse(src, parser)
                root = tree.getroot()

                rdf = about(root)
                for m in md(root):
                    dest.write('    '+etree.tostring(m).decode('utf-8')+'\n')

                for r in rdf:
                    dest.write('    '+etree.tostring(r).decode('utf-8')+'\n')

    dest.write('</rdf:RDF>\n')
    dest.close()


if __name__ == '__main__':
    main()
    print("\n\nDone! \nCreated: rdf/DM_semantics.rdf\n\n")
    sys.exit(0)
