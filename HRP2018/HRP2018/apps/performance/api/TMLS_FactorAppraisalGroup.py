# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import FactorAppraisalGroup
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_tree(args):
    ret=FactorAppraisalGroup.get_factor_appraisal_group()
    return ret.get_list()


def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_factor_group = models.TMLS_FactorAppraisalGroup().aggregate().project(
                    level_code = 1, 
                    factor_group_code = 1,
                    level = 1).match("factor_group_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_factor_group['level'] + 1
                parent_factor_group['level_code'].append(data['factor_group_code'])
                data['level_code'] = parent_factor_group['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [data['factor_group_code']]
            ret  =  models.TMLS_FactorAppraisalGroup().insert(data)
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
                parent_factor_group = models.TMLS_FactorAppraisalGroup().aggregate().project(
                    level_code = 1, 
                    factor_group_code = 1,
                    level = 1).match("factor_group_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_factor_group['level'] + 1
                parent_factor_group['level_code'].append(args['data']['factor_group_code'])
                data['level_code'] = parent_factor_group['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [args['data']['factor_group_code']]

            ret  =  models.TMLS_FactorAppraisalGroup().update(
                data, 
                "factor_group_code == {0}", 
                args['data']['factor_group_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = FactorAppraisalGroup.get_factor_appraisal_group().match("factor_group_code == {0}", args['data']['factor_group_code']).get_item()
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
            list_group_code = [x["factor_group_code"]for x in args['data']]
            if FactorAppraisalGroup.check_exits_factCode_within_factGroup(list_group_code) == False:
                 ret  =  models.TMLS_FactorAppraisalGroup().delete("factor_group_code in {0}",[x["factor_group_code"]for x in args['data']])
                 lock.release()
                 return ret
            else:
                lock.release()
                return dict(
                    error = "not allow"
                    )
        lock.release()
        return  dict(
            error = "request parameter is not exist"
            )
    except Exception as ex:
        lock.release()
        raise(ex)



def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        factor_group_code         = (lambda x: x['factor_group_code']          if x.has_key('factor_group_code')          else None)(args['data']),
        factor_group_name         = (lambda x: x['factor_group_name']          if x.has_key('factor_group_name')          else None)(args['data']),
        factor_group_name2        = (lambda x: x['factor_group_name2']         if x.has_key('factor_group_name2')         else None)(args['data']),
        parent_code      = (lambda x: x['parent_code']       if x.has_key('parent_code')       else None)(args['data']),
        level            = (lambda x: x['level']             if x.has_key('level')             else 1)(args['data']),
        level_code       = (lambda x: x['level_code']        if x.has_key('level_code')        else None)(args['data']),
        ordinal          = (lambda x: x['ordinal']           if x.has_key('ordinal')           else None)(args['data']),
        note             = (lambda x: x['note']              if x.has_key('note')              else None)(args['data']),
        lock             = (lambda x: x['lock']              if x.has_key('lock')              else None)(args['data'])
        
    )

    return ret_dict


def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['factor_group_code']
    return ret_dict
