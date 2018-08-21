(function (scope) {
    /**
     * Table
     */
    scope.$$table = {
        tableFields: [
            { "data": "job_w_code", "title": "${get_res('job_w_code_table_header','Mã chức danh')}", "className": "text-left" },
            { "data": "job_w_name", "title": "${get_res('job_w_name_table_header','Tên chức danh')}", "className": "text-left" },
            { "data": "report_to_job_w", "title": "${get_res('report_to_job_w_table_header','Báo cáo cho')}", "className": "text-left" },
            { "data": "ordinal", "title": "${get_res('ordinal_table_header','Thứ tự')}", "className": "text-center" }
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

    scope.$parent.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.$parent.onRefresh = onRefresh;

    function onSearch(val) {
        scope.$$table.tableSearchText = val;
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function onAdd() {
        if (scope.$$tree.treeCurrentNode && Object.keys(scope.$$tree.treeCurrentNode).length > 0) {
            redirectPage(1);
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_node_Selected','Không có nút được chọn')}", function () { });
        }
    };
    function onEdit() {
        if (scope.$$tree.treeCurrentNode && Object.keys(scope.$$tree.treeCurrentNode).length > 0) {
            if (scope.$$table.currentItem && Object.keys(scope.$$table.currentItem).length > 0) {
                redirectPage(2);
            } else {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_node_Selected','Không có nút được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_JobWorking/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$$table.currentItem = null;
                            scope.$$table.selectedItems = [];
                        } else if (res.error !== null || res.error !== "") {
                            $msg.message("${get_global_res('cannot_delete','Không thể xóa')}", "${get_global_res('job_working_is_using','CDCV đang được sử dụng')}", function () { });
                        }
                    })
            });
        }
    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TMLS_FactorAppraisal'
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
        _loadTreeDataSource();
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
            services.api("${get_api_key('app_main.api.HCSLS_JobWorking/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "lock": scope.$parent.$parent.$parent.$parent.advancedSearch.data_lock,
                    "sort": sort,
                    "gjw_code": scope.$$tree.treeCurrentNode.hasOwnProperty("gjw_code") === true ? scope.$$tree.treeCurrentNode.gjw_code : null
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
        services.api("${get_api_key('app_main.api.HCSLS_JobWorkingGroup/get_tree')}")
            .data()
            .done()
            .then(function (res) {
                scope.$$tree.treeDataSource = res;
                scope.$applyAsync();
            })
    }
    _loadTreeDataSource();

    /**
     * Hàm điều hướng qua trang chi tiết JobWorking
     * @param {number} mode 1:Thêm, 2:Sửa
     */
    function redirectPage(mode) {
        scope.$parent.$parent.$parent.$parent.display = {
            master: false,
            detail: true
        };
        scope.$parent.$parent.$parent.$parent.detail.$partialpage = scope.$parent.$parent.$parent.$parent.detail.mapName[0].url;
        if (mode === 2) {
            scope.$parent.$parent.$parent.$parent.detail.$job_w_code = scope.$$table.currentItem.job_w_code;
            scope.$parent.$parent.$parent.$parent.detail.$job_w_name = scope.$$table.currentItem.job_w_name;            
        }
        scope.$parent.$parent.$parent.$parent.detail.$mode = mode;
        scope.$parent.$parent.$parent.$parent.detail.$gjw_name = scope.$$tree.treeCurrentNode.gjw_name;
        scope.$parent.$parent.$parent.$parent.detail.$gjw_code = scope.$$tree.treeCurrentNode.gjw_code;
        scope.$applyAsync();
    }

    scope.$parent.$parent.$parent.$parent.$watch("advancedSearch.data_lock", function (val) {
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    });

    scope.$watch("$$tree.treeCurrentNode", function () {
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    });
});