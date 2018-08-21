import openpyxl
class excel_name_range(object):
    def __init__(self):
        self.name=None
        self.address=None
        self.col = -1
class excel_config(object):
    def __init__(self):
        self.names=[]
        self.data_sheet=None
        self.workbook=None
    def get_data_template(self):
        ret_data ={}
        ret=ret_data
        for x in self.names:
            ret=ret_data
            if x.name.split('.').__len__() ==1:
                ret.update({x.name: (x.name, x.col)})
            else:
                for y in x.name.split('.'):
                    if not ret.has_key(y):
                        if x.name.split('.').index(y)==x.name.split('.').__len__()-1:
                            ret.update({y:(x.name , x.col)})
                        else:
                            ret.update({y:{}})
                            ret=ret[y]
                    else:
                        ret = ret[y]
        return ret_data
    def get_oject_template(self):
        class Obj(object):
            pass
        ret_data =Obj()
        ret=ret_data
        for x in self.names:
            ret=ret_data
            if x.name.split('.').__len__() ==1:
                setattr(ret,x.name, (x.name, x.col))
            else:
                for y in x.name.split('.'):
                    if not hasattr(ret,y):
                        if x.name.split('.').index(y)==x.name.split('.').__len__()-1:
                            setattr(ret,y,(x.name , x.col))
                        else:
                            setattr(ret,y,Obj())
                            ret=getattr(ret,y)
                    else:
                        ret = getattr(ret,y)
        return ret_data
    def extract_data_as_list_of_dict(self):
        def extract_data(sorted_names,tmp_data,rows,row_index):
            data_item = tmp_data.copy()
            for name_item in sorted_names:

                tmp = data_item
                j=0
                for x in range(0,name_item["n_count"]):
                    tmp = tmp[name_item["names"][x]]
                print "name={0},idx={1}".format(name_item, name_item["idx"])
                tmp[name_item["names"][name_item["n_count"]]] = rows[row_index][name_item["idx"]].value
            return data_item

        sorted_names= sorted(self.names,key = lambda x:x.col)
        sorted_names = [{"names":x.name.split('.'),"n_count":x.name.split('.').__len__()-1,"idx":x.col} for x in sorted_names]
        rows = list(self.data_sheet.rows)
        rows_count =rows.__len__()
        ret_data=[]
        tmp_data=self.get_data_template()
        for i in range(1,rows_count):
            yield extract_data(sorted_names,tmp_data,rows,i)
    def extract_data_as_list_of_object(self):
        def extract_data(sorted_names,tmp_data,rows,row_index):
            import copy
            data_item = copy.copy(tmp_data)
            for name_item in sorted_names:

                tmp = data_item
                j=0
                for x in range(0,name_item["n_count"]):
                    tmp =getattr(tmp,name_item["names"][x])
                setattr(tmp,name_item["names"][name_item["n_count"]],rows[row_index][name_item["idx"]].value)
            return data_item

        sorted_names= sorted(self.names,key = lambda x:x.col)
        sorted_names = [{"names":x.name.split('.'),"n_count":x.name.split('.').__len__()-1,"idx":x.col} for x in sorted_names]
        rows = list(self.data_sheet.rows)
        rows_count =rows.__len__()
        ret_data=[]
        tmp_data=self.get_oject_template()
        for i in range(1,rows_count):
            yield extract_data(sorted_names,tmp_data,rows,i)
def load_from_string_64(base64_content):
    import binascii
    import struct
    import base64
    data = base64_content.split("base64,")[1]
    buffer_array = base64.decodestring(data)
    from io import BytesIO
    filename = BytesIO(buffer_array)
    import openpyxl
    from openpyxl import utils
    wb = openpyxl.load_workbook(filename=filename, data_only=True)
    return load_from_workbook(wb)
def load_from_file(file):

    file = open(file, 'rb')
    wb = openpyxl.load_workbook(filename=file)
    ret = load_from_workbook(wb)
    return ret


def load_from_workbook(wb):
    ret = excel_config()
    ws_data = [ws for ws in wb.worksheets if ws.title == "data"]
    if ws_data.__len__() == 0:
        raise (Exception("Invalid workbook. The workbook must contains one worksheet with name is 'data'"))
    ret.workbook = wb
    ret.data_sheet = ws_data[0]
    ret.names = []
    for x in wb.defined_names.definedName:
        from openpyxl.utils import coordinate_from_string, column_index_from_string
        if hasattr(x, "name"):
            item = excel_name_range()
            item.address = x.value
            item.name = x.name
            item.col = column_index_from_string(x.value.split("!")[1].split(":")[0].replace("$", "")) - 1
            ret.names.append(item)
    ret.names = sorted(ret.names, key=lambda x: x.name)
    return ret

