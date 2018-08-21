(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('templateRating', rating);

    rating.$inject = ['templateService'];
    
    function rating(templateService) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            replace: true, 
            scope: {
                starWidth: "=",
                ratingValue: "=",
                numStars: "=",
                minValue: "=",
                maxValue: "=",
                currentItem: "=",
                ngClick: "=",
                fullStar: "=",
                halfStar: "=",
                readOnly: "=",
                controlItem: "=",
                extendData: "="
            },
            templateUrl: templateService.getTemplatePath('rating')
        };
        return directive;

        function link(scope, element, attrs) {
            element.find(".rateyo-readonly-widg").rateYo({
                rating: scope.ratingValue ? scope.ratingValue : 0,
                numStars: scope.numStars,
                precision: 2,
                minValue: scope.minValue,
                maxValue: scope.maxValue,
                starWidth: scope.starWidth,
                fullStar: scope.fullStar,
                halfStar: scope.halfStar,
                readOnly: scope.readOnly ? scope.readOnly : false
            }).on("rateyo.change", function (e, data) {
                //console.log(data);
            })

            var $rateYo = $(element).find(".rateyo-readonly-widg").rateYo();
            $(element).find(".rateyo-readonly-widg").click(function () {
                if (!scope.readOnly) {
                    var rating = $rateYo.rateYo("rating");
                    scope.currentItem = rating;
                    if (scope.ngClick) {
                        scope.ngClick(rating, scope.controlItem, scope.extendData);
                    }
                    scope.$applyAsync();
                }
            });

            $(element).find(".rateyo-readonly-widg").rateYo({
                onChange: function (rating, rateYoInstance) {
                    $(this).next().text(rating);
                }
            });

            scope.$watch("dataItem", function (v) {
            });

            //var readOnly = $(".rateyo-readonly-widg").rateYo("option", "spacing"); //returns 10px
            //$(".rateyo-readonly-widg").rateYo("option", "spacing", "5px"); //returns a jQuery Element

            //var normalFill = $("#rateYo").rateYo("option", "fullStar"); //returns true
            //$("#rateYo").rateYo("option", "fullStar", true); //returns a jQuery Element
        }

    }

})();