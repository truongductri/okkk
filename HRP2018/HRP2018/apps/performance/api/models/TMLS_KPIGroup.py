from config import database, helpers, db_context
import base
_hasCreated=False
def TMLS_KPIGroup():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMLS_KPIGroup",
            "base",
            [["kpi_group_code"]],
            kpi_group_code = helpers.create_field("text", True),
            kpi_group_name = helpers.create_field("text", True),
            kpi_group_name2 = helpers.create_field("text"),
            parent_code = helpers.create_field("text"),
            level = helpers.create_field("numeric"),
            level_code = helpers.create_field("list"),
            weight = helpers.create_field("numeric"),
            is_team = helpers.create_field("bool"),
            note = helpers.create_field("text"),
            ordinal = helpers.create_field("numeric"),
            lock = helpers.create_field("bool"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("TMLS_KPIGroup")

    return ret