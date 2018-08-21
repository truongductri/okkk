from config import database, helpers, db_context
import base
_hasCreated=False
def TMLS_FactorAppraisal():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMLS_FactorAppraisal",
            "base",
            [["factor_code"]],
            factor_code = helpers.create_field("text", True),
            factor_name = helpers.create_field("text", True),
            factor_name2 = helpers.create_field("text"),
            factor_group_code = helpers.create_field("text"),
            weight = helpers.create_field("numeric"),
            is_apply_all = helpers.create_field("bool"),
            job_working = helpers.create_field("list"),
            note = helpers.create_field("text"),
            ordinal = helpers.create_field("numeric"),
            lock = helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("TMLS_FactorAppraisal")

    return ret