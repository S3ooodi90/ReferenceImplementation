#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
rm_semantics_extractor.py

Extracts the semantics from S3Model RM and creates RDF triples in RDF/XML named the same as the input file with a .rdf extension in place of the .xsd extension.

    Copyright (C) 2016 - 2018 Data Insights, Inc., All Rights Reserved.

"""
import os
import sys
import re
from lxml import etree

def main(rmfile):
    rootdir = '.'
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dct':'http://purl.org/dc/terms/',
            'owl':'http://www.w3.org/2002/07/owl#',
            'vc':'http://www.w3.org/2007/XMLSchema-versioning',
            's3m':'https://www.s3model.com/ns/s3m/'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    #owl_info = etree.XPath("//xs:annotation/xs:appinfo/owl:Ontology", namespaces=nsDict)
    rdf_info = etree.XPath("//xs:annotation/xs:appinfo/rdf:Description", namespaces=nsDict)
    rdffile = rmfile[:-4] + '.rdf'
    print(rdffile)
    dest = open(rdffile, 'w')

    dest.write("""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n""")

    src = open(rmfile, 'r')
    tree = etree.parse(src, parser)
    root = tree.getroot()

    #owl = owl_info(root)
    rdf = rdf_info(root)

    #for r in owl:
        #dest.write('  '+etree.tostring(r).decode('utf-8').strip()+'\n')

    for r in rdf:
        dest.write('  '+etree.tostring(r).decode('utf-8').strip()+'\n')

    dest.write('</rdf:RDF>\n')
    dest.close()
    return(rdffile)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('\nYou must include a path and filename to the RM on the commandline. \n\n')
        sys.exit(1)
    else:
        rmfile = sys.argv[1:][0]    
    rdffile = main(rmfile)
    print("\n\nDone! \nCreated: " + rdffile + "\n\n")
    sys.exit(0)
