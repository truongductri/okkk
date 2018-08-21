(function () {
    'use strict';

    angular.module('ZebraApp.components')
        .directive('pagination', pagination);

    /** @ngInject */
    function pagination() {
        return {
            restrict: 'E',
            replace: true,
            transclude: false,
            scope: {
                items: "=",
                itemsOnPage: "=",
                displayedPages: "=",
                prevText: "@",
                nextText: "@",
                currentPage: "=",
                onPageClick: "="
            },
            template: '<div class="zb-pagination"></div>',
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr) {
                var _draw = function () {
                    $(elem).pagination({
                        items: $scope.items ? $scope.items : 0,
                        itemsOnPage: $scope.itemsOnPage ? $scope.itemsOnPage : 30,
                        displayedPages: $scope.displayedPages ? $scope.displayedPages : 3,
                        cssStyle: 'light-theme',
                        prevText: $scope.prevText ? $scope.prevText : "<",
                        nextText: $scope.nextText ? $scope.nextText : ">",
                        edges: 2, //How many page numbers are visible at the beginning/ending of the pagination.
                        //hrefTextPrefix: "#p=",
                        currentPage: $scope.currentPage ? $scope.currentPage : 1,
                        onPageClick: function (pIdx) {
                            if (angular.isFunction($scope.onPageClick)) {
                                ($scope.onPageClick)(pIdx);
                            }
                            return false;
                        }
                    });
                }
                _draw();

                $scope.$watchGroup(["items", "currentPage"], function (v) {
                    _draw();
                });
            }
        };
    }
})();