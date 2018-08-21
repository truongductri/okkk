# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import threading
import common
from Query import EmpWorking
from Query import Employee
import views
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

#def get_list_with_searchtext(args):
#    try:
#        ret = {}
#        if args['data'] != None:
#            searchText = args['data'].get('search', '')
#            pageSize = args['data'].get('pageSize', 0)
#            pageIndex = args['data'].get('pageIndex', 20)
#            sort = args['data'].get('sort', 20)

#            pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
#            pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

#            if args['data'].has_key('employee_code'):
#                ret = EmpWorking.get_empworking_by_employee_code(args['data']['employee_code'])
#            else:
#                return dict(
#                    error = "parameter 'employee_code' is not exist"
#                )
#            return ret

#        return dict(
#            error = "request parameter is not exist"
#        )
#    except Exception as ex:
#        raise(ex)

def get_empworking_by_emp_code(args):
    try:
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('employee_code') and args['data']['employee_code'] != None and args['data']['employee_code'] != "":
                searchText = args['data'].get('search', '')
                pageSize = args['data'].get('pageSize', 0)
                pageIndex = args['data'].get('pageIndex', 20)
                sort = args['data'].get('sort', 20)

                pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
                pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

                ret = EmpWorking.get_empworking_by_employee_code(args['data']['employee_code'], pageIndex, pageSize, sort, searchText)
                if len(ret) > 0:
                    return ret[0]
                else:
                    ret = {
                    'page_size': pageSize,
                    'page_index': pageIndex,
                    'total_items': 0,
                    'items': []
                    }
                #if(sort != None):
                #    ret.sort(sort)

            else:
                return dict(
                    error = "parameter 'employee_code' is not exist"
                )
            return ret#.get_page(pageIndex, pageSize)

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def get_default_value_curent_employee(args):
    try:
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('employee_code') and args['data']['employee_code'] != None and args['data']['employee_code'] != "":               

                ret = EmpWorking.get_default_value_curent_employee(args['data']['employee_code'])
                if len(ret) > 0:
                    return ret[0]
                else:
                    ret = {}

            else:
                return dict(
                    error = "parameter 'employee_code' is not exist"
                )
            return ret

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
            ret  =  models.HCSEM_EmpWorking().insert(data)
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
            ret  =  models.HCSEM_EmpWorking().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            #if ret['data'].raw_result['updatedExisting'] == True:
            #    ret.update(
            #        item = AdministrativeSubdivisions.get_district().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
            #        )
            lock.release()
            #if ret['data'].raw_result['updatedExisting'] == True:
            #    ret.update(entity=Employee.get_employee_by_employee_code(args['data']['_id']))
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
            ret  =  models.HCSEM_EmpWorking().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        #rec_id                    = common.generate_guid(),
        employee_code             = (lambda x: x['employee_code']           if x.has_key('employee_code')               else None)(args),
        appoint                   = (lambda x: x['appoint']                 if x.has_key('appoint')                   else None)(args),
        effect_date               = (lambda x: x['effect_date']             if x.has_key('effect_date')                  else None)(args),
        begin_date                = (lambda x: x['begin_date']              if x.has_key('begin_date')                  else None)(args),
        end_date                  = (lambda x: x['end_date']                if x.has_key('end_date')                      else None)(args),
        decision_no               = (lambda x: x['decision_no']             if x.has_key('decision_no')                    else None)(args),
        signed_date               = (lambda x: x['signed_date']             if x.has_key('signed_date')             else None)(args),
        signer_code               = (lambda x: x['signer_code']             if x.has_key('signer_code')                 else None)(args),
        note                      = (lambda x: x['note']                    if x.has_key('note')                 else None)(args),
        task                      = (lambda x: x['task']                    if x.has_key('task')               else None)(args),
        reason                    = (lambda x: x['reason']                  if x.has_key('reason')                  else None)(args),
        department_code           = (lambda x: x['department_code']         if x.has_key('department_code')                  else None)(args),
        job_pos_code              = (lambda x: x['job_pos_code']            if x.has_key('job_pos_code')            else None)(args),
        job_w_code                = (lambda x: x['job_w_code']              if x.has_key('job_w_code')                else None)(args),
        emp_type_code             = (lambda x: x['emp_type_code']           if x.has_key('emp_type_code')                  else None)(args),
        region_code               = (lambda x: x['region_code']             if x.has_key('region_code')                 else None)(args),
        department_code_old       = (lambda x: x['department_code_old']     if x.has_key('department_code_old')           else None)(args),
        job_pos_code_old          = (lambda x: x['job_pos_code_old']        if x.has_key('job_pos_code_old')                      else None)(args),
        job_w_code_old            = (lambda x: x['job_w_code_old']          if x.has_key('job_w_code_old')                     else None)(args),
        emp_type_code_old         = (lambda x: x['emp_type_code_old']       if x.has_key('emp_type_code_old')                       else None)(args),
        region_code_old           = (lambda x: x['region_code_old']         if x.has_key('region_code_old')              else None)(args),
        province_code             = (lambda x: x['province_code']           if x.has_key('province_code')                 else None)(args)       
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    #del ret_dict['_id']
    return ret_dict
############Update Employee###############
def update_employee(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_employee(args['data'])
            ret  =  models.HCSEM_Employees().update(
                data, 
                "employee_code == {0}", 
                args['data']['employee_code'])
            lock.release()
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(entity=Employee.get_employee_by_employee_code(args['data']['employee_code']))
            return ret
        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_update_employee(args):
    ret_dict = dict()

    ret_dict.update(
        employee_code             = (lambda x: x['employee_code']             if x.has_key('employee_code')               else None)(args),
        department_code           = (lambda x: x['department_code']           if x.has_key('department_code')             else None)(args),
        job_pos_code              = (lambda x: x['job_pos_code']              if x.has_key('job_pos_code')                else None)(args),
        job_w_code                = (lambda x: x['job_w_code']                if x.has_key('job_w_code')                  else None)(args),
        #region_code              = (lambda x: x['region_code']           if x.has_key('region_code')             else None)(args),
    )
    return ret_dict
