(function (scope) {
    /**
     * Table
     */
    scope.$$table = {
        tableFields: [
            { "data": "kpi_code", "title": "${get_res('kpi_code_table_header','Mã')}" },
            { "data": "kpi_name", "title": "${get_res('kpi_name_table_header','Yếu tố')}" },
            { "data": "weight", "title": "${get_res('weight_table_header','Trọng số')}" },
            { "data": "is_apply_all", "title": "${get_res('is_apply_all_table_header','Toàn cty')}", "format": "checkbox" },
            { "data": "ordinal", "title": "${get_res('ordinal_table_header','Thứ tự')}" },
            { "data": "lock", "title": "${get_res('lock_table_header','Ngưng sử dụng')}", "format": "checkbox" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }


    };
    scope.__tableSource = [];
    scope._tableData = _tableData;
    scope.mode = 0;
    scope.searchText = "";
    scope.onSelectTableRow = pressEnter;


    /* Tree */
    scope.$$tree = {
        treeCurrentNode: {},
        treeSelectedNodes: [],
        treeSelectedRootNodes: [],
        treeCheckAll: false,
        treeSearchText: '',
        treeDisable: false,
        treeMultiSelect: false,
        treeMode: 3,// Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
        treeDataSource: null
    };

    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;


    function onSearch(val) {
        scope.$$table.tableSearchText = val;
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }




    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Add_New_KPI','Thêm mới Chỉ tiêu năng suất')}", 'productivityDictionaryPanel/form/addKPI', function () { });
    };
    function onEdit() {
        if (scope.$$table.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('modified_KPI','Chi tiết Chỉ tiêu năng suất')}", 'productivityDictionaryPanel/form/addKPI', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMLS_KPI/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$$table.currentItem = null;
                            scope.$$table.selectedItems = [];
                        }
                    })
            });
        }
    };

    function pressEnter($row) {
        scope.onEdit();
    }
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TMLS_KPI'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }
    function onAttach() {

    };
    function onRefresh() {
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    };

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {

        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

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
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.TMLS_KPI/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "kpi_group_code": scope.$$tree.treeCurrentNode.hasOwnProperty("kpi_group_code") === true ? scope.$$tree.treeCurrentNode.kpi_group_code : null
                })
                .done()
                .then(function (res) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    function _loadTreeDataSource() {
        services.api("${get_api_key('app_main.api.TMLS_KPIGroup/get_tree')}")
            .data({
                lock: (scope.$root.$commons) ? scope.$root.$commons.$kpi_lock : 0
            })
            .done()
            .then(function (res) {
                scope.$$tree.treeDataSource = res;
                scope.$applyAsync();
            })
    }
    _loadTreeDataSource();

    scope.$watch("$$tree.treeCurrentNode", function () {
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    });
});