# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
from Query import JobWorkingGroup
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_tree(args):
    ret=JobWorkingGroup.get_job_working_group()
        
    return ret.get_list()

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_job_working = models.HCSLS_JobWorkingGroup().aggregate().project(
                    level_code = 1, 
                    gjw_code = 1,
                    level = 1).match("gjw_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_job_working['level'] + 1
                parent_job_working['level_code'].append(data['gjw_code'])
                data['level_code'] = parent_job_working['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [data['gjw_code']]
            ret  =  models.HCSLS_JobWorkingGroup().insert(data)
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
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_job_working = models.HCSLS_JobWorkingGroup().aggregate().project(
                    level_code = 1, 
                    gjw_code = 1,
                    level = 1).match("gjw_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_job_working['level'] + 1
                parent_job_working['level_code'].append(args['data']['gjw_code'])
                data['level_code'] = parent_job_working['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [args['data']['gjw_code']]

            ret  =  models.HCSLS_JobWorkingGroup().update(
                data, 
                "gjw_code == {0}", 
                args['data']['gjw_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = JobWorkingGroup.get_job_working_group().match("gjw_code == {0}", args['data']['gjw_code']).get_item()
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

            #code được chọn
            list_group_code = [x["gjw_code"]for x in args['data']]
            #từ code hiện tại đến các cấp cha
            list_fiter = []
            if len(list_group_code) > 0:
                for x in list_group_code:
                    collection = common.get_collection('HCSLS_JobWorkingGroup').aggregate([
                        { 
                            "$match": { 
                                "$or":[
                                    { "gjw_code": str(x).format() },
                                    { "gjw_code": { "$in": common.get_collection('HCSLS_JobWorkingGroup').find_one({ "gjw_code": str(x).format() })["level_code"] }}
                                    ]}
                        },
                        {
                            "$project":{
                                "_id": 0,
                                "gjw_code": 1
                          }}
                        ])
                    list_fiter += list(collection)
            else:
                lock.release()
                return dict(
                    error = "gjw_code is not exsit"
                )

            #kiểm tra từ code hiện tại đến các cấp cha có group code nào đang được sử dụng không
            #Nếu có 'len(list_job_workig) > 0' return
            #Không có xử lí delete
            list_job_workig = models.HCSLS_JobWorking().aggregate().project(job_w_code = 1, gjw_code = 1).match("gjw_code in {0}", [x["gjw_code"]for x in list_fiter]).get_list()
            if len(list_job_workig) > 0:
                lock.release()
                return dict(
                    error = "JobWorkingGroup is using another PG",
                    items = list_job_workig
                )
            else:
                ret  =  models.HCSLS_JobWorkingGroup().delete("gjw_code in {0}", list_group_code)
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
        gjw_code         = (lambda x: x['gjw_code']          if x.has_key('gjw_code')          else None)(args['data']),
        gjw_name         = (lambda x: x['gjw_name']          if x.has_key('gjw_name')          else None)(args['data']),
        gjw_name2        = (lambda x: x['gjw_name2']         if x.has_key('gjw_name2')         else None)(args['data']),
        parent_code      = (lambda x: x['parent_code']       if x.has_key('parent_code')       else None)(args['data']),
        level            = (lambda x: x['level']             if x.has_key('level')             else 1)(args['data']),
        level_code       = (lambda x: x['level_code']        if x.has_key('level_code')        else None)(args['data']),
        ordinal          = (lambda x: x['ordinal']           if x.has_key('ordinal')           else None)(args['data']),
        note             = (lambda x: x['note']              if x.has_key('note')              else None)(args['data']),
        lock             = (lambda x: x['lock']              if x.has_key('lock')              else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['gjw_code']
    return ret_dict
