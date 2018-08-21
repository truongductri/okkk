from .. import models
def display_list_unit():
    ret=models.HCSLS_Unit().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        unit_code="unit_code",
        unit_name="unit_name",
        unit_name2="unit_name2",
		note="note",
        lock="lock",
        ordinal="ordinal",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret