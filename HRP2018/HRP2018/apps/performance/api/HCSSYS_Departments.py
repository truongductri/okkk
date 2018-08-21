# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
from Query import DepartmentGroup

def get_list(args):
    items = models.HCSSYS_Departments().aggregate().project(
        department_code = 1,
        department_name = 1,
        parent_code     = 1
        )
    
    return items.get_list()

def get_department_by_dept_code(args):
    try:
        if args['data'] != None and args['data'].has_key('department_code'):
            items = models.HCSSYS_Departments().aggregate().project(
                department_code     = 1,
                department_name     = 1,
                department_name2    = 1,
                department_alias    = 1,
                parent_code         = 1,
                level               = 1,
                level_code          = 1,
                department_tel      = 1,
                department_fax      = 1,
                department_email    = 1,
                department_address  = 1,
                nation_code         = 1,
                province_code       = 1,
                district_code       = 1,
                is_company          = 1,
                is_fund             = 1,
                is_fund_bonus       = 1,
                decision_no         = 1,
                decision_date       = 1,
                effect_date         = 1,
                license_no          = 1,
                tax_code            = 1,
                lock_date           = 1,
                logo_image          = 1,
                manager_code        = 1,
                secretary_code      = 1,
                ordinal             = 1,
                lock                = 1,
                note                = 1,
                region_code         = 1,
                domain_code         = 1,
                signed_by           = 1
                ).match("department_code == {0}", args['data']['department_code'])
    
            return items.get_item()
        raise(Exception("not found department_code"))
    except Exception as ex:
        raise(ex)

def get_list_department_by_parent_code(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret= models.HCSSYS_Departments().aggregate().project(
        department_code = 1,
        department_name = 1,
        department_alias = 1,
        department_tel = 1,
        level_code = 1
        )
    ret.match("level_code == {0}", args['data']['where']['department_code'])

    if(searchText != None):
        ret.match("contains(department_code, @name) or contains(department_name, @name)" + \
        "or contains(department_alias, @name) or contains(department_tel, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def get_tree(args):
    ret=DepartmentGroup.get_department_group()
    return ret.get_list()



def get_department_group():
    ret=models.HCSSYS_Departments().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        department_code = "department_code",
        factor_group_name = "factor_group_name",
        factor_group_name2 = "factor_group_name2",
        parent_code = "parent_code",
        level = "level",
        level_code = "level_code",
        ordinal = "ordinal",
        note = "note",
        lock = "lock",
        created_by="uc.login_account",
        created_on= "created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
    )) 
    return ret
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data'].has_key('department_code') or not args['data'].has_key('department_name'):
                field_list = []
                if not args['data'].has_key('department_code'):
                    field_list.append("department_code")
                if not args['data'].has_key('department_name'):
                    field_list.append("department_name")
                lock.release()
                return {
                    "error":{
                        "fields":field_list,
                        "code":"missing"
                        }
                }
                
            data =  set_dict_data(args)
            parent_dept = models.HCSSYS_Departments().aggregate().project(
                department_code = 1,
                level = 1,
                level_code = 1
                ).match("department_code == {0}", args['data']['parent_code']).get_item()

            data['level'] = parent_dept['level'] + 1
            data['level_code'] = parent_dept['level_code'] + [args['data']['department_code']]
            ret  =  models.HCSSYS_Departments().insert(data)
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
            data = set_dict_data(args)
            ret  =  models.HCSSYS_Departments().update(data, "department_code == @department_code", department_code = args['data']['department_code'])
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
            ret =  models.HCSSYS_Departments().delete("department_code in {0}", [x["department_code"]for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_data(args):
    data = dict(
        department_code     =     args['data']['department_code'],
        department_name     =     args['data']['department_name'],
        department_name2    =     (lambda x: x['department_name2'] if x.has_key('department_name2') else None)(args['data']),
        department_alias    =     (lambda x: x['department_alias'] if x.has_key('department_alias') else None)(args['data']),
        parent_code         =     (lambda x: x['parent_code'] if x.has_key('parent_code') else None)(args['data']),
        level               =     (lambda x: x['level'] if x.has_key('level') else None)(args['data']),
        level_code          =     (lambda x: x['level_code'] if x.has_key('level_code') else None)(args['data']),
        department_tel      =     (lambda x: x['department_tel'] if x.has_key('department_tel') else None)(args['data']),
        department_fax      =     (lambda x: x['department_fax'] if x.has_key('department_fax') else None)(args['data']),
        department_email    =     (lambda x: x['department_email'] if x.has_key('department_email') else None)(args['data']),
        department_address  =     (lambda x: x['department_address'] if x.has_key('department_address') else None)(args['data']),
        nation_code         =     (lambda x: x['nation_code'] if x.has_key('nation_code') else None)(args['data']),
        province_code       =     (lambda x: x['province_code'] if x.has_key('province_code') else None)(args['data']),
        district_code       =     (lambda x: x['district_code'] if x.has_key('district_code') else None)(args['data']),
        is_company          =     (lambda x: x['is_company'] if x.has_key('is_company') else None)(args['data']),
        is_fund             =     (lambda x: x['is_fund'] if x.has_key('is_fund') else None)(args['data']),
        is_fund_bonus       =     (lambda x: x['is_fund_bonus'] if x.has_key('is_fund_bonus') else None)(args['data']),
        decision_no         =     (lambda x: x['decision_no'] if x.has_key('decision_no') else None)(args['data']),
        decision_date       =     (lambda x: x['decision_date'] if x.has_key('decision_date') else None)(args['data']),
        effect_date         =     (lambda x: x['effect_date'] if x.has_key('effect_date') else None)(args['data']),
        license_no          =     (lambda x: x['license_no'] if x.has_key('license_no') else None)(args['data']),
        tax_code            =     (lambda x: x['tax_code'] if x.has_key('tax_code') else None)(args['data']),
        lock_date           =     (lambda x: x['lock_date'] if x.has_key('lock_date') else None)(args['data']),
        logo_image          =     (lambda x: x['logo_image'] if x.has_key('logo_image') else None)(args['data']),
        manager_code        =     (lambda x: x['manager_code'] if x.has_key('manager_code') else None)(args['data']),
        secretary_code      =     (lambda x: x['secretary_code'] if x.has_key('secretary_code') else None)(args['data']),
        ordinal             =     (lambda x: x['ordinal'] if x.has_key('ordinal') else None)(args['data']),
        lock                =     (lambda x: x['lock'] if x.has_key('lock') else None)(args['data']),
        note                =     (lambda x: x['note'] if x.has_key('note') else None)(args['data']),
        region_code         =     (lambda x: x['region_code'] if x.has_key('region_code') else None)(args['data']),
        domain_code         =     (lambda x: x['domain_code'] if x.has_key('domain_code') else None)(args['data']),
        signed_by           =     (lambda x: x['signed_by'] if x.has_key('signed_by') else None)(args['data'])
    )
    return data