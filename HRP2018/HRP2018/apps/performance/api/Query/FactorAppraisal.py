from .. import models
from .. import common
def display_list_factor_appraisal(group_code):
    ret=models.TMLS_FactorAppraisal().aggregate()
    ret.join(models.TMLS_FactorAppraisalGroup(), "factor_group_code", "factor_group_code", "fag")
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    if group_code != None and group_code != "":
        ret.match('fag.level_code == {0}', group_code)
    ret.project(
        factor_code="factor_code",
        factor_name="factor_name",
        factor_name2="factor_name2",
        factor_group_code="factor_group_code",
        weight="weight",
        is_apply_all="is_apply_all",
        note="note",
        ordinal="ordinal",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def update_job_working(args):
    try:
        collection  =  common.get_collection('HCSLS_Acadame')
        ret = collection.update(
            {
                "factor_code": args['data']['factor_code'],
            },
            {
                "$set": {
                    'job_working': args['data']['job_working']
                    }
            })
    except Exception as ex:
        raise ex
