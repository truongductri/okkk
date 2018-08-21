(function (scope) {
    scope.$currentEmployeeCode = (scope.$root.$commons) ? scope.$root.$commons.$current_employee_code : null
    console.log(scope.$currentEmployeeCode);

    scope.$active = (scope.$root.$commons) ? scope.$root.$commons.$active : null

    scope.$tableEmpWorking = {
        tableField: [
            { "data": "appoint_name", "title": "${get_res('appoint','Loại')}" },
            { "data": "decision_no", "title": "${get_res('decision_no','Số QĐ')}" },
            { "data": "effect_date", "title": "${get_res('effect_date','Ngày QĐ')}", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "begin_date", "title": "${get_res('begin_date','Từ ngày')}", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "end_date", "title": "${get_res('end_date','Đến ngày')}", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "department_name", "title": "${get_res('department_code','Bộ phận')}" },
            { "data": "job_pos_name", "title": "${get_res('job_pos_code','Chức vụ')}" },
            { "data": "job_w_name", "title": "${get_res('job_w_code','Chức danh')}" },
            { "data": "region_name", "title": "${get_res('region_code','Vùng làm việc')}" }
        ],
        selectedItems: [],
        currentItem: null,
        tableSource: _loadDataServerSide,
        tableSearchText: '',
        SearchText: '',
        onSelectTableRow: function ($row) {
            onEdit();
        },
        refreshDataRow: function () { /*Do nothing*/ },
        $$tableConfig: {},
        latestRecordEmpWorking: [],
        empInfor: []


    }

    scope.$tableEmpExperience = {
        tableField: [
            { "data": "begin_date", "title": "${get_res('begin_date','Từ ngày')}", "className": "text-center", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "end_date", "title": "${get_res('end_date','Đến ngày')}", "className": "text-center", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "working_location", "title": "${get_res('working_location','Đơn vị làm việc')}", "className": "text-left" },
            { "data": "job_pos_name", "title": "${get_res('job_pos_code','Chức vụ')}", "className": "text-left" },
            { "data": "job_w_name", "title": "${get_res('job_w_code','Chức danh')}", "className": "text-left" }
        ],
        selectedItems: [],
        currentItem: null,
        tableSource: _loadDataEmpExperience,
        tableSearchText: '',
        SearchText: '',
        onSelectTableRow: function ($row) {
            onEditExperience();
        },
        refreshDataRow: function () { /*Do nothing*/ },
        $$tableConfig: {}
    }

    //Mode 1: tạo mới, Mode 2: chỉnh sửa, Mode 3: sao chép
    scope.mode = 0;

    scope.event = {
        empWorking: {
            onAdd: onAdd,
            onEdit: onEdit,
            onDelete: onDelete,
            onRefresh: onRefresh
        },
        empExperience: {
            onAdd: onAddExperience,
            onEdit: onEditExperience,
            onDelete: onDeleteExperience,
            onRefresh: onRefreshExperience
        }
    }
    scope.triggerResize = triggerResize;
    scope._tableData = _tableData;
    scope._tableDataEmpExperience = _tableDataEmpExperience;

    function triggerResize() {
        $(window).trigger('resize');
    }

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$tableEmpWorking.$$tableConfig = {
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
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSEM_EmpWorking/get_empworking_by_emp_code')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "employee_code": scope.$currentEmployeeCode
                })
                .done()
                .then(function (res) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    console.log("data", data.data);
                    //lấy giá trị mặc định của nhân viên nếu chưa có quyết định bn-dc
                    services.api("${get_api_key('app_main.api.HCSEM_EmpWorking/get_default_value_curent_employee')}")
                        .data({
                            "employee_code": scope.$currentEmployeeCode
                        })
                        .done()
                        .then(function (r) {
                            scope.$tableEmpWorking.empInfor = r;
                            if (res.items.length > 0) {
                                //lấy giá trị có ngày hiệu lực mới nhất
                                var max = res.items[0];
                                for (var i = 0; i < res.items.length; i++) {
                                    if (res.items[i].effect_date > max.effect_date) {
                                        max = res.items[i];
                                    }
                                }
                                scope.$tableEmpWorking.latestRecordEmpWorking = max;
                            }
                            else {
                                res.effect_date = null;
                                scope.$tableEmpWorking.latestRecordEmpWorking = r;
                                scope.$applyAsync();
                            }

                        })


                    callback(data);
                    scope.$apply();
                })
    }
    function _loadDataEmpExperience(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$tableEmpExperience.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        //setTimeout(function () {
        if (fnReloadData) {
            if (searchText) {
                _tableDataEmpExperience(iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                });
            } else {
                _tableDataEmpExperience(iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
        //}, 1000);
    };
    function _tableDataEmpExperience(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSEM_EmpExperience/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "employee_code": scope.$currentEmployeeCode
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

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.$tableEmpWorking.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('add_empworking','Chi tiết Bổ nhiệm điều chuyển')}", 'profile/form/addEmpWorking', function () {

                //$(window).trigger('resize');
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới        
        //if (scope.$tableEmpWorking.latestRecordEmpWorking.length > 0) {

        //}
        //else {

        //}
        openDialog("${get_res('add_empworking','Chi tiết Bổ nhiệm điều chuyển')}", 'profile/form/addEmpWorking', function () {
        });
    }
    function onDelete() {
        if (!scope.$tableEmpWorking.selectedItems || scope.$tableEmpWorking.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSEM_EmpWorking/delete')}")
                    .data(scope.$tableEmpWorking.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$tableEmpWorking.$$tableConfig.iPage,
                                scope.$tableEmpWorking.$$tableConfig.iPageLength,
                                scope.$tableEmpWorking.$$tableConfig.orderBy,
                                scope.$tableEmpWorking.$$tableConfig.SearchText,
                                scope.$tableEmpWorking.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        } else {
                            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Delete','Không có dòng được xóa')}", function () { });
                        }
                    })
            });
        }
    }

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEditExperience() {
        if (scope.$tableEmpExperience.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('add_empexperience','Chi tiết kinh nghiệm trước đây')}", 'profile/form/addEmpExperience', function () {

                //$(window).trigger('resize');
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAddExperience() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('add_empexperience','Chi tiết kinh nghiệm trước đây')}", 'profile/form/addEmpExperience', function () {
        });
    }
    function onDeleteExperience() {
        if (!scope.$tableEmpExperience.selectedItems || scope.$tableEmpExperience.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSEM_EmpExperience/delete')}")
                    .data(scope.$tableEmpExperience.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableDataEmpExperience(scope.$tableEmpExperience.$$tableConfig.iPage,
                                scope.$tableEmpExperience.$$tableConfig.iPageLength,
                                scope.$tableEmpExperience.$$tableConfig.orderBy,
                                scope.$tableEmpExperience.$$tableConfig.SearchText,
                                scope.$tableEmpExperience.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        } else {
                            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Delete','Không có dòng được xóa')}", function () { });
                        }
                    })
            });
        }
    }

    function onSearch(val) {
        scope.$tableEmpWorking.tableSearchText = val;
    }

    function onSearchExperience(val) {
        scope.$tableEmpExperience = val;
    }

    function onRefresh() {
        _tableData(scope.$tableEmpWorking.$$tableConfig.iPage,
            scope.$tableEmpWorking.$$tableConfig.iPageLength,
            scope.$tableEmpWorking.$$tableConfig.orderBy,
            scope.$tableEmpWorking.$$tableConfig.SearchText,
            scope.$tableEmpWorking.$$tableConfig.fnReloadData);
    }

    function onRefreshExperience() {
        _tableDataEmpExperience(scope.$tableEmpExperience.$$tableConfig.iPage,
            scope.$tableEmpExperience.$$tableConfig.iPageLength,
            scope.$tableEmpExperience.$$tableConfig.orderBy,
            scope.$tableEmpExperience.$$tableConfig.SearchText,
            scope.$tableEmpExperience.$$tableConfig.fnReloadData);
    }

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
    scope.indexTabChange = function (val) {
        setTimeout(function () {
            $(window).trigger('resize');
        }, 200);
    }
});