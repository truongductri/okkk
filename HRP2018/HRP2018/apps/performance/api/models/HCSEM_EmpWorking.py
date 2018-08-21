from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False

def HCSEM_EmpWorking():
    global _hasCreated
    if not _hasCreated:
        dict_permission = dict()
        helpers.extent_model(
            "HCSEM_EmpWorking",
            "base",
            [['rec_id']],
            rec_id =helpers.create_field("text", True),
            employee_code=helpers.create_field("text", True),
            appoint=helpers.create_field("numeric", True),
            effect_date=helpers.create_field("date", True),
            begin_date=helpers.create_field("date", True),
            end_date=helpers.create_field("date"),
            decision_no=helpers.create_field("text", True),
            signed_date=helpers.create_field("date"),
            signer_code=helpers.create_field("text"),
            note=helpers.create_field("text"),
            task=helpers.create_field("text"),
            reason=helpers.create_field("text"),
            department_code=helpers.create_field("text"),
            job_pos_code=helpers.create_field("text"),
            job_w_code=helpers.create_field("text"),
            emp_type_code=helpers.create_field("text"),
            region_code=helpers.create_field("text"),
            department_code_old=helpers.create_field("text"),
            job_pos_code_old=helpers.create_field("text"),
            job_w_code_old=helpers.create_field("text"),
            emp_type_code_old=helpers.create_field("text"),
            region_code_old=helpers.create_field("text"),
            province_code=helpers.create_field("text"),
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

        helpers.events("HCSEM_EmpWorking").on_before_insert(on_before_insert).on_before_update(on_before_update)

        _hasCreated=True
    ret = db_context.collection("HCSEM_EmpWorking")

    return ret