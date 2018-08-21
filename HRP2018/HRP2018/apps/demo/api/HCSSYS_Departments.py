# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import datetime
from Query import DepartmentGroup

def get_list(args):
    items = models.HCSSYS_Departments().aggregate().project(
        department_code = 1,
        department_name = 1,
        parent_code = 1
        )
    
    return items.get_list()


def get_tree(args):
    ret=DepartmentGroup.get_department_group()
    return ret.get_list()


    