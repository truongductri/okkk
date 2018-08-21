from .. import models
from .. import common
def display_list_job_working(group_code):
    ret=models.HCSLS_JobWorking().aggregate()
    ret.join(models.HCSLS_JobWorkingGroup(), "gjw_code", "gjw_code", "jwg")
    ret.left_join(models.HCSEM_Employees(), "report_to_job_w", "employee_code", "emp")
    if group_code != None and group_code != "":
        ret.match('jwg.level_code == {0}', group_code)
    ret.project(
        job_w_code="job_w_code",
        job_w_name="job_w_name",
        report_to_job_w="emp.last_name + emp.first_name",
        lock = "lock",
        ordinal="ordinal"
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_job_working_group_by_group_code(gjw_code):
    rs = models.HCSLS_JobWorkingGroup().aggregate().project(gjw_code = 1, gjw_name = 1, ordinal = 1).match("gjw_code == {0}", gjw_code).sort({"ordinal":1}).get_item()
    return rs

def get_job_description_by_job_working_code(job_w_code):
    ret=models.HCSLS_JobWorking().aggregate()
    ret.join(models.HCSLS_JobWorkingGroup(), "gjw_code", "gjw_code", "gjw")
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        job_w_code="job_w_code",
        job_w_name="job_w_name",
        job_w_name2="job_w_name2",
        gjw_code="gjw_code",
        gjw_name="gjw.gjw_name",
        effect_date="effect_date",
        job_pos_code="job_pos_code",
        is_job_w_main_staff="is_job_w_main_staff",
        report_to_job_w="report_to_job_w",
        dept_contact="dept_contact",
        dept_apply="dept_apply",
        job_w_next="job_w_next",
        job_w_change="job_w_change",
        description="description",
        job_w_duty="job_w_duty",
        ordinal="ordinal",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    ret.match("job_w_code == {0}", job_w_code)
    ret.sort(dict(
        ordinal = 1
    ))

    return ret

def get_list_permission_and_mission_by_job_working_code(job_w_code):
    ret=models.HCSLS_JobWorking().aggregate()
    ret.match("job_w_code == {0}", job_w_code)
    ret.unwind("task")
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        job_w_code="job_w_code",
        rec_id ="task.rec_id",
        task_name="task.task_name",
        weight="task.weight",
        description="task.description",
        ordinal="task.ordinal",
        created_by="uc.login_account",
        created_on="task.created_on",
        modified_on="switch(case(task.modified_on!='',task.modified_on),'')",
        modified_by="switch(case(task.modified_by!='',um.login_account),'')",
    )
    ret.match("task_name != {0}", None)
    ret.sort(dict(
        ordinal = 1
    ))

    return ret

def insert_job_description(args, task):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
                          { "job_w_code": args['data']['job_w_code'] },
                          {
                            '$push': {
                              "task": task
                            }
                          }
                        )
    return ret

def insert_job_kpi(args, task):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
                          { "job_w_code": args['data']['job_w_code'] },
                          {
                            '$push': {
                              "kpi": task
                            }
                          }
                        )
    return ret

def remove_job_description(args):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
                        {
                            "job_w_code": args['data']['job_w_code']
                        },
                        {
                            '$pull':{"task" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
    return ret

def remove_kpi(args):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
                        {
                            "job_w_code": args['data']['job_w_code']
                        },
                        {
                            '$pull':{"kpi" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
    return ret

def update_job_description(args, task):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
        {
            "job_w_code": args['data']['job_w_code'],
            "task":{
                "$elemMatch":{
                    "rec_id":args['data']['task']["rec_id"]
                    }
                }
        },
        {
            "$set": {
                'task.$.task_name': task['task_name'],
                'task.$.weight': task['weight'],
                'task.$.description': task['description'],
                'task.$.ordinal': task['ordinal'],
                'task.$.modified_by': task['modified_by'],
                'task.$.modified_on': task['modified_on']
                }
        })
    return ret

def update_job_kpi(args, kpi):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
        {
            "job_w_code": args['data']['job_w_code'],
            "kpi":{
                "$elemMatch":{
                    "rec_id":args['data']['kpi']["rec_id"]
                    }
                }
        },
        {
            "$set": {
                'kpi.$.kpi_name': kpi['kpi_name'],
                'kpi.$.ordinal': kpi['ordinal'],
                'kpi.$.unit': kpi['unit'],
                'kpi.$.cycle': kpi['cycle'],
                'kpi.$.weight': kpi['weight'],
                'kpi.$.modified_by': kpi['modified_by'],
                'kpi.$.modified_on': kpi['modified_on']
                }
        })
    return ret

def insert_evaluation_factor(args, factor_appraisal):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
                          { "job_w_code": args['data']['job_w_code'] },
                          {
                            '$push': {
                              "factor_appraisal": factor_appraisal
                            }
                          }
                        )
    return ret

def update_evaluation_factor(args, factor_appraisal):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
        {
            "job_w_code": args['data']['job_w_code'],
            "factor_appraisal":{
                "$elemMatch":{
                    "rec_id":args['data']['factor_appraisal']["rec_id"]
                    }
                }
        },
        {
            "$set": {
                'factor_appraisal.$.factor_code': factor_appraisal['factor_code'],
                'factor_appraisal.$.weight': factor_appraisal['weight'],
                'factor_appraisal.$.modified_by': factor_appraisal['modified_by'],
                'factor_appraisal.$.modified_on': factor_appraisal['modified_on']
                }
        })
    return ret

def delete_evaluation_factor(args):
    collection  =  common.get_collection('HCSLS_JobWorking')
    ret = collection.update(
                        {
                            "job_w_code": args['data']['job_w_code']
                        },
                        {
                            '$pull':{"factor_appraisal" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
    return ret

def get_list_job_specific_by_job_working_code(job_w_code):
    pass

def get_list_evaluation_factor_by_job_working_code(job_w_code):
    ret=models.HCSLS_JobWorking().aggregate()
    ret.match("job_w_code == {0}", job_w_code)
    ret.unwind("factor_appraisal")
    ret.join(models.TMLS_FactorAppraisal(), "factor_appraisal.factor_code", "factor_code", "fac")
    ret.join(models.TMLS_FactorAppraisalGroup(), "fac.factor_group_code", "factor_group_code", "fac_g")
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        job_w_code="job_w_code",
        rec_id ="factor_appraisal.rec_id",
        factor_code="factor_appraisal.factor_code",
        factor_name="fac.factor_name",
        factor_group_name="fac_g.factor_group_name",
        weight="factor_appraisal.weight",
        created_by="uc.login_account",
        created_on="factor_appraisal.created_on",
        modified_on="switch(case(factor_appraisal.modified_on!='',factor_appraisal.modified_on),'')",
        modified_by="switch(case(factor_appraisal.modified_by!='',um.login_account),'')",
    )
    ret.match("factor_code != {0}", None)
    ret.sort(dict(
        ordinal = 1
    ))

    return ret

def get_evaluation_file_by_job_working_code(job_w_code):
    pass