# -*- coding: utf-8 -*-
"""
Return strings to build an instance template for a MLHIM 2.5.0 CCD.
"""
from datetime import timedelta, datetime, date
from random import randint, choice, uniform
from xml.sax.saxutils import escape
from decimal import Decimal, ROUND_DOWN, BasicContext, setcontext

from django.contrib import messages

import exrex

def random_dtstr(start=None,end=None):
    if not start:
        start = datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')

    if not end:
        end = datetime.strptime('2015-12-31', '%Y-%m-%d')
    rand_dts = datetime.strftime(start + timedelta(seconds=randint(0, int((end - start).total_seconds()))), '%Y-%m-%dT%H:%M:%S')
    return rand_dts

def dv_boolean(dv, indent):
    choices = []
    for c in dv.trues.splitlines():
        choices.append(c)

    booldv = choice(choices)

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""
    elstr += indent + """  <!-- Use any subtype of ExceptionalValue here when a value is missing or invalid or invalid -->\n"""
    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <true-value>"""+booldv+"""</true-value>\n"""
    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_link(dv, indent, pcs=True):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)
    elstr = ''
    indent += '  '
    if pcs:
        elstr += indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <link>http://www.ccdgen.com</link>\n"""
    elstr += indent + """  <relation>"""+escape(dv.relation.strip())+"""</relation>\n"""
    elstr += indent + """  <relation-uri>"""+escape(dv.relation_uri.strip())+"""</relation-uri>\n"""
    if pcs:
        elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_string(dv, indent, pcs=True):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    if dv.def_val:
        s = dv.def_val
    elif dv.enums:
        enumList = []
        for e in dv.enums.splitlines():
            enumList.append(escape(e))
        s = choice(enumList)
    elif dv.asserts:
        #Example: matches(dvstring-value, '^\d{5}([\-]?\d{3})$')
        try:
            x = dv.asserts.replace("matches(dvstring-value, '",'')[:-1].replace("'",'')
            s = exrex.getone(x)
        except:
            s = 'DefaultString'
    else:
        s = 'DefaultString'

    elstr = ''
    indent += '  '
    if pcs:
        elstr += indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <dvstring-value>"""+s.strip()+"""</dvstring-value>\n"""
    elstr += indent + """  <dvstring-language>"""+dv.lang+"""</dvstring-language>\n"""
    if pcs:
        elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_count(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    enumList = []
    for e in dv.units.enums.splitlines():
        enumList.append(escape(e))
    unit = choice(enumList)

    _min = None
    _max = None

    if dv.min_inclusive != None:
        _min = dv.min_inclusive
    if dv.min_exclusive != None:
        _min = dv.min_exclusive + 1
    if dv.max_inclusive != None:
        _max = dv.max_inclusive
    if dv.max_exclusive != None:
        _max = dv.max_exclusive - 1

    if _max == None:
        _max = 999999
    if _min == None:
        _min = -999999

    mag = randint(_min,_max)

    if dv.total_digits != None:
        if len(str(mag)) > dv.total_digits:  #Opps!  Have to trim it down.
            #Just pick from a list to make life simple
            if dv.total_digits > 14:
                idx = 14
            tdlist = [0,1,11,111,1111,11111,111111,1111111,11111111,1111111111,111111111111,1111111111111,111111111111111]
            mag = tdlist[dv.total_digits]

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """    <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """    <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """    <vte>"""+vte+"""</vte>\n"""
    if dv.reference_ranges:
        for rr in dv.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)

    if dv.normal_status:
        elstr += indent + """  <normal-status>"""+escape(dv.normal_status.strip())+"""</normal-status>\n"""

    elstr += indent + """    <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """    <error>0</error>\n"""
    elstr += indent + """    <accuracy>0</accuracy>\n"""
    elstr += indent + """    <dvcount-value>"""+str(mag)+"""</dvcount-value>\n"""
    elstr += indent + """    <dvcount-units>\n<label>"""+escape(dv.units.label.strip())+"""</label>\n<dvstring-value>"""+unit+"""</dvstring-value>\n</dvcount-units>\n"""

    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_interval(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    indent += '  '
    elstr = indent + """<interval>\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <lower>\n"""
    if dv.lower_bounded:
        elstr += indent + """    <invl-"""+dv.interval_type+""">"""+dv.lower+"""</invl-"""+dv.interval_type+""">\n"""
    else:
        elstr += indent + """    <invl-"""+dv.interval_type+""" xsi:nil='true'/>\n"""
    elstr += indent + """  </lower>\n"""
    elstr += indent + """  <upper>\n"""
    if dv.upper_bounded:
        elstr += indent + """    <invl-"""+dv.interval_type+""">"""+dv.upper+"""</invl-"""+dv.interval_type+""">\n"""
    else:
        elstr += indent + """    <invl-"""+dv.interval_type+""" xsi:nil='true'/>\n"""
    elstr += indent + """  </upper>\n"""

    if dv.lower_included:
        elstr += indent + """  <lower-included>true</lower-included>\n"""
    else:
        elstr += indent + """  <lower-included>false</lower-included>\n"""
    if dv.upper_included:
        elstr += indent + """  <upper-included>true</upper-included>\n"""
    else:
        elstr += indent + """  <upper-included>false</upper-included>\n"""

    if dv.lower_bounded:
        elstr += indent + """  <lower-bounded>true</lower-bounded>\n"""
    else:
        elstr += indent + """  <lower-bounded>false</lower-bounded>\n"""
    if dv.upper_bounded:
        elstr += indent + """  <upper-bounded>true</upper-bounded>\n"""
    else:
        elstr += indent + """  <upper-bounded>false</upper-bounded>\n"""

    elstr += indent + """</interval>\n"""

    return elstr

def dv_file(dv, indent, pcs=True):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    mt = None
    media_list = []
    if dv.media_type:
        for m in dv.media_type.splitlines():
            media_list.append(escape(m))
        mt = choice(media_list)

    elstr = ''
    indent += '  '
    if pcs:
        elstr += indent +"""<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""
    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <size>64536</size>\n"""
    elstr += indent + """  <encoding>utf-8</encoding>\n"""
    elstr += indent + """  <dvfile-language>"""+dv.lang+"""</dvfile-language>\n"""

    if mt:
        elstr += indent + """  <media-type>"""+mt+"""</media-type>\n"""
    else:
        if dv.content_mode == 'binary':
            elstr += indent + """  <media-type>png</media-type>\n"""
        elif dv.content_mode == 'text':
            elstr += indent + """  <media-type>text/plain</media-type>\n"""
        elif dv.content_mode == 'url':
            elstr += indent + """  <media-type>png</media-type>\n"""

    elstr += indent + """  <compression-type>gz</compression-type>\n"""
    elstr += indent + """  <hash-result>dshfsoud6y3rwpef838rhf983trgf9e93w8rytgf</hash-result>\n"""
    elstr += indent + """  <hash-function>MD5</hash-function>\n"""
    elstr += indent + """  <alt-txt>Fake entry data.</alt-txt>\n"""
    if dv.content_mode == 'binary':
        elstr += indent + """<media-content>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</media-content>\n"""
    elif dv.content_mode == 'text':
        elstr += indent + """<text-content>my sample text content</text-content>\n"""
    elif dv.content_mode == 'url':
        elstr += indent + """  <uri>http://www.mlhim.org/fake_media.png</uri>\n"""
    if pcs:
        elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_ordinal(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    o = []
    for a in dv.ordinals.splitlines():
        o.append(escape(a).strip())

    s = []
    for a in dv.symbols.splitlines():
        s.append(escape(a).strip())

    ri = randint(0, len(o)-1) # get a random index

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    if dv.reference_ranges:
        for rr in dv.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if dv.normal_status:
        elstr += indent + """  <normal-status>"""+dv.normal_status.strip()+"""</normal-status>\n"""
    elstr += indent + """  <ordinal>"""+o[ri]+"""</ordinal>\n"""
    elstr += indent + """  <symbol>"""+s[ri]+"""</symbol>\n"""
    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_parsable(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    if dv.size:
        size = dv.size
    else:
        size = 0

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+"""> <!-- DvParsable -->\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <size>"""+str(size)+"""</size>\n"""
    elstr += indent + """  <encoding>utf-8</encoding>\n"""
    elstr += indent + """  <language>"""+dv.lang+"""</language>\n"""
    elstr += indent + """  <DvParsable-dv>Some parsable information.</DvParsable-dv>\n"""
    elstr += indent + """  <formalism>Unknown</formalism>\n"""
    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_quantity(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    enumList = []
    for e in dv.units.enums.splitlines():
        enumList.append(escape(e))
    unit = choice(enumList)

    ctx = BasicContext
    setcontext(ctx)

    _min = None
    _max = None

    if dv.total_digits:  # total digits
        ctx.prec = dv.total_digits

    if dv.min_inclusive != None:
        _min = dv.min_inclusive
    if dv.min_exclusive != None:
        _min = dv.min_exclusive + 1

    if dv.max_inclusive != None:
        _max = dv.max_inclusive
    if dv.max_exclusive != None:
        _max = dv.max_exclusive - 1

    if _max == None:
        _max = 9999.0
    if _min == None:
        _min = 0.0

    _max = float(_max)
    _min = float(_min)

    mag = uniform(_min,_max)

    if dv.fraction_digits:
        if '.' in str(mag):
            fd = str(mag).split('.')[1]
            if len(fd) > dv.fraction_digits:
                fd = fd[0:dv.fraction_digits]
                mag = float(str(mag).split('.')[1] + '.' + fd)

    if dv.total_digits != None:
        if len(str(mag)) > dv.total_digits:  #Opps!  Have to trim it down.
            mag = float(str(mag)[:(0-dv.total_digits)])
            ##Just pick from a list to make life simple
            #if dv.total_digits > 12:
                #idx = 11
            #tdlist = [0,1,11,111,1111,11111,111111,1111111,11111111,1111111111,111111111111,1111111111111,111111111111111]
            #mag = tdlist[dv.total_digits]

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+"""> <!-- DvQuantity -->\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    if dv.reference_ranges:
        for rr in dv.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if dv.normal_status:
        elstr += indent + """  <normal-status>"""+dv.normal_status.strip()+"""</normal-status>\n"""
    elstr += indent + """  <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """  <error>0</error>\n"""
    elstr += indent + """  <accuracy>0</accuracy>\n"""
    elstr += indent + """    <dvquantity-value>"""+str(mag)+"""</dvquantity-value>\n"""
    elstr += indent + """    <dvquantity-units>\n<label>"""+escape(dv.units.label.strip())+"""</label>\n<dvstring-value>"""+unit+"""</dvstring-value>\n</dvquantity-units>\n"""
    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_ratio(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    num_min = None
    num_max = None

    if dv.num_min_inclusive != None:
        num_min = dv.num_min_inclusive
    if dv.num_min_exclusive != None:
        num_min = dv.num_min_exclusive + 1
    if dv.num_max_inclusive != None:
        num_max = dv.num_max_inclusive
    if dv.num_max_exclusive != None:
        num_max = dv.max_exclusive - 1

    if num_max == None:
        num_max = 999999
    if num_min == None:
        num_min = -999999

    fnum_min = float(num_min)
    fnum_max = float(num_max)

    fnum = uniform(fnum_min,fnum_max) # random float

    num = Decimal.from_float(fnum)

    den_min = None
    den_max = None

    if dv.den_min_inclusive != None:
        den_min = dv.den_min_inclusive
    if dv.den_min_exclusive != None:
        den_min = dv.den_min_exclusive + 1
    if dv.den_max_inclusive != None:
        den_max = dv.den_max_inclusive
    if dv.den_max_exclusive != None:
        den_max = dv.den_max_exclusive - 1

    if den_max == None:
        den_max = 999999
    if den_min == None:
        den_min = -999999

    fden_min = float(den_min)
    fden_max = float(den_max)

    fden = uniform(fden_min,fden_max) # random float

    den = Decimal.from_float(fden)

    mag = num/den

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    if dv.reference_ranges:
        for rr in dv.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if dv.normal_status:
        elstr += indent + """  <normal-status>"""+dv.normal_status.strip()+"""</normal-status>\n"""
    elstr += indent + """  <magnitude-status>equal</magnitude-status>\n"""
    elstr += indent + """  <error>0</error>\n"""
    elstr += indent + """  <accuracy>0</accuracy>\n"""
    elstr += indent + """  <ratio-type>"""+dv.ratio_type+"""</ratio-type>\n"""
    elstr += indent + """  <numerator>"""+str(num)+"""</numerator>\n"""
    elstr += indent + """  <denominator>"""+str(den)+"""</denominator>\n"""
    elstr += indent + """    <dvratio-value>"""+str(mag)+"""</dvratio-value>\n"""
    if dv.num_units:
        for e in dv.num_units.enums.splitlines():
            enumList.append(escape(e))
        unit = choice(enumList)
        elstr += indent + """<numerator-units>\n<label>"""+escape(dv.num_units.label.strip())+"""</label>\n<dvstring-value>"""+unit+"""</dvstring-value>\n</numerator-units>\n"""
    if dv.den_units:
        for e in dv.den_units.enums.splitlines():
            enumList.append(escape(e))
        unit = choice(enumList)
        elstr += indent + """<denominator-units>\n<label>"""+escape(dv.den_units.label.strip())+"""</label>\n<dvstring-value>"""+unit+"""</dvstring-value>\n</denominator-units>\n"""
    if dv.ratio_units:
        for e in dv.ratio_units.enums.splitlines():
            enumList.append(escape(e))
        unit = choice(enumList)
        elstr += indent + """<ratio-units>\n<label>"""+escape(dv.ratio_units.label.strip())+"""</label>\n<dvstring-value>"""+unit+"""</dvstring-value>\n</ratio-units>\n"""

    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def dv_temporal(dv, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    start = datetime.strptime('1/1/1970', '%m/%d/%Y')
    end = datetime.strptime('12/31/2020', '%m/%d/%Y')

    rdt = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    rdt2 = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    dur = abs((rdt-rdt2).days)

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+dv.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(dv.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    if dv.reference_ranges:
        for rr in dv.reference_ranges.all():
            elstr += indent + referencerange(rr, indent)
    if dv.normal_status:
        elstr += indent + """  <normal-status>"""+dv.normal_status.strip()+"""</normal-status>\n"""
    if dv.allow_date:
        elstr += indent + """  <dvtemporal-date>"""+datetime.strftime(rdt.date(), '%Y-%m-%d')+"""</dvtemporal-date>\n"""
    if dv.allow_time:
        elstr += indent + """  <dvtemporal-time>"""+datetime.strftime(rdt.date(), '%H:%M:%S')+"""</dvtemporal-time>\n"""
    if dv.allow_datetime:
        elstr += indent + """  <dvtemporal-datetime>"""+random_dtstr()+"""</dvtemporal-datetime>\n"""
    if dv.allow_datetimestamp:
        elstr += indent + """  <dvtemporal-datetime-stamp>"""+random_dtstr()+"""</dvtemporal-datetime-stamp>\n"""
    if dv.allow_day:
        elstr += indent + """  <dvtemporal-day>"""+datetime.strftime(rdt.date(), '---%d')+"""</dvtemporal-day>\n"""
    if dv.allow_month:
        elstr += indent + """  <dvtemporal-month>"""+datetime.strftime(rdt.date(), '--%m')+"""</dvtemporal-month>\n"""
    if dv.allow_year:
        elstr += indent + """  <dvtemporal-year>"""+datetime.strftime(rdt.date(), '%Y')+"""</dvtemporal-year>\n"""
    if dv.allow_year_month:
        elstr += indent + """  <dvtemporal-year-month>"""+datetime.strftime(rdt.date(), '%Y-%m')+"""</dvtemporal-year-month>\n"""
    if dv.allow_month_day:
        elstr += indent + """  <dvtemporal-month-day>--"""+datetime.strftime(rdt.date(), '%m-%d')+"""</dvtemporal-month-day>\n"""
    if dv.allow_duration:
        elstr += indent + """  <dvtemporal-duration>"""+'P'+str(dur)+'D'+"""</dvtemporal-duration>\n"""
    if dv.allow_ymduration:
        elstr += indent + """  <dvtemporal-ymduration>P2Y6M</dvtemporal-ymduration>\n"""
    if dv.allow_dtduration:
        elstr += indent + """  <dvtemporal-dtduration>PT2H10M</dvtemporal-dtduration>\n"""
    elstr += indent + """</mlhim2:pcs-"""+dv.ct_id+""">\n"""

    return elstr

def attestation(a, indent):

    indent += '  '
    elstr = """<label>"""+escape(a.label.strip())+"""</label>\n"""
    if a.view:
        elstr += "<view>\n"
        elstr += dv_file(a.view, indent, False)
        elstr += "</view>\n"
    if a.proof:
        elstr += "<proof>\n"
        elstr += dv_file(a.proof, indent, False)
        elstr += "</proof>\n"
    if a.reason:
        elstr += "<reason>\n"
        elstr += dv_string(a.reason, indent, False)
        elstr += "</reason>\n"
    if a.committer:
        elstr += "<committer>\n"
        elstr += party(a.committer, indent)
        elstr += "</committer>\n"
    elstr += indent + "  <committed>"+random_dtstr()+"Z</committed>\n"
    elstr += indent + "  <pending>true</pending>\n"

    return elstr

def audit(aud, indent):
    indent += '  '
    elstr = indent + """<label>"""+escape(aud.label.strip())+"""</label>\n"""
    if aud.system_id:
        elstr += "<system-id>\n"
        elstr += dv_string(aud.system_id, indent, False)
        elstr += "</system-id>\n"

    if aud.system_user:
        elstr += "<system-user>\n"
        elstr += party(aud.system_user, indent)
        elstr += "</system-user>\n"

    if aud.location:
        elstr += "<location>\n"
        elstr += cluster(aud.location, indent, False)
        elstr += "</location>\n"

    elstr += indent + "  <timestamp>"+random_dtstr()+"Z</timestamp>\n"

    return elstr

def participation(p, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    indent += '  '
    elstr = indent + """<mlhim2:pcs-"""+p.ct_id+""">\n"""
    elstr += indent + """<label>"""+escape(p.label.strip())+"""</label>\n"""

    if p.performer:
        elstr += indent + """<performer>\n"""
        elstr += party(p.performer, indent)
        elstr += indent + """</performer>\n"""

    if p.function:
        elstr += indent + """<function>\n"""
        elstr += dv_string(p.function, indent, False)
        elstr += indent + """</function>\n"""

    if p.mode:
        elstr += indent + """<mode>\n"""
        elstr += dv_string(p.mode, indent, False)
        elstr += indent + """</mode>\n"""

    elstr += indent + """  <start>"""+vtb+"""Z</start>\n"""
    elstr += indent + """  <end>"""+vte+"""Z</end>\n"""
    elstr += indent + """</mlhim2:pcs-"""+p.ct_id+""">\n"""

    return elstr

def party(pi, indent):
    indent += '  '
    elstr = indent + "  <label>"+escape(pi.label.strip())+"</label>\n"
    elstr += indent + "  <party-name>A. Sample Name</party-name>\n"
    if pi.external_ref:
        for ref in pi.external_ref.all():
            elstr += "<party-ref>\n"
            elstr += dv_link(ref, indent, False)
            elstr += "</party-ref>\n"

    if pi.details:
        elstr += "<party-details>\n"
        elstr += cluster(pi.details, indent, False)
        elstr += "</party-details>\n"

    return elstr

def referencerange(rr, indent):

    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    indent += '  '
    elstr = """<mlhim2:pcs-"""+rr.ct_id+"""> <!-- ReferenceRange -->\n"""
    elstr += indent + """  <label>"""+escape(rr.label.strip())+"""</label>\n"""

    elstr += indent + """  <vtb>"""+vtb+"""</vtb>\n"""
    elstr += indent + """  <vte>"""+vte+"""</vte>\n"""
    elstr += indent + """  <definition>"""+escape(rr.definition)+"""</definition>\n"""
    elstr += dv_interval(rr.interval, indent)
    if rr.is_normal:
        n = 'true'
    else:
        n = 'false'
    elstr += indent + """  <is-normal>"""+n+"""</is-normal>\n"""
    elstr += indent + """</mlhim2:pcs-"""+rr.ct_id+""">\n"""

    return elstr

def cluster(clu, indent, pcs=True):
    indent += '  '
    elstr = ''
    if pcs:
        elstr += indent + """<mlhim2:pcs-"""+clu.ct_id+""">\n"""
    elstr += indent + """  <label>"""+escape(clu.label.strip())+"""</label>\n"""
    if clu.clusters:
        for c in clu.clusters.all():
            elstr += cluster(c, indent)

    if clu.dvboolean:
        for dv in clu.dvboolean.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_boolean(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvlink:
        for dv in clu.dvlink.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_link(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvstring:
        for dv in clu.dvstring.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_string(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvfile:
        for dv in clu.dvfile.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_file(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvordinal:
        for dv in clu.dvordinal.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_ordinal(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvcount:
        for dv in clu.dvcount.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_count(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvquantity:
        for dv in clu.dvquantity.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_quantity(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvratio:
        for dv in clu.dvratio.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_ratio(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""

    if clu.dvtemporal:
        for dv in clu.dvtemporal.all():
            elstr += indent + """  <mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
            elstr += dv_temporal(dv, indent+'  ')
            elstr += indent + """  </mlhim2:pcs-"""+dv.adapter_ctid+""">\n"""
    if pcs:
        elstr += indent + """</mlhim2:pcs-"""+clu.ct_id+""">\n"""

    return elstr

