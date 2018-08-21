from .. import models
from .. import common
def display_list_rank():
    ret=models.TMLS_Rank().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        rank_code="rank_code",
        rank_name="rank_name",
        rank_name2="rank_name2",
        rank_content="rank_content",
        total_from="total_from",
        total_to="total_to",
        is_change_object="is_change_object",
        ordinal="ordinal",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_details(rank_code):
    col=models.TMLS_Rank().aggregate().match("rank_code == {0}", rank_code)
    col.unwind("details", False)
    col.join(models.auth_user_info(), "created_by", "username", "uc")
    col.left_join(models.auth_user_info(), "modified_by", "username", "um")
    col.project(
        rec_id = "details.rec_id",
        rank_code = "details.rank_code",
        change_object = "details.change_object",
        object_level = "details.object_level",
        object_code = "details.object_code",
        object_name = "details.object_name",
        priority_no = "details.priority_no",
        total_from = "details.total_from",
        total_to = "details.total_to",
        note = "details.note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(details.modified_on!='',details.modified_on),'')",
        modified_by="switch(case(details.modified_by!='',um.login_account),'')"
        )
    return col

def remove_details(args):
    collection  =  common.get_collection('TMLS_Rank')
    ret = collection.update(
                        {
                            "rank_code": args['data']['rank_code']
                        },
                        {
                            '$pull':{"details" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
    return ret

def insert_details(args, details):
    collection  =  common.get_collection('TMLS_Rank')
    ret = collection.update(
                          { "rank_code": args['data']['rank_code'] },
                          {
                            '$push': {
                              "details": details
                            }
                          }
                        )
    return ret

def update_details(args, details):
    collection  =  common.get_collection('TMLS_Rank')
    ret = collection.update(
        {
            "rank_code": args['data']['rank_code'],
            "details":{
                "$elemMatch":{
                    "rec_id":args['data']['details']["rec_id"]
                    }
                }
        },
        {
            "$set": {
                'details.$.rank_code': details['rank_code'],
                'details.$.change_object': details['change_object'],
                'details.$.object_level': details['object_level'],
                'details.$.object_code': details['object_code'],
                'details.$.object_name': details['object_name'],
                'details.$.priority_no': details['priority_no'],
                'details.$.total_from': details['total_from'],
                'details.$.total_to': details['total_to'],
                'details.$.note': details['note'],
                'details.$.modified_by': details['modified_by'],
                'details.$.modified_on': details['modified_on']
                }
        })
    return ret