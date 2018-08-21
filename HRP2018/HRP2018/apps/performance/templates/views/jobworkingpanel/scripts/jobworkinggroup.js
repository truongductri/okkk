(function (scope) {

    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields": [
            { "data": "gjw_code", "title": "${get_res('function_list','Mã nhóm')}", width: "100px", className: "text-center" },
            { "data": "note", "title": "${get_res('note','Ghi chú')}", width: "100px", className: "text-center" },
            { "data": "ordinal", "title": "${get_res('ordinal','Thứ tự')}", width: "100px", className: "text-center" },
            { "data": "lock", "title": "${get_res('lock','Ngưng sử dụng')}", format: "checkbox", width: "100px", className: "text-center" }
        ],
        "selectTreeNode": function (node) {

        },
        "treeCurrentNode": {},
        "treeSelectedNodes": [],
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 3,
        "treeDisabled": false
    };

    scope.$parent.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.$parent.onRefresh = onRefresh;

    scope._jobWorkingGroup = _jobWorkingGroup;
    function _jobWorkingGroup() {
        services.api("${get_api_key('app_main.api.HCSLS_JobWorkingGroup/get_tree')}")
            .data()
            .done()
            .then(function (res) {
                scope.$$tableTree.dataTableTree = res;
                scope.$applyAsync();
            })
    }

    function onAdd() {
        scope.mode = 1;
        openDialog("${get_res('Jon_Working_Detail','Chi tiết nhóm chức danh công việc')}", 'jobworkingpanel/form/addJobWorkingGroup', function () { });
    };
    function onEdit() {
        scope.mode = 2;
        openDialog("${get_res('Jon_Working_Detail','Chi tiết nhóm chức danh công việc')}", 'jobworkingpanel/form/addJobWorkingGroup', function () { });
    };
    function onDelete() {
        if (!scope.$$tableTree.treeSelectedNodes || scope.$$tableTree.treeSelectedNodes.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_JobWorkingGroup/delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _jobWorkingGroup()
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        } else if (res.error !== null || res.error !== "") {
                            $msg.message("${get_global_res('cannot_delete','Không thể xóa')}", "${get_global_res('job_working_group_is_using','Mã nhóm CDCV đang được sử dụng')}", function () { });
                        } else {
                            $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                        }
                    })
            });
        }
    };
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

    _jobWorkingGroup();
});