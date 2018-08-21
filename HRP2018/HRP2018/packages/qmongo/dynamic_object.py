class dynamic_object(object):
    pass


def create_from_dict(dict_data):
    if type(dict_data) in [str,unicode]:
        return dict_data
    ret = dynamic_object()
    if dict_data == None:
        return None
    for k, v in dict_data.items():
        if type(v) is dict :
            setattr(ret, k, create_from_dict(v))
        elif type(v) is list:
            setattr(ret, k, [create_from_dict(_v) for _v in v])
        else:
            setattr(ret, k, v)
    return ret
def create():
    return dynamic_object()
def create_object_from_fields(fields):
    fields=sorted(fields, key=lambda x: x)
    ret = dynamic_object()
    for x in fields:
        f= x.split('.')
        tmp = ret
        i = 0
        for n in f:
            if not hasattr(tmp,n):
                setattr(tmp,n,None)
            else:
                if i == f.__len__() - 1:
                    setattr(tmp, n, None)
                else:
                    setattr(tmp, n, dynamic_object())
            tmp = getattr(tmp,n)

    return ret
def convert_to_dict(obj):
    if obj == None:
        return None
    ret = {}
    for k, v in obj.__dict__.items():
        if type(v) is list:
            ret.update({
                k:[convert_to_dict(_v) for _v in v]
            })
        elif hasattr(v,"__dict__"):
            ret.update({
                k:convert_to_dict(v)
            })
        else:
            ret.update({
                k: v
            })
    return ret