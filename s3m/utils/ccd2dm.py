import psycopg2
import uuid

print("\n\nPreparing to copy ccdgen DB records")

v10 = psycopg2.connect("dbname=ccdgen_old user=tim password=cl!pper5")
v11 = psycopg2.connect("dbname=ccdgen user=tim password=cl!pper5")
v11.autocommit = True

print("Cleaning the old ccdgen DB")
cur10 = v10.cursor()
isolevel = v10.isolation_level
v10.set_isolation_level(0)
cur10.execute("VACUUM FULL ANALYZE")
v10.set_isolation_level(isolevel)

cur11 = v11.cursor()

# Users & Groups
print("Adding Users and Groups")
cur10.execute("SELECT *  from auth_user")
rows10 = cur10.fetchall()
data = []

for line in rows10:
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
    data.append((pk, pw, last, issuper, uname, first, lastname, email, staff, active, joined))

query = ("""INSERT INTO auth_user
(id,password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from auth_group")
rows10 = cur10.fetchall()
data = []
# mdata = []
for line in rows10:
    pk = line[0]
    name = line[1]
    data.append((pk, name))

query = ("""INSERT INTO auth_group (id,name)
               VALUES(%s,%s)""")

cur11.executemany(query, data)
v11.commit()

#  Projects
print("Adding Projects")
cur10.execute("SELECT *  from ccdgen_project")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    name = line[1]
    descr = line[2]
    data.append((pk, name, descr))

query = ("INSERT INTO ccdgen_project (id,prj_name,description) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

#  Modelers
print("Adding Modelers")
cur10.execute("SELECT *  from ccdgen_modeler")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    userid = line[1]
    name = line[2]
    email = line[3]
    prjid = line[4]
    data.append((pk, userid, name, email, prjid, True))

query = ("INSERT INTO ccdgen_modeler (id,user_id,name,email,project_id,prj_filter) VALUES(%s,%s,%s,%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

#  NS, Predicates and PredObjs
print("Adding NS, Predicates and PredObjs")
cur10.execute("SELECT *  from ccdgen_ns")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    abbrev = line[1]
    uri = line[2]
    data.append((pk, abbrev, uri))

query = ("INSERT INTO ccdgen_ns (id,abbrev,uri) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_predicate")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    ns_abbrev_id = line[1]
    class_name = line[2]
    data.append((pk, ns_abbrev_id, class_name))

query = ("INSERT INTO ccdgen_predicate (id,ns_abbrev_id,class_name) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_predobj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    pred_id = line[1]
    obj_uri = line[2]
    prj_id = line[3]
    po_name = line[2][-50:]
    data.append((pk, pred_id, obj_uri, prj_id, po_name))

query = ("INSERT INTO ccdgen_predobj (id,predicate_id,object_uri,project_id, po_name) VALUES(%s,%s,%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvBoolean
print("Adding DvBooleans")
cur10.execute("SELECT *  from ccdgen_dvboolean")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    trues = line[17]
    falses = line[18]

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 trues, falses,
                 creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_dvboolean
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              trues, falses,
              creator_id, edited_by_id,project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,
              %s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvboolean_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvboolean_pred_obj (id,dvboolean_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

# DvStrings
print("Adding DvStrings")
cur10.execute("SELECT *  from ccdgen_dvstring")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    min_len = line[17]
    max_len = line[18]
    exact_len = line[19]
    enums = line[20]
    defns = line[21]
    def_val = line[22]
    if len(def_val) > 250:
        def_val = ''

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 min_len, max_len, exact_len, enums, defns, def_val,
                 creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_dvstring
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              min_length, max_length, exact_length, enums, definitions, def_val,
              creator_id,edited_by_id,project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,
              %s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvstring_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvstring_pred_obj (id,dvstring_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

# Units
print("Adding Units")
cur10.execute("SELECT *  from ccdgen_units")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    min_len = line[17]
    max_len = line[18]
    exact_len = line[19]
    enums = line[20]
    def_val = line[21]
    defns = line[22]
    if len(def_val) > 250:
        def_val = ''

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 min_len, max_len, exact_len, enums, def_val, defns, creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_units
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              min_length, max_length, exact_length, enums, def_val, definitions,
              creator_id,edited_by_id,project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,
              %s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_units_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_units_pred_obj (id,units_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

# DvIntervals
print("Adding DvIntervals")
cur10.execute("SELECT *  from ccdgen_dvinterval")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    lower = line[17]
    upper = line[18]
    invl_type = line[19]
    li = line[20]
    ui = line[21]
    lb = line[22]
    ub = line[23]
    uname = line[24]
    uuri = line[25]

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 lower, upper, invl_type, li, ui, lb, ub, uname, uuri,
                 creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_dvinterval
    (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
    lower, upper, interval_type, lower_included, upper_included, lower_bounded, upper_bounded, units_name, units_uri,
    creator_id, edited_by_id, project_id)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvinterval_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvinterval_pred_obj (id,dvinterval_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

# ReferenceRanges
print("Adding ReferenceRanges")
cur10.execute("SELECT *  from ccdgen_referencerange")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    defn = line[17]
    interval_id = line[18]
    is_norm = line[19]

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 defn, is_norm, creator_id, edited_by, interval_id, prj))

query = ("""INSERT INTO ccdgen_referencerange
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              definition, is_normal, creator_id, edited_by_id, interval_id, project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_referencerange_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_referencerange_pred_obj (id,referencerange_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

# DvLinks
print("Adding DvLinks")
cur10.execute("SELECT *  from ccdgen_dvlink")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    relation = line[17]
    rel_uri = line[18]

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 relation, rel_uri,
                 creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_dvlink
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              relation, relation_uri,
              creator_id, edited_by_id, project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,
              %s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvlink_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvlink_pred_obj (id,dvlink_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvFiles
print("Adding DvFiles")
cur10.execute("SELECT *  from ccdgen_dvfile")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())

    media_type = line[17]
    encoding = line[18]
    cont_lang = line[19]
    alt_txt = line[20]
    cm = line[21]

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 media_type, encoding, cont_lang, alt_txt, cm,
                 creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_dvfile
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              media_type, encoding, language, alt_txt, content_mode,
              creator_id, edited_by_id, project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,
              %s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvfile_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvfile_pred_obj (id,dvfile_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvTemporals
print("Adding DvTemporals")
cur10.execute("SELECT *  from ccdgen_dvtemporal")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = published
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    normal_status = line[17]
    allow_duration = line[18]
    allow_ymduration = line[19]
    allow_dtduration = line[20]
    allow_date = line[21]
    allow_time = line[22]
    allow_datetime = line[23]
    allow_datetimestamp = line[24]
    allow_day = line[25]
    allow_month = line[26]
    allow_year = line[27]
    allow_year_month = line[28]
    allow_month_day = line[29]

    data.append((pk, label, ct_id, created, updated, published, descr, asserts, lang, ad_ctid,
                 normal_status, allow_duration, allow_ymduration, allow_dtduration,
                 allow_date, allow_time, allow_datetime, allow_datetimestamp, allow_day, allow_month, allow_year,
                 allow_year_month, allow_month_day,
                 creator_id, edited_by, prj))

query = ("""INSERT INTO ccdgen_dvtemporal
              (id, label, ct_id, created, updated, published, description, asserts, lang, adapter_ctid,
              normal_status, allow_duration, allow_ymduration, allow_dtduration, allow_date, allow_time, allow_datetime,
              allow_datetimestamp, allow_day, allow_month, allow_year, allow_year_month, allow_month_day,
              creator_id, edited_by_id, project_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,
              %s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvtemporal_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvtemporal_pred_obj (id,dvtemporal_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvOrdinals
print("Adding DvOrdinals")
cur10.execute("SELECT *  from ccdgen_dvordinal")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    normal_status = line[17]
    ordinals = line[18]
    symbols = line[19]
    eannon = line[20]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by, ad_ctid,
                normal_status, ordinals, symbols, eannon))

query = ("""INSERT INTO ccdgen_dvordinal
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,
              normal_status,ordinals,symbols,annotations)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvordinal_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvordinal_pred_obj (id,dvordinal_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvCounts
print("Adding DvCounts")
cur10.execute("SELECT *  from ccdgen_dvcount")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    normal_status = line[17]
    min_mag = line[18]
    max_mag = line[19]
    min_inc = line[20]
    max_inc = line[21]
    min_exc = line[22]
    max_exc = line[23]
    tot_dig = line[24]
    units_id = line[25]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by, ad_ctid,
                 normal_status, min_mag, max_mag, min_inc, max_inc, min_exc, max_exc,
                 tot_dig, units_id))

query = ("""INSERT INTO ccdgen_dvcount
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,units_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvcount_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvcount_pred_obj (id,dvcount_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvQuantities
print("Adding DvQuantities")
cur10.execute("SELECT *  from ccdgen_dvquantity")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())
    normal_status = line[17]
    min_mag = line[18]
    max_mag = line[19]
    min_inc = line[20]
    max_inc = line[21]
    min_exc = line[22]
    max_exc = line[23]
    tot_dig = line[24]
    frac_dig = line[25]
    units_id = line[26]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by, ad_ctid,
                 normal_status, min_mag, max_mag, min_inc, max_inc, min_exc, max_exc,
                 tot_dig, units_id, frac_dig))

query = ("""INSERT INTO ccdgen_dvquantity
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,units_id,fraction_digits)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvquantity_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvquantity_pred_obj (id,dvquantity_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# DvRatios
print("Adding DvRatios")
cur10.execute("SELECT *  from ccdgen_dvratio")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = str(uuid.uuid4())

    normal_status = line[17]
    min_mag = line[18]
    max_mag = line[19]
    min_inc = line[20]
    max_inc = line[21]
    min_exc = line[22]
    max_exc = line[23]
    tot_dig = line[24]
    ratio_type = line[25]

    num_min_inc = line[26]
    num_max_inc = line[27]
    num_min_exc = line[28]
    num_max_exc = line[29]

    den_min_inc = line[30]
    den_max_inc = line[31]
    den_min_exc = line[32]
    den_max_exc = line[33]
    num_units_id = line[34]
    den_units_id = line[35]
    ratio_units_id = line[36]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by, ad_ctid,
                 normal_status, min_mag, max_mag, min_inc, max_inc, min_exc, max_exc,
                 tot_dig, ratio_type, num_min_inc, num_max_inc, num_min_exc, num_max_exc, den_min_inc, den_max_inc,
                 den_min_exc, den_max_exc, num_units_id, den_units_id, ratio_units_id))

query = ("""INSERT INTO ccdgen_dvratio
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,ratio_type,num_min_inclusive,num_max_inclusive,num_min_exclusive,num_max_exclusive,
              den_min_inclusive,den_max_inclusive,den_min_exclusive,den_max_exclusive,num_units_id,den_units_id,ratio_units_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_dvratio_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_dvratio_pred_obj (id,dvratio_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


# Clusters
print("Adding Clusters")
cur10.execute("SELECT *  from ccdgen_cluster")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by, ''))

query = ("""INSERT INTO ccdgen_cluster
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_cluster_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_cluster_pred_obj (id,cluster_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

# clusters
cur10.execute("SELECT *  from ccdgen_cluster_clusters")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_clusters
              (id,from_cluster_id,to_cluster_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvbooleans
cur10.execute("SELECT *  from ccdgen_cluster_dvboolean")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvboolean
              (id,cluster_id,dvboolean_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvcounts
cur10.execute("SELECT *  from ccdgen_cluster_dvcount")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvcount
              (id,cluster_id,dvcount_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvlink
cur10.execute("SELECT *  from ccdgen_cluster_dvlink")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvlink
              (id,cluster_id,dvlink_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvfile
cur10.execute("SELECT *  from ccdgen_cluster_dvfile")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvfile
              (id,cluster_id,dvfile_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvordinals
cur10.execute("SELECT *  from ccdgen_cluster_dvordinal")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvordinal
              (id,cluster_id,dvordinal_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvquantities
cur10.execute("SELECT *  from ccdgen_cluster_dvquantity")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvquantity
              (id,cluster_id,dvquantity_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvratio
cur10.execute("SELECT *  from ccdgen_cluster_dvratio")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvratio
              (id,cluster_id,dvratio_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvstrings
cur10.execute("SELECT *  from ccdgen_cluster_dvstring")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvstring
              (id,cluster_id,dvstring_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# dvtemporals
cur10.execute("SELECT *  from ccdgen_cluster_dvtemporal")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_cluster_dvtemporal
              (id,cluster_id,dvtemporal_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# Partys
print("Adding Partys")
cur10.execute("SELECT *  from ccdgen_party")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    details = line[16]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 details))

query = ("""INSERT INTO ccdgen_party
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,details_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_party_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_party_pred_obj (id,party_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_party_external_ref")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    party_id = line[1]
    link_id = line[2]
    data.append((pk, party_id, link_id))

query = ("INSERT INTO ccdgen_party_external_ref (id,party_id,dvlink_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


#  Participation
print("Adding Participations")
cur10.execute("SELECT *  from ccdgen_participation")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    performer = line[16]
    function = line[17]
    mode = line[18]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 performer, function, mode))

query = ("""INSERT INTO ccdgen_participation
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              performer_id,function_id,mode_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()


cur10.execute("SELECT *  from ccdgen_participation_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_participation_pred_obj (id,participation_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


#  Attestations
print("Adding Attestations")
cur10.execute("SELECT *  from ccdgen_attestation")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    view = line[16]
    proof = line[17]
    reason = line[18]
    committer = line[19]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 view, proof, reason, committer))

query = ("""INSERT INTO ccdgen_attestation
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              view_id,proof_id,reason_id,committer_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_attestation_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_attestation_pred_obj (id,attestation_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()

#  Audits
print("Adding Audits")
cur10.execute("SELECT *  from ccdgen_audit")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    sysid = line[16]
    sysuser = line[17]
    location = line[18]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 sysid, sysuser, location, ''))

query = ("""INSERT INTO ccdgen_audit
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              system_id_id,system_user_id,location_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_audit_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk, dv_id, pobj_id))

query = ("INSERT INTO ccdgen_audit_pred_obj (id,audit_id,predobj_id) VALUES(%s,%s,%s)")
cur11.executemany(query, data)
v11.commit()


#  AdminEntry
print("Adding AdminEntrys")
cur10.execute("SELECT *  from ccdgen_adminentry")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    language = line[16]
    encoding = line[17]
    state = line[18]
    entrydata = line[19]
    subject = line[20]
    provider = line[21]
    protocol = line[22]
    workflow = line[23]
    audit = line[24]
    attestation = line[25]

    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 language, encoding, state, entrydata, subject, provider, protocol, workflow, audit, attestation))

query = ("""INSERT INTO ccdgen_adminentry
             (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,
             edited_by_id,language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,
             audit_id,attestation_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  links
cur10.execute("SELECT *  from ccdgen_adminentry_links")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_adminentry_links
              (id,adminentry_id,dvlink_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  participations
cur10.execute("SELECT *  from ccdgen_adminentry_participations")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_adminentry_participations
              (id,adminentry_id,participation_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_adminentry_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_adminentry_pred_obj
              (id,adminentry_id,predobj_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  CareEntry
print("Adding CareEntrys")
cur10.execute("SELECT *  from ccdgen_careentry")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    language = line[16]
    encoding = line[17]
    state = line[18]
    entrydata = line[19]
    subject = line[20]
    provider = line[21]
    protocol = line[22]
    workflow = line[23]
    audit = line[24]
    attestation = line[25]


    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 language, encoding, state, entrydata, subject, provider, protocol, workflow, audit, attestation))

query = ("""INSERT INTO ccdgen_careentry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  links
cur10.execute("SELECT *  from ccdgen_careentry_links")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_careentry_links
              (id,careentry_id,dvlink_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  participations
cur10.execute("SELECT *  from ccdgen_careentry_participations")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_careentry_participations
              (id,careentry_id,participation_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_careentry_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_careentry_pred_obj
              (id,careentry_id,predobj_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  DemographicEntry
print("Adding DemographicEntrys")
cur10.execute("SELECT *  from ccdgen_demographicentry")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = str(uuid.uuid4())
    created = line[4]
    updated = line[5]
    published = False
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    language = line[16]
    encoding = line[17]
    state = line[18]
    entrydata = line[19]
    subject = line[20]
    provider = line[21]
    protocol = line[22]
    workflow = line[23]
    audit = line[24]
    attestation = line[25]


    data.append((pk, prj, label, ct_id, created, updated, published, descr, asserts, lang, creator_id, edited_by,
                 language, encoding, state, entrydata, subject, provider, protocol, workflow, audit, attestation))

query = ("""INSERT INTO ccdgen_demographicentry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  links
cur10.execute("SELECT *  from ccdgen_demographicentry_links")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_demographicentry_links
              (id,demographicentry_id,dvlink_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

#  participations
cur10.execute("SELECT *  from ccdgen_demographicentry_participations")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_demographicentry_participations
              (id,demographicentry_id,participation_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

cur10.execute("SELECT *  from ccdgen_demographicentry_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_demographicentry_pred_obj
              (id,demographicentry_id,predobj_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# CCD
print("Adding CCDs")
cur10.execute("SELECT *  from ccdgen_ccd")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    pk = line[0]
    ct_id = line[1]
    created = line[2]
    updated = line[3]
    creator = line[4]
    editedby = line[5]
    published = False
    prj = line[7]
    about = line[8]
    title = line[9]
    author = line[10]
    subject = line[11]
    source = line[12]
    rights = line[13]
    relation = line[14]
    coverage = line[15]
    dc_type = line[16]
    identifier = line[17]
    descr = line[18]
    publisher = line[19]
    pubdate = line[20]
    dc_format = line[21]
    dc_lang = line[22]
    admin_def = line[23]
    care_def = line[24]
    demog_def = line[25]
    asserts = line[26]

    data.append((pk, ct_id, created, updated, published, about, title, subject, source, rights, relation,
                          coverage, dc_type, identifier, descr, publisher, pubdate, dc_format, dc_lang, asserts,
                          admin_def, author, care_def, creator, demog_def, editedby, prj))

query = ("""INSERT INTO ccdgen_ccd
(id,ct_id,created,updated,published,about,title,subject,source,rights,relation,coverage,dc_type,identifier,
description,publisher,pub_date,dc_format,dc_language,asserts,admin_definition_id,
author_id,care_definition_id,creator_id,demog_definition_id,edited_by_id,project_id)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s)""")

cur11.executemany(query, data)
v11.commit()

# ccd_contrib
cur10.execute("SELECT *  from ccdgen_ccd_contrib")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_ccd_contrib
              (id,ccd_id,modeler_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()

# ccd_pred_obj
cur10.execute("SELECT *  from ccdgen_ccd_pred_obj")
rows10 = cur10.fetchall()
data = []

for line in rows10:
    data.append((line[0], line[1], line[2]))

query = ("""INSERT INTO ccdgen_ccd_pred_obj
              (id,ccd_id,predobj_id)
              VALUES(%s,%s,%s)""")
cur11.executemany(query, data)
v11.commit()


#  Close MLHIM DB
print("\nFinished copying.")

cur10.close()

#  Clean and close
print("\nCleaning the new DB")
v11.set_isolation_level(0)
cur11.execute("VACUUM FULL ANALYZE")
cur11.close()

v10.close()
v11.close()

print("\n\n**** All Done! ****\n\n")
