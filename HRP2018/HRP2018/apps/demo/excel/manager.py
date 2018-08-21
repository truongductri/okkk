from django.http import HttpResponse
import quicky
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import load_workbook
import datetime
import base64
from io import BytesIO
import constant as KEY
from demo.lv_core import db

def get_template(args):
    template = list(db.get_collection(KEY.TEMPLATE_COLLECTION).aggregate([{
        '$match': {
            'template': args["data"]["template_name"]
        }
    }]))
    if len(template) > 0:
        return template[0]
    else:
        return {
            "file_content" : None,
            "file_name" : None,
            "template" : None,
            "file_size" : None
        }

