(function (scope) {
    const $$func_id_detail = "HCSSYS0550";
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.detail = {
        mapName: [],
        $partialpage: "",
        $gjw_code: "",
        $job_w_code: "",
        $gjw_name: "",
        $job_w_name: "",
        $mode: 0,
        currentFunction: {},
        selectedFunction: "",
        selectFunc: function (event, f) {
            scope.detail.selectedFunction = f;
        },
        search:""
    }
    scope.advancedSearch = {
        data_lock: "0"
    }
    scope.display = {
        master: true,
        detail: false
    };
    scope.masterPage = masterPage;
    scope.$applyAsync();

    /*                                                         */
    /* ==================== Property Scope - END ==============*/
    /*                                                         */

    /*                                                         */
    /* ==================== Initialize - START=================*/
    /*                                                         */
    activate();
    init();
    /*                                                         */
    /* ==================== Initialize - END ==================*/
    /*                                                         */

    /*                                                                                          */
    /* ===============================  Implementation - START  ================================*/
    /*                                                                                          */

    /* Object handle data */
    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.detail = {
            mapName: []
        }

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        var detailFunction = _.findWhere(scope.$root.$function_list, { function_id: $$func_id_detail });

        this.detail.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(detailFunction.function_id)
                && f.level_code.length == detailFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "name": "sysLock"
            })
            .done()
            .then(function (res) {
                delete res.language;
                delete res.list_name;
                scope.cbbSysLock = res.values;
                scope.$applyAsync();
            })
    }

    function masterPage() {
        scope.detail.mapName = scope.handleData.detail.mapName;
        scope.detail.currentFunction = scope.detail.mapName[0];
        scope.detail.$partialpage = scope.detail.mapName[0].url;
        scope.detail.$mode = 0;
        scope.detail.$gjw_code = "";
        scope.detail.$job_w_code = "";
        scope.detail.$gjw_name = "";
        scope.detail.$job_w_name = "";
        scope.detail.selectedFunction = "";

        scope.display = {
            master: true,
            detail: false
        };
        scope.$applyAsync();
    }

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.detail.mapName = scope.handleData.detail.mapName;
        scope.currentFunction = scope.mapName[0];
        scope.detail.currentFunction = scope.detail.mapName[0];
        _comboboxData();
    }

    /*                                                                                          */
    /* ===============================  Implementation - END  ==================================*/
    /*                                                                                          */

    scope.$watch("selectedFunction", function (function_id) {
        if (function_id) {
            var $his = scope.$root.$history.data();
            window.location.href = "#page=" + $his.page + "&f=" + function_id;
        }
    });

    scope.$watch("detail.selectedFunction", function (function_id) {
        if (function_id) {
            var fn = _.findWhere(scope.detail.mapName, { "function_id": function_id });
            scope.detail.$partialpage = fn.url;
            scope.detail.currentFunction = fn;
        }
    });

    scope.$root.$history.onChange(scope, function (data) {
        //Job working panel
        if (scope.mapName.length > 0) {
            if (data.f) {
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    scope.$partialpage = func[0].url;
                    scope.currentFunction = func[0];
                    scope.selectedFunction = func[0].function_id;
                } else {
                    if (!data.hasOwnProperty('gjw_code'))
                        window.location.href = "#";
                }
            } else {
                scope.$partialpage = scope.mapName[0].url;
            }
            scope.$apply();
        } else {
            window.location.href = "#";
        }
    });
});