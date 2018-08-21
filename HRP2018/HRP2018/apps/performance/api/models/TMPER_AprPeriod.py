from config import database, helpers, db_context
import base
import datetime
_hasCreated=False
def TMPER_AprPeriod():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMPER_AprPeriod",
            "base",
            [["apr_period", "apr_year"]],
            apr_period=helpers.create_field("numeric", True),
			apr_year=helpers.create_field("numeric", True),
            give_target_from=helpers.create_field("date"),
            give_target_to=helpers.create_field("date"),
            review_mid_from=helpers.create_field("date"),
            review_mid_to=helpers.create_field("date"),
			approval_mid_from=helpers.create_field("date"),
            approval_mid_to=helpers.create_field("date"),
            emp_final_from=helpers.create_field("date"),
            emp_final_to=helpers.create_field("date"),
            approval_final_from=helpers.create_field("date"),
            approval_final_to=helpers.create_field("date"),
            note=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    return db_context.collection("TMPER_AprPeriod")

