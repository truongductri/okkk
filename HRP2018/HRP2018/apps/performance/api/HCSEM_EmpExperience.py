# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import threading
import common
from Query import EmpExperience
import views
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    try:
        ret = {}
        if args['data'] != None:
            searchText = args['data'].get('search', '')
            pageSize = args['data'].get('pageSize', 0)
            pageIndex = args['data'].get('pageIndex', 20)
            sort = args['data'].get('sort', 20)

            pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

            if args['data'].has_key('employee_code'):
                ret = EmpExperience.get_emp_experience_by_emp_code(args['data']['employee_code'])
            else:
                return dict(
                    error = "parameter 'employee_code' is not exist"
                )
            
            if(searchText != None):
                ret.match("contains(begin_date, @name) or " + \
                    "contains(end_date, @name) or " + \
                    "contains(working_location, @name) or " + \
                    "contains(job_w_name, @name) or " + \
                    "contains(job_pos_name, @name)",name=searchText.strip())

            return ret.get_page(pageIndex, pageSize)

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args['data'])
            ret  =  models.HCSEM_EmpExperience().insert(data)
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
            data =  set_dict_update_data(args['data'])
            ret  =  models.HCSEM_EmpExperience().update(
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

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.HCSEM_EmpExperience().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        employee_code      = (lambda x: x['employee_code']    if x.has_key('employee_code')    else None)(args),
        begin_date         = (lambda x: x['begin_date']       if x.has_key('begin_date')       else None)(args),
        end_date           = (lambda x: x['end_date']         if x.has_key('end_date')         else None)(args),
        salary             = (lambda x: x['salary']           if x.has_key('salary')           else None)(args),
        currency_code      = (lambda x: x['currency_code']    if x.has_key('currency_code')    else None)(args),
        emp_type_code      = (lambda x: x['emp_type_code']    if x.has_key('emp_type_code')    else None)(args),
        job_pos_code       = (lambda x: x['job_pos_code']     if x.has_key('job_pos_code')     else None)(args),
        job_w_code         = (lambda x: x['job_w_code']       if x.has_key('job_w_code')       else None)(args),
        working_on         = (lambda x: x['working_on']       if x.has_key('working_on')       else None)(args),
        working_location   = (lambda x: x['working_location'] if x.has_key('working_location') else None)(args),
        address            = (lambda x: x['address']          if x.has_key('address')          else None)(args),
        profession_code    = (lambda x: x['profession_code']  if x.has_key('profession_code')  else None)(args),
        quit_job_code      = (lambda x: x['quit_job_code']    if x.has_key('quit_job_code')    else None)(args),
        reason             = (lambda x: x['reason']           if x.has_key('reason')           else None)(args),
        ref_info           = (lambda x: x['ref_info']         if x.has_key('ref_info')         else None)(args),
        note               = (lambda x: x['note']             if x.has_key('note')             else None)(args),
        is_na_company      = (lambda x: x['is_na_company']    if x.has_key('is_na_company')    else None)(args),
        is_in_section      = (lambda x: x['is_in_section']    if x.has_key('is_in_section')    else None)(args)
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    return ret_dict