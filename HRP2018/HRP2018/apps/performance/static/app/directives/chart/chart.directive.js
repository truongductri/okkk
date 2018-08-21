(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('chart', combobox);

    combobox.$inject = ['templateService'];
    
    function combobox(templateService) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            scope: {
                heightChart: "=",
                titleChart: "@",
                chartDataSet: "=",
                chartLabelSet: "=",
                listValue: "=",
                currentItem: "=",
                testThu: "="
            },
            templateUrl: templateService.getTemplatePath('chart')
        };
        return directive;

        function link(scope, element, attrs) {
            $("#chart-0").css({
                height: scope.heightChart
            })
            compile(scope, element, attrs);
            scope.$watch("chartDataSet", function (val) {
                compile(scope, element, attrs);
            })
        }

        function compile(scope, element, attrs) {
            var presets = window.chartColors;
            var utils = Samples.utils;
            var inputs = {
                min: 0,
                max: 100,
                count: 10,
                decimals: 2,
                continuity: 1
            };

            function generateData(config) {
                return utils.numbers(Chart.helpers.merge(inputs, config || {}));
            }

            function generateLabels(config) {
                return utils.months(Chart.helpers.merge({
                    count: inputs.count,
                    section: 3
                }, config || {}));
            }

            var options = {
                maintainAspectRatio: false,
                spanGaps: false,
                elements: {
                    line: {
                        tension: 0.000001
                    }
                },
                plugins: {
                    filler: {
                        propagate: false
                    }
                },
                scales: {
                    xAxes: [{
                        ticks: {
                            autoSkip: false,
                            maxRotation: 0
                        }
                    }]
                }
            };

            new Chart('chart-0', {
                type: 'line',
                data: {
                    labels: scope.chartLabelSet,
                    datasets: scope.chartDataSet
                },
                options: Chart.helpers.merge(options, {
                    title: {
                        text: scope.titleChart,
                        display: true
                    }
                })
            });

            // eslint-disable-next-line no-unused-vars
            function toggleSmooth(btn) {
                var value = btn.classList.toggle('btn-on');
                Chart.helpers.each(Chart.instances, function (chart) {
                    chart.options.elements.line.tension = value ? 0.4 : 0.000001;
                    chart.update();
                });
            }

            // eslint-disable-next-line no-unused-vars
            function randomize() {
                var seed = utils.rand();
                Chart.helpers.each(Chart.instances, function (chart) {
                    utils.srand(seed);

                    chart.data.datasets.forEach(function (dataset) {
                        dataset.data = generateData();
                    });

                    chart.update();
                });
            }
        }

        
    }

})();