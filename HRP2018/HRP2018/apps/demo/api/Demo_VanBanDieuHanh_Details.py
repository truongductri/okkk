import models

def get_list(args):
    where = args["data"]
    items = models.Demo_VanBanDieuHanh_Details().aggregate()
    if(where != None):
        if(where.has_key('pl_code') and where["pl_code"] != None): 
            items.match("(pl_code == @pl_code)", 
                        pl_code=where["pl_code"])
        if(where.has_key('cm_code') and where["cm_code"] != None):
            items.match("(cm_code == @cm_code)", 
                        cm_code=where["cm_code"])
    items.left_join(models.Demo_VanBanDieuHanh(), "pl_code", "code", "pl")   
    items.match("pl.pl_dm == {0}", 1)
    items.project(
        ky_hieu = 1,
        ngay=1,
        ten_van_ban=1,
        pl_code=1,
        cm_code=1,
        pl_name="pl.default_name"
        )
    items.left_join(models.Demo_VanBanDieuHanh(), "cm_code", "code", "cm")  
    items.match("cm.pl_dm == {0}", 2)   
    items.project(
        ky_hieu = 1,
        ngay=1,
        ten_van_ban=1,
        pl_code=1,
        cm_code=1,
        cm_name="cm.default_name",
        pl_name=1
        )
    return items.get_list()
