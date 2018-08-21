(function() {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('inputNote', ["$compile", inputNote]);
    
    function inputNote($compile) {
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
                rows: "@"
            },
            template: `
                <textarea rows="4"></textarea>
            `
        };
        return directive;

        function link(scope, element, attrs) {
            $(element).attr("rows", scope.rows);

            $(element).summernote();
        }

       
    }

})();