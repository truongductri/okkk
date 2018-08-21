(function () {
    'use strict';

    angular.module('ZebraApp.components.combobox')
        .directive('btnDialogCombobox', ["$compile", combobox]);

    /** @ngInject */
    function combobox($compile) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                loadData: "=",
                //dataSource: "=source",
                title: "@",
                //onSelect: "=",
                onAccept: "=",

                /*begin search*/
                onSearchChange: "=",
                onSearchPress: "=",
                /*end search*/

                /*begin pagination*/
                paging: "=",
                //onPaging: "=",
                //numberItems: "@",
                numberOnPage: "=",
                pageIndex: "=",
                /*end pagination*/

                placeholder: "@",
                ngModel: "=",
                /*Field lấy giá trị cho combobox*/
                keyField: "@",
                /*Field hiển thị trên combobox*/
                captionField: "@",
                /*Caption hiển thị khi lần đầu loadCombobox*/
                initData: "=",
                params: "=",
                txtButton: "@",
                classIcon: "@",
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            template: `
                <div class="zb-form-combobox input-group">
                    <div class="zb-combobox-template" ng-transclude style="display:none"></div>
                    <div class="input-group-btn">   
                      <button class="btn btn-default zb-open-modal" style="float:right;">
                        <span><i class="glyphicon glyphicon-plus"></i></span> Add
                      </button>
                    </div>
                  </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrl, transclude) {
                // if(attr["required"]){
                //   $(elem).wrap("<span zb-required></span>")
                // }
                //$(elem).find("button.zb-open-modal").text($scope.txtButton);

                //$(elem).find("span.btnText").text($scope.txtButton);
                //var i = document.createElement("i");
                //i.className = $scope.classIcon;
                //$(elem).find("span.btnText").append(i);
                $scope.$selectedItem = ($scope.initData) ? $scope.initData : [];
                $scope.$selectedItemDisplay = JSON.parse(JSON.stringify($scope.$selectedItem));
                $scope.$applyAsync();

                $scope.$deleteSelectedItem = function (item) {
                    if (item && item[$scope.keyField]) {
                        var idx = _.findIndex($scope.$selectedItem, function (d) {
                            return d[$scope.keyField] == item[$scope.keyField];
                        });
                        if (idx >= 0) {
                            $scope.$selectedItem.splice(idx, 1);
                        }
                        var model = [];
                        $.each($scope.$selectedItem, function (i, v) {
                            model.push(v[$scope.keyField]);
                        });
                        $scope.ngModel = model;
                    }
                    $scope.$selectedItemDisplay = $scope.$selectedItem;
                    $scope.$applyAsync();
                }
                var _control = {
                    setCaption: function (captions) {
                        var placeholder = $(elem).find(".placeholder");
                        var displayValue = $(elem).find(".display-value");
                        if (captions) {
                            placeholder.hide();
                            displayValue.show();
                            //displayValue.html(caption)
                        } else {
                            placeholder.show();
                            displayValue.hide();
                        }
                        $scope.$applyAsync();
                    },
                    // applyCaption: function(items) {
                    //     _control.setCaption($scope.$selectedItem);
                    // },
                    setValue: function (items) {
                        if ($scope.keyField) {
                            var model = [];
                            $.each(items, function (i, v) {
                                model.push(v[$scope.keyField]);
                            });
                            $scope.ngModel = model;
                            $scope.$applyAsync();
                        }
                    },
                    setSelectedItem: function (item) {
                        if (item && item[$scope.keyField]) {
                            var idx = _.findIndex($scope.$selectedItem, function (d) {
                                return d[$scope.keyField] == item[$scope.keyField];
                            });
                            if (idx >= 0) {
                                $scope.$selectedItem.splice(idx, 1);
                            } else {
                                $scope.$selectedItem.push(item);
                            }
                        }
                        $scope.$applyAsync();
                    },
                    clearValue: function () {
                        $scope.ngModel = null;
                        _control.setCaption(null);
                    }
                }

                $(elem).find(".zb-combo-btn-clear").bind("click", function () {
                    _control.clearValue();
                });

                var dialogTemplate = '' +
                    '<div class="zb-modal-combobox modal fade" role="dialog">' +
                    '    <div class="modal-dialog">' +
                    '        <div class="modal-content">' +
                    '            <div class="modal-header">' +
                    '                <div class="left-content pull-left">' +
                    '                    <span class="modal-title">{{title}}</span>' +
                    '                </div>' +
                    '                <div class="right-content pull-right">' +
                    '                    <button type="button" class="close zb-close-modal"><i class="bowtie-icon bowtie-navigate-close"></i></button>' +
                    '                </div>' +
                    '            </div>' +
                    '            <div class="modal-body">' +
                    '                <div class="zb-combobox-toolbar">' +
                    '                    <input-text-icon icon="bowtie-icon bowtie-search" icon-align="right" placeholder="{{}}" on-change="$cbbConfig.onSearchChange" on-click="$cbbConfig.onSearchPress" ng-model="texticon"></input-text-icon>' +
                    '                </div>' +
                    '                <div class="zb-combobox-content">' +
                    '                   <div class="zb-combo-list-multi" ng-repeat="$cbbItem in $cbbConfig.list" ng-click="$cbbConfig.onSelect($event, $cbbItem)">' +
                    '                     <div class="list-checkbox">' +
                    '                       <span><i class="bowtie-icon bowtie-checkbox-empty"></i></span>' +
                    '                     </div>' +
                    '                     <div class="list-content">' +
                    '                       <<template>>' +
                    '                     </div>' +
                    '                   </div>' +
                    '                </div>' +
                    '            </div>' +
                    '            <div class="modal-footer">' +
                    '                <div class="left-content pull-left" ng-if="$cbbConfig.isPaging">' +
                    '                    <pagination class="zb-combobox-footer" items="$cbbConfig.numberItems" items-on-page="$cbbConfig.numberOnPage" current-page="$cbbConfig.pageIndex" on-page-click="$cbbConfig.onPaging"/>' +
                    '                </div>' +
                    '                <div class="right-content pull-right">' +
                    '                    <button ng-click="$cbbConfig.onAccept()"><i class="bowtie-icon bowtie-check-light"></i></button>' +
                    '                </div>' +
                    '            </div>' +
                    '        </div>' +
                    '    </div>' +
                    '</div>';

                var htmlTemplate = $(elem).find(".zb-combobox-template").html();
                var keys = htmlTemplate.match(/(\##.*?\##)/gm);
                $.each(keys, function (i, v) {
                    var key = v.split("##").join("");
                    var retKey = "{{$cbbItem." + key + "}}";
                    htmlTemplate = htmlTemplate.split(v).join(retKey);
                });
                dialogTemplate = dialogTemplate.replace("<<template>>", htmlTemplate);
                var $dialog = $(dialogTemplate);

                $(elem).find(".zb-open-modal").bind("click", function () {
                    debugger
                    $dialog.appendTo("body");
                    $dialog.modal({ backdrop: 'static', keyboard: false });

                    if (!$scope.$cbbConfig) {
                        var fnLoadData = function (pgIdx, txtSearch) {
                            if (angular.isFunction($scope.loadData)) {
                                ($scope.loadData)(function (result) {
                                    $scope.$cbbConfig.list = (result && result.data) ? result.data : [];
                                    $scope.$cbbConfig.numberItems = (result && result.recordsTotal) ? result.recordsTotal : 0;
                                    $scope.$applyAsync();
                                }, pgIdx, txtSearch, $scope.$params);
                            }
                        }

                        $scope.$cbbConfig = {
                            list: [], //$scope.dataSource ? $scope.dataSource : [],
                            onSelect: function ($event, item) {
                                var currElem = $($event.target).closest(".zb-combo-list-multi");
                                //currElem.siblings().removeClass("zb-combo-selected");
                                var icon = currElem.find(".bowtie-icon");
                                if (icon.hasClass("bowtie-checkbox-empty")) {
                                    icon.removeClass("bowtie-checkbox-empty");
                                    icon.addClass("bowtie-checkbox");
                                    currElem.addClass("zb-combo-selected");
                                } else {
                                    icon.addClass("bowtie-checkbox-empty");
                                    icon.removeClass("bowtie-checkbox");
                                    currElem.removeClass("zb-combo-selected");
                                }
                                // if (angular.isFunction($scope.onSelect)) {
                                //     ($scope.onSelect)(item);
                                // }
                                _control.setSelectedItem(item);
                            },
                            onSearchChange: function (txtSearch) {
                                if ($scope.onSearchChange) {
                                    $scope.txtSearch = txtSearch;
                                    $scope.$applyAsync()
                                    fnLoadData($scope.currPageIndex, $scope.txtSearch);
                                }
                            },
                            onSearchPress: function (txtSearch) {
                                if ($scope.onSearchPress) {
                                    $scope.txtSearch = txtSearch;
                                    $scope.$applyAsync()
                                    fnLoadData($scope.currPageIndex, $scope.txtSearch);
                                }
                            },

                            isPaging: $scope.paging ? true : false,
                            onPaging: function (pgIdx) {
                                $scope.currPageIndex = pgIdx;
                                $scope.$applyAsync()
                                fnLoadData($scope.currPageIndex, $scope.txtSearch);
                            },
                            numberItems: 0,
                            numberOnPage: $scope.numberOnPage ? $scope.numberOnPage : 30,
                            pageIndex: $scope.pageIndex ? $scope.pageIndex : 1,

                            onAccept: function () {
                                var item = $scope.$selectedItem;
                                if (item) {
                                    _control.setValue(item);
                                    if (angular.isFunction($scope.onAccept)) {
                                        ($scope.onAccept)(item);
                                    }
                                }
                                $scope.$selectedItemDisplay = $scope.$selectedItem;
                                $scope.$applyAsync();

                                $dialog.modal("hide");
                            }
                        }
                        $scope.$applyAsync();
                        fnLoadData();
                        $compile($dialog)($scope);
                    }
                });
                $dialog.find(".zb-close-modal").bind("click", function () {
                    $dialog.modal("hide");
                });
            }
        };
    }
})();