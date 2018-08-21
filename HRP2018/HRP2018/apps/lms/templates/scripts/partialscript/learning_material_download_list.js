(function (scope) {

		
    scope.$root.extendToolbar = true;

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
    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
            { "data": "material_id", "title": "${get_res('material_id_table_header','ID')}" },
            { "data": "material_name", "title": "${get_res('material_name_table_header','File Name')}" },
            { "data": "material_type", "title": "${get_res('material_type_table_header','File Type')}" },
            { "data": "size_files", "title": "${get_res('Size_table_header','Size')}" },
            { "data": "creator", "title": "${get_res('creator_table_header','Created by')}" },
            { "data": "num_downloads", "title": "${get_res('Number_download_table_header','No. of Download')}" },
            { "data": "last_downloads", "title": "${get_res('latest_download_table_header','Latest Downloaded on')}","format": "date:" + 'dd/MM/yyyy h:mm:ss a' },
        
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
            { "data": "material_id", "title": "${get_res('material_id_table_header','ID')}" },
            { "data": "material_name", "title": "${get_res('material_name_table_header','File Name')}" },
            { "data": "material_type", "title": "${get_res('material_type_table_header','File Type')}" },
            { "data": "size_files", "title": "${get_res('Size_table_header','Size')}" },
            { "data": "creator", "title": "${get_res('creator_table_header','Created by')}" },
            { "data": "num_downloads", "title": "${get_res('Number_download_table_header','No. of Download')}" },
            { "data": "last_downloads", "title": "${get_res('latest_download_table_header','Latest Downloaded on')}", "format": "date:" + 'dd/MM/yyyy h:mm:ss a' },
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
        debugger
        //if (scope.treeCurrentNode.hasOwnProperty('folder_id')) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/get_list_download_history')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
					"sort": sort,
                })
                .done()
            .then(function (res) {
                    debugger
                    var resData = _.map(res.items, function (num) {
                        num.size_files = num.size_files + "KB";
                        return num;
                    });
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: resData
                    };
                    scope.__tableSource = JSON.parse(JSON.stringify(resData));
					scope.ItemTables = JSON.parse(JSON.stringify(resData));
					var total_rating = 0;
					for (var i = 0; i < scope.ItemTables.length; i++) {
						var Ratings = [];
						if (data.data[i].comments == null) {
							data.data[i]["total_rating"] = 0;
						}
						else if (data.data[i].comments && data.data[i].comments.length > 0) {
							for (var j = 0; j < data.data[i].comments.length; j++) {
								Ratings.push(data.data[i].comments[j].rating)
							}
							var sum = Ratings.reduce((previous, current) => current += previous);
							data.data[i]["total_rating"] = sum / Ratings.length;
						}
					}
					scope.ItemTables = JSON.parse(JSON.stringify(data.data));
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
        //}
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


    scope.$watch('treeCurrentNode', function (val) {
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, scope.$$tableConfig.searchText)
    })







    scope.fnSelectDataGrid = fnSelectDataGrid;

    function fnSelectDataGrid(item) {
        scope.currentItem = item ? item : scope.currentItem;
        scope.$applyAsync();
    }

    scope.onCheckItemGird = function (item) {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el._id == item._id
        })
        if (arrayId.length > 0) {
            var arrayItem = scope.selectedItems.filter(function (el) {
                return el._id != item._id
            })
            scope.selectedItems = arrayItem;
        } else {
            scope.selectedItems.push(item);
        }

	}

	scope.getNumber = function (num) {
		var arr = [];
		for (var i = 0; i < num; i++) {
			arr.push(i);
		};
		return arr;
	}


	scope.getStars = function (rating) {
    // Get the value
		var val = parseFloat(rating);
    // Turn value into number/100
		var size = val/5*100;
		return size + '%';
    }

    scope.$watch("$parent.searchText", function (val) {
        debugger
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, val)

        scope.$applyAsync();
    });
});
