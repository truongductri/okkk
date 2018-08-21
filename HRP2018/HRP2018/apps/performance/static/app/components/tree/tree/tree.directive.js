(function () {
    'use strict';

    angular.module('ZebraApp.components.trees')
        .directive('treeData', ["$parse", "$getDataTree", treeData]);

    /** @ngInject */
    function treeData($parse, $getDataTree) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                source: "=",
                displayField: "@",
                parentField: "@",
                parentValue: "=",
                keyField: "@",
                iconField: "@",
                checkedField: "@",
                multiSelect: "=",
                selectMode: "=",
                onSelect: "=",
                currentNode: "=",
                selectedNodes: "=",
                selectedRootNodes: "=",
                searchText: "=",
                checkAll: "=",
                disabled: "=",
                expandAll: "@",
                collapseAll: "@",
                selectFirstNode: "@"
            },
            /*
                @: lấy giá trị trên attrs,
                =: function hoặc data trên parent scope (twoway binding)
                &:function hoặc data trên parent scope (oneway binding)
            */
            templateUrl: "app/components/tree/tree/tree.html",
            link: function ($scope, elem, attr) {
                compileTree($scope, elem, attr, $parse, $getDataTree);
            }
        };
    }


    function compileTree($scope, elem, attr, $parse, $getDataTree) {
        var _tree = null;

        function _initLayout() {

            var _selectedNodes = [];
            var _curentNode = {}
            var _dataSource = [];
            var _selectedRootNodes = [];

            if (!$scope.multiSelect) $scope.multiSelect = false;
            if (!$scope.selectMode) $scope.selectMode = 1;

            function _setCurrentNode(nodeData) {
                _curentNode = nodeData;
                $scope.currentNode = _curentNode;
                $scope.$applyAsync();
                if ($scope.onSelect && angular.isFunction($scope.onSelect)) {
                    $scope.onSelect(_curentNode);
                }
            }

            function _setSelectedNodes(selectedNodes, selectedRootNodes) {
                $scope.selectedNodes = selectedNodes;
                $scope.selectedRootNodes = selectedRootNodes;
                $scope.$applyAsync();
                // console.log("selectedNodes:", selectedNodes);
                // console.log("selectedRootNodes:", selectedRootNodes);
            }

            function _setSelectedOnInit($tree) {
                // Get a list of all selected nodes, and convert to a key array:
                var selDatas = $.map($tree.getSelectedNodes(), function (node) {
                    return node.data;
                });
                _selectedNodes = selDatas;
                // Get a list of all selected TOP nodes
                var selRootDatas = $.map($tree.getSelectedNodes(true), function (node) {
                    return node.data;
                });
                _selectedRootNodes = selRootDatas;
                _setSelectedNodes(_selectedNodes, _selectedRootNodes);
            };

            // 1 (radiobutton: single-selection), 2 (multi-selection) , 3 (hierarchical multi-selection)
            if (!$scope.selectMode) {
                $scope.selectMode = 1;
            }

            var _dataSourceTree = $getDataTree($scope);
            //console.log("TREE DIRECTIVE", _dataSourceTree);

            if (_tree) {
                _tree.reload(_dataSourceTree)
            } else {
                //elem.find("#tree").empty();
                elem.find("#tree").fancytree({
                    extensions: ["filter"],
                    quicksearch: true,
                    checkbox: $scope.multiSelect,
                    selectMode: $scope.selectMode, // 1 (radiobutton: single-selection), 2 (multi-selection) , 3 (hierarchical multi-selection)
                    icon: true, //hide icon => hide counter
                    source: _dataSourceTree,
                    filter: {
                        autoApply: true, // Re-apply last filter if lazy data is loaded
                        autoExpand: true, // Expand all branches that contain matches while filtered
                        counter: false, // Show a badge with number of matching child nodes near parent icons
                        fuzzy: false, // Match single characters in order, e.g. 'fb' will match 'FooBar'
                        hideExpandedCounter: false, // Hide counter badge if parent is expanded
                        hideExpanders: false, // Hide expanders if all child nodes are hidden by filter
                        highlight: true, // Highlight matches by wrapping inside <mark> tags
                        leavesOnly: false, // Match end nodes only
                        nodata: true, // Display a 'no data' status node if result is empty
                        mode: "hide" // "dimm" : Grayout unmatched nodes (pass "hide" to remove unmatched node instead)
                    },
                    loadChildren: function (event, data) {
                        if ($scope.iconField) {
                            function _setIconForChildren(node) {
                                var children = node.getChildren();
                                if (children) {
                                    $.each(children, function (i, v) {
                                        //if (!v.isFolder()) {
                                        if (v.data[$scope.iconField]) {
                                            v.icon = v.data[$scope.iconField];
                                        } else {
                                            v.icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYxIDY0LjE0MDk0OSwgMjAxMC8xMi8wNy0xMDo1NzowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNS4xIFdpbmRvd3MiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MjVFNDJDQkQ3MzVFMTFFMUE0RDU5NUZFN0FEQTdCQjYiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MjVFNDJDQkU3MzVFMTFFMUE0RDU5NUZFN0FEQTdCQjYiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoyNUU0MkNCQjczNUUxMUUxQTRENTk1RkU3QURBN0JCNiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyNUU0MkNCQzczNUUxMUUxQTRENTk1RkU3QURBN0JCNiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PvTbUTsAAERzSURBVHja7N15kFxJ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";
                                        }
                                        //}
                                        _setIconForChildren(v);
                                    });
                                }
                            }
                            _setIconForChildren(data.node);
                        }
                    },
                    //select a node
                    activate: function (event, data) {
                        _setCurrentNode(data.node.data);
                    },
                    // lazyLoad: function(event, data) {
                    //     console.log("lazyLoad", event, data);
                    //     //data.result = { url: "ajax-sub2.json" }
                    //     data.result = [ {"title": "New child 1"}, {"title": "New child 2"} ];
                    // },
                    select: function (event, data) {
                        _setSelectedOnInit(data.tree);
                    }
                    // }).on("keydown", function(e){
                    //  var c = String.fromCharCode(e.which);
                    //  if( c === "F" && e.ctrlKey ) {
                    //      elem.find("input#txtSearch").focus();
                    //  }
                });
                var _tree = elem.find("#tree").fancytree("getTree");

                setTimeout(function () {
                    _tree.reload(_dataSourceTree);
                    _setSelectedOnInit(_tree);

                    if (!$scope.selectFirstNode || $scope.selectFirstNode.toLowerCase() != "false") {
                        if (_tree.getRootNode() && _tree.getRootNode().getFirstChild()) {
                            _tree.getRootNode().getFirstChild().setActive(true);
                        }
                    }
                }, 100);

                if ($scope.expandAll) {
                    $scope.$parent[$scope.expandAll] = expandAll;

                    function expandAll(callback) {
                        $(elem).find("#tree").fancytree("getTree").visit(function (node) {
                            node.setExpanded();
                        });
                        if (callback) callback();
                    }
                }

                if ($scope.collapseAll) {
                    $scope.$parent[$scope.collapseAll] = collapseAll;

                    function collapseAll(callback) {
                        $(elem).find("#tree").fancytree("getTree").visit(function (node) {
                            node.setExpanded(false);
                        });
                        if (callback) callback();
                    }
                }
                $scope.$parent.$applyAsync();

                //console.log("_DATASOURCETREE", _dataSourceTree, _tree);
                var existsWatchSelectAll = false;
                if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                    existsWatchSelectAll = _.filter($scope.$$watchers, function (f) {
                        return f.exp == "checkAll"
                    }).length > 0;
                }
                if (!existsWatchSelectAll) {
                    $scope.$watch("checkAll", function (val, old) {
                        if (val == true) {
                            elem.find("#tree").fancytree("getTree").visit(function (node) {
                                node.setSelected(true);
                            });
                        } else {
                            elem.find("#tree").fancytree("getTree").visit(function (node) {
                                node.setSelected(false);
                            });
                        }
                    });
                }


                // elem.find("button#btnResetSearch").click(function(e) {
                //     elem.find("input#txtSearch").val("");
                //     $("span#matches").text("");
                //     _tree.clearFilter();
                // }).attr("disabled", true);

                $scope.searchText = "";
                var existsWatchSearchText = false;
                if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                    existsWatchSearchText = _.filter($scope.$$watchers, function (f) {
                        return f.exp == "searchText"
                    }).length > 0;
                }
                if (!existsWatchSearchText) {
                    $scope.$watch("searchText", function (val, oVal) {
                        var n,
                            //tree = $.ui.fancytree.getTree(),
                            filterFunc = _tree.filterNodes, //$("#branchMode").is(":checked") ? tree.filterBranches : tree.filterNodes,
                            match = val;
                        if (val && val.trim()) {
                            n = filterFunc.call(_tree, val);
                            console.log("Found: (" + n + " matches) for ('" + val + "')");
                        } else {
                            _tree.clearFilter();
                            console.log("Found: (" + 0 + " matches) for ('" + val + "')");
                        }
                        //n = filterFunc.call(_tree, val);

                        // if (e && e.which === $.ui.keyCode.ESCAPE || $.trim(val) === "") {
                        //     $("button#btnResetSearch").click();
                        //     return;
                        // }

                        // if ($("#regex").is(":checked")) {
                        //     <!-- n = filterFunc.call(_tree, function(node) { -->
                        //     <!-- return new RegExp(match, "i").test(node.title); -->
                        //     <!-- }); -->
                        // } else {
                        //     n = filterFunc.call(_tree, match);
                        // }
                    })
                }
                //Nếu thay đổi chạy lại cây
                let _watchInits = ["multiSelect", "selectMode", "disabled"];
                let _isFirstTime = true;
                $.each(_watchInits, function (i, v) {
                    var existsWatchInit = false;
                    if ($scope.$$watchers && Array.isArray($scope.$$watchers)) {
                        existsWatchInit = _.filter($scope.$$watchers, function (f) {
                            return f.exp == v
                        }).length > 0;
                    }
                    if (!existsWatchInit) {
                        $scope.$watch(v, function (val, old) {
                            //alert(v + "-" + _isFirstTime);
                            if (!_isFirstTime) {
                                _initLayout();
                            }
                        }, true);
                    }
                });
                _isFirstTime = false;
            }
        }

        $scope.$watch("source", function (val, old) {
            _initLayout();
        }, true);
    }
})();