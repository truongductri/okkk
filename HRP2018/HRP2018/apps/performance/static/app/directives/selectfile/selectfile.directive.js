(function() {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('inputSelectFile', ["$compile", inputSelectFile]);
    
    function inputSelectFile($compile) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                ngModel: "=",
                rows: "@"
            },
            template: `
                <div class="input-group input-file">
    		        <input type="text" class="form-control hcs-input-choose-file" placeholder='Choose a file...' />			
                    <span class="input-group-btn">
        		        <button class="btn btn-default btn-choose hcs-button-choose-file" type="button">
                            <i class="bowtie-icon bowtie-transfer-upload"></i>
                        </button>
    		        </span>
		        </div>
            `
        };
        return directive;

        function link(scope, element, attrs) {
            var input = $(element).find('input');
            $(element).find('button').on("click", function () {
                var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
                element.click();
                element.change(function () {
                    $(input).val((element.val()).split('\\').pop());
                    var files = $(this)[0].files;
                    if (files) {
                        readFile(files[0], scope);
                    }
                });
            })
        }
        function readFile(file, scope) {
            var reader = new FileReader();
            reader.onload = function () {
                var obj = {};
                var dataURL = reader.result;
                obj.file_name = file.name;
                obj.file_type = file.type;
                obj.file_size = file.size;
                obj.file_data = dataURL;
                obj.file_extends = file.name.split('.')[1];
                scope.ngModel = obj;
                scope.$applyAsync();
            };
            reader.readAsDataURL(file);
        }

       
    }

})();