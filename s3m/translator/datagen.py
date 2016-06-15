# generate XML data files
import os
import csv
import re
from shutil import copy, rmtree
from xml.sax.saxutils import escape

from django.shortcuts import get_object_or_404

from s3m.settings import MEDIA_ROOT
from dmgen.models import NS
from .models import Record

def party(pi, indent):
    indent += '  '
    elstr = indent + "  <label>" + escape(pi.label.strip()) + "</label>\n"
    elstr += indent + "  <party-name>A. Sample Name</party-name>\n"
    if pi.external_ref:
        for ref in pi.external_ref.all():
            elstr += indent + "<party-ref>\n"
            elstr += Xd_link(ref, indent, False)
            elstr += indent + "</party-ref>\n"

    if pi.details:
        elstr += indent + "<party-details>\n"
        elstr += cluster(pi.details, indent, False)
        elstr += indent + "</party-details>\n"

    return elstr


def Xd_temporal(Xd, indent):

    indent += '  '
    elstr = indent + """<s3m:ms-""" + str(Xd.ct_id) + """>\n"""
    elstr += indent + """  <label>""" + escape(Xd.label.strip()) + """</label>\n"""

    # set the data value here
    value = '1980'

    if Xd.allow_date:
        elstr += indent + """  <xdtemporal-date>""" + value +  """</xdtemporal-date>\n"""
    if Xd.allow_time:
        elstr += indent + """  <xdtemporal-time>""" + value + """</xdtemporal-time>\n"""
    if Xd.allow_datetime:
        elstr += indent + """  <xdtemporal-datetime>""" + value + """</xdtemporal-datetime>\n"""
    if Xd.allow_datetimestamp:
        elstr += indent + """  <xdtemporal-datetime-stamp>""" + value + """</xdtemporal-datetime-stamp>\n"""
    if Xd.allow_day:
        elstr += indent + """  <xdtemporal-day>""" + value + """</xdtemporal-day>\n"""
    if Xd.allow_month:
        elstr += indent + """  <xdtemporal-month>""" + value + """</xdtemporal-month>\n"""
    if Xd.allow_year:
        elstr += indent + """  <xdtemporal-year>""" + value + """</xdtemporal-year>\n"""
    if Xd.allow_year_month:
        elstr += indent + """  <xdtemporal-year-month>""" + value + """</xdtemporal-year-month>\n"""
    if Xd.allow_month_day:
        elstr += indent + """  <xdtemporal-month-day>--""" + value + """</xdtemporal-month-day>\n"""
    if Xd.allow_duration:
        elstr += indent + """  <xdtemporal-duration>""" + value + """</xdtemporal-duration>\n"""
    if Xd.allow_ymduration:
        elstr += indent + """  <xdtemporal-ymduration>""" + value + """</xdtemporal-ymduration>\n"""
    if Xd.allow_dtduration:
        elstr += indent + """  <xdtemporal-dtduration>""" + value + """</xdtemporal-dtduration>\n"""
    elstr += indent + """</s3m:ms-""" + str(Xd.ct_id) + """>\n"""

    return elstr

def cluster(clu, records, csvdata, indent):
    xmlstr = ''
    xmlstr += indent + """<s3m:ms-""" + str(clu.ct_id) + """>\n"""
    xmlstr += indent + """  <label>""" + escape(clu.label.strip()) + """</label>\n"""

    if clu.xdstring:
        for Xd in clu.xdstring.all():
            rec = records.get(label=Xd.label)
            value = csvdata[rec.header.strip()]
            xmlstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            xmlstr += indent + """    <s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """      <label>""" + escape(Xd.label.strip()) + """</label>\n"""
            xmlstr += indent + """      <xdstring-value>""" + value + """</xdstring-value>\n"""
            xmlstr += indent + """      <xdstring-language>""" + Xd.lang + """</xdstring-language>\n"""
            xmlstr += indent + """    </s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdcount:
        for Xd in clu.xdcount.all():
            rec = records.get(label=Xd.label)
            value = re.sub("[^0123456789\.]","",csvdata[rec.header.strip()])
            unit = Xd.units.enums.splitlines()[0].strip()
            xmlstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            xmlstr += indent + """  <s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """    <label>""" + escape(Xd.label.strip()) + """</label>\n"""
            xmlstr += indent + """    <magnitude-status>equal</magnitude-status>\n"""
            xmlstr += indent + """    <error>0</error>\n"""
            xmlstr += indent + """    <accuracy>0</accuracy>\n"""
            xmlstr += indent + """    <xdcount-value>""" + value + """</xdcount-value>\n"""
            xmlstr += indent + """    <xdcount-units>\n"""
            xmlstr += indent + """      <label>""" + escape(Xd.units.label.strip()) + """</label>\n"""
            xmlstr += indent + """      <xdstring-value>""" + unit + """</xdstring-value>\n"""
            xmlstr += indent + """    </xdcount-units>\n"""
            xmlstr += indent + """  </s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdquantity:
        for Xd in clu.xdquantity.all():
            rec = records.get(label=Xd.label)
            value = re.sub("[^0123456789\.]","",csvdata[rec.header.strip()])
            unit = Xd.units.enums.splitlines()[0].strip()
            xmlstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            xmlstr += indent + """  <s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """    <label>""" + escape(Xd.label.strip()) + """</label>\n"""
            xmlstr += indent + """    <magnitude-status>equal</magnitude-status>\n"""
            xmlstr += indent + """    <error>0</error>\n"""
            xmlstr += indent + """    <accuracy>0</accuracy>\n"""
            xmlstr += indent + """    <xdquantity-value>""" + value + """</xdquantity-value>\n"""
            xmlstr += indent + """    <xdquantity-units>\n"""
            xmlstr += indent + """      <label>""" + escape(Xd.units.label.strip()) + """</label>\n"""
            xmlstr += indent + """      <xdstring-value>""" + unit + """</xdstring-value>\n"""
            xmlstr += indent + """    </xdquantity-units>\n"""
            xmlstr += indent + """  </s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    if clu.xdtemporal:
        for Xd in clu.xdtemporal.all():
            rec = records.get(label=Xd.label)
            value = csvdata[rec.header.strip()]
            indent += '  '
            xmlstr += indent + """  <s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""
            xmlstr += indent + """<s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """  <label>""" + escape(Xd.label.strip()) + """</label>\n"""
            if Xd.allow_date:
                xmlstr += indent + """  <xdtemporal-date>""" + value +  """</xdtemporal-date>\n"""
            if Xd.allow_time:
                xmlstr += indent + """  <xdtemporal-time>""" + value + """</xdtemporal-time>\n"""
            if Xd.allow_datetime:
                xmlstr += indent + """  <xdtemporal-datetime>""" + value + """</xdtemporal-datetime>\n"""
            if Xd.allow_datetimestamp:
                xmlstr += indent + """  <xdtemporal-datetime-stamp>""" + value + """</xdtemporal-datetime-stamp>\n"""
            if Xd.allow_day:
                xmlstr += indent + """  <xdtemporal-day>""" + value + """</xdtemporal-day>\n"""
            if Xd.allow_month:
                xmlstr += indent + """  <xdtemporal-month>""" + value + """</xdtemporal-month>\n"""
            if Xd.allow_year:
                xmlstr += indent + """  <xdtemporal-year>""" + value + """</xdtemporal-year>\n"""
            if Xd.allow_year_month:
                xmlstr += indent + """  <xdtemporal-year-month>""" + value + """</xdtemporal-year-month>\n"""
            if Xd.allow_month_day:
                xmlstr += indent + """  <xdtemporal-month-day>--""" + value + """</xdtemporal-month-day>\n"""
            if Xd.allow_duration:
                xmlstr += indent + """  <xdtemporal-duration>""" + value + """</xdtemporal-duration>\n"""
            if Xd.allow_ymduration:
                xmlstr += indent + """  <xdtemporal-ymduration>""" + value + """</xdtemporal-ymduration>\n"""
            if Xd.allow_dtduration:
                xmlstr += indent + """  <xdtemporal-dtduration>""" + value + """</xdtemporal-dtduration>\n"""
            xmlstr += indent + """</s3m:ms-""" + str(Xd.ct_id) + """>\n"""
            xmlstr += indent + """  </s3m:ms-""" + str(Xd.adapter_ctid) + """>\n"""

    xmlstr += indent + """</s3m:ms-""" + str(clu.ct_id) + """>\n"""

    return xmlstr


def dataGen(dmd, dm):
    print('Data generation for: ', dm.ct_id)
    print('Using: ', dmd.csv_file)

    recnum = 0
    datapath = os.path.join(MEDIA_ROOT,dmd.csv_file.url.strip('.csv'))
    records = Record.objects.filter(dmd=dmd)

    if os.path.exists(datapath):
        rmtree(datapath)
    os.makedirs(datapath, 0o777)

    with open(os.path.join(MEDIA_ROOT, dmd.csv_file.url)) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=dmd.delim)
        print("Parsing CSV data file.")
        for row in reader:
            #normalize the keys coming from the CSV data to remove suprious whitespace
            csvdata = {}
            for k in row:
                csvdata[k.strip()] = row[k]

            indent = "  "
            data = DataInstance(dm)
            # Entry begins
            data.xml += indent + """<s3m:ms-""" + str(data.dm.entry.ct_id) + """>\n"""
            data.xml += indent + """<label>""" + data.dm.entry.label + """</label>\n"""
            data.xml += indent + """<entry-language>""" + data.dm.entry.language + """</entry-language>\n"""
            data.xml += indent + """<entry-encoding>""" + data.dm.entry.encoding + """</entry-encoding>\n"""
            data.xml += indent + """<current-state>""" + data.dm.entry.state + """</current-state>\n"""
            indent = indent + "  "

            # data
            data.xml += cluster(data.dm.entry.data, records, csvdata, indent)

            # subject
            data.xml += indent + "<subject>\n"
            data.xml += party(data.dm.entry.subject, indent)
            data.xml += indent + "</subject>\n"
            # provider
            data.xml += indent + "<provider>\n"
            data.xml += party(data.dm.entry.provider, indent)
            data.xml += indent + "</provider>\n"
            indent = "  "
            data.xml += indent + """</s3m:ms-""" + str(data.dm.entry.ct_id) + """>\n"""

            recnum += 1
            outfile = os.path.join(datapath, str(recnum).zfill(20)+'.xml')
            f = open(outfile,'w')
            f.write(data.xmlHead)
            f.write(data.xml)
            f.write(data.xmlTail)
            f.close()

class DataInstance(object):
    """
    From a S3Model Data Model, return an instance model that can be populated with data from the CSV.
    """
    def __init__(self, dm):
        self.dm = dm
        self.xml = ''
        self.xmlHead = self.xmlHeader()
        self.xmlTail = '</s3m:' + self.dm.identifier + '>\n'

    def xmlHeader(self):
        """
        Build the header for the example instance
        """
        hstr = '<?xml version="1.0" encoding="UTF-8"?>\n'
        hstr += '<s3m:' + self.dm.identifier + '\n'
        for ns in NS.objects.all():
            hstr += '  xmlns:' + ns.abbrev.strip() + '="' + ns.uri.strip() + '"\n'
        hstr += 'xsi:schemaLocation="http://www.s3model.com/ns/s3m/ http://dmgen.s3model.com/dmlib/' + \
            self.dm.identifier + '.xsd">\n'
        return(hstr)
