(function (scope) {
	scope.__tableSource = [];
	scope.mode = 0;
	scope.showDetail = false;
	scope.filterFunctionModel = ''
	scope.currentFunction = '';
	scope.mapName = [];
	scope.selectFunc = function (event, f) {
		scope.selectedFunction = f;
	}
    scope.entity = {};
   
	/* Table */
	//Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "apr_year", "title": "${get_res('apr_year_table_header','Năm')}" },
        { "data": "apr_period", "title": "${get_res('apr_period_table_header','Kỳ đánh giá')}"},
        { "data": "emp_final_from", "title": "${get_res('emp_final_from_table_header','NV đánh giá từ')}", "format": "date:" + scope.$root.systemConfig.date_format  },
        { "data": "emp_final_to", "title": "${get_res('emp_final_to_table_header','NV đánh giá đến')}", "format": "date:" + scope.$root.systemConfig.date_format  },
        { "data": "approval_final_from", "title": "${get_res('approval_final_from_table_header','Xét duyệt từ')}", "format": "date:" + scope.$root.systemConfig.date_format  },
		{ "data": "approval_final_to", "title": "${get_res('approval_final_to_header','Xét duyệt đến')}", "format": "date:" + scope.$root.systemConfig.date_format }
	];
	scope.$$tableConfig = {};
	//Dữ liệu cho table
	scope.tableSource = _loadDataServerSide;

    scope.onSelectTableRow = function ($row) {
        debugger
		scope.$root.$commons = {
			$current_apr_period: $row.apr_period
        };
        scope.entity = $row;
		$('.hcs-profile-list').fadeToggle();
		setTimeout(function () {
			scope.showDetail = scope.showDetail === false ? true : false;
			scope.mode = 2;
			scope.$partialpage = scope.mapName[0].url;
			scope.$applyAsync();
			$(window).trigger('resize');
		}, 500);
    };
    function Map_Period(periodNum) {
        var strPeriod = "";
        for (var i = 0; i < 12; i++) {
            if (periodNum == i + 1) {
                strPeriod = "Tháng " + (i + 1).toString();
                return strPeriod;
            }

        }
        for (var j = 13; j <= 16; j++) {
            if (periodNum == j) {
                strPeriod = "Quý " + (j - 12).toString();
                return strPeriod;
            }
        }
        if (periodNum == 17)
            strPeriod = "6 tháng đầu năm";
        else if (periodNum == 18)
            strPeriod = "6 tháng cuối năm";
        else
            strPeriod = "Năm";
        return strPeriod;
    }
	//Danh sách các dòng đc chọn (nếu là table MultiSelect)
	scope.selectedItems = [];
	//Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
	scope.currentItem = null;
	scope.tableSearchText = '';
	//Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };
    scope.$period_obj = {};
 

	

	//function button
    scope.addAprPeriod = addAprPeriod;
    scope.editAprPeriod = editAprPeriod;
    scope.deleteAprPeriod = onDelete;
    scope.btnUpload = onImport;
    scope.btnDownload = onExport;
    scope.btnRefresh = refresh;
   

	//Navigation: quay trở về UI list
	scope.backPage = backPage;

	function backPage() {
		$('.hcs-profile-list').fadeToggle();
		setTimeout(function () {
			scope.showDetail = scope.showDetail === false ? true : false;
			scope.mode = 0;
			scope.$partialpage = scope.mapName[0].url;
			scope.currentItem = scope.mapName[0];
			scope.selectedFunction = scope.mapName[0].function_id;
			scope.$applyAsync();
			$(window).trigger('resize');
		}, 500);
	}

    function addAprPeriod() {
        debugger
            $('.hcs-profile-list').fadeToggle();
            setTimeout(function () {
                scope.showDetail = scope.showDetail === false ? true : false;
                scope.mode = 1;
                scope.currentItem = scope.mapName[0];
                scope.$partialpage = scope.mapName[0].url;
                scope.$applyAsync();
                $(window).trigger('resize');
            }, 500);
        }
		

    function editAprPeriod() {
        debugger
        if (scope.currentItem == null && scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
        else {
            scope.entity = scope.currentItem;
            $('.hcs-profile-list').fadeToggle();
            setTimeout(function () {
                scope.showDetail = scope.showDetail === false ? true : false;
                scope.mode = 2;
                scope.currentItem = scope.mapName[0];
                scope.$partialpage = scope.mapName[0].url;
                scope.$applyAsync();
                $(window).trigger('resize');
            }, 500);
            
        }
    }

	function refresh() {
		var tableConfig = scope.$$tableConfig;
		_tableData(tableConfig.iPage,
			tableConfig.iPageLength, tableConfig.orderBy,
			tableConfig.searchText, tableConfig.fnReloadData);
	}


	

    function onSelectTableRow($row) {
		$('.hcs-profile-list').fadeToggle();
		setTimeout(function () {
			scope.showDetail = scope.showDetail === false ? true : false;
			$(window).trigger('resize');
		}, 500);
	};

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
		var sort = {};
		$.each(orderBy, function (i, v) {
			sort[v.columns] = (v.type === "asc") ? 1 : -1;
		});
		sort[orderBy[0].columns] =
			services.api("${get_api_key('app_main.api.TMPER_AprPeriod/get_list_with_searchtext')}")
				.data({
					//parameter at here
					"pageIndex": iPage - 1,
					"pageSize": iPageLength,
					"search": searchText,
					"sort": sort
				})
				.done()
            .then(function (res) {
                res.items.forEach(function (item) {
                    item.apr_period = Map_Period(item.apr_period);
                });
                var data = {
                    recordsTotal: res.total_items,
                    recordsFiltered: res.total_items,
                    data: res.items
                };
                callback(data);
                scope.currentItem = null;
                scope.$apply();
				})
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

    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TMLS_FactorAppraisal'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }

    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMPER_AprPeriod/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    };

   


	(function _init_() {
		scope.handleData = new handleData();
		scope.mapName = scope.handleData.mapName;
		scope.currentFunction = scope.mapName[0];
		scope.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
		scope.$applyAsync();
	})();

	scope.$watch("selectedFunction", function (function_id) {
		var $his = scope.$root.$history.data();
		if (scope.currentItem) {
			var func = _.filter(scope.mapName, function (f) {
				return f["function_id"] == function_id;
			});
			if (func.length > 0) {
				scope.$partialpage = func[0].url;
				scope.currentFunction = func[0];
			}
		}
		//window.location.href = "#page=" + $his.page + "&f=" + function_id;
	});

});