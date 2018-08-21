(function (scope) {
    scope.mode = 0;
    scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }
    scope.SearchText = '';
    scope._departments = _departments;
    scope._reloadData = _reloadData;
    /* Table */
    scope.$$table = {
        tableFields: [
            { "data": "department_code", "title": "${get_res('department_code_table_title','Mã')}", "className": "text-left" },
            { "data": "department_name", "title": "${get_res('department_name_table_title','Tên')}", "className": "text-left" },
            { "data": "department_alias", "title": "${get_res('department_alias_table_title','Bí danh')}", "className": "text-left" },
            { "data": "department_tel", "title": "${get_res('department_tel_table_title','Số điện thoại')}", "className": "text-left" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) {
            scope.button.edit();
        },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };

    /* Tree */
    scope.$$tree = {
        treeCurrentNode : {},
        treeSelectedNodes :[],
        treeSelectedRootNodes :[],
        treeCheckAll : false,
        treeSearchText : '',
        treeDisable : false,
        treeMultiSelect : false,
        treeMode : 3
    }
    var _treeDepartmentsDataSource = null;
    scope.treeDepartmentsDataSource = null;

    scope.button = {
        add: function () {
            scope.mode = 1;
            redirectPage();
        },
        edit: function () {
            scope.mode = 2;
            redirectPage();
        },
        delete: function () {
            if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            } else {
                $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                    services.api("${get_api_key('app_main.api.HCSSYS_Departments/delete')}")
                        .data(scope.$$table.selectedItems)
                        .done()
                        .then(function (res) {
                            if (res.deleted > 0) {
                                _reloadData();
                                _departments();
                                $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                                scope.$$table.currentItem = null;
                                scope.$$table.selectedItems = [];
                            } else if (res.error !== null || res.error !== "") {
                                $msg.message("${get_global_res('cannot_delete','Không thể xóa')}", "${get_global_res('job_working_is_using','CDCV đang được sử dụng')}", function () { });
                            }
                        })
                });
            }
        },
        import: function () {
            alert('import');
        },
        export: function () {
            alert('export');
        },
        print: function () {
            alert('print');
        },
        refresh: function () {
            _reloadData();
        }
    }

    //Navigation: quay trở về UI list
    scope.backPage = backPage;

    function redirectPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.$partialpage = scope.mapName[0].url;
            $(window).trigger('resize');
        }, 500);
    }

    function _reloadData() {
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy,
            config.searchText, config.fnReloadData)
    }

    function onSelectedRow($row) {
        scope.mode = 2;
        redirectPage();
    }

    function backPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 0;
            scope.$partialpage = scope.mapName[0].url;
            scope.selectedFunction = scope.mapName[0].function_id;
            $(window).trigger('resize');
        }, 500);
    }

    function addEmployee() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 1;
            scope.$$table.currentItem = {};
            scope.$partialpage = scope.mapName[0].url;
            $(window).trigger('resize');
        }, 500);
    }

    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$table.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
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
    };

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        if (scope.$$tree.treeCurrentNode.hasOwnProperty('department_code')) {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.HCSSYS_Departments/get_list_department_by_parent_code')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "where": {
                            'department_code': scope.$$tree.treeCurrentNode.department_code
                        },
                        "sort": sort
                    })
                    .done()
                    .then(function (res) {
                        var data = {
                            recordsTotal: res.total_items,
                            recordsFiltered: res.total_items,
                            data: res.items
                        };
                        callback(data);
                        scope.$apply();
                    })
        }
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog\
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

    function _departments() {
        services.api("${get_api_key('app_main.api.HCSSYS_Departments/get_list')}")
            .data()
            .done()
            .then(function (res) {
                _treeDepartmentsDataSource = res;
                scope.treeDepartmentsDataSource = _treeDepartmentsDataSource;
                scope.$applyAsync();
            })
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }   

    (function _init_() {
        _departments();
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.$partialpage = scope.mapName[0].url;
        scope.currentFunction = scope.mapName[0];
        scope.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
        scope.$applyAsync();
    })();

    scope.$watch("selectedFunction", function (function_id) {
        var $his = scope.$root.$history.data();
        if (scope.$$table.currentItem) {
            var func = _.filter(scope.mapName, function (f) {
                return f["function_id"] == function_id;
            });
            if (func.length > 0) {
                scope.$partialpage = func[0].url;
                scope.currentFunction = func[0];
            }
        }
    });

    scope.$watch('$$tree.treeCurrentNode', function (val) {
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength,
            scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText,
            scope.$$table.$$tableConfig.fnReloadData)
    })
});