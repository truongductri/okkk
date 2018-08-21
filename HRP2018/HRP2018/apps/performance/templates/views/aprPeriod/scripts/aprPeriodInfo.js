(function (scope) {
    scope.__mode = scope.$parent.mode;
    scope.entity = {
        "_id":  scope.$parent.currentItem._id
    };
    
    scope.cbbApprovalPeriod = [];
    scope.$parent.$parent.$parent.onSave = onSave;
    scope.$$tableConfig = {};

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "name": "LApprovalPeriod"
            })
            .done()
            .then(function (res) {
                debugger
                delete res.language;
                delete res.list_name;
                scope.cbbApprovalPeriod = res.values;
                console.log(res);
                scope.$applyAsync();
            })
    }
    function Re_Map_Period(periodStr) {
        debugger
        var numPeriod = 0;
        for (var i = 0; i < 12; i++) {
            if (periodStr === "Tháng " + (i + 1).toString()) {
                numPeriod = i + 1
                return numPeriod;
            }

        }
        for (var j = 13; j <= 16; j++) {
            if (periodStr === "Quý " + (j - 12).toString()) {
                numPeriod = j - 12
                return numPeriod;
            }
        }
        if (periodStr === "6 tháng đầu năm")
            numPeriod = 17;
        else if (periodStr === "6 tháng cuối năm")
            numPeriod = 18;
        else
            numPeriod = 19;
        return numPeriod;
    }

    function save() {
        debugger
        if (scope.entity != null) {
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result == false) {
                //Nhập sai: break khỏi hàm
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(function (res) {
                debugger
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    scope.$applyAsync();
                    reloadData();
                } else {
                    $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", function () { });
                }
            })
        }
    }
    

    function onSave() {
        save();
    };

    function editData(callback) {
        debugger
        var url = getUrl();
        var currentItem = JSON.parse(JSON.stringify(scope.entity));
        services.api(url)
            .data(currentItem)
            .done()
            .then(function (res) {
                callback(res);
                scope.$applyAsync();

            })
    }

    function beforeCallToServer() {

    }

    function reloadData() {
        debugger
        var tableConfig = scope.$parent.$$tableConfig;
        scope.$parent._tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function getUrl() {
        return scope.__mode == 1 || scope.__mode == 3 ? "${get_api_key('app_main.api.TMPER_AprPeriod/insert')}" /*Mode 1: Tạo mới*/
            : "${get_api_key('app_main.api.TMPER_AprPeriod/update')}" /*Mode 2: Cập nhật*/
    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.apr_period);
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('apr_period_is_not_null','Kỳ đánh giá không được để trống')}" + '\n' : "";
        if (rs.result === false) {
            return rs;
        }
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('apr_year_is_not_null','Năm không được để trống')}" + '\n' : "";
        if (rs.result === false) {
            return rs;
        }
        rs.result = check_year(scope.entity.apr_year);
        rs.errorMsg = rs.result === false ? "${get_res('apr_year_is_four_character','Năm phải bao gồm 4 ký tự số')}" + '\n' : "";
        if (rs.result === false) {
            return rs;
        }
        else if (new Date(scope.entity.give_target_from) > new Date(scope.entity.give_target_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('give_target_from_is_larger_give_target_to','Giao chỉ tiêu đến phải >= ngày giao chỉ tiêu từ')}";
        }
        else if (new Date(scope.entity.review_mid_from) > new Date(scope.entity.review_mid_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('review_mid_from_is_larger_review_mid_to','Xem xét giữa kỳ đến phải >= ngày xem xét giữa kỳ từ')}";
        }
        else if (new Date(scope.entity.approval_mid_from) > new Date(scope.entity.approval_mid_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('approval_mid_to_is_larger_approval_mid_from','Xét duyệt giữa kỳ đến phải >= ngày xét duyệt giữa kỳ từ')}";
        }
        else if (new Date(scope.entity.approval_final_from) > new Date(scope.entity.approval_final_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('approval_final_to_is_larger_approval_final_from','Xét duyệt cuối kỳ đến phải >= ngày xét duyệt cuối kỳ từ')}";
        }
        else if (new Date(scope.entity.emp_final_from) > new Date(scope.entity.emp_final_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('emp_final_to_is_larger_emp_final_from','NV xét duyệt cuối kỳ đến phải >= ngày NV xét duyệt cuối kỳ từ')}";
        }
        else if (new Date(scope.entity.review_mid_from) < new Date(scope.entity.give_target_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('give_target_to_is_not_null','Xét duyệt giữa kỳ từ phải >= ngày giao chỉ tiêu đến')}";
        }
        else if (new Date(scope.entity.emp_final_from) < new Date(scope.entity.approval_mid_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('emp_final_from_is_not_null','NV đánh giá cuối kỳ từ phải >= ngày xét duyệt giữa kỳ đến')}";
        }
        else if (new Date(scope.entity.approval_final_from) < new Date(scope.entity.emp_final_to)){
            rs.result = false;
            rs.errorMsg = "${get_res('approval_final_from_is_not_null','Xét duyệt cuối kỳ từ phải >= ngày NV xét duyệt cuối kỳ đến')}";
        }
       
        return rs;
    }

    function check_year(numValid) {
        var a = numValid;
        if (a.toString().length == 4)
            return true;
        return false;
    }


    (function __init__() {
        debugger
        if (scope.__mode == 2) {
            _comboboxData();
            scope.entity.apr_period = Re_Map_Period(scope.$parent.entity.apr_period);
            scope.entity.apr_year = scope.$parent.entity.apr_year;
            scope.$applyAsync();
        }
        else if (scope.__mode == 1 || scope.__mode == 3) {
            _comboboxData();
            scope.$applyAsync();
        }
    })();
});
