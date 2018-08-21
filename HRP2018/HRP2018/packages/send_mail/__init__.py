import pymongo
import threading
import os
import logging
import re
import pystache
from pymongo import mongo_client
import datetime


template_dir=None
coll_items=None #collection contains email content will be sent
coll_attachment=None #collection contains attachment of email content will be sent
coll_email_template_name=None #collection contains template of email content will be sent
db=None

global lock
lock=threading.Lock()
cach={}
def raise_not_implement_error():
    raise (Exception("\n"
                     "It look like you forgot call set_config for '{0}'\n"
                     "\t How to set config for '{0}'?\n"
                     "\t call set_config(\n"
                     "\t\t host=your mongodb host server here,\n"
                     "\t\t port=your mongodb port here,\n"
                     "\t\t name=your db name here,\n"
                     "\t\t user=username,\n"
                     "\t\t password=passworsd,\n"
                     "\t\t collection= collection contains rendered email item before send,\n"
                     "\t\t collection_template=template email of each customer storage collection,\n"
                     "\t\t collection_attachment=collection contains attachment\n,"
                     "\t\t default_template_dir=path to directory contains default template email)"
                     .format(__name__)))
def raise_help():
    raise (Exception("\n"
                     "Follow below instruction to call set_config '{0}'\n"
                     "\t How to set config for '{0}'?\n"
                     "\t call set_config(\n"
                     "\t\t host=your mongodb host server here,\n"
                     "\t\t port=your mongodb port here,\n"
                     "\t\t name=your db name here,\n"
                     "\t\t user=username,\n"
                     "\t\t password=passworsd,\n"
                     "\t\t collection= collection contains rendered email item before send,\n"
                     "\t\t collection_template=template email of each customer storage collection,\n"
                     "\t\t collection_attachment=collection contains attachment\n,"
                     "\t\t default_template_dir=path to directory contains default template email)"
                     .format(__name__)))

def set_config(*args,**kwargs):
    params=args
    global template_dir
    global coll_items
    global coll_attachment
    global coll_email_template_name
    global db
    if args==() and kwargs==None:
        raise_help()
        return
    elif type(kwargs) is dict:
        params=kwargs
    elif type(args) is tuple:
        params=args[0]
    for x in ["host",
              "port",
              "name",
              "user",
              "password",
              "collection",
              "default_template_dir",
              "collection_template",
              "collection_attachment"]:
        if not params.has_key(x):
            raise_help()
    cnn=mongo_client.MongoClient(host=params["host"],port=params["port"])
    db=cnn.get_database(params["name"])
    db.authenticate(params["user"],params["password"])
    coll_items=db.get_collection(params['collection'])
    coll_email_template_name=params["collection_template"]
    coll_attachment=db.get_collection(params["collection_attachment"])

    if not os.path.exists(os.getcwd()+os.sep+params["default_template_dir"]):
        raise (Exception("'{0}' was not found".format(os.getcwd()+os.sep+params["default_template_dir"])))
    template_dir=os.getcwd()+os.sep+params["default_template_dir"]
def get_raw_schema_from_object(obj,field=None):
    """Genarate schema from dictionary. The schema will support for template email editor\n
       Example:
             the tamplate may be contains variable in schema
             Dear ${username},
             ....
    """
    ret=[]
    if type(obj) is list and obj.__len__()>0:
        return get_raw_schema_from_object(obj[0])
    for key in obj.keys():
        if type(obj[key]) is dict:
            k=get_raw_schema_from_object(obj[key],key)
            for x in k:
                if field!=None:
                    ret.append(field+"."+ x)
                else:
                    ret.append(x)
        else:
            if field!=None:
                ret.append(field+"."+key)
            else:
                ret.append(key)
    return ret


def get_template(customer_schema,
                template,
                default_subject,
                default_body,
                sample_object={}):
    ret=dict(
        subject="",
        body=""
    )
    global cach
    key="customer={0};template={1}".format(customer_schema,template)
    if cach.has_key(key):
        return cach[key]
    else:
        lock.acquire()
        try:
            coll=db.get_collection(customer_schema+"."+coll_email_template_name)

            item= coll.find_one({
                "template_name":{
                    "$regex":re.compile("^"+template+"$",re.IGNORECASE)
                }
            })
            if item==None:
                if not os.path.exists(template_dir + os.sep +template):
                    os.makedirs(template_dir + os.sep +template)
                subject_file_path=template_dir + os.sep +template+os.sep+"subject.txt"
                if not os.path.exists(subject_file_path):
                    file=open(subject_file_path,"w")
                    file.write(default_subject)

                    file.close()
                    ret["subject"] = default_subject
                else:
                    file = open(subject_file_path,"r")
                    ret["subject"]=file.read()
                    file.close()
                body_file_path=template_dir + os.sep +template+os.sep+"body.txt"
                if not os.path.exists(body_file_path):
                    file=open(body_file_path,"w")
                    file.write(default_body)
                    file.close()
                    ret["body"] = default_body
                else:
                    file = open(body_file_path,"r")
                    ret["body"]=file.read()
                    file.close()

                schema_file_path=template_dir + os.sep +template+os.sep+"schema.txt"
                if not os.path.exists(schema_file_path):
                    file=open(schema_file_path,"w")
                    file.write("-------------------------------------------\n"
                               "This template is contain schema data will be embeded into template email '{0}'\n"
                               "----------------------------------------------------\n".format(template))
                    for x in get_raw_schema_from_object(sample_object):
                        file.write(x+"\n")
                    file.close()
                coll.insert_one({
                    "template_name":template,
                    "subject":ret["subject"],
                    "body":ret["body"],
                    "schema":get_raw_schema_from_object(sample_object)
                })
                cach[key] = ret
            else:
                ret["subject"]=item["subject"]
                ret["body"]=item["body"]
                cach[key]=ret
            lock.release()
            return cach[key]
        except Exception as ex:
            lock.release()
            logging.error(ex)
            raise ex


def send(
        mail_to,#Email will send
        customer_schema, #the schema of customer that contains template email
        template, #template email directory if not exist directory will bw genarate with tp
        default_subject,
        default_body,
        data={},
        cc_to=None,
        attachment=None,
):
    template_email=get_template(customer_schema,template,default_subject,default_body,data)
    subject=pystache.render(template_email["subject"], data)
    body=pystache.render(template_email["body"], data)
    coll_items.insert_one({
        "customer_schema":customer_schema,
        "subject":subject,
        "body":body,
        "mail_to":mail_to,
        "cc_to":cc_to,
        "data":data,
        "created_on":datetime.datetime.now(),
        "created_on_utc": datetime.datetime.utcnow(),
        "sent_on":None,
        "sent_on_utc": None,
        "has_error":False,
        "sent_error":None

    })





