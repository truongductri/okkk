import re
import sys
from pymongo import MongoClient
import datetime
import threading

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
def track_load_page(app_name,schema,page,username):
    import inspect
    import datetime
    import logging
    name = inspect.stack()[0][3]
    caller =inspect.stack()[1][3]
    time = datetime.datetime.now()
    utc_time =datetime.datetime.utcnow()
    def runner():
        try:
            ret= _coll.insert_one({
                "track_name":name,
                "track_caller":caller,
                "username":username,
                "page":page,
                "track_on":time,
                "track_utc_on":utc_time,
                "app":app_name,
                "schema":schema

            })
            x=ret
        except Exception as ex:
            logging.debug("tracking error",ex)


    import threading
    th = threading.Thread(target=runner)
    th.start()
def track_call_api_before(app_name,schema,data,username):
    from quicky import api
    import inspect
    import datetime
    import logging
    caller = inspect.stack()[1][3]
    time = datetime.datetime.now()
    utc_time = datetime.datetime.utcnow()
    from bson import ObjectId
    rec_id = ObjectId()

    def runner():
        import json
        try:
            _data =json.loads(data)
            api_path = api.get_api_path(_data["path"])
            ret= _coll.insert_one({
                "_id":rec_id,
                "track_name":"track_call_api",
                "track_caller":caller,
                "api":api_path,
                "username":username,
                "page":_data.get("view",_data.get("function_id","<unknown>")),
                "track_on":time,
                "track_utc_on":utc_time,
                "app":app_name,
                "schema":schema,
                "post_data":_data["data"]
            })
            x=ret
        except Exception as ex:
            logging.debug("tracking error",ex)


    import threading
    th = threading.Thread(target=runner)
    th.start()
    return rec_id
def track_call_api_after(app_name,schema,rec_id,data,username):
    from quicky import api
    import inspect
    import datetime
    import logging
    import time
    caller = inspect.stack()[1][3]
    time = datetime.datetime.now()
    utc_time = datetime.datetime.utcnow()
    from bson import ObjectId


    def runner():
        import json
        try:
            _data = json.loads(data)
            ret = _coll.update_one({
                "_id":rec_id},
                {
                    "$set":{
                        "get_data":_data
                    }
                }
            )
            x = ret
        except Exception as ex:
            logging.debug("tracking error", ex)
    import threading
    th = threading.Thread(target=runner)
    th.start()