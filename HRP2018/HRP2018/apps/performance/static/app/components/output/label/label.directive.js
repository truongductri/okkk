(function () {
  'use strict';

  angular.module('ZebraApp.components.inputs')
      .directive('outputLabel', outputLabel);

  /** @ngInject */
    function outputLabel() {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        scope: {
            value: "="
        },
        template: '<label class="zb-output-label">{{value}}</label>',
        link: function($scope, elem, attr) {
            if (attr["required"]) {
                $(elem).wrap("<span zb-required></span>")
            }
        }
    };
  }
})();