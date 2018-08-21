(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('formSearch', formSearch);

    formSearch.$inject = ['$window'];
    
    function formSearch ($window) {
        // Usage:
        //     <form-search></form-search>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            template: template(),
            scope: {
                multi: "=",
                initData: "=",
                ngModel: "=",
                ngDisabled: "=",
                ngClear: "&",
                open: "&",
                onRemoveAll: "&"
            }
        };
        return directive;

        function link(scope, element, attrs) {
            scope.placeholder = attrs['placeholder'];
            scope.deleteSelectedItem = deleteSelectedItem;
            scope.displayItems = [];
            scope.displayItem = {};
            scope.clear = clear;

            function deleteSelectedItem(val) {
                var obj = {};
                obj[scope.valueField] = val[scope.valueField];
                scope.ngModel = _.reject(scope.ngModel, function (v) {
                    return v == val[scope.valueField];
                });
                scope.displayItems = _.reject(scope.displayItems, obj);
                scope.initData['value'] = _.reject(scope.initData['value'], obj);
                scope.$applyAsync();
            }

            function clear() {
                scope.ngModel = null;
                assignValue(scope, null);
                scope.ngClear();
                scope.$applyAsync();
            }

            scope.$watch('initData', function (val) {
                if (val) {
                    if(val['value'] &&!val['value'].hasOwnProperty('error'))
                        assignValue(scope, val['value']);
                }
            })

            scope.$watch('ngModel', function (val) {
                if (!val || val.length === 0) {
                    assignValue(scope, null);
                    scope.$applyAsync();
                }
            }, true)
        }

        function assignValue(scope, val) {
            scope.captionField = scope.initData['caption_field'];
            scope.valueField = scope.initData['value_field'];
            if (scope.multi === true) {
                scope.displayItems = val;
            } else {
                scope.displayItem = val;
            }
        }

        function _init_() {
            
        }
    }

    function template() {
        return `
              <div class="zb-form-combobox input-group" ng-if="multi">
                <div class="form-control">
                  <span class="placeholder" ng-if="displayItems.length<=0">{{placeholder}}</span>
                  <div class="display-value">
                        <span class="multi-value" ng-repeat="v in displayItems">
                            {{v[captionField]}}
                            <i class="bowtie-icon bowtie-math-multiply-light" ng-click="deleteSelectedItem(v)"></i>
                        </span>
                  </div>
                </div>
                <div class="zb-combobox-template"></div>
                <div class="input-group-btn">   
                  <button class="btn btn-default zb-combo-btn-clear" ng-disabled="ngDisabled" ng-click="clear()">
                    <i class="bowtie-icon bowtie-edit-remove"></i>
                  </button>
                  <button class="btn btn-default zb-open-modal" ng-disabled="ngDisabled" ng-click="open()">
                    <i class="bowtie-icon bowtie-navigate-external"></i>
                  </button>
                </div>
              </div>
              <div class="zb-form-combobox input-group" ng-if="!multi">
                  <div class="form-control">
                      <span class="placeholder" ng-if="!displayItem">{{ placeholder }}</span>
                      <span class="display-value">{{ displayItem[captionField] }}</span>
                  </div>
                  <div class="zb-combobox-template"></div>
                  <div class="input-group-btn">
                      <button class="btn btn-default zb-combo-btn-clear" ng-disabled="ngDisabled" ng-click="clear()">
                          <i class="bowtie-icon bowtie-edit-remove"></i>
                      </button>
                      <button class="btn btn-default zb-open-modal" ng-disabled="ngDisabled" ng-click="open()">
                          <i class="bowtie-icon bowtie-navigate-external"></i>
                      </button>
                  </div>
              </div>
            `;
    }

})();