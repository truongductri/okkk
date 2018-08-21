(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI    
     
    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields": [
            { "data": "kpi_group_code", "title": "${get_res('kpi_group_code','Mã nhóm')}", width: "100px", className: "text-center" },
            { "data": "weight", "title": "${get_res('weight','Trọng số')}", width: "100px", className: "text-center" },
            { "data": "is_team", "title": "${get_res('is_team','Tập thể')}", format: "checkbox", width: "100px", className: "text-center" },
            { "data": "ordinal", "title": "${get_res('ordinal','Thứ tự')}", width: "100px", className: "text-center" },
            { "data": "lock", "title": "${get_res('lock','Ngưng sử dụng')}", format: "checkbox", width: "100px", className: "text-center" }
        ],
        "selectTreeNode": function (node) {

        },
        "treeCurrentNode": {},
        "treeSelectedNodes": [],
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 3,
        "treeDisabled": false,
        "lock": 0
    };

    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    //scope.$parent.$parent.$parent.onAttach = onAttach;
    //scope.$parent.$parent.$parent.onRefresh = onRefresh;

    scope.$root.$commons = {
        $kpi_lock: scope.$$tableTree.lock
    };
    scope._kpiGroup = _kpiGroup;
    function _kpiGroup() {        
        services.api("${get_api_key('app_main.api.TMLS_KPIGroup/get_tree')}")
            .data({
                lock: scope.$$tableTree.lock
            })
            .done()
            .then(function (res) {               
                scope.$$tableTree.dataTableTree = res;
                scope.$applyAsync();                
            })
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Add_New_KPI_Group','Thêm mới Nhóm chỉ tiêu năng suất')}", 'productivityDictionaryPanel/form/addKPIGroup', function () { });
    }
    function onEdit() {
        scope.mode = 2;
        openDialog("${get_res('detail_kpi_group','Chi tiết Nhóm chỉ tiêu năng suất')}", 'productivityDictionaryPanel/form/addKPIGroup', function () { });
    };
    //function onDelete() {
    //    debugger
    //    if (!scope.selectedItems || scope.selectedItems.length === 0) {
    //        $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
    //    } else {
    //        $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
    //            services.api("${get_api_key('app_main.api.HCSSYS_DataDomain/delete')}")
    //                .data(scope.selectedItems)
    //                .done()
    //                .then(function (res) {
    //                    if (res.deleted > 0) {
    //                        _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
    //                        $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
    //                        scope.currentItem = null;
    //                        scope.selectedItems = [];
    //                    }
    //                })
    //        });
    //    }
    //};
    function onDelete() {
        if (!scope.$$tableTree.treeSelectedNodes[0]) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
        else {            
            scope.mode = 3;
            //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMLS_KPIGroup/delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope._reloadpage();
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                        }
                        else if (res['error'] == "not allow") {
                            $msg.alert("${get_global_res('Handle_Success','node selected use other process')}", $type_alert.INFO);
                        }
                        else
                            $msg.alert("${get_global_res('Handle_Success','request paramerter is not exist')}", $type_alert.INFO);
                    });
            });
        }
    }
    function onImport() {

    };
    function onExport() {

    };
    function onAttach() {

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

    scope.$watch('$$tableTree.treeSelectedNodes', function (val) {
        console.log(val);
    });

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "name": "sysLock"
            })
            .done()
            .then(function (res) {
                scope.cbbSysLock = res.values;       
                scope.$applyAsync();
            })
    }
   
   
    _comboboxData();
    _kpiGroup();

    scope.$watch('$$tableTree.lock', function (val) {        
        console.log(val);
        scope.$$tableTree.lock = val;
        scope._kpiGroup();
        scope.$applyAsync();

    });
    //scope.onChangeCbbSysLock = function (key) {
    //    debugger
    //    console.log(key)
    //    scope.$$tableTree.lock = key;
    //    scope._kpiGroup();
    //}
    //("===============INIT==================")
    //_tableData();
    //("===============END TABLE==================")
});