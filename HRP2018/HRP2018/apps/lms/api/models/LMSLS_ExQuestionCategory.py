# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def LMSLS_ExQuestionCategory():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "LMSLS_ExQuestionCategory",
            "base",
            [["category_id"]],
            #id=helpers.create_field("numeric",True),
            category_id=helpers.create_field("text", True),
            category_name=helpers.create_field("text", True),
            category_name2=helpers.create_field("text"),
            parent_id=helpers.create_field("text"),
            parent_code=helpers.create_field("text"),
            level=helpers.create_field("numeric"),
            level_code=helpers.create_field("list"),
            order=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            active=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
        _hasCreated=True
    ret = db_context.collection("LMSLS_ExQuestionCategory")

    return ret