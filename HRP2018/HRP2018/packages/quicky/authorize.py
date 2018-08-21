from pymongo import MongoClient
from . import dict_utils
import threading
import logging
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
_view_cache={}
_coll_of_views = None
_coll_of_roles = None
_coll_of_user_role= None
_privileges_cache={}
import datetime
_db=None
def set_config(*args,**kwargs):

    """
    Set database config for authorization
    Example: set_config(
                        host=...,
                        port=...,
                        name=..database name,
                        user=....
                        password=...)
    :param args:
    :param kwargs:
    :return:
    """
    try:
        global _db
        global _coll_of_views
        global _coll_of_roles
        if type(args) is tuple and args.__len__() > 0:
            args = args[0]
        else:
            args = kwargs
        if not dict_utils.has_key(args,"host"):
            raise Exception("'host' was not found")
        if not dict_utils.has_key(args,"port"):
            raise Exception("'port' was not found")
        if not dict_utils.has_key(args,"name"):
            raise Exception("'name' was not found")
        if not dict_utils.has_key(args,"schema"):
            raise Exception("'schema' was not found")
        if _db == None:
            cnn = MongoClient(host=args["host"], port=args["port"])
            _db = cnn.get_database(args["name"])
            if dict_utils.has_key(args,"user") and (args["user"] != "" or args["user"] != None):
                _db.authenticate(args["user"], args["password"])
        _coll_of_views = _db.get_collection( "{0}.views".format(args["schema"]))
        _coll_of_roles = _db.get_collection("{0}.roles".format(args["schema"]))
    except Exception as ex:
        logger.debug(ex)
        raise ex


def register_view(*args,**kwargs):
    # type: (dict) -> dict
    """
    Regist a new view example register_view(
                        view=...view name,
                        app= ... appname)
    :param args:
    :param kwargs:
    :return:
    """
    try:
        if type(args) is tuple and args.__len__() > 0:
            args = args[0]
        else:
            args = kwargs
        if not dict_utils.has_key(args,"app"):
            raise Exception("'app' was not found")
        if not dict_utils.has_key(args,"view"):
            raise Exception("'view' was not found")
        key = "{0}/{1}".format(args["app"], args["view"]).lower()
        if not dict_utils.has_key(_view_cache,key):
            lock.acquire()
            try:
                item = _coll_of_views.find_one({
                    "View": args["view"],
                    "App": args["app"]
                })
                ret_id = None
                if item == None:
                    ret = _coll_of_views.insert_one({
                        "View": args["view"],
                        "App": args["app"],
                        "CreatedOn": datetime.datetime.now(),
                        "CreatedOnUTC": datetime.datetime.utcnow()
                    })
                    _view_cache.update({
                        key: ret.inserted_id.__str__()
                    })
                else:
                    _view_cache.update({
                        key: item["_id"].__str__()
                    })
                lock.release()
                return _view_cache[key]
            except Exception as ex:
                lock.release()
                logger.debug(ex)
                raise (ex)
    except Exception as ex:
        logger.debug(ex)
        raise ex

def get_privileges_of_user(*args,**kwargs):
    global _privileges_cache
    import re
    from django.contrib.auth.models import User
    import django.core.exceptions
    if args.__len__() == 0:
        args =kwargs
    if not dict_utils.has_key(args,"username"):
        raise ("'username' was not found")
    if not dict_utils.has_key(args,"app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args,"view"):
        raise ("'view' was not found")
    if not dict_utils.has_key(args,"schema"):
        raise ("'schema' was not found")
    key="username={0};app={1};view={2};schema={3}".format(
        args["username"],
        args["app"],
        args["view"],
        args["schema"],
    ).lower()
    if dict_utils.has_key(_privileges_cache,key):
        return _privileges_cache[key]
    else:

        try:
            try:
                user=User.objects.get(username=args["username"], schema=args["schema"])
            except django.core.exceptions.ObjectDoesNotExist as ex:

                return None
            if user.is_superuser:
                return dict(
                    isFull=True
                )
            else:
                lock.acquire()
                try:
                    roles =list(_coll_of_roles\
                        .aggregate([
                        {
                            "$match":{
                                "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE)
                            }
                        },{
                            "$unwind":"$apps"
                        },{
                            "$match": {
                                "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE)
                            }
                        },{
                            "$unwind": "$apps.views"
                        },{
                            "$match": {
                                "apps.views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
                            }
                        },{
                            "$unwind":"$apps.views.users"
                        },{
                            "$match": {
                                "apps.views.users.username":re.compile(r"^"+args["username"]+"$",re.IGNORECASE)
                            }
                        }
                    ]))
                    if roles.__len__() == 0:
                        lock.release()
                        return None
                    else:
                        if roles[0]["apps"]["views"]["users"].get("privileges",None) == None:
                            lock.release()
                            return None
                        else:
                            _privileges_cache[key]=roles[0]["apps"]["views"]["users"]["privileges"]
                            lock.release()
                            return _privileges_cache[key]
                except Exception as ex:
                    lock.release()
                    raise (ex)
        except Exception as ex:
            raise (ex)

def create_role(*args,**kwargs):
    import re
    if args.__len__() == 0:
        args =kwargs
    if not dict_utils.has_key(args,"role"):
        raise ("'role' was not found")
    if not dict_utils.has_key(args,"app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args,"schema"):
        raise ("'schema' was not found")
    role=_coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
    })
    if role == None:
        _coll_of_roles.insert_one({
            "schema":args["schema"],
            "role":args["role"],
            "apps":[{"name":args["app"].lower()}],
            "createdOn":datetime.datetime.now(),
            "createdBy":"application"
        })
    else:
        _coll_of_roles.update_one({
            "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
            "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
        },{
            "$push":{
                "apps":{
                    "name":args["app"].lower(),
                    "createdOn": datetime.datetime.now(),
                    "createdBy": "application"
                }
            }
        })


def add_view_to_role(*args,**kwargs):
    import re
    if args.__len__() == 0:
        args = kwargs
    if not dict_utils.has_key(args, "role"):
        raise ("'role' was not found")
    if not dict_utils.has_key(args, "app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args, "schema"):
        raise ("'schema' was not found")
    if not dict_utils.has_key(args, "view"):
        raise ("'view' was not found")
    role = _coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)
    })
    if role == None:
        _coll_of_roles.insert_one({
            "schema":args["schema"],
            "role":args["role"],
            "apps":[],
            "createdOn": datetime.datetime.now(),
            "createdBy": "application"
        })
    else:

        qr_get_index_of_app=_coll_of_roles.aggregate([
            {
                "$match":{
                    "role":re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
                    "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                }
            },
            {
                "$project":{
                    "index": {"$indexOfArray": ["$apps.name", args["app"].lower()]}
                }
            }
        ])
        lst_index_of_app=list(qr_get_index_of_app)
        index_of_app=lst_index_of_app[0]["index"]
        if index_of_app ==-1:
            _coll_of_roles.update_one({
                "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)
            },{
                "$set":{
                    "apps":[{
                        "name":args["app"].lower(),
                        "createdOn":datetime.datetime.now(),
                        "createdBy":"application",
                        "views":[]
                    }]
                }
            })
            index_of_app=0
        qr_get_index_of_view = _coll_of_roles.aggregate([
            {
                "$match": {
                    "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
                    "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                }
            },{
                "$unwind":"$apps"
            },{
                "$match":{
                    "apps.name":re.compile(r"^" + args["app"] + "$", re.IGNORECASE)
                }
            },
            {
                "$project": {
                    "index": {"$indexOfArray": ["$apps.views.name", args["view"].lower()]}
                }
            }
        ])
        lst_index_of_view=list(qr_get_index_of_view)
        index_of_view = lst_index_of_view[0]["index"]
        if index_of_view == None:
            index_of_view=-1
        if index_of_view == -1:
            _coll_of_roles.update_one({
                "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)
            },{
                "$push":{
                    "apps."+index_of_app.__str__()+".views":{
                        "name":args["view"].lower(),
                        "createdOn":datetime.datetime.now(),
                        "createBy":"application",
                        "users":[]
                    }
                }
            })
            index_of_view = 0

def add_user_to_view(*args,**kwargs):
    import re
    if args.__len__() == 0:
        args = kwargs
    if not dict_utils.has_key(args, "role"):
        raise ("'role' was not found")
    if not dict_utils.has_key(args, "app"):
        raise ("'app' was not found")
    if not dict_utils.has_key(args, "schema"):
        raise ("'schema' was not found")
    if not dict_utils.has_key(args, "view"):
        raise ("'view' was not found")
    if not dict_utils.has_key(args, "username"):
        raise ("'username' was not found")
    if not dict_utils.has_key(args, "privileges"):
        raise ("'privileges' was not found")
    if not dict_utils.has_key(args["privileges"], "isFull"):
        raise ("'privileges.isFull' was not found")
    if not dict_utils.has_key(args["privileges"], "allowInsert"):
        raise ("'privileges.allowInsert' was not found")
    if not dict_utils.has_key(args["privileges"], "allowUpdate"):
        raise ("'privileges.allowUpdate' was not found")
    if not dict_utils.has_key(args["privileges"], "allowDelete"):
        raise ("'privileges.allowDelete' was not found")
    role = _coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)
    })
    if role == None:
        create_role(
            role=args["role"],
            app=args["app"],
            schema=args["schema"]
        )
    role = _coll_of_roles.find_one({
        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
        "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
        "apps.views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
    })
    if role == None:
        add_view_to_role(
            role=args["role"],
            app=args["app"].lower(),
            schema=args["schema"],
            view=args["view"].lower()
        )
    else:
        role_user = _coll_of_roles.find_one({
            "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
            "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
            "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
            "apps.views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE),
            "apps.views.users.username": re.compile(r"^" + args["view"] + "$", re.IGNORECASE),
        })
        if role_user == None:
            qr_index_app=_coll_of_roles.aggregate([
                {
                    "$match":{
                        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)
                    }
                },{
                    "$project": {
                        "index": {"$indexOfArray": ["$apps.name", args["app"].lower()]}
                    }
                }
            ])
            lst_index_app=list(qr_index_app)
            index_app=lst_index_app[0]["index"]
            qr_index_view = _coll_of_roles.aggregate([
                {
                    "$match": {
                        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)

                    }
                },{
                    "$unwind":"$apps"
                },{
                    "$match":{
                        "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE)
                    }
                },
                {
                    "$project": {
                        "index": {"$indexOfArray": ["$apps.views.name", args["view"].lower()]}
                    }
                }
            ])
            lst_index_view=list(qr_index_view)
            index_view=lst_index_view[0]["index"]
            qr_index_user = _coll_of_roles.aggregate([
                {
                    "$match": {
                        "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                        "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE)


                    }
                }, {
                    "$unwind": "$apps"
                },{
                    "$match": {
                        "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE)
                    }
                },{
                    "$unwind": "$views"
                },{
                    "$match":{
                        "apps.views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
                    }
                }, {
                    "$project": {
                        "index": {"$indexOfArray": ["$apps.views.users.name", args["username"].lower()]}
                    }
                }
            ])
            lst_index_user=list(qr_index_user)
            if lst_index_user.__len__() > 0:
                index_user=lst_index_user[0]["index"]
            else:
                index_user = -1
            if index_user == -1:
                _coll_of_roles.update_one({
                    "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                    "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
                    "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
                    "apps.views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
                },{
                    "$push":{
                        "apps."+index_app.__str__()+".views."+index_view.__str__()+".users":{
                            "username":args["username"].lower(),
                            "createdOn":datetime.datetime.now(),
                            "createdBy":"application",
                            "privileges":args["privileges"]
                        }
                    }
                })
            else:
                _coll_of_roles.update_one({
                    "schema": re.compile(r"^" + args["schema"] + "$", re.IGNORECASE),
                    "role": re.compile(r"^" + args["role"] + "$", re.IGNORECASE),
                    "apps.name": re.compile(r"^" + args["app"] + "$", re.IGNORECASE),
                    "apps.views.name": re.compile(r"^" + args["view"] + "$", re.IGNORECASE)
                }, {
                    "$set": {
                        "apps." + index_app.__str__() + ".views." + index_view.__str__() + ".users["+index_user+"]": {
                            "username": args["username"].lower(),
                            "createdOn": datetime.datetime.now(),
                            "createdBy": "application",
                            "privileges": args["privileges"]
                        }
                    }
                })





