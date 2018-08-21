from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Unit():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Unit",
            "base",
            [["unit_code"]],
			unit_code=helpers.create_field("text", True),
            unit_name=helpers.create_field("text", True),
            unit_name2=helpers.create_field("text"),
            note=helpers.create_field("text"),
			lock=helpers.create_field("bool"),
            ordinal=helpers.create_field("numeric"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Unit")

    return ret


