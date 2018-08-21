# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
from Query import TMLS_Rank
import logging
import threading
import TMSYS_ConfigChangeObjectPriority
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=TMLS_Rank.display_list_rank()

    ret=common.filter_lock(ret, args)

    if(searchText != None  and searchText !=''):
        ret.match("contains(rank_code, @name) or contains(rank_name, @name)" + \
            "contains(rank_content, @name) or contains(total_from, @name)" + \
            "contains(total_to, @name) or contains(ordinal, @name)" ,name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def getListRankcode(args):
    ret=TMLS_Rank.display_list_rank()
    return ret.get_list()
def get_list_details_with_searchtext(args):

    if args['data'].has_key('rank_code'):
        rank_code = args['data']['rank_code']
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
        ret=TMLS_Rank.get_details(rank_code)
    
        #if(searchText != None):
        #    ret.match("contains(rank_code, @name)",name=searchText)

        if(sort != None):
            ret.sort(sort)

        return ret.get_page(pageIndex, pageSize)

    else:
        return dict(
            error = "rank_code is not exist"
        )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMLS_Rank().insert(data)
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
            ret  =  models.TMLS_Rank().update(
                data, 
                "rank_code == {0}", 
                args['data']['rank_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = TMLS_Rank.display_list_rank().match("rank_code == {0}", args['data']['rank_code']).get_item()
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
            ret  =  models.TMLS_Rank().delete("rank_code in {0}",[x["rank_code"]for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def insert_details(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data']['details'].has_key('rec_id'):
                if args['data'].has_key('rank_code') and args['data']['details'].has_key('change_object') and args['data']['details'].has_key('object_code'):
                    details = []
                    if type(args['data']['details']['object_code']) is list:
                        if len(args['data']['details']['object_code']) > 0:
                            for x in args['data']['details']['object_code']:
                                try:
                                    details.append(set_dict_detail_insert_data({
                                        "change_object":(lambda x: x['change_object'] if x.has_key('change_object') else None)(args['data']['details']),
                                        "object_code": x,
                                        "total_from":(lambda x: x['total_from'] if x.has_key('total_from') else None)(args['data']['details']),
                                        "total_to":(lambda x: x['total_to'] if x.has_key('total_to') else None)(args['data']['details']),
                                        "note":(lambda x: x['note'] if x.has_key('note') else None)(args['data']['details'])
                                        }, args['data'].has_key('rank_code')))
                                except Exception as ex:
                                    raise ex

                            collection  =  common.get_collection('TMLS_Rank')
                            for x in details:
                                check_exist = collection.find_one(
                                {
                                    "rank_code":args['data']['rank_code'], 
                                    "details":{
                                            "$elemMatch":{
                                                "change_object":x["change_object"],
                                                "object_code":x["object_code"]
                                                }
                                            }
                                    })
                                if check_exist != None:
                                    ret = {
                                        "error" : "duplicate",
                                        "item" : check_exist
                                    }
                                    break

                            if ret == {}:
                                for x in details:
                                    try:
                                        ret = TMLS_Rank.insert_details(args, x)
                                    except Exception as ex:
                                        raise ex
                            else:
                                lock.release()
                                return ret
                        else:
                            lock.release()
                            return dict(
                                error = "object_code is not empty"
                            )
                    else:
                        details = set_dict_detail_insert_data(args['data']['details'], args['data'].has_key('rank_code'))
                        ret = TMLS_Rank.insert_details(args, details)
                else:
                    lock.release()
                    return dict(
                        error = "request parameter is not enough"
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

def update_details(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            collection  =  common.get_collection('TMLS_Rank')
            if args['data']['details'].has_key('rec_id'):
                check_exist = collection.find_one(
                    {
                        "rank_code":args['data']['rank_code'], 
                        "details":{
                                "$elemMatch":{
                                    "change_object":args['data']['details']["change_object"],
                                    "object_code":args['data']['details']["object_code"]
                                    }
                             }
                     })
                if check_exist == None:
                    details = set_dict_detail_update_data(args['data']['details'], args['data']['rank_code'])
                    ret = TMLS_Rank.update_details(args, details)
                else:
                    ret = {
                            "error" : "duplicate",
                            "item" : check_exist
                        }

            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete_detail(args):
    try:
        lock.acquire()
        ret = {}
        error_message = None
        if args['data'] != None:
            if args['data'].has_key('rank_code'):
                if args['data'].has_key('rec_id'):
                    ret = TMLS_Rank.remove_details(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'rank_code' is not exist"

            lock.release()
            return dict(
                error = error_message
            )
        else:
            error_message = "request parameter is not exist"

        lock.release()
        return dict(
            error = error_message
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        rank_code         = (lambda x: x['rank_code']         if x.has_key('rank_code')        else None)(args['data']),
        rank_name         = (lambda x: x['rank_name']         if x.has_key('rank_name')        else None)(args['data']),
        rank_name2        = (lambda x: x['rank_name2']        if x.has_key('rank_name2')       else None)(args['data']),
        rank_content      = (lambda x: x['rank_content']      if x.has_key('rank_content')     else None)(args['data']),
        total_from        = (lambda x: x['total_from']        if x.has_key('total_from')       else None)(args['data']),
        total_to          = (lambda x: x['total_to']          if x.has_key('total_to')         else None)(args['data']),
        is_change_object  = (lambda x: x['is_change_object']  if x.has_key('is_change_object') else None)(args['data']),
        ordinal           = (lambda x: x['ordinal']           if x.has_key('ordinal')          else None)(args['data']),
        lock              = (lambda x: x['lock']              if x.has_key('lock')             else None)(args['data']),
        details           = (lambda x: x['details']           if x.has_key('details')          else [])(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['rank_code']
    del ret_dict['details']

    return ret_dict

def set_dict_detail_insert_data(args, rank_code):
    ret_dict = dict()
    change_object = []
    object = {}
    object_name = ""
    column_name = ""
    if args.has_key('change_object') and args.has_key('object_code'):
        change_object = TMSYS_ConfigChangeObjectPriority.get_list({"data":{"name":"TMChangeObjectRank"}})
        for x in change_object:
            if x['change_object'] == args['change_object']:
                object = x
                break
        __collection = getattr(models, object['table_name'])()
        if object['change_object'] == 1:
            column_name = "gjw_code"
            ret = __collection.aggregate().project(gjw_code = 1, gjw_name = 1)
            object_name = ret.match(column_name + " == {0}", args['object_code']).get_item()['gjw_name']
        elif object['change_object'] == 2:
            column_name = "job_w_code"
            ret = __collection.aggregate().project(job_w_code = 1, job_w_name = 1)
            object_name = ret.match(column_name + " == {0}", args['object_code']).get_item()['job_w_name']
        elif object['change_object'] == 3:
            column_name = "job_pos_code"
            ret = __collection.aggregate().project(job_pos_code = 1, job_pos_name = 1)
            object_name = ret.match(column_name + " == {0}", args['object_code']).get_item()['job_pos_name']
        elif object['change_object'] == 4:
            column_name = "emp_type_code"
            ret = __collection.aggregate().project(emp_type_code = 1, emp_type_name = 1)
            object_name = ret.match(column_name + " == {0}", args['object_code']).get_item()['emp_type_name']
    else:
        return None

    ret_dict.update(
            rec_id            = common.generate_guid(),
            rank_code         = rank_code,
            change_object     = (lambda x: x['change_object']  if x.has_key('change_object')    else None)(args),
            object_level      = None,
            object_code       = (lambda x: x['object_code']    if x.has_key('object_code')      else None)(args),
            object_name       = object_name,
            priority_no       = object['priority_no'],
            total_from        = (lambda x: x['total_from']     if x.has_key('total_from')       else None)(args),
            total_to          = (lambda x: x['total_to']       if x.has_key('total_to')         else None)(args),
            note              = (lambda x: x['note']           if x.has_key('note')             else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = "",
            modified_by       = ""
            )
    return ret_dict

def set_dict_detail_update_data(args, rank_code):
    ret_dict = set_dict_detail_insert_data(args, rank_code)
    del ret_dict['rec_id']
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict