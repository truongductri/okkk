from .. import models
def get_emp_experience_by_emp_code(emp_code):
    ret=models.HCSEM_EmpExperience().aggregate()
    ret.match("employee_code == {0}", emp_code)
    ret.left_join(models.HCSLS_Position(), "job_pos_code", "job_pos_code", "pos")
    ret.left_join(models.HCSLS_JobWorking(), "job_w_code", "job_w_code", "job")
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        employee_code="employee_code",
        begin_date="begin_date",
        end_date="end_date",
        salary="salary",
        currency_code="currency_code",
        emp_type_code="emp_type_code",
        job_pos_code="job_pos_code",
        job_w_code="job_w_code",
        working_on="working_on",
        working_location="working_location",
        address="address",
        profession_code="profession_code",
        quit_job_code="quit_job_code",
        reason="reason",
        ref_info="ref_info",
        note="note",
        is_na_company="is_na_company",
        is_in_sectio="is_in_section",
        job_pos_name="pos.job_pos_name",
        job_w_name="job.job_w_name",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        begin_date = 1
        ))

    return ret