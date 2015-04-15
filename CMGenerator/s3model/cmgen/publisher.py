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

The MLHIM2 Reference Model code to write CCD schemas.
Copyright 2013-2015, Timothy W. Cook, All Rights Reserved.

This code is accessed from model.py
Each class from the model will have a 'publish_' function here that will assemble
the strings required to write itself to code in a CCD.
The code is stored in the schema_code text field.

When the published flag is True, this function is executed in order to write the code to the database.
If the schema_code field is not empty, the flag will remain True. In order to rewrite the code the database
field must be manually edited. This is to prevent changes being made to an item and it being rewritten with
the same UUID. THIS **MUST** NEVER HAPPEN!
If there are errors, just create a new component with a new UUID.

"""
def reset_publication(self):
    """
    Insure that the schema code, R code and the published flag is False,anytime there is a publication or modelling error.
    This was needed after noticing that sometimes the published flag gets set even though an error was raised.
    """
    self.schema_code = ''
    self.r_code = ''
    self.published = False
    self.save()


#====================================================================
def publish_DvBoolean(self):
    """
    Writes the complete CCD complexType code for the containing the DvBoolean itself. Saves it in the schema_code
    attribute. Once written it sets the 'published' flag to True. This flag can never be reset to False.

    Completed.
    """

    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvBoolean')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvBoolean')
    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    trues = []
    falses = []
    for t in self.valid_trues.splitlines():
        trues.append(escape(t))

    for f in self.valid_falses.splitlines():
        falses.append(escape(f))

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvBooleanType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvBooleanType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvBooleanType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvBoolean
    dt_str += padding.rjust(indent+8) + ("<xs:choice>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-true'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(len(trues)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+trues[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-false'>\n")
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
     Writes the complete CCD complexType code for the containing the DvURI itself. Saves it in the schema_code
     attribute. Once written it sets the 'published' flag to True. This flag can never be reset to False.

     Completed.
    """
    self.ct_id = str(uuid4())
    self.save()
    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvLink')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvLink')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvURIType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvURIType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvURIType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvURI
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvURI-dv' type='xs:anyURI'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='relation' type='xs:string' fixed='"+escape(self.relation.strip())+"'/>\n")

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
    Writes the complete CCD complexType code for the containing Element and the DvString itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.

    Completed.
    """
    self.ct_id = str(uuid4())
    self.save()
    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvString')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvString')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''

    indent = 2
    enumList = []
    for e in self.enums.splitlines():
        enumList.append(escape(e))

    tips = []
    for t in self.enums_annotations.splitlines():
        tips.append(escape(t))
    if self.default_value:
        default = escape(self.default_value.strip())
    else:
        default = None

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    padding = ('').rjust(indent)

    #Create the datatype
    dt_str += padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvStringType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvStringType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvStringType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvString
    if enumList:  # if enums exist, do not include type
        if default:
            dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvString-dv' default='"+escape(default.strip())+"'>\n")
        else:
            dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvString-dv'>\n")
    else:
        if default:
            dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvString-dv' type='xs:string' default='"+escape(default)+"'/>\n")
        else:
            dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvString-dv' type='xs:string'/>\n")

    # Enumerations
    if enumList:
        if len(tips) != len(enumList):
            if len(tips) == 0:
                tips = enumList
            else:
                reset_publication(self)
                raise PublishingError("Cannot publish: "+self.data_name+" The number of Enumerations and Annotations must be same. Check for empty lines.")
        dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")
        for n in range(len(enumList)):
            dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+escape(enumList[n].strip())+"'>\n")
            dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
            dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
            dt_str += padding.rjust(indent+20) + (escape(tips[n].strip())+"\n")
            dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
            dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")

        dt_str += padding.rjust(indent+14) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='language' type='xs:language'/>\n")
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

def publish_DvCodedString(self):
    """
    ta - list of terminology abbreviated names
    tn - list of terminology names
    tv - list of terminology versions
    tc - list of terminology codes
    cs - list of code strings
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvCodedString')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvCodedString')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)

    if self.t_abbrev and self.t_code and self.t_string:  # check to see if the codes and strings were manually typed into the form.
        ta = []
        for t in self.t_abbrev.splitlines():
            ta.append(escape(t))

        tn = []
        for t in self.t_name.splitlines():
            tn.append(escape(t))

        tv = []
        for t in self.t_version.splitlines():
            tv.append(escape(t))

        tc = []
        for t in self.t_code.splitlines():
            tc.append(escape(t))

        cs = []
        for t in self.t_string.splitlines():
            cs.append(escape(t))

        if not (len(ta) == len(tn) == len(tv) == len(tc) == len(cs)):
            reset_publication(self)
            raise ModellingError("You must have exactly the same number of entries in each of the terminology fields.")

    else: # we need to build the lists based on the number of codes selected.
        if not self.codes.all():
            reset_publication(self)
            raise ModellingError("You haven't defined any codes for the DvCodedString:"+ self.data_name)

        ta = []
        tn = []
        tv = []
        tc = []
        cs = []


        for c in self.codes.all():
            ta.append(escape(self.terminology.abbreviation))
            tn.append(escape(self.terminology.name))
            tv.append(escape(self.terminology.version))
            tc.append(escape(c.code))
            cs.append(escape(c.code_string))

    tips = []
    for t in self.enums_annotations.splitlines():
        tips.append(escape(t))

    default = escape(self.default_value)

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvCodedStringType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvCodedStringType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvCodedStringType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvString
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvString-dv'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(len(cs)):
        dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+cs[n].strip()+"'/>\n")

    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='language' type='xs:language'/>\n")

    #DvCodedString
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='terminology-abbrev'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(cs)):
        dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+ta[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='terminology-name'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(cs)):
        dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+tn[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='terminology-version'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(cs)):
        dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+tv[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='terminology-code'>\n")
    dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(cs)):
        if len(tips) != len(cs):
            tips = cs
        dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+tc[n].strip()+"'>\n")
        dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
        dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
        dt_str += padding.rjust(indent+20) + (tips[n].strip() + "\n")
        dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
        dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
        dt_str += padding.rjust(indent+14) + ("</xs:enumeration>\n")

    dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

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

def publish_DvIdentifier(self):
    """
    Writes the complete CCD complexType code for the DvIdentifier itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.

    .
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvIdentifier')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvIdentifier')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''

    indent = 2
    id_name = []
    for i in self.id_name.splitlines():
        id_name.append(escape(i))

    issuer = []
    for i in self.issuer.splitlines():
        issuer.append(escape(i))

    assignor = []
    for a in self.assignor.splitlines():
        assignor.append(escape(a))

    tips = []
    for t in self.enums_annotations.splitlines():
        tips.append(escape(t))

    default = escape(self.default_value)

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    # issuer and assignor must be the same length as id_name
    if (len(id_name) != len(issuer)) or (len(id_name) != len(assignor)):
        reset_publication(self)
        raise ModellingError("The number of names, issuers and assignors must be exactly equal.")

    #if there isn't exactly one tip for every id name we just overwrite tips with the id names.
    if len(tips) != len(id_name):
        tips = []
        for name in id_name:
            tips.append(name)

    padding = ('').rjust(indent)

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvIdentifierType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvIdentifierType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvIdentifierType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvString

    if self.exact_length or self.min_length or self.max_length:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='DvString-dv'>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")
        if self.exact_length:
            dt_str += padding.rjust(indent+16) + ("<xs:length value='"+str(self.exact_length).strip()+"'/>\n")
        else:
            if self.min_length:
                dt_str += padding.rjust(indent+16) + ("<xs:minLength value='"+str(self.min_length).strip()+"'/>\n")
            if self.max_length:
                dt_str += padding.rjust(indent+16) + ("<xs:maxLength value='"+str(self.max_length)+"'/>\n")

        dt_str += padding.rjust(indent+14) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:element>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='DvString-dv' type='xs:string'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='language' type='xs:language'/>\n")


    #DvIdentifier
    dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='id-name'>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(id_name)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+id_name[n].strip()+"'>\n")
        dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
        dt_str += padding.rjust(indent+18) + ("<xs:appinfo>\n")
        dt_str += padding.rjust(indent+20) + (tips[n].strip()+"\n")
        dt_str += padding.rjust(indent+18) + ("</xs:appinfo>\n")
        dt_str += padding.rjust(indent+16) + ("</xs:annotation>\n")
        dt_str += padding.rjust(indent+16) + ("</xs:enumeration>\n")
    dt_str += padding.rjust(indent+14) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='issuer'>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(id_name)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+issuer[n].strip()+"'/>\n")
    dt_str += padding.rjust(indent+14) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='assignor'>\n")
    dt_str += padding.rjust(indent+12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent+14) + ("<xs:restriction base='xs:string'>\n")
    for n in range(0,len(id_name)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+assignor[n].strip()+"'/>\n")
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

    return dt_str.encode("utf-8")




def publish_DvParsable(self):
    """
    Writes the complete CCD complexType code for the DvParsable itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvParsable')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvParsable')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    f_list = None
    indent = 2

    if self.formalism:
        f_list = []
        for f in self.formalism.splitlines():
            f_list.append(escape(f))

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    padding = ('').rjust(indent)

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvParsableType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvParsableType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvParsableType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvEncapsulated
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='size' type='xs:int'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' default='"+self.encoding.strip()+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='language' type='xs:language' default='"+self.language.strip()+"'/>\n")
    #DvParsable
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='DvParsable-dv' type='xs:string'/>\n")
    if not f_list:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='formalism' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='formalism' type='xs:string'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
        for f in f_list:
            dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+f.strip()+"'/>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

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
    Writes the complete CCD complexType code for the DvMedia itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvMedia')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvMedia')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    dt_str = ''
    mime_list = None
    comp_list = None
    indent = 2

    if self.mime_type:
        mime_list = []
        for m in self.mime_type.splitlines():
            mime_list.append(escape(m))

    if self.compression_type:
        comp_list = []
        for c in self.compression_type.splitlines():
            comp_list.append(escape(c))

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    padding = ('').rjust(indent)

    #Create the datatype
    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvMediaType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvMediaType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvMediaType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name)+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvEncapsulated
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='size' type='xs:int'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' default='"+self.encoding.strip()+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='language' type='xs:language' default='"+self.language.strip()+"'/>\n")
    #DvMedia
    if not mime_list:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='mime-type' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='mime-type'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
        for m in mime_list:
            dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+m.strip()+"'/>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    if not comp_list:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='compression-type' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='compression-type'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+12) + ("<xs:restriction base='xs:string'>\n")
        for c in comp_list:
            dt_str += padding.rjust(indent+14) + ("<xs:enumeration value='"+c.strip()+"'/>\n")
        dt_str += padding.rjust(indent+12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='hash-result' type='xs:string'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='hash-function' type='xs:string' default='"+escape(self.hash_function)+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='alt-txt' type='xs:string' default='"+escape(self.alt_txt)+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='uri' type='xs:anyURI'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='media-content' type='xs:base64Binary'/>\n")



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
    Completed.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvInterval')
    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
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
        raise PublishingError("Enter lower value or uncheck the lower bounded box in "+self.data_name+". ")
    if self.upper_bounded and not self.upper:
        reset_publication(self)
        raise PublishingError("Enter upper value or uncheck the upper bounded box in "+self.data_name+". ")

    if not self.lower_bounded and self.lower:
        reset_publication(self)
        raise PublishingError("Remove lower value or check the lower bounded box in "+self.data_name+". ")
    if not self.upper_bounded and self.upper:
        reset_publication(self)
        raise PublishingError("Remove upper value or check the upper bounded box in "+self.data_name+". ")

    # if the user used a comma as a decimal separator then replace it with a period.
    if self.interval_type == 'decimal':
        if "," in self.lower:
            self.lower = self.lower.replace(",",".")
            self.save()
        if "," in self.upper:
            self.upper = self.upper.replace(",",".")
            self.save()

    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvIntervalType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvIntervalType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvIntervalType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvInterval
    # create an UUIDs for the invl-type restrictions
    lower_id = str(uuid4())
    upper_id = str(uuid4())
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='lower' type='mlhim2:ct-"+lower_id+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='upper' type='mlhim2:ct-"+upper_id+"'/>\n")
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
    dt_str += padding.rjust(indent+6) + ("<xs:restriction base='mlhim2:invl-type'>\n")
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
    dt_str += padding.rjust(indent+6) + ("<xs:restriction base='mlhim2:invl-type'>\n")
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
    Completed.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'ReferenceRange')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()


    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    dt_str = ''
    indent = 2
    rr_def = escape(self.referencerange_definition)
    dvi_id = self.data_range.ct_id
    if self.is_normal:
        normal="true"
    else:
        normal = "false"
    if not self.data_range.published:
        reset_publication(self)
        raise PublishingError("DvInterval: "+self.data_range.data_name+" hasn't been published. Please publish the interval and retry.")

    padding = ('').rjust(indent)

    dt_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    dt_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:ReferenceRangeType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:ReferenceRangeType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:ReferenceRangeType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #ReferenceRange
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='referencerange-definition' type='xs:string' fixed='"+rr_def.strip()+"'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+dvi_id+"'/> <!-- data-range -->\n")
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
    Writes the complete CCD complexType code for the containing Element and the DvOrdinal itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.

    Completed.
    """
    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvOrdinal')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvOrdinal')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvordinal
    dt_str = ''
    indent = 2
    docs = escape(self.description)
    o = []
    for a in self.ordinals.splitlines():
        o.append(escape(a))

    # test that these are really numbers
    for n in o:
        try:
            x = int(n)
        except:
            raise ModellingError(escape(self.data_name.strip())+": You MUST use digits for the Ordinal indicators. It seems one or more of yours is a string.")

    s = []
    for a in self.symbols.splitlines():
        s.append(escape(a))

    tips = []
    for t in self.enums_annotations.splitlines():
        tips.append(escape(t))

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    if len(tips) != len(s): # if the length of tips is not equal the number of symbols copy the symbols to tips
        tips = []
        for n in range(0,len(s)):
            tips.append(' ')
    padding = ('').rjust(indent)

    dt_str = '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (docs + "\n")
    dt_str += padding.rjust(indent+4) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvOrdinalType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvOrdinalType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvOrdinalType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvOrdered
    if len(self.reference_ranges.all()) == 0: # no reference ranges defined
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:reference-ranges'/>\n")
    else:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' default='"+escape(self.normal_status.strip())+"'/> \n")

    #DvOrdinal
    dt_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' name='DvOrdinal-dv'>\n")
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
    for n in range(len(tips)):
        dt_str += padding.rjust(indent+16) + ("<xs:enumeration value='"+s[n].strip()+"'>\n")
        dt_str += padding.rjust(indent+16) + ("<xs:annotation>\n")
        dt_str += padding.rjust(indent+18) + ("<xs:documentation>\n")
        dt_str += padding.rjust(indent+20) + (tips[n].strip()+"\n")
        dt_str += padding.rjust(indent+18) + ("</xs:documentation>\n")
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
    Writes the complete CCD complexType code for the containing Element and the DvCount itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.

    Completed.
    """

    self.ct_id = str(uuid4())
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvCount')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvCount')
    self.save()
    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvcount
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()
    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False


    padding = ('').rjust(indent)

    dt_str = '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (docs +"\n")
    dt_str += padding.rjust(indent+4) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvCountType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvCountType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")

    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvCountType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvOrdered
    if len(self.reference_ranges.all()) == 0: # no reference ranges defined
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:reference-ranges'/>\n")
    else:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' default='"+escape(self.normal_status.strip())+"'/> \n")

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
        dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    #dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='min-magnitude' type='xs:decimal'/>\n")
    #dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='max-magnitude' type='xs:decimal'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:magnitude-status'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='accuracy' type='xs:int' default='0'/>\n")

    #DvCount-units
    if (not self.simple_units) and (not self.coded_units):
        reset_publication(self)
        raise ModellingError("DvCount "+self.data_name+" MUST have either a DvString or a DvCodedString to define the units.")
    elif self.simple_units:
        if not self.simple_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+self.simple_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.simple_units.ct_id+"'/> <!-- DvCount-units -->\n")
    elif self.coded_units:
        if not self.coded_units.published:
            reset_publication(self)
            raise PublishingError( "DvCodedString: "+self.coded_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.coded_units.ct_id+"'/> <!-- DvCount-units -->\n")
    else:
        reset_publication(self)
        raise ModellingError("An unknown error has occurred defining the units for DvCount: "+self.data_name)


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

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvQuantity')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvQuantity')
    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvquantity
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False


    padding = ('').rjust(indent)

    dt_str = '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (docs +"\n")
    dt_str += padding.rjust(indent+4) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvQuantityType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvQuantityType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")

    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvQuantityType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvOrdered
    if len(self.reference_ranges.all()) == 0: # no reference ranges defined
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:reference-ranges'/>\n")
    else:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvQuantity.")
    if not self.normal_status:
        self.normal_status = ''

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' default='"+escape(self.normal_status.strip())+"'/> \n")

    #DvQuantified
    if not mag_constrained:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1'  name='magnitude'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
        if self.min_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str('%.10g' % self.min_inclusive).strip()+"'/>\n")
        if self.max_inclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str('%.10g' % self.max_inclusive).strip().strip()+"'/>\n")
        if self.min_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:minExclusive value='"+str('%.10g' % self.min_exclusive).strip()+"'/>\n")
        if self.max_exclusive != None:
            dt_str += padding.rjust(indent+12) + ("<xs:maxExclusive value='"+str('%.10g' % self.max_exclusive).strip()+"'/>\n")
        if (self.total_digits != None and self.total_digits > 0):
            dt_str += padding.rjust(indent+12) + ("<xs:totalDigits value='"+str(self.total_digits).strip()+"'/>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:magnitude-status'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='accuracy' type='xs:int' default='0'/>\n")


    #DvQuantity-units
    if (not self.simple_units) and (not self.coded_units):
        reset_publication(self)
        raise ModellingError("DvQuantity "+self.data_name+" MUST have either a DvString or a DvCodedString to define the units.")
    elif self.simple_units:
        if not self.simple_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+self.simple_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.simple_units.ct_id+"'/> <!-- DvQuantity-units -->\n")
    elif self.coded_units:
        if not self.coded_units.published:
            reset_publication(self)
            raise PublishingError( "DvCodedString: "+self.coded_units.data_name+" hasn't been published. Please publish the object and retry.")
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.coded_units.ct_id+"'/> <!-- DvQuantity-units -->\n")
    else:
        reset_publication(self)
        raise ModellingError("An unknown error has occurred defining the units for DvQuantity: "+self.data_name)

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

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvRatio')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvRatio')
    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvratio
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()
    # Is the magnitude constrained?
    if self.min_magnitude or self.max_magnitude:
        mag_constrained = True
    else:
        mag_constrained = False

    padding = ('').rjust(indent)

    dt_str = '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (docs +"\n")
    dt_str += padding.rjust(indent+4) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvRatioType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvRatioType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")

    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvRatioType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvOrdered
    if len(self.reference_ranges.all()) == 0: # no reference ranges defined
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:reference-ranges'/>\n")
    else:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' default='"+escape(self.normal_status.strip())+"'/> \n")

    #DvQuantified
    if not mag_constrained:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='magnitude' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0'  name='magnitude'>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent+10) + ("<xs:restriction base='xs:decimal'>\n")
        if self.min_magnitude:
            dt_str += padding.rjust(indent+12) + ("<xs:minInclusive value='"+str(self.min_magnitude).strip()+"'/>\n")
        if self.max_magnitude:
            dt_str += padding.rjust(indent+12) + ("<xs:maxInclusive value='"+str(self.max_magnitude).strip()+"'/>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:magnitude-status'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='accuracy' type='xs:int' default='0'/>\n")
    #DvRatio
    # tests for proper modelling
    if (self.num_min_inclusive and self.num_min_exclusive) or (self.num_max_inclusive and self.num_max_exclusive):
        reset_publication(self)
        raise ModellingError("There is ambiguity in your numerator constraints for min/max.")
    if (self.den_min_inclusive and self.den_min_exclusive) or (self.den_max_inclusive and self.den_max_exclusive):
        reset_publication(self)
        raise ModellingError("There is ambiguity in your denominator constraints for min/max.")

    if self.num_simple_units and self.num_coded_units:
        reset_publication(self)
        raise ModellingError("There is ambiguity in your numerator units selection. Simple and Coded both selected.")
    if self.den_simple_units and self.den_coded_units:
        reset_publication(self)
        raise ModellingError("There is ambiguity in your denominator units selection. Simple and Coded both selected.")
    if self.ratio_simple_units and self.ratio_coded_units:
        reset_publication(self)
        raise ModellingError("There is ambiguity in your ratio units selection. Simple and Coded both selected.")

    # tests for not reusing units PcT
    if self.num_simple_units is not None and self.den_simple_units is not None:
        if self.num_simple_units.ct_id == self.den_simple_units.ct_id:
            reset_publication(self)
            raise ModellingError("Numerator and denominator units must use different PcTs.")

    if self.num_simple_units is not None and self.ratio_simple_units is not None:
        if self.num_simple_units.ct_id == self.ratio_simple_units.ct_id:
            reset_publication(self)
            raise ModellingError("Numerator and ratio units must use different PcTs.")

    if self.den_simple_units is not None and self.ratio_simple_units is not None:
        if self.den_simple_units.ct_id == self.ratio_simple_units.ct_id:
            reset_publication(self)
            raise ModellingError("Denominator and ratio units must use different PcTs.")

    if self.num_coded_units is not None and self.den_coded_units is not None:
        if self.num_coded_units.ct_id == self.den_coded_units.ct_id:
            reset_publication(self)
            raise ModellingError("Numerator and denominator units must use different PcTs.")

    if self.num_coded_units is not None and self.ratio_coded_units is not None:
        if self.num_coded_units.ct_id == self.ratio_coded_units.ct_id:
            reset_publication(self)
            raise ModellingError("Numerator and ratio units must use different PcTs.")

    if self.den_coded_units is not None and self.ratio_coded_units is not None:
        if self.den_coded_units.ct_id == self.ratio_coded_units.ct_id:
            reset_publication(self)
            raise ModellingError("Denominator and ratio units must use different PcTs.")


    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:ratio-type'/>\n")

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
    dt_str += padding.rjust(indent+10) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent+10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent+8) + ("</xs:element>\n")

    num_units_id = ''
    if self.num_simple_units:
        if not self.num_simple_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+num_simple_units.data_name+" hasn't been published. Please publish the object and retry.")
        num_units_id = self.num_simple_units.ct_id
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.num_simple_units.ct_id+"'/> <!-- numerator-units -->\n")
    elif self.num_coded_units:
        if not self.num_coded_units.published:
            reset_publication(self)
            raise PublishingError( "DvCodedString: "+self.num_coded_units.data_name+" hasn't been published. Please publish the object and retry.")
        num_units_id = self.num_coded_units.ct_id
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.num_coded_units.ct_id+"'/> <!-- numerator-units -->\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:numerator-units'/>\n")

    den_units_id = ''
    if self.den_simple_units:
        if not self.den_simple_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+self.den_simple_units.data_name+" hasn't been published. Please publish the object and retry.")
        den_units_id = self.den_simple_units.ct_id
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.den_simple_units.ct_id+"'/> <!-- denominator-units -->\n")
    elif self.den_coded_units:
        if not self.den_coded_units.published:
            reset_publication(self)
            raise PublishingError( "DvCodedString: "+self.den_coded_units.data_name+" hasn't been published. Please publish the object and retry.")
        den_units_id = self.den_coded_units.ct_id
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.den_coded_units.ct_id+"'/> <!-- denominator-units -->\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:denominator-units'/>\n")

    ratio_units_id = ''
    if self.ratio_simple_units:
        if not self.ratio_simple_units.published:
            reset_publication(self)
            raise PublishingError( "DvString: "+self.ratio_simple_units.data_name+" hasn't been published. Please publish the object and retry.")
        ratio_units_id = self.ratio_simple_units.ct_id
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.ratio_simple_units.ct_id+"'/> <!-- ratio-units -->\n")
    elif self.ratio_coded_units:
        if not self.ratio_coded_units.published:
            reset_publication(self)
            raise PublishingError( "DvCodedString: "+self.ratio_coded_units.data_name+" hasn't been published. Please publish the object and retry.")
        ratio_units_id = self.ratio_coded_units.ct_id
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.ratio_coded_units.ct_id+"'/> <!-- ratio-units -->\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ratio-units'/>\n")

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

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'DvTemporal')
    self.save()

    # generate and save the code for a XQuery function.
    self.xqr_code = pct_xqrcode(self, 'DvTemporal')
    self.save()

    # fix double quotes in data-name
    self.data_name.replace('"','&quot;')
    self.save()

    used_ctid_list = [] # it is a modelling error to use multiple reference ranges with the same dvinterval in a dvtemporal
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()
    padding = ('').rjust(indent)

    dt_str = '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.data_name)+" -->\n")
    dt_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent+4) + (docs + "\n")
    dt_str += padding.rjust(indent+4) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    dt_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvTemporalType'/>\n")
            dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
            dt_str += padding.rjust(indent+4) + ("<"+sa[n]+" rdf:resource='"+quote(ru[n])+"'/>\n")
            dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DvTemporalType'/>\n")
        dt_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.data_name.strip())+"</rdfs:label>\n")
        dt_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvTemporalType'>\n")
    dt_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #DvAny
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='data-name' type='xs:string' fixed="+'"'+escape(self.data_name.strip())+'"'+"/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-begin' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='valid-time-end' type='xs:dateTime'/>\n")
    #DvOrdered
    if len(self.reference_ranges.all()) == 0: # no reference ranges defined
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:reference-ranges'/>\n")
    else:
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                raise PublishingError("Reference Range: "+rr.data_name+" hasn't been published. Please publish the reference range and retry.")
            else:
                dt_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+rr.ct_id+"'/> <!-- reference-ranges -->\n"
                if rr.data_range.ct_id not in used_ctid_list:
                    used_ctid_list.append(rr.data_range.ct_id) # track the used DvInterval IDs
                else:
                    reset_publication(self)
                    raise ModellingError("You cannot use multiple ReferenceRanges with the same DvInterval declared as the data-range in one DvOrdinal.")
    if not self.normal_status:
        self.normal_status = ''
    dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='normal-status' type='xs:string' default='"+self.normal_status.strip()+"'/> \n")

    #DvTemporal - every element must be included as either allowed or not allowed.
    if (self.allow_duration and self.allow_ymduration) or (self.allow_duration and self.allow_dtduration) or (self.allow_ymduration and self.allow_dtduration):
        reset_publication(self)
        raise ModellingError("Only one of the duration types are allowed to be selected.")

    if (self.allow_duration or self.allow_ymduration or self.allow_dtduration) and (self.allow_date or self.allow_time or self.allow_datetime or self.allow_day or self.allow_month or self.allow_year or self.allow_year_month or self.allow_month_day):
        reset_publication(self)
        raise ModellingError("You cannot have a duration mixed with other temporal types.")

    if self.allow_date:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-date' type='xs:date'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-date' type='xs:date'/>\n")

    if self.allow_time:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-time' type='xs:time'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-time' type='xs:time'/>\n")

    if self.allow_datetime:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-datetime' type='xs:dateTime'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-datetime' type='xs:dateTime'/>\n")

    if self.allow_day:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-day' type='xs:gDay'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-day' type='xs:gDay'/>\n")

    if self.allow_month:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-month' type='xs:gMonth'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-month' type='xs:gMonth'/>\n")

    if self.allow_year:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-year' type='xs:gYear'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-year' type='xs:gYear'/>\n")

    if self.allow_year_month:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-year-month' type='xs:gYearMonth'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-year-month' type='xs:gYearMonth'/>\n")

    if self.allow_month_day:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-month-day' type='xs:gMonthDay'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-month-day' type='xs:gMonthDay'/>\n")

    if self.allow_duration:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-duration' type='xs:duration'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-duration' type='xs:duration'/>\n")

    if self.allow_ymduration:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-ymduration' type='xs:yearMonthDuration'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-ymduration' type='xs:yearMonthDuration'/>\n")

    if self.allow_dtduration:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='dvtemporal-dtduration' type='xs:dayTimeDuration'/>\n")
    else:
        dt_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='0' minOccurs='0' name='dvtemporal-dtduration' type='xs:dayTimeDuration'/>\n")


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
    xref_id = None

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    party_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    party_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    party_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    party_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    party_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    party_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            party_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            party_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:PartyType'/>\n")
            party_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            party_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        party_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        party_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:PartyType'/>\n")
        party_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    party_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    party_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    party_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    party_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:PartyType'>\n")
    party_str += padding.rjust(indent+6) + ("<xs:sequence>\n")

    if not self.party_name:
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='party-name' type='xs:string'/>\n")
    else:
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='party-name' type='xs:string' default='"+escape(self.party_name.strip())+"'/>\n")

    if not self.external_ref.all():
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:external-ref'/>\n")
    else:
        for xref in self.external_ref.all():
            if not xref.published:
                reset_publication(self)
                raise PublishingError("External Reference: "+xref.data_name+" hasn't been published. Please publish the DvURI and retry.")
            else:
                party_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+xref.ct_id+"'/> <!-- external-ref -->\n"

    if not self.details:
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:details'/>\n")
    else:
        if not self.details.published:
            reset_publication(self)
            raise PublishingError("Cluster: "+self.details.cluster_subject+" hasn't been published. Please publish the item and retry.")
        party_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.details.ct_id+"'/> <!-- details -->\n")

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

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    aud_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    aud_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    aud_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    aud_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    aud_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    aud_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            aud_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            aud_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:AuditType'/>\n")
            aud_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            aud_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        aud_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        aud_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:AuditType'/>\n")
        aud_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    aud_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    aud_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    aud_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    aud_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:AuditType'>\n")
    aud_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #FeederAuditDetails
    if not self.system_id:
        raise PublishingError("System ID: (DvIdentifier) has not been selected.")
    else:
        if not self.system_id.published:
            reset_publication(self)
            raise PublishingError("System ID: (DvIdentifier) "+self.system_id.data_name+" has not been published.")
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.system_id.ct_id+"'/> <!-- system-id -->\n")

    if not self.system_user:
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:system-user'/>\n")
    else:
        if not self.system_user.published:
            reset_publication(self)
            raise PublishingError("System User: (Party) "+self.system_user.label+" has not been published.")
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.system_user.ct_id+"'/> <!-- system-user -->\n")

    if not self.location:
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:location'/>\n")
    else:
        if not self.location.published:
            reset_publication(self)
            raise PublishingError("Location: (Cluster) "+self.location.cluster_subject+" has not been published.")
        aud_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.location.ct_id+"'/> <!-- location -->\n")

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

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    att_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    att_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    att_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    att_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    att_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    att_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            att_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            att_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:AttestationType'/>\n")
            att_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            att_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        att_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        att_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:AttestationType'/>\n")
        att_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    att_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    att_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    att_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    att_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:AttestationType'>\n")
    att_str += padding.rjust(indent+6) + ("<xs:sequence>\n")

    if not self.attested_view:
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:attested-view'/>\n")
    else:
        if not self.attested_view.published:
            reset_publication(self)
            raise PublishingError("AttestedView: (DvMedia) "+self.attested_view.data_name+" has not been published.")
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.attested_view.ct_id+"'/> <!-- attested-view -->\n")

    if not self.proof:
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:proof'/>\n")
    else:
        if not self.proof.published:
            reset_publication(self)
            raise PublishingError("Proof: (DvParsable) "+self.proof.data_name+" has not been published.")
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.proof.ct_id+"'/> <!-- proof -->\n")

    if (not self.reason) and (not self.simple_reason):
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:reason'/>\n")
    elif self.simple_reason:
        if not self.simple_reason.published:
            reset_publication(self)
            raise PublishingError("Reason: (DvString) "+self.simple_reason.data_name+" has not been published.")
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.simple_reason.ct_id+"'/> <!-- reason -->\n")
    elif self.reason:
        if not self.reason.published:
            reset_publication(self)
            raise PublishingError("Reason: (DvCodedString) "+self.reason.data_name+" has not been published.")
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.reason.ct_id+"'/> <!-- reason -->\n")
    else:
        reset_publication(self)
        raise ModellingError("An unknown error has occurred defining the reason for Attestation: "+self.label)

    if not self.committer_p:
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:committer'/>\n")
    else:
        if not self.committer_p.published:
            reset_publication(self)
            raise PublishingError("Committer: (Party) "+self.committer_p.label+" has not been published.")
        att_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.committer_p.ct_id+"'/> <!-- committer -->\n")

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
    Writes the complete CCD complexType code for the Participation.
    """
    self.ct_id = str(uuid4())
    self.save()

    ptn_str = ''

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    ptn_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"' xml:lang='"+self.lang+"'> <!-- "+escape(self.label)+" -->\n")
    ptn_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    ptn_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    ptn_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    ptn_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    ptn_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            ptn_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            ptn_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:ParticipationType'/>\n")
            ptn_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            ptn_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        ptn_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        ptn_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:ParticipationType'/>\n")
        ptn_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    ptn_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    ptn_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    ptn_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    ptn_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:ParticipationType'>\n")
    ptn_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    #Participation
    if not self.performer_p:
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:performer'/>\n")
    else:
        if not self.performer_p.published:
            reset_publication(self)
            raise PublishingError("Performer: "+self.performer_p.label+" hasn't been published. Please publish the DvURI and retry.")
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.performer_p.ct_id+"'/> <!-- performer -->\n")

    if (not self.function) and (not self.simple_function):
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:function'/>\n")
    elif self.simple_function:
        if not self.simple_function.published:
            reset_publication(self)
            raise PublishingError("Function: (DvString) "+self.simple_function.data_name+" has not been published.")
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.simple_function.ct_id+"'/> <!-- function -->\n")
    elif self.function:
        if not self.function.published:
            reset_publication(self)
            raise PublishingError("Function: (DvCodedString) "+self.function.data_name+" has not been published.")
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.function.ct_id+"'/> <!-- function -->\n")
    else:
        reset_publication(self)
        raise ModellingError("An unknown error has occurred defining the function for Participation: "+self.label)

    if (not self.mode) and (not self.simple_mode):
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:mode'/>\n")
    elif self.simple_mode:
        if not self.simple_mode.published:
            reset_publication(self)
            raise PublishingError("Mode: (DvString) "+self.simple_mode.data_name+" has not been published.")
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.simple_mode.ct_id+"'/> <!-- mode -->\n")
    elif self.mode:
        if not self.mode.published:
            reset_publication(self)
            raise PublishingError("Mode: (DvCodedString) "+self.mode.data_name+" has not been published.")
        ptn_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.mode.ct_id+"'/> <!-- mode -->\n")
    else:
        reset_publication(self)
        raise ModellingError("An unknown error has occurred defining the function for Participation: "+self.label)

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

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    cl_str += '\n\n'+padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"'> <!-- "+escape(self.cluster_subject)+" -->\n")
    cl_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    cl_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    cl_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    cl_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    cl_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            cl_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            cl_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:ClusterType'/>\n")
            cl_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.cluster_subject.strip())+"</rdfs:label>\n")
            cl_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            cl_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        cl_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        cl_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:ClusterType'/>\n")
        cl_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.cluster_subject.strip())+"</rdfs:label>\n")
        cl_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    cl_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    cl_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    cl_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    cl_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:ClusterType'>\n")
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

    if self.dvuri.all():
        has_content = True
        for item in self.dvuri.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvURI) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvURI "+item.data_name+" -->\n")

    if self.dvstring.all():
        has_content = True
        for item in self.dvstring.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvString) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvString "+item.data_name+" -->\n")

    if self.dvcodedstring.all():
        has_content = True
        for item in self.dvcodedstring.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvCodedString) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvCodedString "+item.data_name+" -->\n")

    if self.dvidentifier.all():
        has_content = True
        for item in self.dvidentifier.all():
            if not item.published:
                reset_publication(self)
                raise PublishingError( "(DvIdentifier) "+item.data_name+" hasn't been published. Please publish the object and retry.")
            cl_str += padding.rjust(indent+4) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+item.element_ctid+"'/><!-- DvIdentifier "+item.data_name+" -->\n")

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


def publish_AdminEntry(self):
    """
    Publish an AdminEntry definition.

    """
    self.ct_id = str(uuid4())
    self.save()

    entry_str = ''
    links_id = None
    op_id = None

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    entry_str += padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"'> <!-- "+escape(self.entry_name)+" -->\n")
    entry_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    entry_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    entry_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    entry_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    entry_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            entry_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            entry_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:AdminEntryType'/>\n")
            entry_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            entry_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        entry_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        entry_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:AdminEntryType'/>\n")
        entry_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    entry_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    entry_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    entry_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    entry_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:AdminEntryType'>\n")
    entry_str += padding.rjust(indent+6) + ("<xs:sequence>\n")


    if not self.entry_links.all():
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='unbounded' minOccurs='0' ref='mlhim2:entry-links'/>\n")
    else:
        for link in self.entry_links.all():
            if not link.published:
                reset_publication(self)
                raise PublishingError("Link: "+link.data_name+" hasn't been published. Please publish the DvURI and retry.")
            else:
                entry_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+link.ct_id+"'/> <!-- entry-links -->\n"

    if not self.audit:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:entry-audit'/>\n")
    else:
        if not self.audit.published:
            reset_publication(self)
            raise PublishingError("Audit "+self.audit.label+" has not been published.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.audit.ct_id+"'/> <!-- entry-audit -->\n")


    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='language' type='xs:language' fixed='"+self.language+"'/>\n")
    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' fixed='"+self.encoding+"'/>\n")


    if self.entry_subject:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.entry_subject.ct_id+"'/> <!-- entry-subject -->\n")
    else:
        reset_publication(self)
        raise ModellingError("Entry "+self.entry_name+" must have a subject (PartyType) defined.")

    if not self.entry_provider_p:
        reset_publication(self)
        raise ModellingError("Entry "+self.entry_name+" must have a provider defined.")
    else:
        if not self.entry_provider_p.published:
            reset_publication(self)
            raise PublishingError("Entry "+self.entry_provider_p.label+" must be published before publishing the entry.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.entry_provider_p.ct_id+"'/> <!-- entry-provider -->\n")


    if not self.other_participations.all():
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:other-participations'/>\n")
    else:
        for op in self.other_participations.all():
            if not op.published:
                reset_publication(self)
                raise PublishingError("Participation: "+op.label+" hasn't been published. Please publish the Participation and retry.")
            else:
                entry_str += padding.rjust(indent+8) +"<xs:element maxOccurs='unbounded' minOccurs='0' ref='mlhim2:el-"+op.ct_id+"'/> <!-- other-participations -->\n"


    if not self.protocol_id:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:protocol-id'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.protocol_id.ct_id+"'/> <!-- protocol-id -->\n")

    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='current-state' type='xs:string' default='"+escape(self.current_state)+"'/>\n")

    if not self.workflow_id:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:workflow-id'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.workflow_id.ct_id+"'/> <!-- workflow-id -->\n")

    if not self.attestation:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:attestation'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.attestation.ct_id+"'/> <!-- attestation -->\n")

    if not self.entry_data:
        reset_publication(self)
        raise ModellingError("You cannot publish an Entry without an entry_data element; a Cluster.")
    else:
        if not self.entry_data.published:
            reset_publication(self)
            raise PublishingError("Cluster "+self.entry_data.cluster_subject+" must be published before publishing the entry.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.entry_data.ct_id+"'/> <!-- entry-data -->\n")


    entry_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            entry_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    entry_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    entry_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    entry_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return entry_str.encode("utf-8")


def publish_CareEntry(self):
    """
    Publish an CareEntry definition.

    """
    self.ct_id = str(uuid4())
    self.save()

    entry_str = ''
    links_id = None
    op_id = None

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    entry_str += padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"'> <!-- "+escape(self.entry_name)+" -->\n")
    entry_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    entry_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    entry_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    entry_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    entry_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            entry_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            entry_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:CareEntryType'/>\n")
            entry_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            entry_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        entry_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        entry_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:CareEntryType'/>\n")
        entry_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    entry_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    entry_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    entry_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    entry_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:CareEntryType'>\n")
    entry_str += padding.rjust(indent+6) + ("<xs:sequence>\n")


    if not self.entry_links.all():
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='unbounded' minOccurs='0' ref='mlhim2:entry-links'/>\n")
    else:
        for link in self.entry_links.all():
            if not link.published:
                reset_publication(self)
                raise PublishingError("Link: "+link.data_name+" hasn't been published. Please publish the DvURI and retry.")
            else:
                entry_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+link.ct_id+"'/> <!-- entry-links -->\n"

    if not self.audit:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:entry-audit'/>\n")
    else:
        if not self.audit.published:
            reset_publication(self)
            raise PublishingError("Audit "+self.audit.label+" has not been published.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.audit.ct_id+"'/> <!-- entry-audit -->\n")
    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='language' type='xs:language' fixed='"+self.language+"'/>\n")
    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' fixed='"+self.encoding+"'/>\n")

    if self.entry_subject:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.entry_subject.ct_id+"'/> <!-- entry-subject -->\n")
    else:
        reset_publication(self)
        raise ModellingError("Entry "+self.entry_name+" must have a subject (PartyType) defined.")

    if not self.entry_provider_p:
        reset_publication(self)
        raise ModellingError("Entry "+self.entry_name+" must have a provider defined.")
    else:
        if not self.entry_provider_p.published:
            reset_publication(self)
            raise PublishingError("Entry "+self.entry_provider_p.label+" must be published before publishing the entry.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.entry_provider_p.ct_id+"'/> <!-- entry-provider -->\n")


    if not self.other_participations.all():
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:other-participations'/>\n")
    else:
        for op in self.other_participations.all():
            if not op.published:
                reset_publication(self)
                raise PublishingError("Participation: "+op.label+" hasn't been published. Please publish the Participation and retry.")
            else:
                entry_str += padding.rjust(indent+6) +"<xs:element maxOccurs='unbounded' minOccurs='0' ref='mlhim2:el-"+op.ct_id+"'/> <!-- other-participations -->\n"


    if not self.protocol_id:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:protocol-id'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.protocol_id.ct_id+"'/> <!-- protocol-id -->\n")

    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='current-state' type='xs:string' default='"+escape(self.current_state)+"'/>\n")

    if not self.workflow_id:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:workflow-id'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.workflow_id.ct_id+"'/> <!-- workflow-id -->\n")

    if not self.attestation:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:attestation'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.attestation.ct_id+"'/> <!-- attestation -->\n")

    if not self.entry_data:
        reset_publication(self)
        raise ModellingError("You cannot publish an Entry without an entry_data element; a Cluster.")
    else:
        if not self.entry_data.published:
            reset_publication(self)
            raise PublishingError("Cluster "+self.entry_data.cluster_subject+" must be published before publishing the entry.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.entry_data.ct_id+"'/> <!-- entry-data -->\n")


    entry_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            entry_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    entry_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    entry_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    entry_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return entry_str.encode("utf-8")


def publish_DemographicEntry(self):
    """
    Publish a DemographicEntry definition.

    """
    self.ct_id = str(uuid4())
    self.save()

    entry_str = ''
    links_id = None
    op_id = None

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()

    indent = 2
    padding = ('').rjust(indent)

    #Create the datatype
    entry_str += padding.rjust(indent) + ("<xs:complexType name='ct-"+self.ct_id+"'> <!-- "+escape(self.entry_name)+" -->\n")
    entry_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    entry_str += padding.rjust(indent+2) + ("<xs:documentation>\n")
    entry_str += padding.rjust(indent+4) + (escape(self.description)+"\n")
    entry_str += padding.rjust(indent+2) + ("</xs:documentation>\n")
    #Write the semantic links. There must be the same number of attributes and links or none will be written.
    entry_str += padding.rjust(indent+2) + ('<xs:appinfo>\n')
    if len(ru) == len(sa):
        for n in range(0,len(sa)):
            entry_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
            entry_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DemographicEntryType'/>\n")
            entry_str += padding.rjust(indent+2) + ("<"+sa[n]+" rdf:resource='"+ quote(ru[n]) +"'/>\n")
            entry_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    else:
        entry_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
        entry_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:DemographicEntryType'/>\n")
        entry_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    entry_str += padding.rjust(indent+2) + ('</xs:appinfo>\n')
    entry_str += padding.rjust(indent+2) + ("</xs:annotation>\n")
    entry_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    entry_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DemographicEntryType'>\n")
    entry_str += padding.rjust(indent+6) + ("<xs:sequence>\n")



    if not self.entry_links.all():
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='unbounded' minOccurs='0' ref='mlhim2:entry-links'/>\n")
    else:
        for link in self.entry_links.all():
            if not link.published:
                reset_publication(self)
                raise PublishingError("Link: "+link.data_name+" hasn't been published. Please publish the DvURI and retry.")
            else:
                entry_str += padding.rjust(indent+8) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+link.ct_id+"'/> <!-- entry-links -->\n"

    if not self.audit:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:entry-audit'/>\n")
    else:
        if not self.audit.published:
            reset_publication(self)
            raise PublishingError("Audit "+self.audit.label+" has not been published.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.audit.ct_id+"'/> <!-- entry-audit -->\n")


    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='language' type='xs:language' fixed='"+self.language+"'/>\n")
    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' fixed='"+self.encoding+"'/>\n")

    if self.entry_subject:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.entry_subject.ct_id+"'/> <!-- entry-subject -->\n")
    else:
        reset_publication(self)
        raise ModellingError("Entry "+self.entry_name+" must have a subject (PartyType) defined.")

    if not self.entry_provider_p:
        reset_publication(self)
        raise ModellingError("Entry "+self.entry_name+" must have a provider defined.")
    else:
        if not self.entry_provider_p.published:
            reset_publication(self)
            raise PublishingError("Entry "+self.entry_provider_p.label+" must be published before publishing the entry.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.entry_provider_p.ct_id+"'/> <!-- entry-provider -->\n")

    if not self.other_participations.all():
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='unbounded' minOccurs='0' ref='mlhim2:other-participations'/>\n")
    else:
        for op in self.other_participations.all():
            if not op.published:
                reset_publication(self)
                raise PublishingError("Participation: "+op.label+" hasn't been published. Please publish the Participation and retry.")
            else:
                entry_str += padding.rjust(indent+6) +"<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+op.ct_id+"'/> <!-- other-participations -->\n"


    if not self.protocol_id:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:protocol-id'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.protocol_id.ct_id+"'/> <!--  -->\n")
    entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' name='current-state' type='xs:string' default='"+escape(self.current_state)+"'/>\n")

    if not self.workflow_id:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:workflow-id'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.workflow_id.ct_id+"'/> <!-- workflow-id -->\n")

    if not self.attestation:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:attestation'/>\n")
    else:
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='0' ref='mlhim2:el-"+self.attestation.ct_id+"'/> <!-- attestation -->\n")

    if not self.entry_data:
        reset_publication(self)
        raise ModellingError("You cannot publish an Entry without an entry_data element; a Cluster.")
    else:
        if not self.entry_data.published:
            reset_publication(self)
            raise PublishingError("Cluster "+self.entry_data.cluster_subject+" must be published before publishing the entry.")
        entry_str += padding.rjust(indent+8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+self.entry_data.ct_id+"'/> <!-- entry-data -->\n")


    entry_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            entry_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    entry_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    entry_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    entry_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")

    return entry_str.encode("utf-8")


def publish_CCD(self):
    """
    Publishing a CCD puts the code into the database similar to the other publication functions.
    Generating a CCD actually produces the full schema file.

    """
    self.ct_id = str(uuid4())
    self.identifier = 'ccd-'+self.ct_id
    self.save()

    doc_str = "<b>Concept Constraint Definition (CCD)</b><br />\n<div class='ccd_md collapsed'><br /><p style='font-size: larger;'> CCD Meta-Data:</p>\n<div class='content'>\n"
    ccd_str = ''
    rm_ver = self.prj_name.rm_version

    # fix double quotes in title
    self.title.replace('"','&quot;')
    self.save()

    # fix previously bad default
    self.sem_attr = self.sem_attr.replace('rdf:isDefinedBy','rdfs:isDefinedBy')
    self.save()

    sa = self.sem_attr.splitlines()
    ru = self.resource_uri.splitlines()
    if self.contrib_names:
        contrib_names = []
        for c in self.contrib_names.splitlines():
            contrib_names.append(escape(c))

        contrib_emails = []
        for c in self.contrib_emails.splitlines():
            contrib_emails.append(escape(c))

        if len(contrib_names) != len(contrib_emails):
            self.schema_code = ''
            self.save()
            raise ModellingError("The number of contributor names and email addresses are not the same. Please correct and retry.")
    else:
        contrib_names = None

    entry_id = None
    if self.admin_definition:
        entry_id = self.admin_definition.ct_id
    elif self.care_definition:
        entry_id = self.care_definition.ct_id
    elif self.demog_definition:
        entry_id = self.demog_definition.ct_id
    else:
        self.schema_code = ''
        self.save()
        raise ModellingError("You must define either a Care, Admin or Demographic entry.")

    indent = 0
    padding = ('').rjust(indent)

    #Create the schema header and the HTML documentation
    ccd_str += padding.rjust(indent) + ("<?xml version='1.0' encoding='UTF-8'?>\n")
    ccd_str += padding.rjust(indent) + ("<?xml-stylesheet type='text/xsl' href='ccd-description.xsl'?>\n")
    ccd_str += padding.rjust(indent) + ("<xs:schema  xmlns:xs='http://www.w3.org/2001/XMLSchema'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:owl='http://www.w3.org/2002/07/owl#'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:dc='http://purl.org/dc/elements/1.1/'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:sawsdl='http://www.w3.org/ns/sawsdl'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:sawsdlrdf='http://www.w3.org/ns/sawsdl#'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:vc='http://www.w3.org/2007/XMLSchema-versioning'\n")
    ccd_str += padding.rjust(indent+2) + ("xmlns:mlhim2='http://www.mlhim.org/xmlns/mlhim2'\n")
    ccd_str += padding.rjust(indent+2) + ("targetNamespace='http://www.mlhim.org/xmlns/mlhim2'\n")
    ccd_str += padding.rjust(indent+2) + ("vc:minVersion='1.1'\n")
    ccd_str += padding.rjust(indent) + ("xml:lang='"+self.dc_language+"'>\n\n")

    ccd_str += padding.rjust(indent+2) + ("<!-- Include the Reference Model -->\n")
    ccd_str += padding.rjust(indent+2) + ("<xs:include schemaLocation='http://www.mlhim.org/xmlns/mlhim2/mlhim"+rm_ver.version_id.replace('.','')+".xsd'/>\n\n")

    ccd_str += padding.rjust(indent+2) + ("<!-- METADATA Section -->\n")
    ccd_str += padding.rjust(indent+2) + ("<xs:annotation>\n")
    ccd_str += padding.rjust(indent+4) + ("<xs:appinfo>\n")
    ccd_str += padding.rjust(indent+4) + ("<rdf:RDF>\n")
    if 'hkcr.net' in self.about: # update the about field of old CCDs.
        self.about = 'http://www.ccdgen.com/ccdlib/'
        self.save()

    ccd_str += padding.rjust(indent+4) + ("<rdf:Description rdf:about='"+self.about.strip()+"ccd-"+self.ct_id+".xsd'>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:title>"+escape(self.title.strip())+"</dc:title>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:creator>"+escape(self.creator_name.strip())+" "+escape(self.creator_email.strip())+"</dc:creator>\n")
    doc_str += ("<b>Created By:</b>&nbsp;&nbsp;\n")
    doc_str += (self.creator_name.strip()+" "+self.creator_email.strip()+"<br />\n")
    doc_str += ("<b>Contributors:</b><br/>\n")
    if contrib_names:
        for x in range(0,len(contrib_names)):
            ccd_str += padding.rjust(indent+6) + ("<dc:contributor>"+escape(contrib_names[x])+" "+escape(contrib_emails[x])+"</dc:contributor>\n")
            doc_str += (contrib_names[x]+" "+contrib_emails[x]+"<br/>\n")
    else:
        ccd_str += padding.rjust(indent+6) + ("<dc:contributor>None</dc:contributor>\n")
        doc_str += ("No Other Contributors<br/>\n")

    ccd_str += padding.rjust(indent+6) + ("<dc:subject>"+escape(self.subject)+";"+self.prj_name.prj_name.strip()+"</dc:subject>\n")
    doc_str += ("<b>Keywords: </b>&nbsp;&nbsp;"+self.subject+";"+self.prj_name.prj_name.strip()+";<br/>\n")

    ccd_str += padding.rjust(indent+6) + ("<dc:source>"+self.source+"</dc:source>\n")
    doc_str += ("<b>Source: </b>"+self.source+"<br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:rights>"+self.rights+"</dc:rights>\n")
    doc_str += ("<b>Rights: </b>"+self.rights+"<br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:relation>"+escape(self.relation.strip())+"</dc:relation>\n")
    doc_str += ("<b>Related to: </b>&nbsp;&nbsp;"+self.relation+"<br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:coverage>"+escape(self.coverage.strip())+"</dc:coverage>\n")
    doc_str += ("<b>Coverage: </b>&nbsp;&nbsp;"+self.coverage+"<br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:type>"+self.dc_type+"</dc:type>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:identifier>"+self.identifier+"</dc:identifier>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:description>\n        "+escape(self.description)+"\n        This CCD was created by the CCD-Gen application.\n")
    ccd_str += padding.rjust(indent+6) + ("</dc:description>\n")
    doc_str += ("<b>Description: </b>&nbsp;&nbsp;"+self.description+"<br/><br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:publisher>"+escape(self.publisher.strip())+"</dc:publisher>\n")
    doc_str += ("<b>Published By: </b>&nbsp;&nbsp;"+self.publisher+"<br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:date>"+str(self.pub_date)+"</dc:date>\n")
    doc_str += ("<b>Publication Date/Time: </b>&nbsp;&nbsp;"+str(self.pub_date)+"<br/>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:format>"+self.dc_format+"</dc:format>\n")
    ccd_str += padding.rjust(indent+6) + ("<dc:language>"+self.dc_language+"</dc:language>\n")
    doc_str += ("<b>Language: </b>"+self.dc_language+"<br/>\n")
    doc_str += ("<b>MLHIM Reference Model Version: </b>&nbsp;&nbsp;"+rm_ver.version_id+"<br/>\n")
    ccd_str += padding.rjust(indent+4) + ("</rdf:Description>\n")
    ccd_str += padding.rjust(indent+2) + ("<rdf:Description rdf:about='http://www.mlhim.org/xmlns/mlhim2:ct-"+self.ct_id+"'>\n")
    ccd_str += padding.rjust(indent+2) + ("<rdfs:subClassOf rdf:resource='mlhim2:CCDType'/>\n")
    ccd_str += padding.rjust(indent+2) + ("<rdfs:label>"+escape(self.title.strip())+"</rdfs:label>\n")
    ccd_str += padding.rjust(indent+2) + ("</rdf:Description>\n")
    ccd_str += padding.rjust(indent+4) + ("</rdf:RDF>\n")
    ccd_str += padding.rjust(indent+4) + ("</xs:appinfo>\n")
    ccd_str += padding.rjust(indent+2) + ("</xs:annotation>\n\n")

    ccd_str += padding.rjust(indent+2) + ("<!-- CCD Root Element -->\n")
    ccd_str += padding.rjust(indent+2) + ("<xs:element name='"+self.identifier+"' type='mlhim2:ct-"+self.ct_id+"'/>\n")
    ccd_str += padding.rjust(indent+2) + ("<xs:complexType name='ct-"+self.ct_id+"'> <!-- "+escape(self.title)+" -->\n")
    ccd_str += padding.rjust(indent+4) + ("<xs:complexContent>\n")
    ccd_str += padding.rjust(indent+6) + ("<xs:restriction base='mlhim2:CCDType'>\n")
    ccd_str += padding.rjust(indent+8) + ("<xs:sequence>\n")
    ccd_str += padding.rjust(indent+10) + ("<xs:element maxOccurs='1' minOccurs='1' ref='mlhim2:el-"+entry_id+"'/> <!-- definition -->\n")
    ccd_str += padding.rjust(indent+8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 ="/>\n"
        for a in self.asserts.splitlines():
            ccd_str += padding.rjust(indent+8) + (str1+'"'+a+'"'+str2)

    ccd_str += padding.rjust(indent+6) + ("</xs:restriction>\n")
    ccd_str += padding.rjust(indent+4) + ("</xs:complexContent>\n")
    ccd_str += padding.rjust(indent+2) + ("</xs:complexType>\n\n")
    ccd_str += padding.rjust(indent+4) + ("<!-- CCD Components Begin Below -->\n\n")

    doc_str += "<button type='button' class='btn btn-danger hidebutton'>Close</button>\n</div>\n</div><br />\n</div>\n"
    return (ccd_str.encode("utf-8"),doc_str.encode("utf-8"))
