"""
Extracts S3Model 3.0.0 (and later) data and creates RDF triples in RDF/XML
Copyright (C) 2016 Data Insights, Inc., All Rights Reserved.
"""
import os
import sys
import re
from random import randint
from xml.sax.saxutils import escape

from lxml import etree

from s3m.settings import MEDIA_ROOT, DATA_LIB

def parse_el(element, dest, filename, tree):

    for child in element.getchildren():
        print('0: ', child)
        if child.tag is not etree.Comment:
            if 'ms-' not in child.tag:
                print('1: ', child.tag)
                c_name = child.tag.replace('{http://www.s3model.com/ns/s3m/}','s3m:')
                dest.write("<rdf:Description rdf:about='data/" + filename + tree.getpath(child) + "'>\n")
                dest.write("  <rdfs:domain rdf:resource='data/" + filename + "'/>\n")
                dest.write("  <rdf:subPropertyOf rdf:resource='" + tree.getpath(element) + "'/>\n")
                if child.text is not None:
                    dest.write("  <rdf:value>" + escape(child.text) + "</rdf:value>\n")
                else:
                    dest.write("  <rdf:value></rdf:value>\n")
                dest.write("</rdf:Description>\n\n")
            else:
                print('2: ', child.tag)
                c_name = child.tag.replace('{http://www.s3model.com/ns/s3m/}','s3m:')
                dest.write("<rdf:Description rdf:about='data/" + filename + tree.getpath(child) + "'>\n")
                dest.write("  <rdfs:domain rdf:resource='data/" + filename + "'/>\n")
                dest.write("  <rdf:type rdf:resource='" + c_name.replace('ms-', 'mc-') + "'/>\n")
                dest.write("</rdf:Description>\n\n")

                parse_el(child, dest, filename, tree)


def rdfGen(dmd, dm):

    header = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
  xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'
  xmlns:owl="http://www.w3.org/2002/07/owl#"
  xmlns:dc='http://purl.org/dc/elements/1.1/'
  xmlns:s3m='http://www.s3model.com/ns/s3m/'>\n"""

    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dc':'http://purl.org/dc/elements/1.1/',
            's3m': 'http://www.s3model.com/ns/s3m/'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    datapath = os.path.join(DATA_LIB,dmd.csv_file.url.strip('.csv'))

    files = os.listdir(datapath)
    for filename in files:
        if filename[-4:] == '.xml':
            dest = open(os.path.join(datapath,filename.replace('.xml', '.rdf')), 'w')
            dest.write(header)
            src = open(os.path.join(datapath, filename), 'r')
            tree = etree.parse(src, parser)
            root = tree.getroot()
            # fill in the details :-)
            dmid = root.tag.replace('{http://www.s3model.com/ns/s3m/}','')
            # create triple for the file link to DM
            dest.write("\n<rdf:Description rdf:about='" + dmid + "/data/" + filename + "'>\n")
            dest.write("  <s3m:isInstanceOf rdf:resource='http://dmgen.s3model.com/dmlib/" + dmid + ".xsd'/>\n")
            dest.write("</rdf:Description>\n\n")
            entry = root.getchildren()[0]
            # create triple for Entry
            entry_el = entry.tag.replace('{http://www.s3model.com/ns/s3m/}','s3m:')
            dest.write("<rdf:Description rdf:about='" + dmid + "/data/" + filename + "/" + dmid + "/" + entry_el + "'>\n")
            dest.write("  <s3m:isCMSOf rdf:resource='" + entry_el.replace('ms-','mc-') + "'/>\n")
            dest.write('</rdf:Description>\n\n')

            parse_el(entry, dest, filename, tree)




            dest.write('\n</rdf:RDF>\n')
            dest.close()

    return
