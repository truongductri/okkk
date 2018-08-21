(function() {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('tagInput', ["$compile", tagInput]);
    
    function tagInput($compile) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                ngModel: "=",
                label: "@"
            },
            template: `
                    <input type="text" tag-input="primary" class="form-control zb-form-input"
                        data-role="tagsinput">
            `
        };
        return directive;

        function link(scope, element, attrs) {
            if (scope.ngModel) {
                $(element).val(scope.ngModel);
            }
            $(element).tagsinput({
                tagClass: 'label label-' + scope.label
            });
        }

       
    }

})();