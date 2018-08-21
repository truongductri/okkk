(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('templateTableGroup', tablegroup);

    tablegroup.$inject = ['templateService'];
    
    function tablegroup(templateService) {
        var directive = {
            link: link,
            restrict: 'EA',
            scope: {
                currentHeader: "=",
                currentItem: "=",
            },
            templateUrl: templateService.getTemplatePath('tablegroup')
        };
        return directive;

        function link(scope, element, attrs) {
            debugger
            // set Gird Layout
            var girdLayout = _.pluck(scope.currentHeader, 'width').join(" ");
            var header = element.find('.lms-table-history-custom-header');
            if (header) {
                header.css({ 'grid-template-columns': girdLayout })
            }
            setInterval(function () {
                var body = element.find('.lms-table-history-custom');
                if (body) {
                    body.css({ 'grid-template-columns': girdLayout })
                }
            })

        }

        function setGirdLayout() {
            return "";
        }
    }

})();