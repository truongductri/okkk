(function (scope) {
    scope.$root.extendToolbar = false;
    scope.dashBoard = {}
    scope.labelSetChart = [];
    (function getLabelDateChart() {
        var arr = [];
        for (var i = 0; i < 10; i++) {
            arr.push(moment().subtract(i, 'd').format('DD/MM/YYYY'));
        }
        scope.labelSetChart = arr.reverse();
    })();

    scope.$chartLine = {
        numberView: 10,
        
    };
    scope.dataSetChart = '';
    scope.labelSetChart = scope.labelSetChart;
    scope.labelsPie = [];
    scope.dataPie = [];
    scope.colorsPie = ['#803690', '#00ADF9', '#DCDCDC', '#46BFBD','#FDB45C']

    scope.arrData = function (list) {
        

    }
    scope.labelsHorizontalBar = [];
    
    //scope.seriesHorizontalBar = ['Series A', 'Series B'];

    scope.dataHorizontalBar = [];
    scope.downLoadsChart = [];
    scope.viewChart = [];
    scope.shareChart = [];
    scope.loadInfoDashBoardPage = function () {
        services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/get_data_dash_board_page')}")
            .data({
            })
            .done()
            .then(function (res) {
                debugger
                
                 scope.dashBoard = res;
                var arr_folder = [];
                var folder_views = _.map(scope.dashBoard.top_five_folder, function (val) {
                    if (val.items.length > 0) {
                        return { folder_id: val.folder_id, number: _.reduce(val.items, function (memo, num) { return memo.views.length + num.views.length; }) }
                    } else { return { folder_id: val.folder_id, number: 0 } }
                })
                for (var i = 0; i < 5; i++) {
                    var max = _.max(folder_views, function (val) { return val.number; });
                    if (max.number != 0) {
                        scope.dataPie.push(max.number)
                        scope.labelsPie.push(max.folder_id)
                        folder_views = _.reject(folder_views, function (num) { return num.folder_id == _.max(folder_views, function (val) { return val.number; }).folder_id });
                    }        
                    
                }

                for (var i = 0; i < scope.dashBoard.top_five_material.length; i++) {
                    if (scope.dashBoard.top_five_material[i]) {
                        scope.labelsHorizontalBar.push(scope.dashBoard.top_five_material[i].material_name)
                        scope.dataHorizontalBar.push(scope.dashBoard.top_five_material[i].views.length)
                    }
                }

                var date_now = moment().format('YYYY-MM-DD')
                for (var j = 0; j < 10; j++) {
                    var download_chart = 0
                    var view_chart = 0
                    var share_chart = 0

                    for (var i = 0; i < scope.dashBoard.dynamic_chart.length; i++) {
                        if (scope.dashBoard.dynamic_chart[i].downloads) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].downloads.length; k++) {
                                scope.dashBoard.dynamic_chart[i].downloads.length
                                var date_created = scope.dashBoard.dynamic_chart[i].downloads[k].date_created
                                var value_date_created = moment(date_created, 'YYYY-MM-DD')
                                var rangeTime = moment.preciseDiff(date_now, value_date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    download_chart += 1;

                            }
                        }
                        ////////////////////////////////////
                        if (scope.dashBoard.dynamic_chart[i].views) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].views.length; k++) {
                                scope.dashBoard.dynamic_chart[i].views.length
                                var date_created = scope.dashBoard.dynamic_chart[i].views[k].date_created
                                var value_date_created = moment(date_created, 'YYYY-MM-DD')
                                var rangeTime = moment.preciseDiff(date_now, value_date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    view_chart += 1;

                            }
                        }
                        ////////////////////////////////////
                        if (scope.dashBoard.dynamic_chart[i].sharing_info) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].sharing_info.length; k++) {
                                scope.dashBoard.dynamic_chart[i].sharing_info.length
                                var date_created = scope.dashBoard.dynamic_chart[i].sharing_info[k].date_created
                                var value_date_created = moment(date_created, 'YYYY-MM-DD')
                                var rangeTime = moment.preciseDiff(date_now, value_date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    share_chart += 1;
                            }
                        }
                        //////////////////////////////
                        if (scope.dashBoard.dynamic_chart[i].sharing_social) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].sharing_social.length; k++) {
                                scope.dashBoard.dynamic_chart[i].sharing_social.length
                                var date_created = scope.dashBoard.dynamic_chart[i].sharing_social[k].date_created
                                var rangeTime = moment.preciseDiff(date_now, date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    share_chart += 1;
                            }
                        }

                    }
                    scope.downLoadsChart.push(download_chart)
                    scope.viewChart.push(view_chart)
                    scope.shareChart.push(share_chart)

                }
                var dataSetChart = [
                    {
                        backgroundColor: "rgb(106, 143, 0)",
                        borderColor: "rgb(106, 143, 0)",
                        borderWidth: 1,
                        data: scope.downLoadsChart.reverse(),
                        label: 'Download',
                        fill: false,
                        type: 'line',
                        lineTension: 0,
                    }, {
                        backgroundColor: "rgb(1, 110, 208)",
                        borderColor: "rgb(1, 110, 208)",
                        borderWidth: 1,
                        data: scope.viewChart.reverse(),
                        label: 'View',
                        fill: false,
                        type: 'line',
                        lineTension: 0,
                    }, {
                        backgroundColor: "rgb(226, 113, 54)",
                        borderColor: "rgb(226, 113, 54)",
                        borderWidth: 1,
                        data: scope.shareChart.reverse(),
                        label: 'Share',
                        fill: false,
                        type: 'line',
                        lineTension: 0,
                    }
                ]
                scope.dataSetChart = dataSetChart;
                scope.$applyAsync();
            })
    }

    scope.loadInfoDashBoardPage();
});