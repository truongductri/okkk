(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('templateDragDrop', dragdrop);

    dragdrop.$inject = ['templateService'];
    
    function dragdrop(templateService) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            scope: {
                limitCondition: "=",
                currentItem: "="
            },
            templateUrl: templateService.getTemplatePath('dragdropfile')
        };
        return directive;

        function link(scope, element, attrs) {
            DropAndDrag(scope, element, attrs);
        }

        function DropAndDrag(scope, element, attrs) {
            var acceptFileType = ['xlsx', 'doc', 'docx', "aif",
                "cda",
                "mid",
                "mp3",
                "mpa",
                "ogg",
                "wav",
                "wma",
                "wpl", "css",
                "html",
                "json",
                "sql",
                "php", "pdf",
                "docx",
                "doc",
                "odt",
                "rtf",
                "txt",
                "tex",
                "wks",
                "wps",
                "wpd", "ai", "ppt", 
                "bmp",
                "gif",
                "ico",
                "jpeg",
                "jpg",
                "png",
                "ps",
                "psd",
                "svg",
                "tiff",
                "tif"]
            var dropzone = new Dropzone('#demo-upload', {
                maxFiles: 1,
                init: function () {
                    var me = this;
                    this.on("maxfilesexceeded", function (file) {
                        this.removeAllFiles();
                        this.addFile(file);
                        readFile(file);
                    });
                    if (scope.currentItem) {
                        var val = scope.currentItem;
                        var mockFile = {
                            name: val.file_name,
                            size: val.file_size,
                            type: val.file_type,
                            thumbnail: val,
                            accepted: true
                        };
                        me.files.push(mockFile);    // add to files array
                        me.emit("addedfile", mockFile);
                        me.emit("thumbnail", mockFile, val.file_thumbnail);
                        me.emit("complete", mockFile);
                    }
                },
                previewTemplate: document.querySelector('#preview-template').innerHTML,
                parallelUploads: 2,
                thumbnailHeight: 32,
                thumbnailWidth: 32,
                maxFilesize: 3,
                filesizeBase: 1000,
                thumbnail: function (file, dataUrl) {
                    if (file.previewElement) {
                        file.previewElement.classList.remove("dz-file-preview");
                        var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
                        for (var i = 0; i < images.length; i++) {
                            var thumbnailElement = images[i];
                            thumbnailElement.alt = file.name;
                            thumbnailElement.src = scope.$root.url_static + dataUrl;
                        }
                        setTimeout(function () { file.previewElement.classList.add("dz-image-preview"); }, 1);
                    }
                },
                error: function (file, errormessage, xhr) {
                    this.removeFile(file);
                    //if (errormessage) {
                    //    alert(errormessage);
                    //}
                },
                errormultiple: null,
                accept: function (file, done) {
                    if (acceptFileType.indexOf(file.name.split('.').pop()) == -1) {
                        this.removeFile(file);
                        alert("Upfile sai");
                    }
                    else { done(); }
                }
            });

            // Now fake the file upload, since GitHub does not handle file uploads
            // and returns a 404

            var minSteps = 6,
                maxSteps = 60,
                timeBetweenSteps = 100,
                bytesPerStep = 100000;

            dropzone.uploadFiles = function (files) {
                var self = this;
                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    readFile(file);
                    var totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));
                    for (var step = 0; step < totalSteps; step++) {
                        var duration = timeBetweenSteps * (step + 1);
                        setTimeout(function (file, totalSteps, step) {
                            return function () {
                                file.upload = {
                                    progress: 100 * (step + 1) / totalSteps,
                                    total: file.size,
                                    bytesSent: (step + 1) * file.size / totalSteps
                                };
                                self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
                                if (file.upload.progress == 100) {
                                    file.status = Dropzone.SUCCESS;
                                    self.emit("success", file, 'success', null);
                                    self.emit("complete", file);
                                    self.processQueue();
                                    //document.getElementsByClassName("dz-success-mark").style.opacity = "1";
                                }
                            };
                        }(file, totalSteps, step), duration);
                    }
                }
            }

            function getExtension(ext, type) {
                debugger
                var url = '';
                switch (ext.toLowerCase()) {
                    case 'docx':
                    case 'doc':
                        url = 'css/icon/doc.png'
                        break;
                    case 'xls':
                    case 'xlsx':
                        url = 'css/icon/xls.png'
                        break;
                    case 'img':
                    case 'jpg':
                        url = 'css/icon/jpg.svg'
                        break;
                    case 'png':
                        url = 'css/icon/png.svg'
                        break;
                    case 'pdf':
                        url = 'css/icon/pdf.svg'
                        break;
                    case 'mp3':
                        url = 'css/icon/mp3.svg'
                        break;
                    case 'mp4':
                        url = 'css/icon/mp4.svg'
                        break;
                    case 'aif':
                    case 'cda':
                    case 'mid':
                    case 'mpa':
                    case 'ogg':
                    case 'wav':
                    case 'wma':
                    case 'wp':
                        url = 'css/icon/mp4.svg'
                        break;
                    case 'bmp':
                    case 'gif':
                    case 'ico':
                    case 'jpeg':
                    case 'ps':
                    case 'svg':
                    case 'tiff':
                    case 'ti':
                        url = 'css/icon/image.svg'
                        break;
                    case 'ppt':
                        url = 'css/icon/ppt.svg'
                        break;
                    case 'ai':
                        url = 'css/icon/ai.svg'
                        break;
                    case 'txt':
                        url = 'css/icon/txt.svg'
                        break;
                    case 'psd':
                        url = 'css/icon/psd.svg'
                        break;
                    default:
                        url = 'css/icon/psd.svg'
                }
                return type == 1 ? scope.$root.url_static + url : url;
            }

            function readFile(file) {
                var reader = new FileReader();
                reader.onload = function () {
                    var obj = {};
                    var dataURL = reader.result;
                    obj.file_name = file.name;
                    obj.file_type = file.type;
                    obj.file_size = file.size;
                    obj.file_data = dataURL;
                    obj.file_extends = file.name.split('.')[1];
                    if (file.previewElement) {
                        file.previewElement.classList.remove("dz-file-preview");
                        var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
                        for (var i = 0; i < images.length; i++) {
                            var thumbnailElement = images[i];
                            thumbnailElement.alt = file.name;
                            thumbnailElement.src = getExtension(file.name.split('.')[1], 1);
                            obj.file_thumbnail = getExtension(file.name.split('.')[1]);
                        }
                        setTimeout(function () { file.previewElement.classList.add("dz-image-preview"); }, 1);
                    }
                    scope.currentItem = obj;
                    scope.$applyAsync();
                };
                reader.readAsDataURL(file);
            }

            function confirm(callback) {
                dropzone.confirm = function (question, accepted, rejected) {
                    if (accepted) {
                        callback();
                    }
                };
            }
        }
    }

})();