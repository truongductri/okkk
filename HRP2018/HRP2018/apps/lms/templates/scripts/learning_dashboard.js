(function (scope) {
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.$root.currentItem = [];
    scope.isDisplayGird = false;
    scope.isList = true;
    scope.isGrid = false;
    scope.onDisplayListData = function () {
        scope.isList = true;
        scope.isGrid = false;
    }
    scope.onDisplayGridData = function () {
        scope.isList = false;
        scope.isGrid = true;
    }

    scope.advancedSearch = {
        main_region_code: null,
        main_nation_code: null
    }

    scope.addLearningMaterial = function () {
        scope.$root.add();
    }

    scope.editLearningMaterial = function () {
        scope.$root.edit();
    }

    scope.delLearningMaterial = function () {
        scope.$root.delete();
    }

    scope.viewDetailsLearningMaterial = function () {
        scope.$root.viewDetailsLearningMaterial();
    }

    scope.viewHistoryLearningMaterial = function () {
        scope.$root.viewHistoryLearningMaterial();
    }

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

        //this.mapName = [
        //    { 'function_id': 'function1', 'name': 'Loại nhân viên', 'url': 'category/employeetype' },
        //    { 'function_id': 'function2', 'name': 'Quốc gia', 'url': 'category/nation' },
        //    { 'function_id': 'function3', 'name': 'Vùng làm việc', 'url': 'category/usergroup' },
        //    { 'function_id': 'function4', 'name': 'Phân cấp hành chính', 'url': 'category/function' },
        //    { 'function_id': 'function5', 'name': 'Dân tộc', 'url': 'category/domain' },
        //    { 'function_id': 'function6', 'name': 'Tôn giáo', 'url': 'category/user' },
        //    { 'function_id': 'function7', 'name': 'Trình độ học vấn', 'url': 'category/usergroup' },
        //    { 'function_id': 'function8', 'name': 'Tình trạng hôn nhân', 'url': 'category/function' },
        //    { 'function_id': 'function9', 'name': 'Nghề nghiệp chuyên môn', 'url': 'category/domain' },
        //    { 'function_id': 'function10', 'name': 'Nhóm CDCV/CDCV', 'url': 'category/user' }
        //];

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
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

    scope.$root.$history.onChange(scope, function (data) {
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