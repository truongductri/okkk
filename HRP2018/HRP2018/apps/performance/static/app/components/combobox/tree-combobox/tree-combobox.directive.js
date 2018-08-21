(function() {
    'use strict';

    angular.module('ZebraApp.components.combobox')
        .directive('treeCombobox', ["$compile", combobox]);

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
                //onSearch: "=",
                /*end search*/

                multiSelect: "=",

                //closeOnSelect: "=",

                placeholder: "@",
                ngModel: "=",

                captionField: "@",
                parentField: "@",
                keyField: "@",
                checkedField: "@",

                initData: "=",
                params: "=",
                reload: "="
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            template: `
              <div class="zb-form-combobox input-group">
                <div class="form-control">
                  <span class="placeholder">{{placeholder}}</span>
                  <span class="display-value" ng-if="!multiSelect">{{$selectedItem[captionField]}}</span>
                  <div class="display-value" ng-if="multiSelect">
                        <span class="multi-value" ng-repeat="v in $selectedItem">
                            {{v[captionField]}}
                            <i class="bowtie-icon bowtie-math-multiply-light" ng-click="$deleteSelectedItem(v)"></i>
                        </span>
                  </div>
                </div>
                <div class="zb-combobox-template" ng-transclude style="display:none"></div>
                <div class="input-group-btn">   
                  <button class="btn btn-default zb-combo-btn-clear">
                    <i class="bowtie-icon bowtie-edit-remove"></i>
                  </button>
                  <button class="btn btn-default zb-open-modal">
                    <i class="bowtie-icon bowtie-navigate-external"></i>
                  </button>
                </div>
              </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function($scope, elem, attr, ctrl, transclude) {
                // if(attr["required"]){
                //   $(elem).wrap("<span zb-required></span>")
                // }
                var _control = {
                    setCaption: function() {
                        var placeholder = $(elem).find(".placeholder");
                        var displayValue = $(elem).find(".display-value");
                        if ($scope.$selectedItem && ($scope.$selectedItem[$scope.captionField] || $scope.$selectedItem.length > 0)) {
                            placeholder.hide();
                            displayValue.show();
                        } else {
                            placeholder.show();
                            displayValue.hide();
                        }
                    },
                    setValue: function(item) {
                        if ($scope.keyField) {
                            if ($scope.multiSelect) {
                                var data = [];
                                $.each(item, function(i, v){
                                    data.push(v[$scope.keyField]);
                                });
                                $scope.ngModel = data;
                            } else {
                                $scope.ngModel = item[$scope.keyField];
                            }
                            $scope.$applyAsync();
                        }
                    },
                    // setSelectedItem: function(item) {
                    //     $scope.$selectedItem = item;
                    //     $scope.$applyAsync();
                    // },
                    clearValue: function() {
                        $scope.ngModel = null;
                        $scope.$selectedItem = null;
                        _control.setCaption();
                        $scope.$applyAsync();
                    }
                }

                $scope.$deleteSelectedItem = function(item){
                    if($scope.multiSelect && $scope.keyField){
                        $scope.$selectedItem = _.reject($scope.$selectedItem, function(f){ 
                            return f === item; 
                        });
                        $scope.$applyAsync();
                    }
                }
                

                $(elem).find(".zb-combo-btn-clear").bind("click", function() {
                    _control.clearValue();
                });
                console.log($scope.selectedItem);
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
                    '                    <button type="button" class="zb-btn" ng-click="$$$treeCollapseAll()"><i class="bowtie-icon bowtie-chevron-up-all"></i></button>' +
                    '                    <button type="button" class="zb-btn" ng-click="$$$treeExpandAll()"><i class="bowtie-icon bowtie-chevron-down-all"></i></button>' +
                    '                    <input-text-icon icon="bowtie-icon bowtie-search" icon-align="right" placeholder="{{placeholder}}" ng-model="$cbbConfig.treeSearchText" style="float: right; width: 92%"></input-text-icon>' +
                    '                </div>' +
                    '                <div class="zb-combobox-content">' +
                    '                   <tree-data data-source="$cbbConfig.list" ' +
                    '                       display-field="{{captionField}}" parent-field="{{parentField}}" key-field="{{keyField}}"' +
                    '                       select-mode="$cbbConfig.selectMode" multi-select="$cbbConfig.multiSelect" on-select="$cbbConfig.selectTreeNode" ' +
                    '                       current-node="$cbbConfig.treeCurrentNode" selected-nodes="$cbbConfig.treeSelectedNodes" selected-root-nodes="$cbbConfig.treeSelectedRootNodes"' +
                    '                       search-text="$cbbConfig.treeSearchText" check-all="treeCheckAll" checked-field="$$$isChecked" ' +
                    '                       disabled="$cbbConfig.treeDisabled" expand-all="$$$treeExpandAll" collapse-all="$$$treeCollapseAll" select-first-node="false" />' +
                    '                </div>' +
                    '            </div>' +
                    '            <div class="modal-footer">' +
                    //'                <div class="left-content pull-left" ng-if="$cbbConfig.isPaging">' +
                    //'                    <pagination class="zb-combobox-footer" items="$cbbConfig.numberItems" items-on-page="$cbbConfig.numberOnPage" current-page="$cbbConfig.pageIndex" on-page-click="$cbbConfig.onPaging"/>' +
                    //'                </div>' +
                    '                <div class="right-content pull-right">' +
                    '                    <button ng-click="$cbbConfig.onAccept()"><i class="bowtie-icon bowtie-check-light"></i></button>' +
                    '                </div>' +
                    '            </div>' +
                    '        </div>' +
                    '    </div>' +
                    '</div>';

                var $dialog = $(dialogTemplate);

                $(elem).find(".zb-open-modal").bind("click", function() {
                    $dialog.appendTo("body");
                    $dialog.modal({ backdrop: 'static', keyboard: false });

                    if (!$scope.$cbbConfig) {
                        var fnLoadData = function(pgIdx, txtSearch) {
                            if (angular.isFunction($scope.loadData)) {
                                ($scope.loadData)($scope, function(result) {
                                    if ($scope.multiSelect && $scope.$selectedItem && $scope.$selectedItem.length > 0) {
                                        $.each(result, function(i, v) {
                                            if (_.filter($scope.$selectedItem, function(f) {
                                                    return f[$scope.keyField] === v[$scope.keyField];
                                                }).length > 0) {
                                                console.log("++++++++++++++++++", v[$scope.keyField]);
                                                v["$$$isChecked"] = true;
                                            } else{
                                                v["$$$isChecked"] = false;
                                            }
                                        });
                                    }
                                    $scope.$cbbConfig.list = (result) ? result : [];
                                    $scope.$applyAsync();
                                }, $scope.$params);
                            }
                        }

                        $scope.$cbbConfig = {
                            list: [], //$scope.dataSource ? $scope.dataSource : [],
                            treeCurrentNode: null,
                            treeSelectedNodes: [],
                            treeSelectedRootNodes: [],
                            treeSearchText: null,
                            selectMode: $scope.multiSelect ? 3 : 1,
                            multiSelect: $scope.multiSelect ? true : false,
                            treeDisabled: false,

                            selectTreeNode: function(node) {
                                console.log("APP.JS -> $scope.selectTreeNode", node);
                                if (!$scope.multiSelect) {
                                    $scope.$cbbConfig.onAccept(node);
                                    $dialog.modal("hide");
                                }
                                // if ($scope.closeOnSelect) {
                                //     $scope.$cbbConfig.onAccept(item);
                                //     $dialog.modal("hide");
                                // }
                            },

                            onAccept: function(item) {
                                if ($scope.multiSelect) {
                                    $scope.$selectedItem = $scope.$cbbConfig.treeSelectedNodes;
                                    _control.setValue($scope.$selectedItem);
                                } else {
                                    if (item) {
                                        $scope.$selectedItem = item;
                                        _control.setValue(item);

                                        if (angular.isFunction($scope.onAccept)) {
                                            ($scope.onAccept)(item);
                                        }
                                    }
                                }
                                _control.setCaption();
                                $dialog.modal("hide");
                                $scope.$applyAsync();
                            }
                        };
                        $scope.$applyAsync();
                        fnLoadData();
                        $compile($dialog)($scope);
                    }
                });
                $dialog.find(".zb-close-modal").bind("click", function() {
                    $dialog.modal("hide");
                });

                $scope.$watch("initData", function(val) {
                    if (val) {
                        $scope.$selectedItem = val;
                        _control.setValue(val);
                        $scope.$applyAsync();
                    }
                    $scope.$applyAsync();
                });
                $scope.$watch("captionField", function(val) {
                    _control.setCaption();
                    $scope.$applyAsync();
                });
            }
        };
    }
})();