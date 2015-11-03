#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
S3Model_Semantics.py   Copyright (C) 2014 Timothy W. Cook timothywayne.cook@gmail.com

See: http://www.srdc.com.tr/projects/salus/blog/?p=189

This tool collects the semantics from your S3Models and applies those semantics to your XML data. It does so by creating a RDF/XML triples file for each file. These files are ready to be uploaded to your favorite Triple Store or imported by your visualization tool.

The semantics generator uses a configuration file to find your data, concept models and reference models. It does not check for the S3Model.owl base ontology or any XML catalog files.

The configuration file must be located in the same directory as S3Model_Semantics.py it is named: config.ini

Edit the config.ini file with a text editor to set the proper paths for your installation.
The default config.ini file looks like this:

    [PATHS]
    RM_PATH = rm_lib/
    CM_PATH = cm_lib/
    XML_PATH = xml_data/
    RDF_PATH = rdf_data/

This is what each option means:

    RM_PATH - this is where your reference model schema(s) is/are located.
    CM_PATH - this is where your concept model schema(s) is/are located.
    XML_PATH - this is the location of your XML data instances.
    RDF_PATH - this is the output directory to write your RDF files into.

"""
import os
import sys
import re
from random import randint
from xml.sax.saxutils import escape

from lxml import etree

nsDict = {'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'owl':'http://www.w3.org/2002/07/owl#',
            'dc':'http://purl.org/dc/elements/1.1/',
            'sawsdl':'http://www.w3.org/ns/sawsdl',
            'sawsdlrdf':'http://www.w3.org/ns/sawsdl#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#'}

dest = None
filename = None
tree = None

def parse_el(element):
    global dest
    global filename
    global tree


    for child in element.getchildren():
        if child.tag is not etree.Comment:
            if 'el-' not in child.tag:
                c_name = child.tag.replace('{http://www.S3Model.org/xmlns/S3Model2}','S3Model2:')
                dest.write("<rdf:Description rdf:about='data/"+filename+tree.getpath(child)+"'>\n")
                dest.write("  <rdfs:domain rdf:resource='data/"+filename+"'/>\n")
                dest.write("  <rdf:subPropertyOf rdf:resource='"+tree.getpath(element)+"'/>\n")
                dest.write("  <rdf:value>"+escape(child.text)+"</rdf:value>\n")
                dest.write("</rdf:Description>\n\n")
            else:
                c_name = child.tag.replace('{http://www.S3Model.org/xmlns/S3Model2}','S3Model2:')
                dest.write("<rdf:Description rdf:about='data/"+filename+tree.getpath(child)+"'>\n")
                dest.write("  <rdfs:domain rdf:resource='data/"+filename+"'/>\n")
                dest.write("  <rdf:type rdf:resource='"+c_name.replace('el-','ct-')+"'/>\n")
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
  xmlns:S3Model2='http://www.S3Model.org/xmlns/S3Model2'>
\n"""
    nsDict={'xs':'http://www.w3.org/2001/XMLSchema',
            'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
            'dc':'http://purl.org/dc/elements/1.1/'}

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

            ccdid = root.tag.replace('{http://www.S3Model.org/xmlns/S3Model2}','')

            # create triple for the file link to CCD
            dest.write("\n<rdf:Description rdf:about='data/"+filename+"'> <!-- The document unique path/filename -->\n")
            dest.write("  <rdf:domain rdf:resource='http://www.ccdgen.com/ccdlib/"+ccdid+".xsd'/>\n")
            dest.write("  <owl:hasValue ehr:patid='"+str(randint(1,1000))+"'/> <!-- the patient ID -->\n")
            dest.write("  <owl:hasValue ehr:hcpid='"+str(randint(1,11))+"'/> <!-- the healthcare provider ID -->\n")
            dest.write("</rdf:Description>\n\n")
            entry = root.getchildren()[0]

            # create triple for Entry
            entry_el = entry.tag.replace('{http://www.S3Model.org/xmlns/S3Model2}','S3Model2:')
            dest.write("<rdf:Description rdf:about='data/"+filename+"/"+ccdid+"/"+entry_el+"'>\n")
            dest.write("  <rdfs:domain rdf:resource='data/"+filename+"'/>\n")
            dest.write("  <rdf:type rdf:resource='"+entry_el.replace('el-','ct-')+"'/>\n")
            dest.write('</rdf:Description>\n\n')
            parse_el(entry)

            dest.write('\n</rdf:RDF>\n')
            dest.close()


def genEntry(tree, entry, filename, ccdid, dest):
    entry_el = entry.tag.replace('{http://www.S3Model.org/xmlns/S3Model2}','S3Model2:')
    dest.write("<rdf:Description rdf:about='data/"+filename+"/"+ccdid+"/"+entry_el+"'>\n")
    children = entry.getchildren()
    for child in children:
        if child.tag is etree.Comment:
            pass
        else:
            el_name = child.tag.replace('{http://www.S3Model.org/xmlns/S3Model2}','S3Model2:')
            print("<rdf:Description rdf:about='data/"+filename+tree.getpath(child)+"'>\n")
            print("<rdf:type rdf:resource='"+el_name.replace('el-','ct-')+"'/>\n")
    dest.write("</rdf:Description>\n")


if __name__ == '__main__':
    main()
    print("\n\nDone! \nCreated RDF/XML files in the rdf directory.\n\n")
    sys.exit(0)
