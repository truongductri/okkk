# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

#def get_list_data():
#    items = models.LMSLS_ExTemplateList().aggregate()
#    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
#    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
#    items.project(
#        folder_id=1,
#        folder_name=1,
#        folder_name2=1,
#        parent_id=1,
#        parent_code=1,
#        level=1,
#        level_code=1,
#        ordinal=1,
#        lock=1,
#        note=1,
#        moderator_id=1,
#        approver_id=1,
#        active=1,
#        permisions=1,
#        approve_type=1,
#        created_by="uc.login_account",
#        created_on="created_on",
#        modified_on="switch(case(modified_on!='',modified_on),'')",
#        modified_by="switch(case(modified_by!='',um.login_account),'')",
#        )
    
#    return items
#def get_list_with_searchtext(args):
#    searchText = args['data'].get('search', '')
#    pageSize = args['data'].get('pageSize', 0)
#    pageIndex = args['data'].get('pageIndex', 20)
#    sort = args['data'].get('sort', 20)
#    where = args['data'].get('where')

#    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
#    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
#    ret=models.LMSLS_ExTemplateList().aggregate()
#    ret.left_join(models.models.auth_user_info(), "created_by", "username", "uc")
#    ret.left_join(models.models.auth_user_info(), "modified_by", "username", "um")
#    ret.project(
#            folder_id=1,
#            folder_name=1,
#            folder_name2=1,
#            parent_id=1,
#            parent_code=1,
#            level=1,
#            level_code=1,
#            ordinal=1,
#            lock=1,
#            note=1,
#            moderator_id=1,
#            approver_id=1,
#            active=1,
#            permisions=1,
#            approve_type=1,
#            created_by="uc.login_account",
#            created_on="created_on",
#            modified_on="switch(case(modified_on!='',modified_on),'')",
#            modified_by="switch(case(modified_by!='',um.login_account),'')",
#        )
    
#    if(where != None):
#        ret.match("(level_code==@folder_id)",folder_id=where['folder_id'])

#    if(searchText != None):
#        ret.match("contains(folder_name, @name) or contains(moderator_id, @name)",name=searchText)

#    if(sort != None):
#        ret.sort(sort)
        
#    data = ret.get_page(pageIndex, pageSize)
#    return  data

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.LMSLS_ExQuestionBank().insert(data)
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
            ret  =  models.LMSLS_ExTemplateList().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = get_list_data().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret  =  models.LMSLS_ExTemplateList().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        ques_id= (lambda x: x['ques_id'] if x.has_key('ques_id') else None)(args['data']),
        ques_category= (lambda x: x['ques_category'] if x.has_key('ques_category') else None)(args['data']),
        ques_type= (lambda x: x['ques_type'] if x.has_key('ques_type') else None)(args['data']),
        ques_level= (lambda x: x['ques_level'] if x.has_key('ques_level') else None)(args['data']),
        ques_file= (lambda x: x['ques_file'] if x.has_key('ques_file') else None)(args['data']),
        ques_detail_1= (lambda x: x['ques_detail_1'] if x.has_key('ques_detail_1') else None)(args['data']),
        ques_detail_2= (lambda x: x['ques_detail_2'] if x.has_key('ques_detail_2') else None)(args['data']),
        ques_hint= (lambda x: x['ques_hint'] if x.has_key('ques_hint') else None)(args['data']),
        ques_answers= (lambda x: x['ques_answers'] if x.has_key('ques_answers') else None)(args['data']),
        ques_total_marks= (lambda x: x['ques_total_marks'] if x.has_key('ques_total_marks') else None)(args['data']),
        ques_attach_file= (lambda x: x['ques_attach_file'] if x.has_key('ques_attach_file') else None)(args['data']),
        ques_max_answer_time= (lambda x: x['ques_max_answer_time'] if x.has_key('ques_max_answer_time') else 0)(args['data']),
        ques_explanation= (lambda x: x['ques_explanation'] if x.has_key('ques_explanation') else None)(args['data']),
        ques_answer_options= (lambda x: x['ques_answer_options'] if x.has_key('ques_answer_options') else None)(args['data']),
        ques_randomization= (lambda x: x['ques_randomization'] if x.has_key('ques_randomization') else None)(args['data']),
        ques_tags= (lambda x: x['ques_tags'] if x.has_key('ques_tags') else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['category_id']
    return ret_dict
#def get_level_code_by_folder_id(args):
#    where = args['data'].get('where')
#    ret=models.LMSLS_ExTemplateList().aggregate()
#    if(where != None):
#        ret.match("(folder_id==@folder_id)",folder_id=where['folder_id'])
#    ret.project(
#        level_code=1
#        )
#    return ret.get_page(0, 100)