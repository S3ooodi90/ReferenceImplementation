#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    from urllib.parse import quote
except ImportError:
    from urllib.parse import quote

from uuid import uuid4
from collections import OrderedDict
from xml.sax.saxutils import escape

from .exceptions import PublishingError, ModellingError
from .r_code_gen import pct_rcode
from .xqr_code_gen import pct_xqrcode

"""
publisher.py

The S3Model Reference Model code to write CM schemas.
Copyright 2015, Timothy W. Cook, All Rights Reserved.

This code is accessed from model.py
Each class from the model will have a 'publish_' function here that will assemble
the strings required to write itself to code in a CM.
The code is stored in the schema_code text field.

When the published flag is True, this function is executed in order to write the code to the database.
If the schema_code field is not empty, the flag will remain True and the code will not be overwritten.

The Unpublish admin action must be executed to remove the existing code and reset the flag.
This must only be used on test PcTs during development. Otherwise conflicting code with the same UUIDs can result.

TODO: Maybe in the unpublish action also reissue new UUIDs.

"""
def reset_publication(self):
    """
    Insure that the schema code, R code and the published flag is False,anytime there is a
    publication or modelling error.
    This was needed after noticing that sometimes the published flag gets set even though an error
    was raised.
    """
    self.schema_code = ''
    self.r_code = ''
    self.published = False
    self.save()


#====================================================================
def publish_DvBoolean(self):
    """
    Writes the complete CM complexType code for the containing the DvBoolean itself.
    Saves it in the schema_code attribute.
    Once written it sets the 'published' flag to True.
    """

    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvBoolean')
##    self.save()

    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvBoolean')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')


    trues = []
    falses = []
    for t in self.true_values.splitlines():
        trues.append(escape(t))

    for f in self.true_values.splitlines():
        falses.append(escape(f))


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvBooleanType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvBooleanType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")
    #DvBoolean
    dt_str += padding.rjust(indent+8) + ("<xs:choice maxOccurs='1' minOccurs='0'>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element name='true-value'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(len(trues)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+trues[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element name='false-value'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(len(falses)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+falses[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("</xs:choice>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode("utf-8")


def publish_DvLink(self):
    """
     Writes the complete CM complexType code for the containing the DvLink itself. Saves it in the schema_code
     attribute. Once written it sets the 'published' flag to True. This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()
    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvLink')
##    self.save()

    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvLink')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvLinkType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvLinkType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvLink
    if self.link_value:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='link-value' type='xs:anyURI' fixed='"+escape(self.link_value.strip())+"'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='link-value' type='xs:anyURI'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='relation' type='xs:string' fixed='"+escape(self.relation.strip())+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='relation-uri' type='xs:anyURI' fixed='"+escape(self.relation_uri.strip())+"'/>\n")

    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode("utf-8")


def publish_DvString(self):
    """
    Writes the complete CM complexType code for the DvString.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()
    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvString')
##    self.save()

    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvString')
##    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')


    langReq = ('1' if self.lang_required else '0')
    enumList = []
    for e in self.enums.splitlines():
        enumList.append(escape(e))

    eDefs = []

    for d in self.enums_def.splitlines():
        eDefs.append(escape(d))

    # if there is only one enum definition and there are more than 1 enumerations then use the same definition for each enum
    if len(eDefs) == 1 and len(enumList) > 1:
        s = eDefs[0]
        for x in range(2,len(enumList)):
            eDefs.append(s)

    if self.default_value:
        default = escape(self.default_value.strip())
    else:
        default = None

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvStringType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvStringType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvString
    if default:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='dvstring-value' default='"+escape(default.strip())+"'>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='dvstring-value'>\n")

    dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")

    if not enumList:
        dt_str += padding.rjust(indent+16) + ("<xs:whiteSpace value='"+self.whitespace+"'/>\n")


    if not enumList and self.exact_length:
        dt_str += padding.rjust(indent+16) + ("<xs:length value='"+self.exact_length+"'/>\n")
    else:
        if self.min_length:
            dt_str += padding.rjust(indent+16) + ("<xs:minLength value='"+self.min_length+"'/>\n")
        if self.max_length:
            dt_str += padding.rjust(indent+16) + ("<xs:maxLength value='"+self.max_length+"'/>\n")

    if not enumList and self.pattern:
        dt_str += padding.rjust(indent+16) + ("<xs:pattern value='"+self.pattern+"'/>\n")

    # Enumerations
    if enumList:
        if len(eDefs) != len(enumList):
            reset_publication(self)
            raise PublishingError("Cannot publish: "+self.data_name+" The number of Enumerations and Definitions must be same. Check for empty lines.")
        for n in range(len(enumList)):
            dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+escape(enumList[n].strip())+"'>\n")
            dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
            dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"#"+enumList[n].strip()+"'>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:subPropertyOf rdf:resource='s3m:ct-"+self.ct_id+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:label>"+enumList[n].strip()+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:isDefinedBy rdf:resource='"+eDefs[n]+"'")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
            dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")


    dt_str += padding.rjust(indent+14) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+langReq+"' name='language' type='xs:language'/>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode("utf-8")

def publish_DvParsable(self):
    """
    Writes the complete CM complexType code for the DvParsable itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvParsable')
##    self.save()

    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvParsable')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    langReq = ('1' if self.lang_required else '0')
    fenumList = []
    for e in self.fenums.splitlines():
        fenumList.append(escape(e))

    feDefs = []

    for d in self.fenums_def.splitlines():
        feDefs.append(escape(d))


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvParsableType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvParsableType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvEncapsulated
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='size' type='xs:int'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' default='"+self.encoding.strip()+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+langReq+"' name='language' type='xs:language' default='"+self.language.strip()+"'/>\n")

    if not fenumList:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='formalism' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='formalism'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")

        if len(feDefs) != len(fenumList):
            reset_publication(self)
            raise PublishingError("Cannot publish: "+self.data_name+" The number of Enumerations and Definitions must be same. Check for empty lines.")

        for n in range(len(fenumList)):
            dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+escape(fenumList[n].strip())+"'>\n")
            dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
            dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"#"+fenumList[n].strip()+"'>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:subPropertyOf rdf:resource='s3m:ct-"+self.ct_id+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:label>"+fenumList[n].strip()+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:isDefinedBy rdf:resource='"+feDefs[n]+"'")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
            dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    #DvParsable
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvparsable-value' type='xs:string'/>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")

    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode("utf-8")


def publish_DvMedia(self):
    """
    Writes the complete CM complexType code for the DvMedia itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvMedia')
##    self.save()

    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvMedia')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    langReq = ('1' if self.lang_required else '0')
    fenumList = []
    for e in self.fenums.splitlines():
        fenumList.append(escape(e))

    feDefs = []

    for d in self.fenums_def.splitlines():
        feDefs.append(escape(d))

    altReq = ('1' if self.alt_required else '0')
    mediaReq = ('1' if self.media_required else '0')
    compReq = ('1' if self.comp_required else '0')
    hashReq = ('1' if self.hash_required else '0')

    if self.media_type:
        media_list = []
        for m in self.media_type.splitlines():
            media_list.append(escape(m).strip())

    if self.compression_type:
        comp_list = []
        for c in self.compression_type.splitlines():
            comp_list.append(escape(c).strip())


    if self.hash_function:
        hash_list = []
        for h in self.hash_type.splitlines():
            hash_list.append(escape(h).strip())


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvMediaType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvMediaType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvEncapsulated
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='size' type='xs:int'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' default='"+self.encoding.strip()+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+langReq+"' name='language' type='xs:language' default='"+self.language.strip()+"'/>\n")

    if not fenumList:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='formalism' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='formalism'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")

        if len(feDefs) != len(fenumList):
            reset_publication(self)
            raise PublishingError("Cannot publish: "+self.data_name+" The number of Enumerations and Definitions must be same. Check for empty lines.")

        for n in range(len(fenumList)):
            dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+escape(fenumList[n].strip())+"'>\n")
            dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
            dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"#"+fenumList[n].strip()+"'>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:subPropertyOf rdf:resource='s3m:ct-"+self.ct_id+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:label>"+fenumList[n].strip()+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:isDefinedBy rdf:resource='"+feDefs[n]+"'")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
            dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    #DvMedia
    if not media_list:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+mediaReq+"' name='media-type' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+mediaReq+"' name='media-type'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
        for m in media_list:
            dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+m+"'>\n")
            dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
            dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"#"+m+"'>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:subPropertyOf rdf:resource='s3m:ct-"+self.ct_id+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:label>"+m+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+2) + ("  <rdfs:isDefinedBy rdf:resource='http://purl.org/NET/mediatypes/"+m+"'/>")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
            dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    if not comp_list:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+compReq+"' name='compression-type' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+compReq+"' name='compression-type'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
        for c in comp_list:
            dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+c+"'/>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+hashReq+"' name='hash-result' type='xs:string'/>\n")

    if not hash_list:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+hashReq+"' name='hash-function' type='xs:string' default='"+escape(self.hash_function)+"'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+compReq+"' name='hash-function'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
        for h in hash_list:
            dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+h+"'/>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+altReq+"' name='alt-txt' type='xs:string' default='"+escape(self.alt_txt)+"'/>\n")

    #choice
    if self.content == 'user':
        dt_str += padding.rjust(indent+8) + ("<xs:choice maxOccurs='1' minOccurs='1'>")
        dt_str += padding.rjust(indent+10) + ("<xs:element name='uri' type='xs:anyURI'/>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:element name='media-content' type='xs:base64Binary'/>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:choice>")
    elif self.content == 'url':
        dt_str += padding.rjust(indent+8) + ("<xs:element name='uri' type='xs:anyURI'/>\n")
    elif self.content == 'embed':
        dt_str += padding.rjust(indent+8) + ("<xs:element name='media-content' type='xs:base64Binary'/>\n")
    else:
        pass # because this should never happen and if it does your DvMedia is broken.

    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode("utf-8")


def publish_DvInterval(self):
    """
    Writes the complete CM complexType code for the DvInterval itself.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvInterval')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    #Convert the bools to XSD strings
    li,ui,lb,ub = 'false','false','false','false'
    if self.lower_included:
        li = 'true'
    if self.upper_included:
        ui = 'true'
    if self.lower_bounded:
        lb = 'true'
    if self.upper_bounded:
        ub = 'true'

    # Interval type must be set and be an ordered type
    if self.interval_type == 'None':
        reset_publication(self)
        raise PublishingError("Missing Interval Type. "+self.data_name)

    if self.interval_type not in ['int', 'decimal','date','time','dateTime','float','duration']:
        reset_publication(self)
        raise TypeError("Invalid Type for DvInterval. "+repr(self.interval_type)+" in "+self.data_name+" is not an allowed, ordered type.")

    # check for modelling errors
    if self.lower_bounded and not self.lower:
        reset_publication(self)
        raise ModellingError("Enter lower value or uncheck the lower bounded box in "+self.data_name+". ")
    if self.upper_bounded and not self.upper:
        reset_publication(self)
        raise ModellingError("Enter upper value or uncheck the upper bounded box in "+self.data_name+". ")

    if not self.lower_bounded and self.lower:
        reset_publication(self)
        raise ModellingError("Remove lower value or check the lower bounded box in "+self.data_name+". ")
    if not self.upper_bounded and self.upper:
        reset_publication(self)
        raise ModellingError("Remove upper value or check the upper bounded box in "+self.data_name+". ")

    # if the user used a comma as a decimal separator then replace it with a period.
    if self.interval_type == 'decimal':
        if "," in self.lower:
            self.lower = self.lower.replace(",",".")
            self.save()
        if "," in self.upper:
            self.upper = self.upper.replace(",",".")
            self.save()


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvIntervalType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvIntervalType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")


    #DvInterval
    # create an UUIDs for the invl-type restrictions
    lower_id = str(uuid4())
    upper_id = str(uuid4())
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='lower' type='s3m:ct-"+lower_id+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='upper' type='s3m:ct-"+upper_id+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='lower-included' type='xs:boolean' fixed='"+li+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='upper-included' type='xs:boolean' fixed='"+ui+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='lower-bounded' type='xs:boolean' fixed='"+lb+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='upper-bounded' type='xs:boolean' fixed='"+ub+"'/>\n")

    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    # lower value restriction
    dt_str += padding.rjust(indent+2) + ("<xs:complexType name='ct-"+lower_id+"'> <!-- interval lower -->\n")
    dt_str += padding.rjust(indent+4) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:restriction base='s3m:InvlType'>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:choice>\n")
    if self.lower_bounded:
        dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-"+self.interval_type+"' type='xs:"+self.interval_type+"' fixed='"+self.lower.strip()+"'/>\n")
    else:
        dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-"+self.interval_type+"' type='xs:"+self.interval_type+"' nillable='true'/> <!-- Instance elements must be set to xsi:nil='true' -->\n")
    dt_str += padding.rjust(indent+8) + ("</xs:choice>\n")
    if not self.lower_bounded:
        dt_str += padding.rjust(indent+8) + ("<xs:assert test='boolean(invl-"+self.interval_type+"/node()) = false()'/>\n")
    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    # upper value restriction
    dt_str += padding.rjust(indent+2) + ("<xs:complexType name='ct-"+upper_id+"'> <!-- interval upper -->\n")
    dt_str += padding.rjust(indent+4) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:restriction base='s3m:InvlType'>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:choice>\n")
    if self.upper_bounded:
        dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-"+self.interval_type+"' type='xs:"+self.interval_type+"' fixed='"+self.upper.strip()+"'/>\n")
    else:
        dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-"+self.interval_type+"' type='xs:"+self.interval_type+"' nillable='true'/> <!-- Instance elements must be set to xsi:nil='true' -->\n")
    dt_str += padding.rjust(indent+8) + ("</xs:choice>\n")
    if not self.upper_bounded:
        dt_str += padding.rjust(indent+8) + ("<xs:assert test='boolean(invl-"+self.interval_type+"/node()) = false()'/>\n")
    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")


    return dt_str.encode('utf-8')

def publish_ReferenceRange(self):
    """

    """
    self.ct_id = str(uuid4())
    self.save()

##    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'ReferenceRange')
##    self.save()
##    # fix double quotes in data-name
##    self.data_name.replace('"','&quot;')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    rr_def = escape(self.definition)
    dvi_id = self.data_range.ct_id
    if self.is_normal:
        normal="true"
    else:
        normal = "false"
    if not self.data_range.published:
        reset_publication(self)
        raise PublishingError("DvInterval: "+self.data_range.data_name+" hasn't been published. Please publish the interval and retry.")


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:ReferenceRangeType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:ReferenceRangeType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #ReferenceRange
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='definition' type='xs:string' fixed='"+rr_def.strip()+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-range' type='s3m:ct-"+dvi_id+"'/> <!-- data-range -->\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='is-normal' type='xs:boolean' fixed='"+normal+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode('utf-8')


def publish_DvOrdinal(self):
    """
    Writes the complete CM complexType code for the DvOrdinal itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()

##    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvOrdinal')
##    self.save()
##
##    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvOrdinal')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')


    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvordered

    o = []
    for a in self.ordinals.splitlines():
        o.append(escape(a))

    # test that these are really ints
    for n in o:
        try:
            x = int(n)
        except:
            raise ModellingError(escape(self.data_name.strip())+": You MUST use numbers for the Ordinal indicators. It seems one or more of yours is not.")

    s = []
    for a in self.symbols.splitlines():
        s.append(escape(a))

    symDefs = []
    for sd in self.symbols_def.splitlines():
        symDefs.append(escape(sd))

    # if there is only one symbol definition and there are more than 1 symbols then use the same definition for each symbol
    if len(symDefs) == 1 and len(s) > 1:
        sd = symDefs[0]
        for x in range(2,len(s)):
            symDefs.append(sd)


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvOrdinalType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvOrdinalType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvOrdered
    if len(self.reference_ranges.all()) > 0:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='1' name-'reference-range' type='s3m:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' fixed='"+escape(self.normal_status.strip())+"'/> \n")

    #DvOrdinal
    dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='dvordinal-value'>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:decimal'>\n")
    for n in range(0,len(o)):
        dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+o[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='symbol'>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")
    for n in range(len(s)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+s[n].strip()+"'>\n")
        dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
        dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"#"+s[n].strip()+"'>\n")
        dt_str += padding.rjust(indent+2) + ("  <rdfs:subPropertyOf rdf:resource='s3m:ct-"+self.ct_id+"'/>\n")
        dt_str += padding.rjust(indent+2) + ("  <rdfs:label>"+s[n].strip()+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("  <rdfs:isDefinedBy rdf:resource='"+symDefs[n]+"'")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
        dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
        dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
        dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")

    dt_str += padding.rjust(indent+14) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:element>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode('utf-8')


def publish_DvCount(self):
    """
    Writes the complete CM complexType code for the DvCount itself.
    """

    self.ct_id = str(uuid4())
    self.save()

##    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvCount')
##    self.save()
##
##    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvCount')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvordered

    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvCountType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvCountType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvOrdered
    if len(self.reference_ranges.all()) > 0:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='1' name-'reference-range' type='s3m:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' fixed='"+escape(self.normal_status.strip())+"'/> \n")


    #DvQuantified
    if not mag_constrained:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
        if self.min_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str(self.min_inclusive).strip()+"'/>\n")
        if self.max_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str(self.max_inclusive).strip()+"'/>\n")
        if self.min_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minExclusive value='"+str(self.min_exclusive).strip()+"'/>\n")
        if self.max_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxExclusive value='"+str(self.max_exclusive).strip()+"'/>\n")
        if (self.total_digits != None and self.total_digits > 0):
            dt_str += padding.rjust(indent+12) + ("<xs:totalDigits value='"+str(self.total_digits).strip()+"'/>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:fractionDigits value='0'/>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='magnitude-status' type='s3m:MagnitudeStatus'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='accuracy' type='xs:int' default='0'/>\n")

    #DvCount
    if not self.units.published:
        reset_publication(self)
        raise PublishingError( "DvString: "+self.units.data_name+" hasn't been published. Please publish the object and retry.")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='s3m:el-"+self.units.ct_id+"'/> <!-- DvCount-units -->\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode('utf-8')


def publish_DvQuantity(self):
    """
    Publish DvQuantity
    """
    self.ct_id = str(uuid4())
    self.save()

##    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvQuantity')
##    self.save()
##
##    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvQuantity')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvordered

    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvQuantityType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvQuantityType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvOrdered
    if len(self.reference_ranges.all()) > 0:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='1' name-'reference-range' type='s3m:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' fixed='"+escape(self.normal_status.strip())+"'/> \n")


    #DvQuantified
    if not mag_constrained:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
        if self.min_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str(self.min_inclusive).strip()+"'/>\n")
        if self.max_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str(self.max_inclusive).strip()+"'/>\n")
        if self.min_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minExclusive value='"+str(self.min_exclusive).strip()+"'/>\n")
        if self.max_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxExclusive value='"+str(self.max_exclusive).strip()+"'/>\n")
        if (self.total_digits != None and self.total_digits > 0):
            dt_str += padding.rjust(indent+12) + ("<xs:totalDigits value='"+str(self.total_digits).strip()+"'/>\n")
        if self.fraction_digits != None:
            dt_str += padding.rjust(indent+12) + ("<xs:fractionDigits value='"+str(self.fraction_digits).strip()+"'/>\n")

        dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='magnitude-status' type='s3m:MagnitudeStatus'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='accuracy' type='xs:int' default='0'/>\n")

    #DvQuantity
    if not self.units.published:
        reset_publication(self)
        raise PublishingError( "DvString: "+self.units.data_name+" hasn't been published. Please publish the object and retry.")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='s3m:el-"+self.units.ct_id+"'/> <!-- DvCount-units -->\n")
    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode('utf-8')



def publish_DvRatio(self):
    """
    Publish DvRatio
    """
    self.ct_id = str(uuid4())
    self.save()

##    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvRatio')
##    self.save()
##
##    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvRatio')
##    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvordered

    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False


    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvQuantityType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvQuantityType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvOrdered
    if len(self.reference_ranges.all()) > 0:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='1' name-'reference-range' type='s3m:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' fixed='"+escape(self.normal_status.strip())+"'/> \n")


    #DvQuantified
    if not mag_constrained:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
        if self.min_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str(self.min_inclusive).strip()+"'/>\n")
        if self.max_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str(self.max_inclusive).strip()+"'/>\n")
        if self.min_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minExclusive value='"+str(self.min_exclusive).strip()+"'/>\n")
        if self.max_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxExclusive value='"+str(self.max_exclusive).strip()+"'/>\n")
        if (self.total_digits != None and self.total_digits > 0):
            dt_str += padding.rjust(indent+12) + ("<xs:totalDigits value='"+str(self.total_digits).strip()+"'/>\n")
        if self.fraction_digits != None:
            dt_str += padding.rjust(indent+12) + ("<xs:fractionDigits value='"+str(self.fraction_digits).strip()+"'/>\n")

        dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='magnitude-status' type='s3m:MagnitudeStatus'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='accuracy' type='xs:int' default='0'/>\n")


    #DvRatio
    # tests for proper modelling
    if (self.num_min_inclusive and self.num_min_exclusive) or (self.num_max_inclusive and self.num_max_exclusive):
        reset_publication(self)
        raise ModellingError("There is ambiguity in your numerator constraints for min/max.")
    if (self.den_min_inclusive and self.den_min_exclusive) or (self.den_max_inclusive and self.den_max_exclusive):
        reset_publication(self)
        raise ModellingError("There is ambiguity in your denominator constraints for min/max.")

    # tests for not reusing units PcT
    if self.num_units is not None and self.den_units is not None:
        if self.num_units.ct_id == self.den_units.ct_id:
            reset_publication(self)
            raise ModellingError("Numerator and denominator units must use different PcTs.")

    if self.num_units is not None and self.ratio_units is not None:
        if self.num_units.ct_id == self.ratio_units.ct_id:
            reset_publication(self)
            raise ModellingError("Numerator and ratio units must use different PcTs.")

    if self.den_units is not None and self.ratio_units is not None:
        if self.den_units.ct_id == self.ratio_units.ct_id:
            reset_publication(self)
            raise ModellingError("Denominator and ratio units must use different PcTs.")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='ratio-type' type='s3m:RatioType' fixed='"+self.ratio_type+"'/>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='numerator'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
    if self.num_min_inclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str(self.num_min_inclusive).strip()+"'/>\n")
    if self.num_min_exclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:minExclusive value='"+str(self.num_min_exclusive).strip()+"'/>\n")
    if self.num_max_inclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str(self.num_max_inclusive).strip()+"'/>\n")
    if self.num_max_exclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:maxExclusive value='"+str(self.num_max_exclusive).strip()+"'/>\n")
    if (self.num_total_digits != None and self.num_total_digits > 0):
        dt_str += padding.rjust(indent+12) + ("<xs:totalDigits value='"+str(self.num_total_digits).strip()+"'/>\n")
    if self.num_fraction_digits != None:
        dt_str += padding.rjust(indent+12) + ("<xs:fractionDigits value='"+str(self.num_fraction_digits).strip()+"'/>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='denominator'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
    if self.den_min_inclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str(self.den_min_inclusive).strip()+"'/>\n")
    if self.den_min_exclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:minExclusive value='"+str(self.den_min_exclusive).strip()+"'/>\n")
    if self.den_max_inclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str(self.den_max_inclusive).strip()+"'/>\n")
    if self.den_max_exclusive:
        dt_str += padding.rjust(indent+12) + ("<xs:maxExclusive value='"+str(self.den_max_exclusive).strip()+"'/>\n")
    if (self.den_total_digits != None and self.total_digits > 0):
        dt_str += padding.rjust(indent+12) + ("<xs:totalDigits value='"+str(self.den_total_digits).strip()+"'/>\n")
    if self.den_fraction_digits != None:
        dt_str += padding.rjust(indent+12) + ("<xs:fractionDigits value='"+str(self.den_fraction_digits).strip()+"'/>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    if self.num_units:
        if not self.num_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+num_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='numerator-units' type='s3m:ct-"+self.num_units.ct_id+"'/> <!-- numerator-units -->\n")

    if self.den_units:
        if not self.den_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+self.den_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='denominator-units' type='s3m:ct-"+self.den_units.ct_id+"'/> <!-- denominator-units -->\n")

    if self.ratio_units:
        if not self.ratio_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+self.ratio_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='ratio-units' type='s3m:ct-"+self.ratio__units.ct_id+"'/> <!-- ratio-units -->\n")

    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode('utf-8')


def publish_DvTemporal(self):
    """
    All time based options.
    Only one duration type is allowed.  If multiple durations are chosen by the modeller, a modelling error is raised.
    If any duration type is allowed then no other types are allowed.
    """
    self.ct_id = str(uuid4())
    self.save()

##    # generate and save the code for a R function.
##    self.r_code = pct_rcode(self, 'DvTemporal')
##    self.save()
##
##    # generate and save the code for a XQuery function.
##    self.xqr_code = pct_xqrcode(self, 'DvTemporal')
##    self.save()


    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    vtbMin = ('1' if self.vtb_required else '0')
    vteMin = ('1' if self.vte_required else '0')

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvordered

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:DvQuantityType'/>\n")
    dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
    for s in sems:
        dt_str += padding.rjust(indent+2) + s # the selected semantics
    dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:DvQuantityType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vtbMin+"' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+vteMin+"' name='vte' type='xs:dateTime'/>\n")

    #DvOrdered
    if len(self.reference_ranges.all()) > 0:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='1' name-'reference-range' type='s3m:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' fixed='"+escape(self.normal_status.strip())+"'/> \n")

    #DvTemporal

    # set minOccurs for each element
    dateMin = ('1' if self.require_date else '0')
    timeMin = ('1' if self.require_time else '0')
    datetimeMin = ('1' if self.require_datetime else '0')
    dayMin = ('1' if self.require_day else '0')
    monthMin = ('1' if self.require_month else '0')
    yearMin = ('1' if self.require_year else '0')
    year_monthMin = ('1' if self.require_year_month else '0')
    month_dayMin = ('1' if self.require_month_day else '0')
    durationMin = ('1' if self.require_duration else '0')
    ymdurationMin = ('1' if self.require_ymduration else '0')
    dtdurationMin = ('1' if self.require_dtduration else '0')

    # set maxOccurs for each element
    dateMax = ('1' if self.allow_date else '0')
    timeMax = ('1' if self.allow_time else '0')
    datetimeMax = ('1' if self.allow_datetime else '0')
    dayMax = ('1' if self.allow_day else '0')
    monthMax = ('1' if self.allow_month else '0')
    yearMax = ('1' if self.allow_year else '0')
    year_monthMax = ('1' if self.allow_year_month else '0')
    month_dayMax = ('1' if self.allow_month_day else '0')
    durationMax = ('1' if self.allow_duration else '0')
    ymdurationMax = ('1' if self.allow_ymduration else '0')
    dtdurationMax = ('1' if self.allow_dtduration else '0')

    #ony one element can be required and if one is required no others are allowed
    required_set = False
    if self.require_date:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_time:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_datetime:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_day:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_month:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_year:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_year_month:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_month_day:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_duration:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_ymduration:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    if self.require_dtduration:
        if not required_set:
            required_set = True
        else:
            reset_publication(self)
            raise ModellingError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

    #only one duration is allowed
    if (self.allow_duration and self.allow_ymduration) or (self.allow_duration and self.allow_dtduration) or (self.allow_ymduration and self.allow_dtduration):
        reset_publication(self)
        raise ModellingError("Only one of the duration types are allowed to be selected.")

    # if there is a duration, you cannot have any other temporal elements.
    if (self.allow_duration or self.allow_ymduration or self.allow_dtduration) and (self.allow_date or self.allow_time or self.allow_datetime or self.allow_day or self.allow_month or self.allow_year or self.allow_year_month or self.allow_month_day):
        reset_publication(self)
        raise ModellingError("You cannot have a duration mixed with other temporal types.")

    #every element must be included as either allowed or not allowed (maxOccurs = 1 or 0).

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+dateMax+"' minOccurs='"+dateMin+"' name='dvtemporal-date' type='xs:date'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+timeMax+"' minOccurs='"+timeMin+"' name='dvtemporal-time' type='xs:time'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+datetimeMax+"' minOccurs='"+datetimeMin+"' name='dvtemporal-datetime' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+dayMax+"' minOccurs='"+dayMin+"' name='dvtemporal-day' type='xs:gDay'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+monthMax+"' minOccurs='"+monthMin+"' name='dvtemporal-month' type='xs:gMonth'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+yearMax+"' minOccurs='"+yearMin+"' name='dvtemporal-year' type='xs:gYear'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+year_monthMax+"' minOccurs='"+year_monthMin+"' name='dvtemporal-year-month' type='xs:gYearMonth'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+month_dayMax+"' minOccurs='"+month_dayMin+"' name='dvtemporal-month-day' type='xs:gMonthDay'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+durationMax+"' minOccurs='"+durationMin+"' name='dvtemporal-duration' type='xs:duration'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+ymdurationMax+"' minOccurs='"+ymdurationMin+"' name='dvtemporal-ymduration' type='xs:yearMonthDuration'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='"+dtdurationMax+"' minOccurs='"+dtdurationMin+"' name='dvtemporal-dtduration' type='xs:dayTimeDuration'/>\n")

    dt_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    dt_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return dt_str.encode('utf-8')

def publish_Party(self):
    """
    Publish a Party definition.

    """
    self.ct_id = str(uuid4())
    self.save()

    party_str = ''
    indent = 2
    padding = ('').rjust(indent)
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    nameMin = ('1' if self.require_name else '0')


    #Create the datatype
    party_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    party_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    party_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    party_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    party_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    party_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    party_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    party_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:PartyType'/>\n")
    party_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.label.strip())+"</rdfs:label>\n")
    for s in sems:
        party_str += padding.rjust(indent+2) + s # the selected semantics
    party_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    party_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    party_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    party_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    party_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:PartyType'>\n")
    party_str += padding.rjust(indent+6) + ("<xs:sequence>\n")

    party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='"+nameMin+"' name='party-name' type='xs:string'/>\n")

    if not self.party_ref.all():
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='party-ref' type='s3m:DvLinkType'/>\n")
    else:
        for xref in self.party_ref.all():
            if not xref.published:
                reset_publication(self)
                raise PublishingError("External Reference: "+xref.data_name+" hasn't been published. Please publish the DvLink and retry.")
            else:
                party_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ct-"+xref.ct_id+"'/> <!-- external-ref -->\n"

    if not self.party_details:
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='party-details' type='s3m:ClusterType'/>\n")
    else:
        if not self.party_details.published:
            reset_publication(self)
            raise PublishingError("Cluster: "+self.party_details.cluster_subject+" hasn't been published. Please publish the item and retry.")
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='party-details' type='s3m:ct-"+self.party_details.ct_id+"'/> <!-- details -->\n")
    party_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            party_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    party_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    party_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    party_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return party_str.encode("utf-8")


def publish_Audit(self):
    """
    Writes the complete CCD complexType code for Audit.

    """
    self.ct_id = str(uuid4())
    self.save()

    aud_str = ''
    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    indent = 2
    padding = ('').rjust(indent)


    #Create the datatype
    aud_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    aud_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    aud_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    aud_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    aud_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    aud_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    aud_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    aud_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:AuditType'/>\n")
    aud_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.label.strip())+"</rdfs:label>\n")
    for s in sems:
        aud_str += padding.rjust(indent+2) + s # the selected semantics
    aud_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    aud_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    aud_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    aud_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    aud_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:AuditType'>\n")
    aud_str += padding.rjust(indent+6) + ("<xs:sequence>\n")

    if not self.system_id:
        raise PublishingError("System ID: (DvString) has not been selected.")
    else:
        if not self.system_id.published:
            reset_publication(self)
            raise PublishingError("System ID: (DvString) "+self.system_id.data_name+" has not been published.")
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='s3m:el-"+self.system_id.ct_id+"'/> <!-- system-id -->\n")

    if not self.system_user:
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:System-user'/>\n")
    else:
        if not self.system_user.published:
            reset_publication(self)
            raise PublishingError("System User: (Party) "+self.system_user.label+" has not been published.")
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:el-"+self.system_user.ct_id+"'/> <!-- system-user -->\n")

    if not self.location:
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:Location'/>\n")
    else:
        if not self.location.published:
            reset_publication(self)
            raise PublishingError("Location: (Cluster) "+self.location.cluster_subject+" has not been published.")
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:el-"+self.location.ct_id+"'/> <!-- location -->\n")

    aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='timestamp' type='xs:dateTime'/>\n")

    aud_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            aud_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    aud_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    aud_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    aud_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return aud_str.encode("utf-8")


def publish_Attestation(self):
    """
    Publish an Attestation definition.

    """
    self.ct_id = str(uuid4())
    self.save()

    att_str = ''

    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    indent = 2
    padding = ('').rjust(indent)


    #Create the datatype
    att_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    att_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    att_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    att_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    att_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    att_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    att_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    att_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:AttestationType'/>\n")
    att_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.label.strip())+"</rdfs:label>\n")
    for s in sems:
        att_str += padding.rjust(indent+2) + s # the selected semantics
    att_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    att_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    att_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    att_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    att_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:AttestationType'>\n")
    att_str += padding.rjust(indent+6) + ("<xs:sequence>\n")

    if not self.attested_view.published:
        reset_publication(self)
        raise PublishingError("AttestedView: (DvMedia) "+self.attested_view.data_name+" has not been published.")
    att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='attested-view' type='s3m:ct-"+self.attested_view.ct_id+"'/> <!-- attested-view -->\n")

    if not self.proof.published:
        reset_publication(self)
        raise PublishingError("Proof: (DvParsable) "+self.proof.data_name+" has not been published.")
    att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='s3m:proof' ref='s3m:ct-"+self.proof.ct_id+"'/> <!-- proof -->\n")

    if not self.reason.published:
        reset_publication(self)
        raise PublishingError("Reason: (DvString) "+self.reason.data_name+" has not been published.")
    att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='reason' type='s3m:ct-"+self.reason.ct_id+"'/> <!-- reason -->\n")

    if not self.committer.published:
        reset_publication(self)
        raise PublishingError("Committer: (Party) "+self.committer.label+" has not been published.")
    att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='committer' type='s3m:ct-"+self.committer.ct_id+"'/> <!-- committer -->\n")

    att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='time-committed' type='xs:dateTime'/>\n")
    att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' default='true' name='is-pending' type='xs:boolean'/>\n")
    att_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            att_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    att_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    att_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    att_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return att_str.encode("utf-8")


def publish_Participation(self):
    """
    Writes the complete CM complexType code for the Participation.
    """
    self.ct_id = str(uuid4())
    self.save()

    ptn_str = ''

    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    indent = 2
    padding = ('').rjust(indent)


    #Create the datatype
    ptn_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    ptn_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    ptn_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    ptn_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    ptn_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    ptn_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    ptn_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    ptn_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:ParticipationType'/>\n")
    ptn_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.label.strip())+"</rdfs:label>\n")
    for s in sems:
        ptn_str += padding.rjust(indent+2) + s # the selected semantics
    ptn_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    ptn_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    ptn_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    ptn_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    ptn_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:ParticipationType'>\n")
    ptn_str += padding.rjust(indent+6) + ("<xs:sequence>\n")


    #Participation
    if not self.performer.published:
        reset_publication(self)
        raise PublishingError("Performer: "+self.performer.label+" hasn't been published. Please publish the Party and retry.")
    ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' type='s3m:ct-"+self.performer.ct_id+"'/> <!-- performer -->\n")

    if not self.function.published:
        reset_publication(self)
        raise PublishingError("Function: (DvString) "+self.function.data_name+" has not been published.")
    ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='function' type='s3m:ct-"+self.function.ct_id+"'/> <!-- function -->\n")

    if not self.mode.published:
        reset_publication(self)
        raise PublishingError("Mode: (DvString) "+self.mode.data_name+" has not been published.")
    ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='mode' type='s3m:ct-"+self.mode.ct_id+"'/> <!-- mode -->\n")

    ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='start-time' type='xs:dateTime'/>\n")
    ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='end-time' type='xs:dateTime'/>\n")

    ptn_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            ptn_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    ptn_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    ptn_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    ptn_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return ptn_str.encode("utf-8")


def publish_Cluster(self):
    """
    Publish a Cluster definition.

    """
    self.ct_id = str(uuid4())
    self.save()

    cl_str = ''
    links_id = None
    has_content = False

    # fix double quotes in cluster-subject
    self.cluster_subject.replace('"','&quot;')
    self.save()
    indent = 2
    padding = ('').rjust(indent)

    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    indent = 2
    padding = ('').rjust(indent)


    #Create the datatype
    cl_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.cluster_subject)+" -->\n")
    cl_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    cl_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    cl_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    cl_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    cl_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    cl_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    cl_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:ClusterType'/>\n")
    cl_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.cluster_subject.strip())+"</rdfs:label>\n")
    for s in sems:
        cl_str += padding.rjust(indent+2) + s # the selected semantics
    cl_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    cl_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    cl_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    cl_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    cl_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:ClusterType'>\n")
    cl_str += padding.rjust(indent+6) + ("<xs:sequence>\n")


    #Cluster
    cl_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='cluster-subject' type='xs:string' fixed="+'"'+escape(self.cluster_subject.strip())+'"'+"/>\n")

    if self.clusters.all():
        has_content = True
        for item in self.clusters.all():
            if item.ct_id != self.ct_id: # cannot put a Cluster inside itself
                if not item.published:
                    reset_publication(self)
                    raise PublishingError( "(Cluster) "+item.cluster_subject+" hasn't been published.")
                cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.ct_id+"'/><!-- Cluster "+item.cluster_subject+" -->\n")
            else:
                reset_publication(self)
                raise PublishingError( "(Cluster) "+item.cluster_subject+" NOTICE: You cannot nest a Cluster inside of itself at any level.")

    if self.dvboolean.all():
        has_content = True
        for item in self.dvboolean.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvBoolean) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvBoolean "+item.data_name+" -->\n")

    if self.dvlink.all():
        has_content = True
        for item in self.dvlink.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvLink) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvURI "+item.data_name+" -->\n")

    if self.dvstring.all():
        has_content = True
        for item in self.dvstring.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvString) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvString "+item.data_name+" -->\n")

    if self.dvparsable.all():
        has_content = True
        for item in self.dvparsable.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvParsable) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvParsable "+item.data_name+" -->\n")

    if self.dvmedia.all():
        has_content = True
        for item in self.dvmedia.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvMedia) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvMedia "+item.data_name+" -->\n")

    if self.dvordinal.all():
        has_content = True
        for item in self.dvordinal.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvOrdinal) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvOrdinal "+item.data_name+" -->\n")

    if self.dvcount.all():
        has_content = True
        for item in self.dvcount.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvCount) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvCount "+item.data_name+" -->\n")

    if self.dvquantity.all():
        has_content = True
        for item in self.dvquantity.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvQuantity) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvQuantity "+item.data_name+" -->\n")


    if self.dvratio.all():
        has_content = True
        for item in self.dvratio.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvRatio) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvRatio "+item.data_name+" -->\n")

    if self.dvtemporal.all():
        has_content = True
        for item in self.dvtemporal.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvTemporal) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvTemporal "+item.data_name+" -->\n")


    cl_str += padding.rjust(indent+6) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            cl_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    cl_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    cl_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    cl_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    if not has_content:
        reset_publication(self)
        raise PublishingError("Cluster: "+self.cluster_subject+" appears to be empty. You cannot publish an empty Cluster.")

    return cl_str.encode("utf-8")


def publish_Concept(self):
    """
    Writes the complete CM complexType code for the Concept.
    """
    self.ct_id = str(uuid4())
    self.save()

    con_str = ''

    sems = []
    # get the selected semantics
    for t in self.semantics.all():
        sems.append('  <' + t.pred + " rdf:resource='" + t.obj + "'/>\n")

    indent = 2
    padding = ('').rjust(indent)


    #Create the datatype
    con_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.title)+" -->\n")
    con_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    con_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    con_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    con_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    con_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    con_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='s3m:ct-"+self.ct_id+"'>\n")
    con_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='s3m:ConceptType'/>\n")
    con_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.label.strip())+"</rdfs:label>\n")
    #metadata
    con_str += padding.rjust(indent+2) + ("<dcterms:identifier xsi:type='dcterms:URI'>http://www.s3model.com/schemas/cm-"+self.ct_id+".xsd'</dcterms:identifier>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:title xml:lang='"+self.language+"'>"+self.title+"</dcterms:title>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:creator>\n")
    con_str += padding.rjust(indent+4) + ("<foaf:Person>\n")
    con_str += padding.rjust(indent+6) + ("<foaf:name>"+self.author.get_full_name()+"</foaf:name>\n")
    con_str += padding.rjust(indent+6) + ("<foaf:mbox rdf:resource='mailto:"+self.author.email+"'/>\n")
    con_str += padding.rjust(indent+4) + ("</foaf:Person>\n")
    con_str += padding.rjust(indent+2) + ("</dcterms:creator>\n")
    if len(self.contributors.all()) > 0:
        for con in self.contributors.all():
            con_str += padding.rjust(indent+2) + ("<dcterms:contributor>\n")
            con_str += padding.rjust(indent+4) + ("<foaf:Person>\n")
            con_str += padding.rjust(indent+6) + ("<foaf:name>"+con.get_full_name()+"</foaf:name>\n")
            con_str += padding.rjust(indent+6) + ("<foaf:mbox rdf:resource='mailto:"+con.email+"'/>\n")
            con_str += padding.rjust(indent+4) + ("</foaf:Person>\n")
            con_str += padding.rjust(indent+2) + ("</dcterms:contributor>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:rightsHolder>\n")
    con_str += padding.rjust(indent+4) + ("<foaf:Person>\n")
    con_str += padding.rjust(indent+6) + ("<foaf:name>"+self.rights_holder_name().strip()+"</foaf:name>\n")
    con_str += padding.rjust(indent+6) + ("<foaf:mbox rdf:resource='mailto:"+self.rights_holder_email.strip()+"'/>\n")
    con_str += padding.rjust(indent+4) + ("</foaf:Person>\n")
    con_str += padding.rjust(indent+2) + ("</dcterms:rightsHolder>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:issued>"+str(self.pub_date)+"</dcterms:issued>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:format rdf:value='text/xml'/>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:language rdf:value='"+self.lang+"'/>\n")
    con_str += padding.rjust(indent+2) + ("<dcterms:abstract>\n")
    con_str += padding.rjust(indent+2) + (escape(self.description)+"\n")
    con_str += padding.rjust(indent+2) + ("</dcterms:abstract>\n")
    #additional modelled semantics
    for s in sems:
        con_str += padding.rjust(indent+2) + s # the selected semantics
    con_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    con_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    con_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    con_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    con_str += padding.rjust(indent+4) + ("<xs:restriction base='s3m:ConceptType'>\n")
    con_str += padding.rjust(indent+6) + ("<xs:sequence>\n")


    #Concept elements
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='language' type='xs:language' fixed='"+self.lang+"'/>\n")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' fixed='"+self.encoding+"'/>\n")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='current-state' type='xs:string'/>\n")

    if not self.data.published:
        reset_publication(self)
        raise PublishingError("Data Cluster: "+self.data.cluster_subject+" hasn't been published. Please publish the Cluster and retry.")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data' type='s3m:ct-"+self.data.ct_id+"'/>\n")

    if not self.subject.published:
        reset_publication(self)
        raise PublishingError("Subject: (Party) "+self.subject.label+" has not been published.")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='subject' type='s3m:ct-"+self.subject.ct_id+"'/>\n")

    if not self.protocol.published:
        reset_publication(self)
        raise PublishingError("Protocol: (DvLink) "+self.protocol.data_name+" has not been published.")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='protocol' type='s3m:ct-"+self.protocol.ct_id+"'/>\n")

    if not self.workflow.published:
        reset_publication(self)
        raise PublishingError("Workflow: (DvLink) "+self.workflow.data_name+" has not been published.")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='workflow' type='s3m:ct-"+self.workflow.ct_id+"'/>\n")

    if not self.attested.published:
        reset_publication(self)
        raise PublishingError("Attested: (Attestation) "+self.attested.data_name+" has not been published.")
    con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='attested' type='s3m:ct-"+self.attested.ct_id+"'/>\n")

    if len(self.participations.all()) > 0:
        for p in self.participations.all():
            if not self.p.published:
                reset_publication(self)
                raise PublishingError("Participation: "+p.label+" has not been published.")
            con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:el-"+p.ct_id+"'/><!-- Participation -->\n")

    if len(self.audits.all()) > 0:
        for a in self.audits.all():
            if not self.a.published:
                reset_publication(self)
                raise PublishingError("Audit: "+a.label+" has not been published.")
            con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:el-"+a.ct_id+"'/><!-- Audit -->\n")

    if len(self.links.all()) > 0:
        for k in self.links.all():
            if not self.k.published:
                reset_publication(self)
                raise PublishingError("DvLink: "+k.data_name+" has not been published.")
            con_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='s3m:el-"+k.ct_id+"'/><!-- Audit -->\n")

    con_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            con_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    con_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    con_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    con_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return con_str.encode("utf-8")
