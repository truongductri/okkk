from .. import models


#def check_exits_factCode_within_factGroup(list_factor_group):
#    list_factCode = models.TMLS_FactorAppraisal().aggregate().match("factor_group_code in {0}", list_factor_group).get_list()
#    if (list_factCode != None) and len(list_factCode) > 0:
#        return True
#    return False


def get_department_group():
    ret=models.HCSSYS_Departments().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        department_code = "department_code",
        department_name = "department_name",
        department_name2 = "department_name2",
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




