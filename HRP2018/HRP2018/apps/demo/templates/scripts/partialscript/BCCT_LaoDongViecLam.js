(function (scope) {
    var $url = "https://app.powerbi.com/view?r=eyJrIjoiOTMzZjM5YTgtMmE1ZS00YmRmLWI2YzUtMGJmMjJiYTk1ZmZhIiwidCI6IjFhYjlmNGUxLTFkMTQtNGM4Zi1hNGEwLWFjZDMwNjIzMzVkMCIsImMiOjEwfQ%3D%3D";
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

    scope.tableSource = _loadDataServerSide;
    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        //setTimeout(function () {
        if (fnReloadData) {
            if (searchText) {
                _tableData(iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                });
            } else {
                _tableData(iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
        //}, 1000);
    };
    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        if (scope.treeCurrentNode.hasOwnProperty('department_code')) {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.Demo_BaoCaoChiTieu_Detail/get_list')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "sort": sort,
                        "parent_code": scope.$parent.$dataItem.code
                    })
                    .done()
                    .then(function (res) {
                        var data = {
                            recordsTotal: res.total_items,
                            recordsFiltered: res.total_items,
                            data: res.items
                        };
                        scope.__tableSource = JSON.parse(JSON.stringify(res.items));
                        callback(data);
                        scope.currentItem = null;
                        scope.$apply();
                    })
        }
    }
});