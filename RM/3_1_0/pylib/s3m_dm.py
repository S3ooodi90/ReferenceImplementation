"""
Data Model 
"""
import os
from xml.sax.saxutils import escape
from urllib.parse import quote

from datetime import datetime
from collections import OrderedDict
from cuid import cuid

from s3m_settings import DM_LIB
from s3m_utils import get_acs
from s3m_xdt import XdStringType, XdLinkType
from s3m_struct import ClusterType
from s3m_meta import ParticipationType, PartyType, AuditType, AttestationType
from s3m_errors import ValidationError, PublicationError

ACS = []

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
        self._pred_obj_list = []
        self._data = None
        self._dm_language = self.metadata['language']
        self._dm_encoding = 'utf-8'
        self._current_state = ''
        self._subject = None
        self._provider = None
        self._participations = []
        self._protocol = None
        self._workflow = None
        self._audits = []
        self._attestations = []
        self._links = []
        self._published = False

    def __str__(self):
        return("S3Model Data Model\n" + "ID: " + self.mcuid + "\n" + self.showMetadata(self.metadata))

    def showMetadata(self):
        mdStr = ''
        for k, v in self.metadata.items():
            mdStr += k + ': ' + repr(v) + '\n'
        return(mdStr)

    def genMD(self):
        """
        Create a metadata dictionary for the DM. Each element has a default.
        """
        md = OrderedDict()
        md['creator'] = 'Unknown'
        md['contribs'] = []
        md['subject'] = 'S3M Data Model Example'
        md['rights'] = 'Creative Commons'
        md['relation'] = 'None'
        md['coverage'] = 'Global'
        md['description'] = 'Needs a description.'
        md['publisher'] = 'Data Insights, Inc.'
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
    def pred_obj_list(self):
        """
        A list of additional predicate object pairs to describe the model.

        Each list item is a tuple where 0 is the predicate and 1 is the object.

        Example:
        ('rdf:resource','https://www.niddk.nih.gov/health-information/health-statistics')
        The setter accepts the tuple and appends it to the list.
        If an empty list is supplied it resets the value to the empty list.
        """
        return self._pred_obj_list

    @pred_obj_list.setter
    def pred_obj_list(self, v: Iterable):
        if not self.published:
            if isinstance(v, list) and len(v) == 0:
                self._pred_obj_list = []
            elif isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], str) and isinstance(v[1], str):
                self._pred_obj_list.append(v)
            else:
                raise ValueError("the Predicate Object List value must be a tuple of two strings or an empty list.")
        else:
            raise ValueError("The model has been published and cannot be edited.")


    @property
    def md_creator(self):
        """
        An entity primarily responsible for making the content of the resource.

        Examples of a Creator include a person, an organisation,
        or a service. Typically, the name of a Creator should be used to
        indicate the entity.
        """
        return self._metadata['creator']

    @creator.setter
    def md_creator(self, v):
        if isinstance(v, str):
            self._metadata['creator'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_contrib(self):
        """
        An entity responsible for making contributions to the content of the resource.
        Examples of a Contributor include a person, an organisation, or a service.
        Typically, the name of a Contributor should be used to indicate the entity.

        Any number of contributors may be added.
        """
        return self._metadata['contribs']

    @contrib.setter
    def md_contrib(self, v):
        if isinstance(v, str):
            self._metadata['contribs'].append(v.strip())
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_subject(self):
        """
        The topic of the content of the resource.

        Typically, a Subject will be expressed as keywords,
        key phrases or classification codes  (semi-colon separated)
        that describe a topic of the resource.

        Recommended best practice is to select a value from a
        controlled vocabulary or formal classification scheme.
        """
        return self._metadata['subject']

    @subject.setter
    def md_subject(self, v):
        if isinstance(v, str):
            self._metadata['subject'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_rights(self):
        """
        Information about rights held in and over the resource.

        Typically, a Rights element will contain a rights
        management statement for the resource, or reference
        a service providing such information. Rights information
        often encompasses Intellectual Property Rights (IPR),
        Copyright, and various Property Rights.
        If the Rights element is absent, no assumptions can be made
        about the status of these and other rights with respect to
        the resource.
        """
        return self._metadata['rights']

    @rights.setter
    def md_rights(self, v):
        if isinstance(v, str):
            self._metadata['rights'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_relation(self):
        """
        A reference to a related resource.

        In S3Model this would be the identifier of another data model.
        """
        return self._metadata['relation']

    @relation.setter
    def md_relation(self, v):
        if isinstance(v, str):
            self._metadata['relation'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_coverage(self):
        """
        The extent or scope of the content of the resource.

        Coverage will typically include spatial location (a place name
        or geographic coordinates), temporal period (a period label,
        date, or date range) or jurisdiction (such as a named
        administrative entity).

        Recommended best practice is to select a value from a
        controlled vocabulary (for example, the Thesaurus of Geographic
        Names [TGN]) and that, where appropriate, named places or time
        periods be used in preference to numeric identifiers such as
        sets of coordinates or date ranges.
        """
        return self._metadata['coverage']

    @coverage.setter
    def md_coverage(self, v):
        if isinstance(v, str):
            self._metadata['coverage'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_description(self):
        """
        An account of the content of the resource.

        Description may include but is not limited to: an abstract,
        table of contents, reference to a graphical representation
        of content or a free-text account of the content.
        """
        return self._metadata['description']

    @description.setter
    def md_description(self, v):
        if isinstance(v, str):
            self._metadata['description'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_publisher(self):
        """
        An entity responsible for making the resource available.

        Examples of a Publisher include a person, an organisation,
        or a service.
        Typically, the name of a Publisher should be used to
        indicate the entity.
        """
        return self._metadata['publisher']

    @publisher.setter
    def md_publisher(self, v):
        if isinstance(v, str):
            self._metadata['publisher'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def md_language(self):
        """
        A language of the intellectual content of the resource.

        Recommended best practice for the values of the Language
        element is defined by RFC 1766 [RFC1766] which includes
        a two-letter Language Code (taken from the ISO 639
        standard [ISO639]), followed optionally, by a two-letter
        Country Code (taken from the ISO 3166 standard [ISO3166]).
        For example, 'en' for English, 'fr' for French, or
        'en-uk' for English used in the United Kingdom.
        """
        return self._metadata['language']

    @language.setter
    def md_language(self, v):
        if isinstance(v, str):
            self._metadata['language'] = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def encoding(self):
        """
        Name of character set encoding in which text values in this DM are encoded. 
        
        Default is utf-8.
        """
        return self._dm_encoding

    @encoding.setter
    def encoding(self, v):
        if isinstance(v, str):
            self._dm_encoding = v
        else:
            raise TypeError("the value must be a string.")

    @property
    def state(self):
        """
        The current state according to the state machine / workflow engine 
        identified in the workflow element.
        """
        return self._current_state

    @state.setter
    def state(self, v):
        if isinstance(v, str):
            self._current_state = v
        else:
            raise TypeError("the value must be a string.")

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
    def subject(self):
        """
        Id of human subject of the data, e.g.: 
        • subject of record (patient, customer, etc.) 
        • a family member 
        • another relevant person.
        """
        return self._subject

    @subject.setter
    def subject(self, v):
        if isinstance(v, PartyType):
            self._subject = v
        else:
            raise TypeError("the value must be a PartyType.")

    @property
    def provider(self):
        """
        Optional identification of the source of the information, which might be: 
        • a patient 
        • a patient agent, e.g. parent, guardian 
        • a clinician
        • a technician
        • a device or software
        """
        return self._provider

    @provider.setter
    def provider(self, v):
        if isinstance(v, PartyType):
            self._provider = v
        else:
            raise TypeError("the value must be a PartyType.")

    @property
    def participations(self):
        """
        List of other participations in the data.
        """
        return self._participations

    @participations.setter
    def participations(self, v):
        if isinstance(v, ParticipationType):
            self._provider.append(v)
        else:
            raise TypeError("the value must be a ParticipationType.")

    @property
    def protocol(self):
        """
        Optional external identifier of protocol used when collecting the data. 
        This could be a clinical guideline, an operations protocol, etc.
        """
        return self._protocol

    @protocol.setter
    def protocol(self, v):
        if isinstance(v, XdStringType):
            self._protocol = v
        else:
            raise TypeError("the value must be a XdStringType.")

    @property
    def workflow(self):
        """
        Identifier of externally held workflow engine (state machine) data for this 
        workflow execution.
        """
        return self._workflow

    @workflow.setter
    def workflow(self, v):
        if isinstance(v, XdLinkType):
            self._workflow = v
        else:
            raise TypeError("the value must be a XdLinkType.")


    @property
    def acs(self):
        """
        Access Control System. 
        """
        return self._acs

    @acs.setter
    def acs(self, v):
        if isinstance(v, XdLinkType):
            self._acs = v
        else:
            raise TypeError("the value must be a XdLinkType.")
        
        global ACS
        ACS = get_acs(acs.link)

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
        if self._published:
            raise PublicationError(self.label + " - " + self.metadata['identifier'] + " -- This Data Model has already been published.")
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
        if len(self.pred_obj_list) != 0:
            for po in self.pred_obj_list:
                xdstr += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
        xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
        xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
        xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:DMType">\n'
        xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + self.label.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="dm-language" type="xs:language" default="en-US"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="dm-encoding" type="xs:string" default="utf-8"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="current-state" type="xs:string" default=""/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" ref="s3m:ms-' + self.data.mcuid + '"/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="subject" type="s3m:mc-"' + self.subject.mcuid + '/>\n'
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="provider" type="s3m:mc-"' + self.provider.mcuid + '/>\n'


        xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
        xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
        xdstr += padding.rjust(indent) + '</xs:complexType>\n\n'
        xdstr += self.data.getModel()

        xdstr += "</xs:schema>"

        with open(os.path.join(DM_LIB, 'dm-' + self.mcuid + '.xsd'), 'w') as f:
            f.write(xdstr)

        msg = "Wrote " + os.path.join(DM_LIB, 'dm-' + self.mcuid + '.xsd')
        self._published = True
        return(msg)

    def _header(self):
        """
        Return the data model schema header.
        """
        xsd = """<?xml version="1.0" encoding="UTF-8"?>
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
        Return the data model metadata.
        """
        contribs = ''
        for contrib in self.metadata['contribs']:
            contribs += "<dc:contributor>" + contrib + "</dc:contributor>\n    "
        contribs = contribs.strip('\n    ') # remove the last newline
        md = """
        
  <!-- Dublin Core Metadata -->
  <xs:annotation><xs:appinfo><rdf:RDF><rdf:Description
    rdf:about='dm-""" + self.mcuid + """' >
    <dc:title>""" + self.label.strip() + """</dc:title>
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
    <dc:date>""" + '{0:%Y-%m-%d}'.format(datetime.now()) + """</dc:date>
    <dc:format>text/xml</dc:format>
    <dc:language>""" + self.metadata['language'] + """</dc:language>
  </rdf:Description></rdf:RDF></xs:appinfo></xs:annotation>

        """

        return(md)

    def exportXML(self, example):
        """
        Export a XML instance for the Data Model.
        """
        if not self.published:
            raise ValueError("The model must first be published.")
        if example:
            self.party_name = "A. Sample Name"

        indent = 2
        padding = ('').rjust(indent)

        xmlstr = ''
        xmlstr += padding + "<s3m:dm-" + self.mcuid + ">\n"
        xmlstr += padding + "  <label>" + escape(self.label) + "</label>\n"
        xmlstr += padding + "  <dm-language>" + escape(self.language) + "</dm-language>\n"
        xmlstr += padding + "  <dm-encoding>" + escape(self.encoding) + "</dm-encoding>\n"
        xmlstr += padding + "  <current-state>" + escape(self.state) + "</current-state>\n"
        
        xmlstr += padding + "</s3m:dm-" + self.mcuid + ">\n"
        return(xmlstr)

    def exportJSON(self, example):
        """
        Export a JSON instance for the Data Model.
        """
        xml = self.exportXML(example)
        parsed = xmltodict.parse(xml, encoding='UTF-8', process_namespaces=False)
        return(json.dumps(parsed, indent=2, sort_keys=False))



    def extractRDF(self):
        """
        Return the RDF/XML Triples for the Model.
        """
        indent = 2
        padding = ('').rjust(indent)
        
        xmlstr = 'TODO: Write template.'
        return(xmlstr)

