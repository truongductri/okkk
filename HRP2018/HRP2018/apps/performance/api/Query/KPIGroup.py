from .. import models


def check_exits_kpicode_within_kpiGroup(list_kpi_group_code):
    list_kpi_group = models.TMLS_KPIGroup().aggregate().match("kpi_group_code in {0}", list_kpi_group_code).get_list()
    if (list_kpi_group != None) and len(list_kpi_group) > 0:
        return True
    return False
def get_kpi_group(lock): 
    if lock != None:
        if (int(lock) == 0):
            lock = False
        elif (int(lock) == 1):
            lock = True
        else: 
            lock = None;    
    ret = models.TMLS_KPIGroup().aggregate();
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc");
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um");

    if lock != None:
        ret.match("lock == {0}", lock);

    ret.project(kpi_group_code = 1,
        kpi_group_name = 1,
        kpi_group_name2 = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        weight= 1,
        is_team=1,
        note = 1,
        ordinal = 1,
        lock = 1,
        created_by="uc.login_account",
        created_on= "created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(kpi_group_code = 1,
        ordinal = 1)) 
    return ret



