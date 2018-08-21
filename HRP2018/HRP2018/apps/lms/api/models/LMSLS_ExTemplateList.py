# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def LMSLS_ExTemplateList():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "LMSLS_ExTemplateList",
            "base",
            [["ques_id"]],
            ques_id=helpers.create_field("text", True),
            ques_category=helpers.create_field("text", True),
            ques_type=helpers.create_field("numeric"),
            ques_level=helpers.create_field("numeric"),
            ques_file=helpers.create_field("object"),
            ques_detail_1=helpers.create_field("text"),
            ques_detail_2=helpers.create_field("text"),
            ques_hint=helpers.create_field("object"),
            ques_answers=helpers.create_field("list", False, dict(
                    text=helpers.create_field("text"),
                    isCorrect=helpers.create_field("bool"),
                    answers=helpers.create_field("text"),
                    if_correct=helpers.create_field("text"),
                    if_incorrect=helpers.create_field("text"),
                    question=helpers.create_field("text"),
                )),
            ques_total_marks=helpers.create_field("object"),
            ques_attach_file=helpers.create_field("bool"),
            ques_max_answer_time=helpers.create_field("numeric"),
            ques_explanation=helpers.create_field("text"),
            ques_answer_options=helpers.create_field("numeric"),
            ques_randomization=helpers.create_field("numeric"),
            ques_tags=helpers.create_field("list"),
            ques_evaluated_by=helpers.create_field("text"),
            ques_limit_on_text=helpers.create_field("numeric"),
            ques_specify_limit=helpers.create_field("numeric"),
        )
        _hasCreated=True
    ret = db_context.collection("LMSLS_ExTemplateList")

    return ret