"""
The S3M Reference Model code to write DM schemas.

This code is accessed from model.py
Each class from the model will have a 'publish_' function here that will assemble
the strings required to write itself to code in a DM.
The code is stored in the schema_code text field.

When the published flag is True, this function is executed in order to write the code to the database.
If the schema_code field is not empty, the flag will remain True. In order to rewrite the code the database
field must be manually edited. This is to prevent changes being made to an item and it being rewritten with
the same UUID. THIS **MUST** NEVER HAPPEN!
If there are errors, just create a new component with a new UUID.

"""
try:
    from urllib.parse import quote
except ImportError:
    from urllib.parse import quote

from uuid import uuid4
from collections import OrderedDict
from xml.sax.saxutils import escape
from django.contrib import messages

from s3m.settings import RMVERSION

from .exceptions import PublishingError, ModellingError
from .r_code_gen import pct_rcode


def reset_publication(self):
    """
    Insure that the schema code, R code and the published flag is False,anytime there is a publication or modelling error.
    This was needed after noticing that sometimes the published flag gets set even though an error was raised.
    """
    self.schema_code = ''
    self.r_code = ''
    self.published = False
    self.save()


def publish_XdBoolean(self):
    """
    Writes the complete DM complexType code for the containing the XdBoolean itself. Saves it in the schema_code
    attribute. Once written it sets the 'published' flag to True. This flag can never be reset to False.


    """

    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdBoolean')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)

    dt_str = ''
    trues = []
    falses = []
    for t in self.trues.splitlines():
        trues.append(escape(t))

    for f in self.falses.splitlines():
        falses.append(escape(f))

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    dt_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdBooleanType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdBooleanType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdBooleanType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdBoolean
    dt_str += padding.rjust(indent + 8) + \
        ("<xs:choice maxOccurs='1' minOccurs='1'>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element name='true-value'>\n")
    dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent + 12) + \
        ("<xs:restriction base='xs:string'>\n")
    for n in range(len(trues)):
        dt_str += padding.rjust(indent + 16) + \
            ("<xs:enumeration value='" + trues[n].strip() + "'/>\n")
    dt_str += padding.rjust(indent + 12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element name='false-value'>\n")
    dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent + 12) + \
        ("<xs:restriction base='xs:string'>\n")
    for n in range(len(falses)):
        dt_str += padding.rjust(indent + 16) + \
            ("<xs:enumeration value='" + falses[n].strip() + "'/>\n")
    dt_str += padding.rjust(indent + 12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent + 8) + ("</xs:choice>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdLink(self):
    """
     Writes the complete DM complexType code for the containing the XdLink itself. Saves it in the schema_code
     attribute. Once written it sets the 'published' flag to True. This flag can never be reset to False.


    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()
    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdLink')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()
    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)

    dt_str = ''

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    dt_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdLinkType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + (
            "<rdf:Description rdf:about='s3m:mc-" + quote(self.ct_id) + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdLinkType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdLinkType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdLink
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='link' type='xs:anyURI'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='relation' type='xs:string' fixed='" + escape(self.relation.strip()) + "'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='relation-uri' type='xs:anyURI' fixed='" +
                                           escape(self.relation_uri.strip()) + "'/>\n")

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdString(self):
    """
    Writes the complete DM complexType code for the containing Element and the XdString itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()
    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdString')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''

    indent = 2
    enumList = []
    for e in self.enums.splitlines():
        enumList.append(escape(e))

    tips = []
    for t in self.definitions.splitlines():
        tips.append(escape(t))

    if self.def_val:
        default = escape(self.def_val.strip())
    else:
        default = None

    padding = ('').rjust(indent)

    # Create the datatype
    dt_str += padding.rjust(indent) + ("<xs:complexType name='mc-" +
                                       self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdStringType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdStringType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdStringType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdString
    if enumList:
        if default:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='Xdstring-value' default='" + escape(default.strip()) + "'>\n")
        else:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='Xdstring-value'>\n")
    else:
        if default:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='Xdstring-value' type='xs:string' default='" + escape(default) + "'/>\n")
        else:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='Xdstring-value' type='xs:string'/>\n")

# Enumerations
    if enumList:
        if len(tips) != len(enumList):
            if len(tips) == 0:
                tips = enumList
            else:
                reset_publication(self)
                msg = ("Cannot publish: " + self.__str__() +
                       " The number of Enumerations and Definitions must be same. Check for empty lines.", messages.ERROR)
                return msg

        dt_str += padding.rjust(indent + 12) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent + 14) + \
            ("<xs:restriction base='xs:string'>\n")
        for n in range(len(enumList)):
            dt_str += padding.rjust(indent + 16) + (
                "<xs:enumeration value='" + escape(enumList[n].strip()) + "'>\n")
            dt_str += padding.rjust(indent + 16) + ("<xs:annotation>\n")
            dt_str += padding.rjust(indent + 18) + ("<xs:appinfo>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdf:Description rdf:about='s3m:mc-" +
                                                   self.ct_id + "/Xdstring-value/" + quote(enumList[n].strip()) + "'>\n")
            dt_str += padding.rjust(indent + 2) + (
                "  <rdfs:subPropertyOf rdf:resource='s3m:mc-" + self.ct_id + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("  <rdfs:label>" +
                                                   enumList[n].strip() + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("  <rdfs:isDefinedBy>" +
                                                   tips[n].strip() + "</rdfs:isDefinedBy>")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
            dt_str += padding.rjust(indent + 18) + ("</xs:appinfo>\n")
            dt_str += padding.rjust(indent + 16) + ("</xs:annotation>\n")
            dt_str += padding.rjust(indent + 16) + ("</xs:enumeration>\n")
        dt_str += padding.rjust(indent + 14) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent + 12) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='Xdstring-language' type='xs:language' default='" + self.lang + "'/>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdFile(self):
    """
    Writes the complete DM complexType code for the XdFile itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdFile')
    self.save()

    # encode double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    mime_list = None
    comp_list = None
    indent = 2

    media_list = []
    if self.media_type:
        for m in self.media_type.splitlines():
            media_list.append(escape(m))

    padding = ('').rjust(indent)

    # Create the datatype
    dt_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdFileType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdFileType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdFileType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" + '"' + escape(self.label) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdFile
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='size' type='xs:int'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='encoding' type='xs:string' default='" + self.encoding.strip() + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='Xdfile-language' type='xs:language' default='" + self.language.strip() + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='formalism' type='xs:string' default=''/>\n")
    if not media_list:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='media-type' type='xs:string'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + \
            ("<xs:element maxOccurs='1' minOccurs='1' name='media-type'>\n")
        dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent + 12) + \
            ("<xs:restriction base='xs:string'>\n")
        for m in media_list:
            dt_str += padding.rjust(indent + 14) + \
                ("<xs:enumeration value='" + m.strip() + "'/>\n")
        dt_str += padding.rjust(indent + 12) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='compression-type' type='xs:string'/>\n")

    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='hash-result' type='xs:string'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='hash-function' type='xs:string'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='alt-txt' type='xs:string' default='" + escape(self.alt_txt) + "'/>\n")

    if self.content_mode == 'select':
        reset_publication(self)
        msg = ("Cannot publish: " + self.__str__() +
               " until you select a Content Mode.", messages.ERROR)
    elif self.content_mode == 'url':
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='uri' type='xs:anyURI'/>\n")
    elif self.content_mode == 'text':
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='text-content' type='xs:string'/>\n")
    elif self.content_mode == 'binary':
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='media-content' type='xs:base64Binary'/>\n")
    else:
        reset_publication(self)
        msg = ("Something REALLY REALLY bad happened: " + self.__str__() +
               " has an error in the Content Mode that I cannot fix. Please report this to the DM-Gen Admin.", messages.ERROR)

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdInterval(self):
    """

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    padding = ('').rjust(indent)
    # Convert the bools to XSD strings
    li, ui, lb, ub = 'false', 'false', 'false', 'false'
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
        msg = ("Missing Interval Type. " + self.label, messages.ERROR)

    if self.interval_type not in ['int', 'decimal', 'date', 'time', 'dateTime', 'float', 'duration']:
        reset_publication(self)
        msg = ("Invalid Type for XdInterval. " + repr(self.interval_type) +
               " in " + self.label + " is not an allowed, ordered type.", messages.ERROR)

    # check for modelling errors
    if self.lower_bounded and not self.lower:
        reset_publication(self)
        msg = ("Enter lower value or uncheck the lower bounded box in " +
               self.label + ". ", messages.ERROR)
    if self.upper_bounded and not self.upper:
        reset_publication(self)
        msg = ("Enter upper value or uncheck the upper bounded box in " +
               self.label + ". ", messages.ERROR)

    if not self.lower_bounded and self.lower:
        reset_publication(self)
        msg = ("Remove lower value or check the lower bounded box in " +
               self.label + ". ", messages.ERROR)
    if not self.upper_bounded and self.upper:
        reset_publication(self)
        msg = ("Remove upper value or check the upper bounded box in " +
               self.label + ". ", messages.ERROR)

    # if the user used a comma as a decimal separator then replace it with a
    # period.
    if self.interval_type == 'decimal':
        if "," in self.lower:
            self.lower = self.lower.replace(",", ".")
            self.save()
        if "," in self.upper:
            self.upper = self.upper.replace(",", ".")
            self.save()

    dt_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdIntervalType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdIntervalType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdIntervalType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdInterval
    # create an UUIDs for the invl-type restrictions
    lower_id = str(uuid4())
    upper_id = str(uuid4())
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='lower' type='s3m:mc-" + lower_id + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='upper' type='s3m:mc-" + upper_id + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='lower-included' type='xs:boolean' fixed='" + li + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='upper-included' type='xs:boolean' fixed='" + ui + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='lower-bounded' type='xs:boolean' fixed='" + lb + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='upper-bounded' type='xs:boolean' fixed='" + ub + "'/>\n")
    # both must be present or they are both ignored.
    if self.units_name and self.units_uri:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='units-name' type='xs:string' fixed='" + self.units_name.strip() + "'/>\n")
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='units-uri' type='xs:anyURI' fixed='" + self.units_uri.strip() + "'/>\n")

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    # lower value restriction
    dt_str += padding.rjust(indent + 2) + \
        ("<xs:complexType name='mc-" + lower_id + "'>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 6) + \
        ("<xs:restriction base='s3m:InvlType'>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:choice>\n")
    if self.lower_bounded:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" +
                                                self.interval_type + "' type='xs:" + self.interval_type + "' fixed='" + self.lower.strip() + "'/>\n")
    else:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" + self.interval_type +
                                                "' type='xs:" + self.interval_type + "' nillable='true'/> <!-- Instance elements must be set to xsi:nil='true' -->\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:choice>\n")
    if not self.lower_bounded:
        dt_str += padding.rjust(indent + 8) + ("<xs:assert test='boolean(invl-" +
                                               self.interval_type + "/node()) = false()'/>\n")
    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    # upper value restriction
    dt_str += padding.rjust(indent + 2) + \
        ("<xs:complexType name='mc-" + upper_id + "'>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 6) + \
        ("<xs:restriction base='s3m:InvlType'>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:choice>\n")
    if self.upper_bounded:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" +
                                                self.interval_type + "' type='xs:" + self.interval_type + "' fixed='" + self.upper.strip() + "'/>\n")
    else:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" + self.interval_type +
                                                "' type='xs:" + self.interval_type + "' nillable='true'/> <!-- Instance elements must be set to xsi:nil='true' -->\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:choice>\n")
    if not self.upper_bounded:
        dt_str += padding.rjust(indent + 8) + ("<xs:assert test='boolean(invl-" +
                                               self.interval_type + "/node()) = false()'/>\n")
    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_ReferenceRange(self):
    """

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    rr_def = escape(self.definition)

    # TODO - change interval to interval

    Xdi_id = str(self.interval.ct_id)
    if self.is_normal:
        normal = "true"
    else:
        normal = "false"
    if not self.interval.published:
        reset_publication(self)
        msg = ("XdInterval: " + self.interval.label +
               " hasn't been published. Please publish the interval and retry.", messages.ERROR)

    padding = ('').rjust(indent)

    dt_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:ReferenceRangeType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:ReferenceRangeType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:ReferenceRangeType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # ReferenceRange
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='definition' type='xs:string' fixed='" + rr_def.strip() + "'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='interval' type='s3m:mc-" + Xdi_id + "'/> \n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='is-normal' type='xs:boolean' fixed='" + normal + "'/>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_SimpleReferenceRange(self):
    """
    Simple Reference Range contains one XdInterval.
    This publisher produces the schema code for a XdInterval as well as the Reference Range.
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()
    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    rr_def = escape(self.definition)

    dvi_id = str(uuid4())
    if self.is_normal:
        normal = "true"
    else:
        normal = "false"

    # Convert the bools to XSD strings
    li, ui, lb, ub = 'false', 'false', 'false', 'false'
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
        msg = ("Missing Interval Type. " + self.label, messages.ERROR)

    if self.interval_type not in ['int', 'decimal', 'date', 'time', 'dateTime', 'float', 'duration']:
        reset_publication(self)
        msg = ("Invalid Type for XdInterval. " + repr(self.interval_type) + " in " +
               self.label + " is not an allowed, ordered type.", messages.ERROR)

    # check for modelling errors
    if self.lower_bounded and not self.lower:
        reset_publication(self)
        msg = ("Enter lower value or uncheck the lower bounded box in " +
               self.label + ". ", messages.ERROR)
    if self.upper_bounded and not self.upper:
        reset_publication(self)
        msg = ("Enter upper value or uncheck the upper bounded box in " +
               self.label + ". ", messages.ERROR)

    if not self.lower_bounded and self.lower:
        reset_publication(self)
        msg = ("Remove lower value or check the lower bounded box in " +
               self.label + ". ", messages.ERROR)
    if not self.upper_bounded and self.upper:
        reset_publication(self)
        msg = ("Remove upper value or check the upper bounded box in " +
               self.label + ". ", messages.ERROR)

    # if the user used a comma as a decimal separator then replace it with a
    # period.
    if self.interval_type == 'decimal':
        if "," in self.lower:
            self.lower = self.lower.replace(",", ".")
            self.save()
        if "," in self.upper:
            self.upper = self.upper.replace(",", ".")
            self.save()

    padding = ('').rjust(indent)

    # Create the  RR datatype
    dt_str += '\n\n' + padding.rjust(indent) + ("<xs:complexType name='cm-" + self.ct_id + "' xml:lang='" +
                                                self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:cm-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:ReferenceRangeType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" +
                                                   quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:pcm-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:ReferenceRangeType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:ReferenceRangeType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # ReferenceRange
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='definition' type='xs:string' "
                                            "fixed='") + rr_def.strip() + "'/>\n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='interval' "
                                            "type='s3m:pcm-") + dvi_id + "'/> \n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='is-normal' "
                                            "type='xs:boolean' fixed='") + normal + "'/>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>")

    # XdInterval
    dt_str += '\n\n' + padding.rjust(indent) + ("<xs:complexType name='pcm-" + dvi_id + "' xml:lang='" +
                                                self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:pcm-" + dvi_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdIntervalType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" +
                                                   quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:pcm-" + dvi_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdIntervalType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdIntervalType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' "
                                            "fixed=") + '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='vte' type='xs:dateTime'/>\n")
    # XdInterval
    # create UUIDs for the invl-type restrictions
    lower_id = str(uuid4())
    upper_id = str(uuid4())
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='0' name='lower' "
                                            "type='s3m:pcm-") + lower_id + "'/>\n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='0' name='upper' "
                                            "type='s3m:pcm-") + upper_id + "'/>\n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='lower-included' "
                                            "type='xs:boolean' fixed='") + li + "'/>\n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='upper-included' "
                                            "type='xs:boolean' fixed='") + ui + "'/>\n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='lower-bounded' "
                                            "type='xs:boolean' fixed='") + lb + "'/>\n")
    dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='upper-bounded' "
                                            "type='xs:boolean' fixed='") + ub + "'/>\n")
    if self.units_name and self.units_uri:
        dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='units-name' "
                                                "type='xs:string' fixed='") + self.units_name.strip() + "'/>\n")
        dt_str += (padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='units-uri' "
                                                "type='xs:anyURI' fixed='") + self.units_uri.strip() + "'/>\n")
    elif self.units_name or self.units_uri:
        reset_publication(self)
        msg = ("Missing Units Name or Units URI in Simple Reference Range" +
               self.label + ". ", messages.ERROR)

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    # lower value restriction
    dt_str += padding.rjust(indent + 2) + \
        ("<xs:complexType name='pcm-" + lower_id + "'>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 6) + \
        ("<xs:restriction base='s3m:InvlType'>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:choice>\n")
    if self.lower_bounded:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" +
                                                self.interval_type + "' type='xs:" +
                                                self.interval_type + "' fixed='" + self.lower.strip() + "'/>\n")
    else:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" +
                                                self.interval_type + "' type='xs:" +
                                                self.interval_type + ("' nillable='true'/> "
                                                                      "<!-- Instance elements must be set to "
                                                                      "xsi:nil='true' -->\n"))
    dt_str += padding.rjust(indent + 8) + ("</xs:choice>\n")
    if not self.lower_bounded:
        dt_str += padding.rjust(indent + 8) + ("<xs:assert test='boolean(invl-" +
                                               self.interval_type + "/node()) = false()'/>\n")
    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    # upper value restriction
    dt_str += padding.rjust(indent + 2) + \
        ("<xs:complexType name='pcm-" + upper_id + "'>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 6) + \
        ("<xs:restriction base='s3m:InvlType'>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:choice>\n")
    if self.upper_bounded:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" +
                                                self.interval_type + "' type='xs:" +
                                                self.interval_type + "' fixed='" + self.upper.strip() + "'/>\n")
    else:
        dt_str += padding.rjust(indent + 10) + ("<xs:element maxOccurs='1' minOccurs='1' name='invl-" +
                                                self.interval_type + "' type='xs:" +
                                                self.interval_type + ("' nillable='true'/> "
                                                                      "<!-- Instance elements must be set to "
                                                                      "xsi:nil='true' -->\n"))
    dt_str += padding.rjust(indent + 8) + ("</xs:choice>\n")
    if not self.upper_bounded:
        dt_str += padding.rjust(indent + 8) + ("<xs:assert test='boolean(invl-" +
                                               self.interval_type + "/node()) = false()'/>\n")
    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdOrdinal(self):
    """
    Writes the complete DM complexType code for the containing Element and the XdOrdinal itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.


    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdOrdinal')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # it is a modelling error to use multiple reference ranges with the same
    # Xdinterval in a Xdordinal
    used_ctid_list = []

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
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
            msg = (escape(self.label.strip()) + ": You MUST use digits for the Ordinal indicators. It seems one or more in " +
                   self.label.strip() + " is a string.", messages.ERROR)
            return msg

    s = []
    for a in self.symbols.splitlines():
        s.append(escape(a))

    tips = []
    for t in self.annotations.splitlines():
        tips.append(escape(t))

    if len(tips) != len(s):  # if the length of tips is not equal the number of symbols copy the symbols to tips
        tips = []
        for n in range(0, len(s)):
            tips.append(' ')
    padding = ('').rjust(indent)

    dt_str = '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (docs + "\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdOrdinalType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdOrdinalType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdOrdinalType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdOrdered
    if len(self.reference_ranges.all()) != 0:  # reference ranges defined
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                msg = ("Reference Range: " + rr.label +
                       " hasn't been published. Please publish the reference range and retry.", messages.ERROR)
                return msg

            else:
                dt_str += padding.rjust(indent + 8) + \
                    "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + rr.ct_id + "'/> \n"
                if rr.interval.ct_id not in used_ctid_list:
                    # track the used XdInterval IDs
                    used_ctid_list.append(rr.interval.ct_id)
                else:
                    reset_publication(self)
                    msg = (self.label + ": You cannot use multiple ReferenceRanges with the same XdInterval declared as the data-range in one XdOrdinal.", messages.ERROR)
                    return msg
    if self.normal_status:
        dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='normal-status' type='xs:string' fixed='" +
                                               escape(self.normal_status.strip()) + "'/> \n")
    else:
        self.normal_status = ''

    # XdOrdinal
    dt_str += padding.rjust(indent + 10) + \
        ("<xs:element maxOccurs='1' minOccurs='1' name='ordinal'>\n")
    dt_str += padding.rjust(indent + 12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent + 12) + \
        ("<xs:restriction base='xs:decimal'>\n")
    for n in range(0, len(o)):
        dt_str += padding.rjust(indent + 14) + \
            ("<xs:enumeration value='" + o[n].strip() + "'/>\n")
    dt_str += padding.rjust(indent + 12) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:element>\n")

    dt_str += padding.rjust(indent + 10) + \
        ("<xs:element maxOccurs='1' minOccurs='1' name='symbol'>\n")
    dt_str += padding.rjust(indent + 12) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent + 14) + \
        ("<xs:restriction base='xs:string'>\n")
    for n in range(len(tips)):
        dt_str += padding.rjust(indent + 16) + \
            ("<xs:enumeration value='" + s[n].strip() + "'>\n")
        dt_str += padding.rjust(indent + 16) + ("<xs:annotation>\n")
        dt_str += padding.rjust(indent + 18) + ("<xs:appinfo>\n")
        dt_str += padding.rjust(indent + 18) + ("<rdf:Description rdf:about='s3m:mc-" +
                                                self.ct_id + "/symbol/" + quote(s[n].strip()) + "'>\n")
        dt_str += padding.rjust(indent + 20) + (
            "<rdfs:isDefinedBy rdf:resource='" + quote(tips[n].strip()) + "'/>\n")
        dt_str += padding.rjust(indent + 18) + ("</rdf:Description>\n")
        dt_str += padding.rjust(indent + 18) + ("</xs:appinfo>\n")
        dt_str += padding.rjust(indent + 16) + ("</xs:annotation>\n")
        dt_str += padding.rjust(indent + 16) + ("</xs:enumeration>\n")
    dt_str += padding.rjust(indent + 14) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 12) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:element>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdCount(self):
    """
    Writes the complete DM complexType code for the containing Element and the XdCount itself.
    Saves it in the schema_code attribute. Once written it sets the 'published' flag to True.
    This flag can never be reset to False.


    """

    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdCount')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # it is a modelling error to use multiple reference ranges with the same
    # Xdinterval in a Xdcount
    used_ctid_list = []

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False

    padding = ('').rjust(indent)

    dt_str = '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (docs + "\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdCountType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdCountType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")

    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdCountType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdOrdered
    if len(self.reference_ranges.all()) != 0:  # reference ranges defined
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                msg = ("Reference Range: " + rr.label +
                       " hasn't been published. Please publish the reference range and retry.", messages.ERROR)
                return msg
            else:
                dt_str += padding.rjust(indent + 8) + \
                    "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + rr.ct_id + "'/> \n"
                if rr.interval.ct_id not in used_ctid_list:
                    # track the used XdInterval IDs
                    used_ctid_list.append(rr.interval.ct_id)
                else:
                    reset_publication(self)
                    msg = (self.__str__(
                    ) + ": You cannot use multiple ReferenceRanges with the same XdInterval declared as the data-range in one XdOrdinal.", messages.ERROR)
                    return msg

    if self.normal_status:
        dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='normal-status' type='xs:string' fixed='" +
                                               escape(self.normal_status.strip()) + "'/> \n")
    else:
        self.normal_status = ''

    # XdQuantified
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='magnitude-status' type='s3m:MagnitudeStatus'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='accuracy' type='xs:int' default='0'/>\n")

    # XdCount
    if not mag_constrained:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1'  name='Xdcount-value' type='xs:int'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1'  name='Xdcount-value'>\n")
        dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent + 10) + \
            ("<xs:restriction base='xs:int'>\n")
        if self.min_inclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:minInclusive value='" +
                                                    str(self.min_inclusive).strip() + "'/>\n")
        if self.max_inclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:maxInclusive value='" +
                                                    str(self.max_inclusive).strip() + "'/>\n")
        if self.min_exclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:minExclusive value='" +
                                                    str(self.min_exclusive).strip() + "'/>\n")
        if self.max_exclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:maxExclusive value='" +
                                                    str(self.max_exclusive).strip() + "'/>\n")
        if (self.total_digits is not None and self.total_digits > 0):
            dt_str += padding.rjust(indent + 12) + ("<xs:totalDigits value='" +
                                                    str(self.total_digits).strip() + "'/>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    if not self.units:
        reset_publication(self)
        msg = ("XdCount " + self.__str__() +
               " MUST have a Units definition.", messages.ERROR)
        return msg

    else:
        if not self.units.published:
            reset_publication(self)
            msg = ("Units: " + self.units.label +
                   " hasn't been published. Please publish the object and retry.", messages.ERROR)
            return msg

        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='Xdcount-units' type='s3m:mc-" + str(self.units.ct_id) + "'/> \n")

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdQuantity(self):
    """
    Publish XdQuantity
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdQuantity')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # it is a modelling error to use multiple reference ranges with the same
    # Xdinterval in a Xdquantity
    used_ctid_list = []

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # Is the magnitude constrained?
    if self.min_inclusive or self.max_inclusive or self.min_exclusive or self.max_exclusive or (self.total_digits and self.total_digits > 0):
        mag_constrained = True
    else:
        mag_constrained = False

    padding = ('').rjust(indent)

    dt_str = '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (docs + "\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdQuantityType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdQuantityType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")

    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdQuantityType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdOrdered
    if len(self.reference_ranges.all()) != 0:  # reference ranges defined
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                msg = ("Reference Range: " + rr.label +
                       " hasn't been published. Please publish the reference range and retry.", messages.ERROR)
                return msg
            else:
                dt_str += padding.rjust(indent + 8) + \
                    "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + rr.ct_id + "'/> \n"
                if rr.interval.ct_id not in used_ctid_list:
                    # track the used XdInterval IDs
                    used_ctid_list.append(rr.interval.ct_id)
                else:
                    reset_publication(self)
                    msg = (self.__str__(
                    ) + ": You cannot use multiple ReferenceRanges with the same XdInterval declared as the data-range in one XdOrdinal.", messages.ERROR)
                    return msg
    if self.normal_status:
        dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='normal-status' type='xs:string' fixed='" +
                                               escape(self.normal_status.strip()) + "'/> \n")
    else:
        self.normal_status = ''

    # XdQuantified
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='magnitude-status' type='s3m:MagnitudeStatus'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='accuracy' type='xs:int' default='0'/>\n")

    # XdQuantity
    if not mag_constrained:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1'  name='Xdquantity-value' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1'  name='Xdquantity-value'>\n")
        dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent + 10) + \
            ("<xs:restriction base='xs:decimal'>\n")
        if self.min_inclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:minInclusive value='" +
                                                    str('%.10g' % self.min_inclusive).strip() + "'/>\n")
        if self.max_inclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:maxInclusive value='" + str(
                '%.10g' % self.max_inclusive).strip().strip() + "'/>\n")
        if self.min_exclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:minExclusive value='" +
                                                    str('%.10g' % self.min_exclusive).strip() + "'/>\n")
        if self.max_exclusive is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:maxExclusive value='" +
                                                    str('%.10g' % self.max_exclusive).strip() + "'/>\n")
        if (self.total_digits is not None and self.total_digits >= 0):
            dt_str += padding.rjust(indent + 12) + ("<xs:totalDigits value='" +
                                                    str(self.total_digits).strip() + "'/>\n")
        if (self.fraction_digits is not None and self.fraction_digits >= 0):
            dt_str += padding.rjust(indent + 12) + (
                "<xs:fractionDigits value='" + str(self.fraction_digits).strip() + "'/>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    if not self.units:
        reset_publication(self)
        msg = ("XdQuantity " + self.__str__() +
               " MUST have a Units definition.", messages.ERROR)
        return msg

    else:
        if not self.units.published:
            reset_publication(self)
            msg = ("Units: " + self.units.label +
                   " hasn't been published. Please publish the object and retry.", messages.ERROR)
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='Xdquantity-units' type='s3m:mc-" + str(self.units.ct_id) + "'/>\n")

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdRatio(self):
    """
    Publish XdRatio
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdRatio')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # it is a modelling error to use multiple reference ranges with the same
    # Xdinterval in a Xdratio
    used_ctid_list = []

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    docs = escape(self.description)

    # Is the magnitude constrained?
    if self.min_magnitude or self.max_magnitude:
        mag_constrained = True
    else:
        mag_constrained = False

    padding = ('').rjust(indent)

    dt_str = '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (docs + "\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdRatioType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdRatioType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")

    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdRatioType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdOrdered
    if len(self.reference_ranges.all()) != 0:  # reference ranges defined
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                msg = ("Reference Range: " + rr.label +
                       " hasn't been published. Please publish the reference range and retry.", messages.ERROR)
                return msg

            else:
                dt_str += padding.rjust(indent + 8) + \
                    "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + rr.ct_id + "'/> \n"
                if rr.interval.ct_id not in used_ctid_list:
                    # track the used XdInterval IDs
                    used_ctid_list.append(rr.interval.ct_id)
                else:
                    reset_publication(self)
                    msg = (self.__str__(
                    ) + ": You cannot use multiple ReferenceRanges with the same XdInterval declared as the data-range in one XdOrdinal.", messages.ERROR)
                    return msg

    if self.normal_status:
        dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='normal-status' type='xs:string' fixed='" +
                                               escape(self.normal_status.strip()) + "'/> \n")
    else:
        self.normal_status = ''

    # XdQuantified
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='magnitude-status' type='s3m:MagnitudeStatus'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='error'  type='xs:int' default='0'/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='accuracy' type='xs:int' default='0'/>\n")

    # XdRatio

    # tests for proper modelling
    if (self.num_min_inclusive and self.num_min_exclusive) or (self.num_max_inclusive and self.num_max_exclusive):
        reset_publication(self)
        msg = (self.__str__() + ": There is ambiguity in your numerator constraints for min/max. Please use EITHER minimum or maximum values, not both.", messages.ERROR)
        return msg
    if (self.den_min_inclusive and self.den_min_exclusive) or (self.den_max_inclusive and self.den_max_exclusive):
        reset_publication(self)
        msg = (self.__str__() + ": There is ambiguity in your denominator constraints for min/max. Please use EITHER minimum or maximum values, not both.", messages.ERROR)
        return msg
    # tests for not reusing units PcT
    if self.num_units is not None and self.den_units is not None:
        if self.num_units.ct_id == self.den_units.ct_id:
            reset_publication(self)
            msg = (self.__str__(
            ) + ": Numerator and denominator units must use different PCMs.", messages.ERROR)
            return msg

    if self.num_units is not None and self.ratio_units is not None:
        if self.num_units.ct_id == self.ratio_units.ct_id:
            reset_publication(self)
            msg = (self.__str__(
            ) + ": Numerator and ratio units must use different PCMs.", messages.ERROR)
            return msg

    if self.den_units is not None and self.ratio_units is not None:
        if self.den_units.ct_id == self.ratio_units.ct_id:
            reset_publication(self)
            msg = (self.__str__(
            ) + ": Denominator and ratio units must use different PCMs.", messages.ERROR)
            return msg

    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='ratio-type' type='s3m:TypeOfRatio'/>\n")

    dt_str += padding.rjust(indent + 8) + \
        ("<xs:element maxOccurs='1' minOccurs='0' name='numerator'>\n")
    dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent + 10) + \
        ("<xs:restriction base='xs:decimal'>\n")
    if self.num_min_inclusive:
        dt_str += padding.rjust(indent + 12) + ("<xs:minInclusive value='" +
                                                str(self.num_min_inclusive).strip() + "'/>\n")
    if self.num_min_exclusive:
        dt_str += padding.rjust(indent + 12) + ("<xs:minExclusive value='" +
                                                str(self.num_min_exclusive).strip() + "'/>\n")
    if self.num_max_inclusive:
        dt_str += padding.rjust(indent + 12) + ("<xs:maxInclusive value='" +
                                                str(self.num_max_inclusive).strip() + "'/>\n")
    if self.num_max_exclusive:
        dt_str += padding.rjust(indent + 12) + ("<xs:maxExclusive value='" +
                                                str(self.num_max_exclusive).strip() + "'/>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    dt_str += padding.rjust(indent + 8) + \
        ("<xs:element maxOccurs='1' minOccurs='0' name='denominator'>\n")
    dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
    dt_str += padding.rjust(indent + 10) + \
        ("<xs:restriction base='xs:decimal'>\n")
    if self.den_min_inclusive is not None:
        dt_str += padding.rjust(indent + 12) + ("<xs:minInclusive value='" +
                                                str(self.den_min_inclusive).strip() + "'/>\n")
    if self.den_min_exclusive is not None:
        dt_str += padding.rjust(indent + 12) + ("<xs:minExclusive value='" +
                                                str(self.den_min_exclusive).strip() + "'/>\n")
    if self.den_max_inclusive is not None:
        dt_str += padding.rjust(indent + 12) + ("<xs:maxInclusive value='" +
                                                str(self.den_max_inclusive).strip() + "'/>\n")
    if self.den_max_exclusive is not None:
        dt_str += padding.rjust(indent + 12) + ("<xs:maxExclusive value='" +
                                                str(self.den_max_exclusive).strip() + "'/>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
    dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    if not mag_constrained:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdratio-value' type='xs:decimal'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0'  name='Xdratio-value'>\n")
        dt_str += padding.rjust(indent + 10) + ("<xs:simpleType>\n")
        dt_str += padding.rjust(indent + 10) + \
            ("<xs:restriction base='xs:decimal'>\n")
        if self.min_magnitude is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:minInclusive value='" +
                                                    str(self.min_magnitude).strip() + "'/>\n")
        if self.max_magnitude is not None:
            dt_str += padding.rjust(indent + 12) + ("<xs:maxInclusive value='" +
                                                    str(self.max_magnitude).strip() + "'/>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:restriction>\n")
        dt_str += padding.rjust(indent + 10) + ("</xs:simpleType>\n")
        dt_str += padding.rjust(indent + 8) + ("</xs:element>\n")

    if self.num_units:
        if not self.num_units.published:
            reset_publication(self)
            msg = ("Units: " + self.num_units.label +
                   " hasn't been published. Please publish the object and retry.", messages.ERROR)
        else:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='numerator-units' type='s3m:mc-" + self.num_units.ct_id + "'/> \n")

    if self.den_units:
        if not self.den_units.published:
            reset_publication(self)
            msg = ("Units: " + self.den_units.label +
                   " hasn't been published. Please publish the object and retry.", messages.ERROR)
        else:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='denominator-units' type='s3m:mc-" + self.den_units.ct_id + "'/>\n")

    if self.ratio_units:
        if not self.ratio_units.published:
            reset_publication(self)
            msg = ("Units: " + self.ratio_units.label +
                   " hasn't been published. Please publish the object and retry.", messages.ERROR)
        else:
            dt_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='1' name='ratio-units' type='s3m:mc-" + self.ratio_units.ct_id + "'/> \n")

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_XdTemporal(self):
    """
    All time based options.
    Only one duration type is allowed.  If multiple durations are chosen by the modeller, a modelling error is raised.
    If any duration type is allowed then no other types are allowed.
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # generate and save the code for a R function.
    self.r_code = pct_rcode(self, 'XdTemporal')
    self.save()

    # fix double quotes in label
    self.label.replace('"', '&quot;')
    self.save()

    # it is a modelling error to use multiple reference ranges with the same
    # Xdinterval in a Xdtemporal
    used_ctid_list = []

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    dt_str = ''
    indent = 2
    docs = escape(self.description)
    padding = ('').rjust(indent)

    dt_str = '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    dt_str += padding.rjust(indent + 4) + ("<xs:documentation>\n")
    dt_str += padding.rjust(indent + 4) + (docs + "\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    dt_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            dt_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            dt_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:XdTemporalType'/>\n")
            dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            dt_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        dt_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        dt_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:XdTemporalType'/>\n")
        dt_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        dt_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    dt_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    dt_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    dt_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    dt_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:XdTemporalType'>\n")
    dt_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    # XdAny
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")
    dt_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:ExceptionalValue'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vtb)) + "' name='vtb' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_vte)) + "' name='vte' type='xs:dateTime'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" +
                                           str(int(self.require_tr)) + "' name='tr' type='xs:dateTimeStamp'/>\n")
    dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='" + str(
        int(self.require_mod)) + "' name='modified' type='xs:dateTimeStamp'/>\n")
    # XdOrdered
    if len(self.reference_ranges.all()) != 0:  # reference ranges defined
        for rr in self.reference_ranges.all():
            if not rr.published:
                reset_publication(self)
                msg = ("Reference Range: " + rr.label +
                       " hasn't been published. Please publish the reference range and retry.", messages.ERROR)
                return msg
            else:
                dt_str += padding.rjust(indent + 8) + \
                    "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + rr.ct_id + "'/> \n"
                if rr.interval.ct_id not in used_ctid_list:
                    # track the used XdInterval IDs
                    used_ctid_list.append(rr.interval.ct_id)
                else:
                    reset_publication(self)
                    msg = (self.__str__(
                    ) + ": You cannot use multiple ReferenceRanges with the same XdInterval declared as the data-range in one XdOrdinal.", messages.ERROR)
                    return msg
    if self.normal_status:
        dt_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='normal-status' type='xs:string' fixed='" +
                                               escape(self.normal_status.strip()) + "'/> \n")
    else:
        self.normal_status = ''

    # XdTemporal - every element must be included as either allowed or not
    # allowed.
    if (self.allow_duration and self.allow_ymduration) or (self.allow_duration and self.allow_dtduration) or (self.allow_ymduration and self.allow_dtduration):
        reset_publication(self)
        msg = (self.__str__(
        ) + ": Only one of the duration types are allowed to be selected.", messages.ERROR)
        return msg

    if (self.allow_duration or self.allow_ymduration or self.allow_dtduration) and (self.allow_date or self.allow_time or self.allow_datetime or self.allow_day or self.allow_month or self.allow_year or self.allow_year_month or self.allow_month_day):
        reset_publication(self)
        msg = (self.__str__(
        ) + ": You cannot have a duration mixed with other temporal types.", messages.ERROR)
        return msg

    if self.allow_date:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-date' type='xs:date'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-date' type='xs:date'/>\n")

    if self.allow_time:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-time' type='xs:time'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-time' type='xs:time'/>\n")

    if self.allow_datetime:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-datetime' type='xs:dateTime'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-datetime' type='xs:dateTime'/>\n")

    if self.allow_datetimestamp:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-datetime-stamp' type='xs:dateTimeStamp'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-datetime-stamp' type='xs:dateTimeStamp'/>\n")

    if self.allow_day:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-day' type='xs:gDay'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-day' type='xs:gDay'/>\n")

    if self.allow_month:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-month' type='xs:gMonth'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-month' type='xs:gMonth'/>\n")

    if self.allow_year:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-year' type='xs:gYear'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-year' type='xs:gYear'/>\n")

    if self.allow_year_month:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-year-month' type='xs:gYearMonth'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-year-month' type='xs:gYearMonth'/>\n")

    if self.allow_month_day:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-month-day' type='xs:gMonthDay'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-month-day' type='xs:gMonthDay'/>\n")

    if self.allow_duration:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-duration' type='xs:duration'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-duration' type='xs:duration'/>\n")

    if self.allow_ymduration:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-ymduration' type='xs:yearMonthDuration'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-ymduration' type='xs:yearMonthDuration'/>\n")

    if self.allow_dtduration:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='Xdtemporal-dtduration' type='xs:dayTimeDuration'/>\n")
    else:
        dt_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='0' minOccurs='0' name='Xdtemporal-dtduration' type='xs:dayTimeDuration'/>\n")

    dt_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            dt_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    dt_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    dt_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    dt_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = dt_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_Party(self):
    """
    Publish a Party definition.

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    party_str = ''
    xref_id = None

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    party_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    party_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    party_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    party_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    party_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    party_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            party_str += padding.rjust(indent + 2) + (
                "<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            party_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:PartyType'/>\n")
            party_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                      escape(self.label.strip()) + "</rdfs:label>\n")
            party_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__(
            ) + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            party_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        party_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        party_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:PartyType'/>\n")
        party_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    party_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    party_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    party_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    party_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:PartyType'>\n")
    party_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    party_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                              '"' + escape(self.label.strip()) + '"' + "/>\n")

    party_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='party-name' type='xs:string'/>\n")

    if self.external_ref.all():
        for xref in self.external_ref.all():
            if not xref.published:
                reset_publication(self)
                msg = ("External Reference: " + xref.__str__().strip() +
                       " hasn't been published. Please publish the XdLink and retry.", messages.ERROR)
                return msg
            else:
                party_str += padding.rjust(
                    indent + 8) + "<xs:element maxOccurs='1' minOccurs='0' name='party-ref' type='s3m:mc-" + str(xref.ct_id) + "'/>\n"

    if self.details:
        if not self.details.published:
            reset_publication(self)
            msg = ("Cluster: " + self.details.__str__().strip() +
                   " hasn't been published. Please publish the item and retry.", messages.ERROR)
            return msg
        party_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='party-details' type='s3m:mc-" + str(self.details.ct_id) + "'/>\n")

    party_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            party_str += padding.rjust(indent + 8) + \
                (str1 + '"' + a + '"' + str2)

    party_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    party_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    party_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = party_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_Audit(self):
    """
    Writes the complete DM complexType code for Audit.

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    aud_str = ''

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    aud_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    aud_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    aud_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    aud_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    aud_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    aud_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            aud_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            aud_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:AuditType'/>\n")
            aud_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                    escape(self.label.strip()) + "</rdfs:label>\n")
            aud_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__(
            ) + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            aud_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        aud_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        aud_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:AuditType'/>\n")
        aud_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    aud_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    aud_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    aud_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    aud_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:AuditType'>\n")
    aud_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    aud_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                            '"' + escape(self.label.strip()) + '"' + "/>\n")

    if not self.system_id:
        msg = ("System ID: (XdString) has not been selected.", messages.ERROR)
        return msg
    else:
        if not self.system_id.published:
            reset_publication(self)
            msg = ("System ID: (XdString) " + self.system_id.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        aud_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' name='system-id' type='s3m:mc-" + str(self.system_id.ct_id) + "'/>\n")

    if self.system_user:
        if not self.system_user.published:
            reset_publication(self)
            msg = ("System User: (Party) " + self.system_user.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        aud_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='system-user' type='s3m:mc-" + str(self.system_user.ct_id) + "'/>\n")

    if self.location:
        if not self.location.published:
            reset_publication(self)
            msg = ("Location: (Cluster) " + self.location.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        aud_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='location' type='s3m:mc-" + str(self.location.ct_id) + "'/>\n")

    aud_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='timestamp' type='xs:dateTimeStamp'/>\n")

    aud_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            aud_str += padding.rjust(indent + 8) + \
                (str1 + '"' + a + '"' + str2)

    aud_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    aud_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    aud_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = aud_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_Attestation(self):
    """
    Publish an Attestation definition.

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    att_str = ''

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    att_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'>\n")
    att_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    att_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    att_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    att_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    att_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            att_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            att_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:AttestationType'/>\n")
            att_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                    escape(self.label.strip()) + "</rdfs:label>\n")
            att_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__(
            ) + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            att_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        att_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        att_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:AttestationType'/>\n")
        att_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    att_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    att_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    att_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    att_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:AttestationType'>\n")
    att_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    att_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                            '"' + escape(self.label.strip()) + '"' + "/>\n")

    if self.view:
        if not self.view.published:
            reset_publication(self)
            msg = ("View: (XdFile) " + self.view.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        att_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='view' type='s3m:mc-" + str(self.view.ct_id) + "'/> \n")

    if self.proof:
        if not self.proof.published:
            reset_publication(self)
            msg = ("Proof: (XdFile) " + self.proof.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        att_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='proof' type='s3m:mc-" + str(self.proof.ct_id) + "'/> \n")

    if self.reason:
        if not self.reason.published:
            reset_publication(self)
            msg = ("Reason: (XdString) " + self.reason.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        att_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='reason' type='s3m:mc-" + str(self.reason.ct_id) + "'/> \n")

    if self.committer:
        if not self.committer.published:
            reset_publication(self)
            msg = ("Committer: (Party) " + self.committer.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        att_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='committer' type='s3m:mc-" + str(self.committer.ct_id) + "'/>\n")

    att_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='committed' type='xs:dateTimeStamp'/>\n")
    att_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' default='true' name='pending' type='xs:boolean'/>\n")
    att_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            att_str += padding.rjust(indent + 8) + \
                (str1 + '"' + a + '"' + str2)

    att_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    att_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    att_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = att_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_Participation(self):
    """
    Writes the complete DM complexType code for the Participation.
    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    ptn_str = ''

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    ptn_str += '\n\n' + padding.rjust(indent) + (
        "<xs:complexType name='mc-" + self.ct_id + "' xml:lang='" + self.lang + "'> \n")
    ptn_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    ptn_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    ptn_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    ptn_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    ptn_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            ptn_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            ptn_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:ParticipationType'/>\n")
            ptn_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                    escape(self.label.strip()) + "</rdfs:label>\n")
            ptn_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__(
            ) + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            ptn_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        ptn_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        ptn_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:ParticipationType'/>\n")
        ptn_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    ptn_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    ptn_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    ptn_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    ptn_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:ParticipationType'>\n")
    ptn_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    ptn_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                            '"' + escape(self.label.strip()) + '"' + "/>\n")

    # Participation
    if self.performer:
        if not self.performer.published:
            reset_publication(self)
            msg = ("Performer: " + self.performer.__str__().strip() +
                   " hasn't been published. Please publish the XdURI and retry.", messages.ERROR)
            return msg
        ptn_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='performer' type='s3m:mc-" + str(self.performer.ct_id) + "'/>\n")
    else:
        reset_publication(self)
        msg = ("You must define a performer (Party) for Participation: " +
               self.__str__().strip(), messages.ERROR)
        return msg

    if self.function:
        if not self.function.published:
            reset_publication(self)
            msg = ("Function: (XdString) " + self.function.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        ptn_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='function' type='s3m:mc-" + str(self.function.ct_id) + "'/>\n")
    else:
        reset_publication(self)
        msg = ("You must define a function (XdString) for Participation: " +
               self.__str__().strip(), messages.ERROR)
        return msg

    if self.mode:
        if not self.mode.published:
            reset_publication(self)
            msg = ("Mode: (XdString) " + self.simple_mode.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        ptn_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='mode' type='s3m:mc-" + str(self.mode.ct_id) + "'/> \n")
    else:
        reset_publication(self)
        msg = ("You must define a mode (XdString) for Participation: " +
               self.__str__().strip(), messages.ERROR)
        return msg

    ptn_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='start' type='xs:dateTimeStamp'/>\n")
    ptn_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='end' type='xs:dateTimeStamp'/>\n")

    ptn_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            ptn_str += padding.rjust(indent + 8) + \
                (str1 + '"' + a + '"' + str2)

    ptn_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    ptn_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    ptn_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = ptn_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_Cluster(self):
    """
    Publish a Cluster definition.

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    cl_str = ''
    links_id = None
    has_content = False

    # fix double quotes in cluster-subject
    self.label.replace('"', '&quot;')
    self.save()

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    cl_str += '\n\n' + \
        padding.rjust(indent) + ("<xs:complexType name='mc-" +
                                 self.ct_id + "'> \n")
    cl_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    cl_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    cl_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    cl_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    cl_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            cl_str += padding.rjust(indent + 2) + \
                ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            cl_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:ClusterType'/>\n")
            cl_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                   escape(self.label.strip()) + "</rdfs:label>\n")
            cl_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" +
                                                   po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            cl_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        cl_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        cl_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:ClusterType'/>\n")
        cl_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                               escape(self.label.strip()) + "</rdfs:label>\n")
        cl_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    cl_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    cl_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    cl_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    cl_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:ClusterType'>\n")
    cl_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")

    # Cluster
    cl_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                           '"' + escape(self.label.strip()) + '"' + "/>\n")

    if self.clusters.all():
        has_content = True
        for item in self.clusters.all():
            if item.ct_id != self.ct_id:  # cannot put a Cluster inside itself
                if not item.published:
                    reset_publication(self)
                    msg = ("(Cluster) " + item.__str__().strip() +
                           " hasn't been published.", messages.ERROR)
                    return msg
                cl_str += padding.rjust(indent + 4) + (
                    "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.ct_id) + "'/>\n")

            else:
                reset_publication(self)
                msg = ("(Cluster) " + item.__str__().strip() +
                       " NOTICE: You cannot nest a Cluster inside of itself at any level.", messages.ERROR)
                return msg

    if self.xdboolean.all():
        has_content = True
        for item in self.xdboolean.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdBoolean) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdlink.all():
        has_content = True
        for item in self.xdlink.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdLink) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdstring.all():
        has_content = True
        for item in self.xdstring.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdString) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdfile.all():
        has_content = True
        for item in self.xdfile.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdFile) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdordinal.all():
        has_content = True
        for item in self.xdordinal.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdOrdinal) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdcount.all():
        has_content = True
        for item in self.xdcount.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdCount) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdquantity.all():
        has_content = True
        for item in self.xdquantity.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdQuantity) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdratio.all():
        has_content = True
        for item in self.xdratio.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdRatio) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    if self.xdtemporal.all():
        has_content = True
        for item in self.xdtemporal.all():
            if not item.published:
                reset_publication(self)
                msg = ("(XdTemporal) " + item.__str__().strip() +
                       " hasn't been published. Please publish the object and retry.", messages.ERROR)
            cl_str += padding.rjust(indent + 4) + (
                "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(item.adapter_ctid) + "'/>\n")

    cl_str += padding.rjust(indent + 6) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            cl_str += padding.rjust(indent + 8) + (str1 + '"' + a + '"' + str2)

    cl_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    cl_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    cl_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if not has_content:
        reset_publication(self)
        msg = ("Cluster: " + self.__str__().strip() +
               " appears to be empty. You cannot publish an empty Cluster.", messages.ERROR)

    if msg[1] == messages.SUCCESS:
        self.schema_code = cl_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg


def publish_Entry(self):
    """
    Publish an Entry definition.

    """
    self.ct_id = str(uuid4())
    self.published = False
    self.save()

    # default return message
    msg = (self.__str__().strip() + ' was Published.', messages.SUCCESS)
    entry_str = ''
    links_id = None
    op_id = None

    indent = 2
    padding = ('').rjust(indent)

    # Create the datatype
    entry_str += padding.rjust(indent) + \
        ("<xs:complexType name='mc-" + self.ct_id + "'> \n")
    entry_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
    entry_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
    entry_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
    entry_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
    # Write the semantic links. There must be the same number of attributes
    # and links or none will be written.
    entry_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
    if len(self.pred_obj.all()) != 0:
        for po in self.pred_obj.all():
            entry_str += padding.rjust(indent + 2) + (
                "<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
            entry_str += padding.rjust(indent + 2) + \
                ("<rdfs:subClassOf rdf:resource='s3m:EntryType'/>\n")
            entry_str += padding.rjust(indent + 2) + ("<rdfs:label>" +
                                                      escape(self.label.strip()) + "</rdfs:label>\n")
            entry_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__(
            ) + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
            entry_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    else:
        entry_str += padding.rjust(indent + 2) + \
            ("<rdf:Description rdf:about='s3m:mc-" + self.ct_id + "'>\n")
        entry_str += padding.rjust(indent + 2) + \
            ("<rdfs:subClassOf rdf:resource='s3m:EntryType'/>\n")
        entry_str += padding.rjust(indent + 2) + ("</rdf:Description>\n")
    entry_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
    entry_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
    entry_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
    entry_str += padding.rjust(indent + 4) + \
        ("<xs:restriction base='s3m:EntryType'>\n")
    entry_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
    entry_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" +
                                              '"' + escape(self.label.strip()) + '"' + "/>\n")
    entry_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='entry-language' type='xs:language' fixed='" + self.language + "'/>\n")
    entry_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='1' name='entry-encoding' type='xs:string' fixed='" + self.encoding + "'/>\n")
    entry_str += padding.rjust(indent + 8) + (
        "<xs:element maxOccurs='1' minOccurs='0' name='current-state' type='xs:string' default='" + escape(self.state) + "'/>\n")
    if not self.data:
        reset_publication(self)
        msg = (self.__str__(
        ) + ": You cannot publish an Entry without a data element composed as a Cluster.", messages.ERROR)
        return msg
    else:
        if not self.data.published:
            reset_publication(self)
            msg = ("Cluster " + self.data.__str__().strip() +
                   " must be published before publishing the entry.", messages.ERROR)
            return msg
        entry_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='1' ref='s3m:me-" + str(self.data.ct_id) + "'/>\n")

    if self.subject:
        entry_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='subject' type='s3m:mc-" + str(self.subject.ct_id) + "'/>\n")
    else:
        reset_publication(self)
        msg = ("Entry " + self.__str__().strip() +
               " must have a subject (PartyType) defined.", messages.ERROR)
        return msg

    if not self.provider:
        reset_publication(self)
        msg = ("Entry " + self.__str__().strip() +
               " must have a provider defined.", messages.ERROR)
        return msg
    else:
        if not self.provider.published:
            reset_publication(self)
            msg = ("Entry " + self.provider.__str__().strip() +
                   " must be published before publishing the entry.", messages.ERROR)
            return msg
        entry_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='provider' type='s3m:mc-" + str(self.provider.ct_id) + "'/> \n")

    if not self.participations.all():
        entry_str += padding.rjust(indent + 8) + \
            ("<!-- No Participations -->\n")
    else:
        for op in self.participations.all():
            if not op.published:
                reset_publication(self)
                msg = ("Participation: " + op.__str__().strip() +
                       " hasn't been published. Please publish the Participation and retry.", messages.ERROR)
                return msg
            else:
                entry_str += padding.rjust(
                    indent + 8) + "<xs:element maxOccurs='unbounded' minOccurs='0' ref='s3m:me-" + str(op.ct_id) + "'/>\n"

    if self.protocol:
        if not self.protocol.published:
            reset_publication(self)
            msg = ("Protocol: " + self.protocol.__str__().strip() +
                   " hasn't been published. Please publish the XdString and retry.", messages.ERROR)
            return msg
        else:
            entry_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='0' name='protocol' type='s3m:mc-" + str(self.protocol.ct_id) + "'/>\n")
    else:
        entry_str += padding.rjust(indent + 8) + \
            ("<!-- No protocol model -->\n")

    if self.workflow:
        if not self.workflow.published:
            reset_publication(self)
            msg = ("Workflow: " + self.workflow.__str__().strip() +
                   " hasn't been published. Please publish the XdLink and retry.", messages.ERROR)
            return msg
        else:
            entry_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='0' name='workflow' type='s3m:mc-" + str(self.workflow.ct_id) + "'/>\n")
    else:
        entry_str += padding.rjust(indent + 8) + \
            ("<!-- No  workflow model -->\n")

    if self.audit:
        if not self.audit.published:
            reset_publication(self)
            msg = ("Audit " + self.audit.__str__().strip() +
                   " has not been published.", messages.ERROR)
            return msg
        entry_str += padding.rjust(indent + 8) + (
            "<xs:element maxOccurs='1' minOccurs='0' name='audit' type='s3m:mc-" + str(self.audit.ct_id) + "'/>\n")
    else:
        entry_str += padding.rjust(indent + 8) + ("<!-- No  audit model -->\n")

    if self.attestation:
        if not self.attestation.published:
            reset_publication(self)
            msg = ("Attestation: " + self.attestation.__str__().strip() +
                   " hasn't been published. Please publish the Attestation and retry.", messages.ERROR)
            return msg
        else:
            entry_str += padding.rjust(indent + 8) + (
                "<xs:element maxOccurs='1' minOccurs='0' name='attestation' type='s3m:mc-" + str(self.attestation.ct_id) + "'/>\n")
    else:
        entry_str += padding.rjust(indent + 8) + \
            ("<!-- No attestation model -->\n")

    if not self.links.all():
        entry_str += padding.rjust(indent + 8) + ("<!-- No entry links -->\n")
    else:
        for link in self.links.all():
            if not link.published:
                reset_publication(self)
                msg = ("Link: " + link.__str__().strip() +
                       " hasn't been published. Please publish the XdLink and retry.", messages.ERROR)
                return msg
            else:
                entry_str += padding.rjust(
                    indent + 8) + "<xs:element maxOccurs='1' minOccurs='0' ref='s3m:me-" + str(link.ct_id) + "'/>\n"

    entry_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
    if self.asserts:
        str1 = "<xs:assert test="
        str2 = "/>\n"
        for a in self.asserts.splitlines():
            entry_str += padding.rjust(indent + 8) + \
                (str1 + '"' + a + '"' + str2)

    entry_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
    entry_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
    entry_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

    if msg[1] == messages.SUCCESS:
        self.schema_code = entry_str.encode("utf-8")
        self.published = True
        self.save()
    else:
        reset_publication(self)

    return msg
