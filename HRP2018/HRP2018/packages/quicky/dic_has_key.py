import sys
if sys.version_info[0] <= 2:
    def dic_has_key(obj,key):
        return obj.has_key(key)
else:
    def dic_has_key(obj,key):
        return obj.__contains__(key)
