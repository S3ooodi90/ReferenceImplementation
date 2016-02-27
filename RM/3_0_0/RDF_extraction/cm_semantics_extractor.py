#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
ccd_semantics_extractor.py

Extracts the semantics from S3Model 2.4.6 (and later) CCDs and creates RDF triples in RDF/XML
This script must be executed before the data_semantics_extractor.py script.


    Copyright (C) 2014 Timothy W. Cook tim@S3Model.org

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import os
import sys
import re
from lxml import etree

nsDict = {'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'owl':'http://www.w3.org/2002/07/owl#',
            'dc':'http://purl.org/dc/elements/1.1/',
            'sawsdl':'http://www.w3.org/ns/sawsdl',
            'sawsdlrdf':'http://www.w3.org/ns/sawsdl#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#'}

def main():
    rootdir = '.'
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dc':'http://purl.org/dc/elements/1.1/'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    about = etree.XPath("//xs:complexType/xs:annotation/xs:appinfo/rdf:Description", namespaces=nsDict)
    md = etree.XPath("//rdf:RDF/rdf:Description", namespaces=nsDict)
    dest = open('rdf/ccd_semantics.rdf', 'w')

    dest.write("""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'
xmlns:dc='http://purl.org/dc/elements/1.1/'
xmlns:tdv='http://www.S3Model.org/xmlns/tdv'
xmlns:S3Model2='http://www.S3Model.org/xmlns/S3Model2'>

\n""")

    for folder, subs, files in os.walk(rootdir):
        for filename in files:
            if filename[-4:] == '.xsd' and filename.startswith('ccd-'):
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
    print("\n\nDone! \nCreated: rdf/ccd_semantics.rdf\n\n")
    sys.exit(0)
