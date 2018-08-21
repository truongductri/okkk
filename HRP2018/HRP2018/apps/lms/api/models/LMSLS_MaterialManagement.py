# -*- coding: utf-8 -*-
from config import database, helpers, db_context, qview
from performance.api import common
_hasCreated=False

def LMS_VW_Author_Name():
    return qview.create_mongodb_view(
            LMSLS_MaterialManagement().aggregate().project(
                    author_name=1
                ).match("author_name != {0}", None)  
        ,
        "LMS_VW_Author_Name"
        )

def LMSLS_MaterialManagement():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "LMSLS_MaterialManagement",
            "base",
            [["material_id"]],
            #id=helpers.create_field("numeric",True),
            material_id=helpers.create_field("text", True), 
            material_name=helpers.create_field("text", True),
            material_name2=helpers.create_field("text"),
            material_version=helpers.create_field("list"),
            version=helpers.create_field("text"),
            submit_user_id=helpers.create_field("text"),
            submit_date=helpers.create_field("date"),
            approve_user_id=helpers.create_field("text"),
            approve_date=helpers.create_field("date"),
            ordinal=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            lock=helpers.create_field("bool"),
            source=helpers.create_field("text"),
            material_format=helpers.create_field("text"),
            folder_id=helpers.create_field("text"),
            author_name=helpers.create_field("text"),
            course_name=helpers.create_field("text"),
            views=helpers.create_field("list",False,dict(
                id_user=helpers.create_field("text"),
                login_account=helpers.create_field("text"),
                date_created=helpers.create_field("date"),
            )),
            size=helpers.create_field("text"),
            creator=helpers.create_field("text"),
            category=helpers.create_field("text",True),
            level_code=helpers.create_field("list"),
            identifier=helpers.create_field("text",True),
            material_type=helpers.create_field("text",True),
            description=helpers.create_field("text",True),
            publisher_name=helpers.create_field("text"),
            publisher_date=helpers.create_field("date"),
            date_valid_from=helpers.create_field("date",True),
            date_valid_to=helpers.create_field("date"),
            course_id=helpers.create_field("text"),
            language=helpers.create_field("text"),
            coverage=helpers.create_field("text"),
            rights=helpers.create_field("text",True),
            link_file=helpers.create_field("text"),
            permission=helpers.create_field("list"),
            relations=helpers.create_field("list",False,dict(
                ref_relation=helpers.create_field("text"),
                intro_relation=helpers.create_field("text"),
            )),
            files=helpers.create_field("object",False,dict(
                file_thumbnail=helpers.create_field("text"),
                file_name=helpers.create_field("text"),
                file_type=helpers.create_field("text"),
                file_size=helpers.create_field("numeric"),
                file_data=helpers.create_field("text"),
                file_extends=helpers.create_field("text"),
            )),
            comments=helpers.create_field("list",False,dict(
                id_comment=helpers.create_field("text"),
                id_user=helpers.create_field("text"),
                login_account=helpers.create_field("text"),
                content=helpers.create_field("text"),
                created_on=helpers.create_field("date"),
                rating=helpers.create_field("numeric"),
                votes=helpers.create_field("list",False,dict(
                    number=helpers.create_field("numeric"),
                    id_user=helpers.create_field("text"),
                    login_account=helpers.create_field("text"),
                    created_on=helpers.create_field("date"),
                )),
                reply=helpers.create_field("list",False,dict(
                    id_user=helpers.create_field("text"),
                    content=helpers.create_field("text"),
                    created_on=helpers.create_field("date"), 
                    login_account=helpers.create_field("text"),
                    id_reply=helpers.create_field("text"),
                    votes=helpers.create_field("list",False,dict(
                        number=helpers.create_field("numeric"),
                        id_user=helpers.create_field("text"),
                        login_account=helpers.create_field("text"),
                        created_on=helpers.create_field("date"),
                    )),
                )),
            )),
            sharing_info=helpers.create_field("list",False,dict(
            	material_id=helpers.create_field("text"),
                message=helpers.create_field("text"),
                date_created=helpers.create_field("date"),
                date_update=helpers.create_field("date"),
                members_group=helpers.create_field("list"),
                invited_email=helpers.create_field("list"),
            )),
            sharing_social=helpers.create_field("list",False,dict(
            	material_id=helpers.create_field("text"),
                social=helpers.create_field("text"),
                date_created=helpers.create_field("date"),
            )),
            downloads=helpers.create_field("list",False,dict(
            	id_user=helpers.create_field("text"),
                login_account=helpers.create_field("text"),
                date_created=helpers.create_field("date"),
            )),
        )
        def on_before_insert(data):
            pass

        def on_before_update(data):
            if data.has_key("comments"):
                data['comments'].update({
                    "_id":common.generate_guid()
                    })
                #data.update({
                #    "detail": [{
                #            "department_code":x['department_code'],
                #            } for x in data.get('detail',[])]
                #    })

        helpers.events("LMSLS_MaterialManagement").on_before_insert(on_before_insert).on_before_update(on_before_update)
        _hasCreated=True
    ret = db_context.collection("LMSLS_MaterialManagement")

    return ret