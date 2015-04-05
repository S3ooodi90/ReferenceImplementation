"""
S3ModelTester.py Copyright 2015, Timothy W. Cook.

This tool tests that a valid XML schema meets the guidelines established for it to be considered
a S3Model Concept Model.

The schema(s) to be checked must be in a 'schemas' subdirectory of this file location.

"""
import os
import sys
import re
import datetime
from random import randint
from xml.sax.saxutils import escape
import uuid
from lxml import etree


def main():

    # TODO: pull the namespace defs from the CM.
    nsDict = {'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
              'xs':'http://www.w3.org/2001/XMLSchema',
              'foaf':'http://xmlns.com/foaf/0.1/',
              'owl':'http://www.w3.org/2002/07/owl#',
              'sawsdl':'http://www.w3.org/ns/sawsdl',
              'sawsdlrdf':'http://www.w3.org/ns/sawsdl#',
              'dct':'http://purl.org/dc/terms/',
              'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
              's3m':'http://www.s3model.com/',
              'sch':'http://purl.oclc.org/dsdl/schematron'}

    parser = etree.XMLParser(ns_clean=True, recover=True)
    #create a new log file for each run and write the date and time.
    lf = open('S3ModelTester.log', 'w')
    lf.write('S3Model Errors: '+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")+'\n')

    ct = etree.XPath("//xs:complexType", namespaces=nsDict)

    files = os.listdir('schemas')
    print('\n\nTesting ', len(files), ' files.')
    for filename in files:
        print('\n\nProcessing: ', os.path.join('schemas', filename))
        src = open(os.path.join('schemas', filename), 'r')
        tree = etree.parse(src, parser)
        root = tree.getroot()
        cxt = ct(root)
        for c in cxt:

            #ERRORS:
            # check for 'ct-' followed by a UUID4 name.
            name = c.attrib['name']
            if name[0:3] != 'ct-':
                lf.write('ERROR: complexType: ' + name + ' has an invalid prefix. \n')
            try:
                uuid.UUID(name[3:])
            except ValueError:
                lf.write('ERROR: complexType: ' + name + ' has an invalid UUID. \n')
                print('ERROR: complexType: ' + name + ' has an invalid UUID.')


            # check for a restriction of a RM type

            #WARNINGS:

            # check for ct docs.

            # check for ct semantics

            # check for element docs

            # check that enumerations should have semantics


    lf.write('\nAll tests completed. Any errors or warnings appear above this line.\n')
    lf.close()

    return

if __name__ == '__main__':
    main()
    print("\n\nDone! See the file S3ModelTester.log for errors and warnings.\n\n")
    sys.exit(0)


