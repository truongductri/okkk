from .. import models
def display_list_apr_period():
    ret=models.TMPER_AprPeriod().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        apr_period="apr_period",
        apr_year="apr_year",
        emp_final_from="emp_final_from",    
		emp_final_to="emp_final_to",
        approval_final_from="approval_final_from",
        approval_final_to="approval_final_to",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        apr_year = 1
        ))

    return ret



def get_empNotApr_by_apr_period():
    ret=models.TMPER_AprPeriodEmpOut().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.left_join(models.HCSEM_Employees(), "employee_code", "employee_code", "ee")
    ret.project(
        apr_period="apr_period",
        apr_year="apr_year",
        employee_code="employee_code",
        department_code="department_code",
        job_w_code="job_w_code",
        reason="reason",
        note="note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        employee_name = "switch(case(employee_code!='',concat(ee.last_name, ' ' , ee.first_name)),'')",
    )
    ret.sort(dict(
        employee_code =1,
    ))

    return ret




