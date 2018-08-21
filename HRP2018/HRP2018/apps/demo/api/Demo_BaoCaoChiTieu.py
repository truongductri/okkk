import models

def get_list(args):
    where = args["data"]
    if(where != None):
        items = models.Demo_BaoCaoChiTieu().aggregate()
        items.lookup(models.Demo_BaoCaoChiTieu_Detail(), "code", "parent_code", "uc")
        items.match("function_id == {0}", where["function_id"])
        items.project(
            sorting              = "sorting",
            description          = "description",
            custom_name          = "custom_name",
            style_class          = "style_class",
            url                  = "url",
            image                = "image",
            default_name         = "default_name",
            height               = "height",
            parent_id            = "parent_id",
            active               = "active",
            function_id          = "function_id",
            type                 = "type",
            width                = "width",
            icon                 = "icon",
            app                  = "app",
            level_code           = "level_code",
            color                = "color",
            code                 = "code",
            data_code            = "uc.code"
            ).sort({"sorting":1})
    
        return items.get_list()
    return []