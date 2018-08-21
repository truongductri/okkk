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

def import_template(args):
    #wb = load_workbook(filename=BytesIO(base64.b64decode(args["data"]["_content"])), data_only=True)
    template_name = args["view"]
    template = list(db.get_collection(KEY.TEMPLATE_COLLECTION).aggregate([{
        '$match': {
            'template': template_name
        }
    }]))
    if len(template) == 0:
        db.get_collection(KEY.TEMPLATE_COLLECTION).insert_one({
            'template': args["view"],
            'file_name': args["data"]["_fileName"],
            'file_content': args["data"]["_content"],
            'file_size': args["data"]["_size"]
        })
    else:
        db.get_collection(KEY.TEMPLATE_COLLECTION).update_one(
        {
            'template': template_name
        },
        { 
            '$set' : {
                'template': args["view"],
                'file_name': args["data"]["_fileName"],
                'file_content': args["data"]["_content"],
                'file_size': args["data"]["_size"]
            }
        })
    return {'data': args["data"]}

