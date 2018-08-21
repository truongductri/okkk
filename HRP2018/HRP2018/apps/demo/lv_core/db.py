#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers
import constant as KEY


app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)

def get_collection(collection_name):
    return db_context.db.get_collection(quicky.tenancy.get_schema() + "." + collection_name)


