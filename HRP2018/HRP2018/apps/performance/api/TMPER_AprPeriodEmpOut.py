# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
from Query import AprPeriodEmpOut
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
import quicky
from collections import OrderedDict

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=AprPeriodEmpOut.get_empNotApr_by_apr_period()

    ret=common.filter_lock(ret, args)
    
    #if(searchText != None):
    #    ret.match("contains(apr_period, @name) or " + \
    #        "contains(apr_year, @name) or contains(employee_code, @name) "+ \
    #        "contains(department_code, @name) or contains(job_w_code, @name)"
    #      ,name=searchText.strip())
    if(sort != None):
        ret.sort(sort)
    return ret.get_page(pageIndex, pageSize)

#def get_list_distinct_approval_year_and_period(args):
#    ret=models.TMPER_AprPeriodEmpOut().aggregate()
#    ret.project(
#        apr_period="apr_period",
#        apr_year="apr_year",
#        caption = "apr_year"
#    )
#    ret.sort(dict(
#       apr_period =1
#    ))
#    return ret.get_list()

def get_list_distinct_approval_year_and_period(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriod').aggregate([

        {"$lookup":{'from':common.get_collection_name_with_schema('SYS_VW_ValueList'), 'localField':'apr_period', 'foreignField':'value', 'as': 'aprPeriod'}},
        {"$unwind":{'path':'$aprPeriod', "preserveNullAndEmptyArrays":True}},
        {"$match":{
            "$and": [ { 'aprPeriod.list_name': "LApprovalPeriod" }, { 'aprPeriod.language': quicky.language.get_language()} ]
        }},

        {"$project": {
            "apr_period_a":{ "$ifNull": ["$aprPeriod.caption", ""] },
            "apr_year_a": {'$toString': "$apr_year"},
            "apr_period": {'$toString': "$apr_period"},
            "apr_year": 1
        }},
        {"$project": {
            "caption": { '$concat': [ "$apr_year_a", " / ", "$apr_period_a" ]},
            "value" : { '$concat': [ "$apr_year_a", "__", "$apr_period" ]},
            "apr_period":  -1,
            "apr_year":  -1
        }}])
     
    sort_dict = OrderedDict()
    sort_dict['_id.currency'] = 1
    sort_dict['total'] = -1
    ret = list(collection)
    return ret

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMPER_AprPeriodEmpOut().insert(data)
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
            if(args['data']['tmp']==1):
                del(args['data']['tmp'])
                data =  set_dict_update_data(args)
                ret  =  models.TMPER_AprPeriodEmpOut().update(
                    data, 
                    "_id == {0}", 
                    ObjectId(args['data']['_id']))
                lock.release()
                return ret
            else:
                del(args['data']['tmp'])
                data = {
                    "reason":args['data']['reason'],
                    "note":args['data']['note']
                    }
                ret  =  models.TMPER_AprPeriodEmpOut().update(
                    data, 
                    "_id in {0}", 
                    [ObjectId(x) for x in args['data']['_id']])
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
            ret  =  models.TMPER_AprPeriodEmpOut().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        apr_period         = (lambda x: x['apr_period']        if x.has_key('apr_period')       else None)(args['data']),
        apr_year         = (lambda x: x['apr_year']        if x.has_key('apr_year')       else None)(args['data']),
        employee_code        = (lambda x: x['employee_code']       if x.has_key('employee_code')      else None)(args['data']),
        department_code   = (lambda x: x['department_code']  if x.has_key('department_code') else None)(args['data']),
        job_w_code              = (lambda x: x['job_w_code']             if x.has_key('job_w_code')            else None)(args['data']),
        reason        = (lambda x: x['reason']       if x.has_key('reason')      else None)(args['data']),
        job_working         = (lambda x: x['job_working']        if x.has_key('job_working')       else None)(args['data']),
        note                = (lambda x: x['note']               if x.has_key('note')              else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    return ret_dict