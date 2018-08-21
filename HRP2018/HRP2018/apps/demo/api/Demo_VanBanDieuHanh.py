import models

def get_list(args):
    where = args["data"]
    itemPLs = models.Demo_VanBanDieuHanh().aggregate().match("pl_dm == {0}", 1)
    itemPLs.lookup(models.Demo_VanBanDieuHanh_Details(), "code", "pl_code", "pl")
    itemPLs.project(
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
            data_details            = "pl.ky_hieu"
            ).sort({"sorting":1})
    itemCMs = models.Demo_VanBanDieuHanh().aggregate().match("pl_dm == {0}", 2)
    itemCMs.lookup(models.Demo_VanBanDieuHanh_Details(), "code", "cm_code", "cm")
    itemCMs.project(
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
            data_details            = "cm.ky_hieu"
            ).sort({"sorting":1})
    
    return dict(
        itemPLs = itemPLs.get_list(),
        itemCMs = itemCMs.get_list()
        )