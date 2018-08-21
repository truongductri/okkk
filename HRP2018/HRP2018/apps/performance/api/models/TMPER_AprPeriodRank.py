from config import database, helpers, db_context
import base
_hasCreated=False
def TMPER_AprPeriodRank():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMPER_AprPeriodRank",
            "base",
            [["apr_period"]],
            apr_period=helpers.create_field("numeric", True),
            apr_year=helpers.create_field("numeric", True),
            department_code=helpers.create_field("text"),
            rank_code_1=helpers.create_field("text"),
            percent_1=helpers.create_field("numeric"),
            rank_code_2=helpers.create_field("text"),
            percent_2=helpers.create_field("numeric"),
            rank_code_n=helpers.create_field("text"),
            percent_n=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("TMPER_AprPeriodRank")

    return ret