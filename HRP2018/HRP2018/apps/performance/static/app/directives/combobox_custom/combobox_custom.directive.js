(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('inputComboboxCustom', combobox);

    combobox.$inject = ['templateService'];
    
    function combobox(templateService) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            scope: {
                listCode: "@",
                listValue: "=",
                listData: "=",
                currentItem: "=",
                currentItemOther: "=",
                isPushData: "=",
                itemCustom: "=",
            },
            templateUrl: templateService.getTemplatePath('combobox_custom')
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs.hasOwnProperty("required")) {
                $(element).wrap("<span zb-required></span>")
            }
            var btn = element.find('button');
            scope.custom_key = null;
            scope.api_url = templateService.getApiCombobox();
            scope.combobox_info = null;
            scope.removeItem = removeItem;
            scope.item = null;//Single select

            getData(function () { assignDataInit(); });

            btn.click(function () {
                //getData(function () {
                    openDialog(scope.combobox_info.display_name, "directives/combobox/template", function () {
                        setTimeout(function () {
                            $(window).trigger('resize');
                        }, 200)
                    }, "myComboboxDialog");
                //});
            });

            /**
            * Hàm mở dialog
            * @param {string} title Tittle của dialog
            * @param {string} path Đường dẫn file template
            * @param {function} callback Xử lí sau khi gọi dialog
            * @param {string} id Id của form dialog, default = 'myModal'
            */
            function openDialog(title, path, callback, id = "myComboboxDialog") {
                //check tồn tại của form dialog theo id
                if ($('#' + id).length === 0) {
                    scope.headerTitle = title;
                    //Đặt ID cho form dialog
                    dialog(scope, id).url(path).done(function () {
                        callback();
                        //Set draggable cho form dialog
                        $('#' + id).ready(function () {
                            $('#' + id + ' .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                                $('#' + id + ' .modal-dialog').draggable();
                            }).bind('mouseup touchend', function () {
                                $('#' + id + ' .modal-dialog').draggable('destroy');
                            });
                        })
                    });
                }
            }

            /**
             * Hàm get data combobox
             */
            function getData(callback) {
                 /*
                 *      Response data
                 *{
                 *  "data" : [], //Datasource
                 *  "display_name" : "", //Title dialog
                 *  "display_fields" : [], //Cột table
                 *  "value_field" : "", //Cột values được chọc khi check
                 *  "caption_field" : "", //Cột name được hiển thị khi check
                 *  "sorting_field" : [], //Trình tự sort data
                 *  "filter_field" : [], //Cột được where khi search
                 *  "error": "" //Lỗi trả về
                }*/
                services.api(scope.api_url)
                    .data({
                        //parameter at here
                        "key": scope.listCode,
                        "value": scope.listValue,
                        "code": scope.currentItem
                    })
                    .done()
                    .then(function (res) {
                        res.data.items.push(...scope.listData);
                        res.data.total_items += 1;
                        scope.custom_key = res["value_custom"];
                        scope.combobox_info = res;
                        scope.combobox_info.data;
                        if(scope.currentItem)
                            assignDataInit();
                        scope.$applyAsync();

                        if (!scope.combobox_info.error)
                            callback();
                    })
            }

            function assignDataInit() {
                var prop = {};
                prop[scope.combobox_info.value_field] = scope.currentItem ? scope.currentItem : scope.currentItemOther;

                var obj = _.findWhere(scope.combobox_info.data.items, prop);
                if (obj) {
                    scope.item = {
                        "value": obj[scope.combobox_info.value_field],
                        "caption": obj[scope.combobox_info.caption_field]
                    }
                    if (scope.combobox_info.value_custom) {
                        for (var i = 0; i < scope.combobox_info.value_custom.length; i++) {
                            scope.item[scope.combobox_info.value_custom[i]] = obj[scope.combobox_info.value_custom[i]];
                        }
                    }
                    scope.$applyAsync();
                }
            }

            function removeItem() {
                scope.currentItem = null;
                scope.item = null;
                scope.$applyAsync();
            }

            scope.$watch('item', function (val) {
                if (val) {
                    scope.currentItem = val['value'];
                    if (scope.custom_key) {
                        var arr = [];
                        for (var i = 0; i < scope.custom_key.length; i++) {
                            if (val[scope.custom_key[i]]) {
                                var obj = {};
                                obj[scope.custom_key[i]] = val[scope.custom_key[i]];
                                arr.push(obj);
                            }
                        }
                        scope.itemCustom = arr;
                    }
                    scope.$applyAsync();
                }
            });

            scope.$watch('currentItem', function (newVal, oldVal) {
                if (newVal != oldVal) {
                    assignDataInit();
                }
            })

            scope.$watch('listCode', function (val) {
                getData(function () { assignDataInit(); });
            })

        }

    }

})();