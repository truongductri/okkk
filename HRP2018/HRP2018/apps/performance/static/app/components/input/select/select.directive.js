(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('inputSelect', ["$parse", "$filter", "$sce", inputSelect])
        .controller('SelectpickerPanelCtrl', SelectpickerPanelCtrl);

    /** @ngInject */
    function inputSelect($parse, $filter, $sce) {
        return {
            restrict: 'E',
            //replace: true,
            scope: {
                list: "=",
                ngModel: "=",
                placeholder: "@",
                fieldValue: "@value",
                fieldCaption: "@caption",
                ngChange: "=",
                except: "=",
                exceptField: "@"
            },
            //transclude: true,
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            //template: '<input type="text" class="form-control zb-form-input"/>',
            templateUrl: "app/components/input/select/select.html",
            //controller: function($scope, $element, $attrs) {
            //    $scope.math = Math.random();
            //    console.log("++++++++++++++++++++++++++++++++++++++++++++");
            //    console.log($scope, $element, $attrs)
            //    console.log("++++++++++++++++++++++++++++++++++++++++++++");
            //},
            link: function ($scope, elem, attr) {
                var cmp = $(elem);
                //$compile(cmp.contents())($scope);
                if (attr["required"]) {
                    cmp.attr("zb-required", '');
                }
                $scope.selectedItem = {};

                function checkExcept(val) {
                    if (val && val.length > 0 && $scope.list && $scope.list.length > 0) {
                        $scope.selectWithSearchItems = JSON.parse(JSON.stringify($scope.list));
                        $.each($scope.selectWithSearchItems, function (i, v) {
                            v["__fieldCaption"] = $sce.trustAsHtml(v[$scope.fieldCaption]);
                        });
                        $.each($scope.except, function (i, v) {
                            var filterObj = {};
                            if (typeof (v) == "string") {
                                filterObj[$scope.fieldValue] = v;
                            } else if (v && typeof (v) == "object" && v.hasOwnProperty($scope.exceptField)) {
                                filterObj[$scope.fieldValue] = v[$scope.exceptField];
                            }
                            var item = _.findWhere($scope.selectWithSearchItems, filterObj);
                            if (item) {
                                var idx = $scope.selectWithSearchItems.indexOf(item);
                                if (idx >= 0) {
                                    $scope.selectWithSearchItems.splice(idx, 1);
                                }
                            }
                            $scope.$applyAsync();
                        });
                    }
                }

                $scope.$watch("list", function (val, old) {
                    if ($scope.list) {
                        $scope.selectWithSearchItems = JSON.parse(JSON.stringify($scope.list));
                        $.each($scope.selectWithSearchItems, function (i, v) {
                            v["__fieldCaption"] = $sce.trustAsHtml(v[$scope.fieldCaption]);
                        });
                        /*Watch model*/
                        var existsWatchModel = false;
                        if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                            existsWatchModel = _.filter($scope.$$watchers, function (f) {
                                return f.exp === "ngModel"
                            }).length > 0;
                        }
                        if (!existsWatchModel) {
                            $scope.$watch("ngModel", function (v) {
                                if ($scope.ngModel) {
                                    var $selectedItem = $filter('filter')($scope.selectWithSearchItems, function (f) {
                                        return f[$scope.fieldValue] == $scope.ngModel;
                                    });
                                    if ($selectedItem.length > 0) {
                                        $scope.selectedItem = {
                                            selected: $selectedItem[0]
                                        };
                                    }
                                }
                            });
                        }
                        /*Watch Selected Item*/
                        var existsWatch = false;
                        if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                            existsWatch = _.filter($scope.$$watchers, function (f) {
                                return f.exp === "selectedItem.selected"
                            }).length > 0;
                        }
                        if (!existsWatch) {
                            $scope.$watch("selectedItem.selected", function (val, old) {
                                var retval = (val && val[$scope.fieldValue]) ? val[$scope.fieldValue] : null;
                                $scope.ngModel = retval;
                                if (angular.isFunction($scope.ngChange)) {
                                    ($scope.ngChange)(retval);
                                }
                            });
                        }
                        checkExcept($scope.except);
                    }
                });
                $scope.$watch("except", function (val) {
                    checkExcept(val);
                })
            }
        };
    }
    function SelectpickerPanelCtrl($scope, $sce) { }
})();