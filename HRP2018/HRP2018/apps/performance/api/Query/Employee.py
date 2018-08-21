from .. import models
from .. import common
def get_employee_list_by_department(dept_code, active, page_size, page_index, sort, search):
    #db = common.get_db_context()
    #ret =
    #db.system_js.getEmployeeByDepartmentCode(common.get_current_schema(),
    #"PERF", dept_code, page_size, page_index, sort, search)
    #return ret
    rs = []
    #var lstDepartmentCode = [];
    #departments.forEach(function (el) {
    #    lstDepartmentCode =
    #    lstDepartmentCode.concat(el.level_code.slice(el.level_code.indexOf(departmentCode),
    #    el.level_code.length));
    #});    
    if (active == "0"):
        active = {
            "$match":{"emp.active": {"$eq": True}}  
            }
    elif (active == "1"):
        active = {
                "$match":{"emp.active": {"$ne": True}}  
            }
    else:
        active =  {
            "$match":{"$or":[{"emp.active":{"$ne":True}}, {"emp.active":{"$eq":True}}]} #get all
            }

    rs = list(common.get_collection('SYS_ValueList').aggregate([{ "$match":  { "list_name": "LGender" } },
        { "$unwind": { "path": "$values", "preserveNullAndEmptyArrays": False } },
        { "$lookup": { "from": common.get_collection_name_with_schema("HCSEM_Employees"), "localField": "values.value", "foreignField": "gender", "as": "emp" } },
        { "$unwind": { "path": "$emp", "preserveNullAndEmptyArrays": True } },
        { "$lookup": { "from": common.get_collection_name_with_schema("HCSSYS_Departments"), "localField": "emp.department_code", "foreignField": "department_code", "as": "dept" } },
        { "$unwind": { "path": "$dept", "preserveNullAndEmptyArrays": False } },
        { "$match":  { "dept.level_code": dept_code } },
        active,
        {
            "$project": {
                "full_name": { "$concat": ["$emp.last_name", " ", "$emp.first_name"] },
                "employee_code": "$emp.employee_code",
                "gender": "$values.caption",
                "job_w_code": "$emp.job_w_code",
                "join_date": "$emp.join_date",
                "department_code": "$emp.department_code",
                "department_name": "$dept.department_name",
                "photo_id": "$emp.photo_id",
                "last_name": "$emp.last_name",
                "first_name": "$emp.first_name",
                "extra_name": "$emp.extra_name",
                "birthday": "$emp.birthday",
                "b_province_code": "$emp.b_province_code",
                "nation_code": "$emp.nation_code",
                "ethnic_code": "$emp.ethnic_code",
                "religion_code": "$emp.religion_code",
                "culture_id": "$emp.culture_id",
                "is_retrain": "$emp.is_retrain",
                "train_level_code": "$emp.train_level_code",
                "marital_code": "$emp.marital_code",
                "id_card_no": "$emp.id_card_no",
                "issued_date": "$emp.issued_date",
                "issued_place_code": "$emp.issued_place_code",
                "mobile": "$emp.mobile",
                "p_phone": "$emp.p_phone",
                "email": "$emp.email",
                "personal_email": "$emp.personal_email",
                "document_no": "$emp.document_no",
                "official_date": "$emp.official_date",
                "career_date": "$emp.career_date",
                "personnel_date": "$emp.personnel_date",
                "emp_type_code": "$emp.emp_type_code",
                "labour_type": "$emp.labour_type",
                "job_pos_code": "$emp.job_pos_code",
                "job_pos_date": "$emp.job_pos_date",
                "job_w_date": "$emp.job_w_date",
                "profession_code": "$emp.profession_code",
                "level_management": "$emp.level_management",
                "is_cbcc": "$emp.is_cbcc",
                "is_expert_recruit": "$emp.is_expert_recruit",
                "is_expert_train": "$emp.is_expert_train",
                "manager_code": "$emp.manager_code",
                "manager_sub_code": "$emp.manager_sub_code",
                "user_id": "$emp.user_id",
                "job_pos_hold_code": "$emp.job_pos_hold_code",
                "job_w_hold_code": "$emp.job_w_hold_code",
                "department_code_hold": "$emp.department_code_hold",
                "job_pos_hold_from_date": "$emp.job_pos_hold_from_date",
                "job_pos_hold_to_date": "$emp.job_pos_hold_to_date",
                "end_date": "$emp.end_date",
                "retire_ref_no": "$emp.retire_ref_no",
                "signed_date": "$emp.signed_date",
                "signed_person": "$emp.signed_person",
                "active": "$emp.active",
                "note": "$emp.note",
                "p_address": "$emp.p_address",
                "p_province_code": "$emp.p_province_code",
                "p_district_code": "$emp.p_district_code",
                "p_ward_code": "$emp.p_ward_code",
                "p_hamlet_code": "$emp.p_hamlet_code",
                "t_address": "$emp.t_address",
                "t_province_code": "$emp.t_province_code",
                "t_district_code": "$emp.t_district_code",
                "t_ward_code": "$emp.t_ward_code",
                "t_hamlet_code": "$emp.t_hamlet_code",
                "foreigner": "$emp.foreigner",
                "vn_foreigner": "$emp.vn_foreigner",
                "is_not_reside": "$emp.is_not_reside",
                "fo_working": "$emp.fo_working",
                "fo_permiss": "$emp.fo_permiss",
                "fo_begin_date": "$emp.fo_begin_date",
                "fo_end_date": "$emp.fo_end_date"
            }
        },
        {
            "$match": {
                "$or": [{ "full_name": { "$regex": search, "$options": 'i' } },
                    { "employee_code": { "$regex": search, "$options": 'i' } },
                    { "gender": { "$regex": search, "$options": 'i' } },
                    { "job_w_code": { "$regex": search, "$options": 'i' } },
                    { "join_date": { "$regex": search, "$options": 'i' } },
                    { "department_name": { "$regex": search, "$options": 'i' } }]
            }
        },        
        { "$sort": sort },
        {
            "$facet": {
                "metadata": [{ "$count": "total" }, { "$addFields": { "page_index": page_index, "page_size": page_size } }],
                "data": [{ "$skip": page_size * page_index }, { "$limit": page_size }]
            }
        },
        { "$unwind": { "path": '$metadata', "preserveNullAndEmptyArrays": False } },
        {
            "$project": {
                'page_size': '$metadata.page_size',
                'page_index': '$metadata.page_index',
                'total_items': '$metadata.total',
                'items': '$data',
            }
        }]))

    if len(rs) > 0:
        return rs[0]
    return {
        'page_size': page_size,
        'page_index': page_index,
        'total_items': 0,
        'items': [],
    }

def get_employee_by_employee_code(emp_code):
    ret = {}
    collection = common.get_collection('HCSEM_Employees').aggregate([{"$match":{'employee_code':{'$regex':'^' + emp_code}}},
        {"$lookup":{'from':common.get_collection_name_with_schema('HCSSYS_Departments'), 'localField':'department_code', 'foreignField':'department_code', 'as': 'dept'}},
        {"$unwind":{'path':'$dept', "preserveNullAndEmptyArrays":False}},
        {"$project":{
            "photo_id"                     : 1,
            "employee_code"                : 1,
            "last_name"                    : 1,
            "first_name"                   : 1,
            "extra_name"                   : 1,
            "gender"                       : 1,
            "birthday"                     : 1,
            "b_province_code"              : 1,
            "nation_code"                  : 1,
            "ethnic_code"                  : 1,
            "religion_code"                : 1,
            "culture_id"                   : 1,
            "is_retrain"                   : 1,
            "train_level_code"             : 1,
            "marital_code"                 : 1,
            "id_card_no"                   : 1,
            "issued_date"                  : 1,
            "issued_place_code"            : 1,
            "mobile"                       : 1,
            "p_phone"                      : 1,
            "email"                        : 1,
            "personal_email"               : 1,
            "document_no"                  : 1,
            "join_date"                    : 1,
            "official_date"                : 1,
            "career_date"                  : 1,
            "personnel_date"               : 1,
            "emp_type_code"                : 1,
            "labour_type"                  : 1,
            "department_code"              : 1,
            "department_name"              : "$dept.department_name",
            "job_pos_code"                 : 1,
            "job_pos_date"                 : 1,
            "job_w_code"                   : 1,
            "job_w_date"                   : 1,
            "profession_code"              : 1,
            "level_management"             : 1,
            "is_cbcc"                      : 1,
            "is_expert_recruit"            : 1,
            "is_expert_train"              : 1,
            "manager_code"                 : 1,
            "manager_sub_code"             : 1,
            "user_id"                      : 1,
            "job_pos_hold_code"            : 1,
            "job_w_hold_code"              : 1,
            "department_code_hold"         : 1,
            "job_pos_hold_from_date"       : 1,
            "job_pos_hold_to_date"         : 1,
            "end_date"                     : 1,
            "retire_ref_no"                : 1,
            "signed_date"                  : 1,
            "signed_person"                : 1,
            "active"                       : 1,
            "note"                         : 1,
            "p_address"                    : 1,
            "p_province_code"              : 1,
            "p_district_code"              : 1,
            "p_ward_code"                  : 1,
            "p_hamlet_code"                : 1,
            "t_address"                    : 1,
            "t_province_code"              : 1,
            "t_district_code"              : 1,
            "t_ward_code"                  : 1,
            "t_hamlet_code"                : 1,
            "foreigner"                    : 1,
            "vn_foreigner"                 : 1,
            "is_not_reside"                : 1,
            "fo_working"                   : 1,
            "fo_permiss"                   : 1,
            "fo_begin_date"                : 1,
            "fo_end_date"                  : 1
            }}])

    ret = list(collection)[0]

    return ret