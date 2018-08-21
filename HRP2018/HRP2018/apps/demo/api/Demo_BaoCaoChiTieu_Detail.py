import models

def get_list(args):
    where = args["data"]
    if(where != None):
        items = models.Demo_BaoCaoChiTieu_Detail().aggregate().project(
            parent_code     = 1,
            code            = 1,
            name            = 1,
            url             = 1,
            data_year       = 1,
            ).match("parent_code == {0}", where["parent_code"]).sort({"sorting":1})
    
        return items.get_list()
    return []