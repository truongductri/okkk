# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import quicky
from quicky import encryptor
from qmongo import helpers
import qmongo
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
import uuid
import threading
logger = logging.getLogger(__name__)

__collectionName = ''
__collection = {}
__transaction_collection = None

def generate_guid():
    return str(uuid.uuid4())

def get_collection(col_name):
    return models.db_context.db.get_collection(quicky.tenancy.get_schema() + "." + col_name)

def get_db_context():
    return models.db_context.db

def get_current_schema():
    return quicky.tenancy.get_schema()

def get_collection_name_with_schema(col_name):
    return quicky.tenancy.get_schema() + "." + col_name

def create_session(coll):
    session = coll.client.start_session()
    return session

def start_transaction(session):
    session.start_transaction(
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern(w="majority"))
    return session

def abort_transaction(session):
    session.abort_transaction()
    return  session

def end_session(session):
    session.end_session()

def commit_transaction(session):
    session.commit_transaction()

def get_user_id():
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    return user

def get_pagination(args):
    try:
        global __collectionName 
        global __collection 

        if('collection' in args['data'].keys()):
            __collectionName    =   args['data']['collection']
            __collection        =   getattr(models, __collectionName)()
            pageIndex           =   args['data'].get('pageIndex', 0)
            pageSize            =   args['data'].get('pageSize', 20)
            where               =   args['data'].get('where', '')
            sort                =   args['data'].get('sort', {})
            return get_data(pageIndex, pageSize, where, sort)
        return {"error":"Not found collection name"}

    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def get_data(pageIndex, pageSize, where, sort):
    try:
        global __collection
        _Sort   =   (lambda x: x if x != None else {})(sort)
        item    =   __collection.aggregate()
        if(where != ''):
            item.match(where)
            if _Sort != {}:
                item.sort(_Sort)
        return item.get_page((lambda pIndex: pIndex if pIndex != None else 0)(pageIndex),\
                            (lambda pSize: pSize if pSize != None else 20)(pageSize))
    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def get_config(args):
    try:
        return models.HCSSYS_SystemConfig().aggregate().get_list()[0]
    except Exception as ex:
        logger.debug(ex)
        raise(ex)

def filter_lock(collection, args):
    try:
        return filter_data(collection, args, "lock")
    except Exception as ex:
        raise ex

def filter_stop(collection, args):
    try:
        return filter_data(collection, args, "stop")
    except Exception as ex:
        raise ex

def filter_data(collection, args, column_name):
    if args['data'].has_key(column_name) and args['data'][column_name] != None and args['data'][column_name] != "":
            if int(args['data'][column_name]) == 0:
                collection.match(column_name + " != {0}", True)
            elif int(args['data'][column_name]) == 1:
                collection.match(column_name + " == {0}", True)
    return collection

def get_dropdown_list(args):
    return create_data_combobox(args)

def get_combobox_data(args):
    return create_data_combobox(args)

def get_init_data_combobox(args):
    #Hàm get data init cho combobox
    if args['data'] != None:
        result = []
        if args['data'].has_key('name'):
            list_name = args["data"].get("name", None)
            if list_name != None:
                try:
                    if type(list_name) is list:
                        for x in list_name:
                            result.append({
                                "key":x['key'],
                                "value":None,
                                "code":x['code'],
                                "name":encryptor.get_value(x['key']),
                                "display_fields":[],
                                "caption_field":"",
                                "alias": (lambda x: x['alias'] if x.has_key('alias') else "")(x)
                                })
                        for x in result:
                            display_fields = [[]]
                            caption_field = [[]]
                            x['value'] = create_data_init_combobox(dict(data = {"key":x["key"], "code":x["code"]}), display_fields, caption_field)
                            x['display_fields'] = display_fields[0]
                            x['caption_field'] = caption_field[0]

                        return result
                    else:
                        display_fields = [[]]
                        caption_field = [[]]
                        return {
                            "key": args["data"].get("name", "")["key"],
                            "value": create_data_init_combobox(dict(data = {"key":args["data"].get("name", "")["key"], "code":args["data"].get("name", "")["code"]}), display_fields, caption_field),
                            "code": args["data"].get("name", "")["code"],
                            "name":encryptor.get_value(args["data"].get("name", "")['key']),
                            "display_fields": display_fields[0],
                            "caption_field": caption_field[0],
                            "alias":(lambda x: x['alias'] if x.has_key("alias") else "")(args["data"].get("name", ""))
                            }
                except Exception as ex:
                    logger.debug(ex)
                    return {"value": None, "error": ex.message}
            else:
                return {
                    "error":"name is not empty"
                    }

def create_data_init_combobox(args, display_field, caption_field):
    try:
        global __collectionName 
        global __collection 

        ret      = {}
        ret_list = []

        if (args['data'] != None) or (not args['data'].has_key('key')) or (args['data']['key'] == ""):

            combobox_code = encryptor.get_value(args['data']['key'])

            combobox_info = models.HCSSYS_ComboboxList().aggregate().project(
                combobox_code       =   1,
                language            =   1,
                display_name        =   1,
                description         =   1,
                table_name          =   1,
                table_fields        =   1,
                display_fields      =   1,
                predicate           =   1,
                value_field         =   1,
                caption_field       =   1,
                sorting_field       =   1,
                filter_field        =   1,
                multi_select        =   1,
                page_size           =   1)

            language_code = quicky.applications.get_settings().LANGUAGE_CODE
            combobox_info = combobox_info.match("combobox_code == {0} and language == {1}", combobox_code, language_code).get_item()

            if combobox_info == None:
                return {"error":"combobox not defined"}

            __collectionName = combobox_info['table_name']
            display_field[0] = combobox_info['display_fields']
            caption_field[0] = combobox_info['caption_field']

            try:
                __collection = getattr(models, __collectionName)()
            except Exception as ex:
                return {"error":"Not found collection name"}



            column    = combobox_info['table_fields']
            multi     = combobox_info['multi_select']

            if column != []:
                try:
                    dict_column = dict()
                    for x in column:
                        dict_column.update({x:1})
                    ret = __collection.aggregate().project(dict_column)
                except Exception as ex:
                    raise(Exception("column not exist in collection"))
            else:
                raise(Exception("Not found column name"))

            if args['data'].has_key('code'):
                if multi == True:
                    ret.match(combobox_info['value_field'] + " in {0}", args['data']['code'])
                else:
                    ret.match(combobox_info['value_field'] + " == {0}", args['data']['code'])

            if multi == True:
                return ret.get_list()
            else:
                return ret.get_item()

        raise(Exception("Not found collection name"))

    except Exception as ex:
        logger.debug(ex)
        return {"data": None, "error": ex.message}

def create_data_combobox(args):
    #Hàm get dropdown list theo tên collection và tên cột
    try:
        global __collectionName 
        global __collection 

        ret      = {}
        ret_list = []

        if (args['data'] != None) or (not args['data'].has_key('key')) or (args['data']['key'] == ""):

            combobox_code = encryptor.get_value(args['data']['key'])

            combobox_info = models.HCSSYS_ComboboxList().aggregate().project(
                combobox_code       =   1,
                language            =   1,
                display_name        =   1,
                description         =   1,
                table_name          =   1,
                table_fields        =   1,
                display_fields      =   1,
                predicate           =   1,
                value_field         =   1,
                caption_field       =   1,
                sorting_field       =   1,
                filter_field        =   1,
                multi_select        =   1,
                page_size           =   1)

            language_code = quicky.applications.get_settings().LANGUAGE_CODE
            combobox_info = combobox_info.match("combobox_code == {0} and language == {1}", combobox_code, language_code).get_item()

            if combobox_info == None:
                return {"error":"combobox not defined"}

            __collectionName = combobox_info['table_name']

            try:
                __collection = getattr(models, __collectionName)()
            except Exception as ex:
                return {"error":"Not found collection name"}

            column    = combobox_info['table_fields']
            where     = combobox_info['predicate']
            sort      = combobox_info['sorting_field']
            filter    = []
            page_size = 30

            if combobox_info.has_key("filter_field"):
                filter = combobox_info['filter_field']

            if combobox_info.has_key("page_size"):
                page_size = combobox_info['page_size']

            if column != []:
                try:
                    dict_column = dict()
                    for x in column:
                        dict_column.update({x:1})
                    if where.has_key("column") and (where.get('column', None) != None and len(where.get('column', None)) > 0):
                        for x in where['column']:
                            dict_column.update({x:1})
                    ret = __collection.aggregate().project(dict_column)
                except Exception as ex:
                    raise(Exception("column not exist in collection"))
            else:
                raise(Exception("Not found column name"))

            #predicate
            if where.has_key('operator') and \
               (where.get('column', None) != None and\
               len(where.get('column', None)) > 0) and\
               where.get('operator', '') != "":
                try:
                    if args['data'].has_key('value') and args['data'].get('value', None) != None and type(args['data']['value']) is list:
                        dict_where = dict()
                        for x in args['data']['value']:
                            new_key    = x.keys()[0].replace("@", "")
                            old_key    = x.keys()[0]
                            x[new_key] = x.pop(old_key)
                            dict_where.update(x)

                        ret.match(where['operator'], dict_where)
                        if args['data'].has_key('code') and args['data'].get('code', None) != None and args['data']['code'] != "":
                            ret.match(combobox_info['value_field'] + " == {0}", args['data']['code'])
                    else:
                        ret.match(where['operator'])

                except Exception as ex:
                    raise(Exception("syntax where error"))

            #filter with text from browser
            if args['data'].has_key('search') and args['data'].get('search', None) != None and args['data']['search'] != "":
                if len(filter) > 0:
                    filter_query = ""
                    filter_dict = dict()
                    for i in range(len(filter)):
                        if i == (len(filter) - 1):
                            filter_query += "contains(" + filter[i] + ", " + "@" + filter[i] + ")"
                        else:
                            filter_query += "contains(" + filter[i] + ", " + "@" + filter[i] + ") or "
                        filter_dict.update({filter[i].format() : args['data']['search']})

                    ret.match(filter_query, filter_dict)

            if sort != {}:
                try:
                    ret.sort(sort)
                except Exception as ex:
                    raise(Exception("syntax sort error"))

            #Pagination
            page_index = 0
            data = dict()
            if args['data'].has_key('pageIndex') and args['data'].get('pageIndex', None) != None:
                page_index = args['data']['pageIndex']

            data = ret.get_page(page_index, page_size)

            if data != {}:
                for y in where['column']:
                    for x in data['items']:
                        if y not in data['items'][0].keys():
                            del x[y.format()]

            ret_list = data


            return {"data"           : ret_list,
                    "display_name"   : combobox_info["display_name"],
                    "display_fields" : combobox_info["display_fields"],
                    "value_field"    : combobox_info["value_field"],
                    "caption_field"  : combobox_info["caption_field"],
                    "sorting_field"  : combobox_info["sorting_field"],
                    "filter_field"   : combobox_info["filter_field"],
                    "page_size"      : combobox_info["page_size"],
                    "error"          : None}
        raise(Exception("Not found collection name"))

    except Exception as ex:
        logger.debug(ex)
        return {"data": None, "error": ex.message}
