"""
Data Model 
"""
from xml.sax.saxutils import escape
from urllib.parse import quote

from datetime import datetime
from collections import OrderedDict
from cuid import cuid

from s3m_struct import ClusterType


class DMType(object):
    """
    This is the root node of a Data Model (DM)
    """

    def __init__(self, title):
        """
        The Data Model is the wrapper for all of the data components as well as the semantics.
        """
        self._acs = []
        self._mcuid = cuid()
        self._label = title
        self._metadata = self.genMD()
        self._data = None
        self._dm_language = self.metadata['language']
        self._dm_encoding = 'utf-8'
        self._current_state = ''
        self._subject = None
        self._provider = None
        self._participations = list()
        self._protocol = None
        self._workflow = None
        self._audits = list()
        self._attestations = list()
        self._links = list()

    def __str__(self):
        return("S3Model Data Model\n" + "ID: " + self.mcuid + "\n" + self.showMetadata(self.metadata))

    def showMetadata(self):
        mdStr = ''
        for k, v in self.metadata.items():
            mdStr += k + ': ' + repr(v) + '\n'
        return(mdStr)

    def genMD(self):
        """
        Create a metadata dictionary for the DM if one isn't passed in.
        """
        md = OrderedDict()
        md['title'] = self._label
        md['creator'] = 'Unknown'
        md['contribs'] = ['Unknown', 'Well Known']
        md['subject'] = 'S3M DM'
        md['rights'] = 'Creative Commons'
        md['relation'] = 'None'
        md['coverage'] = 'Global'
        md['identifier'] = 'dm-' + self.mcuid
        md['description'] = 'Needs a description'
        md['publisher'] = 'Data Insights, Inc.'
        md['date'] = '{0:%Y-%m-%dT%H:%M:%S}'.format(datetime.now())
        md['language'] = 'en-US'

        return(md)

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    @property
    def mcuid(self):
        """
        The unique identifier of the component.
        """
        return self._mcuid

    @property
    def metadata(self):
        """
        The model metadata.
        """
        return self._metadata

    @property
    def data(self):
        """
        The data structure of the model.
        """
        return self._data

    @data.setter
    def data(self, v):
        if self._data is None and isinstance(v, ClusterType):
            self._data = v
        else:
            raise TypeError("the data attribute must be empty and the value passed must be a ClusterType.")

    @property
    def acs(self):
        """
        Access Control System. 
        """
        return self._acs

    @acs.setter
    def acs(self, v: list):
        self._acs = v
        global ACS
        ACS = v

    def __str__(self):
        if self.validate():
            return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)
        else:
            raise ValidationError(self.__class__.__name__ + ' : ' + self.label + " failed validation.")

    def validate(self):
        """
        Validation called before exporting code or execution of the __str__ method.
        """
        return(True)

    def exportDM(self):
        """
        Return a XML Schema for a complete Data Model.
        """
        indent = 0
        padding = ('').rjust(indent)
        xdstr = ''
        xdstr += self._header()
        xdstr += self._metaxsd()

        xdstr += padding.rjust(indent) + '<xs:element name="dm-' + self.mcuid + '" substitutionGroup="s3m:DM" type="s3m:mc-' + self.mcuid + '"/>\n'
        xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
        xdstr += padding.rjust(indent + 6) + escape(self.metadata['description'].strip()) + '\n'
        xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

        # add RDF
        xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + self.mcuid + '">\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd#DMType"/>\n'
        xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
        #xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(self.definition_url.strip()) + '"/>\n'
        # if len(self.pred_obj_list) > 0:  # are there additional predicate-object definitions?
        # for po in self.pred_obj_list:
        #pred = po[0]
        #obj = po[1]
        #xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:DMType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="dm-language" type="xs:language" fixed="en-US"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="dm-encoding" type="xs:string" default="utf-8"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="current-state" type="xs:string"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" ref="s3m:ms-' + self.data.mcuid + '"/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        #xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="" type=""/>\n'
        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n\n'
        xdstr += self.data.asXSD()

        xdstr += "</xs:schema>"

        return(xdstr)

    def _header(self):
        """
        Return the data model schema header.
        """
        xsd = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>
<xs:schema
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:owl="http://www.w3.org/2002/07/owl#"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:sawsdlrdf="http://www.w3.org/ns/sawsdl#"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron"
  xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:skos="http://www.w3.org/2004/02/skos/core#"
  xmlns:s3m="https://www.s3model.com/ns/s3m/"
  xmlns:sh="http://www.w3.org/ns/shacl"
  targetNamespace="https://www.s3model.com/ns/s3m/"
  xml:lang="en-US">
  
  <!-- Include the RM Schema -->
  <xs:include schemaLocation="https://www.s3model.com/ns/s3m/s3model_3_1_0.xsd"/>
    """
        return(xsd)

    def _metaxsd(self):
        """
        Return the daa model metadata.
        """
        contribs = ''
        for contrib in self.metadata['contribs']:
            contribs += "<dc:contributor>" + contrib + "</dc:contributor>\n    "
        contribs = contribs.strip('\n    ')
        md = """
        
  <!-- Dublin Core Metadata -->
  <xs:annotation><xs:appinfo><rdf:RDF><rdf:Description
    rdf:about='dm-""" + self.mcuid + """' >
    <dc:title>""" + self.metadata['title'] + """</dc:title>
    <dc:creator>""" + self.metadata['creator'] + """</dc:creator>
    """ + contribs + """
    <dc:dc_subject>""" + self.metadata['subject'] + """</dc:dc_subject>
    <dc:rights>""" + self.metadata['rights'] + """</dc:rights>
    <dc:relation>""" + self.metadata['relation'] + """</dc:relation>
    <dc:coverage>""" + self.metadata['coverage'] + """</dc:coverage>
    <dc:type>S3Model Data Model (DM)</dc:type>
    <dc:identifier>dm-""" + self.mcuid + """</dc:identifier>
    <dc:description>""" + self.metadata['description'] + """</dc:description>
    <dc:publisher>""" + self.metadata['publisher'] + """</dc:publisher>
    <dc:date>""" + self.metadata['date'] + """</dc:date>
    <dc:format>text/xml</dc:format>
    <dc:language>""" + self.metadata['language'] + """</dc:language>
  </rdf:Description></rdf:RDF></xs:appinfo></xs:annotation>

        """

        return(md)
