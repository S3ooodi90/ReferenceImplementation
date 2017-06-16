"""
Return strings to build an HTML Form template
"""
from datetime import timedelta, datetime
from random import randint, choice
from xml.sax.saxutils import escape

import exrex


def random_dtstr(start=None, end=None):
    if not start:
        start = datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')

    if not end:
        end = datetime.strptime('2015-12-31', '%Y-%m-%d')
    rand_dts = datetime.strftime(
        start + timedelta(seconds=randint(0, int((end - start).total_seconds()))), '%Y-%m-%d %H:%M:%S')
    return rand_dts


def buildHTML(dm_pkg):
    """
    The CCD Package is sent from the generator, then returned after filling in the ccdPkg.html string.
    """

    entry = dm_pkg.dm.entry

    dm_pkg.html = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n  <head>'
    dm_pkg.html += '    <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">\n'
    dm_pkg.html += '    <title>' + dm_pkg.dm.title + '</title>\n'
    dm_pkg.html += ' <style type="text/css">\n'
    dm_pkg.html += ' legend {\n'
    dm_pkg.html += '   font-size: 16px;\n'
    dm_pkg.html += '   font-weight: bold;\n'
    dm_pkg.html += ' }\n'
    dm_pkg.html += ' .label {\n'
    dm_pkg.html += '   font-size: 12px;\n'
    dm_pkg.html += '   font-weight: bold;\n'
    dm_pkg.html += ' }\n'
    dm_pkg.html += ' .mc {\n'
    dm_pkg.html += '  margin-top: 10px; \n'
    dm_pkg.html += '  margin-bottom: 10px; \n'
    dm_pkg.html += '  margin-left: 10px; \n'
    dm_pkg.html += '  margin-right: 10px; \n'
    dm_pkg.html += '  padding: 5px; \n'
    dm_pkg.html += '  border-style: dotted; \n'
    dm_pkg.html += '  border-size: 6px; \n'
    dm_pkg.html += '  border-color: #009999; \n'
    dm_pkg.html += '}\n'
    dm_pkg.html += '.button_bar {\n'
    dm_pkg.html += '  text-align: center;\n'
    dm_pkg.html += '  border-radius: 15px;\n'
    dm_pkg.html += '  background-color: #005566;\n'
    dm_pkg.html += '  margin: 10px;\n'
    dm_pkg.html += '  padding: 10px;\n'
    dm_pkg.html += '}\n'
    dm_pkg.html += '.button_row {\n'
    dm_pkg.html += '  margin: auto;\n'
    dm_pkg.html += '  width: 60%;\n'
    dm_pkg.html += '  padding: 5px;\n'
    dm_pkg.html += '}\n'
    dm_pkg.html += '.button {\n'
    dm_pkg.html += '   border-top: 1px solid #96d1f8;\n'
    dm_pkg.html += '   background: #65a9d7;\n'
    dm_pkg.html += '   background: -webkit-gradient(linear, left top, left bottom, from(#3e779d), to(#65a9d7));\n'
    dm_pkg.html += '   background: -webkit-linear-gradient(top, #3e779d, #65a9d7);\n'
    dm_pkg.html += '   background: -moz-linear-gradient(top, #3e779d, #65a9d7);\n'
    dm_pkg.html += '   background: -ms-linear-gradient(top, #3e779d, #65a9d7);\n'
    dm_pkg.html += '   background: -o-linear-gradient(top, #3e779d, #65a9d7);\n'
    dm_pkg.html += '   padding: 5px 10px;\n'
    dm_pkg.html += '   margin-left 10px;\n'
    dm_pkg.html += '   -webkit-border-radius: 8px;\n'
    dm_pkg.html += '   -moz-border-radius: 8px;\n'
    dm_pkg.html += '   border-radius: 8px;\n'
    dm_pkg.html += '   -webkit-box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    dm_pkg.html += '   -moz-box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    dm_pkg.html += '   box-shadow: rgba(0,0,0,1) 0 1px 0;\n'
    dm_pkg.html += '   text-shadow: rgba(0,0,0,.4) 0 1px 0;\n'
    dm_pkg.html += '   color: white;\n'
    dm_pkg.html += '   font-size: 14px;\n'
    dm_pkg.html += '   font-family: Georgia, serif;\n'
    dm_pkg.html += '   text-decoration: none;\n'
    dm_pkg.html += '   vertical-align: middle;\n'
    dm_pkg.html += '   }\n'
    dm_pkg.html += '.button:hover {\n'
    dm_pkg.html += '   border-top-color: #28597a;\n'
    dm_pkg.html += '   background: #28597a;\n'
    dm_pkg.html += '   color: #ccc;\n'
    dm_pkg.html += '   }\n'
    dm_pkg.html += '.button:active {\n'
    dm_pkg.html += '   border-top-color: #1b435e;\n'
    dm_pkg.html += '   background: #1b435e;\n'
    dm_pkg.html += '   }\n'
    dm_pkg.html += '.subpage {\n'
    dm_pkg.html += '  text-align: left;\n'
    dm_pkg.html += '}\n'
    dm_pkg.html += '\n'
    dm_pkg.html += ' </style>\n'
    dm_pkg.html += ' </head>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '<body style="color: rgb(0, 0, 0); background-color: rgb(238, 239, 255);" alink="#349923" link="#000099" vlink="#990099">\n'
    dm_pkg.html += '<div class="" style="text-align: center;">\n'
    dm_pkg.html += '<h1 id="topOfPage">' + dm_pkg.dm.title + '</h1>\n'
    dm_pkg.html += '<div style="text-align: left;">\n'
    dm_pkg.html += '<form  id="' + \
        str(entry.ct_id) + '" action="" method="post" name="' + \
        entry.label + '" target="" >\n'
    dm_pkg.html += '<div class="button_bar">\n'
    dm_pkg.html += '<span class="button_row">\n'
    dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#subject'"> """ + \
        entry.subject.label + """ </button>\n"""
    dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#provider'"> """ + \
        entry.provider.label + """ </button>\n"""
    if entry.participations.all():
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#participants'"> """ + \
            'Other Participants' + """ </button>\n"""
    if entry.attestation:
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#attestation'"> """ + \
            entry.attestation.label + """ </button>\n"""
    if entry.audit.all():
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#audit'"> """ + \
            entry.audit.label + """ </button>\n"""
    if entry.links.all():
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#references'"> """ + \
            'References' + """ </button>\n"""
    if entry.workflow:
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#workflow'">Workflow - """ + \
            entry.workflow.label + """ </button>\n"""
    if entry.protocol:
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#protocol'">Protocol - """ + \
            entry.protocol.label + """ </button>\n"""
    dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#other'"> """ + \
        'Other Info' + """ </button>\n"""
    dm_pkg.html += '</span>\n'
    dm_pkg.html += '</div>\n'
    # process the PCMs in a cluster then iterate through the cluster levels
    # one at a time, coming back to the top until completed.
    dm_pkg.html += fcluster(entry.data, '  ')
    dm_pkg.html += '\n'
    dm_pkg.html += '<div style="font-size: 10px; text-align: center;">\n'
    dm_pkg.html += '<button class="button" type="submit" form="' + \
        str(entry.ct_id) + '" > Submit </button> \n'
    dm_pkg.html += '<button class="button" type="cancel" form="' + \
        str(entry.ct_id) + '" > Cancel </button>\n'
    dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '</form>\n'
    dm_pkg.html += '</div>\n'
    dm_pkg.html += '<div>\n'
    dm_pkg.html += '</div>\n'
    dm_pkg.html += '<div id="subject" class="subpage">\n'
    dm_pkg.html += '<hr/>\n'
    dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    dm_pkg.html += '<form  id="' + \
        str(entry.subject.ct_id) + '" action="" method="post" name="' + \
        entry.subject.label + '" target="" >\n'
    dm_pkg.html += fparty(entry.subject, '  ')
    dm_pkg.html += '</form>\n'
    dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '<div id="provider" class="subpage">\n'
    dm_pkg.html += '<hr/>\n'
    dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    dm_pkg.html += '<form  id="' + \
        str(entry.provider.ct_id) + '" action="" method="post" name="' + \
        entry.provider.label + '" target="" >\n'
    dm_pkg.html += fparty(entry.provider, '  ')
    dm_pkg.html += '</form>\n'
    dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    if entry.participations.all():
        dm_pkg.html += '<div id="participants" class="subpage">\n'
        dm_pkg.html += '<hr/>\n'
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        for p in entry.participations.all():
            dm_pkg.html += fparticipation(p, '  ')
        dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    if entry.attestation:
        dm_pkg.html += '<div id="attestation" class="subpage">\n'
        dm_pkg.html += '<hr/>\n'
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dm_pkg.html += fattestation(entry.attestation, '  ')
        dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    if entry.audit.all():
        dm_pkg.html += '<div id="audit" class="subpage">\n'
        dm_pkg.html += '<hr/>\n'
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        for a in entry.audit.all():
            dm_pkg.html += faudit(a, '  ')
        dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    if entry.links.all():
        dm_pkg.html += '<div id="references" class="subpage">\n'
        dm_pkg.html += '<hr/>\n'
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dm_pkg.html += 'Reference Links:\n'
        for e in entry.links.all():
            dm_pkg.html += fXd_link(e, '  ')
        dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    if entry.workflow:
        dm_pkg.html += '<div id="workflow" class="subpage">\n'
        dm_pkg.html += '<hr/>\n'
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dm_pkg.html += '<br/>Link to workflow engine:\n'
        dm_pkg.html += fXd_link(entry.workflow, '  ')
        dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    if entry.protocol:
        dm_pkg.html += '<div id="protocol" class="subpage">\n'
        dm_pkg.html += '<hr/>\n'
        dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
        dm_pkg.html += '<br/>Protocol definition:\n'
        dm_pkg.html += fXd_string(entry.protocol, '  ')
        dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '<div id="other" class="subpage">\n'
    dm_pkg.html += '<hr/>\n'
    dm_pkg.html += """<button class="button" type="button" onClick="parent.location='#topOfPage'">Top</button>\n"""
    dm_pkg.html += '<h3>Other Information</h3>\n'
    dm_pkg.html += 'Language: ' + entry.language + '<br/>\n'
    dm_pkg.html += 'Current State: ' + entry.state + '<br/>\n'
    dm_pkg.html += 'Encoding: ' + entry.encoding + '<br/>\n'
    dm_pkg.html += '<h3>Model Information</h3>\n'
    dm_pkg.html += '<p>Description: <br/> ' + dm_pkg.dm.description + '</p>\n'
    dm_pkg.html += '<p>Author: ' + dm_pkg.dm.author.__str__() + '</p>\n'
    if dm_pkg.dm.contrib.all():
        dm_pkg.html += '<p>Contributors: <br/>\n'
        for c in dm_pkg.dm.contrib.all():
            dm_pkg.html += c.__str__() + '<br/>\n'
        dm_pkg.html += '</p>\n'
    dm_pkg.html += '<p>Keywords: ' + dm_pkg.dm.subject + '</p>\n'
    dm_pkg.html += '<p>Source Reference: ' + dm_pkg.dm.source + '</p>\n'
    dm_pkg.html += '<p>Relation to another model: ' + dm_pkg.dm.relation + '</p>\n'
    dm_pkg.html += '<p>Coverage: ' + dm_pkg.dm.coverage + '</p>\n'
    dm_pkg.html += '<p>Publisher: ' + dm_pkg.dm.publisher + '</p>\n'
    dm_pkg.html += '<p>License: ' + dm_pkg.dm.rights + '</p>\n'
    dm_pkg.html += '<p>Publication Date: ' + str(dm_pkg.dm.pub_date) + '</p>\n'
    dm_pkg.html += '<p>Language: ' + dm_pkg.dm.dc_language + '</p>\n'
    dm_pkg.html += '<p>Top level RDF: <br/><code> <pre>&lt;rdf:Description rdf:about="https://www.s3model.com/ns/s3m/dm-' + \
        str(dm_pkg.dm.ct_id) + '"/&gt;<br/>\n'
    dm_pkg.html += '  &lt;rdfs:subClassOf rdf:resource="s3m:CCDType"/&gt;<br/>\n'
    dm_pkg.html += '  &lt;rdfs:label&gt;' + \
        dm_pkg.dm.title + '&lt;/rdfs:label&gt;<br/>\n'
    if len(dm_pkg.dm.pred_obj.all()) != 0:
        for po in dm_pkg.dm.pred_obj.all():
            dm_pkg.html += "&lt;" + po.predicate.ns_abbrev.__str__() + ":" + po.predicate.class_name.strip() + \
                " rdf:resource='" + po.object_uri + "'/&gt;<br/>\n"
    dm_pkg.html += '&lt;/rdf:Description&gt;</pre></code><br/>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '</p>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '</div>\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '\n'
    dm_pkg.html += '<span style="font-size: 10px; text-align: center;">\n'
    dm_pkg.html += 'Generated by the <a href="http://dmgen.s3model.com" target="_blank">DMGen</a> \n'
    dm_pkg.html += '</span>\n'

    dm_pkg.html += '    </div>\n  </body>\n</html>'

    return(dm_pkg)


def fcluster(clu, indent):
    indent += '  '
#     if len(clu.pred_obj.all()) != 0:
#         link = clu.pred_obj.all()[0].object_uri
#     else:
#         link = "#"

    frmstr = ''
    frmstr += '<fieldset><legend>' + clu.label + '</legend><br/>\n'
    frmstr += '<div>\n'

    if clu.xdstring:
        for Xd in clu.xdstring.all():
            frmstr += fXd_string(Xd, indent + '  ')

    if clu.xdboolean:
        for Xd in clu.xdboolean.all():
            frmstr += fXd_boolean(Xd, indent + '  ')

    if clu.xdlink:
        for Xd in clu.xdlink.all():
            frmstr += fXd_link(Xd, indent + '  ')

    if clu.xdfile:
        for Xd in clu.xdfile.all():
            frmstr += fXd_file(Xd, indent + '  ')

    if clu.xdordinal:
        for Xd in clu.xdordinal.all():
            frmstr += fXd_ordinal(Xd, indent + '  ')

    if clu.xdcount:
        for Xd in clu.xdcount.all():
            frmstr += fXd_count(Xd, indent + '  ')

    if clu.xdquantity:
        for Xd in clu.xdquantity.all():
            frmstr += fXd_quantity(Xd, indent + '  ')

    if clu.xdratio:
        for Xd in clu.xdratio.all():
            frmstr += fXd_ratio(Xd, indent + '  ')

    if clu.xdtemporal:
        for Xd in clu.xdtemporal.all():
            frmstr += fXd_temporal(Xd, indent + '  ')

    # close the fieldset after getting all of the data types, then loop
    # through clusters
    frmstr += '</div>\n'
    frmstr += '</fieldset>\n'

    if clu.clusters:
        for c in clu.clusters.all():
            frmstr += fcluster(c, indent)

    return(frmstr)


def fXd_boolean(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    choices = ['-------']
    for c in xd.trues.splitlines():
        choices.append(c)
    for c in xd.falses.splitlines():
        choices.append(c)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    frmstr += indent + " Choose  a value: <select name='mc-" + \
        str(xd.ct_id) + "'>\n"
    for c in choices:
        frmstr += indent + "  <option value='" + c + \
            "' label='" + c + "'>" + c + "</option><br />\n"
    frmstr += indent + "</select><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_link(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    frmstr += indent + " Enter a URI: <input name='mc-" + \
        str(xd.ct_id) + ":XdURI' type='text' size='30' value=''/>\n"
    frmstr += indent + " Relationship: <em>" + xd.relation.strip() + "</em><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_string(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    enum_list = []

    x = None
    if xd.def_val:
        s = xd.def_val
    elif xd.enums:
        enum_list = []
        for e in xd.enums.splitlines():
            enum_list.append(escape(e))
        s = choice(enum_list)
    elif xd.asserts:
        # Example: matches(Xdstring-value, '^\d{5}([\-]?\d{3})$')
        try:
            x = xd.asserts.replace(
                "matches(Xdstring-value, '", '')[:-1].replace("'", '')
            s = exrex.getone(x)
        except:
            s = 'DefaultString'
    else:
        s = 'DefaultString'

    if xd.enums:
        for e in xd.enums.splitlines():
            enum_list.append(escape(e))

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    if enum_list:
        frmstr += indent + " Choose a value: <select name='mc-" + \
            str(xd.ct_id) + ":Xdstring-value'>\n"
        for c in enum_list:
            frmstr += indent + "  <option value='" + c + \
                "' label='" + c + "'>" + c + "</option>\n"
        frmstr += indent + "</select><br />\n"
    else:
        frmstr += indent + " Enter a string: <input name='mc-" + \
            str(xd.ct_id) + ":XdString' type='text' size='30' value='" + s + "'/>"
    if x:
        frmstr += indent + " Match (regex): " + x + "<br />\n"
    frmstr += indent + " Language: <input name='mc-" + \
        str(xd.ct_id) + ":language' type='text' size='6' value='" + \
        xd.lang + "'/><br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_count(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    if xd.normal_status:
        ns = xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if xd.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

    _min = None
    _max = None

    if xd.min_inclusive:
        _min = xd.min_inclusive
    if xd.min_exclusive:
        _min = xd.min_exclusive + 1
    if xd.max_inclusive:
        _max = xd.max_inclusive
    if xd.max_exclusive:
        _max = xd.max_exclusive - 1

    if not _max:
        _max = 999999
    if not _min:
        _min = -999999

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    frmstr += indent + " Enter Count:  <input name='mc-" + \
        str(xd.ct_id) + ":Xdcount-value' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='mc-" + \
        str(xd.ct_id) + ":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + \
        "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + \
        "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='mc-" + \
        str(xd.ct_id) + ":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='mc-" + \
        str(xd.ct_id) + ":accuracy' type='number' value='0'/><br />\n"
    frmstr += indent + " Normal:  " + ns.strip() + "<br />\n"
    frmstr += rrstr

    frmstr += indent + " Units:<br />\n"
    if xd.units:
        frmstr += fXd_string(xd.units, indent) + '<br />'

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_interval(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"
    frmstr += indent + "Lower Value: " + \
        str(xd.lower) + " Upper Value: " + str(xd.upper) + "<br />\n"
    frmstr += indent + "Lower Included: " + \
        str(xd.lower_included) + " Upper Included: " + \
        str(xd.upper_included) + "<br />\n"
    frmstr += indent + "Lower Bounded: " + \
        str(xd.lower_bounded) + " Upper Bounded: " + \
        str(xd.upper_bounded) + "<br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_file(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"
    frmstr += indent + " Size (bytes):  <input name='mc-" + \
        str(xd.ct_id) + ":size' type='number' value='0'/>\n"
    frmstr += indent + " Encoding: <input name='mc-" + \
        str(xd.ct_id) + ":encoding' type='text' value='utf-8'/>\n"
    frmstr += indent + " Language:  <input name='mc-" + \
        str(xd.ct_id) + ":language' type='text' value='" + \
        xd.lang + "'/><br />\n"
    frmstr += indent + " MIME Type: <input name='mc-" + \
        str(xd.ct_id) + ":mime-type' type='text' value=''/>\n"
    frmstr += indent + " Compression Type: <input name='mc-" + \
        str(xd.ct_id) + ":compression-type' type='text' value=''/><br />\n"
    frmstr += indent + " HASH Result: <input name='mc-" + \
        str(xd.ct_id) + ":hash-result' type='text' value=''/>\n"
    frmstr += indent + " HASH Function: <input name='mc-" + \
        str(xd.ct_id) + ":hash-function' type='text' value=''/><br />\n"
    frmstr += indent + " Alt. Text: <input name='mc-" + \
        str(xd.ct_id) + ":alt-txt' type='text' value=''/><br />\n"
    if xd.content_mode == 'url':
        frmstr += indent + " URL: <input name='mc-" + \
            str(xd.ct_id) + ":uri' type='url' value=''/> (to content location)<br />\n"
    elif xd.content_mode == 'binary':
        frmstr += indent + " Media Content: <br /><textarea name='mc-" + \
            str(xd.ct_id) + ":media-content' type='text' value=''/> (paste base64Binary encoded content here)</textarea>\n"
        frmstr += "<b>OR</b> Select a file to upload: <input type='file' name='mc-" + \
            str(xd.ct_id) + ":media-content' size='40' /><br /><br />\n"
    elif xd.content_mode == 'text':
        frmstr += indent + " Text Content: <br /><textarea name='mc-" + \
            str(xd.ct_id) + ":text-content' type='text' value=''/> (paste text content here)</textarea>\n"
        frmstr += "<b>OR</b> Select a file to upload: <input type='file' name='mc-" + \
            str(xd.ct_id) + ":text-content'  size='40' /><br /><br />\n"
    else:
        frmstr += "<br /><b>An error in the model was detected and it doesn't allow a content mode.</b><br /><br />\n"

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_ordinal(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    if xd.normal_status:
        ns = xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if xd.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent) + '<br />'

    o = []
    for a in xd.ordinals.splitlines():
        o.append(escape(a).strip())

    s = []
    for a in xd.symbols.splitlines():
        s.append(escape(a).strip())

    ann = []
    for x in xd.annotations.splitlines():
        ann.append(escape(x).strip())

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"
    if s:
        frmstr += indent + " Choose a value: <select name='mc-" + \
            str(xd.ct_id) + ":symbol'>\n"
        for c in s:
            frmstr += indent + "  <option value='" + c + \
                "' label='" + c + "'>" + c + "</option>\n"
        frmstr += indent + "</select><br />\n"

    frmstr += indent + " Normal:  " + ns.strip() + "<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_quantity(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"
    frmstr = ""
    frmstr += '<div class="mc">\n'

    if xd.normal_status:
        ns = xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if xd.reference_ranges:
        rrstr += 'Reference Ranges:<br /> '
        for rr in xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

#     ctx = BasicContext

#     _min = None
#     _max = None
#
#     if Xd.total_digits:  # total digits
#         ctx.prec = int(Xd.total_digits)
#
#     if Xd.min_inclusive is not None:
#         _min = Xd.min_inclusive
#     if Xd.min_exclusive is not None:
#         _min = Xd.min_exclusive + 1
#
#     if Xd.max_inclusive is not None:
#         _max = Xd.max_inclusive
#     if Xd.max_exclusive is not None:
#         _max = Xd.max_exclusive - 1
#
#     if _max is None:
#         _max = 999999999999999999999999999999999999999999
#     if _min is None:
#         _min = -99999999999999999999999999999999999999999
#
#     f_min = float(_min)
#     f_max = float(_max)
#
#     fmag = uniform(f_min, f_max)  # random float between min and max
#
#     mag = ctx.create_decimal_from_float(fmag)

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    frmstr += indent + " Enter Quantity:  <input name='mc-" + \
        str(xd.ct_id) + ":magnitude' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='mc-" + \
        str(xd.ct_id) + ":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + \
        "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + \
        "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='mc-" + \
        str(xd.ct_id) + ":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='mc-" + \
        str(xd.ct_id) + ":accuracy' type='number' value='0'/><br />\n"

    frmstr += indent + " Units:<br />\n"
    if xd.units:
        frmstr += fXd_string(xd.units, indent) + '<br />'

    frmstr += indent + " Normal:  " + ns.strip() + "<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_ratio(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="mc">\n'

    if xd.normal_status:
        ns = xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if xd.reference_ranges:
        rrstr += 'Reference Ranges:<br /> '
        for rr in xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

#     num_min = None
#     num_max = None
#
#     if Xd.num_min_inclusive:
#         num_min = Xd.num_min_inclusive
#     if Xd.num_min_exclusive:
#         num_min = Xd.num_min_exclusive + 1
#     if Xd.num_max_inclusive:
#         num_max = Xd.num_max_inclusive
#     if Xd.num_max_exclusive:
#         num_max = Xd.max_exclusive - 1
#
#     if not num_max:
#         num_max = 999999
#     if not num_min:
#         num_min = -999999
#
#     num = uniform(num_min, num_max)  # random float
#
#     den_min = None
#     den_max = None
#
#     if Xd.den_min_inclusive:
#         den_min = Xd.den_min_inclusive
#     if Xd.den_min_exclusive:
#         den_min = Xd.den_min_exclusive + 1
#     if Xd.den_max_inclusive:
#         den_max = Xd.den_max_inclusive
#     if Xd.den_max_exclusive:
#         den_max = Xd.den_max_exclusive - 1
#
#     if not den_max:
#         den_max = 999999
#     if not den_min:
#         den_min = -999999
#
#     den = uniform(den_min, den_max)  # random float

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    frmstr += indent + " Enter Ratio (magnitude):  <input name='mc-" + \
        str(xd.ct_id) + ":magnitude' type='number' />\n"
    frmstr += indent + " Magnitude Status:  <select name='mc-" + \
        str(xd.ct_id) + ":magnitude-status'>\n"
    frmstr += indent + "  <option value='='  label='Magnitude is exactly.'>=</option>\n"
    frmstr += indent + \
        "  <option value='<=' label='Magnitude is less than or equal to'><=</option>\n"
    frmstr += indent + \
        "  <option value='=>' label='Magnitude is greater than or equal to'>=></option>\n"
    frmstr += indent + "  <option value='<'  label='Magnitude is less than.'><</option>\n"
    frmstr += indent + "  <option value='>'  label='Magnitude is greater than.'>></option>\n"
    frmstr += indent + "  <option value='~'  label='Magnitude is approximately.'>~</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Error:  <input name='mc-" + \
        str(xd.ct_id) + ":error' type='number' value='0'/>\n"
    frmstr += indent + " Accuracy:  <input name='mc-" + \
        str(xd.ct_id) + ":accuracy' type='number' value='0'/><br />\n"
    frmstr += indent + " Ratio Type:  <select name='mc-" + \
        str(xd.ct_id) + ":ratio-type'>\n"
    frmstr += indent + "  <option value='ratio'  label='Ratio'>Ratio</option>\n"
    frmstr += indent + "  <option value='proportion' label='Proportion'>Proportion</option>\n"
    frmstr += indent + "  <option value='rate' label='Rate'>Rate</option>\n"
    frmstr += indent + " </select><br />\n"
    frmstr += indent + " Numerator:  <input name='mc-" + \
        str(xd.ct_id) + ":numerator' type='number' value='0'/>\n"
    frmstr += indent + " Denominator:  <input name='mc-" + \
        str(xd.ct_id) + ":denominator' type='number' value='0'/><br />\n"

    frmstr += indent + "  Numerator Units:<br />\n"
    if xd.num_units:
        frmstr += fXd_string(xd.num_units, indent)

    frmstr += indent + "  Denominator Units:<br />\n"
    if xd.den_units:
        frmstr += fXd_string(xd.den_units, indent)

    frmstr += indent + "  Ratio Units: <br />\n"
    if xd.ratio_units:
        frmstr += fXd_string(xd.ratio_units, indent)

    frmstr += indent + " Normal:  " + ns.strip() + "<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr


def fXd_temporal(xd, indent):
    vtb = random_dtstr()
    vte = random_dtstr(start=vtb)

    tt = escape(xd.description) + "\n\n"  # tooltip
    if len(xd.pred_obj.all()) != 0:
        link = xd.pred_obj.all()[0].object_uri
    else:
        link = "#"

    frmstr = ""
    frmstr += '<div class="mc">\n'

    if xd.normal_status:
        ns = xd.normal_status
    else:
        ns = '(not defined)'

    rrstr = indent + ''
    if xd.reference_ranges:
        rrstr += 'Reference Ranges: <br />'
        for rr in xd.reference_ranges.all():
            rrstr += indent + freferencerange(rr, indent)

#     start = datetime.strptime('1/1/1970', '%m/%d/%Y')
#     end = datetime.strptime('12/31/2020', '%m/%d/%Y')
#     rdt = start + \
#         timedelta(seconds=randint(0, int((end - start).total_seconds())))
#     rdt2 = start + \
#         timedelta(seconds=randint(0, int((end - start).total_seconds())))

    indent += '  '
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + xd.label.strip() + "</a><br /></span>\n"

    if xd.allow_date:
        frmstr += indent + " Date:  <input name='mc-" + \
            str(xd.ct_id) + \
            ":Xdtemporal-date' type='date' value=''/> (YYYY-MM-DD)<br />\n"
    if xd.allow_time:
        frmstr += indent + " Time:  <input name='mc-" + \
            str(xd.ct_id) + \
            ":Xdtemporal-time' type='time' value=''/> (HH:MM:SS)<br />\n"
    if xd.allow_datetime:
        frmstr += indent + " Datetime:  <input name='mc-" + \
            str(xd.ct_id) + ":Xdtemporal-datetime' type='datetime-local' value=''/> (YYYY-MM-DDTHH:MM:SS)<br />\n"
    if xd.allow_datetimestamp:
        frmstr += indent + " DatetimeStamp:  <input name='mc-" + \
            str(xd.ct_id) + ":Xdtemporal-datetime-stamp' type='datetimestamp' value=''/> (YYYY-MM-DDTHH:MM:SS)<br />\n"
    if xd.allow_day:
        frmstr += indent + " Day:  <input name='mc-" + \
            str(xd.ct_id) + ":Xdtemporal-day' type='day' value=''/> (--DD)<br />\n"
    if xd.allow_month:
        frmstr += indent + " Month:  <input name='mc-" + \
            str(xd.ct_id) + ":Xdtemporal-month' type='month' value=''/> (-MM)<br />\n"
    if xd.allow_year:
        frmstr += indent + " Year:  <input name='mc-" + \
            str(xd.ct_id) + ":Xdtemporal-year' type='year' value=''/> (YYYY)<br />\n"
    if xd.allow_year_month:
        frmstr += indent + " Year-Month:  <input name='mc-" + \
            str(xd.ct_id) + \
            ":Xdtemporal-year-month' type='text' value=''/> (YYYY-MM)<br />\n"
    if xd.allow_month_day:
        frmstr += indent + " Month-Day:  <input name='mc-" + \
            str(xd.ct_id) + \
            ":Xdtemporal-month-day' type='text' value=''/> (-MM-DD)<br />\n"
    if xd.allow_duration:
        frmstr += indent + " Duration:  <input name='mc-" + \
            str(xd.ct_id) + ":Xdtemporal-duration' type='text' value='P'/> (PxxYxxMxxDTxxHxxMxxS)<br />\n"
    if xd.allow_ymduration:
        frmstr += indent + " Year-Month Duration:  <input name='mc-" + \
            str(xd.ct_id) + \
            ":Xdtemporal-ymduration' type='text' value='P'/> (PxxYxxM)<br />\n"
    if xd.allow_dtduration:
        frmstr += indent + " Day Time Duration:  <input name='mc-" + \
            str(xd.ct_id) + \
            ":Xdtemporal-dtduration' type='text' value='P'/> (PxDTxxHxxMxxS)<br />\n"

    frmstr += indent + " Normal:  " + ns.strip() + "<br />\n"
    frmstr += rrstr

    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(xd.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(xd.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
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
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + pi.label + "</a><br /></span>\n"
    frmstr += indent + "Name: <input name='mc-" + \
        str(pi.ct_id) + ":Party' type='text' size='80'/><br/>\n"
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
    frmstr = indent + "<div id='" + str(p.ct_id) + "' class='mc'> \n"
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + p.label + "</a><br /></span>\n"
    if p.performer:
        frmstr += fparty(p.performer, indent)

    if p.function:
        frmstr += fXd_string(p.function, indent)

    if p.mode:
        frmstr += fXd_string(p.mode, indent)

    frmstr += indent + "  Start Time: <input name='mc-" + \
        str(p.ct_id) + ":start-time' type='datetime-local' value='" + \
        vtb + "'/><br />\n"
    frmstr += indent + "  End Time: <input name='mc-" + \
        str(p.ct_id) + ":end-time' type='datetime-local' value='" + \
        vte + "'/><br />\n"

    frmstr += indent + " </div>\n"

    return frmstr


def fattestation(a, indent):
    tt = escape(a.description) + "\n\n"  # tooltip
    if len(a.pred_obj.all()) != 0:
        link = a.pred_obj.all()[0].object_uri
    else:
        link = "#"

    indent += '  '
    frmstr = indent + "<div id='" + str(a.ct_id) + "' class='mc'> \n"
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + a.label + "</a><br /></span>\n"

    if a.view:
        frmstr += fXd_file(a.view, indent)

    if a.proof:
        frmstr += fXd_file(a.proof, indent)

    if a.reason:
        frmstr += fXd_string(a.reason, indent)

    if a.committer:
        frmstr += fparty(a.committer, indent)

    frmstr += indent + "  Time Committed: <input name='mc-" + \
        str(a.ct_id) + ":time-committed' type='datetime-local' value='" + \
        datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M') + "'/><br />\n"
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
    frmstr = indent + "<div id='" + str(aud.ct_id) + "' class='mc'> \n"
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + aud.label + "</a><br /></span>\n"

    if aud.system_id:
        frmstr += fXd_string(aud.system_id, indent)

    if aud.system_user:
        frmstr += fparty(aud.system_user, indent)

    if aud.location:
        frmstr += fcluster(aud.location, indent)

    frmstr += indent + "  Timestamp: <input name='mc-" + \
        str(aud.ct_id) + ":timestamp' type='datetime-local' value='" + \
        datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M') + "'/><br />\n"

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
    frmstr += indent + "<span class='label'><a href='" + link + "' title='" + \
        tt + "' target='_blank'>" + rr.label.strip() + "</a><br /></span>\n"
    frmstr += indent + "ReferenceRange Definition: <b>" + rr.definition + "</b><br />\n"
    frmstr += fXd_interval(rr.interval, indent)
    if rr.is_normal:
        n = 'Yes'
    else:
        n = 'No'

    frmstr += indent + "Normal range: " + n + "<br />\n"
    frmstr += indent + "<span> Begin Valid Time:  <input name='mc-" + \
        str(rr.ct_id) + ":vtb' type='datetime-local' value='" + vtb + "'/>\n"
    frmstr += indent + " End Valid Time: <input name='mc-" + \
        str(rr.ct_id) + ":vte' type='datetime-local' value='" + \
        vte + "'/><br /></span>\n"
    frmstr += '</div>\n'

    return frmstr
