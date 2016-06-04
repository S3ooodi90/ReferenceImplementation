#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
rm_rdf_extractor.py

Extracts the semantics from S3Model RM and creates RDF triples in RDF/XML

    Copyright (C) 2014 Timothy W. Cook, All Rights Reserved.

"""
import os
import sys
import re
from lxml import etree

def main():
    rootdir = '.'
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dct':'http://purl.org/dc/terms/',
            'owl':'http://www.w3.org/2002/07/owl#',
            'vc':'http://www.w3.org/2007/XMLSchema-versioning',
            'sch':'http://purl.oclc.org/dsdl/schematron',
            's3m':'http://www.s3model.com/rm'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    owl_info = etree.XPath("//xs:annotation/xs:appinfo/owl:Ontology", namespaces=nsDict)
    rdf_info = etree.XPath("//xs:annotation/xs:appinfo/rdf:Description", namespaces=nsDict)
    dest = open('rdf/rm_semantics.rdf', 'w')

    dest.write("""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n""")

    src = open('../s3model_1_0_0.xsd', 'r')
    tree = etree.parse(src, parser)
    root = tree.getroot()

    owl = owl_info(root)
    rdf = rdf_info(root)

    for r in owl:
        dest.write('  '+etree.tostring(r).decode('utf-8').strip()+'\n')

    for r in rdf:
        dest.write('  '+etree.tostring(r).decode('utf-8').strip()+'\n')

    dest.write('</rdf:RDF>\n')
    dest.close()


if __name__ == '__main__':
    main()
    print("\n\nDone! \nCreated: rdf/rm_semantics.rdf\n\n")
    sys.exit(0)
