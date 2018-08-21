(function (scope) {
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;

    function onAdd() {
        alert('add');
    };
    function onEdit() {

    };
    function onDelete() {

    };
    function onImport() {

    };
    function onExport() {

    };
    function onAttach() {

    };
    function onRefresh() {

    };
});