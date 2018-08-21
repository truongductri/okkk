(function (scope) {
    scope.$parent.$parent.$parent.onSave = onSave;

    function onSave() {
        alert('onSave');
    };
});