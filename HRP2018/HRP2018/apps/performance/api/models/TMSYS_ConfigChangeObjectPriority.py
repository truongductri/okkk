# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def TMSYS_ConfigChangeObjectPriority():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TMSYS_ConfigChangeObjectPriority",
            "base",
            [[]],
            value_list_key = helpers.create_field('text'),
            change_object = helpers.create_field('numeric'),
            change_object_name = helpers.create_field('text'),
            priority_no = helpers.create_field('numeric'),
            table_name = helpers.create_field('text'),
            note = helpers.create_field('text'),
            language = helpers.create_field('numeric'),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
        _hasCreated=True

    ret = db_context.collection("TMSYS_ConfigChangeObjectPriority")

    return ret