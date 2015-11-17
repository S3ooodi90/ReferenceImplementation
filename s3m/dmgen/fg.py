# -*- coding: utf-8 -*-
"""
Return strings to build an HTML Form template for a MLHIM 2.5.0 CCD.
"""
from datetime import timedelta, datetime, date
from random import randint, choice, uniform
from xml.sax.saxutils import escape
from decimal import Decimal, ROUND_DOWN, BasicContext

import exrex

def random_dtstr(start=None,end=None):
    if not start:
        start = datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')

    if not end:
        end = datetime.strptime('2015-12-31', '%Y-%m-%d')
    rand_dts = datetime.strftime(start + timedelta(seconds=randint(0, int((end - start).total_seconds()))), '%Y-%m-%d %H:%M:%S')
    return rand_dts

def buildHTML(ccdPkg):
    """
    The CCD Package is sent from the generator, then returned after filling in the ccdPkg.html string.
    """

    #check for an Entry
    if ccdPkg.ccd.admin_definition:
        entry = ccdPkg.ccd.admin_definition
    elif ccdPkg.ccd.care_definition:
        entry = ccdPkg.ccd.care_definition
    elif ccdPkg.ccd.demog_definition:
        entry = ccdPkg.ccd.demog_definition

    ccdPkg.html = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n  <head>'
    ccdPkg.html += '    <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">\n'
    ccdPkg.html += '    <title>'+ccdPkg.ccd.title+'</title>\n'
    ccdPkg.html += ' <style type="text/css">\n'
    ccdPkg.html += ' legend {\n'
    ccdPkg.html += '   font-size: 16px;\n'
    ccdPkg.html += '   font-weight: bold;\n'
    ccdPkg.html += ' }\n'
    ccdPkg.html += ' .label {\n'
    ccdPkg.html += '   font-size: 12px;\n'
    ccdPkg.html += '   font-weight: bold;\n'
    ccdPkg.html += ' }\n'
    ccdPkg.html += ' .pcm {\n'
    ccdPkg.html += '  margin-top: 10px; \n'
    ccdPkg.html += '  margin-bottom: 10px; \n'
    ccdPkg.html += '  margin-left: 10px; \n'
    ccdPkg.html += '  margin-right: 10px; \n'
    ccdPkg.html += '  padding: 5px; \n'
    ccdPkg.html += '  border-style: dotted; \n'
    ccdPkg.html += '  border-size: 6px; \n'
    ccdPkg.html += '  border-color: #009999; \n'
    ccdPkg.html += '}\n'
    ccdPkg.html += '.button_bar {\n'
    ccdPkg.html += '  text-align: center;\n'
    ccdPkg.html += '  border-radius: 15px;\n'
    ccdPkg.html += '  background-color: #005566;\n'
    ccdPkg.html += '  margin: 10px;\n'
    ccdPkg.html += '  padding: 10px;\n'
    ccdPkg.html += '}\n'
    ccdPkg.html += '.button_row {\n'
    ccdPkg.html += '  margin: auto;\n'
    ccdPkg.html += '  width: 60%;\n'
    ccdPkg.html += '  padding: 5px;\n'
    ccdPkg.html += '}\n'
    ccdPkg.html += '.button {\n'
    ccdPkg.html += '   border-top: 1px solid #96d1f8;\n'
    ccdPkg.html += '   background: #65a9d7;\n'
    ccdPkg.html += '   background: -webkit-gradient(linear, left top, left bottom, from(#3e779d), to(#65a9d7));\n'
    ccdPkg.html += '   background: -webkit-linear-gradient(top, #3e779d, #65a9d7);\n'
    ccdPkg.html += '   background: -moz-linear-gradient(top, #3e779d, #65a9d7);\n'
    ccdPkg.html += '   background: -ms-linear-gradient(top, #3e779d, #65a9d7);\n'
    ccdPkg.html += '   background: -o-linear-gradient(top, #3e779d, #65a9d7);\n'
    ccdPkg.html += '   padding: 5px 10px;\n'
    ccdPkg.html += '   margin-left 10px;\n'
    ccdPkg.html += '   -webkit-border-radius: 8px;\n'
    ccdPkg.html += '   -moz-border-radius: 8px;\n'
    ccdPkg.html += '   border-radius: 8px;\n'
    ccdPkg.html += '   -webkit-box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    ccdPkg.html += '   -moz-box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    ccdPkg.html += '   box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    ccdPkg.html += '   text-shadow: rgba(0,0,0,.4) 0 1px 0;\n'
    ccdPkg.html += '   color: white;\n'
    ccdPkg.html += '   font-size: 14px;\n'
    ccdPkg.html += '   font-family: Georgia, serif;\n'
    ccdPkg.html += '   text-decoration: none;\n'
    ccdPkg.html += '   vertical-align: middle;\n'
    ccdPkg.html += '   }\n'
    ccdPkg.html += '.button:hover {\n'
    ccdPkg.html += '   border-top-color: #28597a;\n'
    ccdPkg.html += '   background: #28597a;\n'
    ccdPkg.html += '   color: #ccc;\n'
    ccdPkg.html += '   }\n'
    ccdPkg.html += '.button:active {\n'
    ccdPkg.html += '   border-top-color: #1b435e;\n'
    ccdPkg.html += '   background: #1b435e;\n'
    ccdPkg.html += '   }\n'
    ccdPkg.html += '.subpage {\n'
    ccdPkg.html += '  text-align: left;\n'
    ccdPkg.html += '}\n'
    ccdPkg.html += '\n'
    ccdPkg.html += ' </style>\n'
    ccdPkg.html += ' </head>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '<body style="color: rgb(0, 0, 0); background-color: rgb(238, 239, 255);" alink="#349923" link="#000099" vlink="#990099">\n'
    ccdPkg.html += '<div class="" style="text-align: center;">\n'
    ccdPkg.html += '<h1 id="topOfPage">'+ccdPkg.ccd.title+'</h1>\n'
    ccdPkg.html += '<div style="text-align: left;">\n'
    ccdPkg.html += '<form  id="'+entry.ct_id+'" action="" method="post" name="'+entry.label+'" target="" >\n'
    ccdPkg.html += '<div class="button_bar">\n'
    ccdPkg.html += '<span class="button_row">\n'
    ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#subject'"> """+entry.subject.label+""" </button>\n"""
    ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#provider'"> """+entry.provider.label+""" </button>\n"""
    if entry.participations.all():
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#participants'"> """+'Other Participants'+""" </button>\n"""
    if entry.attestation:
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#attestation'"> """+entry.attestation.label+""" </button>\n"""
    if entry.audit:
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#audit'"> """+entry.audit.label+""" </button>\n"""
    if entry.links.all():
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#references'"> """+'References'+""" </button>\n"""
    if entry.workflow:
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#workflow'">Workflow - """+entry.workflow.label+""" </button>\n"""
    if entry.protocol:
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#protocol'">Protocol - """+entry.protocol.label+""" </button>\n"""
    ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#other'"> """+'Other Info'+""" </button>\n"""
    ccdPkg.html += '</span>\n'
    ccdPkg.html += '</div>\n'
    # process the PCMs in a cluster then iterate through the cluster levels one at a time, coming back to the top until completed.
    ccdPkg.html += fcluster(entry.data, '  ')
    ccdPkg.html += '\n'
    ccdPkg.html += '<div style="font-size: 10px; text-align: center;">\n'
    ccdPkg.html += '<button class="button" type="submit" form="'+entry.ct_id+'" > Submit </button> \n'
    ccdPkg.html += '<button class="button" type="cancel" form="'+entry.ct_id+'" > Cancel </button>\n'
    ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '</form>\n'
    ccdPkg.html += '</div>\n'
    ccdPkg.html += '<div>\n'
    ccdPkg.html += '</div>\n'
    ccdPkg.html += '<div id="subject" class="subpage">\n'
    ccdPkg.html += '<hr/>\n'
    ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    ccdPkg.html += '<form  id="'+entry.subject.ct_id+'" action="" method="post" name="'+entry.subject.label+'" target="" >\n'
    ccdPkg.html += fparty(entry.subject, '  ')
    ccdPkg.html += '</form>\n'
    ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '<div id="provider" class="subpage">\n'
    ccdPkg.html += '<hr/>\n'
    ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    ccdPkg.html += '<form  id="'+entry.provider.ct_id+'" action="" method="post" name="'+entry.provider.label+'" target="" >\n'
    ccdPkg.html += fparty(entry.provider, '  ')
    ccdPkg.html += '</form>\n'
    ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    if entry.participations.all():
        ccdPkg.html += '<div id="participants" class="subpage">\n'
        ccdPkg.html += '<hr/>\n'
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        for p in entry.participations.all():
            ccdPkg.html += fparticipation(p, '  ')
        ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    if entry.attestation:
        ccdPkg.html += '<div id="attestation" class="subpage">\n'
        ccdPkg.html += '<hr/>\n'
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        ccdPkg.html += fattestation(entry.attestation,'  ')
        ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    if entry.audit:
        ccdPkg.html += '<div id="audit" class="subpage">\n'
        ccdPkg.html += '<hr/>\n'
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        ccdPkg.html += faudit(entry.audit, '  ')
        ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    if entry.links.all():
        ccdPkg.html += '<div id="references" class="subpage">\n'
        ccdPkg.html += '<hr/>\n'
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        ccdPkg.html += 'Reference Links:\n'
        for e in entry.links.all():
            ccdPkg.html += fdv_link(e, '  ')
        ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    if entry.workflow:
        ccdPkg.html += '<div id="workflow" class="subpage">\n'
        ccdPkg.html += '<hr/>\n'
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        ccdPkg.html += '<br/>Link to workflow engine:\n'
        ccdPkg.html += fdv_link(entry.workflow,'  ')
        ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    if entry.protocol:
        ccdPkg.html += '<div id="protocol" class="subpage">\n'
        ccdPkg.html += '<hr/>\n'
        ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        ccdPkg.html += '<br/>Protocol definition:\n'
        ccdPkg.html += fdv_string(entry.protocol, '  ')
        ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '<div id="other" class="subpage">\n'
    ccdPkg.html += '<hr/>\n'
    ccdPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    ccdPkg.html += '<h3>Other Information</h3>\n'
    ccdPkg.html += 'Language: '+entry.language+'<br/>\n'
    ccdPkg.html += 'Current State: '+entry.state+'<br/>\n'
    ccdPkg.html += 'Encoding: '+entry.encoding+'<br/>\n'
    ccdPkg.html += '<h3>Model Information</h3>\n'
    ccdPkg.html += '<p>Description: <br/> '+ccdPkg.ccd.description+'</p>\n'
    ccdPkg.html += '<p>Author: '+ccdPkg.ccd.author.__str__()+'</p>\n'
    if ccdPkg.ccd.contrib.all():
        ccdPkg.html += '<p>Contributors: <br/>\n'
        for c in ccdPkg.ccd.contrib.all():
            ccdPkg.html += c.__str__()+'<br/>\n'
        ccdPkg.html += '</p>\n'
    ccdPkg.html += '<p>Keywords: '+ccdPkg.ccd.subject+'</p>\n'
    ccdPkg.html += '<p>Source Reference: '+ccdPkg.ccd.source+'</p>\n'
    ccdPkg.html += '<p>Relation to another model: '+ccdPkg.ccd.relation+'</p>\n'
    ccdPkg.html += '<p>Coverage: '+ccdPkg.ccd.coverage+'</p>\n'
    ccdPkg.html += '<p>Publisher: '+ccdPkg.ccd.publisher+'</p>\n'
    ccdPkg.html += '<p>License: '+ccdPkg.ccd.rights+'</p>\n'
    ccdPkg.html += '<p>Publication Date: '+str(ccdPkg.ccd.pub_date)+'</p>\n'
    ccdPkg.html += '<p>Language: '+ccdPkg.ccd.dc_language+'</p>\n'
    ccdPkg.html += '<p>Top level RDF: <br/><code> <pre>&lt;rdf:Description rdf:about="http://www.mlhim.org/ns/mlhim2:pcm-'+ccdPkg.ccd.ct_id+'"/&gt;<br/>\n'
    ccdPkg.html += '  &lt;rdfs:subClassOf rdf:resource="mlhim2:CCDType"/&gt;<br/>\n'
    ccdPkg.html += '  &lt;rdfs:label&gt;'+ccdPkg.ccd.title+'&lt;/rdfs:label&gt;<br/>\n'
    if len(ccdPkg.ccd.pred_obj.all()) != 0:
        for po in ccdPkg.ccd.pred_obj.all():
                ccdPkg.html += "&lt;"+po.predicate.ns_abbrev.__str__()+":"+po.predicate.class_name.strip()+" rdf:resource='"+ po.object_uri +"'/&gt;<br/>\n"
    ccdPkg.html += '&lt;/rdf:Description&gt;</pre></code><br/>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '</p>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '</div>\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '\n'
    ccdPkg.html += '<span style="font-size: 10px; text-align: center;">\n'
    ccdPkg.html += 'Generated by the <a href="http:www.ccdgen.com" target="_blank">CCD-Gen</a> \n'
    ccdPkg.html += '</span>\n'

    ccdPkg.html += '    </div>\n  </body>\n</html>'

    return(ccdPkg)

def fcluster(clu, indent):
    indent += '  '
    if len(clu.pred_obj.all()) != 0:
        link = clu.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ''
    frmstr += '<fieldset><legend>'+clu.label+'</legend><br/>\n'
    frmstr += '<div>\n'

    if clu.dvstring:
        for dv in clu.dvstring.all():
            frmstr += fdv_string(dv, indent+'  ')

    if clu.dvboolean:
        for dv in clu.dvboolean.all():
            frmstr += fdv_boolean(dv, indent+'  ')

    if clu.dvlink:
        for dv in clu.dvlink.all():
            frmstr += fdv_link(dv, indent+'  ')

    if clu.dvfile:
        for dv in clu.dvfile.all():
            frmstr += fdv_file(dv, indent+'  ')

    if clu.dvordinal:
        for dv in clu.dvordinal.all():
            frmstr += fdv_ordinal(dv, indent+'  ')

    if clu.dvcount:
        for dv in clu.dvcount.all():
            frmstr += fdv_count(dv, indent+'  ')

    if clu.dvquantity:
        for dv in clu.dvquantity.all():
            frmstr += fdv_quantity(dv, indent+'  ')

    if clu.dvratio:
        for dv in clu.dvratio.all():
            frmstr += fdv_ratio(dv, indent+'  ')

    if clu.dvtemporal:
        for dv in clu.dvtemporal.all():
            frmstr += fdv_temporal(dv, indent+'  ')

    # close the fieldset after getting all of the data types, then loop through clusters
    frmstr += '</div>\n'
    frmstr += '</fieldset>\n'

    if clu.clusters:
        for c in clu.clusters.all():
            frmstr += fcluster(c, indent)

    return(frmstr)

def fdv_boolean(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    choices = ['-------']
    for c in dv.trues.splitlines():
        choices.append(c)
    for c in dv.falses.splitlines():
        choices.append(c)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Choose  a value: <select name='pcm-"+dv.ct_id+"'>\n"
    for c in choices:
        frmstr += indent + "  <option value='"+c+"' label='"+c+"'>"+c+"</option><br />\n"
    frmstr += indent + "</select><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_link(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter a URI: <input name='pcm-"+dv.ct_id+":DvURI' type='text' size='30' value=''/>\n"
    frmstr += indent + " Relationship: <em>"+dv.relation.strip()+"</em><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_string(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    a = None
    enumList = []

    x = None
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

    if dv.enums:
        for e in dv.enums.splitlines():
            enumList.append(escape(e))

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    if enumList:
        frmstr += indent + " Choose a value: <select name='pcm-"+dv.ct_id+":dvstring-value'>\n"
        for c in enumList:
            frmstr += indent + "  <option value='"+c+"' label='"+c+"'>"+c+"</option>\n"
        frmstr += indent + "</select><br />\n"
    else:
        frmstr += indent + " Enter a string: <input name='pcm-"+dv.ct_id+":DvString' type='text' size='30' value='"+s+"'/>"
    if x:
        frmstr += indent + " Match (regex): "+x+"<br />\n"
    frmstr += indent + " Language: <input name='pcm-"+dv.ct_id+":language' type='text' size='6' value='"+dv.lang+"'/><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_count(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    if dv.normal_status:
        ns = dv.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if dv.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in dv.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    _min = None
    _max = None

    if dv.min_inclusive:
        _min = dv.min_inclusive
    if dv.min_exclusive:
        _min = dv.min_exclusive + 1
    if dv.max_inclusive:
        _max = dv.max_inclusive
    if dv.max_exclusive:
        _max = dv.max_exclusive - 1

    if not _max:
        _max = 999999
    if not _min:
        _min = -999999

    mag = randint(_min,_max)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter Count:  <input name='pcm-"+dv.ct_id+":dvcount-value' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='pcm-"+dv.ct_id+":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='pcm-"+dv.ct_id+":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='pcm-"+dv.ct_id+":accuracy' type='number' value='0'/><br />\n"
    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + " Units:<br />\n"
    if dv.units:
        frmstr += fdv_string(dv.units, indent)+'<br />'

    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_interval(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"
    frmstr += indent + "Lower Value: "+str(dv.lower)+" Upper Value: "+str(dv.upper)+"<br />\n"
    frmstr += indent + "Lower Included: "+str(dv.lower_included)+" Upper Included: "+str(dv.upper_included)+"<br />\n"
    frmstr += indent + "Lower Bounded: "+str(dv.lower_bounded)+" Upper Bounded: "+str(dv.upper_bounded)+"<br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_file(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"
    frmstr += indent + " Size (bytes):  <input name='pcm-"+dv.ct_id+":size' type='number' value='0'/>\n"
    frmstr += indent + " Encoding: <input name='pcm-"+dv.ct_id+":encoding' type='text' value='utf-8'/>\n"
    frmstr += indent + " Language:  <input name='pcm-"+dv.ct_id+":language' type='text' value='"+dv.lang+"'/><br />\n"
    frmstr += indent + " MIME Type: <input name='pcm-"+dv.ct_id+":mime-type' type='text' value=''/>\n"
    frmstr += indent + " Compression Type: <input name='pcm-"+dv.ct_id+":compression-type' type='text' value=''/><br />\n"
    frmstr += indent + " HASH Result: <input name='pcm-"+dv.ct_id+":hash-result' type='text' value=''/>\n"
    frmstr += indent + " HASH Function: <input name='pcm-"+dv.ct_id+":hash-function' type='text' value=''/><br />\n"
    frmstr += indent + " Alt. Text: <input name='pcm-"+dv.ct_id+":alt-txt' type='text' value=''/><br />\n"
    if dv.content_mode == 'url':
        frmstr += indent + " URL: <input name='pcm-"+dv.ct_id+":uri' type='url' value=''/> (to content location)<br />\n"
    elif dv.content_mode == 'binary':
        frmstr += indent + " Media Content: <br /><textarea name='pcm-"+dv.ct_id+":media-content' type='text' value=''/> (paste base64Binary encoded content here)</textarea>\n"
        frmstr += "<b>OR</b> Select a file to upload: <input type='file' name='pcm-"+dv.ct_id+":media-content' size='40' /><br /><br />\n"
    elif dv.content_mode == 'text':
        frmstr += indent + " Text Content: <br /><textarea name='pcm-"+dv.ct_id+":text-content' type='text' value=''/> (paste text content here)</textarea>\n"
        frmstr += "<b>OR</b> Select a file to upload: <input type='file' name='pcm-"+dv.ct_id+":text-content'  size='40' /><br /><br />\n"
    else:
        frmstr += "<br /><b>An error in the model was detected and it doesn't allow a content mode.</b><br /><br />\n"

    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_ordinal(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    if dv.normal_status:
        ns = dv.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if dv.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in dv.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent) + '<br />'

    o = []
    for a in dv.ordinals.splitlines():
        o.append(escape(a).strip())

    s = []
    for a in dv.symbols.splitlines():
        s.append(escape(a).strip())

    ann = []
    for x in dv.annotations.splitlines():
        ann.append(escape(x).strip())

    ri = randint(0, len(o)-1) # get a random index

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"
    if s:
        frmstr += indent + " Choose a value: <select name='pcm-"+dv.ct_id+":symbol'>\n"
        for c in s:
            frmstr += indent + "  <option value='"+c+"' label='"+c+"'>"+c+"</option>\n"
        frmstr += indent + "</select><br />\n"

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_quantity(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'

    if dv.normal_status:
        ns = dv.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if dv.reference_ranges:
        rrstr += 'Reference Ranges:<br /> '
        for rr in dv.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    ctx = BasicContext

    _min = None
    _max = None

    if dv.total_digits:  # total digits
        ctx.prec = int(dv.total_digits)

    if dv.min_inclusive != None:
        _min = dv.min_inclusive
    if dv.min_exclusive != None:
        _min = dv.min_exclusive + 1

    if dv.max_inclusive != None:
        _max = dv.max_inclusive
    if dv.max_exclusive != None:
        _max = dv.max_exclusive - 1

    if _max == None:
        _max = 999999999999999999999999999999999999999999
    if _min == None:
        _min = -99999999999999999999999999999999999999999

    f_min = float(_min)
    f_max = float(_max)

    fmag = uniform(f_min,f_max) # random float between min and max

    mag = ctx.create_decimal_from_float(fmag)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter Quantity:  <input name='pcm-"+dv.ct_id+":magnitude' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='pcm-"+dv.ct_id+":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='pcm-"+dv.ct_id+":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='pcm-"+dv.ct_id+":accuracy' type='number' value='0'/><br />\n"

    frmstr += indent + " Units:<br />\n"
    if dv.units:
        frmstr += fdv_string(dv.units, indent) + '<br />'

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_ratio(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="pcm">\n'

    if dv.normal_status:
        ns = dv.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if dv.reference_ranges:
        rrstr += 'Reference Ranges:<br /> '
        for rr in dv.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    num_min = None
    num_max = None

    if dv.num_min_inclusive:
        num_min = dv.num_min_inclusive
    if dv.num_min_exclusive:
        num_min = dv.num_min_exclusive + 1
    if dv.num_max_inclusive:
        num_max = dv.num_max_inclusive
    if dv.num_max_exclusive:
        num_max = dv.max_exclusive - 1

    if not num_max:
        num_max = 999999
    if not num_min:
        num_min = -999999

    num = uniform(num_min,num_max) # random float

    den_min = None
    den_max = None

    if dv.den_min_inclusive:
        den_min = dv.den_min_inclusive
    if dv.den_min_exclusive:
        den_min = dv.den_min_exclusive + 1
    if dv.den_max_inclusive:
        den_max = dv.den_max_inclusive
    if dv.den_max_exclusive:
        den_max = dv.den_max_exclusive - 1

    if not den_max:
        den_max = 999999
    if not den_min:
        den_min = -999999

    den = uniform(den_min,den_max) # random float

    mag = num/den

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter Ratio (magnitude):  <input name='pcm-"+dv.ct_id+":magnitude' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='pcm-"+dv.ct_id+":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='pcm-"+dv.ct_id+":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='pcm-"+dv.ct_id+":accuracy' type='number' value='0'/><br />\n"
    frmstr += indent + " Ratio Type:  <select name='pcm-"+dv.ct_id+":ratio-type'>\n"
    frmstr += indent + "  <option value='ratio'  label='Ratio'>Ratio</option>\n"
    frmstr += indent + "  <option value='proportion' label='Proportion'>Proportion</option>\n"
    frmstr += indent + "  <option value='rate' label='Rate'>Rate</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Numerator:  <input name='pcm-"+dv.ct_id+":numerator' type='number' value='0'/>\n"
    frmstr += indent + " Denominator:  <input name='pcm-"+dv.ct_id+":denominator' type='number' value='0'/><br />\n"

    frmstr += indent + "  Numerator Units:<br />\n"
    if dv.num_units:
        frmstr += fdv_string(dv.num_units, indent)

    frmstr += indent + "  Denominator Units:<br />\n"
    if dv.den_units:
        frmstr += fdv_string(dv.den_units, indent)

    frmstr += indent + "  Ratio Units: <br />\n"
    if dv.ratio_units:
        frmstr += fdv_string(dv.ratio_units, indent)

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fdv_temporal(dv, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(dv.description) + "\n\n"  # tooltip
    if len(dv.pred_obj.all()) != 0:
        link = dv.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="pcm">\n'

    if dv.normal_status:
        ns = dv.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if dv.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in dv.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    start = datetime.strptime('1/1/1970', '%m/%d/%Y')
    end = datetime.strptime('12/31/2020', '%m/%d/%Y')
    rdt = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    rdt2 = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    dur = abs((rdt-rdt2).days)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+dv.label.strip()+"</a><br /></span>\n"

    if dv.allow_date:
        frmstr += indent + " Date:  <input name='pcm-"+dv.ct_id+":dvtemporal-date' type='date' value=''/> (YYYY-MM-DD)<br />\n"
    if dv.allow_time:
        frmstr += indent + " Time:  <input name='pcm-"+dv.ct_id+":dvtemporal-time' type='time' value=''/> (HH:MM:SS)<br />\n"
    if dv.allow_datetime:
        frmstr += indent + " Datetime:  <input name='pcm-"+dv.ct_id+":dvtemporal-datetime' type='datetime-local' value=''/> (YYYY-MM-DDTHH:MM:SS)<br />\n"
    if dv.allow_datetimestamp:
        frmstr += indent + " DatetimeStamp:  <input name='pcm-"+dv.ct_id+":dvtemporal-datetime-stamp' type='datetimestamp' value=''/> (YYYY-MM-DDTHH:MM:SS)<br />\n"
    if dv.allow_day:
        frmstr += indent + " Day:  <input name='pcm-"+dv.ct_id+":dvtemporal-day' type='day' value=''/> (--DD)<br />\n"
    if dv.allow_month:
        frmstr += indent + " Month:  <input name='pcm-"+dv.ct_id+":dvtemporal-month' type='month' value=''/> (-MM)<br />\n"
    if dv.allow_year:
        frmstr += indent + " Year:  <input name='pcm-"+dv.ct_id+":dvtemporal-year' type='year' value=''/> (YYYY)<br />\n"
    if dv.allow_year_month:
        frmstr += indent + " Year-Month:  <input name='pcm-"+dv.ct_id+":dvtemporal-year-month' type='text' value=''/> (YYYY-MM)<br />\n"
    if dv.allow_month_day:
        frmstr += indent + " Month-Day:  <input name='pcm-"+dv.ct_id+":dvtemporal-month-day' type='text' value=''/> (-MM-DD)<br />\n"
    if dv.allow_duration:
        frmstr += indent + " Duration:  <input name='pcm-"+dv.ct_id+":dvtemporal-duration' type='text' value='P'/> (PxxYxxMxxDTxxHxxMxxS)<br />\n"
    if dv.allow_ymduration:
        frmstr += indent + " Year-Month Duration:  <input name='pcm-"+dv.ct_id+":dvtemporal-ymduration' type='text' value='P'/> (PxxYxxM)<br />\n"
    if dv.allow_dtduration:
        frmstr += indent + " Day Time Duration:  <input name='pcm-"+dv.ct_id+":dvtemporal-dtduration' type='text' value='P'/> (PxDTxxHxxMxxS)<br />\n"

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+dv.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+dv.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fparty(pi, indent):
    tt = escape(pi.description) + "\n\n"  # tooltip
    if len(pi.pred_obj.all()) != 0:
        link = pi.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="pcm">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+pi.label+"</a><br /></span>\n"
    frmstr += indent + "Name: <input name='pcm-"+pi.ct_id+":Party' type='text' size='80'/><br/>\n"
    if pi.external_ref:
        for ref in pi.external_ref.all():
            frmstr += fdv_link(ref, indent)

    if pi.details:
        frmstr += fcluster(pi.details, indent)

    frmstr += '</div>\n'

    return frmstr

def fparticipation(p, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(p.description) + "\n\n"  # tooltip
    if len(p.pred_obj.all()) != 0:
        link = p.pred_obj.all()[0].object_uri
    else:
        link = "#"

    indent += '  '
    frmstr = indent + "<div id='"+p.ct_id+"' class='pcm'> \n"
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+p.label+"</a><br /></span>\n"
    if p.performer:
        frmstr += fparty(p.performer, indent)

    if p.function:
        frmstr += fdv_string(p.function, indent)

    if p.mode:
        frmstr += fdv_string(p.mode, indent)

    frmstr += indent + "  Start Time: <input name='pct-"+p.ct_id+":start-time' type='datetime-local' value='"+vtb+"'/><br />\n"
    frmstr += indent + "  End Time: <input name='pct-"+p.ct_id+":end-time' type='datetime-local' value='"+vte+"'/><br />\n"

    frmstr += indent + " </div>\n"

    return frmstr

def fattestation(a, indent):
    tt = escape(a.description) + "\n\n"  # tooltip
    if len(a.pred_obj.all()) != 0:
        link = a.pred_obj.all()[0].object_uri
    else:
        link = "#"

    indent += '  '
    frmstr = indent + "<div id='"+a.ct_id+"' class='pcm'> \n"
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+a.label+"</a><br /></span>\n"

    if a.view:
        frmstr += fdv_file(a.view, indent)

    if a.proof:
        frmstr += fdv_file(a.proof, indent)

    if a.reason:
        frmstr += fdv_string(a.reason, indent)

    if a.committer:
        frmstr += fparty(a.committer, indent)

    frmstr += indent + "  Time Committed: <input name='pct-"+a.ct_id+":time-committed' type='datetime-local' value='"+datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')+"'/><br />\n"
    frmstr += indent + "  Is Pending: <select>"
    frmstr += indent + "<option>Yes</option>"
    frmstr += indent + "<option>No</option>"
    frmstr += indent + "</select><br />\n"

    frmstr += indent + " </div>\n"

    return frmstr

def faudit(aud, indent):
    tt = escape(aud.description) + "\n\n"  # tooltip
    if len(aud.pred_obj.all()) != 0:
        link = aud.pred_obj.all()[0].object_uri
    else:
        link = "#"

    indent += '  '
    frmstr = indent + "<div id='"+aud.ct_id+"' class='pcm'> \n"
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+aud.label+"</a><br /></span>\n"

    if aud.system_id:
        frmstr += fdv_string(aud.system_id, indent)

    if aud.system_user:
        frmstr += fparty(aud.system_user, indent)

    if aud.location:
        frmstr += fcluster(aud.location, indent)

    frmstr += indent + "  Timestamp: <input name='pct-"+aud.ct_id+":timestamp' type='datetime-local' value='"+datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')+"'/><br />\n"

    frmstr += indent + " </div>\n"

    return frmstr

def freferencerange(rr, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(rr.description) + "\n\n"  # tooltip
    if len(rr.pred_obj.all()) != 0:
        link = rr.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="pcm">\n'
    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+rr.label.strip()+"</a><br /></span>\n"
    frmstr += indent + "ReferenceRange Definition: <b>"+rr.definition+"</b><br />\n"
    frmstr += fdv_interval(rr.interval, indent)
    if rr.is_normal:
        n = 'Yes'
    else:
        n = 'No'

    frmstr += indent + "Normal range: "+n+"<br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='pcm-"+rr.ct_id+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='pcm-"+rr.ct_id+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr
