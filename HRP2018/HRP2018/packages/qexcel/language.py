import re
import sys
from pymongo import MongoClient
import datetime

_coll=None
_db=None
_collection_name=None
def set_config(*args,**kwargs):
    global _coll
    global _db
    global _collection_name
    if type(args) is tuple and args.__len__()>0:
        args=args[0]
    else:
        args=kwargs
    if sys.version_info[0] <=2:
        if not args.has_key("host"):
            raise Exception("'host' was not found")
        if not args.has_key("port"):
            raise Exception("'port' was not found")
        if not args.has_key("name"):
            raise Exception("'name' was not found")
        if not args.has_key("collection"):
            raise Exception("'collection' was not found")
    else:
        if not args.__contains__("host"):
            raise Exception("'host' was not found")
        if not args.__contains__("port"):
            raise Exception("'port' was not found")
        if not args.__contains__("name"):
            raise Exception("'name' was not found")
        if not args.__contains__("collection"):
            raise Exception("'collection' was not found")
    if _coll==None:
        cnn=MongoClient(host=args["host"],port=args["port"])
        _db=cnn.get_database(args["name"])
        if sys.version_info[0]<=2:
            if args.has_key("user") and (args["user"]!="" or args["user"]!=None):
                _db.authenticate(args["user"],args["password"])
            _coll=_db.get_collection(args["collection"])
            _collection_name=args["collection"]
        else:
            if args.__contains__("user") and (args["user"]!="" or args["user"]!=None):
                _db.authenticate(args["user"],args["password"])
            _coll=_db.get_collection(args["collection"])
            _collection_name=args["collection"]

def get_columns(language,app_name,schema,source,cols):
    global _coll
    if _coll == None:
        raise (Exception("It looks like you forgot set 'DB_EXCEL_EXPORT_CONFIG' in settings.py"))
    columns =[]
    ord=1000
    for x in cols:
        if type(x) in [str,unicode]:
            columns.append(dict(
                field=x,
                caption=x,
                display_index=ord
            ))
        elif type(x) is dict:
            columns.append(dict(
                field=x.get("field"),
                caption=x.get("caption",x.get("field")),
                display_index=x.get("display_index",ord)
            ))
        ord += 1000
    qr=_coll.aggregate([
        {
            "$match":{
                "language":{"$regex": re.compile(r"^"+language+r"$",re.IGNORECASE)}
            }
        }
    ])
    items=list(qr)
    if items.__len__() == 0:
        _coll.insert_one({
            "language":language,
            "apps":[]
        })
    qr = _coll.aggregate([
        {
            "$match": {
                 "language":{"$regex": re.compile(r"^"+language+"$",re.IGNORECASE)}
            }
        },{
            "$project" : {
                "index" : {"$indexOfArray":["$apps.name", app_name.lower()]},
                "n_index":{"$size":"$apps"}
            }
        }
    ])
    items =list(qr)
    index_of_app =-1

    if items.__len__() > 0:
        index_of_app = items[0]["index"]
    if index_of_app == -1 :

        _coll.update_one({
            "language": {"$regex": re.compile(r"^" + language + "$", re.IGNORECASE)}
        }, {
            "$push": {
                "apps": {
                    "name": app_name.lower(),
                    "schema":[]
                }
            }
        })
        index_of_app = items[0]["n_index"]


    qr = _coll.aggregate([
        {
            "$match": {
                "language": {"$regex": re.compile(r"^"+ language+ "$", re.IGNORECASE)}
            }
        }, {
            "$unwind": "$apps"
        }, {
            "$match": {
                "apps.name": {"$regex": re.compile(r"^" + app_name + r"$", re.IGNORECASE)}
            }
        },{
            "$project":{
                "index":{"$indexOfArray":["$apps.schema.name", app_name.lower()]},
                "n_index":{"$size":"$apps.schema"}
            }
        }
    ])

    index_of_schema = -1

    items = list(qr)
    if items.__len__() >0 :
        index_of_schema =items[0]["index"]
    if index_of_schema == -1:
        _coll.update_one({
            "language": {"$regex": re.compile(r"^"+ language+ "$", re.IGNORECASE)}
        },{
            "$push":{
                "apps."+index_of_app.__str__()+".schema":{
                    "name":schema.lower(),
                    "source":[]
                }
            }
        })
        index_of_schema = items[0]["n_index"]

    qr = _coll.aggregate([
        {
            "$match": {
                "language": {"$regex": re.compile(r"^" + language + "$", re.IGNORECASE)}
            }
        }, {
            "$unwind": "$apps"
        }, {
            "$match": {
                "apps.name": {"$regex": re.compile(r"^" + app_name + r"$", re.IGNORECASE)}
            }
        }, {
            "$unwind": "$apps.schema"
        },{
            "$match": {
                "apps.schema.name": {"$regex": re.compile(r"^" + schema + r"$", re.IGNORECASE)}
            }
        }, {
            "$project": {
                "index": {"$indexOfArray": ["$apps.schema.source.name", source.lower()]},
                "n_index":{"$size":"$apps.schema.source"}
            }
        }
    ])

    index_of_source = -1

    items = list(qr)
    if items.__len__() > 0:
        index_of_source = items[0]["index"]
    if index_of_source == -1:
        _coll.update_one({
            "language": {"$regex": re.compile(r"^"+ language+ "$", re.IGNORECASE)}
        }, {
            "$push": {
                "apps." + index_of_app.__str__() + ".schema."+index_of_schema.__str__()+".source" : {
                     "name": source.lower(),
                     "columns": columns
                }
            }
        })
        index_of_source = items[0]["n_index"]
    else:
        qr_get_col = _coll.aggregate([
            {
                "$match": {
                    "language": {"$regex": re.compile(r"^" + language + "$", re.IGNORECASE)}
                }
            }, {
                "$unwind": "$apps"
            }, {
                "$match": {
                    "apps.name": {"$regex": re.compile(r"^" + app_name + r"$", re.IGNORECASE)}
                }
            }, {
                "$unwind": "$apps.schema"
            }, {
                "$match": {
                    "apps.schema.name": {"$regex": re.compile(r"^" + schema + r"$", re.IGNORECASE)}
                }
            },{
                "$unwind":"$apps.schema.source"
            }, {
                "$match": {
                    "apps.schema.source.name": {"$regex": re.compile(r"^" + source + r"$", re.IGNORECASE)}
                }
            }
        ])
        _cols =list(qr_get_col)
        __cols=_cols[0]["apps"]["schema"]["source"]["columns"]
        col_fields = [{x["field"]: x} for x in columns]
        _map_col ={}
        for x in col_fields:
            c_fields = [x for x in __cols if x["field"] == x.keys()[0]]

            if c_fields.__len__() >0:
                __cols.append(x.get(x.keys()[0]))


        _coll.update_one({
            "language": {"$regex": re.compile(r"^" + language + "$", re.IGNORECASE)}
        }, {
            "$set": {
                "apps." + index_of_app.__str__() + ".schema." + index_of_schema.__str__() + ".source."+index_of_source.__str__()+".columns":__cols

            }
        })
        return __cols
