import sys
if sys.version_info[0] <= 2:
    def has_key(obj,key):
        return obj.has_key(key)
else:
    def has_key(obj,key):
        return obj.__contains__(key)