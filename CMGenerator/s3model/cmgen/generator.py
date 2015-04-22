#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import sys
import time
import codecs
from datetime import datetime
import hashlib
import zipfile
from shutil import copy
from uuid import uuid4
from collections import OrderedDict
from xml.sax.saxutils import escape
import json

import xmltodict
import shortuuid

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.files.base import ContentFile, File

from .exceptions import PublishingError, GenerationError

import ccdgen.models

from .ig import ccdinstance, dv_uri, dv_boolean, dv_codedstring, dv_count, dv_identifier, dv_interval, \
    dv_media, dv_ordinal, dv_parsable, dv_quantity, dv_ratio, dv_string, dv_temporal, \
    party, participation, attestation, cluster, audit

from .fg import fdv_uri, fdv_boolean, fdv_codedstring, fdv_count, fdv_identifier, fdv_interval, \
    fdv_media, fdv_ordinal, fdv_parsable, fdv_quantity, fdv_ratio, fdv_string, fdv_temporal, \
    fparticipation, fparty, fattestation, fcluster, faudit


"""
generator.py

The MLHIM2 Reference Model code to write CCD schemas.
Copyright 2014-2015, Timothy W. Cook, All Rights Reserved.

This code is accessed from CCD model class in model.py

"""
USED_CLUSTERS = []
USED_UUIDS = []
USED_ELEMENTS = []
REF_DICT = OrderedDict()
INSTR = """<?xml version="1.0" encoding="UTF-8"?>""" # Instance header string
FRMSTR = """<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n"""
n = time.localtime()
now = "%d-%d-%d" % (n.tm_year, n.tm_mon, n.tm_mday)

def use_uuid(ctid, elname, reset=False):
    global USED_UUIDS
    global REF_DICT

    if reset == True:
        USED_UUIDS = []
        REF_DICT = OrderedDict()


    added = False
    #if we haven't used the UUID yet, add it to the list and let the generator know to get the code
    if ctid not in USED_UUIDS:
        USED_UUIDS.append(ctid)
        added = True

    # we need to add each call to a dict so that we can build the referenced elements with substitution groups
    if ctid in list(REF_DICT.keys()):
        if elname != None and elname not in REF_DICT[ctid]:
            REF_DICT[ctid].append(elname)
    else:
        REF_DICT[ctid] = [elname,]

    return added

def getDvAdapter(ct_id, elem_id, dvname):
    """
    Create an Element adapter for a complexType when used in a Cluster.
    Requires the ct_id of the complexType and the pre-generated Element ID for that datatype.
    Returns the string.
    """
    elem_str = ''
    indent = 2
    padding = ('').rjust(indent)


    #Create the Element
    elem_str += padding.rjust(indent) + ("<xs:element name='el-"+elem_id+"' substitutionGroup='mlhim2:items' type='mlhim2:ct-"+elem_id+"'/>\n")
    elem_str += padding.rjust(indent) + ("<xs:complexType name='ct-"+elem_id+"'> <!-- Adapter for: "+escape(dvname)+" -->\n")
    elem_str += padding.rjust(indent+2) + ("<xs:complexContent>\n")
    elem_str += padding.rjust(indent+4) + ("<xs:restriction base='mlhim2:DvAdapterType'>\n")
    elem_str += padding.rjust(indent+6) + ("<xs:sequence>\n")
    elem_str += padding.rjust(indent+8) + ("<xs:element  maxOccurs='unbounded' minOccurs='0' ref='mlhim2:el-"+ct_id+"'/> <!-- Reference to: "+escape(dvname)+" -->\n")
    elem_str += padding.rjust(indent+6) + ("</xs:sequence>\n")
    elem_str += padding.rjust(indent+4) + ("</xs:restriction>\n")
    elem_str += padding.rjust(indent+2) + ("</xs:complexContent>\n")
    elem_str += padding.rjust(indent) + ("</xs:complexType>\n\n")

    return elem_str

def getAudit(aud):
    audit_str = aud.schema_code
    if aud.system_id:
        if use_uuid(aud.system_id.ct_id, 'system-id'):
            if len(aud.system_id.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvIDentifier: "+aud.system_id.data_name+" is published.")
            audit_str += aud.system_id.schema_code

    if aud.system_user:
        if use_uuid(aud.system_user.ct_id, 'system-user'):
            if len(aud.system_user.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that Party: "+aud.system_user.label+" is published.")
            audit_str += getParty(aud.system_user)

    if aud.location:
        if use_uuid(aud.location.ct_id, 'location'):
            if len(aud.location.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that Cluster: "+aud.location.cluster_subject+" is published.")
            audit_str += getCluster(aud.location, True)


    return audit_str

def getParty(party):
    party_str = party.schema_code

    if party.external_ref.all():
        for ref in party.external_ref.all():
            if use_uuid(ref.ct_id, 'external-ref'):
                if len(ref.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                    raise GenerationError("Something happened to your PCT code. Check that DvURI: "+ref.data_name+" is published.")
                party_str += ref.schema_code

    if party.details:
        if use_uuid(party.details.ct_id, 'details'):
            if len(party.details.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that Cluster: "+party.details.cluster_subject+" is published.")
            party_str += getCluster(party.details, True)

    return party_str

def getParticipation(part):
    part_str = part.schema_code

    if part.performer_p:
        if use_uuid(part.performer_p.ct_id, 'performer'):
            if len(part.performer_p.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that PartyIdentified: "+part.performer_p.label+" is published.")
            part_str += getParty(part.performer_p)

    if part.function:
        if use_uuid(part.function.ct_id, 'function'):
            if len(part.function.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+part.function.data_name+" is published.")
            part_str += part.function.schema_code
    elif part.simple_function:
        if use_uuid(part.simple_function.ct_id, 'function'):
            if len(part.simple_function.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvString: "+part.simple_function.data_name+" is published.")
            part_str += part.simple_function.schema_code

    if part.mode:
        if use_uuid(part.mode.ct_id, 'mode'):
            if len(part.mode.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+part.mode.data_name+" is published.")
            part_str += part.mode.schema_code
    elif part.simple_mode:
        if use_uuid(part.simple_mode.ct_id, 'mode'):
            if len(part.simple_mode.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvString: "+part.simple_mode.data_name+" is published.")
            part_str += part.simple_mode.schema_code


    return part_str

def getAttestation(att):
    att_str = att.schema_code

    if att.attested_view:
        if use_uuid(att.attested_view.ct_id, 'attested-view'):
            if len(att.attested_view.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvMedia: "+att.attested_view.data_name+" is published.")
            att_str += att.attested_view.schema_code

    if att.proof:
        if use_uuid(att.proof.ct_id, 'proof'):
            if len(att.proof.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvParsable: "+att.proof.data_name+" is published.")
            att_str += att.proof.schema_code

    if att.reason:
        if use_uuid(att.reason.ct_id, 'reason'):
            if len(att.reason.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+att.reason.data_name+" is published.")
            att_str += att.reason.schema_code
    elif att.reason:
        if use_uuid(att.simple_reason.ct_id, 'reason'):
            if len(att.simple_reason.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvString: "+att.simple_reason.data_name+" is published.")
            att_str += att.simple_reason.schema_code

    if att.committer_p:
        if use_uuid(att.committer_p.ct_id, 'committer'):
            if len(att.committer_p.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that PartyIdentified: "+att.committer_p.data_name+" is published.")
            att_str += getParty(att.committer_p)

    return att_str

def getCluster(cluster, reset=False):
    clu_str = cluster.schema_code
    global USED_CLUSTERS
    global USED_ELEMENTS

    #if reset:
        #USED_CLUSTERS = []
        #USED_ELEMENTS = []

    for clust in cluster.clusters.all():
        USED_CLUSTERS.append(clust.ct_id)
        if USED_CLUSTERS.count(clust.ct_id) > 100:
            raise GenerationError("I think the CCDGEN is in a loop because you have embedded a Cluster inside itself on some level. OR there are more than 100 embedded Clusters, which seems kind of ridiculous.")

        if use_uuid(clust.ct_id, 'items'):
            clu_str += getCluster(clust)

    for dv in cluster.dvboolean.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvBoolean: "+dv.data_name+" is published.")
            clu_str += dv.schema_code #get the Dv code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvuri.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvURI: "+dv.data_name+" is published.")
            clu_str += dv.schema_code #get the Dv code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvstring.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvString: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvcodedstring.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvidentifier.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvIndentifer: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvparsable.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvParsable: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvmedia.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvMedia: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvordinal.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvOrdinal: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
            if dv.reference_ranges.all():
                for rr in dv.reference_ranges.all():
                    if use_uuid(rr.ct_id, 'reference-ranges'):
                        if len(rr.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                            raise GenerationError("Something happened to your PCT code. Check that ReferenceRange: "+rr.data_name+" is published.")
                        clu_str += rr.schema_code
                        if use_uuid(rr.data_range.ct_id, 'data-range'):
                            if len(rr.data_range.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                                raise GenerationError("Something happened to your PCT code. Check that DvInterval: "+rr.data_range.data_name+" is published.")
                            clu_str += rr.data_range.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvcount.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvCount: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
            if dv.reference_ranges.all():
                for rr in dv.reference_ranges.all():
                    if use_uuid(rr.ct_id, 'reference-ranges'):
                        if len(rr.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                            raise GenerationError("Something happened to your PCT code. Check that ReferenceRange: "+rr.data_name+" is published.")
                        clu_str += rr.schema_code
                        if use_uuid(rr.data_range.ct_id, 'data-range'):
                            if len(rr.data_range.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                                raise GenerationError("Something happened to your PCT code. Check that DvInterval: "+rr.data_range.data_name+" is published.")
                            clu_str += rr.data_range.schema_code
            if dv.simple_units:
                if use_uuid(dv.simple_units.ct_id, 'DvCount-units'):
                    if len(dv.simple_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvString: "+dv.simple_units.data_name+" is published.")
                    clu_str += dv.simple_units.schema_code
            elif dv.coded_units:
                if use_uuid(dv.coded_units.ct_id, 'DvCount-units'):
                    if len(dv.coded_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+dv.coded_units.data_name+" is published.")
                    clu_str += dv.coded_units.schema_code
            else:
                raise GenerationError("Your DvCount is missing a DvCount-units value. This should have been a publishing error; <b>Contact the CCDGEN authors</b>.")
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)


    for dv in cluster.dvquantity.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvQuantity: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
            if dv.reference_ranges.all():
                for rr in dv.reference_ranges.all():
                    if use_uuid(rr.ct_id, 'reference-ranges'):
                        if len(rr.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                            raise GenerationError("Something happened to your PCT code. Check that ReferenceRange: "+rr.data_name+" is published.")
                        clu_str += rr.schema_code
                        if use_uuid(rr.data_range.ct_id, 'data-range'):
                            if len(rr.data_range.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                                raise GenerationError("Something happened to your PCT code. Check that DvInterval: "+rr.data_range.data_name+" is published.")
                            clu_str += rr.data_range.schema_code
            if dv.simple_units:
                if use_uuid(dv.simple_units.ct_id, 'DvQuantity-units'):
                    if len(dv.simple_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvString: "+dv.simple_units.data_name+" is published.")
                    clu_str += dv.simple_units.schema_code
            elif dv.coded_units:
                if use_uuid(dv.coded_units.ct_id, 'DvQuantity-units'):
                    if len(dv.coded_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+dv.coded_units.data_name+" is published.")
                    clu_str += dv.coded_units.schema_code
            else:
                raise GenerationError("Your DvQuanity is missing a DvQuantity-units value. This should have been a publishing error; <b>Contact the CCDGEN authors</b>.")
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)


    for dv in cluster.dvratio.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvRatio: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
            if dv.num_simple_units is not None:
                if use_uuid(dv.num_simple_units.ct_id, 'numerator-units'):
                    if len(dv.num_simple_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvString: "+dv.num_simple_units.data_name+" is published.")
                    clu_str += dv.num_simple_units.schema_code
            elif dv.num_coded_units is not None:
                if use_uuid(dv.num_coded_units.ct_id, 'numerator-units'):
                    if len(dv.num_coded_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+dv.num_coded_units.data_name+" is published.")
                    clu_str += dv.num_coded_units.schema_code
##            else:
##                raise GenerationError("Your DvRatio is missing a numerator-units value. This should have been a publishing error; <b>Contact the CCDGEN authors</b>.")

            if dv.den_simple_units is not None:
                if use_uuid(dv.den_simple_units.ct_id, 'denominator-units'):
                    if len(dv.den_simple_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvString: "+dv.den_simple_units.data_name+" is published.")
                    clu_str += dv.den_simple_units.schema_code
            elif dv.den_coded_units is not None:
                if use_uuid(dv.den_coded_units.ct_id, 'denominator-units'):
                    if len(dv.den_coded_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+dv.den_coded_units.data_name+" is published.")
                    clu_str += dv.den_coded_units.schema_code
##            else:
##                raise GenerationError("Your DvRatio is missing a denominator-units value. This should have been a publishing error; <b>Contact the CCDGEN authors</b>.")

            if dv.ratio_simple_units is not None:
                if use_uuid(dv.ratio_simple_units.ct_id, 'ratio-units'):
                    if len(dv.ratio_simple_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvString: "+dv.ratio_simple_units.data_name+" is published.")
                    clu_str += dv.ratio_simple_units.schema_code
            elif dv.ratio_coded_units is not None:
                if use_uuid(dv.ratio_coded_units.ct_id, 'ratio-units'):
                    if len(dv.ratio_coded_units.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                        raise GenerationError("Something happened to your PCT code. Check that DvCodedString: "+dv.ratio_coded_units.data_name+" is published.")
                    clu_str += dv.ratio_coded_units.schema_code
            else:
                pass # not mandatory


            if dv.reference_ranges.all():
                for rr in dv.reference_ranges.all():
                    if use_uuid(rr.ct_id, 'reference-ranges'):
                        if len(rr.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                            raise GenerationError("Something happened to your PCT code. Check that ReferenceRange: "+rr.data_name+" is published.")
                        clu_str += rr.schema_code
                        if use_uuid(rr.data_range.ct_id, 'data-range'):
                            if len(rr.data_range.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                                raise GenerationError("Something happened to your PCT code. Check that DvInterval: "+rr.data_range.data_name+" is published.")
                            clu_str += rr.data_range.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    for dv in cluster.dvtemporal.all():
        if use_uuid(dv.ct_id, 'DvAdapter-dv'):
            if len(dv.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvTemporal: "+dv.data_name+" is published.")
            clu_str += dv.schema_code
            if dv.reference_ranges.all():
                for rr in dv.reference_ranges.all():
                    if use_uuid(rr.ct_id, 'reference-ranges'):
                        if len(rr.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                            raise GenerationError("Something happened to your PCT code. Check that ReferenceRange: "+rr.data_name+" is published.")
                        clu_str += rr.schema_code
                        if use_uuid(rr.data_range.ct_id, 'data-range'):
                            if len(rr.data_range.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                                raise GenerationError("Something happened to your PCT code. Check that DvInterval: "+rr.data_range.data_name+" is published.")
                            clu_str += rr.data_range.schema_code
        if not (dv.element_ctid in USED_ELEMENTS):
            clu_str += getDvAdapter(dv.ct_id,dv.element_ctid, dv.data_name) #create the DvAdapterType code
            USED_ELEMENTS.append(dv.element_ctid)

    return clu_str

def getEntry(entry):

    global INSTR     # XML instance string
    global FRMSTR    # HTML Form string

    indent = '  '

    if len(entry.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
        raise GenerationError("Something happened to your PCT code. Check that Entry: "+entry.entry_name+" is published.")
    entry_str = entry.schema_code
    FRMSTR += indent + """<div class='entry collapsed'><br /> <span style="text-align: center; font-weight: bold;"> Entry: """+entry.entry_name+"""</span><br />\n\n<em>The Entry meta-data is not normally user facing. It is shown here for developers. <a href='#entry-data'>Entry data begins here</a>.</em>\n"""
    FRMSTR += indent + "<form action='' method='' name='"+entry.entry_name+"' target='' >\n"
    INSTR += indent + """<mlhim2:el-"""+entry.ct_id+"""> <!-- Entry -->\n"""
    FRMSTR += indent + " <div class='devonly collapsed'>\n"
    #FRMSTR += indent + " <div class='content'>\n"
    #entry-links
    FRMSTR += indent + ' entry-links: <br />\n'
    INSTR += indent + '<!-- entry-links -->\n'
    if entry.entry_links.all():
        for link in entry.entry_links.all():
            if use_uuid(link.ct_id,'entry-links'):
                if len(link.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                    raise GenerationError("Something happened to your PCT code. Check that DvURI: "+link.data_name+" is published.")
                entry_str += link.schema_code
            INSTR += indent + dv_uri(link, indent)
            FRMSTR += indent + fdv_uri(link, indent)
    else:
        FRMSTR += indent + "<b>No entry-links defined.</b><br />\n"

    #entry-audit
    FRMSTR += indent + ' entry-audit: <br />\n'
    INSTR += indent + '<!-- entry-audit -->\n'
    if entry.audit:
        if use_uuid(entry.audit.ct_id, 'entry-audit'):
            entry_str += getAudit(entry.audit)
        INSTR += '  ' + audit(entry.audit, indent)
        FRMSTR += indent + '  ' + faudit(entry.audit, indent)
    else:
        FRMSTR += indent + "<b>No entry-audit defined.</b><br />\n"

    INSTR += indent + '<language>'+entry.language+'</language>\n'
    INSTR += indent + '<encoding>'+entry.encoding+'</encoding>\n'
    FRMSTR += indent + '<br />language: &nbsp;&nbsp;<b>'+entry.language+'</b><br />\n'
    FRMSTR += indent + 'encoding: &nbsp;&nbsp;<b>'+entry.encoding+'</b><br /><br />\n'

    #entry-subject
    FRMSTR += indent + ' entry-subject: <br />\n'
    INSTR += indent + '<!-- entry-subject -->\n'
    if entry.entry_subject:
        if use_uuid(entry.entry_subject.ct_id, 'entry-subject'):
            entry_str += getParty(entry.entry_subject)
        INSTR += '  ' + party(entry.entry_subject, indent)
        FRMSTR += indent + '  ' + fparty(entry.entry_subject, indent)

    #entry-provider
    FRMSTR += indent + ' entry-provider: <br />\n'
    INSTR += indent + '<!-- entry-provider -->\n'
    if entry.entry_provider_p:
        if use_uuid(entry.entry_provider_p.ct_id, 'entry-provider'):
            entry_str += getParty(entry.entry_provider_p)
        INSTR += '  ' + party(entry.entry_provider_p, indent)
        FRMSTR += indent + '  ' + fparty(entry.entry_provider_p, indent)

    #other-participations
    FRMSTR += indent + ' other-participations: <br />\n'
    INSTR += indent + '<!-- other-participations -->\n'
    if entry.other_participations.all():
        for op in entry.other_participations.all():
            if use_uuid(op.ct_id, 'other-participations'):
                entry_str += getParticipation(op)
            INSTR += '  ' + participation(op, indent)
            FRMSTR += indent + '  ' + fparticipation(op, indent)
    else:
        FRMSTR += indent + "<b>No other-paticipations defined.</b><br />\n"

    #protocol-id
    FRMSTR += indent + ' protocol-id: <br />\n'
    INSTR += indent + '<!-- protocol-id -->\n'
    if entry.protocol_id:
        if use_uuid(entry.protocol_id.ct_id, 'protocol-id'):
            if len(entry.protocol_id.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvIdentifier: "+entry.protocol_id.data_name+" is published.")
            entry_str += entry.protocol_id.schema_code
        INSTR += '  ' + dv_identifier(entry.protocol_id, indent)
        FRMSTR += '  ' + fdv_identifier(entry.protocol_id, indent)
    else:
        FRMSTR += indent + "<b>No protocol-id defined.</b><br />\n"

    INSTR += indent + '<current-state>default</current-state>\n'
    FRMSTR += indent + '<br />current-state: &nbsp;&nbsp;<b>default</b><br />\n'

    #workflow-id
    FRMSTR += indent + ' workflow-id: <br />\n'
    INSTR += indent + '<!-- workflow-id -->\n'
    if entry.workflow_id:
        if use_uuid(entry.workflow_id.ct_id, 'workflow-id'):
            if len(entry.workflow_id.schema_code) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
                raise GenerationError("Something happened to your PCT code. Check that DvIdentifier: "+entry.workflow_id.data_name+" is published.")
            entry_str += entry.workflow_id.schema_code
        INSTR += '  ' + dv_uri(entry.workflow_id, indent)
        FRMSTR += indent + '  ' + fdv_uri(entry.workflow_id, indent)
    else:
        FRMSTR += indent + "<b>No workflow-id defined.</b><br />\n"

    #attestation
    FRMSTR += indent + ' attestation: <br />\n'
    INSTR += indent + '<!-- attestation -->\n'
    if entry.attestation:
        if use_uuid(entry.attestation.ct_id, 'attestation'):
            entry_str += getAttestation(entry.attestation)
        INSTR += '  ' + attestation(entry.attestation, indent)
        FRMSTR += indent + '  ' + fattestation(entry.attestation, indent)
    elif not entry.attestation:
        FRMSTR += indent + "<b>No attestation defined.</b><br />\n"

    FRMSTR += "\n</div> <!-- closes the devonly section -->\n"
    FRMSTR += """\n<div class='entry-data collapsed'>\n"""
    FRMSTR += "<a name='entry-data' id='entry-data'>Entry data:</a><br />\n"

    #entry-data
    FRMSTR += indent + ' entry-data: <br />\n'
    INSTR += indent + '<!-- entry-data -->\n'
    if entry.entry_data:
        if use_uuid(entry.entry_data.ct_id, 'entry-data'):
            entry_str += getCluster(entry.entry_data, True)
        INSTR += '  ' + cluster(entry.entry_data, indent)
        FRMSTR += indent + '  ' + fcluster(entry.entry_data, indent)

    FRMSTR += indent + '</div></form>\n</div>\n'
    #FRMSTR += "\n<button type='button' class='btn btn-danger hidebutton'>Close</button>\n</div>\n</div><br />\n</div>\n"
    #FRMSTR += "\n</div>\n"

    FRMSTR += indent + "<div><span class='ccdtitle' style='background-color: lightgreen;'>Created using the CCD-Gen!</span><span style='float: right; font-size: 8px;'>form design contributions by <a href='https://www.google.com/+MichalZubkowiczMZ'>Michal Zubkowicz</a></span><br />\n"
    FRMSTR += indent + "<span class='ccdid'>"+datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')+"</span><br /></div>\n"

    INSTR += indent + """</mlhim2:el-"""+entry.ct_id+""">\n"""

    return entry_str

def generateCCD(self):
    """
    Called from the CCD model
    This is where the string is built to write the schema file and the instance example.
    """
    global INSTR
    global FRMSTR
    global USED_ELEMENTS
    USED_ELEMENTS = []

    INSTR = """<?xml version="1.0" encoding="UTF-8"?>""" #reset the global between executions
    FRMSTR = """<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n"""

    if not self.published:
        raise GenerationError("You must first Publish the CCD before generating the code.")
    elif self.xsd_file:
        raise GenerationError("CCD: "+self.title+" was previously generated. You must unpublish it and publish a new CCD.")

    ccd_str = self.schema_code

    if len(ccd_str) < 10: # len 10 was arbitrarily chosen as an obviously incorrect code length.
        raise GenerationError("Something happened to your PCT code. Check that CCD: "+self.title+" is published.")

    #get the entry information and start the tree.
    if self.admin_definition:
        entry = self.admin_definition
    elif self.care_definition:
        entry = self.care_definition
    elif self.demog_definition:
        entry = self.demog_definition
    else:
        raise GenerationError("You do not have any definition for your CCD.")

    INSTR += ccdinstance('ccd-'+self.ct_id)

    FRMSTR += "<title>"+self.title.strip()+"</title>\n"
    FRMSTR += """<meta name="description" content="HTML Form Template for ccd-"""+self.ct_id+""""/>\n"""
    FRMSTR += """<meta name="keywords" content="HTML,CSS,XML, MLHIM, CCD, PcT"/>\n"""
    FRMSTR += """<meta name="author" content="CCD-Gen http://www.ccdgen.com"/>\n"""
    FRMSTR += """<meta charset="UTF-8"/>\n"""
    FRMSTR += """<meta id='ccd-"""+self.ct_id+"""'/>\n"""
    FRMSTR += """<meta lang='"""+self.dc_language+"""'/>\n"""
    FRMSTR += """<link href="http://www.mlhim.org/css/mlhim246.css" title="MLHIM 2.4.6 " type="text/css" rel="stylesheet" />\n"""
    FRMSTR += """<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">\n"""
    FRMSTR += """<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">\n"""

    FRMSTR += """<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>\n"""
    FRMSTR += """<script type="text/javascript">"""
    FRMSTR += """  if (typeof jQuery == 'undefined') {"""
    FRMSTR += """  document.write(unescape("%3Cscript src='/js/jquery-1.10.2.min.js' type='text/javascript'%3E%3C/script%3E"));"""
    FRMSTR += """}"""
    FRMSTR += """</script>"""

    # dev On/Off scripts
    FRMSTR += """<script type="text/javascript" >\n"""
    FRMSTR += """  $(document).ready(function() {\n"""
    FRMSTR += """  $('#devon').click(function() {\n"""
    FRMSTR += """  $('.devonly').css('display','inline');\n"""
    FRMSTR += """});\n"""
    FRMSTR += """});\n"""
    FRMSTR += """</script>\n"""
    FRMSTR += """<script type="text/javascript" >\n"""
    FRMSTR += """  $(document).ready(function() {\n"""
    FRMSTR += """  $('#devoff').click(function() {\n"""
    FRMSTR += """  $('.devonly').css('display', 'none');\n"""
    FRMSTR += """});\n"""
    FRMSTR += """});\n"""
    FRMSTR += """</script>\n"""
    # collapse/uncollapse script
    FRMSTR += """<script type="text/javascript">\n"""
    FRMSTR += """$(document).ready(function () {\n"""
    FRMSTR += """    $('.collapsed').on('click', function (e) {\n"""
    FRMSTR += """        $(this).removeClass('collapsed');\n"""
    FRMSTR += """        $(this).addClass('uncollapsed');\n"""
    FRMSTR += """        $(this).children('.content').show();\n"""
    FRMSTR += """        e.preventDefault();\n"""
    FRMSTR += """    });\n"""
    FRMSTR += """    $('.hidebutton').on('click', function (e) {\n"""
    FRMSTR += """        $(this).parent().hide();\n"""
    FRMSTR += """        $(this).parent().parent().removeClass('uncollapsed');\n"""
    FRMSTR += """        $(this).parent().parent().addClass('collapsed');\n"""
    FRMSTR += """        e.stopPropagation();\n"""
    FRMSTR += """        e.preventDefault();\n"""
    FRMSTR += """        });\n"""
    FRMSTR += """    });\n"""
    FRMSTR += """</script>\n"""
    FRMSTR += "</head>\n<body>\n"
    FRMSTR += "<span class='ccdtitle'>"+self.title+"</span><br />\n"
    FRMSTR += "<span class='ccdid'>ccd-"+self.ct_id+"</span><br />\n"

    FRMSTR += """<div style="text-align: center; font-weight: bold; font-size: 14px;">Developer View: <a href="#" id='devon' class="devon">On</a>   \n"""
    FRMSTR += """<a href="#" id='devoff' class="devoff">Off</a> &nbsp; &nbsp; &nbsp;<a href='http://mlhim.org/rm246_html' target='RM_246'>(Reference model details index)</a><br /><span style='color: red;  font-size: 12px;'>(click on the section titles below to expand the content)</span></div> <br />\n"""

    FRMSTR += "<div class='ccd collapsed'>\n<div class='devonly collapsed'>\n"
    FRMSTR += self.doc_code # previously saved meta-data documentation

    # reset - used uuid and ref_dict
    if use_uuid(entry.ct_id, 'definition', True):
        ccd_str += getEntry(entry)                            #This is the 'dive' into the CCD creation


    # create reference elements with substitution groups at the bottom of the CCD
    for r in list(REF_DICT.keys()):
        if len(REF_DICT[r]) > 1 or REF_DICT[r][0] != None:
            sg_str = "substitutionGroup='"
            if REF_DICT[r][0] != None:
                for sg in REF_DICT[r]:
                    sg_str += 'mlhim2:' + sg + " "
                ccd_str += ("  <xs:element name='el-"+r+"' "+sg_str.strip()+"' type='mlhim2:ct-"+r+"'/>\n")


    #close the schema
    ccd_str += "\n</xs:schema>\n"

    # close the instance
    INSTR += "</mlhim2:ccd-"+self.ct_id+">\n"

    # close the form
    FRMSTR += "</div>\n</body>\n</html>"


    """
    The file writing to the library begins here.
    """
    # set the umask so we can create files in the directory we create via Apache.
    prevumask = os.umask(0o000)

    #create a unique directory based on the CCD ID
    CWD = os.getcwd()

    if CWD == '/home/ubuntu/ccdgen':                      # Live site
        lib_dir = "/home/ubuntu/ccdgen/ccdlib" #needed because on the production server we use it to force a disk write because apache/django isn't writing it.
    else:                               # development
        lib_dir =  "ccdlib"

    ccd_dir = lib_dir+"/CCD_"+ self.ct_id

    if not os.path.exists(ccd_dir): #in production it shouldn't ever exist.
        os.makedirs(ccd_dir,0o777)

    #open and write an html form file ccd-(uuid).html
    f = ContentFile(FRMSTR.encode("utf-8"))
    html = self.html_file
    html.save('ccd-'+self.ct_id+'.html', f)
    html.close()
    lf = os.open(ccd_dir+'/ccd-'+ self.ct_id+'.html', os.O_RDWR|os.O_CREAT )
    os.write(lf,FRMSTR.encode("utf-8"))
    os.close(lf)

    #open and write an XML instance file ccd-(uuid).xml
    f = ContentFile(INSTR.encode("utf-8"))
    xml = self.xml_file
    xml.save('ccd-'+self.ct_id+'.xml', f)
    xml.close()
    f.close()
    lf = os.open(ccd_dir+'/ccd-'+ self.ct_id+'.xml', os.O_RDWR|os.O_CREAT )
    os.write(lf,INSTR.encode("utf-8"))
    os.close(lf)

    #open and write a JSON instance file ccd-(uuid).json
    #f = ContentFile(INSTR.encode("utf-8")) #this is the XML instance before conversion
    #xmldict = xmltodict.parse(f)
    #j = json.dumps(xmldict, indent=2)
    #jfile = ContentFile(j)
    #jsonfile = self.json_file


    #jsonfile.save('ccd-'+self.ct_id+'.json', jfile)
    #jsonfile.close()
    #if lib_dir:
        #lf = os.open(ccd_dir+'/ccd-'+ self.ct_id+'.json', os.O_RDWR|os.O_CREAT )
        #os.write(lf,j.encode("utf-8"))
        #os.close(lf)


    #open a schema file ccd-(uuid).xsd

    f = ContentFile(ccd_str.encode("utf-8"))
    xsd = self.xsd_file
    xsd.save('ccd-'+self.ct_id+'.xsd', f, save=True)
    xsd.flush()
    self.xsd_file.close()
    f.close()
    lf = os.open(ccd_dir+'/ccd-'+ self.ct_id+'.xsd', os.O_RDWR|os.O_CREAT )
    os.write(lf,ccd_str.encode("utf-8"))
    os.close(lf)

    #generate and write the SHA1 file
    ccd = open(ccd_dir+'/ccd-'+self.ct_id+'.xsd', encoding="utf-8")
    ccd_content = ccd.read()
    ccd.close()
    h = hashlib.sha1(ccd_content.encode("utf-8")).hexdigest()
    f = ContentFile(h)
    sha1 = self.sha1_file
    sha1.save('ccd-'+self.ct_id+'.sha1', f)
    sha1.close()
    f.close()
    lf = os.open(ccd_dir+'/ccd-'+ self.ct_id+'.sha1', os.O_RDWR|os.O_CREAT )
    os.write(lf,h.encode("utf-8"))
    os.close(lf)

    # copy the XSLT file from the ccdlib parent directory into the ccd_dir
    copy(lib_dir+'/ccd-description.xsl',ccd_dir+'/ccd-description.xsl')



    """
    Create a subdirectory for the R project using the following string:
    'ccd': A prefix to help identifiy the module if it is included in the CRAN
    ccd.title: Collapse all white space and remove any non-alphanum characters
    uuid segment: take the last segement from the CCD UUID
    """
    # setup the project name
    r_proj = 'ccd'
    r_proj += ''.join([c for c in self.title if c.isalnum() and ord(c) <= 127])
    r_proj += self.ct_id.split('-')[-1]

    r_projdir = ccd_dir + '/' + r_proj
    # create the project directory
    os.makedirs(r_projdir,0o777)
    #create the required sub dirs
    os.makedirs(r_projdir+'/R',0o777)
    os.makedirs(r_projdir+'/man',0o777)
    os.makedirs(r_projdir+'/inst/examples',0o777)


    #use the list of PcT IDs used to can get the R code and data_name.
    exports = []
    for n in range(0, len(USED_UUIDS)):
        rinfo = None
        rinfo = ccdgen.models.get_rcode(USED_UUIDS[n])
        if rinfo:
            r_name = ''.join(e for e in rinfo[0] if e.isalnum() and ord(e) <= 127 )  # replace all special characters.

            r_filename = r_name + '.R'

            r_code = rinfo[1]
            exports.append('get'+r_name) # for writing to the NAMESPACE file

            #create the R code file
            rf = open(r_projdir+'/R/'+r_filename, 'wb')
            rf.write(r_code.encode("utf-8"))
            rf.close()

    # write the metadata.R file.
    rf = open(r_projdir+'/R/metadata.R', 'wb')
    rf.write(gen_metadataR(self).encode("utf-8"))
    rf.close()

    #create the required NAMESPACE and DESCRIPTION files
    r_nsfile = open(r_projdir+'/NAMESPACE', 'w')
    for n in range(0, len(exports)):
        r_nsfile.write('export('+exports[n]+')\n')
    r_nsfile.close()

    r_descfile = open(r_projdir+'/DESCRIPTION', 'wb')
    r_descfile.write(('Package: '+ r_proj+'\n').encode("utf-8"))
    r_descfile.write(('Type: Package'+'\n').encode("utf-8"))
    r_descfile.write(('Title: '+r_proj+'\n').encode("utf-8"))
    r_descfile.write('Version: 1.0\n'.encode("utf-8"))
    r_descfile.write(('Date: '+self.pub_date.strftime("%Y-%m-%d")+'\n').encode("utf-8"))
    r_descfile.write('Author: Timothy W. Cook <tim@mlhim.org>\n'.encode("utf-8"))
    r_descfile.write('Maintainer: Timothy W. Cook <tim@mlhim.org>\n'.encode("utf-8"))
    r_descfile.write(('Description: Creates a data frame from instances of the MLHIM CCD for:\n  '+self.title +'\n  The CCD ID is: '+self.ct_id+'\n  '+self.description+'\n').encode("utf-8"))
    r_descfile.write('License: Apache License 2.0\n'.encode("utf-8"))
    r_descfile.write('Depends: \n'.encode("utf-8"))
    r_descfile.write('  XML\n'.encode("utf-8"))
    r_descfile.close()

    #put the sample XML file in the R project as an example.
    xmlfile = open(ccd_dir+'/ccd-'+self.ct_id+'.xml', 'r', encoding="utf-8")
    xml = xmlfile.read()
    xmlfile.close
    xmlfile = open(r_projdir+'/inst/examples/example01.xml', 'w', encoding="utf-8")
    xmlfile.write(xml)
    xmlfile.close
    xmlfile = open(r_projdir+'/inst/examples/example02.xml', 'w', encoding="utf-8")
    xmlfile.write(xml)
    xmlfile.close

    #create a project file for RStudio
    r_studiofile = open(r_projdir+'/'+r_proj+'.Rproj', 'w', encoding="utf-8")
    r_studiofile.write('Version: 1.0\n')
    r_studiofile.write('\n')
    r_studiofile.write('RestoreWorkspace: Default\n')
    r_studiofile.write('SaveWorkspace: Default\n')
    r_studiofile.write('AlwaysSaveHistory: Default\n')
    r_studiofile.write('\n')
    r_studiofile.write('EnableCodeIndexing: Yes\n')
    r_studiofile.write('UseSpacesForTab: Yes\n')
    r_studiofile.write('NumSpacesForTab: 2\n')
    r_studiofile.write('Encoding: UTF-8\n')
    r_studiofile.write('\n')
    r_studiofile.write('RnwWeave: Sweave\n')
    r_studiofile.write('LaTeX: pdfLaTeX\n')
    r_studiofile.write('\n')
    r_studiofile.write('BuildType: Package\n')
    r_studiofile.write('PackageInstallArgs: --no-multiarch --with-keep.source\n')
    r_studiofile.write('PackageRoxygenize: rd\n')
    r_studiofile.write('\n')
    r_studiofile.close()



    #create ZIP of the directory and the html, xsd, xml, sha1 files and the R project
    if CWD == '/home/ubuntu/ccdgen':
        zf = zipfile.ZipFile('/home/ubuntu/ccdgen/ccdlib/ccd-'+self.ct_id+'.zip','w')
    else:
        zf = zipfile.ZipFile('ccdlib/ccd-'+self.ct_id+'.zip','w')
    for dirname, subdirs, files in os.walk(ccd_dir):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))

    zf.close()

    newumask = os.umask(prevumask)  #reset the umask

    return None

def gen_metadataR(self):
    """
    Create and return a string to build an R metadata file.
    """
    rstr = '' #The string to write
    rstr += "# Copyright 2014, Timothy W. Cook <tim@mlhim.org>\n"
    rstr += "# metadata.R for ccd-"+self.ct_id+".xsd\n"
    rstr += "# Licensed under the Apache License, Version 2.0 (the 'License');\n"
    rstr += "# you may not use this file except in compliance with the License.\n"
    rstr += "# You may obtain a copy of the License at\n"
    rstr += "# http://www.apache.org/licenses/LICENSE-2.0\n"
    rstr += "\n"
    rstr += "# Unless required by applicable law or agreed to in writing, software\n"
    rstr += "# distributed under the License is distributed on an 'AS IS' BASIS,\n"
    rstr += "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
    rstr += "# See the License for the specific language governing permissions and\n"
    rstr += "# limitations under the License.\n"
    rstr += "#' @title getMetadata\n"
    rstr += "#'\n"
    rstr += "#' The Concept Constraint Definition (CCD) Metadata\n"
    rstr += "#' @export\n"
    rstr += "getMetadata <- data.frame(\n"
    rstr += "  dc_title='"+self.title.strip()+"',\n"
    rstr += "  dc_creator='"+self.creator_name+" <"+self.creator_email+">',\n"
    rstr += "  dc_contributors='None',\n"
    rstr += "  dc_subject='"+self.subject+"',\n"
    rstr += "  dc_source='"+self.source+"',\n"
    rstr += "  dc_relation='"+self.relation+"',\n"
    rstr += "  dc_coverage='"+self.coverage+"',\n"
    rstr += "  dc_type='MLHIM Concept Constraint Definition (CCD)',\n"
    rstr += "  dc_identifier='ccd-"+self.ct_id+"',\n"
    rstr += "  dc_description='"+self.description+"',\n"
    rstr += "  dc_publisher='"+self.publisher+"',\n"
    pdstr = self.pub_date.strftime("%Y-%m-%d %H:%M%S")
    rstr += "  dc_date=as.POSIXct(strptime('"+pdstr+"', '%Y-%m-%d %HH:%MM%SS')),\n"
    rstr += "  dc_format='text/xml',\n"
    rstr += "  dc_language='en-us',\n"
    rstr += "  stringsAsFactors=FALSE)\n"
    rstr += "  \n"

    rstr += "nsDEF <- function(){\n"
    rstr += "  return()  \n"
    rstr += "} \n"
    rstr += "\n"
    rstr += "ccduri <- function(){\n"
    rstr += "    return('http://www.ccdgen.com/ccdlib/ccd-"+self.ct_id+".xsd')\n"
    rstr += "}\n"
    rstr += "\n"

    return(rstr)
