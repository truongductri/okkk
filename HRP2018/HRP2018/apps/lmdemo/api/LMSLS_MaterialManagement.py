# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import datetime
import common
import json
from bson import json_util
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_data():
    items = models.LMSLS_MaterialManagement().aggregate()
    items.left_join(models.models.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.models.auth_user_info(), "modified_by", "username", "um")
    items.project(
            material_id=1,
            material_name=1,
            material_name2=1,
            material_version=1,
            submit_user_id=1,
            submit_date=1,
            approve_user_id=1,
            approve_date=1,
            ordinal=1,
            note=1,
            lock=1,
            folder_id=1,
            author_name=1,
            course_name=1,
            size=1,
            creator=1,
            category=1,
            level_code=1,
            description=1,
            publisher_name=1,
            publisher_date=1,
            date_valid_from=1,
            date_valid_to=1,
            course_id=1,
            language=1,
            version=1,
            coverage=1,
            rights=1,
            relations=1,
            files=1,
            comments=1,
            views=1,
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    
    return items

def get_list(args):
    items = models.LMSLS_MaterialManagement().aggregate().project(
        folder_id = 1,
        folder_name = 1,
        parent_code = 1
        )

def get_list_user_with_searchtext(args):
    if args['data'] != None:
        try:
            searchText      = args['data'].get('search', '')
            pageSize        = args['data'].get('pageSize', 0)
            pageIndex       = args['data'].get('pageIndex', 20)
            sort            = args['data'].get('sort', 20)
            where           = (lambda data: data["where"] if data.has_key("where") else {})(args['data'])
            pageIndex       = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize        = (lambda pSize: pSize if pSize != None else 20)(pageSize)

            items = models.extend.auth_user_info().aggregate().project(
                    login_account       = 1,
                    username            = 1,
                    display_name        = 1,
                    role_code           = 1,
                    is_system           = 1,
                    never_expire        = 1,
                    manlevel_from       = 1,
                    manlevel_to         = 1,
                    email               = 1,
                    mobile              = 1,
                    description         = 1,
                    created_on          = 1
                    )

            if(searchText != None):
                items.match("contains(login_account, @name) or contains(display_name, @name) " + \
                    "or contains(role_code, @name) or contains(manlevel_from, @name) " + \
                    "or contains(manlevel_to, @name) or contains(created_on, @name)",name=searchText.strip())

            if(where != None and where != {}):
                try:
                    if where.has_key('filter') and  where.has_key('value') and len(where['filter']) and len(where['value']):
                        items.match(where["filter"],where["value"])
                except Exception as ex:
                    raise(Exception("syntax where error"))

            if(sort != None):
                items.sort(sort)

            return items.get_page(pageIndex, pageSize)
        except Exception as ex:
            raise(ex)

    return dict(
            error = "request parameter is not exist"
        )

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=models.LMSLS_MaterialManagement().aggregate()
    ret.left_join(models.models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.models.auth_user_info(), "modified_by", "username", "um")
    # Tìm kiếm theo advance search 
    # nếu không có advance search thì bỏ qua
    isWhereAdvance = False
    if(where != None):
        #search text
        if(where.has_key('searchAdvance') and where["searchAdvance"] != None):
            isWhereAdvance = True
            if(where["searchAdvance"].has_key('searchText') and where["searchAdvance"]["searchText"] != None): 
                if(where["searchAdvance"].has_key('search_criteria') and where["searchAdvance"]['search_criteria'] != None 
                   and where["searchAdvance"]['search_criteria'] == 1):
                    ret.match("(material_name==@name)",name=where["searchAdvance"]["searchText"])
                else:
                    ret.match("contains(material_name, @name)",name=where["searchAdvance"]["searchText"])

    # search theo Date Contributed from - Date Contributed to
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('date_contributed_from') and where["searchAdvance"]["date_contributed_from"] != None
           and where["searchAdvance"].has_key('date_contributed_to') and where["searchAdvance"]["date_contributed_to"] != None): 
            ret.match("(submit_date <= @date_contributed_to) and (submit_date >= @date_contributed_from)"
                          ,date_contributed_to=where["searchAdvance"]['date_contributed_to']
                          ,date_contributed_from=where["searchAdvance"]['date_contributed_from'])

    # search theo Date Created from - Date Created to
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('date_created_from') and where["searchAdvance"]["date_created_from"] != None
           and where["searchAdvance"].has_key('date_created_to') and where["searchAdvance"]["date_created_to"] != None): 
            ret.match("(publisher_date <= @date_created_to) and (publisher_date >= @date_created_from)"
                          ,date_created_to=where["searchAdvance"]['date_created_to']
                          ,date_created_from=where["searchAdvance"]['date_created_from'])
    
    # search theo size của file
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('size_from') and where["searchAdvance"]["size_from"] != None
           and where["searchAdvance"].has_key('size_to') and where["searchAdvance"]["size_to"] != None): 
            ret.match("(files.file_size <= @size_to) and (files.file_size >= @size_from)"
                          ,size_to=where["searchAdvance"]['size_to']
                          ,size_from=where["searchAdvance"]['size_from'])    
    
    # search theo category
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('category_id') and where["searchAdvance"]["category_id"] != None): 
            if(isinstance(where["searchAdvance"]['category_id'], list) == True):
                ret.match("level_code in @level_code", level_code=where["searchAdvance"]['category_id'])
            else:
                ret.match("level_code in @level_code", level_code=[where["searchAdvance"]['category_id']])

    #search theo Create By -> Author 
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('created_by') and where["searchAdvance"]["created_by"] != None): 
            ret.match("author_name == @author_name", author_name=where["searchAdvance"]['created_by'])

    #search theo Contributed by -> Created_by
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('contributed_by') and where["searchAdvance"]["contributed_by"] != None): 
            ret.match("created_by == @contributed_by", contributed_by=where["searchAdvance"]['contributed_by'])

    if(searchText != None):
        ret.match("contains(material_name, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)

    ret.project(
            material_id=1,
            material_name=1,
            material_name2=1,
            material_version=1,
            submit_user_id=1,
            submit_date=1,
            approve_user_id=1,
            approve_date=1,
            ordinal=1,
            note=1,
            lock=1,
            folder_id=1,
            author_name=1,
            course_name=1,
            size=1,
            creator=1,
            category=1,
            level_code=1,
            description=1,
            publisher_name=1,
            publisher_date=1,
            date_valid_from=1,
            date_valid_to=1,
            course_id=1,
            language=1,
            coverage=1,
            rights=1,
            relations=1,
            files=1,
            version=1,
            comments=1,
            identifier=1,           
            material_type=1,           
            source=1,    
            views=1,
            material_format=1,
            total_rating="avg(comments.rating)",
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    if(isWhereAdvance == True):
        #search star form - star to
            if(where["searchAdvance"].has_key('star_rating_from') and where["searchAdvance"]["star_rating_from"] != None and
               where["searchAdvance"].has_key('star_rating_to') and where["searchAdvance"]["star_rating_to"] != None):
                ret.match("(total_rating <= @star_rating_to) and (total_rating >= @star_rating_from)"
                          ,star_rating_to=where["searchAdvance"]['star_rating_to']
                          ,star_rating_from=where["searchAdvance"]['star_rating_from'])
    data_items = ret.get_page(pageIndex, pageSize)
    arrItems = []
     # search theo file format
    if(isWhereAdvance == True):
        if(where["searchAdvance"].has_key('file_format') and where["searchAdvance"]["file_format"] != None): 
            if(isinstance(where["searchAdvance"]['file_format'], list) == True):
                if(data_items["items"]!=None and len(data_items["items"]) > 0):
                    for x in data_items["items"]:
                        if (x['files']['file_extends'] in where["searchAdvance"]['file_format']):
                            arrItems.append(x)
                    data_items["items"] = arrItems
    
    return data_items


def get_data_info_details(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.left_join(models.LMSLS_MaterialFolder(), "category", "folder_id", "mf")
    ret.left_join(models.models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.models.auth_user_info(), "created_by", "username", "um")
    ret.project(
            material_id=1,
            material_name=1,
            material_name2=1,
            material_version=1,
            submit_user_id=1,
            submit_date=1,
            approve_user_id=1,
            approve_date=1,
            ordinal=1,
            note=1,
            lock=1,
            folder_id=1,
            author_name=1,
            course_name=1,
            size=1,
            creator=1,
            category=1,
            level_code=1,
            description=1,
            publisher_name=1,
            publisher_date=1,
            date_valid_from=1,
            date_valid_to=1,
            course_id=1,
            language=1,
            coverage=1,
            rights=1,
            relations=1,
            files=1,
            version=1,
            comments=1,
            identifier=1,           
            material_type=1,           
            source=1,                 
            material_format=1,
            views=1,
            category_name="mf.folder_name",
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    return ret.get_page(0, 100)

def get_data_info_comment(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    data_rating=models.LMSLS_MaterialManagement().aggregate()
    data_total_rating=count_star_on_comment(args)
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
        data_rating.match("(_id==@id)",id=ObjectId(where['id']))
    ret.unwind("comments", True)
    ret.project(
            id_comment= "comments.id_comment",
            content= "comments.content",
            rating= "comments.rating",
            created_on= "comments.created_on",
            id_user= "comments.id_user",
            login_account= "comments.login_account",
            total_vote="avg(comments.votes.number)",
            user_votes= "comments.votes.id_user",
            reply= "comments.reply"
        )
    data_rating.project(
            total_rating="avg(comments.rating)"
        )
    return dict(
            comments=check_user_ratinged(ret.get_list(), where),
            rating=data_rating.get_item(),
            data_rating=data_total_rating
        )


def get_data_info_link_share(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.project(
            link_file=1, 
        )
    return ret.get_page(0, 100)
def get_data_info_history_share_social(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.project(
            sharing_social=1, 
        )
    return ret.get_page(0, 100)
def get_data_info_history_version(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.project(
            material_version=1, 
        )
    return ret.get_page(0, 100)
def get_data_info_history_version(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.project(
            material_name=1,
            material_version=1,
            creator=1,
            created_on=1,
            
        )
    return ret.get_page(0, 100)
def get_data_info_history_download(args):
    where = args['data'].get('where')

    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.project(
            downloads=1, 
        )
    return ret.get_page(0, 100)
def get_list_with_select_node(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    collection = common.get_collection('LMSLS_MaterialManagement')
    where = args['data'].get('where')
    arrayData = []
    match = {}
    if(where['folder_id'] != None or searchText != None):
        match = {
                "$match": {
                }
            }
    if(where['folder_id'] != None):
        match["$match"]["level_code"] = where['folder_id']

    if(searchText != None):
        match["$match"]["material_name"] = { "$regex": ".*" + searchText + "*" }

    if(where['folder_id'] != None or searchText != None):
        arrayData.append(match)
    arrayData.append({
                "$project": {
                    "material_id":1,
                    "material_name":1,
                    "material_name2":1,
                    "material_version":1,
                    "submit_user_id":1,
                    "submit_date":1,
                    "approve_user_id":1,
                    "approve_date":1,
                    "ordinal":1,
                    "note":1,
                    "lock":1,
                    "folder_id":1,
                    "author_name":1,
                    "course_name": 1,
                    "size":1,
                    "version":1,
                    "creator":1,
                    "category":1,
                    "level_code":1,
                    "description":1,
                    "publisher_name":1,
                    "publisher_date":1,
                    "date_valid_from":1,
                    "date_valid_to":1,
                    "course_id":1,
                    "language":1,
                    "coverage":1,
                    "rights":1,
                    "relations":1,
                    "files":1,
                    "comments":1,
                    "identifier":1,           
                    "material_type":1,           
                    "source":1,                 
                    "material_format":1,        
                    "views":1,
                }
            })

    if(sort != None):
        arrayData.append({
            "$sort": sort    
        })
    ret=collection.aggregate(arrayData)
    return dict(
        items=list(ret),
        page_index=pageIndex,
        page_size=pageSize,
        total_items=list(ret).__len__()
    )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            temp = data
            del temp['material_version']
            del temp['version']
            dat = {
                "version":"v01.0.0",
                "data_version": json.loads(json.dumps(temp, default=json_util.default), object_hook=json_util.object_hook) 
            }
            data["material_version"] = [dat]
            data["version"]="v01.0.0"
            ret  =  models.LMSLS_MaterialManagement().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)
def post_comment(args):
    
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            where = args['data']['where']
            data =  set_dict_update_data_comment(where)
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(where['id']) },
                    {
                        '$push': {
                            "comments": data['comments']
                        }
                    }
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
def post_reply(args):
    
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            where = args['data']['where']
            data =  set_dict_update_data_reply(where)
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(where['id']) ,
                      "comments.id_comment":  ObjectId(where['id_comment'])                     
                    },
                    {
                        '$push': {
                            "comments.$.reply":  data['reply']
                        }
                    }
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
def update_info_sharing_file(args):
    
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            where = args['data']['where']
            data =  set_dict_update_sharing_file(where)
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(where['id']) },
                    {
                        '$push': {
                            "sharing_info": data['sharing_info']
                        }
                    }
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
def update_info_permission(args):
    
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = args['data']['where']
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(data['id']) },
                    {
                        '$set': {
                            "permission": data['permission']
                        }
                    }
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
def update_info_public_sharing_social(args):
    
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            where = args['data']['where']
            data =  set_dict_update_public_sharing_social(where)
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(where['id']) },
                    {
                        '$push': {
                            "sharing_social": data['sharing_social']
                        }
                    }
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
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            temp =  json.loads(json.dumps(data, default=json_util.default), object_hook=json_util.object_hook) 
            del temp['material_version']
            
            dat = {
                "version":process_version_material(data['version']),
                "data_version": temp,
            }
            data["material_version"].append(dat)
            data["version"]=process_version_material(data['version'])
            ret  =  models.LMSLS_MaterialManagement().update(
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
def process_version_material(args):
    version =args.lstrip('v')
    a,b,c=version.split('.')
    a=int(a)
    b=int(b)
    c=int(c)
    if c >= 9:
        c=0
        if b>=9:
            b=0
            a+=1
        else: 
            b+=1
    else: 
        c+=1
    if a<10 :
        str1 = "v"+"0"+str(a)+"."+str(b) +"." +str(c)
    else:
        str1 = "v"+str(a)+"."+str(b) +"." +str(c)
    return str1

    


def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.LMSLS_MaterialManagement().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        material_id             = (lambda x: x['material_id']           if x.has_key('material_id')             else None)(args['data']),
        material_name           = (lambda x: x['material_name']         if x.has_key('material_name')           else None)(args['data']),
        material_name2          = (lambda x: x['material_name2']        if x.has_key('material_name2')          else None)(args['data']),
        material_version        = (lambda x: x['material_version']      if x.has_key('material_version')        else None)(args['data']),
        submit_user_id          = (lambda x: x['submit_user_id']        if x.has_key('submit_user_id')          else None)(args['data']),
        submit_date             = (lambda x: x['submit_date']           if x.has_key('submit_date')             else None)(args['data']),
        approve_user_id         = (lambda x: x['approve_user_id']       if x.has_key('approve_user_id')         else None)(args['data']),
        approve_date            = (lambda x: x['approve_date']          if x.has_key('approve_date')            else None)(args['data']),
        ordinal                 = (lambda x: x['ordinal']               if x.has_key('ordinal')                 else 0)(args['data']),
        note                    = (lambda x: x['note']                  if x.has_key('note')                    else None)(args['data']),
        lock                    = (lambda x: x['lock']                  if x.has_key('lock')                    else False)(args['data']),
        folder_id               = (lambda x: x['folder_id']             if x.has_key('folder_id')               else None)(args['data']),
        author_name             = (lambda x: x['author_name']           if x.has_key('author_name')             else None)(args['data']),
        course_name             = (lambda x: x['course_name']           if x.has_key('course_name')             else None)(args['data']),
        size                    = (lambda x: x['size']                  if x.has_key('size')                    else None)(args['data']),
        creator                 = (lambda x: x['creator']               if x.has_key('creator')                 else None)(args['data']),
        category                = (lambda x: x['category']              if x.has_key('category')                else None)(args['data']),
        level_code              = (lambda x: x['level_code']            if x.has_key('level_code')              else None)(args['data']),
        description             = (lambda x: x['description']           if x.has_key('description')             else None)(args['data']),
        publisher_name          = (lambda x: x['publisher_name']        if x.has_key('publisher_name')          else None)(args['data']),
        publisher_date          = (lambda x: x['publisher_date']        if x.has_key('publisher_date')          else None)(args['data']),
        date_valid_from         = (lambda x: x['date_valid_from']       if x.has_key('date_valid_from')         else None)(args['data']),
        date_valid_to           = (lambda x: x['date_valid_to']         if x.has_key('date_valid_to')           else None)(args['data']),
        course_id               = (lambda x: x['course_id']             if x.has_key('course_id')               else None)(args['data']),
        language                = (lambda x: x['language']              if x.has_key('language')                else None)(args['data']),
        coverage                = (lambda x: x['coverage']              if x.has_key('coverage')                else None)(args['data']),
        rights                  = (lambda x: x['rights']                if x.has_key('rights')                  else None)(args['data']),
        relations               = (lambda x: x['relations']             if x.has_key('relations')               else None)(args['data']),
        files                   = (lambda x: x['files']                 if x.has_key('files')                   else None)(args['data']),
        link_file               = (lambda x: x['link_file']             if x.has_key('link_file')               else None)(args['data']),
        version                 = (lambda x: x['version']               if x.has_key('version')                 else None)(args['data']),
        identifier              = (lambda x: x['identifier']            if x.has_key('identifier')              else None)(args['data']),
        material_type           = (lambda x: x['material_type']         if x.has_key('material_type')           else None)(args['data']),
        source                  = (lambda x: x['source']                if x.has_key('source')                  else None)(args['data']),
        material_format         = (lambda x: x['material_format']       if x.has_key('material_format')         else None)(args['data']),
        views                   = (lambda x: x['views']                 if x.has_key('views')                   else 0)(args['data']),
    )

    return ret_dict

def set_dict_insert_data_comment(args):
    ret_dict = dict()
    user = "application"
    login_account= ""
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
        login_account = get_login_account(user)
    ret_dict.update(
        comments = dict(
            id_comment    = ObjectId(),
            content       = (lambda x: x['comments']      if x.has_key('comments')            else None)(args),
            id_user       = user,
            login_account = login_account,
            created_on    = datetime.datetime.now(),
            rating        = (lambda x: x['rating']         if x.has_key('rating')              else 0)(args)
        )
    )

    return ret_dict

def get_data_info_login_account(args):
    user = "application"
    login_account= ""
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
        login_account = get_login_account(user)      
    return dict(login_account=login_account)
def set_dict_insert_data_reply(args):
    ret_dict = dict()
    login_account= ""
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
        login_account = get_login_account(user)
    ret_dict.update(
        reply = dict(
            id_reply = ObjectId(),
            content = (lambda x: x['reply']                 if x.has_key('reply')                   else None)(args),
            id_user    = user,
            login_account= login_account,
            created_on = datetime.datetime.now(),
        )
    )

    return ret_dict


def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['folder_id']
    return ret_dict

def set_dict_update_data_comment(args):
    ret_dict = set_dict_insert_data_comment(args)
    return ret_dict
def set_dict_update_data_reply(args):
    ret_dict = set_dict_insert_data_reply(args)
    return ret_dict


def get_login_account(args):
    ret=models.models.auth_user_info().aggregate()
    ret.match("(username==@username)",username=args)
    return ret.get_item()["login_account"]

def get_list_employees(args):
    ret = models.models.HCSEM_Employees().aggregate()
    return ret.get_list()

def set_dict_rating_comment(args):
    ret_dict = dict()
    user = "application"
    login_account= ""
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
        login_account = get_login_account(user)
    ret_dict.update(
        ratings = dict(
            number          = (lambda x: x['rating']    if x.has_key('rating')    else 0)(args),
            id_user         = user,
            login_account   = login_account,
            created_on = datetime.datetime.now(),
        )
    )

    return ret_dict
def set_dict_update_sharing_file(args):
    ret_dict = set_dict_insert_sharing_files(args)
    return ret_dict
def set_dict_insert_sharing_files(args):
    ret_dict = dict()
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    ret_dict.update(
        sharing_info = dict(
            material_id   = (lambda x: x['id']           if x.has_key('id')              else None)(args),
            id_sharing    = ObjectId(),
            message       = (lambda x: x['sharing_info']['message']           if x['sharing_info'].has_key('message')                      else None)(args),          
            date_created  = datetime.datetime.now(),
            date_update   = datetime.datetime.now(),
            members_group = (lambda x: x['sharing_info']['members_group']           if x['sharing_info'].has_key('members_group')              else None)(args),
            invited_email = (lambda x: x['sharing_info']['invited_email']           if x['sharing_info'].has_key('invited_email')              else None)(args),
            
        )
    )

    return ret_dict
def set_dict_update_public_sharing_social(args):
    ret_dict = set_dict_insert_public_sharing_social(args)
    return ret_dict
def set_dict_insert_public_sharing_social(args):
    ret_dict = dict()
    user = "application"
    login_account= ""
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
        login_account = get_login_account(user)
    ret_dict.update(
        sharing_social = dict(
            material_id   = (lambda x: x['id']           if x.has_key('id')              else None)(args),
            id_sharing    = ObjectId(),
            social       = (lambda x: x['sharing_social']           if x.has_key('sharing_social')                      else None)(args),          
            date_created  = datetime.datetime.now(),
            login_account =login_account
            
        )
    )

    return ret_dict

def check_user_rating(args):
    try:
        ret={}
        collection = common.get_collection('LMSLS_MaterialManagement')
        ret=collection.aggregate([
            {
                "$match": {
                    "_id" : ObjectId(args['id']),
                    "comments": {
                        "$elemMatch": {
                            "id_comment": ObjectId(args['id_comment']),
                            "votes.id_user": threading.current_thread().user.username
                        }   
                    }
                }
            }    
        ])
        return list(ret)
    except Exception as ex:
        lock.release()
        raise(ex)

def rating_comment(args):
    try:
        lock.acquire()
        data=check_user_rating(args['data']['where'])
        if len(data) <= 0:
            ret = {}
            if args['data'] != None:
                where = args['data']['where']
                data =  set_dict_rating_comment(args['data'])
                collection  =  common.get_collection('LMSLS_MaterialManagement')
                ret = collection.update(
                        { "_id": ObjectId(where['id']) ,
                            "comments.id_comment":  ObjectId(where['id_comment'])                     
                        },
                        {
                            '$push': {
                                "comments.$.votes":  data['ratings']
                            }
                        }
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

def check_user_ratinged(args, where):
    for  x in range(0, len(args)):
        if args[x]["user_votes"] != None:
            if threading.current_thread().user.username in args[x]["user_votes"]:
                args[x]["is_vote"] = True
                args[x]["reply"] = get_reply_by_id_comment(where["id"], args[x]['id_comment'])
    return args


def count_star_on_comment(args):
    arr = []
    for x in range(0, 6):
        obj = {}
        where = args['data'].get('where')
        ret=models.LMSLS_MaterialManagement().aggregate()
        if(where != None):
            ret.match("(_id==@id)",id=ObjectId(where['id']))
        ret.unwind("comments", True)
        ret.match("(comments.rating==@rating)", rating=x)
        ret.project(
            total_rating="avg(comments.rating)",
        )
        data = ret.get_list()
        s = "rating"
        if(data != None):
            obj[s]=len(data)
        else:
            obj[s]=0
        arr.append(obj)
    return arr

def get_data_info_ratings(args):
    where = args['data'].get('where')

    data_rating=models.LMSLS_MaterialManagement().aggregate()
    data_check_user_rating=check_user_rating(ObjectId(where['id']))
    if(len(data_check_user_rating) > 0):
        data_check_user_rating = True
    else:
        data_check_user_rating = False
    if(where != None):
        data_rating.match("(_id==@id)",id=ObjectId(where['id']))
    data_rating.project(
            total_rating="avg(ratings.rating)"
        )
    return dict(
            rating=data_rating.get_item(),
            checked=data_check_user_rating
        )

def get_index_reply(args):
    try:
        ret = {}
        if args['data'] != None:
            where = args['data']['where']
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.aggregate([
                    {
                        "$match": {
                            "_id" : ObjectId(where['id'])
                        }
                    }, {
                        "$unwind": "$comments"
                    }, {
                        "$match": {
                            "comments.id_comment": ObjectId(where['id_comment'])
                        }
                    }, {
                        "$replaceRoot": {"newRoot": "$comments"}
                    },{
                        "$project":
                          {
                            "index": { 
                                "$indexOfArray": [ "$reply.id_reply", ObjectId(where['id_reply']) ] 
                             },
                          }
                    }    
                ])
            return ret
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def rating_reply(args):
    try:
        index_reply = list(get_index_reply(args))
        if len(index_reply) > 0:
            where = args['data']['where']
            idx = index_reply[0]["index"]
            obj_push = {}
            user = "application"
            login_account= ""
            if hasattr(threading.current_thread(),"user"):
                user = threading.current_thread().user.username
                login_account = get_login_account(user)
            obj_push["comments.$.reply." + str(idx) + ".votes"] = dict(
                    number=args['data']['rating'],
                    id_user=user,
                    login_account=login_account,
                    created_on=datetime.datetime.now()
                )
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update({
                "_id" : ObjectId(where['id']),
                "comments.id_comment": ObjectId(where['id_comment']),
                "comments.reply.id_reply": ObjectId(where['id_reply']),
            }, {
                "$push": obj_push
            })
            return ret
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)
def get_reply_by_id_comment(id, id_comment):
    try:
        user = "application"
        if hasattr(threading.current_thread(),"user"):
            user = threading.current_thread().user.username
        collection  =  common.get_collection('LMSLS_MaterialManagement')
        ret = collection.aggregate([
            {
                "$match": {
                    "_id" : ObjectId(id)
                }
            }, {
                "$unwind": "$comments"
            },{
                "$match": {
                    "comments.id_comment" : id_comment
                }
            }, {
                "$unwind": "$comments.reply"
            }, {
                "$replaceRoot": {"newRoot": "$comments.reply"}
            }, {
                "$project": {
                    "content" : 1,
        	        "created_on" : 1,
        	        "id_reply" : 1,
        	        "id_user" : 1,
        	        "login_account" : 1,
        	        "total_vote": {
        	            "$avg": "$votes.number"
        	        },
        	        "user_votes" : { 
        	            "$cond": [{
    	                    "$setIsSubset": [
        	                    [user], 
        	                    {"$ifNull": ["$votes.id_user", []]}
    	                    ]}, True, False
    	                ]}
                }
            }    
        ])
        return list(ret)
    except Exception as ex:
        raise(ex)

def get_file_by_master_id (args):
    try:
        if(args != None):
            collection = models.LMSLS_MaterialManagement().aggregate()
            ret = collection.match("(material_id==@material_id)",material_id=args)
            ret.project(
                files=1
            )
            return ret.get_item()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def insert_user_download_file(args):
    try:
        lock.acquire()
        ret = {}
        user = "application"
        login_account= ""
        if hasattr(threading.current_thread(),"user"):
            user = threading.current_thread().user.username
            login_account = get_login_account(user)
        if args['data'] != None:
            where = args['data']['where']
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(where['id']) },
                    {
                        '$push': {
                            "downloads": {
                                    "id_user": user,
                                    "login_account": login_account,
                                    "date_created": datetime.datetime.now(),
                                }
                        }
                    }
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
def get_list_group_user(args):
    try:
        if args['data'] != None:
                searchText      = args['data'].get('search', '')
                pageSize        = args['data'].get('pageSize', 0)
                pageIndex       = args['data'].get('pageIndex', 20)
                sort            = args['data'].get('sort', 20)

                pageIndex       = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
                pageSize        = (lambda pSize: pSize if pSize != None else 20)(pageSize)

                items = models.extend.AD_Roles().aggregate()
                items.join(models.HCSSYS_DataDomain(), "dd_code", "dd_code", "domain")
                items.project(
                        role_code       = 1,
                        role_name       = 1,
                        dd_code         = 1,
                        dd_name         = "switch(case(dd_code!='',domain.dd_name),'')",
                        description     = 1,
                        stop            = 1,
                        created_on      = 1
                        )

                items=common.filter_stop(items, args)

                if(searchText != None):
                    items.match("contains(role_name, @name) or contains(role_code, @name) " + \
                        "or contains(dd_code, @name) or contains(description, @name) " + \
                       "or contains(created_on, @name)",name=searchText.strip())

                if(sort != None):
                    items.sort(sort)
            
                return items.get_page(pageIndex, pageSize)

        return dict(
                error = "request parameter is not exist"
            )
    except Exception as ex:
        raise(ex)
def get_data_permission(args):
    where = args['data'].get('where')
    ret=models.LMSLS_MaterialManagement().aggregate()
    if(where != None):
        ret.match("(_id==@id)",id=ObjectId(where['id']))
    ret.project(
            permission=1, 
        )
    return ret.get_item()

def get_data_dash_board_page(args):
    ret=models.LMSLS_MaterialManagement().aggregate()
    len_ret =len(ret.get_list())
    ret_fold=models.LMSLS_MaterialFolder().aggregate()
    len_ret_fold =len(ret_fold.get_list())
    len_download = 0
    len_share    = 0
    for x in ret.get_list():
        if x.has_key('downloads'):
            len_download+=len(x['downloads'])
    for x in ret.get_list():
        if x.has_key('sharing_info'):
            len_share+=len(x['sharing_info'])
    for x in ret.get_list():
        if x.has_key('sharing_social'):
            len_share+=len(x['sharing_social'])
    list_element = ret.get_list()
    arr =[]
    
    for i in range(5):
        max=0
        for x in list_element:
            if x.has_key('views'):
                if x['views'] > max:
                    max=x['views']
                    arr.insert(len(arr),x)
                    list_element.remove(x)

    
    
    return dict(
        number_material= len_ret,
        number_folder= len_ret_fold,
        number_download =len_download,
        number_share =len_share,
        top_five_material = arr,
        
        )
def update_view_file(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            where = args['data']['where']
            collection  =  common.get_collection('LMSLS_MaterialManagement')
            ret = collection.update(
                    { "_id": ObjectId(where['id']) },
                    {
                        '$inc': {
                            "views": 1
                        }
                    }
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
