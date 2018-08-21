# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import KPIGroup
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_tree(args):
    ret=KPIGroup.get_kpi_group(args["data"]["lock"]);
    
    return ret.get_list()

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = set_dict_insert_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_kpi_group_code = models.TMLS_KPIGroup().aggregate().project(level_code = 1, 
                    kpi_group_code = 1,
                    level = 1).match("kpi_group_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_kpi_group_code['level'] + 1
                parent_kpi_group_code['level_code'].append(data['kpi_group_code'])
                data['level_code'] = parent_kpi_group_code['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [data['kpi_group_code']]
            ret = models.TMLS_KPIGroup().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(error = "request parameter is not exist")
    except Exception as ex:
        lock.release()
        raise(ex)





def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = set_dict_update_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_kpi_group_code = models.TMLS_KPIGroup().aggregate().project(level_code = 1, 
                    kpi_group_code = 1,
                    level = 1).match("kpi_group_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_kpi_group_code['level'] + 1
                parent_kpi_group_code['level_code'].append(args['data']['kpi_group_code'])
                data['level_code'] = parent_kpi_group_code['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [args['data']['kpi_group_code']]

            ret = models.TMLS_KPIGroup().update(data, 
                "kpi_group_code == {0}", 
                args['data']['kpi_group_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(item = KPIGroup.get_kpi_group(args["data"]["lock"]).match("kpi_group_code == {0}", args['data']['kpi_group_code']).get_item())
            lock.release()
            return ret

        lock.release()
        return dict(error = "request parameter is not exist")
    except Exception as ex:
        lock.release()
        raise(ex)




#def delete(args):
#    try:
#        lock.acquire()
#        ret = {}
#        if args['data'] != None:
#            list_group_code = [x["kpi_group_code"]for x in args['data']]
#            if KPIGroup.check_exits_kpicode_within_kpiGroup(list_group_code) == False:
#                 ret = models.TMLS_KPIGroup().delete("kpi_group_code in {0}",[x["kpi_group_code"]for x in args['data']])
#                 lock.release()
#                 return ret
#            else:
#                lock.release()
#                return dict(error = "not allow")
#        lock.release()
#        return  dict(error = "request parameter is not exist")
#    except Exception as ex:
#        lock.release()
#        raise(ex)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            #code được chọn
            list_group_code = [x["kpi_group_code"]for x in args['data']]
            #từ code hiện tại đến các cấp cha
            list_fiter = []
            if len(list_group_code) > 0:
                for x in list_group_code:
                    collection = common.get_collection('TMLS_KPIGroup').aggregate([
                        { 
                            "$match": { 
                                "$or":[
                                    { "kpi_group_code": str(x).format() },
                                    { "kpi_group_code": { "$in": common.get_collection('TMLS_KPIGroup').find_one({ "kpi_group_code": str(x).format() })["level_code"] }}
                                    ]}
                        },
                        {
                            "$project":{
                                "_id": 0,
                                "kpi_group_code": 1
                          }}
                        ])
                    list_fiter += list(collection)
            else:
                lock.release()
                return dict(
                    error = "kpi_group_code is not exsit"
                )

            #kiểm tra từ code hiện tại đến các cấp cha có group code nào đang được sử dụng không
            #Nếu có 'len(list_kpi_workig) > 0' return
            #Không có xử lí delete
            list_kpi_workig = models.HCSLS_JobWorking().aggregate().project(job_w_code = 1, kpi_group_code = 1).match("kpi_group_code in {0}", [x["kpi_group_code"]for x in list_fiter]).get_list()
            if len(list_kpi_workig) > 0:
                lock.release()
                return dict(
                    error = "KPIGroup is using another PG",
                    items = list_kpi_workig
                )
            else:
                ret  =  models.TMLS_KPIGroup().delete("kpi_group_code in {0}", list_group_code)
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
        kpi_group_code         = (lambda x: x['kpi_group_code']          if x.has_key('kpi_group_code')          else None)(args['data']),
        kpi_group_name         = (lambda x: x['kpi_group_name']          if x.has_key('kpi_group_name')          else None)(args['data']),
        kpi_group_name2        = (lambda x: x['kpi_group_name2']         if x.has_key('kpi_group_name2')         else None)(args['data']),
        parent_code      = (lambda x: x['parent_code']       if x.has_key('parent_code')       else None)(args['data']),
        level            = (lambda x: x['level']             if x.has_key('level')             else 1)(args['data']),
        level_code       = (lambda x: x['level_code']        if x.has_key('level_code')        else None)(args['data']),
        weight           = (lambda x: x['weight']             if x.has_key('weight')            else None)(args['data']),
        is_team          = (lambda x: x['is_team']             if x.has_key('is_team')            else None)(args['data']),
        ordinal          = (lambda x: x['ordinal']           if x.has_key('ordinal')           else None)(args['data']),
        note             = (lambda x: x['note']              if x.has_key('note')              else None)(args['data']),
        lock             = (lambda x: x['lock']              if x.has_key('lock')              else None)(args['data']))

    return ret_dict


def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['kpi_group_code']
    return ret_dict
