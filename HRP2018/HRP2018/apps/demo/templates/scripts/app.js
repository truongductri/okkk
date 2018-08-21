window.set_component_template_url('${get_static("app/directives/")}')
window.set_api_combobox("${get_api_key('app_main.api.common/get_dropdown_list')}")
angular
    .module("admin", ["c-ui", 'ZebraApp.components', 'ZebraApp.widgets', 'hcs-template', 'ngclipboard'])
    .controller("admin", controller);

controller.$inject = ["$dialog", "$scope"];
dialog_root_url('${get_app_url("pages/")}')
function controller($dialog, $scope, systemService) {
    $scope.$root.systemConfig = null;/*HCSSYS_SystemConfig*/
    $scope.$root.language = "${get_language()}";
    $scope.$root.APP_URL = "${get_app_url('')}";
    $scope.VIEW_ID = "${register_view()}";
    $dialog($scope)
    ws_set_url("${get_app_url('api')}")
    ws_set_export_token_url("${get_api_key('app_main.excel.manager/generate_token')}");
    ws_onBeforeCall(function () {
        mask = $("<div class='mask'></div>")
        mask.appendTo("body");
        return mask
    });
    ws_onAfterCall(function (mask) {
        mask.remove();
    })
    history_navigator($scope.$root);

    $scope.view_path = "${get_view_path()}";
    $scope.services = services = ws($scope);
    $scope.$root.$getComboboxData = extension().getComboboxData;
    $scope.$root.$getInitComboboxData = extension().getInitComboboxData;
    $scope.$root.system = systemService;
    $scope.$root.collapseSubMenu = function collapseSubMenu(e) {
        e.stopPropagation();
        $('#hcs-top-bar-menu ul li ul').slideUp();
        if (($(e.currentTarget.parentElement.children[1]).css('display') != 'block')) {
            $(e.currentTarget.parentElement.children[1]).slideDown(500);
        }
    };

    $("#btnShowMessage").unbind("click");
    $("#btnShowMessage").bind("click", function () {
        $(this).siblings(".hcs-message-list").toggleClass("message-hidden");
        event.stopPropagation();
    });
    $("#btnShowMenu").unbind("click");
    $("#btnShowMenu").bind("click", function () {
        $(this).siblings(".hcs-menu-list").toggleClass("menu-hidden");
        event.stopPropagation();
    });
    $(window).bind("click", function (e) {
        var isMenu = $(e.target).closest(".hcs-menu-list").length > 0;
        var isMessage = $(e.target).closest(".hcs-message-list").length > 0;
        if (!isMenu && !isMessage) {
            $("#btnShowMenu").siblings(".hcs-menu-list").addClass("menu-hidden");
            $("#btnShowMessage").siblings(".hcs-message-list").addClass("message-hidden");
        }
    });

    $scope.$root.doLogout = function () {
        window.location = "${get_app_url('logout')}";
    }
    $scope.redirectPage = (child) => {
        if (url) {
            if (child.url.indexOf("http://") != -1 || child.url.indexOf("https://") != -1) {
                var win = window.open(child.url, '_blank');
                win.focus();
            } else {
                if (child.parent_id) {
                    if (child.url.trim()) {
                        scope.$root.currentModule = _.filter(scope.$root.$functions, function (d) {
                            return d["function_id"] == child.parent_id;
                        })[0].custom_name.replace("/", " ");
                        scope.$root.currentFunction = child.custom_name;
                    }
                }
                location.href = '#page=' + child.function_id;
            }
        }
    }

    ////Đồng hồ
    //$scope.$root.timer = {
    //    clock: Clock(),
    //    meridiem: getMeridiem(),
    //    date: Calendar()
    //};
    //setInterval(function () {
    //    $scope.$root.timer.clock = Clock();
    //    if ($scope.$root.timer.clock === "00:00") {
    //        $scope.$root.timer.date = Calendar();
    //        $scope.$root.timer.meridiem = getMeridiem();
    //    }
    //    $scope.$root.$applyAsync();
    //}, 10000);

    /**
     * Initialize Data
     */
    function activate() {
        $scope.$root.currentModule = '';
        $scope.$root.currentFunction = {};
        $scope.$root.logo = 'http://www.molisa.gov.vn/_layouts/images/NCS.UI.TiengViet.Molisa/logo.png';

        //Get function list
        services.api("${get_api_key('app_main.api.functionlist/get_list')}")
            .data({
                //parameter at here
            })
            .done()
            .then(function (res) {
                var functions = JSON.parse(JSON.stringify(res));
                /**
                 * Customize string tittle group when display data
                 */
                $.each(res, function (idx, val) {
                    if (val.parent_id == null) {
                        var arr = val["custom_name"].split("/");
                        var display_name = arr[0];
                        var display_name_bold = arr[1];
                        val["display_name"] = display_name;
                        val['display_name_bold'] = display_name_bold;
                    }
                });

                /**
                 * Function list
                 */
                $scope.$root.$function_list = functions;

                var fs = _.filter(res, function (d) {
                    return d["parent_id"] == null;
                });
                $.each(fs, function (idx, val) {
                    val["child_items"] = _.filter(res, function (d) {
                        return d["parent_id"] == val["function_id"];
                    });
                });
                $scope.$root.$functions = fs;
                $scope.$applyAsync();
                $scope.$root.getPage = function () {
                    return (angular.isObject($scope.$root.currentFunction))
                        ? "${get_app_url('')}/pages/" + $scope.$root.currentFunction.url
                        : "${get_app_url('')}/pages/home";
                }
                $scope.$root.$history.change(function (data) {
                    if (data.page) {
                        var currentFunction = _.filter(functions, function (d) {
                            return d["function_id"] == data.page;
                        });
                        if (currentFunction.length > 0) {
                            //Set current function
                            $scope.$root.currentFunction = currentFunction[0];
                            $scope.$root.currentModule = _.filter(functions, function (d) {
                                return d["function_id"] == currentFunction[0].parent_id ? currentFunction[0].parent_id : data.page;
                            })[0];
                        }
                    } else {
                        $scope.$root.currentFunction = $scope.$root.currentModule = null;
                        $scope.$root.currentModule = { default_name: 'Trung tâm điều hành lao động thương binh & xã hội' };
                    }
                    $scope.$root.$applyAsync();
                })
            })

        //Get HCSSYS_SystemConfig
        services.api("${get_api_key('app_main.api.common/get_config')}")
            .data({
                //parameter at here
            })
            .done()
            .then(function (res) {
                //Set HCSSYS_SystemConfig
                $scope.$root.systemConfig = res;
            })
    }
    /**
     * Init
     */
    activate();
}

function extension() {
    var fac = {};

    fac.guid = function () {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    };

    fac.getComboboxData = getComboboxData;
    fac.getInitComboboxData = getInitComboboxData;

    /**
     * Hàm get combobox data
     * @param {object} scope
     * @param {void} cbSetData
     * @param {number} pgIdx
     * @param {string} txtSearch
     */
    function getComboboxData(scope, cbSetData, pgIdx, txtSearch) {
        services.api("${get_api_key('app_main.api.common/get_combobox_data')}")
            .data({
                //parameter at here
                "key": scope.params.key,
                "value": scope.params.value,
                "pageIndex": pgIdx - 1,
                "search": txtSearch,
            })
            .done()
            .then(function (res) {
                scope.captionField = res.caption_field;
                scope.keyField = res.value_field;
                scope.title = res.display_name;
                scope.templateFields = res.display_fields;
                var data = {
                    recordsTotal: res.data.total_items,
                    data: res.data.items
                };
                cbSetData(data);
            });
    }

    /**
     * Hàm get data init combobox
     * @param {object} scope
     * @param {any} key Trường hợp get nhiều truyền tham số là array object
     * example:[{key:xxx, code:xxx}, {key:yyy, code:yyy}]
     * Trường hợp get đơn lẻ truyền tham số là object
     * example:{key:xxx, code:xxx}
     */
    function getInitComboboxData(scope, key) {
        services.api("${get_api_key('app_main.api.common/get_init_data_combobox')}")
            .data({
                name: key
            })
            .done()
            .then(function (res) {
                if (angular.isArray(res)) {
                    $.each(res, function (i, v) {
                        scope[v.alias] = v;
                    });
                } else {
                    scope[res.alias] = res;
                }
                scope.$apply();
            })
    }

    return fac;
};

function Clock() {
    return moment().locale("${get_language()}").format("HH:mm");
}

function toStartCase(str) {
    return str
        .toLowerCase()
        .split(' ')
        .map(function (word) {
            return word[0].toUpperCase() + word.substr(1);
        })
        .join(' ');
}

function Calendar() {
    return toStartCase(moment().locale("${get_language()}").format('dddd, DD MMMM, YYYY'));
}

//function getMeridiem() {
//    return moment().locale("${get_language()}").format("a");
//}