import sys
import bson
if sys.version_info[0]<=2:
    def is_unicode(txt):
        return type(txt) is unicode
    def to_unicode(txt):
        return unicode(txt)
else:
    def is_unicode(txt):
        return type(txt) is str
    def to_unicode(txt):
        if type(txt) is bson.ObjectId:
            return txt.__str__()
        return str(txt)