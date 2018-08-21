(function (scope) {
    scope.$data = {
        $dataChiTieu: []
    }
    scope.$dataItem = null;
    scope.$partialpage = 'partialpage/BCCT_LaoDongViecLam';
    scope.redirectPage = (child) => {
        if (child) {
            scope.$partialpage = child.url;
            scope.$dataItem = child;
        }
        $(".lms-dashboard-header-box-hover").removeClass("lms-dashboard-header-box-hover");
        $(".lms-dashboard-header-span-cl").removeClass("lms-dashboard-header-span-cl");
        $(event.target).parent().parent().parent().addClass("lms-dashboard-header-box-hover");
        var span = $(event.target).parent().parent().parent().find("span");
        for (var i = 0; i < span.length; i++) {
            $(span[i]).addClass("lms-dashboard-header-span-cl")
        }
    }
    scope.$dataPL = [];
    scope.$dataCM = [];
    scope.cm_code = null;
    scope.pl_code = null;
    //
    services.api("${get_api_key('app_main.api.Demo_VanBanDieuHanh/get_list')}")
        .data({
            
        })
        .done()
        .then(function (res) {
            if (res) {
                scope.$dataPL = res.itemPLs;
                scope.$dataCM = res.itemCMs;
                scope.getDetails();
                scope.$applyAsync();
            }
        })
    scope.getDetails = function (cm_code, pl_code) {
        if (cm_code) {
            scope.cm_code = cm_code;
        }
        if (pl_code) {
            scope.pl_code = pl_code;
        }
        services.api("${get_api_key('app_main.api.Demo_VanBanDieuHanh_Details/get_list')}")
            .data({
                cm_code: scope.cm_code,
                pl_code: scope.pl_code
            })
            .done()
            .then(function (res) {
                if (res) {
                    scope.$data.$dataChiTieu = res;
                    scope.$applyAsync();
                }
            })
    }
});