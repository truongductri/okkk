import models

def get_list(args):
    where = args["data"]
    if(where != None):
        items = models.Demo_Bobaocao().aggregate().project(
            sorting              = 1,
            description          = 1,
            custom_name          = 1,
            style_class          = 1,
            url                  = 1,
            image                = 1,
            default_name         = 1,
            height               = 1,
            parent_id            = 1,
            active               = 1,
            function_id          = 1,
            type                 = 1,
            width                = 1,
            icon                 = 1,
            app                  = 1,
            level_code           = 1,
            color                = 1,
            ).match("function_id == {0}", where["function_id"]).sort({"sorting":1})
    
        return items.get_list()
    return []