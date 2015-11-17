import json
import datetime
import psycopg2

print("\n\nPreparing to coppy ccdgen DB records to dmgen DB")

MLHIM = psycopg2.connect("dbname=ccdgen user=tim password=cl!pper5")
S3M = psycopg2.connect("dbname=dmgen user=tim password=cl!pper5")
S3M.autocommit = True

print("Cleaning the ccdgen DB")
curMLHIM = MLHIM.cursor()
isolevel = MLHIM.isolation_level
MLHIM.set_isolation_level(0)
curMLHIM.execute("VACUUM FULL ANALYZE")
MLHIM.set_isolation_level(isolevel)

curS3M = S3M.cursor()

#Users & Groups
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
    data.append((pk,pw,last,issuper,uname,first,lastname,email,staff,active,joined))
    if staff:
        mdata.append((pk,pk,lastname,email))

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
    data.append((pk,name))

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
    data.append((pk,name,descr))

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
    userid = line[1]
    name = line[2]
    email = line[3]
    prjid = line[4]
    data.append((pk,userid,name,email,prjid))

query = ("INSERT INTO dmgen_modeler (id,user_id,name,email,project_id) VALUES(%s,%s,%s,%s,%s)")
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
    data.append((pk,abbrev,uri))

query = ("INSERT INTO dmgen_ns (id,abbrev,uri) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_predicate")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    ns_abbrev_id = line[1]
    class_name = line[2]
    data.append((pk,ns_abbrev_id,class_name))

query = ("INSERT INTO dmgen_predicate (id,ns_abbrev_id,class_name) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_predobj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    pred_id = line[1]
    obj_uri = line[2]
    prj_id = line[3]
    data.append((pk,pred_id,obj_uri,prj_id))

query = ("INSERT INTO dmgen_predobj (id,predicate_id,object_uri,project_id) VALUES(%s,%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvBoolean
print("Adding DvBooleans")
curMLHIM.execute("SELECT *  from ccdgen_dvboolean")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]
    trues = line[17]
    falses = line[18]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,trues,falses,''))

query = ("""INSERT INTO dmgen_dvboolean
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              trues,falses,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvboolean_pred_obj (id,dvboolean_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()



#DvStrings
print("Adding DvStrings")
curMLHIM.execute("SELECT *  from ccdgen_dvstring")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]
    min_len = line[17]
    max_len = line[18]
    exact_len = line[19]
    enums = line[20]
    eanno  = line[21]
    def_val = line[22][0:1999]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                           min_len,max_len,exact_len,enums,eanno,def_val,''))

query = ("""INSERT INTO dmgen_dvstring
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              min_length,max_length,exact_length,enums,definitions,def_val,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvstring_pred_obj (id,dvstring_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

#Units
print("Adding Units")
curMLHIM.execute("SELECT *  from ccdgen_units")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]
    min_len = line[17]
    max_len = line[18]
    exact_len = line[19]
    enums = line[20]
    eanno  = line[21]
    def_val = line[22][0:1999]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                           min_len,max_len,exact_len,enums,eanno,def_val,''))

query = ("""INSERT INTO dmgen_units
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              min_length,max_length,exact_length,enums,definitions,def_val,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_units_pred_obj (id,units_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

#DvIntervals
print("Adding DvIntervals")
curMLHIM.execute("SELECT *  from ccdgen_dvinterval")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

    lower = line[17]
    upper = line[18]
    invl_type = line[19]
    li = line[20]
    ui = line[21]
    lb  = line[22]
    ub = line[23]
    uname = line[24]
    uuri = line[25]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                           lower,upper,invl_type,li,ui,lb,ub,uname,uuri,''))

query = ("""INSERT INTO dmgen_dvinterval
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              lower,upper,interval_type,lower_included,upper_included,lower_bounded,upper_bounded,units_name,units_uri,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvinterval_pred_obj (id,dvinterval_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

#ReferenceRanges
print("Adding ReferenceRanges")
curMLHIM.execute("SELECT *  from ccdgen_referencerange")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]
    defn = line[17]
    interval_id = line[18]
    is_norm = line[19]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                         defn,interval_id,is_norm,''))

query = ("""INSERT INTO dmgen_referencerange
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              definition,interval_id,is_normal,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_referencerange_pred_obj (id,referencerange_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

#DvLinks
print("Adding DvLinks")
curMLHIM.execute("SELECT *  from ccdgen_dvlink")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]
    relation = line[17]
    rel_uri = line[18]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                          relation,rel_uri,''))

query = ("""INSERT INTO dmgen_dvlink
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              relation,relation_uri,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvlink_pred_obj (id,dvlink_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvFiles
print("Adding DvFiles")
curMLHIM.execute("SELECT *  from ccdgen_dvfile")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

    mime = line[17]
    encoding = line[18]
    cont_lang = line[19]
    alt_txt = line[20]
    cm = line[21]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                          mime,encoding,cont_lang,alt_txt,cm,''))

query = ("""INSERT INTO dmgen_dvfile
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              media_type,encoding,language,alt_txt,content_mode,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvfile_pred_obj (id,dvfile_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvTemporals
print("Adding DvTemporals")
curMLHIM.execute("SELECT *  from ccdgen_dvtemporal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

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

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                          normal_status,allow_duration,allow_ymduration,allow_dtduration,allow_date,allow_time,
                          allow_datetime,allow_datetimestamp,allow_day,allow_month,allow_year,allow_year_month,allow_month_day,''))

query = ("""INSERT INTO dmgen_dvtemporal
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              normal_status,allow_duration,allow_ymduration,allow_dtduration,allow_date,allow_time,allow_datetime,allow_datetimestamp,
              allow_day,allow_month,allow_year,allow_year_month,allow_month_day,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvtemporal_pred_obj (id,dvtemporal_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvOrdinals
print("Adding DvOrdinals")
curMLHIM.execute("SELECT *  from ccdgen_dvordinal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

    normal_status = line[17]
    ordinals  = line[18]
    symbols = line[19]
    eannon = line[20]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                          normal_status,ordinals,symbols,eanno,''))

query = ("""INSERT INTO dmgen_dvordinal
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              normal_status,ordinals,symbols,annotations,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvordinal_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvordinal_pred_obj (id,dvordinal_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvCounts
print("Adding DvCounts")
curMLHIM.execute("SELECT *  from ccdgen_dvcount")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

    normal_status = line[17]
    min_mag = line[18]
    max_mag = line[19]
    min_inc = line[20]
    max_inc = line[21]
    min_exc = line[22]
    max_exc = line[23]
    tot_dig   = line[24]
    units_id  = line[25]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                         normal_status,min_mag,max_mag,min_inc,max_inc,min_exc,max_exc,tot_dig,units_id,''))

query = ("""INSERT INTO dmgen_dvcount
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,units_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvcount_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvcount_pred_obj (id,dvcount_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvQuantities
print("Adding DvQuantities")
curMLHIM.execute("SELECT *  from ccdgen_dvquantity")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

    normal_status = line[17]
    min_mag = line[18]
    max_mag = line[19]
    min_inc = line[20]
    max_inc = line[21]
    min_exc = line[22]
    max_exc = line[23]
    tot_dig   = line[24]
    frac_dig   = line[25]
    units_id  = line[26]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                         normal_status,min_mag,max_mag,min_inc,max_inc,min_exc,max_exc,tot_dig,units_id,frac_dig,''))

query = ("""INSERT INTO dmgen_dvquantity
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,units_id,fraction_digits,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvquantity_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvquantity_pred_obj (id,dvquantity_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#DvRatios
print("Adding DvRatios")
curMLHIM.execute("SELECT *  from ccdgen_dvratio")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    ad_ctid = line[16]

    normal_status = line[17]
    min_mag = line[18]
    max_mag = line[19]
    min_inc = line[20]
    max_inc = line[21]
    min_exc = line[22]
    max_exc = line[23]
    tot_dig   = line[24]
    ratio_type = line[25]

    num_min_inc = line[26]
    num_max_inc = line[27]
    num_min_exc = line[28]
    num_max_exc = line[29]

    den_min_inc = line[30]
    den_max_inc = line[31]
    den_min_exc = line[32]
    den_max_exc = line[33]

    num_units_id  = line[34]
    den_units_id  = line[35]
    ratio_units_id  = line[36]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,ad_ctid, False,False,False,
                           normal_status,min_mag,max_mag,min_inc,max_inc,min_exc,max_exc,tot_dig,ratio_type,num_min_inc,num_max_inc,num_min_exc,num_max_exc,
                           den_min_inc,den_max_inc,den_min_exc,den_max_exc,num_units_id,den_units_id,ratio_units_id,''))

query = ("""INSERT INTO dmgen_dvratio
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,adapter_ctid,require_vtb,require_vte,require_tr,
              normal_status,min_magnitude,max_magnitude,min_inclusive,max_inclusive,min_exclusive,max_exclusive,total_digits,ratio_type,num_min_inclusive,num_max_inclusive,num_min_exclusive,num_max_exclusive,
              den_min_inclusive,den_max_inclusive,den_min_exclusive,den_max_exclusive,num_units_id,den_units_id,ratio_units_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_dvratio_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    dv_id = line[1]
    pobj_id = line[2]
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_dvratio_pred_obj (id,dvratio_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#Clusters
print("Adding Clusters")
curMLHIM.execute("SELECT *  from ccdgen_cluster")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,''))

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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_cluster_pred_obj (id,cluster_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

#clusters
curMLHIM.execute("SELECT *  from ccdgen_cluster_clusters")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_clusters
              (id,from_cluster_id,to_cluster_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvbooleans
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvboolean")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvboolean
              (id,cluster_id,dvboolean_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvcounts
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvcount")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvcount
              (id,cluster_id,dvcount_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvlink
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvlink")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvlink
              (id,cluster_id,dvlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvfile
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvfile")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvfile
              (id,cluster_id,dvfile_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvordinals
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvordinal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvordinal
              (id,cluster_id,dvordinal_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvquantities
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvquantity")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvquantity
              (id,cluster_id,dvquantity_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvratio
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvratio")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvratio
              (id,cluster_id,dvratio_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvstrings
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvstring")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvstring
              (id,cluster_id,dvstring_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#dvtemporals
curMLHIM.execute("SELECT *  from ccdgen_cluster_dvtemporal")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_cluster_dvtemporal
              (id,cluster_id,dvtemporal_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#Partys
print("Adding Partys")
curMLHIM.execute("SELECT *  from ccdgen_party")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    details = line[16]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,details,''))

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
    data.append((pk,dv_id,pobj_id))

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
    data.append((pk,party_id,link_id))

query = ("INSERT INTO dmgen_party_external_ref (id,party_id,dvlink_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#Participation
print("Adding Participations")
curMLHIM.execute("SELECT *  from ccdgen_participation")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    performer = line[16]
    function = line[17]
    mode = line[18]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,
                          performer,function,mode,''))

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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_participation_pred_obj (id,participation_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#Attestations
print("Adding Attestations")
curMLHIM.execute("SELECT *  from ccdgen_attestation")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    view = line[16]
    proof = line[17]
    reason = line[18]
    committer = line[19]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,
                          view,proof,reason,committer,''))

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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_attestation_pred_obj (id,attestation_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()

#Audits
print("Adding Audits")
curMLHIM.execute("SELECT *  from ccdgen_audit")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
    descr = line[7]
    asserts = line[9]
    lang = line[10]
    creator_id = line[11]
    edited_by = line[12]
    sysid = line[16]
    sysuser = line[17]
    location = line[18]

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,
                          sysid,sysuser,location,''))

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
    data.append((pk,dv_id,pobj_id))

query = ("INSERT INTO dmgen_audit_pred_obj (id,audit_id,predobj_id) VALUES(%s,%s,%s)")
curS3M.executemany(query, data)
S3M.commit()


#AdminEntry
print("Adding AdminEntrys")
curMLHIM.execute("SELECT *  from ccdgen_adminentry")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0]
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
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

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,
                          language,encoding,state,entrydata,subject,provider,protocol,workflow,audit,attestation,''))

query = ("""INSERT INTO dmgen_entry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#links
curMLHIM.execute("SELECT *  from ccdgen_adminentry_links")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_entry_links
              (id,entry_id,dvlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#participations
curMLHIM.execute("SELECT *  from ccdgen_adminentry_participations")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_entry_participations
              (id,entry_id,participation_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_adminentry_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0],line[1],line[2]))

query = ("""INSERT INTO dmgen_entry_pred_obj
              (id,entry_id,predobj_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#CareEntry
print("Adding CareEntrys")
curMLHIM.execute("SELECT *  from ccdgen_careentry")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0] + 100
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
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

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,
                          language,encoding,state,entrydata,subject,provider,protocol,workflow,audit,attestation,''))

query = ("""INSERT INTO dmgen_entry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#links
curMLHIM.execute("SELECT *  from ccdgen_careentry_links")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0]+100,line[1]+100,line[2]))

query = ("""INSERT INTO dmgen_entry_links
              (id,entry_id,dvlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#participations
curMLHIM.execute("SELECT *  from ccdgen_careentry_participations")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0]+100,line[1]+100,line[2]))

query = ("""INSERT INTO dmgen_entry_participations
              (id,entry_id,participation_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_careentry_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0]+100,line[1]+100,line[2]))

query = ("""INSERT INTO dmgen_entry_pred_obj
              (id,entry_id,predobj_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#DemographicEntry
print("Adding DemographicEntrys")
curMLHIM.execute("SELECT *  from ccdgen_demographicentry")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    pk = line[0] + 200
    prj = line[1]
    label = line[2]
    ct_id = line[3]
    created = line[4]
    updated = line[5]
    published = line[6]
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

    data.append((pk,prj,label,ct_id,created,updated,False,descr,asserts,lang,creator_id,edited_by,
                          language,encoding,state,entrydata,subject,provider,protocol,workflow,audit,attestation,''))

query = ("""INSERT INTO dmgen_entry
              (id,project_id,label,ct_id,created,updated,published,description,asserts,lang,creator_id,edited_by_id,
              language,encoding,state,data_id,subject_id,provider_id,protocol_id,workflow_id,audit_id,attestation_id,schema_code)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#links
curMLHIM.execute("SELECT *  from ccdgen_demographicentry_links")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0]+200,line[1]+200,line[2]))

query = ("""INSERT INTO dmgen_entry_links
              (id,entry_id,dvlink_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

#participations
curMLHIM.execute("SELECT *  from ccdgen_demographicentry_participations")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0]+200,line[1]+200,line[2]))

query = ("""INSERT INTO dmgen_entry_participations
              (id,entry_id,participation_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()

curMLHIM.execute("SELECT *  from ccdgen_demographicentry_pred_obj")
rowsMLHIM = curMLHIM.fetchall()
data = []

for line in rowsMLHIM:
    data.append((line[0]+200,line[1]+200,line[2]))

query = ("""INSERT INTO dmgen_entry_pred_obj
              (id,entry_id,predobj_id)
              VALUES(%s,%s,%s)""")
curS3M.executemany(query, data)
S3M.commit()


#Close all
print("\nFinished copying.")

curMLHIM.close()
print("Cleaning the dmgen DB")
S3M.set_isolation_level(0)
curS3M.execute("VACUUM FULL ANALYZE")
curS3M.close()

MLHIM.close()
S3M.close()

print("\n\n**** All Done! ****\n\n")
