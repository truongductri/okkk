(function (scope) {
    scope.$parent.$partialpage = "partialpage/examination_management_question_bank";

    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.$root.extendToolbar = true;

    scope.currentFunction = '';
    scope.mapName = [];
    scope.$root.currentItem = [];
    scope.isDisplayGird = true;
    scope.isList = true;
    scope.isGrid = false;
    scope.objSearch = {};
    scope.onDisplayListData = function () {
        scope.isList = true;
        scope.isGrid = false;
        scope.$root.onDisplayListData();
    }
    scope.onDisplayGridData = function () {
        scope.isList = false;
        scope.isGrid = true;
        scope.$root.onDisplayGridData();
    }
    scope.onSearchText = function () {

        scope.searchText = scope.objSearch.$$$modelSearch

    }
    scope.advancedSearch = {
        main_region_code: null,
        main_nation_code: null
    }

    scope.createTemplate = function () {
            scope.mode = 1; // set mode chỉnh sửa
             openDialog("${get_res('Create_question_category','Create Question Category')}", 'form/addQuestionCategory', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
    }

    scope.editTemplate = function () {
        debugger
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('edit_question_category','Edit Question Category')}", 'form/addQuestionCategory', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });

        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.delTemplate = function () {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el && el._id
        })
        //
        if (scope.selectedItems.length > 0) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_ExQuestionCategory/delete')}")
                    .data(arrayId)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope.currentItem = [];
                            scope.$root.refresh();
                        }
                    })
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }





    /**
    * Hàm mở dialog
    * @param {string} title Tittle của dialog
    * @param {string} path Đường dẫn file template
    * @param {function} callback Xử lí sau khi gọi dialog\
    * @param {string} id Id của form dialog, default = 'myModal'
    */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
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
    /////////////////////////////////////////////////////////////
       scope.$root.isDisplay = true;
    scope.__tableSource = [];
    scope.mode = 0;
    scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.$parent.isDisplayGird = true;
    scope.$root.onDisplayListData = function () {
        scope.selectedItems = []
    }
 
 
    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }

    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "category_id", "title": "${get_res('category_id_table_header','ID')}" },
        { "data": "category_name", "title": "${get_res('category_name_table_header','Question Category Name')}" },
        { "data": "number_ques", "title": "${get_res('number_ques_header','Number of Questions')}" },
        { "data": "created_on", "title": "${get_res('created_at_table_header','Created at')}", "format": "date:" + 'dd/MM/yyyy h:mm:ss a' },  
    ];
    scope.$$tableConfig = {};
    scope.$root.$$tableConfig = {};
    scope.$root._tableData = _tableData;
    scope.$root._departments = _departments;
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.mode = 2;
        scope.editQuestionCategory();
    };
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = refresh;
    scope.$root.refresh = refresh;

    scope.treeCurrentNode = {};
    scope.treeSelectedNodes = [];
    scope.treeSelectedRootNodes = [];
    scope.treeCheckAll = false;
    scope.treeSearchText = '';
    scope.treeDisable = false;
    scope.treeMultiSelect = false;
    scope.treeMode = 3; // Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
    var _treeDepartmentsDataSource = null;
    scope.treeDepartmentsDataSource = null;

    //selectbox datasource
    scope.cbbGender = [];
    scope.cbbEmployeeActive = [];
    scope.cbbCulture = [];
    scope.cbbRetrain = [];
    scope.cbbTrainLevel = [];
    scope.cbbLabourType = [];
    scope.cbbLevelManagement = [];
    scope.cbbWorkingType = [];

    //navigation button
    scope.firstRow = firstRow;
    scope.previousRow = previousRow;
    scope.nextRow = nextRow;
    scope.lastRow = lastRow;

    //function button
    scope.addEmployee = addEmployee;
    scope.refresh = refresh;

    //Navigation: quay trở về UI list
    scope.backPage = backPage;

    function backPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 0;
            $(window).trigger('resize');
        }, 500);
    }

    function addEmployee() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 1;
            scope.currentItem = {};
            scope.$partialpage = scope.mapName[0].url;
            $(window).trigger('resize');
        }, 500);
    }

    function refresh() {
        var tableConfig = scope.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
        _departments();
    }

    function firstRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.__tableSource[0];
        }
    }

    function previousRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === 0 ? scope.__tableSource.length - 1 : idx_item - 1;
            scope.currentItem = scope.__tableSource[index];
        }
    }

    function nextRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === (scope.__tableSource.length - 1) ? 0 : idx_item + 1;
            scope.currentItem = scope.__tableSource[index];
        }
    }

    function lastRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.__tableSource[scope.__tableSource.length - 1];
        }
    }

    function tableFields() {
        return [
            { "data": "category_id", "title": "${get_res('category_id_table_header','ID')}" },
            { "data": "category_name", "title": "${get_res('category_name_table_header','Question Category Name')}" },
            { "data": "number_ques", "title": "${get_res('number_ques_header','Number of Questions')}" },
            { "data": "created_on", "title": "${get_res('created_at_table_header','Created at')}" },
        ];
    }


    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
	};

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
			searchText: searchText

        };
        scope.$root.$$tableConfig = {
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

	scope._tableData = _tableData;
    function _tableData(iPage, iPageLength, orderBy, searchText, callback, objSearchAdvance) {
        
        //if (scope.treeCurrentNode.hasOwnProperty('folder_id')) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_ExQuestionCategory/get_list_category_question')}")
                .data({
                    //parameter at here
                    "train_level_code": scope.entity ? scope.entity.train_level_code : " ",
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
            .then(function (res) {
                
                _.map(res.items, function (val) { val.number_ques = 10;  return val})
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                   // scope.$$table.currentItem = null;
                    scope.$apply();

                })

    }


    function _departments() {
        services.api("${get_api_key('app_main.api.LMSLS_ExQuestionCategory/get_list')}")
            .data()
            .done()
            .then(function (res) {
                _treeDepartmentsDataSource = res;
                scope.treeDepartmentsDataSource = _treeDepartmentsDataSource;
                scope.treeCurrentNode = res[0];
                scope.$applyAsync();
            })
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }



});