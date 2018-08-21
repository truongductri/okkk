from config import database, helpers, db_context
_hasCreated=False
def Demo_BaoCaoChiTieu_Detail():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "Demo_BaoCaoChiTieu_Detail",
            [["code"]],
            code=helpers.create_field("numberic", True),
            parent_code=helpers.create_field("numberic"),
            name=helpers.create_field("text"),
            url=helpers.create_field("text"),
            data_year=helpers.create_field("object"),
        )
        _hasCreated=True
    ret = db_context.collection("Demo_BaoCaoChiTieu_Detail")

    return ret