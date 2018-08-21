(function (scope) {

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
        dataSetChart: [{
            backgroundColor: "rgb(106, 143, 0)",
            borderColor: "rgb(106, 143, 0)",
            borderWidth: 1,
            data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            label: 'Download',
            fill: false,
            type: 'line',
            lineTension: 0,
        }, {
            backgroundColor: "rgb(1, 110, 208)",
            borderColor: "rgb(1, 110, 208)",
            borderWidth: 1,
            data: [10, 9, 30, 8, 5, 22, 33, 11, 2, 55],
            label: 'View',
            fill: false,
            type: 'line',
            lineTension: 0,
        }, {
            backgroundColor: "rgb(226, 113, 54)",
            borderColor: "rgb(226, 113, 54)",
            borderWidth: 1,
            data: [10, 20, 30, 40, 50, 10, 20, 30, 40, 54],
            label: 'Share',
            fill: false,
            type: 'line',
            lineTension: 0,
        }],
        labelSetChart: scope.labelSetChart,
    };
    scope.labelsPie = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"];
    scope.dataPie = [300, 500, 100, 200, 100];
    scope.colorsPie = ['#803690', '#00ADF9', '#DCDCDC', '#46BFBD','#FDB45C']


    scope.labelsHorizontalBar = ['Document 1', 'Document 2', 'Document 3', 'Document 4', 'Document 5'];
    //scope.seriesHorizontalBar = ['Series A', 'Series B'];

    scope.dataHorizontalBar = [
        [65, 59, 80, 81, 56],
    ];

    scope.loadInfoDashBoardPage = function () {

        services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/get_data_dash_board_page')}")
            .data({
            })
            .done()
            .then(function (res) {
                debugger
                scope.dashBoard = res
                scope.$applyAsync();
            })
    }
    scope.loadInfoDashBoardPage();
});