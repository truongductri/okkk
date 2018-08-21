(function (scope) {
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

        
        
        var fs = _.filter(scope.$root.$function_list, function (d) {
            return d["parent_id"] == scope.$root.currentFunction["function_id"];
        });
        $.each(fs, function (idx, val) {
            val["child_items"] = _.filter(scope.$root.$function_list, function (d) {
                return d["parent_id"] == val["function_id"];
            });
        });
        scope.$functions = fs;
        /*
        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });*/
        

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
        this.redirectPage = (child) => {
            
            if (child.url.trim()) {
                scope.$root.currentModule = _.filter(scope.$functions, function (d) {
                    return d["function_id"] == child.parent_id;
                })[0].custom_name.replace("/", " ");
                scope.$root.currentFunction = child.custom_name;
            }
            location.href = '#page=' + child.function_id;
        }
    };

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        //scope.$functions = scope.handleData.$functions;
        scope.currentFunction = scope.$root.currentFunction
        
    }
});