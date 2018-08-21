from config import database, helpers, db_context
_hasCreated=False
def Demo_VanBanDieuHanh():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "Demo_VanBanDieuHanh",
            sorting	 		= helpers.create_field("text"),
            description	 	= helpers.create_field("text"),
            custom_name	 	= helpers.create_field("text"),
            style_class	 	= helpers.create_field("text"),
            url	 			= helpers.create_field("text"),
            image	 		= helpers.create_field("text"),
            default_name	= helpers.create_field("text"),
            height	 		= helpers.create_field("text"),
            parent_id	 	= helpers.create_field("text"),
            active	 		= helpers.create_field("text"),
            function_id	 	= helpers.create_field("text"),
            type	 	 	= helpers.create_field("text"),
            width	 		= helpers.create_field("text"),
            icon	 		= helpers.create_field("text"),
            app	 			= helpers.create_field("text"),
            level_code	 	= helpers.create_field("text"),
            color	 		= helpers.create_field("text"),
            code	 		= helpers.create_field("numberic"),
            pl_dm           = helpers.create_field("numberic")
        )
        _hasCreated=True
    ret = db_context.collection("Demo_VanBanDieuHanh")

    return ret