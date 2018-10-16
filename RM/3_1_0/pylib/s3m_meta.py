"""
Meta information classes used by a data model (DMType)

"""
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape
from urllib.parse import quote

from cuid import cuid
from validator_collection import checkers


class PartyType:
    """
    Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party
    information is to be anonymous then do not include the details element.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._party_name = None
        self._party_ref = None
        self._party_details = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class AuditType:
    """
    AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._system_id = None
        self._system_user = None
        self._location = None
        self._timestamp = None

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

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)

    def asXSD(self):
        """
        Return a XML Schema stub for the Audit.
        """

        indent = 2
        padding = ('').rjust(indent)
        aud_str = ''

        # Create the datatype
        aud_str += '\n\n' + padding.rjust(indent) + ("<xs:complexType name='mc-" + self.mcuid + "' xml:lang='" + self.lang + "'>\n")
        aud_str += padding.rjust(indent + 2) + ("<xs:annotation>\n")
        aud_str += padding.rjust(indent + 2) + ("<xs:documentation>\n")
        aud_str += padding.rjust(indent + 4) + (escape(self.description) + "\n")
        aud_str += padding.rjust(indent + 2) + ("</xs:documentation>\n")
        # Write the semantic links. There must be the same number of attributes
        # and links or none will be written.
        aud_str += padding.rjust(indent + 2) + ('<xs:appinfo>\n')
        aud_str += padding.rjust(indent + 2) + ("<rdfs:Class rdf:about='mc-" + self.mcuid + "'>\n")
        aud_str += padding.rjust(indent + 2) + ("<rdfs:subClassOf rdf:resource='" + RM_URI + "#AuditType'/>\n")
        aud_str += padding.rjust(indent + 2) + ("<rdfs:subClassOf rdf:resource='https://www.s3model.com/ns/s3m/s3model/RMC'/>\n")
        aud_str += padding.rjust(indent + 2) + ("<rdfs:label>" + escape(self.label.strip()) + "</rdfs:label>\n")
        if len(self.pred_obj.all()) != 0:
            for po in self.pred_obj.all():
                aud_str += padding.rjust(indent + 2) + ("<" + po.predicate.ns_abbrev.__str__() + ":" + po.predicate.class_name.strip() + " rdf:resource='" + quote(po.object_uri) + "'/>\n")
        aud_str += padding.rjust(indent + 2) + ("</rdfs:Class>\n")
        aud_str += padding.rjust(indent + 2) + ('</xs:appinfo>\n')
        aud_str += padding.rjust(indent + 2) + ("</xs:annotation>\n")
        aud_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
        aud_str += padding.rjust(indent + 4) + ("<xs:restriction base='s3m:AuditType'>\n")
        aud_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
        aud_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" + '"' + escape(self.label.strip()) + '"' + "/>\n")

        if not self.system_id:
            msg = ("System ID: (XdString) has not been selected.", messages.ERROR)
            return msg
        else:
            if not self.system_id.published:
                reset_publication(self)
                msg = ("System ID: (XdString) " + self.system_id.__str__().strip() + " has not been published.", messages.ERROR)
                return msg
            aud_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='system-id' type='s3m:mc-" + str(self.system_id.mcuid) + "'/>\n")

        if self.system_user:
            if not self.system_user.published:
                reset_publication(self)
                msg = ("System User: (Party) " + self.system_user.__str__().strip() + " has not been published.", messages.ERROR)
                return msg
            aud_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='0' name='system-user' type='s3m:mc-" + str(self.system_user.mcuid) + "'/>\n")

        if self.location:
            if not self.location.published:
                reset_publication(self)
                msg = ("Location: (Cluster) " + self.location.__str__().strip() + " has not been published.", messages.ERROR)
                return msg
            aud_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='0' name='location' type='s3m:mc-" + str(self.location.mcuid) + "'/>\n")

        aud_str += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='timestamp' type='xs:dateTime'/>\n")

        aud_str += padding.rjust(indent + 8) + ("</xs:sequence>\n")
        aud_str += padding.rjust(indent + 6) + ("</xs:restriction>\n")
        aud_str += padding.rjust(indent + 4) + ("</xs:complexContent>\n")
        aud_str += padding.rjust(indent + 2) + ("</xs:complexType>\n\n")

        return(aud_str)


class AttestationType:
    """
    Record an attestation by a party of the DM content. The type of attestation is recorded by the reason attribute, which my be coded.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._view = None
        self._proof = None
        self._reason = None
        self._committer = None
        self._committed = None
        self._pending = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class ParticipationType:
    """
    Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse. Can be used to record past or future participations.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self.label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._performer = None
        self._function = None
        self._mode = None
        self._start = None
        self._end = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)

