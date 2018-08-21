# -*- coding: utf-8 -*-
import models
import common
import logging
import datetime
import threading
import quicky
logger = logging.getLogger(__name__)

def get_tree_kpi(args):
    ret=models.TMLS_KPIGroup().aggregate().project(
        kpi_group_code = 1,
        kpi_group_name = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        lock = 1
        ).match("lock != {0}", True)
        
    return ret.get_list()

#def get_list_kpi(args):
#    searchText = args['data'].get('search', '')
#    pageSize = args['data'].get('pageSize', 0)
#    pageIndex = args['data'].get('pageIndex', 20)
#    sort = args['data'].get('sort', 20)

#    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
#    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

#    ret = models.TMLS_KPI().aggregate()
#    ret.left_join(models.SYS_VW_ValueList(), "cycle_type", "value", "val")
#    ret.match("val.list_name == {0}", "LCycleType")
#    ret.left_join(models.HCSLS_Unit(), "unit_code", "unit_code", "unit")
#    ret.project(
#        kpi_code      = "kpi_code",
#        kpi_name      = "kpi_name",
#        unit_code     = "unit.unit_name",
#        cycle_type    = "val.caption",
#        kpi_desc      = "kpi_desc",
#        weight        = "weight",
#        benchmark     = "benchmark",
#        is_apply_all  = "is_apply_all",
#        lock          = "lock"
#        )
#    ret.match("lock != {0}", True)

#    if(sort != None):
#        ret.sort(sort)
        
#    return ret.get_page(pageIndex, pageSize)

def get_list_kpi(args):
    searchText = args['data'].get('search', '')
    page_size = args['data'].get('pageSize', 0)
    page_index = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    collection = common.get_collection('TMLS_KPI')
    ret = collection.aggregate([
    {'$lookup': {
        'foreignField': 'value', 
        'as': 'val', 
        'from': common.get_collection_name_with_schema('SYS_VW_ValueList'),
        'localField': 'cycle_type'
        }
    }, 
    {'$unwind': {
        'path': '$val', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$match': {   
        '$and':[{
                    '$or' :[{ 'val.list_name':None},
                            { 'val.list_name':'LCycleType'}]
                },
                {
                    '$or' :[{ 'val.language':None},
                            { 'val.language': common.get_language()}]
                }]
        }
    },
    {'$lookup': {
        'foreignField': 'unit_code', 
        'as': 'unit', 
        'from': common.get_collection_name_with_schema('HCSLS_Unit'), 
        'localField': 'unit_code'
        }
    }, 
    {'$unwind': {
        'path': '$unit', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$lookup': {
        'foreignField': 'kpi_group_code', 
        'as': 'kpig', 
        'from': common.get_collection_name_with_schema('TMLS_KPIGroup'), 
        'localField': 'kpi_group_code'
        }
    }, 
    {'$unwind': {
        'path': '$kpig', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$project': {
        'kpi_name': '$kpi_name', 
        'is_apply_all': '$is_apply_all', 
        'kpi_desc': '$kpi_desc', 
        'cycle_type': { '$ifNull': [ '$val.caption', '' ] }, 
        'kpi_code': '$kpi_code', 
        'level_code': '$kpig.level_code',
        'weight': '$weight', 
        'unit_code': { '$ifNull': [ '$unit.unit_name', '' ] }, 
        'lock': '$lock', 
        'benchmark': { '$ifNull': [ '$benchmark', '' ] }
        }
    }, 
    {'$match': {'lock': {'$ne': True}, 'level_code':{'$eq':args['data']['kpi_group_code']}}}, 
    {'$sort': {'kpi_code': 1}},
    {"$facet": {
           "metadata": [{ "$count": "total" }, { "$addFields": { "page_index": page_index, "page_size": page_size } }],
           "data": [{ "$skip": page_size * page_index }, { "$limit": page_size }]
       }
    },
    {"$unwind": { "path": '$metadata', "preserveNullAndEmptyArrays": False }},
    {"$project": {
            'page_size': '$metadata.page_size',
            'page_index': '$metadata.page_index',
            'total_items': '$metadata.total',
            'items': '$data'
        }
    }])

    return (lambda x: x[0] if x != None and len(x) > 0 else {
        'page_size': page_size,
        'page_index': page_index,
        'total_items': 0,
        'items': []
        })(list(ret))