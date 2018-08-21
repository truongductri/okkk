def auto_load(name,file):
    import importlib
    import imp
    import sys
    import os
    mdl= sys.modules[name]
    models = importlib.import_module("qmongo.helpers").models
    for x in os.walk(os.path.dirname(file)).next():
        if type(x) is list:
            for f in x:
                if  f[f.__len__()-3:f.__len__()]==".py":
                    items=f.split(os.sep)
                    file_name=items[items.__len__()-1]
                    module_name = file_name.split('.')[0]
                    if module_name != "__init__":
                        print "auto load import file {0}".format(f)

                        _mdl=importlib.import_module(name+"."+module_name)
                        if hasattr(models,module_name):
                            m= getattr(models,module_name)
                            setattr(mdl, module_name, m)





