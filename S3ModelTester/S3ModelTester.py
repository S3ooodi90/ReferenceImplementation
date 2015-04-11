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
              'sch':'http://purl.oclc.org/dsdl/schematron',
              'vc':'http://www.w3.org/2007/XMLSchema-versioning'}

    rmTypes = {'s3m:DvParsableType', 's3m:DvBooleanType', 's3m:AttestationType', 's3m:ClusterType',
               's3m:DvIntervalType', 's3m:AuditType', 's3m:DvQuantityType', 's3m:DvCountType',
               's3m:DvMediaType', 's3m:DvRatioType', 's3m:DvStringType', 's3m:InvlType', 's3m:DvLinkType',
               's3m:ConceptType', 's3m:PartyType', 's3m:ParticipationType', 's3m:DvAdapterType',
               's3m:ReferenceRangeType'}


    parser = etree.XMLParser(ns_clean=True, recover=True)
    #create a new log file for each run and write the date and time.
    lf = open('S3ModelTester.log', 'w')
    lf.write('S3Model CM Tests Run: '+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")+'\n')

    ct = etree.XPath("//xs:complexType", namespaces=nsDict)

    files = os.listdir('schemas')
    print('\n\nTesting ', len(files), ' files.')
    for filename in files:
        lf.write('\n\nProcessing: '+ os.path.join('schemas', filename)+'\n')
        print('\n\nProcessing: ', os.path.join('schemas', filename))
        src = open(os.path.join('schemas', filename), 'r')
        tree = etree.parse(src, parser)
        root = tree.getroot()
        cxt = ct(root) # get the complexTypes

        #ERRORS:

        # check for vc:minVersion = '1.1'
        try:
            if not root.xpath('@vc:minVersion', namespaces=nsDict)[0] == '1.1':
                lf.write('ERROR: Incorrect minVersion attribute value. \n')
                print('ERROR: Incorrect minVersion attribute value.')
        except IndexError:
            lf.write('ERROR: Missing minVersion attribute. \n')
            print('ERROR: Missing minVersion attribute.')

        # check for RM include
        try:
            rm = root.xpath('./xs:include/@schemaLocation', namespaces=nsDict)[0]
            if not rm.startswith('http://www.s3model.com/rm/s3model'):
                lf.write('ERROR: ' + rm + ' is an invalid xs:include. \n')
                print('ERROR: ' + rm + ' is an invalid xs:include.')
        except IndexError:
            lf.write('ERROR: file ' + filename + ' is missing a RM xs:include. \n')
            print('ERROR: file ' + filename + ' is missing a RM xs:include.')


        # check for metadata on the first ct which should also be the s3m:ConceptType restriction.
        if not cxt[0].xpath('./xs:complexContent/xs:restriction/@base', namespaces=nsDict)[0] == 's3m:ConceptType':
            lf.write('ERROR: The first complexType should be a s3m:ConceptType restriction. Cannot test metadata. \n')
            print('ERROR: The first complexType should be a s3m:ConceptType restriction. Cannot test metadata.')
        else:
            md_okay = True # set this to False if there are any issues in the metadata
            md = cxt[0].xpath('./xs:annotation/xs:appinfo/rdf:Description', namespaces=nsDict)
            if not len(md) > 0: # missing metadata
                md_okay = False
            else:
                if not len(md[0].xpath('//dct:title', namespaces=nsDict)) > 0: #missing
                    md_okay = False
                if not len(md[0].xpath('//dct:creator', namespaces=nsDict)) > 0: #missing
                    md_okay = False
                if not len(md[0].xpath('//dct:rightsHolder', namespaces=nsDict)) > 0: #missing
                    md_okay = False
                if not len(md[0].xpath('//dct:issued', namespaces=nsDict)) > 0: #missing
                    md_okay = False
                if not len(md[0].xpath('//dct:format', namespaces=nsDict)) > 0: #missing
                    md_okay = False
                if not len(md[0].xpath('//dct:language', namespaces=nsDict)) > 0: #missing
                    md_okay = False
                if not len(md[0].xpath('//dct:abstract', namespaces=nsDict)) > 0: #missing
                    md_okay = False


            if not md_okay:
                lf.write('ERROR: There are errors in your metadata. \n')
                print('ERROR: There are errors in your metadata.')



        for c in cxt:
            #ERRORS:
            # check for 'ct-' followed by a UUID4 name.
            name = c.attrib['name']
            if name[0:3] != 'ct-':
                lf.write('ERROR: complexType: ' + name + ' has an invalid prefix. \n')
                print('ERROR: complexType: ' + name + ' has an invalid prefix.')

            try:
                uuid.UUID(name[3:])
            except ValueError:
                lf.write('ERROR: complexType: ' + name + ' has an invalid UUID. \n')
                print('ERROR: complexType: ' + name + ' has an invalid UUID.')


            # check for a restriction of a RM type
            restriction = c.xpath('./xs:complexContent/xs:restriction/@base', namespaces=nsDict)
            for r in restriction:
                if r not in rmTypes:
                    lf.write('ERROR: ' + r + ' is not a valid S3Model RM type. \n')
                    print('ERROR: ' + r + ' is not a valid S3Model RM type.')

            # check for an extension of a RM type
            extension = c.xpath('./xs:complexContent/xs:extension', namespaces=nsDict)
            if len(extension) > 0:
                    lf.write('ERROR: complexType: ' + name + ' uses xs:extension. This is not allowed in S3Model. \n')
                    print('ERROR: complexType: ' + name + ' uses xs:extension. This is not allowed in S3Model.')

            # TODO: an exception is to allow the extension of an ExceptionalValue
            # TODO: test Interval types for correctness.
            

            #WARNINGS:

            # check for ct docs.
            docs = c.xpath('./xs:annotation/xs:documentation/text()', namespaces=nsDict)
            if not len(docs) > 0:
                lf.write('WARNING: complexType: ' + name + ' is missing documentation. \n')
                print('WARNING: complexType: ' + name + ' is missing documentation.')

            # check for ct semantics
            sem = c.xpath('./xs:annotation/xs:appinfo/rdf:Description', namespaces=nsDict)
            if not len(sem) > 0:
                lf.write('WARNING: complexType: ' + name + ' is missing a semantics definition. \n')
                print('WARNING: complexType: ' + name + ' is missing a semantics definition.')


            # TODO: check for element docs



            # TODO: check that enumerations should have semantics
            # TODO: check Interval types for validity


    lf.write('\nAll tests completed. Errors and/or warnings appear above this line.\n')
    lf.close()

    return

if __name__ == '__main__':
    main()
    print("\n\nDone! See the file S3ModelTester.log for errors and warnings.\n\n")
    sys.exit(0)


