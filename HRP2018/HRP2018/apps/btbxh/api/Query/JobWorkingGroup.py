from .. import models

def get_job_working_group():
    ret=models.HCSLS_JobWorkingGroup().aggregate()
    ret.project(
        gjw_code = 1,
        gjw_name = 1,
        gjw_name2 = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        ordinal = 1,
        note = 1,
        lock = 1
        )
    ret.sort(dict(
        ordinal = 1,
        gjw_name = 1
    ))
    return ret

