from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False

def HCSEM_EmpExperience():
    global _hasCreated
    if not _hasCreated:
        dict_permission = dict()
        helpers.extent_model(
            "HCSEM_EmpExperience",
            "base",
            [['rec_id']],
            rec_id =helpers.create_field("text", True),
            employee_code=helpers.create_field("text"),
            begin_date=helpers.create_field("date", True),
            end_date=helpers.create_field("date"),
            salary=helpers.create_field("numeric", True),
            currency_code=helpers.create_field("text"),
            emp_type_code=helpers.create_field("text"),
            job_pos_code=helpers.create_field("text"),
            job_w_code=helpers.create_field("text"),
            working_on=helpers.create_field("text"),
            working_location=helpers.create_field("text", True),
            address=helpers.create_field("text"),
            profession_code=helpers.create_field("text"),
            quit_job_code=helpers.create_field("text"),
            reason=helpers.create_field("text"),
            ref_info=helpers.create_field("text"),
            note=helpers.create_field("text"),
            is_na_company=helpers.create_field("bool"),
            is_in_section=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        def on_before_insert(data):
            data.update({
                "rec_id": common.generate_guid()
                })

        def on_before_update(data):
            pass

        helpers.events("HCSEM_EmpExperience").on_before_insert(on_before_insert).on_before_update(on_before_update)

        _hasCreated=True
    ret = db_context.collection("HCSEM_EmpExperience")

    return ret