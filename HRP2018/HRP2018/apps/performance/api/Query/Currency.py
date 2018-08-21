from .. import models
def display_list_currency():
    ret=models.HCSLS_Currency().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        currency_code="currency_code",
        currency_name="currency_name",
        currency_name2="currency_name2",
        temp_rate="temp_rate",
        multiply="multiply",
        cons_code="cons_code",
        dec_place="dec_place",
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