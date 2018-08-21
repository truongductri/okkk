(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('collapseBox', collapseBox);

    function collapseBox() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            // scope: {
            //     txtTitle: "@title",
            //     txtDescription: "@description"
            // },
            template: '' +
                '<div class="zb-collapse-box">' +
                '   <div class="zb-header hcs-zb-header-custom">' +
                '       <div class="zb-header-left hcs-zb-header-left-custom">' +
                '          <div class="zb-header-content hcs-zb-header-content-custom">' +
                '              <span class="zb-header-icon hcs-zb-header-icon-custom">' +
                '                  <i class="bowtie-icon bowtie-chevron-left-light zb-icon-up hcs-zb-icon-up-custom"></i>' +
                /*bowtie-navigate-back-circle*/
                '              </span>' +
                '              <span class="zb-header-number hcs-zb-header-number-custom"></span>' +
                '              <span class="zb-header-title hcs-zb-header-title-custom"></span>' +
                '          </div>' +
                '          <span class="zb-header-description hcs-zb-header-description-custom"></span>' +
                '       </div>' +
                '       <div class="zb-header-right hcs-zb-header-right-custom"></div>' +
                '   </div>' +
                '   <div class="zb-content hcs-zb-content-custom"></div>' +
                '</div>',
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrls, $transclude) {
                var $config = {
                    txtTitle: attr["title"],
                    txtDescription: attr["description"],
                    txtNumber: attr["number"],
                };

                var headerIcon = $(elem).find(".zb-header-icon");
                var headerTitle = $(elem).find(".zb-header-title");
                var headerNumber = $(elem).find(".zb-header-number");
                var headerDescription = $(elem).find(".zb-header-description");
                var content = $(elem).find(".zb-content");

                $transclude($scope, function (nodes) {
                    $.each(nodes, function (i, v) {
                        if (v.tagName && v.tagName.toLowerCase() == "toolbar") {
                            $(elem).find(".zb-header-right").append(v)
                        } else {
                            $(elem).find(".zb-content").append(v);
                        }
                    });
                })

                headerTitle.html($config.txtTitle);
                headerNumber.html($config.txtNumber);
                headerDescription.html($config.txtDescription);
                if (!$config.txtDescription) {
                    headerDescription.remove();
                }

                var _collapse = function () {
                    if (content.is(":hidden")) {
                        headerIcon.find("i").addClass("zb-icon-up");
                        headerIcon.find("i").removeClass("zb-icon-down");
                    } else {
                        headerIcon.find("i").removeClass("zb-icon-up");
                        headerIcon.find("i").addClass("zb-icon-down");
                    }
                    var toggle = content.slideToggle(300);
                }
                headerIcon.bind("click", _collapse);
                headerTitle.bind("click", _collapse);
            }
        };
    }
})();