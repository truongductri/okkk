var lv;
(function (lv) {
    var _FormSearch = (function () {
        var __scope;
        var __alias;
        function _FormSearch(scope, alias) {
            __scope = scope;
            __alias = alias;
        }

        _FormSearch.prototype.cancel = function (callback) {
            __scope.$frmSearch[__alias]['event']['cancel'] = callback;
        }

        _FormSearch.prototype.accept = function (callback) {
            __scope.$frmSearch[__alias]['event']['accept'] = callback;
        }
        _FormSearch.prototype.JobWorking = JobWorking;
        _FormSearch.prototype.FactorAppraisal = FactorAppraisal;
        _FormSearch.prototype.KPI = KPI;

        function setConfigFrmSearch(ngModel, title = "", multiCheck = false, prop) {
            ngModel = !ngModel ? {} : ngModel;
            __scope.$frmSearch = {
            };
            __scope.$frmSearch[__alias] = {};
            __scope.$frmSearch[__alias].title = title;
            __scope.$frmSearch[__alias].multi = multiCheck;
            __scope.$frmSearch.alias = __alias;
            __scope.$frmSearch[__alias].prop = prop;
            __scope.$frmSearch[__alias]['event'] = {
                "accept": function () { },
                "cancel": function () { }
            }
        }

        function KPI(ngModel, prop, title, multi) {
            debugger
            var me = this;
            me.title = title;
            me.path = "commons/FormSearch/KPI";
            me.multi = multi;
            me.prop = prop;
            me.openDialog = openDialog(me.title, me.path, function () { });
            setConfigFrmSearch(ngModel, me.title, me.multi, me.prop);
            __scope.$frmSearch[__alias].selected = ngModel[prop];
            __scope.$frmSearch[__alias].setValue = function (val) {
                ngModel[prop] = val;
            }

            return me;
        }

        function JobWorking(ngModel, prop, title, multi) {
            var me = this;
            me.title = title;
            me.path = "commons/FormSearch/JobWorking";
            me.multi = multi;
            me.prop = prop;
            me.openDialog = openDialog(me.title, me.path, function () { });
            setConfigFrmSearch(ngModel, me.title, me.multi, me.prop);
            __scope.$frmSearch[__alias].selected = ngModel[prop];
            __scope.$frmSearch[__alias].setValue = function (val) {
                ngModel[prop] = val;
            }

            return me;
        }

        function FactorAppraisal(ngModel, prop, title, multi) {
            var me = this;
            me.title = title;
            me.path = "commons/FormSearch/FactorAppraisal";
            me.multi = multi;
            me.prop = prop;
            me.openDialog = openDialog(me.title, me.path, function () { });
            setConfigFrmSearch(ngModel, me.title, me.multi, me.prop);
            __scope.$frmSearch[__alias].selected = ngModel[prop];
            __scope.$frmSearch[__alias].setValue = function (val) {
                ngModel[prop] = val;
            }

            return me;
        }

        /**
         * Hàm mở dialog
         * @param {string} title Tittle của dialog
         * @param {string} path Đường dẫn file template
         * @param {function} callback Xử lí sau khi gọi dialog
         */
        function openDialog(title, path, callback) {
            __scope.headerTitle = title;
            dialog(__scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }

        return _FormSearch;
    }());
    lv.FormSearch = function (scope, alias) {
        return new _FormSearch(scope, alias);
    };
})(lv || (lv = {}));
