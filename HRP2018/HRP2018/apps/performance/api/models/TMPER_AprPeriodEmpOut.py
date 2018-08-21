from config import database, helpers, db_context
import base
_hasCreated=False
def TMPER_AprPeriodEmpOut():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMPER_AprPeriodEmpOut",
            "base",
            [["apr_period"]],
            apr_period=helpers.create_field("numeric", True),
            apr_year=helpers.create_field("numeric", True),
            employee_code=helpers.create_field("text"),
            department_code=helpers.create_field("text"),
            job_w_code=helpers.create_field("text"),
            reason=helpers.create_field("text"),
            note=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("TMPER_AprPeriodEmpOut")

    return ret