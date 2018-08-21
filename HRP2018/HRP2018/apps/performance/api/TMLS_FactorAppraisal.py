# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
from Query import FactorAppraisal
from Query import JobWorking
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

    if not args['data'].has_key('factor_group_code') or args['data']['factor_group_code'] == None or args['data']['factor_group_code'] == "":
        return None

    ret=FactorAppraisal.display_list_factor_appraisal(args['data']['factor_group_code'])

    ret=common.filter_lock(ret, args)
    
    if(searchText != None):
        ret.match("contains(factor_code, @name) or contains(factor_name, @name)" + \
            " or contains(weight, @name) or contains(ordinal, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def delete_factor_appraisal(args):
    try:
        lock.acquire()
        ret = {}
        rs = {
            "deleted": 0,
            "error":None
            }
        err = None
        if args['data']['factor_code'] != None:
            collection  =  common.get_collection('HCSLS_JobWorking')
            try:
                for x in args['data']['job_w_code']:
                    ret = collection.update(
                    {
                        "job_w_code": str(x).format(),
                    }, 
                    { 
                        "$pull": 
                            { 
                                "factor_appraisal" : { 
                                    "factor_code": args['data']['factor_code'] 
                                    } 
                            } 
                    },
                    True)

                    if ret['updatedExisting'] and ret['nModified'] > 0:
                        rs['deleted'] += ret['nModified']
                
                lock.release()
                return rs
            except Exception as ex:
                err = ex

            lock.release()
            return dict(
                error = (lambda x: err.message if x != None else None)(err),
                data = ret
                )

        lock.release()
        return dict(
            error = "request parameter 'factor_code' is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def get_factor_appraisal_by_factor_code(args):
    try:
        ret = models.HCSLS_VW_JobWorkingFactorAppraisal().aggregate().project(
            job_w_code = 1,
            factor_code = 1
            ).match("factor_code == {0}", args['data']['factor_code'])
        ret.project(
            _id = 0,
            job_w_code = 1
            )
        return ret.get_list()
    except Exception as ex:
        raise(ex)

def insert_factor_appraisal(args):
    try:
        #lock.acquire()
        ret = {}
        rs = {
            "upserted": 0,
            "error":None
            }
        if args['data'] != None:
            if args['data'].has_key('factor_code'):
                if(args['data'].has_key('job_w_code')):
                    collection  =  common.get_collection('HCSLS_JobWorking')
                    collection.update_many({
                                                "factor_appraisal":{
                                                "$elemMatch":{
                                                    "factor_code":args['data']['factor_code']
                                                    }
                                                }
                                            },
                                            {
                                                "$set": {
                                                    'factor_appraisal': [],
                                                    }
                                            })
                    if args['data']['job_w_code'] != None and len(args['data']['job_w_code']) > 0:
                        for x in args['data']['job_w_code']:
                            try:
                                param = {
                                    "job_w_code"  : str(x).format(),
                                    "factor_code" : args['data']['factor_code'],
                                    "rec_id"      : common.generate_guid(),
                                    "weight"      : None,
                                    "created_on"  : datetime.datetime.now(),
                                    "created_by"  : common.get_user_id(),
                                    "modified_on" : None,
                                    "modified_by" : ''
                                    }
                                factor = param
                                
                                
                                ret = JobWorking.insert_evaluation_factor({"data":{"job_w_code":str(x).format()}}, factor)
                                if ret['updatedExisting'] and ret['nModified'] > 0:
                                    rs['upserted'] += ret['nModified']
                            except Exception as ex:
                                raise ex
                        #lock.release()
                        return rs
                else:
                    return dict(
                        error=dict(
                            fields=['job_w_code'],
                            code="missing"
                        )
                    )
            else:
                #lock.release()
                return dict(
                        error=dict(
                                fields=['factor_code'],
                                code="missing"
                            )
                    )

            #lock.release()
            return ret

        #lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        #lock.release()
        raise(ex)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMLS_FactorAppraisal().insert(data)
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
            ret  =  models.TMLS_FactorAppraisal().update(
                data, 
                "factor_code == {0}", 
                args['data']['factor_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                insert_factor_appraisal({
                    "data":{
                        "job_w_code":args['data']['job_working'],
                        "factor_code":args['data']['factor_code'],
                        }
                    })
                ret.update(
                    item = FactorAppraisal.display_list_factor_appraisal(args['data']['factor_group_code']).match("factor_code == {0}", args['data']['factor_code']).get_item()
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
            ret  =  models.TMLS_FactorAppraisal().delete("factor_code in {0}",[x["factor_code"]for x in args['data']])
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
        factor_code         = (lambda x: x['factor_code']        if x.has_key('factor_code')       else None)(args['data']),
        factor_name         = (lambda x: x['factor_name']        if x.has_key('factor_name')       else None)(args['data']),
        factor_name2        = (lambda x: x['factor_name2']       if x.has_key('factor_name2')      else None)(args['data']),
        factor_group_code   = (lambda x: x['factor_group_code']  if x.has_key('factor_group_code') else None)(args['data']),
        weight              = (lambda x: x['weight']             if x.has_key('weight')            else None)(args['data']),
        is_apply_all        = (lambda x: x['is_apply_all']       if x.has_key('is_apply_all')      else None)(args['data']),
        #job_working         = (lambda x: x['job_working']        if x.has_key('job_working')       else None)(args['data']),
        note                = (lambda x: x['note']               if x.has_key('note')              else None)(args['data']),
        ordinal             = (lambda x: x['ordinal']            if x.has_key('ordinal')           else None)(args['data']),
        lock                = (lambda x: x['lock']               if x.has_key('lock')              else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['factor_code']
    return ret_dict