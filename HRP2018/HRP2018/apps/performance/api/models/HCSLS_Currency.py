from config import database, helpers, db_context
import base
_hasCreated=False
def HCSLS_Currency():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_Currency",
            "base",
            [["currency_code"]],
			currency_code=helpers.create_field("text", True),
            currency_name=helpers.create_field("text", True),
            currency_name2=helpers.create_field("text"),
            temp_rate=helpers.create_field("numeric"),
            multiply=helpers.create_field("bool",True),
            cons_code=helpers.create_field("text"),
            dec_place=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
			lock=helpers.create_field("bool"),
            ordinal=helpers.create_field("numeric"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True
    ret = db_context.collection("HCSLS_Currency")

    return ret


