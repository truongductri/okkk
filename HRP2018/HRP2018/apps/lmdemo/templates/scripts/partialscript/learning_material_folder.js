(function (scope) {
    scope.__tableSource = [];
    scope.$root.isDisplay = false;
    scope.mode = 0;
    scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.$root.add = function () {
        scope.mode = 1; // set mode chỉnh sửa
        openDialog("${get_res('Detail_LearningMaterial','Create New Folder')}", 'form/addLearningMaterial', function () {
            setTimeout(function () {
                $(window).trigger('resize');
            }, 200);
        });
    }
    scope.$root.edit = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_LearningMaterial','Create New Folder')}", 'form/addLearningMaterial', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
        } else {
            scope.currentItem = null;
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    scope.$root.delete = function () {
        if (scope.currentItem) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_MaterialFolder/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope.currentItem = [];
                            scope.selectedItems = [];
                            scope.$root.refresh();
                        }
                    })
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }
    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "folder_name", "title": "${get_res('category_name_table_header','Category Name')}" },
        { "data": "moderator_id", "title": "${get_res('moderator_table_header','Moderator')}" },
        { "data": "approver_id", "title": "${get_res('approver_table_header','Approver(s)')}" },
        { "data": "active", "title": "${get_res('status_table_header','Status')}" },
    ];
    scope.$$tableConfig = {};
    scope.$root.$$tableConfig = {};
    scope.$root._tableData = _tableData;
    scope.$root._departments = _departments;
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.mode = 2;
        scope.$root.edit();
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

    /* Tree */
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
            { "data": "folder_name", "title": "${get_res('category_name_table_header','Category Name')}" },
            { "data": "moderator_id", "title": "${get_res('moderator_table_header','Moderator')}" },
            { "data": "approver_id", "title": "${get_res('approver_table_header','Approver(s)')}" },
            { "data": "active", "title": "${get_res('status_table_header','Status')}" },
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

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        //if (scope.treeCurrentNode.hasOwnProperty('folder_id')) {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.LMSLS_MaterialFolder/get_list_with_searchtext')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "where": {
                            'folder_id': scope.treeCurrentNode.folder_id ? scope.treeCurrentNode.folder_id : null
                        },
                        "sort": sort
                    })
                    .done()
                    .then(function (res) {
                        var data = {
                            recordsTotal: res.total_items,
                            recordsFiltered: res.total_items,
                            data: res.items
                        };
                        scope.__tableSource = JSON.parse(JSON.stringify(res.items));
                        callback(data);
                        scope.currentItem = null;
                        scope.$apply();
                    })
        //}
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

    function _departments() {
        services.api("${get_api_key('app_main.api.LMSLS_MaterialFolder/get_list')}")
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

    function _selectBoxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": [
                    "LMSTypeFolder",
                ]
            })
            .done()
            .then(function (res) {
                scope.$root.cbbTypeFolder = getValue(res.values, "LMSTypeFolder");
                scope.$applyAsync();
                function getValue(response, listName) {
                    return _.findWhere(response, { "list_name": listName }) ? _.findWhere(response, { "list_name": listName }).values : [];
                }
            })
    }

    (function _init_() {
        _departments();
        _selectBoxData();
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
        scope.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
        scope.$applyAsync();
    })();

    scope.$watch("selectedFunction", function (function_id) {
        console.log(function_id);
        var $his = scope.$root.$history.data();
        if (scope.currentItem)
            window.location.href = "#page=" + $his.page + "&f=" + function_id;
    });

    scope.$watch("currentItem", function () {
        scope.$root.currentItem.push(scope.currentItem);
        scope.$applyAsync();
    });

    //scope.$root.$history.onChange(scope, function (data) {
    //    if (scope.mapName.length > 0) {
    //        if (data.f) {
    //            scope.$partialpage = _.filter(scope.$root.$functions, function (f) {
    //                return f.function_id = data.f
    //            })[0].url;
    //            var func = _.filter(scope.mapName, function (f) {
    //                return f["function_id"] == data.f;
    //            });
    //            if (func.length > 0) {
    //                scope.$partialpage = func[0].url;
    //                scope.currentFunction = func[0];
    //            } else {
    //                window.location.href = "#";
    //            }
    //        } else {
    //            //scope.$partialpage = scope.mapName[0].url;
    //        }
    //        scope.$apply();
    //    } else {
    //        window.location.href = "#";
    //    }
    //});

    scope.$watch('treeCurrentNode', function (val) {
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, scope.$$tableConfig.searchText)
    })
});