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

def buildHTML(dmPkg):
    """
    The CCD Package is sent from the generator, then returned after filling in the ccdPkg.html string.
    """

    entry = dmPkg.dm.entry

    dmPkg.html = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n  <head>'
    dmPkg.html += '    <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">\n'
    dmPkg.html += '    <title>'+dmPkg.dm.title+'</title>\n'
    dmPkg.html += ' <style type="text/css">\n'
    dmPkg.html += ' legend {\n'
    dmPkg.html += '   font-size: 16px;\n'
    dmPkg.html += '   font-weight: bold;\n'
    dmPkg.html += ' }\n'
    dmPkg.html += ' .label {\n'
    dmPkg.html += '   font-size: 12px;\n'
    dmPkg.html += '   font-weight: bold;\n'
    dmPkg.html += ' }\n'
    dmPkg.html += ' .mc {\n'
    dmPkg.html += '  margin-top: 10px; \n'
    dmPkg.html += '  margin-bottom: 10px; \n'
    dmPkg.html += '  margin-left: 10px; \n'
    dmPkg.html += '  margin-right: 10px; \n'
    dmPkg.html += '  padding: 5px; \n'
    dmPkg.html += '  border-style: dotted; \n'
    dmPkg.html += '  border-size: 6px; \n'
    dmPkg.html += '  border-color: #009999; \n'
    dmPkg.html += '}\n'
    dmPkg.html += '.button_bar {\n'
    dmPkg.html += '  text-align: center;\n'
    dmPkg.html += '  border-radius: 15px;\n'
    dmPkg.html += '  background-color: #005566;\n'
    dmPkg.html += '  margin: 10px;\n'
    dmPkg.html += '  padding: 10px;\n'
    dmPkg.html += '}\n'
    dmPkg.html += '.button_row {\n'
    dmPkg.html += '  margin: auto;\n'
    dmPkg.html += '  width: 60%;\n'
    dmPkg.html += '  padding: 5px;\n'
    dmPkg.html += '}\n'
    dmPkg.html += '.button {\n'
    dmPkg.html += '   border-top: 1px solid #96d1f8;\n'
    dmPkg.html += '   background: #65a9d7;\n'
    dmPkg.html += '   background: -webkit-gradient(linear, left top, left bottom, from(#3e779d), to(#65a9d7));\n'
    dmPkg.html += '   background: -webkit-linear-gradient(top, #3e779d, #65a9d7);\n'
    dmPkg.html += '   background: -moz-linear-gradient(top, #3e779d, #65a9d7);\n'
    dmPkg.html += '   background: -ms-linear-gradient(top, #3e779d, #65a9d7);\n'
    dmPkg.html += '   background: -o-linear-gradient(top, #3e779d, #65a9d7);\n'
    dmPkg.html += '   padding: 5px 10px;\n'
    dmPkg.html += '   margin-left 10px;\n'
    dmPkg.html += '   -webkit-border-radius: 8px;\n'
    dmPkg.html += '   -moz-border-radius: 8px;\n'
    dmPkg.html += '   border-radius: 8px;\n'
    dmPkg.html += '   -webkit-box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    dmPkg.html += '   -moz-box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    dmPkg.html += '   box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    dmPkg.html += '   text-shadow: rgba(0,0,0,.4) 0 1px 0;\n'
    dmPkg.html += '   color: white;\n'
    dmPkg.html += '   font-size: 14px;\n'
    dmPkg.html += '   font-family: Georgia, serif;\n'
    dmPkg.html += '   text-decoration: none;\n'
    dmPkg.html += '   vertical-align: middle;\n'
    dmPkg.html += '   }\n'
    dmPkg.html += '.button:hover {\n'
    dmPkg.html += '   border-top-color: #28597a;\n'
    dmPkg.html += '   background: #28597a;\n'
    dmPkg.html += '   color: #ccc;\n'
    dmPkg.html += '   }\n'
    dmPkg.html += '.button:active {\n'
    dmPkg.html += '   border-top-color: #1b435e;\n'
    dmPkg.html += '   background: #1b435e;\n'
    dmPkg.html += '   }\n'
    dmPkg.html += '.subpage {\n'
    dmPkg.html += '  text-align: left;\n'
    dmPkg.html += '}\n'
    dmPkg.html += '\n'
    dmPkg.html += ' </style>\n'
    dmPkg.html += ' </head>\n'
    dmPkg.html += '\n'
    dmPkg.html += '<body style="color: rgb(0, 0, 0); background-color: rgb(238, 239, 255);" alink="#349923" link="#000099" vlink="#990099">\n'
    dmPkg.html += '<div class="" style="text-align: center;">\n'
    dmPkg.html += '<h1 id="topOfPage">'+dmPkg.dm.title+'</h1>\n'
    dmPkg.html += '<div style="text-align: left;">\n'
    dmPkg.html += '<form  id="'+str(entry.ct_id)+'" action="" method="post" name="'+entry.label+'" target="" >\n'
    dmPkg.html += '<div class="button_bar">\n'
    dmPkg.html += '<span class="button_row">\n'
    dmPkg.html += """<button class="button" type="button" onClick="parent.location='#subject'"> """+entry.subject.label+""" </button>\n"""
    dmPkg.html += """<button class="button" type="button" onClick="parent.location='#provider'"> """+entry.provider.label+""" </button>\n"""
    if entry.participations.all():
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#participants'"> """+'Other Participants'+""" </button>\n"""
    if entry.attestation:
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#attestation'"> """+entry.attestation.label+""" </button>\n"""
    if entry.audit:
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#audit'"> """+entry.audit.label+""" </button>\n"""
    if entry.links.all():
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#references'"> """+'References'+""" </button>\n"""
    if entry.workflow:
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#workflow'">Workflow - """+entry.workflow.label+""" </button>\n"""
    if entry.protocol:
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#protocol'">Protocol - """+entry.protocol.label+""" </button>\n"""
    dmPkg.html += """<button class="button" type="button" onClick="parent.location='#other'"> """+'Other Info'+""" </button>\n"""
    dmPkg.html += '</span>\n'
    dmPkg.html += '</div>\n'
    # process the PCMs in a cluster then iterate through the cluster levels one at a time, coming back to the top until completed.
    dmPkg.html += fcluster(entry.data, '  ')
    dmPkg.html += '\n'
    dmPkg.html += '<div style="font-size: 10px; text-align: center;">\n'
    dmPkg.html += '<button class="button" type="submit" form="'+str(entry.ct_id)+'" > Submit </button> \n'
    dmPkg.html += '<button class="button" type="cancel" form="'+str(entry.ct_id)+'" > Cancel </button>\n'
    dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    dmPkg.html += '</form>\n'
    dmPkg.html += '</div>\n'
    dmPkg.html += '<div>\n'
    dmPkg.html += '</div>\n'
    dmPkg.html += '<div id="subject" class="subpage">\n'
    dmPkg.html += '<hr/>\n'
    dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    dmPkg.html += '<form  id="'+str(entry.subject.ct_id)+'" action="" method="post" name="'+entry.subject.label+'" target="" >\n'
    dmPkg.html += fparty(entry.subject, '  ')
    dmPkg.html += '</form>\n'
    dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    dmPkg.html += '<div id="provider" class="subpage">\n'
    dmPkg.html += '<hr/>\n'
    dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    dmPkg.html += '<form  id="'+str(entry.provider.ct_id)+'" action="" method="post" name="'+entry.provider.label+'" target="" >\n'
    dmPkg.html += fparty(entry.provider, '  ')
    dmPkg.html += '</form>\n'
    dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    if entry.participations.all():
        dmPkg.html += '<div id="participants" class="subpage">\n'
        dmPkg.html += '<hr/>\n'
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        for p in entry.participations.all():
            dmPkg.html += fparticipation(p, '  ')
        dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    if entry.attestation:
        dmPkg.html += '<div id="attestation" class="subpage">\n'
        dmPkg.html += '<hr/>\n'
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dmPkg.html += fattestation(entry.attestation,'  ')
        dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    if entry.audit:
        dmPkg.html += '<div id="audit" class="subpage">\n'
        dmPkg.html += '<hr/>\n'
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dmPkg.html += faudit(entry.audit, '  ')
        dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    if entry.links.all():
        dmPkg.html += '<div id="references" class="subpage">\n'
        dmPkg.html += '<hr/>\n'
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dmPkg.html += 'Reference Links:\n'
        for e in entry.links.all():
            dmPkg.html += fXd_link(e, '  ')
        dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    if entry.workflow:
        dmPkg.html += '<div id="workflow" class="subpage">\n'
        dmPkg.html += '<hr/>\n'
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dmPkg.html += '<br/>Link to workflow engine:\n'
        dmPkg.html += fXd_link(entry.workflow,'  ')
        dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    if entry.protocol:
        dmPkg.html += '<div id="protocol" class="subpage">\n'
        dmPkg.html += '<hr/>\n'
        dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dmPkg.html += '<br/>Protocol definition:\n'
        dmPkg.html += fXd_string(entry.protocol, '  ')
        dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    dmPkg.html += '<div id="other" class="subpage">\n'
    dmPkg.html += '<hr/>\n'
    dmPkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    dmPkg.html += '<h3>Other Information</h3>\n'
    dmPkg.html += 'Language: '+entry.language+'<br/>\n'
    dmPkg.html += 'Current State: '+entry.state+'<br/>\n'
    dmPkg.html += 'Encoding: '+entry.encoding+'<br/>\n'
    dmPkg.html += '<h3>Model Information</h3>\n'
    dmPkg.html += '<p>Description: <br/> '+dmPkg.dm.description+'</p>\n'
    dmPkg.html += '<p>Author: '+dmPkg.dm.author.__str__()+'</p>\n'
    if dmPkg.dm.contrib.all():
        dmPkg.html += '<p>Contributors: <br/>\n'
        for c in dmPkg.dm.contrib.all():
            dmPkg.html += c.__str__()+'<br/>\n'
        dmPkg.html += '</p>\n'
    dmPkg.html += '<p>Keywords: '+dmPkg.dm.subject+'</p>\n'
    dmPkg.html += '<p>Source Reference: '+dmPkg.dm.source+'</p>\n'
    dmPkg.html += '<p>Relation to another model: '+dmPkg.dm.relation+'</p>\n'
    dmPkg.html += '<p>Coverage: '+dmPkg.dm.coverage+'</p>\n'
    dmPkg.html += '<p>Publisher: '+dmPkg.dm.publisher+'</p>\n'
    dmPkg.html += '<p>License: '+dmPkg.dm.rights+'</p>\n'
    dmPkg.html += '<p>Publication Date: '+str(dmPkg.dm.pub_date)+'</p>\n'
    dmPkg.html += '<p>Language: '+dmPkg.dm.dc_language+'</p>\n'
    dmPkg.html += '<p>Top level RDF: <br/><code> <pre>&lt;rdf:Description rdf:about="http://www.mlhim.org/ns/s3m:mc-'+str(dmPkg.dm.ct_id)+'"/&gt;<br/>\n'
    dmPkg.html += '  &lt;rdfs:subClassOf rdf:resource="s3m:CCDType"/&gt;<br/>\n'
    dmPkg.html += '  &lt;rdfs:label&gt;'+dmPkg.dm.title+'&lt;/rdfs:label&gt;<br/>\n'
    if len(dmPkg.dm.pred_obj.all()) != 0:
        for po in dmPkg.dm.pred_obj.all():
                dmPkg.html += "&lt;"+po.predicate.ns_abbrev.__str__()+":"+po.predicate.class_name.strip()+" rdf:resource='"+ po.object_uri +"'/&gt;<br/>\n"
    dmPkg.html += '&lt;/rdf:Description&gt;</pre></code><br/>\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '</p>\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '</div>\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '\n'
    dmPkg.html += '<span style="font-size: 10px; text-align: center;">\n'
    dmPkg.html += 'Generated by the <a href="http://dmgen.s3model.com" target="_blank">DMGen</a> \n'
    dmPkg.html += '</span>\n'

    dmPkg.html += '    </div>\n  </body>\n</html>'

    return(dmPkg)

def fcluster(clu, indent):
    indent += '  '
    if len(clu.pred_obj.all()) != 0:
        link = clu.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ''
    frmstr += '<fieldset><legend>'+clu.label+'</legend><br/>\n'
    frmstr += '<div>\n'

    if clu.Xdstring:
        for Xd in clu.Xdstring.all():
            frmstr += fXd_string(Xd, indent+'  ')

    if clu.Xdboolean:
        for Xd in clu.Xdboolean.all():
            frmstr += fXd_boolean(Xd, indent+'  ')

    if clu.Xdlink:
        for Xd in clu.Xdlink.all():
            frmstr += fXd_link(Xd, indent+'  ')

    if clu.Xdfile:
        for Xd in clu.Xdfile.all():
            frmstr += fXd_file(Xd, indent+'  ')

    if clu.Xdordinal:
        for Xd in clu.Xdordinal.all():
            frmstr += fXd_ordinal(Xd, indent+'  ')

    if clu.Xdcount:
        for Xd in clu.Xdcount.all():
            frmstr += fXd_count(Xd, indent+'  ')

    if clu.Xdquantity:
        for Xd in clu.Xdquantity.all():
            frmstr += fXd_quantity(Xd, indent+'  ')

    if clu.Xdratio:
        for Xd in clu.Xdratio.all():
            frmstr += fXd_ratio(Xd, indent+'  ')

    if clu.Xdtemporal:
        for Xd in clu.Xdtemporal.all():
            frmstr += fXd_temporal(Xd, indent+'  ')

    # close the fieldset after getting all of the data types, then loop through clusters
    frmstr += '</div>\n'
    frmstr += '</fieldset>\n'

    if clu.clusters:
        for c in clu.clusters.all():
            frmstr += fcluster(c, indent)

    return(frmstr)

def fXd_boolean(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    choices = ['-------']
    for c in Xd.trues.splitlines():
        choices.append(c)
    for c in Xd.falses.splitlines():
        choices.append(c)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Choose  a value: <select name='mc-"+str(Xd.ct_id)+"'>\n"
    for c in choices:
        frmstr += indent + "  <option value='"+c+"' label='"+c+"'>"+c+"</option><br />\n"
    frmstr += indent + "</select><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_link(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter a URI: <input name='mc-"+str(Xd.ct_id)+":XdURI' type='text' size='30' value=''/>\n"
    frmstr += indent + " Relationship: <em>"+Xd.relation.strip()+"</em><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_string(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    a = None
    enumList = []

    x = None
    if Xd.def_val:
        s = Xd.def_val
    elif Xd.enums:
        enumList = []
        for e in Xd.enums.splitlines():
            enumList.append(escape(e))
        s = choice(enumList)
    elif Xd.asserts:
        #Example: matches(Xdstring-value, '^\d{5}([\-]?\d{3})$')
        try:
            x = Xd.asserts.replace("matches(Xdstring-value, '",'')[:-1].replace("'",'')
            s = exrex.getone(x)
        except:
            s = 'DefaultString'
    else:
        s = 'DefaultString'

    if Xd.enums:
        for e in Xd.enums.splitlines():
            enumList.append(escape(e))

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    if enumList:
        frmstr += indent + " Choose a value: <select name='mc-"+str(Xd.ct_id)+":Xdstring-value'>\n"
        for c in enumList:
            frmstr += indent + "  <option value='"+c+"' label='"+c+"'>"+c+"</option>\n"
        frmstr += indent + "</select><br />\n"
    else:
        frmstr += indent + " Enter a string: <input name='mc-"+str(Xd.ct_id)+":XdString' type='text' size='30' value='"+s+"'/>"
    if x:
        frmstr += indent + " Match (regex): "+x+"<br />\n"
    frmstr += indent + " Language: <input name='mc-"+str(Xd.ct_id)+":language' type='text' size='6' value='"+Xd.lang+"'/><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_count(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    if Xd.normal_status:
        ns = Xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if Xd.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in Xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    _min = None
    _max = None

    if Xd.min_inclusive:
        _min = Xd.min_inclusive
    if Xd.min_exclusive:
        _min = Xd.min_exclusive + 1
    if Xd.max_inclusive:
        _max = Xd.max_inclusive
    if Xd.max_exclusive:
        _max = Xd.max_exclusive - 1

    if not _max:
        _max = 999999
    if not _min:
        _min = -999999

    mag = randint(_min,_max)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter Count:  <input name='mc-"+str(Xd.ct_id)+":Xdcount-value' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='mc-"+str(Xd.ct_id)+":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='mc-"+str(Xd.ct_id)+":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='mc-"+str(Xd.ct_id)+":accuracy' type='number' value='0'/><br />\n"
    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + " Units:<br />\n"
    if Xd.units:
        frmstr += fXd_string(Xd.units, indent)+'<br />'

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_interval(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"
    frmstr += indent + "Lower Value: "+str(Xd.lower)+" Upper Value: "+str(Xd.upper)+"<br />\n"
    frmstr += indent + "Lower Included: "+str(Xd.lower_included)+" Upper Included: "+str(Xd.upper_included)+"<br />\n"
    frmstr += indent + "Lower Bounded: "+str(Xd.lower_bounded)+" Upper Bounded: "+str(Xd.upper_bounded)+"<br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_file(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"
    frmstr += indent + " Size (bytes):  <input name='mc-"+str(Xd.ct_id)+":size' type='number' value='0'/>\n"
    frmstr += indent + " Encoding: <input name='mc-"+str(Xd.ct_id)+":encoding' type='text' value='utf-8'/>\n"
    frmstr += indent + " Language:  <input name='mc-"+str(Xd.ct_id)+":language' type='text' value='"+Xd.lang+"'/><br />\n"
    frmstr += indent + " MIME Type: <input name='mc-"+str(Xd.ct_id)+":mime-type' type='text' value=''/>\n"
    frmstr += indent + " Compression Type: <input name='mc-"+str(Xd.ct_id)+":compression-type' type='text' value=''/><br />\n"
    frmstr += indent + " HASH Result: <input name='mc-"+str(Xd.ct_id)+":hash-result' type='text' value=''/>\n"
    frmstr += indent + " HASH Function: <input name='mc-"+str(Xd.ct_id)+":hash-function' type='text' value=''/><br />\n"
    frmstr += indent + " Alt. Text: <input name='mc-"+str(Xd.ct_id)+":alt-txt' type='text' value=''/><br />\n"
    if Xd.content_mode == 'url':
        frmstr += indent + " URL: <input name='mc-"+str(Xd.ct_id)+":uri' type='url' value=''/> (to content location)<br />\n"
    elif Xd.content_mode == 'binary':
        frmstr += indent + " Media Content: <br /><textarea name='mc-"+str(Xd.ct_id)+":media-content' type='text' value=''/> (paste base64Binary encoded content here)</textarea>\n"
        frmstr += "<b>OR</b> Select a file to upload: <input type='file' name='mc-"+str(Xd.ct_id)+":media-content' size='40' /><br /><br />\n"
    elif Xd.content_mode == 'text':
        frmstr += indent + " Text Content: <br /><textarea name='mc-"+str(Xd.ct_id)+":text-content' type='text' value=''/> (paste text content here)</textarea>\n"
        frmstr += "<b>OR</b> Select a file to upload: <input type='file' name='mc-"+str(Xd.ct_id)+":text-content'  size='40' /><br /><br />\n"
    else:
        frmstr += "<br /><b>An error in the model was detected and it doesn't allow a content mode.</b><br /><br />\n"

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_ordinal(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    if Xd.normal_status:
        ns = Xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if Xd.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in Xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent) + '<br />'

    o = []
    for a in Xd.ordinals.splitlines():
        o.append(escape(a).strip())

    s = []
    for a in Xd.symbols.splitlines():
        s.append(escape(a).strip())

    ann = []
    for x in Xd.annotations.splitlines():
        ann.append(escape(x).strip())

    ri = randint(0, len(o)-1) # get a random index

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"
    if s:
        frmstr += indent + " Choose a value: <select name='mc-"+str(Xd.ct_id)+":symbol'>\n"
        for c in s:
            frmstr += indent + "  <option value='"+c+"' label='"+c+"'>"+c+"</option>\n"
        frmstr += indent + "</select><br />\n"

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_quantity(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    if Xd.normal_status:
        ns = Xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if Xd.reference_ranges:
        rrstr += 'Reference Ranges:<br /> '
        for rr in Xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    ctx = BasicContext

    _min = None
    _max = None

    if Xd.total_digits:  # total digits
        ctx.prec = int(Xd.total_digits)

    if Xd.min_inclusive != None:
        _min = Xd.min_inclusive
    if Xd.min_exclusive != None:
        _min = Xd.min_exclusive + 1

    if Xd.max_inclusive != None:
        _max = Xd.max_inclusive
    if Xd.max_exclusive != None:
        _max = Xd.max_exclusive - 1

    if _max == None:
        _max = 999999999999999999999999999999999999999999
    if _min == None:
        _min = -99999999999999999999999999999999999999999

    f_min = float(_min)
    f_max = float(_max)

    fmag = uniform(f_min,f_max) # random float between min and max

    mag = ctx.create_decimal_from_float(fmag)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter Quantity:  <input name='mc-"+str(Xd.ct_id)+":magnitude' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='mc-"+str(Xd.ct_id)+":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='mc-"+str(Xd.ct_id)+":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='mc-"+str(Xd.ct_id)+":accuracy' type='number' value='0'/><br />\n"

    frmstr += indent + " Units:<br />\n"
    if Xd.units:
        frmstr += fXd_string(Xd.units, indent) + '<br />'

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_ratio(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="mc">\n'

    if Xd.normal_status:
        ns = Xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if Xd.reference_ranges:
        rrstr += 'Reference Ranges:<br /> '
        for rr in Xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    num_min = None
    num_max = None

    if Xd.num_min_inclusive:
        num_min = Xd.num_min_inclusive
    if Xd.num_min_exclusive:
        num_min = Xd.num_min_exclusive + 1
    if Xd.num_max_inclusive:
        num_max = Xd.num_max_inclusive
    if Xd.num_max_exclusive:
        num_max = Xd.max_exclusive - 1

    if not num_max:
        num_max = 999999
    if not num_min:
        num_min = -999999

    num = uniform(num_min,num_max) # random float

    den_min = None
    den_max = None

    if Xd.den_min_inclusive:
        den_min = Xd.den_min_inclusive
    if Xd.den_min_exclusive:
        den_min = Xd.den_min_exclusive + 1
    if Xd.den_max_inclusive:
        den_max = Xd.den_max_inclusive
    if Xd.den_max_exclusive:
        den_max = Xd.den_max_exclusive - 1

    if not den_max:
        den_max = 999999
    if not den_min:
        den_min = -999999

    den = uniform(den_min,den_max) # random float

    mag = num/den

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    frmstr += indent + " Enter Ratio (magnitude):  <input name='mc-"+str(Xd.ct_id)+":magnitude' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='mc-"+str(Xd.ct_id)+":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='mc-"+str(Xd.ct_id)+":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='mc-"+str(Xd.ct_id)+":accuracy' type='number' value='0'/><br />\n"
    frmstr += indent + " Ratio Type:  <select name='mc-"+str(Xd.ct_id)+":ratio-type'>\n"
    frmstr += indent + "  <option value='ratio'  label='Ratio'>Ratio</option>\n"
    frmstr += indent + "  <option value='proportion' label='Proportion'>Proportion</option>\n"
    frmstr += indent + "  <option value='rate' label='Rate'>Rate</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Numerator:  <input name='mc-"+str(Xd.ct_id)+":numerator' type='number' value='0'/>\n"
    frmstr += indent + " Denominator:  <input name='mc-"+str(Xd.ct_id)+":denominator' type='number' value='0'/><br />\n"

    frmstr += indent + "  Numerator Units:<br />\n"
    if Xd.num_units:
        frmstr += fXd_string(Xd.num_units, indent)

    frmstr += indent + "  Denominator Units:<br />\n"
    if Xd.den_units:
        frmstr += fXd_string(Xd.den_units, indent)

    frmstr += indent + "  Ratio Units: <br />\n"
    if Xd.ratio_units:
        frmstr += fXd_string(Xd.ratio_units, indent)

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr

def fXd_temporal(Xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(Xd.description) + "\n\n"  # tooltip
    if len(Xd.pred_obj.all()) != 0:
        link = Xd.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="mc">\n'

    if Xd.normal_status:
        ns = Xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if Xd.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in Xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    start = datetime.strptime('1/1/1970', '%m/%d/%Y')
    end = datetime.strptime('12/31/2020', '%m/%d/%Y')
    rdt = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    rdt2 = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
    dur = abs((rdt-rdt2).days)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+Xd.label.strip()+"</a><br /></span>\n"

    if Xd.allow_date:
        frmstr += indent + " Date:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-date' type='date' value=''/> (YYYY-MM-DD)<br />\n"
    if Xd.allow_time:
        frmstr += indent + " Time:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-time' type='time' value=''/> (HH:MM:SS)<br />\n"
    if Xd.allow_datetime:
        frmstr += indent + " Datetime:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-datetime' type='datetime-local' value=''/> (YYYY-MM-DDTHH:MM:SS)<br />\n"
    if Xd.allow_datetimestamp:
        frmstr += indent + " DatetimeStamp:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-datetime-stamp' type='datetimestamp' value=''/> (YYYY-MM-DDTHH:MM:SS)<br />\n"
    if Xd.allow_day:
        frmstr += indent + " Day:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-day' type='day' value=''/> (--DD)<br />\n"
    if Xd.allow_month:
        frmstr += indent + " Month:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-month' type='month' value=''/> (-MM)<br />\n"
    if Xd.allow_year:
        frmstr += indent + " Year:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-year' type='year' value=''/> (YYYY)<br />\n"
    if Xd.allow_year_month:
        frmstr += indent + " Year-Month:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-year-month' type='text' value=''/> (YYYY-MM)<br />\n"
    if Xd.allow_month_day:
        frmstr += indent + " Month-Day:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-month-day' type='text' value=''/> (-MM-DD)<br />\n"
    if Xd.allow_duration:
        frmstr += indent + " Duration:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-duration' type='text' value='P'/> (PxxYxxMxxDTxxHxxMxxS)<br />\n"
    if Xd.allow_ymduration:
        frmstr += indent + " Year-Month Duration:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-ymduration' type='text' value='P'/> (PxxYxxM)<br />\n"
    if Xd.allow_dtduration:
        frmstr += indent + " Day Time Duration:  <input name='mc-"+str(Xd.ct_id)+":Xdtemporal-dtduration' type='text' value='P'/> (PxDTxxHxxMxxS)<br />\n"

    frmstr += indent + " Normal:  "+ns.strip()+"<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(Xd.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(Xd.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fparty(pi, indent):
    tt = escape(pi.description) + "\n\n"  # tooltip
    if len(pi.pred_obj.all()) != 0:
        link = pi.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+pi.label+"</a><br /></span>\n"
    frmstr += indent + "Name: <input name='mc-"+str(pi.ct_id)+":Party' type='text' size='80'/><br/>\n"
    if pi.external_ref:
        for ref in pi.external_ref.all():
            frmstr += fXd_link(ref, indent)

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
    frmstr = indent + "<div id='"+str(p.ct_id)+"' class='mc'> \n"
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+p.label+"</a><br /></span>\n"
    if p.performer:
        frmstr += fparty(p.performer, indent)

    if p.function:
        frmstr += fXd_string(p.function, indent)

    if p.mode:
        frmstr += fXd_string(p.mode, indent)

    frmstr += indent + "  Start Time: <input name='mc-"+str(p.ct_id)+":start-time' type='datetime-local' value='"+vtb+"'/><br />\n"
    frmstr += indent + "  End Time: <input name='mc-"+str(p.ct_id)+":end-time' type='datetime-local' value='"+vte+"'/><br />\n"

    frmstr += indent + " </div>\n"

    return frmstr

def fattestation(a, indent):
    tt = escape(a.description) + "\n\n"  # tooltip
    if len(a.pred_obj.all()) != 0:
        link = a.pred_obj.all()[0].object_uri
    else:
        link = "#"

    indent += '  '
    frmstr = indent + "<div id='"+str(a.ct_id)+"' class='mc'> \n"
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+a.label+"</a><br /></span>\n"

    if a.view:
        frmstr += fXd_file(a.view, indent)

    if a.proof:
        frmstr += fXd_file(a.proof, indent)

    if a.reason:
        frmstr += fXd_string(a.reason, indent)

    if a.committer:
        frmstr += fparty(a.committer, indent)

    frmstr += indent + "  Time Committed: <input name='mc-"+str(a.ct_id)+":time-committed' type='datetime-local' value='"+datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')+"'/><br />\n"
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
    frmstr = indent + "<div id='"+str(aud.ct_id)+"' class='mc'> \n"
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+aud.label+"</a><br /></span>\n"

    if aud.system_id:
        frmstr += fXd_string(aud.system_id, indent)

    if aud.system_user:
        frmstr += fparty(aud.system_user, indent)

    if aud.location:
        frmstr += fcluster(aud.location, indent)

    frmstr += indent + "  Timestamp: <input name='mc-"+str(aud.ct_id)+":timestamp' type='datetime-local' value='"+datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')+"'/><br />\n"

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
    frmstr += '<div class="mc">\n'
    indent += '  '
    frmstr += indent + "<span class='label'><a href='"+link+"' title='"+tt+"' target='_blank'>"+rr.label.strip()+"</a><br /></span>\n"
    frmstr += indent + "ReferenceRange Definition: <b>"+rr.definition+"</b><br />\n"
    frmstr += fXd_interval(rr.interval, indent)
    if rr.is_normal:
        n = 'Yes'
    else:
        n = 'No'

    frmstr += indent + "Normal range: "+n+"<br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-"+str(rr.ct_id)+":vtb' type='datetime-local' value='"+vtb+"'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-"+str(rr.ct_id)+":vte' type='datetime-local' value='"+vte+"'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr
