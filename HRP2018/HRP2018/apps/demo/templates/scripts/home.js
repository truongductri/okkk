(function (scope) {

    scope.handleEvent = handleEvent;
    scope.$functions = scope.$root.$functions;
    scope.handleEvent = new handleEvent();

    /**
     * Handle events in page
     */
    function handleEvent() {

        //Event toggle group function
        this.onCollapse = (id, event) => {
            $("#hcs-body-" + id).slideToggle(400);
            //set css class when clicked header
            var cssClass = $('#icon-' + id).attr('class') == 'la la-angle-down'
                ? 'la la-angle-right'
                : 'la la-angle-down';
            $('#icon-' + id).removeAttr('class');
            $('#icon-' + id).prop('class', cssClass);
        };

        //Close notification
        this.onCloseNotify = ($event) => {
            //$($event.target).parent().parent().parent().fadeOut();
            $($event.target).parent().parent().parent().swipe({
                tap: function (event, target) {
                    alert('tap');
                },
                swipe: function (event, direction, distance, duration, fingerCount) {
                    //Handling swipe direction.
                    $($event.target).parent().parent().parent().hide("slide", { direction: "right" }, "fast");
                }
            });
        }

        this.redirectPage = (child) => {
            if (child.url.indexOf("http://") != -1 || child.url.indexOf("https://") != -1) {
                var win = window.open(child.url, '_blank');
                win.focus();
            } else if (child.url.substring(0, 1) == "/") {
                var win = window.open(child.url, '_blank');
                win.focus();
            } else {
                if (child.parent_id) {
                    if (child.url.trim()) {
                        scope.$root.currentModule = _.filter(scope.$root.$functions, function (d) {
                            return d["function_id"] == child.parent_id;
                        })[0].custom_name.replace("/", " ");
                        scope.$root.currentFunction = child.custom_name;
                    }
                }
                location.href = '#page=' + child.function_id;
            }
        }
    }



    /**
     * ===============================  Implementation - END  ==================================
     */
});