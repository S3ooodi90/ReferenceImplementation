"""
The S3Model Reference Model code to write DM schemas.
"""
import os
from datetime import date
import hashlib
import zipfile
from shutil import copy, rmtree
from xml.sax.saxutils import escape
from urllib.parse import quote
import json
import xmltodict
from lxml import etree

from django.core.files.base import ContentFile
from django.contrib import messages

from s3m.settings import DM_LIB, MEDIA_ROOT, RMVERSION, RM_URI

from dmgen.models import NS, get_rcode

from .ig import cluster, Xd_link, party, participation, Xd_string, audit, attestation

from .fg import buildHTML


class DMPkg(object):
    """
    The class that collects all of the components for a DM package.
    A DM package consists of the DM (XML Schema), an XML instance, a JSON instance and an RStudio project.
    Also, the dm-description.xsl file is copied into the package from the root of the DM Library.
    """

    def __init__(self, dm, request):
        self.dm = dm
        self.request = request
        self.xsd = ''
        self.html = ''
        self.xml = ''
        self.used_uuids = {}
        self.clusters = []
        self.adapters = []
        self.xsdHead = self.xsdHeader()
        self.xsdTail = '\n</xs:schema>\n'
        self.xmlHead = self.xmlHeader()
        self.xmlTail = '</s3m:' + self.dm.identifier + '>\n'
        self.xsdMetadata = self.xsdMetadata()
        self.rm = '<!-- Include the RM Schema -->\n  <xs:include schemaLocation="https://www.s3model.com/ns/s3m/s3model_' + \
            RMVERSION.replace('.', '_') + '.xsd"/>\n'

    def xmlHeader(self):
        """
        Build the header for the example instance
        """
        hstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
        hstr += '<s3m:' + self.dm.identifier + '\n'
        for ns in NS.objects.all():
            hstr += '  xmlns:' + ns.abbrev.strip() + '="' + ns.uri.strip() + '"\n'
        hstr += 'xsi:schemaLocation="https://www.s3model.com/ns/s3m/  http://dmgen.s3model.com/dmlib/' + \
            self.dm.identifier + '.xsd">\n'
        return(hstr)

    def xsdHeader(self):
        """
        Build the header string for the XSD
        """
        hstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
        hstr += '<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>\n'
        hstr += '<xs:schema\n'
        for ns in NS.objects.all():
            hstr += '  xmlns:' + ns.abbrev.strip() + '="' + ns.uri.strip() + '"\n'
        hstr += '  targetNamespace="https://www.s3model.com/ns/s3m/"\n'
        hstr += '  xml:lang="' + self.dm.dc_language.strip() + \
            '">\n'
        return(hstr)

    def xsdMetadata(self):
        mds = '<!-- Metadata -->\n  <xs:annotation><xs:appinfo><rdf:RDF><rdf:Description\n'
        mds += '    rdf:about="dm-' + str(self.dm.ct_id) + '">\n'
        mds += '    <dc:title>' + \
            escape(self.dm.title.strip()) + '</dc:title>\n'
        mds += '    <dc:creator>' + \
            escape(self.dm.author.__str__()) + '</dc:creator>\n'
        if len(self.dm.contrib.all()) != 0:
            for c in self.dm.contrib.all():
                mds += '    <dc:contributor>' + \
                    escape(c.__str__()) + '</dc:contributor>\n'
        mds += '    <dc:subject>' + \
            escape(self.dm.subject.strip()) + '</dc:subject>\n'
        mds += '    <dc:rights>' + escape(self.dm.rights) + '</dc:rights>\n'
        mds += '    <dc:relation>' + \
            escape(self.dm.relation.strip()) + '</dc:relation>\n'
        mds += '    <dc:coverage>' + \
            escape(self.dm.coverage.strip()) + '</dc:coverage>\n'
        mds += '    <dc:type>' + \
            escape(self.dm.dc_type.strip()) + '</dc:type>\n'
        mds += '    <dc:identifier>' + \
            escape(self.dm.identifier.strip()) + '</dc:identifier>\n'
        mds += '    <dc:description>' + \
            escape(self.dm.description.strip()) + '</dc:description>\n'
        mds += '    <dc:publisher>' + \
            escape(self.dm.publisher.strip()) + '</dc:publisher>\n'
        mds += '    <dc:date>' + str(self.dm.pub_date) + '</dc:date>\n'
        mds += '    <dc:format>' + \
            escape(self.dm.dc_format.strip()) + '</dc:format>\n'
        mds += '    <dc:language>' + \
            escape(self.dm.dc_language.strip()) + '</dc:language>\n'
        mds += '  </rdf:Description></rdf:RDF></xs:appinfo></xs:annotation>\n'
        return(mds)

    def registerUUID(self, uuid, rmtype, sg=None):
        """
        Register all of the UUIDs used for MCs in the DM. Insure that each complexType is included only one time.
        uuid is a string representation of the UUID.
        rmtype is a string representing the RM type.
        sg is a string representing the substitution group needed.
        """
        new = True
        if uuid in self.used_uuids:
            self.used_uuids[uuid].append((rmtype, sg))
            new = False
        else:
            self.used_uuids[uuid] = [(rmtype, sg)]

        return(new)

    def processDM(self):
        msg = ("The DM complexType was generated.", messages.SUCCESS)

        entry = self.dm.entry

        # build the DMType restriction
        if msg[1] == messages.SUCCESS:
            self.xsd += '<xs:element name="' + self.dm.identifier + \
                '" type="s3m:mc-' + str(self.dm.ct_id) + '"/>\n'
            self.xsd += '<xs:complexType name="mc-' + str(self.dm.ct_id) + '"> \n'
            self.xsd += '  <xs:annotation>\n'
            self.xsd += '    <xs:appinfo>\n'
            self.xsd += '      <rdf:Description rdf:about="mc-' + str(self.dm.ct_id) + '">\n'
            self.xsd += '        <rdfs:subClassOf rdf:resource="' + RM_URI + 'DMType"/>\n'
            self.xsd += '        <rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
            self.xsd += '        <rdfs:label>' + \
                escape(self.dm.title.strip()) + '</rdfs:label>\n'
            if len(self.dm.pred_obj.all()) != 0:
                for po in self.dm.pred_obj.all():
                    self.xsd += "        <" + po.predicate.ns_abbrev.__str__() + ":" + \
                        po.predicate.class_name.strip() + " rdf:resource='" + \
                        quote(po.object_uri) + "'/>\n"

            self.xsd += '      </rdf:Description>\n'
            self.xsd += '    </xs:appinfo>\n'
            self.xsd += '  </xs:annotation>\n'
            self.xsd += '  <xs:complexContent>\n'
            self.xsd += '    <xs:restriction base="s3m:DMType">\n'
            self.xsd += '      <xs:sequence>\n'
            self.xsd += '        <xs:element maxOccurs="1" minOccurs="1" ref="s3m:ms-' + \
                str(entry.ct_id) + '"/> \n'
            self.xsd += '      </xs:sequence>\n'
            if self.dm.asserts:
                str1 = '      <xs:assert test='
                str2 = '/>\n'
                for a in self.dm.asserts.splitlines().strip():
                    self.xsd += str1 + '"' + a + '"' + str2
            self.xsd += '    </xs:restriction>\n'
            self.xsd += '  </xs:complexContent>\n'
            self.xsd += '</xs:complexType>\n\n'

            # this registration should always succeed, but it is checked here anyway.
            if self.registerUUID(entry.ct_id, 'EntryType', 'Definition'):
                msg = self.processEntry(entry)

        return(msg)

    def processEntry(self, entry):
        indent = ""
        link_str = ''
        msg = ("The Entry was generated.", messages.SUCCESS)
        self.xsd += '\n<!-- Entry -->\n'
        if not entry.published:
            msg = ("The Entry has not been published.", messages.ERROR)
            return(msg)

        else:
            # add the published Entry code to the schema and example instance
            # data
            self.xsd += entry.schema_code
            self.xml += """<s3m:ms-""" + str(entry.ct_id) + """>\n"""
            self.xml += """<label>""" + entry.label + """</label>\n"""
            self.xml += """<entry-language>""" + entry.language + """</entry-language>\n"""
            self.xml += """<entry-encoding>""" + entry.encoding + """</entry-encoding>\n"""
            self.xml += """<current-state>""" + entry.state + """</current-state>\n"""

            # links - we need to process links first because a XdLink 'could' be
            # reused in a later Cluster and we need to insure it gets a
            # substitution group PCS
            if entry.links.all():
                for link in entry.links.all():
                    if self.registerUUID(link.ct_id, 'XdLinkType', 'XdLink'):
                        self.xsd += link.schema_code
                        # we put the XdLink instance info in a temp string and
                        # add it at the bottom of the Entry
                        link_str += Xd_link(link, indent)
                        if msg[1] == messages.ERROR:
                            return(msg)

            # data
            if entry.data:
                if self.registerUUID(entry.data.ct_id, 'ClusterType', 'Item'):
                    self.xsd += entry.data.schema_code
                    msg = self.processCluster(entry.data)
                    self.xml += cluster(entry.data, indent)
                    if msg[1] == messages.ERROR:
                        return(msg)
            else:
                msg = (
                    "The Entry is missing a Data (ClusterType) model.", messages.ERROR)
                return(msg)

            # subject
            if entry.subject:
                if self.registerUUID(entry.subject.ct_id, 'PartyType'):
                    self.xsd += entry.subject.schema_code
                    self.xml += "<subject>\n"
                    self.xml += party(entry.subject, indent)
                    self.xml += "</subject>\n"
                    msg = self.processParty(entry.subject)
                    if msg[1] == messages.ERROR:
                        return(msg)

            # provider
            if entry.provider:
                if self.registerUUID(entry.provider.ct_id, 'PartyType'):
                    self.xsd += entry.provider.schema_code
                    self.xml += "<provider>\n"
                    self.xml += party(entry.provider, indent)
                    self.xml += "</provider>\n"
                    msg = self.processParty(entry.provider)
                    if msg[1] == messages.ERROR:
                        return(msg)

            # participations
            if entry.participations.all():
                for part in entry.participations.all():
                    if self.registerUUID(part.ct_id, 'ParticipationType', 'Participation'):
                        self.xsd += part.schema_code
                        self.xml += participation(part, indent)
                        msg = self.processParticipation(part)
                        if msg[1] == messages.ERROR:
                            return(msg)

            # protocol
            if entry.protocol:
                if self.registerUUID(entry.protocol.ct_id, 'XdStringType'):
                    self.xsd += entry.protocol.schema_code
                    self.xml += "<protocol>\n"
                    self.xml += Xd_string(entry.protocol, indent, False)
                    self.xml += "</protocol>\n"

            # workflow
            if entry.workflow:
                if self.registerUUID(entry.workflow.ct_id, 'XdLinkType'):
                    self.xsd += entry.workflow.schema_code
                    self.xml += "<workflow>\n"
                    self.xml += Xd_link(entry.workflow, indent, False)
                    self.xml += "</workflow>\n"

            # audit
            if entry.audit.all():
                if self.registerUUID(entry.audit.ct_id, 'AuditType'):
                    self.xsd += entry.audit.schema_code
                    msg = self.processAudit(entry.audit)
                    self.xml += "<audit>\n"
                    self.xml += audit(entry.audit, indent)
                    self.xml += "</audit>\n"
                    if msg[1] == messages.ERROR:
                        return(msg)

            # attestation
            if entry.attestation:
                if self.registerUUID(entry.attestation.ct_id, 'AuditType'):
                    self.xsd += entry.attestation.schema_code
                    msg = self.processAttestation(entry.attestation)
                    self.xml += "<attestation>\n"
                    self.xml += attestation(entry.attestation, indent)
                    self.xml += "</attestation>\n"
                    if msg[1] == messages.ERROR:
                        return(msg)

            # add the XdLink string to the XML instance
            self.xml += link_str
            self.xml += """</s3m:ms-""" + str(entry.ct_id) + """>\n"""

        return(msg)

    def processCluster(self, cluster):
        msg = ("Processed " + cluster.label, messages.SUCCESS)

        # Clusters
        for clust in cluster.clusters.all():
            self.clusters.append(clust.ct_id)
            # first check for Cluster loops that cannot be resolved.
            if self.clusters.count(clust.ct_id) > 100:
                msg = ("I think the DMGEN is in a loop because you have embedded a Cluster inside itself on some level, OR there are more than 100 embedded Clusters, which seems kind of ridiculous.", messages.ERROR)
                return(msg)

            # register the clusters
            if self.registerUUID(clust.ct_id, 'ClusterType', 'Items'):
                self.xsd += clust.schema_code
                msg = self.processCluster(clust)
                if msg[1] == messages.ERROR:
                    return(msg)

        # XdBooleans in Cluster
        for Xd in cluster.xdboolean.all():
            if self.registerUUID(Xd.ct_id, 'XdBooleanType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdBoolean: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code   # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdLinks in Cluster
        for Xd in cluster.xdlink.all():
            if self.registerUUID(Xd.ct_id, 'XdLinkType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdLink: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code   # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdStrings in Cluster
        for Xd in cluster.xdstring.all():
            if self.registerUUID(Xd.ct_id, 'XdStringType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdString: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code  # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdFiles in Cluster
        for Xd in cluster.xdfile.all():
            if self.registerUUID(Xd.ct_id, 'XdFileType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdFile: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code   # get the Xd code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdOrdinals in Cluster
        for Xd in cluster.xdordinal.all():
            if self.registerUUID(Xd.ct_id, 'XdOrdinalType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdOrdinal: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code   # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            # len 10 was arbitrarily chosen as an obviously
                            # incorrect code length.
                            if len(rr.schema_code) < 10:
                                msg = ("Something happened to your MC code. Check that ReferenceRange: " +
                                       rr.label + " is published.", messages.ERROR)
                                return(msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                # len 10 was arbitrarily chosen as an obviously
                                # incorrect code length.
                                if len(rr.interval.schema_code) < 10:
                                    msg = ("Something happened to your MC code. Check that XdInterval: " +
                                           rr.interval.label + " is published.", messages.ERROR)
                                    return(msg)
                                self.xsd += rr.interval.schema_code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdCounts in Cluster
        for Xd in cluster.xdcount.all():
            if self.registerUUID(Xd.ct_id, 'XdCountType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdCount: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code  # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            # len 10 was arbitrarily chosen as an obviously
                            # incorrect code length.
                            if len(rr.schema_code) < 10:
                                msg = ("Something happened to your MC code. Check that ReferenceRange: " +
                                       rr.label + " is published.", messages.ERROR)
                                return(msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                # len 10 was arbitrarily chosen as an obviously
                                # incorrect code length.
                                if len(rr.interval.schema_code) < 10:
                                    msg = ("Something happened to your MC code. Check that XdInterval: " +
                                           rr.interval.label + " is published.", messages.ERROR)
                                    return(msg)
                                self.xsd += rr.interval.schema_code
                if Xd.units:
                    if self.registerUUID(Xd.units.ct_id, 'Units'):
                        # len 10 was arbitrarily chosen as an obviously
                        # incorrect code length.
                        if len(Xd.units.schema_code) < 10:
                            msg = ("Something happened to your MC code. Check that Units: " +
                                   Xd.units.label + " is published.", messages.ERROR)
                            return(msg)
                        self.xsd += Xd.units.schema_code
                else:
                    msg = ("Your XdCount is missing a Xdcount-units value. This should have been a publishing error; <b>Contact the DMGEN authors</b>.", messages.ERROR)
                    return(msg)
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdQuantities in Cluster
        for Xd in cluster.xdquantity.all():
            if self.registerUUID(Xd.ct_id, 'XdQuantityType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdQuanitiy: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code  # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            # len 10 was arbitrarily chosen as an obviously
                            # incorrect code length.
                            if len(rr.schema_code) < 10:
                                msg = ("Something happened to your MC code. Check that ReferenceRange: " +
                                       rr.label + " is published.", messages.ERROR)
                                return(msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                # len 10 was arbitrarily chosen as an obviously
                                # incorrect code length.
                                if len(rr.interval.schema_code) < 10:
                                    msg = ("Something happened to your MC code. Check that XdInterval: " +
                                           rr.interval.label + " is published.", messages.ERROR)
                                    return(msg)
                                self.xsd += rr.interval.schema_code
                if Xd.units:
                    if self.registerUUID(Xd.units.ct_id, 'Units'):
                        # len 10 was arbitrarily chosen as an obviously
                        # incorrect code length.
                        if len(Xd.units.schema_code) < 10:
                            msg = ("Something happened to your MC code. Check that Units: " +
                                   Xd.units.label + " is published.", messages.ERROR)
                            return(msg)
                        self.xsd += Xd.units.schema_code
                else:
                    msg = ("Your XdQuantity is missing a Xdquantity-units value. This should have been a publishing error; <b>Contact the DMGEN authors</b>.", messages.ERROR)
                    return(msg)
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdRatios in Cluster
        for Xd in cluster.xdratio.all():
            if self.registerUUID(Xd.ct_id, 'XdRatioType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdRatio: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code   # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            # len 10 was arbitrarily chosen as an obviously
                            # incorrect code length.
                            if len(rr.schema_code) < 10:
                                msg = ("Something happened to your MC code. Check that ReferenceRange: " +
                                       rr.label + " is published.", messages.ERROR)
                                return(msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                # len 10 was arbitrarily chosen as an obviously
                                # incorrect code length.
                                if len(rr.interval.schema_code) < 10:
                                    msg = ("Something happened to your MC code. Check that XdInterval: " +
                                           rr.interval.label + " is published.", messages.ERROR)
                                    return(msg)
                                self.xsd += rr.interval.schema_code
                if Xd.num_units:
                    if self.registerUUID(Xd.num_units.ct_id, 'Units'):
                        # len 10 was arbitrarily chosen as an obviously
                        # incorrect code length.
                        if len(Xd.num_units.schema_code) < 10:
                            msg = ("Something happened to your MC code. Check that Units: " +
                                   Xd.num_units.label + " is published.", messages.ERROR)
                            return(msg)
                        self.xsd += Xd.num_units.schema_code
                if Xd.den_units:
                    if self.registerUUID(Xd.den_units.ct_id, 'Units'):
                        # len 10 was arbitrarily chosen as an obviously
                        # incorrect code length.
                        if len(Xd.den_units.schema_code) < 10:
                            msg = ("Something happened to your MC code. Check that Units: " +
                                   Xd.den_units.label + " is published.", messages.ERROR)
                            return(msg)
                        self.xsd += Xd.den_units.schema_code

                if Xd.ratio_units:
                    if self.registerUUID(Xd.ratio_units.ct_id, 'Units'):
                        # len 10 was arbitrarily chosen as an obviously
                        # incorrect code length.
                        if len(Xd.ratio_units.schema_code) < 10:
                            msg = ("Something happened to your MC code. Check that Units: " +
                                   Xd.ratio_units.label + " is published.", messages.ERROR)
                            return(msg)
                        self.xsd += Xd.ratio_units.schema_code

            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        # XdTemporals in Cluster
        for Xd in cluster.xdtemporal.all():
            if self.registerUUID(Xd.ct_id, 'XdTemporalType', 'XdAdapter-value'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(Xd.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdTemporall: " +
                           Xd.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += Xd.schema_code   # get the Xd code
                if Xd.reference_ranges.all():
                    for rr in Xd.reference_ranges.all():
                        if self.registerUUID(rr.ct_id, 'ReferenceRangeType', 'ReferenceRange'):
                            # len 10 was arbitrarily chosen as an obviously
                            # incorrect code length.
                            if len(rr.schema_code) < 10:
                                msg = ("Something happened to your MC code. Check that ReferenceRange: " +
                                       rr.label + " is published.", messages.ERROR)
                                return(msg)
                            self.xsd += rr.schema_code
                            if self.registerUUID(rr.interval.ct_id, 'XdIntervalType'):
                                # len 10 was arbitrarily chosen as an obviously
                                # incorrect code length.
                                if len(rr.interval.schema_code) < 10:
                                    msg = ("Something happened to your MC code. Check that XdInterval: " +
                                           rr.interval.label + " is published.", messages.ERROR)
                                    return(msg)
                                self.xsd += rr.interval.schema_code
            if not (Xd.adapter_ctid in self.adapters):
                # create the XdAdapterType code
                self.xsd += self.makeXdAdapter(Xd.ct_id,
                                               Xd.adapter_ctid, Xd.label)
                self.adapters.append(Xd.adapter_ctid)

        return(msg)

    def processParty(self, party):
        msg = ("Processed Party " + party.label, messages.SUCCESS)

        if party.external_ref.all():
            for ref in party.external_ref.all():
                if self.registerUUID(ref.ct_id, 'XdLinkType'):
                    # len 10 was arbitrarily chosen as an obviously incorrect
                    # code length.
                    if len(ref.schema_code) < 10:
                        msg = ("Something happened to your MC code. Check that XdLink: " +
                               ref.label + " is published.", messages.ERROR)
                        return(msg)
                    self.xsd += ref.schema_code

        if party.details:
            if self.registerUUID(party.details.ct_id, 'ClusterType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(party.details.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that Cluster: " +
                           party.details.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += party.details.schema_code
                msg = self.processCluster(party.details)

        return(msg)

    def processParticipation(self, part):
        msg = ("Processed Participation " + part.label, messages.SUCCESS)

        if part.performer:
            if self.registerUUID(part.performer.ct_id, 'PartyType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(part.performer.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that Party: " +
                           part.performer.label + " is published.", messages.ERROR)
                self.xsd += part.performer.schema_code
                msg = self.processParty(part.performer)

        if part.function:
            if self.registerUUID(part.function.ct_id, 'XdStringType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(part.function.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdString: " +
                           part.function.label + " is published.")
                    return(msg)
                self.xsd += part.function.schema_code

        if part.mode:
            if self.registerUUID(part.mode.ct_id, 'XdStringType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(part.mode.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdString: " +
                           part.mode.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += part.mode.schema_code

        return(msg)

    def processAudit(self, aud):
        msg = ("Processed Audit " + aud.label, messages.SUCCESS)

        if aud.system_id:
            if self.registerUUID(aud.system_id.ct_id, 'XdStringType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(aud.system_id.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdString: " +
                           aud.system_id.label + " is published.", messages.ERROR)
                self.xsd += aud.system_id.schema_code

        if aud.system_user:
            if self.registerUUID(aud.system_user.ct_id, 'PartyType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(aud.system_user.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that Party: " +
                           aud.system_user.label + " is published.")
                    return(msg)
                self.xsd += aud.system_user.schema_code
                msg = self.processParty(aud.system_user)

        if aud.location:
            if self.registerUUID(aud.location.ct_id, 'ClusterType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(aud.location.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that Cluster: " +
                           aud.location.label + " is published.", messages.ERROR)
                    return(msg)
                self.xsd += aud.location.schema_code
                msg = self.processCluster(aud.location)

        return(msg)

    def processAttestation(self, att):
        msg = ("Processed Attestation " + att.label, messages.SUCCESS)

        if att.view:
            if self.registerUUID(att.view.ct_id, 'XdFileType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(att.view.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdFile: " +
                           att.view.label + " is published.", messages.ERROR)
                self.xsd += att.view.schema_code

        if att.proof:
            if self.registerUUID(att.proof.ct_id, 'XdFileType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(att.proof.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdFile: " +
                           att.proof.label + " is published.", messages.ERROR)
                self.xsd += att.proof.schema_code

        if att.reason:
            if self.registerUUID(att.reason.ct_id, 'XdStringType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(att.reason.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that XdString: " +
                           att.reason.label + " is published.", messages.ERROR)
                self.xsd += att.reason.schema_code

        if att.committer:
            if self.registerUUID(att.committer.ct_id, 'PartyType'):
                # len 10 was arbitrarily chosen as an obviously incorrect code
                # length.
                if len(att.committer.schema_code) < 10:
                    msg = ("Something happened to your MC code. Check that Party: " +
                           att.committer.label + " is published.")
                    return(msg)
                self.xsd += att.committer.schema_code
                msg = self.processParty(att.committer)

        return(msg)

    def makeXdAdapter(self, ct_id, adapter_id, xd_name):
        """
        Create an Element adapter for a complexType when used in a Cluster.
        Requires the ct_id of the complexType and the pre-generated Element ID for that datatype.
        Returns the string.
        """
        adr_str = ''
        indent = 2
        padding = ('').rjust(indent)
        adapter_id = str(adapter_id)
        ct_id = str(ct_id)

        # Create the Adapter
        adr_str += padding.rjust(indent) + ("<xs:element name='ms-" + adapter_id +
                                            "' substitutionGroup='s3m:Items' type='s3m:mc-" + adapter_id + "'/>\n")
        adr_str += padding.rjust(indent) + ("<xs:complexType name='mc-" +
                                            adapter_id + "'> <!-- Adapter for: " + escape(xd_name) + " -->\n")
        adr_str += padding.rjust(indent + 2) + ("<xs:complexContent>\n")
        adr_str += padding.rjust(indent + 4) + \
            ("<xs:restriction base='s3m:XdAdapterType'>\n")
        adr_str += padding.rjust(indent + 6) + ("<xs:sequence>\n")
        adr_str += padding.rjust(indent + 8) + ("<xs:element  maxOccurs='unbounded' minOccurs='0' ref='s3m:ms-" +
                                                ct_id + "'/> <!-- Reference to: " + escape(xd_name) + " -->\n")
        adr_str += padding.rjust(indent + 6) + ("</xs:sequence>\n")
        adr_str += padding.rjust(indent + 4) + ("</xs:restriction>\n")
        adr_str += padding.rjust(indent + 2) + ("</xs:complexContent>\n")
        adr_str += padding.rjust(indent) + ("</xs:complexType>\n")

        return adr_str

    def processSubstitutionGroups(self):
        msg = ("Substitution Groups generated.", messages.SUCCESS)

        self.xsd += '\n<!-- Substitution Groups -->\n'

        for uuid in self.used_uuids:
            sg_names = []
            for n in range(0, len(self.used_uuids[uuid])):
                if self.used_uuids[uuid][n][1] is not None:
                    if 's3m:' + self.used_uuids[uuid][n][1] not in sg_names:
                        sg_names.append('s3m:' + self.used_uuids[uuid][n][1])
                        sg_str = 'substitutionGroup="' + " ".join(sg_names)
                        self.xsd += ('  <xs:element name="ms-' + str(uuid) +
                                     '" ' + sg_str + '" type="s3m:mc-' + str(uuid) + '"/>\n')
        return(msg)

    def pcmRDF(self):
        msg = ("PCM RDF was generated.", messages.SUCCESS)

        self.xsd += '\n<!-- RDF for contained Reusable Model Components -->\n'
        self.xsd += "  <xs:annotation>\n"
        self.xsd += "  <xs:appinfo>\n"

        for uuid in self.used_uuids:
            self.xsd += '      <rdf:Description rdf:about="dm-' + str(self.dm.ct_id) + '">\n'
            self.xsd += '        <s3m:containsRMC rdf:resource="mc-' + str(uuid) + '"/>\n'
            self.xsd += '      </rdf:Description>\n'

        self.xsd += "  </xs:appinfo>\n"
        self.xsd += "  </xs:annotation>\n"

        return(msg)

    def getXSD(self):
        """
        The method that intiates building the XML Schema.
        """
        msg = ("The schema was generated.", messages.SUCCESS)

        self.xsd += self.xsdHead
        self.xsd += self.rm
        self.xsd += self.xsdMetadata
        self.xsd += '<!-- Complex Type Definitions -->\n'

        self.xml += self.xmlHead
        # start building the DM and the XML instance
        msg = self.processDM()

        # create the substitution groups, add RDF for contained MCs and close the schema and instance
        if msg[1] == messages.SUCCESS:
            msg = self.processSubstitutionGroups()
            msg = self.pcmRDF()

        if msg[1] == messages.SUCCESS:
            self.xsd += self.xsdTail
            self.xml += self.xmlTail

        return(msg)


def generateDM(dm, request):
    """
    Called from the DMAdmin in admin.py.
    This function triggers building the objects used to defined the artifacts for output.
    """

    # Cleanup - Remove old files if this DM has been generated before. Set
    # Published as false.
    dm.html_file.delete()
    dm.xml_file.delete()
    dm.json_file.delete()
    dm.xsd_file.delete()
    dm.sha1_file.delete()
    dm.zip_file.delete()
    dm.published = False
    dm.save()

    # begin processing
    dmpkg = DMPkg(dm, request)
    msg = dmpkg.getXSD()

    # build the HTML form
    dmpkg = buildHTML(dmpkg)

    # set the umask so we can create files in the directory we create via
    # Apache/NGINX.
    prevumask = os.umask(0o000)

    # create a unique directory based on the DM Title
    lib_dir = DM_LIB
    fldr_title = ''.join([c for c in dm.title if c.isalnum() and ord(c) <= 127])
    dm_dir = lib_dir + "/" + fldr_title
    if os.path.exists(dm_dir):
        rmtree(dm_dir)

    os.makedirs(dm_dir, 0o777)

    if msg[1] == messages.SUCCESS:
        # write the files

        # open a schema file dm-(uuid).xsd
        f = ContentFile(dmpkg.xsd.encode("utf-8"))
        xsd = dm.xsd_file
        xsd.save('dm-' + str(dm.ct_id) + '.xsd', f, save=True)
        xsd.flush()
        dm.xsd_file.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) +
                     '.xsd', os.O_RDWR | os.O_CREAT)
        os.write(lf, dmpkg.xsd.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS,
                             "Wrote the DM schema file.")
        copy(lib_dir + '/dm-description.xsl', dm_dir + '/dm-description.xsl')

        # open an HTML file dm-(uuid).html
        f = ContentFile(dmpkg.html.encode("utf-8"))
        html = dm.html_file
        html.save('dm-' + str(dm.ct_id) + '.html', f, save=True)
        html.flush()
        dm.html_file.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) +
                     '.html', os.O_RDWR | os.O_CREAT)
        os.write(lf, dmpkg.html.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS,
                             "Wrote the HTML form file.")

        # open an instance file dm-(uuid).xml
        f = ContentFile(dmpkg.xml.encode("utf-8"))
        xml = dm.xml_file
        xml.save('dm-' + str(dm.ct_id) + '.xml', f, save=True)
        xml.flush()
        dm.xml_file.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) +
                     '.xml', os.O_RDWR | os.O_CREAT)
        os.write(lf, dmpkg.xml.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS,
                             "Wrote the XML Instance file.")

        """
         open and write a JSON instance file dm-(uuid).json
        """
        namespaces = {}
        for ns in NS.objects.all():
            namespaces[ns.uri.strip()] = ns.abbrev.strip()
        f = ContentFile(dmpkg.xml.encode("utf-8"))  # this is the XML instance before conversion
        xmldict = xmltodict.parse(f, process_namespaces=True, namespaces=namespaces)
        j = json.dumps(xmldict, indent=2)
        jfile = ContentFile(j)
        jsonfile = dm.json_file
        jsonfile.save('dm-' + str(dm.ct_id) + '.json', jfile)
        jsonfile.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.json', os.O_RDWR | os.O_CREAT)
        os.write(lf, j.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS, "Wrote the JSON Instance file.")

        """
        generate and write the SHA1 file
        """
        dmxsd = open(dm_dir + '/dm-' + str(dm.ct_id) + '.xsd', encoding="utf-8")
        dm_content = dmxsd.read()
        dmxsd.close()
        h = hashlib.sha1(dm_content.encode("utf-8")).hexdigest()
        f = ContentFile(h)
        sha1 = dm.sha1_file
        sha1.save('dm-' + str(dm.ct_id) + '.sha1', f)
        sha1.close()
        f.close()
        lf = os.open(dm_dir + '/dm-' + str(dm.ct_id) +
                     '.sha1', os.O_RDWR | os.O_CREAT)
        os.write(lf, h.encode("utf-8"))
        os.close(lf)
        messages.add_message(request, messages.SUCCESS,
                             "Wrote the SHA1 digital signature file.")

        """
        Generate the RDF from the semantics embeded in the XSD.
        """

        ns_dict = {'xs': 'http://www.w3.org/2001/XMLSchema',
                   'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                   'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                   'dct': 'http://purl.org/dc/terms/',
                   'owl': 'http://www.w3.org/2002/07/owl#',
                   'vc': 'http://www.w3.org/2007/XMLSchema-versioning',
                   's3m': 'https://www.s3model.com/ns/s3m/'}

        parser = etree.XMLParser(ns_clean=True, recover=True)
        about = etree.XPath("//xs:annotation/xs:appinfo/rdf:Description", namespaces=ns_dict)
        md = etree.XPath("//rdf:RDF/rdf:Description", namespaces=ns_dict)
        rdf_file = os.open(dm_dir + '/dm-' + str(dm.ct_id) + '.rdf', os.O_RDWR | os.O_CREAT)

        rdfstr = """<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n"""

        tree = etree.parse(ContentFile(dmpkg.xsd.encode("utf-8")), parser)
        root = tree.getroot()

        rdf = about(root)
        for m in md(root):
            rdfstr += '    '+etree.tostring(m).decode('utf-8')+'\n'

        for r in rdf:
            rdfstr += '    '+etree.tostring(r).decode('utf-8')+'\n'

        rdfstr += '</rdf:RDF>\n'
        os.write(rdf_file, rdfstr.encode("utf-8"))
        os.close(rdf_file)
        messages.add_message(request, messages.SUCCESS,
                             "Wrote the RDF for the DM.")

        """
        create ZIP of the directory and the JSON, html, xsd, xml, sha1 files and the R project
        """
        zf = zipfile.ZipFile(MEDIA_ROOT + '/dm-' + str(dm.ct_id) + '.zip', 'w')
        for dirname, subdirs, files in os.walk(dm_dir):
            for filename in files:
                zf.write(os.path.join(dirname, filename),
                         dirname.replace('../dmlib/', '') + '/' + filename)

        zf.close()
        messages.add_message(request, messages.SUCCESS,
                             "Created a ZIP of all the files.")

        os.umask(prevumask)  # reset the umask

        dm.published = True
        dm.save()

    return(msg)

