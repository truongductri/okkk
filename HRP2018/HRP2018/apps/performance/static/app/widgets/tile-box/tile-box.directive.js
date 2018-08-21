(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('tileBox', collapseBox);

    function collapseBox() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                txtTitle: "@title",
                txtheaderInfo: "@info",
                txtDescription: "@description",
                iWidth: "@width",
                txtIcon: "@icon",
                txtNumber: "@number",
                txtColor: "@color",
                imageUrl: "@image",
                iframeUrl: "@iframe"
            },
            template: `
                <div class="zb-tile-box zb-tile-box-w{{iWidth ? iWidth : 1}}">
                    <div class="zb-tile-header">
                        <span class="zb-tile-header-left">{{txtTitle}}</span>
                        <span class="zb-tile-header-right">{{txtheaderInfo}}</span>
                    </div>
                    <div class="zb-tile-content">
                        <p class="zb-tile-content-description">{{txtDescription}}</p>
                        <div class="zb-tile-content-bottom">
                            <span class="zb-tile-number {{txtColor}}">{{txtNumber}}</span>
                            <span class="zb-tile-icon">
                                <i class="{{txtIcon}}"></i>
                            </span>
                        </div>
                    </div>
                </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr) {
                var header = $(elem).find(".zb-tile-header");
                var headerTitle = $(elem).find(".zb-tile-header-left");
                var headerInfo = $(elem).find(".zb-tile-header-right");
                var contentDescription = $(elem).find(".zb-tile-content-description");

                var content = $(elem).find(".zb-tile-content");
                var contentButton = $(elem).find(".zb-tile-content-bottom");
                var contentNumber = $(elem).find(".zb-tile-content-bottom>.zb-tile-number");
                var contentIcon = $(elem).find(".zb-tile-content-bottom>.zb-tile-icon");

                if ($scope.iframeUrl) {
                    header.remove();
                    content.remove();
                    $(elem).html("<iframe src='" + $scope.iframeUrl + "' width='100%' height='100%' style='border:none'></iframe>");
                } else if ($scope.imageUrl) {
                    header.remove();
                    content.remove();
                    $(elem).html("<img src='" + $scope.imageUrl + "' width='100%' height='100%'/>");
                } else {
                    /*HEADER*/
                    if (!$scope.txtTitle) {
                        header.remove();
                    }

                    if (!$scope.txtheaderInfo) {
                        headerInfo.remove();
                    }

                    if (!$scope.txtDescription) {
                        contentDescription.remove();
                    }
                    /*CONTENT*/
                    if (!$scope.txtIcon && !$scope.txtNumber) {
                        contentButton.remove()
                    } else {
                        if (!$scope.txtIcon) {
                            $scope.txtIcon = "bowtie-icon bowtie-file";
                        }
                    }
                }

                $scope.$applyAsync();
            }
        };
    }
})();