import threading
def set_schema(name):
    setattr(threading.currentThread(), "tenancy_code",name)
def set_schema():
    if hasattr(threading.currentThread(),"tenancy_code"):
        return threading.currentThread().tenancy_code
    else:
        return ""