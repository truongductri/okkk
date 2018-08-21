(function (scope) {
    scope.$$table = {
        tableFields: [
            { "data": "ordinal", "title": "${get_res('ordinal_table_header','Thứ tự')}", "className": "text-center" },
            { "data": "task_name", "title": "${get_res('task_name_table_header','Nhiệm vụ')}", "className": "text-left" },
            { "data": "weight", "title": "${get_res('weight_table_header','Trọng số')}", "className": "text-center" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };
    scope.$parent.$parent.$parent.$parent.detail.onAdd = onAdd;
    scope.$parent.$parent.$parent.$parent.detail.onEdit = onEdit;
    scope.$parent.$parent.$parent.$parent.detail.onDelete = onDelete;
    scope.$parent.$parent.$parent.$parent.detail.onRefresh = onRefresh;
    scope.$job_w_code = scope.$parent.$parent.$parent.$parent.detail.$job_w_code;
    scope._tableData = _tableData;

    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Detail_Function_And_Mission','Chi tiết chức năng và nhiệm vụ')}", 'jobworkingpanel/jobworkingdetail/form/addFunctionAndMission', function () { });
    };
    function onEdit() {
        if (scope.$$table.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_Function_And_Mission','Chi tiết chức năng và nhiệm vụ')}", 'jobworkingpanel/jobworkingdetail/form/addFunctionAndMission', function () {});
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_JobWorking/delete_task')}")
                    .data({
                        "job_w_code": scope.$job_w_code,
                        "rec_id": _.pluck(scope.$$table.selectedItems, 'rec_id')
                    })
                    .done()
                    .then(function (res) {
                        if (res.updatedExisting == true) {
                            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$$table.currentItem = null;
                            scope.$$table.selectedItems = [];
                        }
                        if (res.error != null || res.updatedExisting == false) {
                            $msg.alert("${get_global_res('Handle_Failed','Thao tác thất bại')}", $type_alert.DANGER);
                        }
                    })
            });
        }
    };
    function onRefresh() {

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
            services.api("${get_api_key('app_main.api.HCSLS_JobWorking/get_list_permission_and_mission')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "job_w_code": scope.$job_w_code
                })
                .done()
                .then(function (res) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.$$table.currentItem = null;
                    scope.$apply();
                })
    }
});