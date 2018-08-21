(function (scope) {
    debugger
    var _default = {
        department_code: null,
        department_name: null,
        department_name2: null,
        department_alias: null,
        parent_code: null,
        level: null,
        level_code: null,
        department_tel: null,
        department_fax: null,
        department_email: null,
        department_address: null,
        nation_code: null,
        province_code: null,
        district_code: null,
        is_company: null,
        is_fund: null,
        is_fund_bonus: null,
        decision_no: null,
        decision_date: null,
        effect_date: null,
        license_no: null,
        tax_code: null,
        lock_date: null,
        logo_image: null,
        manager_code: null,
        secretary_code: null,
        ordinal: null,
        lock: null,
        note: null,
        region_code: null,
        domain_code: null,
        signed_by: null
    }
    scope.$parent.$parent.$parent.$parent.onSave = onSave;
    scope.__mode = scope.$parent.$parent.$parent.$parent.mode;
    scope.entity = {};
    scope.$$department_code = scope.__mode == 2 ? scope.$parent.$parent.$parent.$parent.$$table.currentItem.department_code : null;


    function onSave() {
        $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_res('Notify_Save','Bạn có muốn lưu không?')}", function () {
            var url = scope.__mode === 1 ? "${get_api_key('app_main.api.HCSSYS_Departments/insert')}" 
            : "${get_api_key('app_main.api.HCSSYS_Departments/update')}" ;
            callApi(url, scope.entity, function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    scope.$parent.$parent._departments();
                    scope.$parent.$parent._reloadData();
                } else if (res.error.hasOwnProperty('code') && res.error.code == "duplicate") {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${ get_res('department_code', 'Mã phòng ban') }" + "${get_global_res('exists','đã tồn tại')}", function () { });
                } else if (res.error.hasOwnProperty('code') && res.error.code == "missing") {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('missing_fields','Nhập liệu thiếu')}" + "\n" + 
                        "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                } else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            })
        });
    }

    /**
     * Hàm gọi api
     * @param {string} url
     * @param {object} parameter
     * @param {void} callback
     */
    function callApi(url, parameter, callback) {
        console.log(parameter)
        services.api(url)
            .data(parameter)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function _getDepartmentByDeptCode(deptCod, callback) {
        callApi("${get_api_key('app_main.api.HCSSYS_Departments/get_department_by_dept_code')}",
            {
                "department_code" : deptCod
            },callback)
    }

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [
                {
                    "key": "${encryptor.get_key('cbb_nation')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('nation_code')
                        ? scope.entity.nation_code
                        : null,
                    "alias": "$$$cbb_nation"
                },
                {
                    "key": "${encryptor.get_key('cbb_province_of_nation')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('province_code')
                        ? scope.entity.province_code
                        : null,
                    "alias": "$$$province_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_district_of_province')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('district_code')
                        ? scope.entity.district_code
                        : null,
                    "alias": "$$$district_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_region')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('region_code')
                        ? scope.entity.region_code
                        : null,
                    "alias": "$$$region_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_departments')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('parent_code')
                        ? scope.entity.parent_code
                        : null,
                    "alias": "$$$cbb_departments"
                },
                {
                    "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('manager_code')
                        ? scope.entity.manager_code
                        : null,
                    "alias": "$$$manager_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('secretary_code')
                        ? scope.entity.secretary_code
                        : null,
                    "alias": "$$$secretary_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('signed_by')
                        ? scope.entity.signed_by
                        : null,
                    "alias": "$$$signed_by"
                }
            ]

        );
    };

    (function _init_() {
        if (scope.__mode == 2) {
            _getDepartmentByDeptCode(scope.$$department_code, function (res) {
                scope.entity = res;
                _getDataInitCombobox();
            })
        } else {
            scope.entity = _default;
            _getDataInitCombobox();
        }
    })();
});