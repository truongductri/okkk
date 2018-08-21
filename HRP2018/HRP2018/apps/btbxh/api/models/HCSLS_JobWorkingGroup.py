# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSLS_JobWorkingGroup():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSLS_JobWorkingGroup",
            "base",
            [["gjw_code"]],
            gjw_code=helpers.create_field("text", True),
            gjw_name=helpers.create_field("text", True),
            gjw_name2=helpers.create_field("text"),
            level_code=helpers.create_field("list"),
            parent_code=helpers.create_field("text"),
            level=helpers.create_field("numeric"), 
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"), 
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("HCSLS_JobWorkingGroup")

    return ret