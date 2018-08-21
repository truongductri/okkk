from types import MethodType
class _obj(object):
    pass

def connect(*args,**kwargs):
    from . import database
    ret = _obj()
    ret.db=database.connect(*args,**kwargs)
    ret.collections=_obj()
    def reload(self):
        self.items=self.db.db.collection_names()
    ret.reload=reload
    return ret

