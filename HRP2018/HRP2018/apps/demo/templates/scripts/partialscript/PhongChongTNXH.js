(function (scope) {
    scope.entity = {
        department: "Sở Lao động - Thương binh và xã hội Thành phố Hồ Chí Minh",
        year: "2018",
        period: "6 tháng đầu năm (Báo cáo trước ngày 15/7)", //kỳ báo cáo
        template: "Biểu số 04-BCN: BÁO CÁO CAI NGHIỆN MA TÚY VÀ QUẢN LÝ SAU CAI NGHIỆN CẤP TỈNH",
        file_name: "",
        document: "http://surehcs.vn/DocViewer/Huong-dan-lap-Mau-04-BCN.docx"
    };
    scope.$applyAsync();

    var TEMPLATE_NAME = "PhongChongTNXH";

    function uploadTemplate(file) {
        /*BEGIN UPLOAD FILE*/
        var now = new Date();
        var offset_minutes = now.getTimezoneOffset();
        $.ajax({
            url: ws_get_url(),
            type: "post",
            dataType: "json",
            data: JSON.stringify({
                path: "${get_api_key('app_main.excel.import/import_template')}",
                view: TEMPLATE_NAME,
                data: file,
                offset_minutes: offset_minutes
            }),
            success: function (res) {
                console.log(res);
                scope.entity.file_name = res._fileName;
                scope.$applyAsync();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                var newWindow = window.open();
                var txt = jqXHR.responseText
                while (txt.indexOf(String.fromCharCode(10)) > -1) {
                    txt = txt.replace(String.fromCharCode(10), "<br/>")
                }
                newWindow.document.write(txt);
            }
        });
        /*END UPLOAD FILE*/
    }

    function loadExcelTemplate() {
        var url = window.location.href.split("#")[0] + "/excel_export?template=" + TEMPLATE_NAME;
        //var template_path = url.replace("//excel_export", "/excel_export");
        //http://localhost:8888/lv/demo/excel_export?template=PhongChongTNXH
        var template_path = "http://surehcs.vn/DocViewer/EXCEL_TEMPLATE.xlsx";
        var excelViewer = $("#iframe_ExcelViewer");
        excelViewer.empty();
        var iframe = '<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=' + template_path.trim() + '" style="width: 100%; height: 600px" frameborder="0"></iframe>';
        excelViewer.html(iframe);
    }

    function loadInit() {
        $("#fileUpload").on("change", function (evt) {
            var me = this;
            var inputfile = $(me);
            var file = me.files[0];
            $("#fileUpload").val("");
            var reader = new FileReader();
            reader.onload = function () {
                var arrayBuffer = this.result;
                var array = new Uint8Array(arrayBuffer);

                var _uploadService = new lv.UploadService();
                _uploadService
                    //.setProcessMethod("strApi")
                    .setFileName(file.name)
                    .setContent(array)
                    .setSize(file.size)
                    //.setParams(dataparams)
                    .done(function (res) {
                        uploadTemplate(res);
                    });
            };
            reader.readAsArrayBuffer(file);
        });

        services.api("${get_api_key('app_main.excel.manager/get_template')}")
            .data({
                template_name: TEMPLATE_NAME
            })
            .done()
            .then(function (res) {
                console.log(res);
                scope.entity.file_name = res.file_name;
                scope.$applyAsync();

                loadExcelTemplate(scope.entity.template_path);
            })
    };
    setTimeout(function () {
        //console.log($("#fileUpload"));
        loadExcelTemplate();
    }, 300);

    scope.uploadFile = function () {
        $("#fileUpload").trigger("click");
    };
});