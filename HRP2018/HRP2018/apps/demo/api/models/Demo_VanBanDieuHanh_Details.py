from config import database, helpers, db_context
_hasCreated=False
def Demo_VanBanDieuHanh_Details():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "Demo_VanBanDieuHanh_Details",
            [["ky_hieu"]],
            ky_hieu=helpers.create_field("text"),
            ngay=helpers.create_field("datetime"),
            ten_van_ban=helpers.create_field("text"),
            pl_code=helpers.create_field("numberic"),
            cm_code=helpers.create_field("numberic"),
        )
        _hasCreated=True
    ret = db_context.collection("Demo_VanBanDieuHanh_Details")

    return ret