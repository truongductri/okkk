﻿(function (scope) {
    var $url = "https://app.powerbi.com/view?r=eyJrIjoiMzhkZWUzMjctYWNhMS00Y2MwLThlMDgtY2ZmYmI3OTc4OGYxIiwidCI6IjFhYjlmNGUxLTFkMTQtNGM4Zi1hNGEwLWFjZDMwNjIzMzVkMCIsImMiOjEwfQ%3D%3D";
    scope.$parent.$urlPowerBi = $url;
    scope.$parent.$applyAsync();
    //Cấu hình tên field và caption hiển thị trên UI
    scope.$watch("$parent.$dataItem", function (val) {
        if (val) {
            scope.$$dataItem = scope.$parent.$dataItem;
            scope.$data = {};
            services.api("${get_api_key('app_main.api.Demo_BaoCaoChiTieu_Detail/get_list')}")
                .data({
                    //parameter at here
                    "parent_code": scope.$parent.$dataItem.code
                })
                .done()
                .then(function (res) {
                    //scope.$partialpage = res[0].url;
                    scope.$data.$dataChiTieu = res;
                    // Set height
                    $(".dataTables_scrollBody").css({
                        height: $(".hcs-demo-gird-tree").height() - $(".dataTables_scrollHead").height()
                    })
                    setTimeout(function () {
                        $("iframe").attr("src", $url);
                    }, 300)
                    scope.$applyAsync();
                });
        }
    });
    scope.onCompilerIframe = function (item, event) {
        if (item.url) {
            $("iframe").attr("src", item.url);
        } else {
            $("iframe").removeAttr("src");
        }
        $("tr").removeClass("zb-table-row-focus");
        $("td").removeClass("focus");
        $(event.target).parent().addClass("zb-table-row-focus");
    }
    scope.isNumber = function (number) {
        return angular.isNumber(number) && !isNaN(number);
    }
});