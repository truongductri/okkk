# -*- coding: utf-8 -*-
from django.http import HttpResponse
#from openpyxl import Workbook
#from openpyxl.writer.excel import save_virtual_workbook
#from openpyxl.worksheet.datavalidation import DataValidation
#from openpyxl.workbook import defined_name
import datetime
import quicky
#from format_worksheet import worksheet_style, format_style 
import constant as KEY 
from demo.lv_core import db
import base64


@quicky.view.template("")
def call(request):
    template_name = request._get_get().get("template")

    template = list(db.get_collection(KEY.TEMPLATE_COLLECTION).aggregate([{
        '$match': {
            'template': template_name
        }
    }]))
    if len(template) > 0:
        template_data = template[0]
        response = HttpResponse(content=base64.b64decode(template_data['file_content']), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=excel_template.xlsx'
        return response
    else:
        return None

