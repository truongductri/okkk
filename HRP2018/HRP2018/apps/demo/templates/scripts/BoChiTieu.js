(function (scope) {
    scope.$dataBoBaoCao = [];
    scope.$dataItem = null;
    scope.$partialpage = 'partialpage/PhongChongTNXH';
    (function dataBoBaoCao() {
        services.api("${get_api_key('app_main.api.Demo_Bobaocao/get_list')}")
            .data({
                //parameter at here
                "function_id": scope.$root.currentFunction.function_id
            })
            .done()
            .then(function (res) {
                if (res.length > 0) {
                    scope.$dataItem = res[0];
                    scope.$dataBoBaoCao = res;
                    scope.$applyAsync();
                }
            })
    })();

    scope.redirectPage = (child, event) => {
        if (child) {
            scope.$partialpage = child.url;
            scope.$dataItem = child;
        }
        $(".lms-dashboard-header-box-hover").removeClass("lms-dashboard-header-box-hover");
        $(".lms-dashboard-header-span-cl").removeClass("lms-dashboard-header-span-cl");
        $(event.target).closest('.lms-dashboard-header-box').addClass("lms-dashboard-header-box-hover");
        var span = $(event.target).closest('.lms-dashboard-header-box').find("span");
        for (var i = 0; i < span.length; i++) {
            $(span[i]).addClass("lms-dashboard-header-span-cl")
        }
    }

    //scope.$watch("selectedFunction", function (function_id) {
    //    if (function_id) {
    //        var $his = scope.$root.$history.data();
    //        window.location.href = "#page=" + $his.page + "&f=" + function_id;
    //    }
    //});

    //scope.$root.$history.onChange(scope, function (data) {
    //    debugger
    //    if (scope.mapName.length > 0) {
    //        if (data.f) {
    //            var func = _.filter(scope.mapName, function (f) {
    //                return f["function_id"] == data.f;
    //            });
    //            if (func.length > 0) {
    //                scope.$partialpage = func[0].url;
    //                scope.currentFunction = func[0];
    //                scope.selectedFunction = func[0].function_id;
    //            } else {
    //                window.location.href = "#";
    //            }
    //        } else {
    //            scope.$partialpage = scope.mapName[0].url;
    //        }
    //        scope.$apply();
    //    } else {
    //        window.location.href = "#";
    //    }
    //});
});