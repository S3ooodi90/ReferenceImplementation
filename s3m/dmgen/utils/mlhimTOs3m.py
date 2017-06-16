import psycopg2

print("\n\nPreparing to copy ccdgen DB records to miansanon DB")

MLHIM = psycopg2.connect("dbname=ccdgen user=tim password=cl!pper5")
S3M = psycopg2.connect("dbname=miansanon user=tim password=cl!pper5")
S3M.autocommit = True

print("Cleaning the ccdgen DB")
curMLHIM = MLHIM.cursor()
isolevel = MLHIM.isolation_level
MLHIM.set_isolation_level(0)
curMLHIM.execute("VACUUM FULL ANALYZE")
MLHIM.set_isolation_level(isolevel)

curS3M = S3M.cursor()

# Users & Groups
print("Adding Users and Groups")
curMLHIM.execute("SELECT *  from auth_user")
rowsMLHIM = curMLHIM.fetchall()
data = []
mdata = []
for line in rowsMLHIM:
    pk = line[0]
    pw = line[1]
    last = line[2]
    issuper = line[3]
    uname = line[4]
    first = line[5]
    lastname = line[6]
    email = line[7]
    staff = line[8]
    active = line[9]
    joined = line[10]
    data.append((pk, pw, last, issuper, uname, first,
                 lastname, email, staff, active, joined))
    if staff:
        mdata.append((pk, pk, lastname, email))

query = ("""INSERT INTO auth_user (id,password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined)
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from auth_group")
rowsMLHIM = curMLHIM.fetchall()
data = []
mdata = []
for line in rowsMLHIM:
    pk = line[0]
    name = line[1]
    data.append((pk, name))

query = ("""INSERT INTO auth_group (id,name)
               VALUES(%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

# Projects
print("Adding Projects")
curMLHIM.execute("SELECT *  from ccdgen_project")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    name = line[1]
    descr = line[2]
    data.append((pk, name, descr))

query = ("INSERT INTO dmgen_project (id,prj_name,description) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# Modelers
print("Adding Modelers")
curMLHIM.execute("SELECT *  from ccdgen_modeler")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    name = line[1]
    email = line[2]
    prjfilter = line[3]
    prjid = line[4]
    userid = line[5]
    if name == 'admin':
        adminpk = pk

    data.append((pk, userid, name, email, prjid, prjfilter))

query = ("INSERT INTO dmgen_modeler (id,user_id,name,email,project_id,prj_filter) VALUES(%s,%s,%s,%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# NS, Predicates and PredObjs
print("Adding NS, Predicates and PredObjs")
curMLHIM.execute("SELECT *  from ccdgen_ns")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    abbrev = line[1]
    uri = line[2]
    data.append((pk, abbrev, uri))

query = ("INSERT INTO dmgen_ns (id,abbrev,uri) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_predicate")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    class_name = line[1]
    ns_abbrev_id = line[2]
    data.append((pk, ns_abbrev_id, class_name))

query = ("INSERT INTO dmgen_predicate (id,ns_abbrev_id,class_name) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_predobj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    po_name = line[1]
    obj_uri = line[2]
    pred_id = line[3]
    prj_id = line[4]
    data.append((pk, po_name, obj_uri, pred_id, prj_id))

query = ("INSERT INTO dmgen_predobj (id,po_name,object_uri,predicate_id,project_id) VALUES(%s,%s,%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdBoolean
print("Adding XdBooleans")
curMLHIM.execute("SELECT *  from ccdgen_dvboolean")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    trues = line[12]
    falses = line[13]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[16]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 ad_ctid, False, False, False, False,
                 trues, falses, ''))

query = ("""INSERT INTO dmgen_xdboolean
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              trues,falses,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvboolean_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdboolean_pred_obj (id,xdboolean_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdStrings
print("Adding XdStrings")
curMLHIM.execute("SELECT *  from ccdgen_dvstring")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    min_len = line[12]
    max_len = line[13]
    exact_len = line[14]
    enums = line[15]
    eanno = line[16]
    def_val = line[17]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[20]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 min_len, max_len, exact_len, enums, eanno, def_val, ''))

query = ("""INSERT INTO dmgen_xdstring
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              min_length,max_length,exact_length,enums,definitions,def_val,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
             %s,%s,%s,%s,%s,%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvstring_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdstring_pred_obj (id,xdstring_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# Units
print("Adding Units")
curMLHIM.execute("SELECT *  from ccdgen_units")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    min_len = line[12]
    max_len = line[13]
    exact_len = line[14]
    enums = line[15]
    def_val = line[16]
    eanno = line[17]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[20]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,  min_len, max_len, exact_len, enums, eanno, def_val, ''))

query = ("""INSERT INTO dmgen_units
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              min_length,max_length,exact_length,enums,definitions,def_val,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
             %s,%s,%s,%s,%s,%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_units_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_units_pred_obj (id,units_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# XdIntervals
print("Adding XdIntervals")
curMLHIM.execute("SELECT *  from ccdgen_dvinterval")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    lower = line[12]
    upper = line[13]
    invl_type = line[14]
    li = line[15]
    ui = line[16]
    lb = line[17]
    ub = line[18]
    uname = line[19]
    uuri = line[20]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[23]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 lower, upper, invl_type, li, ui, lb, ub, uname, uuri, ''))

query = ("""INSERT INTO dmgen_xdinterval
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              lower,upper,interval_type,lower_included,upper_included,lower_bounded,upper_bounded,units_name,units_uri,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
             %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvinterval_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdinterval_pred_obj (id,xdinterval_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# ReferenceRanges
print("Adding ReferenceRanges")
curMLHIM.execute("SELECT *  from ccdgen_referencerange")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    defn = line[12]
    is_norm = line[13]
    creator_id = adminpk
    edited_by = adminpk
    interval_id = line[16]
    prj = line[17]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 defn, interval_id, is_norm, ''))

query = ("""INSERT INTO dmgen_referencerange
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              definition,interval_id,is_normal,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_referencerange_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_referencerange_pred_obj (id,referencerange_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# XdLinks
print("Adding XdLinks")
curMLHIM.execute("SELECT *  from ccdgen_dvlink")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    relation = line[12]
    rel_uri = line[13]

    creator_id = adminpk
    edited_by = adminpk
    prj = line[16]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 relation, rel_uri, ''))

query = ("""INSERT INTO dmgen_xdlink
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              relation,relation_uri,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvlink_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdlink_pred_obj (id,xdlink_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdFiles
print("Adding XdFiles")
curMLHIM.execute("SELECT *  from ccdgen_dvfile")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    mime = line[12]
    encoding = line[13]
    cont_lang = line[14]
    alt_txt = line[15]
    cm = line[16]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[19]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 mime, encoding, cont_lang, alt_txt, cm, ''))

query = ("""INSERT INTO dmgen_xdfile
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              media_type,encoding,language,alt_txt,content_mode,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvfile_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdfile_pred_obj (id,xdfile_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdTemporals
print("Adding XdTemporals")
curMLHIM.execute("SELECT *  from ccdgen_dvtemporal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    normal_status = line[12]
    allow_duration = line[13]
    allow_ymduration = line[14]
    allow_dtduration = line[15]
    allow_date = line[16]
    allow_time = line[17]
    allow_datetime = line[18]
    allow_datetimestamp = line[19]
    allow_day = line[20]
    allow_month = line[21]
    allow_year = line[22]
    allow_year_month = line[23]
    allow_month_day = line[24]

    creator_id = adminpk
    edited_by = adminpk
    prj = line[27]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 normal_status, allow_duration, allow_ymduration, allow_dtduration, allow_date, allow_time,
                 allow_datetime, allow_datetimestamp, allow_day, allow_month, allow_year, allow_year_month, allow_month_day, ''))

query = ("""INSERT INTO dmgen_xdtemporal
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              normal_status,allow_duration,allow_ymduration,allow_dtduration,allow_date,allow_time,allow_datetime,allow_datetimestamp,
              allow_day,allow_month,allow_year,allow_year_month,allow_month_day,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvtemporal_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdtemporal_pred_obj (id,xdtemporal_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdOrdinals
print("Adding XdOrdinals")
curMLHIM.execute("SELECT *  from ccdgen_dvordinal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    normal_status = line[12]
    ordinals = line[13]
    symbols = line[14]
    eannon = line[15]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[18]
    srr = line[19]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 normal_status, ordinals, symbols, eanno, srr, ''))

query = ("""INSERT INTO dmgen_xdordinal
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              normal_status,ordinals,symbols,annotations,simple_rr_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvordinal_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdordinal_pred_obj (id,xdordinal_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdCounts
print("Adding XdCounts")
curMLHIM.execute("SELECT *  from ccdgen_dvcount")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    normal_status = line[12]
    min_mag = line[13]
    max_mag = line[14]
    min_inc = line[15]
    max_inc = line[16]
    min_exc = line[17]
    max_exc = line[18]
    tot_dig = line[19]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[22]
    srr = line[23]
    units_id = line[24]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 normal_status, min_mag, max_mag, min_inc, max_inc, min_exc, max_exc, tot_dig, units_id, srr, ''))

query = ("""INSERT INTO dmgen_xdcount
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,units_id,simple_rr_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvcount_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdcount_pred_obj (id,xdcount_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdQuantities
print("Adding XdQuantities")
curMLHIM.execute("SELECT *  from ccdgen_dvquantity")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    normal_status = line[12]
    
    # significant problems with overflow re-using these values.
    
    min_mag = None  # line[13]
    max_mag = None  # line[14]
    min_inc = None  # line[15]
    max_inc = None  # line[16]
    min_exc = None  # line[17]
    max_exc = None  # line[18]
    tot_dig = line[19]
    frac_dig = line[20]
    
    creator_id = adminpk
    edited_by = adminpk
    prj = line[23]
    srr = line[24]
    units_id = line[25]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 normal_status, min_mag, max_mag, min_inc, max_inc, min_exc, max_exc, tot_dig, units_id, frac_dig, srr, ''))

query = ("""INSERT INTO dmgen_xdquantity
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits, units_id, fraction_digits, simple_rr_id, schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")


curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvquantity_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdquantity_pred_obj (id,xdquantity_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# XdRatios
print("Adding XdRatios")
curMLHIM.execute("SELECT *  from ccdgen_dvratio")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    ad_ctid = line[11]

    normal_status = line[12]
    min_mag = line[13]
    max_mag = line[14]
    min_inc = line[15]
    max_inc = line[16]
    min_exc = line[17]
    max_exc = line[18]
    tot_dig = line[19]
    ratio_type = line[20]

    num_min_inc = line[21]
    num_max_inc = line[22]
    num_min_exc = line[23]
    num_max_exc = line[24]

    den_min_inc = line[25]
    den_max_inc = line[26]
    den_min_exc = line[27]
    den_max_exc = line[28]

    creator_id = adminpk
    den_units_id = line[30]
    edited_by = adminpk
    num_units_id = line[32]
    prj = line[33]
    ratio_units_id = line[34]
    srr = line[35]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by, ad_ctid, False, False, False, False,
                 normal_status, min_mag, max_mag, min_inc, max_inc, min_exc, max_exc, tot_dig, ratio_type, num_min_inc, num_max_inc, num_min_exc, num_max_exc,
                 den_min_inc, den_max_inc, den_min_exc, den_max_exc, num_units_id, den_units_id, ratio_units_id, srr, ''))

query = ("""INSERT INTO dmgen_xdratio
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,require_mod,              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,ratio_type,num_min_inclusive,num_max_inclusive,num_min_exclusive,num_max_exclusive,
              den_min_inclusive,den_max_inclusive,den_min_exclusive,den_max_exclusive,num_units_id,den_units_id,ratio_units_id,simple_rr_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvratio_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_xdratio_pred_obj (id,xdratio_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# Clusters
print("Adding Clusters")
curMLHIM.execute("SELECT *  from ccdgen_cluster")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[13]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False,
                 descr, asserts, lang, creator_id, edited_by, ''))

query = ("""INSERT INTO dmgen_cluster
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_cluster_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_cluster_pred_obj (id,cluster_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# clusters
curMLHIM.execute("SELECT *  from ccdgen_cluster_clusters")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_clusters
              (id,from_cluster_id,to_cluster_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvbooleans
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvboolean")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdboolean
              (id,cluster_id,xdboolean_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvcounts
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvcount")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdcount
              (id,cluster_id,xdcount_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvlink
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvlink")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdlink
              (id,cluster_id,xdlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvfile
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvfile")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdfile
              (id,cluster_id,xdfile_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvordinals
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvordinal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdordinal
              (id,cluster_id,xdordinal_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvquantities
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvquantity")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdquantity
              (id,cluster_id,xdquantity_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvratio
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvratio")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdratio
              (id,cluster_id,xdratio_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvstrings
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvstring")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdstring
              (id,cluster_id,xdstring_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# dvtemporals
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvtemporal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_cluster_xdtemporal
              (id,cluster_id,xdtemporal_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# Partys
print("Adding Partys")
curMLHIM.execute("SELECT *  from ccdgen_party")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    creator_id = adminpk
    details = line[12]
    edited_by = adminpk
    prj = line[14]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False,
                 descr, asserts, lang, creator_id, edited_by, details, ''))

query = ("""INSERT INTO dmgen_party
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,details_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_party_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_party_pred_obj (id,party_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_party_external_ref")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    party_id = line[1]
    link_id = line[2]
    data.append((pk, party_id, link_id))

query = ("INSERT INTO dmgen_party_external_ref (id,party_id,xdlink_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# Participation
print("Adding Participations")
curMLHIM.execute("SELECT *  from ccdgen_participation")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    creator_id = adminpk
    edited_by = adminpk
    function = line[13]
    mode = line[14]
    performer = line[15]
    prj = line[16]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 performer, function, mode, ''))

query = ("""INSERT INTO dmgen_participation
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              performer_id,function_id,mode_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()


curMLHIM.execute("SELECT *  from ccdgen_participation_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_participation_pred_obj (id,participation_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# Attestations
print("Adding Attestations")
curMLHIM.execute("SELECT *  from ccdgen_attestation")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    committer = line[11]
    creator_id = adminpk
    edited_by = adminpk
    prj = line[14]
    proof = line[15]
    reason = line[16]
    view = line[17]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 view, proof, reason, committer, ''))

query = ("""INSERT INTO dmgen_attestation
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              view_id,proof_id,reason_id,committer_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_attestation_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_attestation_pred_obj (id,attestation_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

# Audits
print("Adding Audits")
curMLHIM.execute("SELECT *  from ccdgen_audit")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]

    creator_id = adminpk
    edited_by = adminpk
    location = line[13]
    prj = line[14]
    sysid = line[15]
    sysuser = line[16]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 sysid, sysuser, location, ''))

query = ("""INSERT INTO dmgen_audit
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              system_id_id,system_user_id,location_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_audit_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO dmgen_audit_pred_obj (id,audit_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


# AdminEntry
print("Adding AdminEntrys")
curMLHIM.execute("SELECT *  from ccdgen_adminentry")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    language = line[11]
    encoding = line[12]
    state = line[13]
    attestation = line[14]
    audit = line[15]
    creator_id = adminpk
    entrydata = line[17]
    edited_by = adminpk
    prj = line[19]
    protocol = line[20]
    provider = line[21]
    subject = line[22]
    workflow = line[23]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 language, encoding, state, entrydata, subject, provider, protocol, workflow, audit, attestation, ''))

query = ("""INSERT INTO dmgen_entry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# links
curMLHIM.execute("SELECT *  from ccdgen_adminentry_links")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_entry_links
              (id,entry_id,xdlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# participations
curMLHIM.execute("SELECT *  from ccdgen_adminentry_participations")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_entry_participations
              (id,entry_id,participation_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_adminentry_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO dmgen_entry_pred_obj
              (id,entry_id,predobj_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# CareEntry
print("Adding CareEntrys")
curMLHIM.execute("SELECT *  from ccdgen_careentry")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0] + 100
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    language = line[11]
    encoding = line[12]
    state = line[13]
    attestation = line[14]
    audit = line[15]
    creator_id = adminpk
    entrydata = line[17]
    edited_by = adminpk
    prj = line[19]
    protocol = line[20]
    provider = line[21]
    subject = line[22]
    workflow = line[23]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 language, encoding, state, entrydata, subject, provider, protocol, workflow, audit, attestation, ''))

query = ("""INSERT INTO dmgen_entry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# links
curMLHIM.execute("SELECT *  from ccdgen_careentry_links")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0] + 100, line[1] + 100, line[2]))

query = ("""INSERT INTO dmgen_entry_links
              (id,entry_id,xdlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# participations
curMLHIM.execute("SELECT *  from ccdgen_careentry_participations")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0] + 100, line[1] + 100, line[2]))

query = ("""INSERT INTO dmgen_entry_participations
              (id,entry_id,participation_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_careentry_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0] + 100, line[1] + 100, line[2]))

query = ("""INSERT INTO dmgen_entry_pred_obj
              (id,entry_id,predobj_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# DemographicEntry
print("Adding DemographicEntrys")
curMLHIM.execute("SELECT *  from ccdgen_demographicentry")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0] + 200
    label = line[1]
    ct_id = line[2]
    created = line[3]
    updated = line[4]
    published = line[5]
    descr = line[6]
    asserts = line[8]
    lang = line[9]
    language = line[11]
    encoding = line[12]
    state = line[13]
    attestation = line[14]
    audit = line[15]
    creator_id = adminpk
    entrydata = line[17]
    edited_by = adminpk
    prj = line[19]
    protocol = line[20]
    provider = line[21]
    subject = line[22]
    workflow = line[23]

    if isinstance(asserts, str):
        asserts = asserts.replace('dv', 'xd')

    data.append((pk, prj, label, ct_id, created, updated, False, descr, asserts, lang, creator_id, edited_by,
                 language, encoding, state, entrydata, subject, provider, protocol, workflow, audit, attestation, ''))

query = ("""INSERT INTO dmgen_entry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# links
curMLHIM.execute("SELECT *  from ccdgen_demographicentry_links")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0] + 200, line[1] + 200, line[2]))

query = ("""INSERT INTO dmgen_entry_links
              (id,entry_id,xdlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

# participations
curMLHIM.execute("SELECT *  from ccdgen_demographicentry_participations")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0] + 200, line[1] + 200, line[2]))

query = ("""INSERT INTO dmgen_entry_participations
              (id,entry_id,participation_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_demographicentry_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0] + 200, line[1] + 200, line[2]))

query = ("""INSERT INTO dmgen_entry_pred_obj
              (id,entry_id,predobj_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()


# Close all
print("\nFinished copying.")

curMLHIM.close()
print("Cleaning the dmgen DB")
S3M.set_isolation_level(0)
curS3M.execute("VACUUM FULL")
curS3M.close()

MLHIM.close()
S3M.close()

print("\n\n**** All Done! ****\n\n")
