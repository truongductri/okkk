# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_data():
    items = models.LMSLS_MaterialFolder().aggregate()
    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
    items.project(
        folder_id=1,
        folder_name=1,
        folder_name2=1,
        parent_id=1,
        parent_code=1,
        level=1,
        level_code=1,
        ordinal=1,
        lock=1,
        note=1,
        moderator_id=1,
        approver_id=1,
        active=1,
        permisions=1,
        approve_type=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    
    return items

def get_list(args):
    items = models.LMSLS_MaterialFolder().aggregate().project(
        folder_id = 1,
        folder_name = 1,
        parent_code = 1
        )
    
    return items.get_list()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=models.LMSLS_MaterialFolder().aggregate()
    ret.left_join(models.models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
            folder_id=1,
            folder_name=1,
            folder_name2=1,
            parent_id=1,
            parent_code=1,
            level=1,
            level_code=1,
            ordinal=1,
            lock=1,
            note=1,
            moderator_id=1,
            approver_id=1,
            active=1,
            permisions=1,
            approve_type=1,
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    
    if(where != None):
        ret.match("(level_code==@folder_id)",folder_id=where['folder_id'])

    if(searchText != None):
        ret.match("contains(folder_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    data = ret.get_page(pageIndex, pageSize)
    return  data

def get_list_with_select_node(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    collection = common.get_collection('LMSLS_MaterialFolder')
    where = args['data'].get('where')
    arrayData = []
    match = {}
    if(where['folder_id'] != None or searchText != None):
        match = {
                "$match": {
                }
            }
    if(where['folder_id'] != None):
        match["$match"]["level_code"] = where['folder_id']

    if(searchText != None):
        match["$match"]["folder_name"] = { "$regex": ".*" + searchText + "*" }

    if(where['folder_id'] != None or searchText != None):
        arrayData.append(match)

    lookup = {
        "$lookup":
            {
                "from":common.get_collection_name_with_schema("auth_user_info"), 
                "localField":'created_by', 
                "foreignField":'username', 
                "as":'us'}
        }
    arrayData.append(lookup)
    arrayData.append({
                "$project": {
                    "folder_id":1,
                    "folder_name":1,
                    "folder_name2":1,
                    "parent_id":1,
                    "parent_code":1,
                    "level":1,
                    "level_code":1,
                    "ordinal":1,
                    "lock":1,
                    "note":1,
                    "moderator_id":1,
                    "approver_id":1,
                    "active":1,
                    "permisions": 1,
                    "approve_type":1,
                    "created_on":1,
                    "created_by": "$us.login_account",
                    "modified_on":1,
                    "modified_by":1
                }
            })

    if(sort != None):
        arrayData.append({
            "$sort": sort    
        })
    ret=collection.aggregate(arrayData)
    return dict(
        items=list(ret),
        page_index=pageIndex,
        page_size=pageSize,
        total_items=list(ret).__len__()
    )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.LMSLS_MaterialFolder().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  models.LMSLS_MaterialFolder().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = get_list_data().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
                    )
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.LMSLS_MaterialFolder().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        parent_id            = (lambda x: x['parent_id']            if x.has_key('parent_id')           else None)(args['data']),
        parent_code          = (lambda x: x['parent_code']          if x.has_key('parent_code')         else None)(args['data']),
        folder_id            = (lambda x: x['folder_id']            if x.has_key('folder_id')           else None)(args['data']),
        folder_name          = (lambda x: x['folder_name']          if x.has_key('folder_name')         else None)(args['data']),
        folder_name2         = (lambda x: x['folder_name2']         if x.has_key('folder_name2')        else None)(args['data']),
        ordinal              = (lambda x: x['ordinal']              if x.has_key('ordinal')             else None)(args['data']),
        note                 = (lambda x: x['note']                 if x.has_key('note')                else None)(args['data']),
        lock                 = (lambda x: x['lock']                 if x.has_key('lock')                else False)(args['data']),
        approver_id          = (lambda x: x['approver_id']          if x.has_key('approver_id')         else None)(args['data']),
        active               = (lambda x: x['active']               if x.has_key('active')              else True)(args['data']),
        approve_type         = (lambda x: x['approve_type']         if x.has_key('approve_type')        else None)(args['data']),
        level                = (lambda x: x['level']                if x.has_key('level')               else None)(args['data']),
        level_code           = (lambda x: x['level_code']           if x.has_key('level_code')          else None)(args['data']),
        moderator_id         = (lambda x: x['moderator_id']         if x.has_key('moderator_id')        else None)(args['data']),
        permisions           = (lambda x: x['permisions']           if x.has_key('permisions')          else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['folder_id']
    return ret_dict
def get_level_code_by_folder_id(args):
    where = args['data'].get('where')
    ret=models.LMSLS_MaterialFolder().aggregate()
    if(where != None):
        ret.match("(folder_id==@folder_id)",folder_id=where['folder_id'])
    ret.project(
        level_code=1
        )
    return ret.get_page(0, 100)