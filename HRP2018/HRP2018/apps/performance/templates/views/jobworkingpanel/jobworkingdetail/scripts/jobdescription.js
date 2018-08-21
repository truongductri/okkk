(function (scope) {
    scope.$parent.$parent.$parent.$parent.detail.onSave = onSave;
    scope.__mode = scope.$parent.$parent.$parent.$parent.detail.$mode;
    scope.gjw_code = scope.$parent.$parent.$parent.$parent.detail.$gjw_code;
    //scope.gjw_name = scope.$parent.$parent.$parent.$parent.$$currentJobWorkingGroupName;

    scope.set_job_w_change = function () {
        var frm = lv.FormSearch(scope, "$$$job_working");
        frm.JobWorking(scope.entity, "job_w_change", "${get_res('job_w_change','CDCV có thể thuyên chuyển')}", true);
        frm.openDialog;
    }

    scope.set_job_w_next = function () {
        var frm = lv.FormSearch(scope, "$$$job_working_next");
        frm.JobWorking(scope.entity, "job_w_next", "${get_res('job_w_next','CDCV thuyên chuyển')}", false);
        frm.openDialog;
    }

    scope.set_report_to_job_w = function () {
        var frm = lv.FormSearch(scope, "$$$job_working_report_to_job_w");
        frm.JobWorking(scope.entity, "report_to_job_w", "${get_res('report_to_job_w','Báo cáo cho')}", false);
        frm.openDialog;
    }

    function onSave() {
        save();
    };

    function save() {
        if (scope.entity != null) {
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result) {
                //Nhập sai: break khỏi hàm
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    scope.entity = res.data;
                    if (scope.__mode == 1) {
                        scope.__mode = 2;
                        scope.$parent.$parent.$parent.$parent.detail.$mode = 2;
                        scope.$parent.$parent.$parent.$parent.detail.$gjw_code = scope.entity.gjw_code;
                        scope.$parent.$parent.$parent.$parent.detail.$job_w_code = scope.entity.job_w_code;

                    }
                    scope.$parent.$parent.$parent.currentJobWorkingName = res.data.job_w_name;
                    scope.$parent.$parent.$parent.detail.$gjw_name = res.data.gjw_name;
                    scope.$parent.$parent.$parent.detail.$job_w_name = res.data.job_w_name;
                    scope.$apply();
                } else {
                    $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", function () { });
                }
            })
        }
    }

    function editData(callback) {
        var url = getUrl();  
        services.api(url)
            .data(scope.entity)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function beforeCallToServer() {
        //scope.entity.gjw_code = scope.gjw_code;
    }

    function getUrl() {
        return scope.__mode == 1 ? "${get_api_key('app_main.api.HCSLS_JobWorking/insert')}" /*Mode 1: Tạo mới*/
            : "${get_api_key('app_main.api.HCSLS_JobWorking/update')}" /*Mode 2: Cập nhật*/
    }

    /**
     * Function check input
     */
    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.job_w_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_code_is_not_null','Mã chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.job_w_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_name_is_not_null','Tên chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.job_w_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_name_is_not_null','Tên chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        return rs;
    }

    function _getJobDescription(callback) {
        services.api("${get_api_key('app_main.api.HCSLS_JobWorking/get_job_description')}")
            .data({
                "job_w_code": scope.$parent.$parent.$parent.$parent.detail.$job_w_code
            })
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [{
                "key": "${encryptor.get_key('cbb_position')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_pos_code')
                    ? scope.entity.job_pos_code
                    : null,
                "alias": "$$$cbb_position"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_multi_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_w_change')
                    ? scope.entity.job_w_change
                    : null,
                "alias": "$$$job_working"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_single_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_w_next')
                    ? scope.entity.job_w_next
                    : null,
                "alias": "$$$job_working_next"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_single_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('report_to_job_w')
                    ? scope.entity.report_to_job_w
                    : null,
                "alias": "$$$job_working_report_to_job_w"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_group')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('gjw_code')
                    ? scope.entity.gjw_code
                    : null,
                "alias": "$$$cbb_job_working_group"
            },
            {
                "key": "${encryptor.get_key('cbb_departments_multi_select')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('dept_contact')
                    ? scope.entity.dept_contact
                    : null,
                "alias": "$$$cbb_departments_multi_select"
            },
            {
                "key": "${encryptor.get_key('cbb_departments_multi_select')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('dept_apply')
                    ? scope.entity.dept_apply
                    : null,
                "alias": "$$$dept_apply"
            }
            ]
        );
    }

    (function __init__() {
        if (scope.__mode == 2) {
            _getJobDescription(function (res) {
                scope.entity = res;
                _getDataInitCombobox();
                scope.$applyAsync();
            })
        } else {
            scope.entity = {};
            scope.entity.gjw_code = scope.gjw_code;
            _getDataInitCombobox();
        }
    })();
});