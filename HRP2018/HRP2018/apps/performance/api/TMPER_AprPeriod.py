# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
from Query import AprPeriod
import logging
import threading
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

    ret=AprPeriod.display_list_apr_period()
    ret=common.filter_lock(ret, args)
    if(searchText != None):
        ret.match("contains(apr_period, @name) or contains(apr_year, @name)" ,name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
      
    return ret.get_page(pageIndex, pageSize)


def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMPER_AprPeriod().insert(data)
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
            ret  =  models.TMPER_AprPeriod().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

    


def get_apr_period_by_id(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('apr_period'):
                ret = AprPeriod.get_period_by_apr_period(args['data']['apr_period'])
            else:
                return dict(
                    error = "parameter 'apr_period' is not exist"
                )
            return ret.get_item()

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.TMPER_AprPeriod().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        apr_period      =                   (lambda x: x['apr_period']      if x.has_key('apr_period')       else None)(args['data']),
        apr_year      =                     (lambda x: x['apr_year']      if x.has_key('apr_year')       else None)(args['data']),
        give_target_from     =              (lambda x: x['give_target_from']     if x.has_key('give_target_from')      else None)(args['data']),
        give_target_to            =         (lambda x: x['give_target_to']            if x.has_key('give_target_to')             else None)(args['data']),
        review_mid_from               =     (lambda x: x['review_mid_from']               if x.has_key('review_mid_from')                else None)(args['data']),
        review_mid_to               =       (lambda x: x['review_mid_to']               if x.has_key('review_mid_to')                else None)(args['data']),
        approval_mid_from     =                (lambda x: x['approval_mid_from']     if x.has_key('approval_mid_from')      else None)(args['data']),
        approval_mid_to            =           (lambda x: x['approval_mid_to']            if x.has_key('approval_mid_to')             else None)(args['data']),
        emp_final_from               = (lambda x: x['emp_final_from']               if x.has_key('emp_final_from')                else None)(args['data']),
        emp_final_to               =   (lambda x: x['emp_final_to']               if x.has_key('emp_final_to')                else None)(args['data']),
        approval_final_from               = (lambda x: x['approval_final_from']               if x.has_key('approval_final_from')                else None)(args['data']),
        approval_final_to               =   (lambda x: x['approval_final_to']               if x.has_key('approval_final_to')                else None)(args['data']),
        note                      =   (lambda x: x['note']               if x.has_key('note')                else None)(args['data'])
        )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    #del ret_dict['_id']
    return ret_dict