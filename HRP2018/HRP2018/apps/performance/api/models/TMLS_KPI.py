from config import database, helpers, db_context
import base
_hasCreated=False
def TMLS_KPI():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMLS_KPI",
            "base",
            [["kpi_code"]],
            kpi_code = helpers.create_field("text", True),
            kpi_name = helpers.create_field("text", True),
            kpi_name2 = helpers.create_field("text"),
            kpi_group_code = helpers.create_field("text"),
            unit_code=helpers.create_field("text"),
            cycle_type=helpers.create_field("numeric"),
            kpi_desc=helpers.create_field("text"),
            kpi_ref=helpers.create_field("text"),
            weight=helpers.create_field("text"),
            benchmark=helpers.create_field("text"),
            kpi_formula=helpers.create_field("text"),
            value_cal_type=helpers.create_field("numeric", True),
            input_type=helpers.create_field("numeric"),
            is_apply_all=helpers.create_field("bool"),
            kpi_years=helpers.create_field("text"),
            is_kpi_not_weight=helpers.create_field("bool"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("TMLS_KPI")

    return ret